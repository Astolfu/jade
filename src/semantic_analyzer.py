"""
Analizador semántico para Jade
Verifica tipos, scopes y semántica del programa
"""

from typing import Dict, List, Optional
from ast_nodes import *
from type_system import *
from token_types import TokenType
from builtin_functions import es_funcion_builtin, obtener_funcion_builtin


class TablaSimbolos:
    """Tabla de símbolos para rastrear variables y funciones"""
    
    def __init__(self, padre=None):
        self.simbolos: Dict[str, Tipo] = {}
        self.constantes: set = set()
        self.padre = padre
    
    def definir(self, nombre: str, tipo: Tipo, es_constante=False):
        """Define un símbolo en el scope actual"""
        if nombre in self.simbolos:
            raise NameError(f"Variable '{nombre}' ya está definida en este scope")
        self.simbolos[nombre] = tipo
        if es_constante:
            self.constantes.add(nombre)
    
    def buscar(self, nombre: str) -> Optional[Tipo]:
        """Busca un símbolo en el scope actual y padres"""
        if nombre in self.simbolos:
            return self.simbolos[nombre]
        if self.padre:
            return self.padre.buscar(nombre)
        return None
    
    def es_constante(self, nombre: str) -> bool:
        """Verifica si un símbolo es constante"""
        if nombre in self.constantes:
            return True
        if self.padre:
            return self.padre.es_constante(nombre)
        return False
    
    def crear_hijo(self):
        """Crea un scope hijo"""
        return TablaSimbolos(self)


class AnalizadorSemantico:
    """Analizador semántico que verifica tipos y contexto"""
    
    def __init__(self):
        self.scope_actual = TablaSimbolos()
        self.funciones: Dict[str, tuple] = {}  # nombre -> (params, tipo_retorno)
        self.en_funcion = None  # Nombre de la función actual
        self.en_bucle = False
        self.errores: List[str] = []
    
    def error(self, mensaje: str, nodo=None):
        """Registra un error semántico"""
        if hasattr(nodo, 'token'):
            self.errores.append(
                f"Error semántico en línea {nodo.token.linea}: {mensaje}"
            )
        else:
            self.errores.append(f"Error semántico: {mensaje}")
    
    def analizar(self, programa: Programa):
        """Analiza el programa completo"""
        # Primera pasada: registrar todas las funciones
        for decl in programa.declaraciones:
            if isinstance(decl, DeclaracionFuncion):
                self.registrar_funcion(decl)
        
        # Segunda pasada: analizar cuerpos de funciones
        for decl in programa.declaraciones:
            if isinstance(decl, DeclaracionFuncion):
                self.analizar_funcion(decl)
            elif isinstance(decl, DeclaracionVariable):
                self.analizar_declaracion_variable(decl)
        
        # Verificar que existe función main
        if 'main' not in self.funciones:
            self.error("El programa debe tener una función 'main'")
        
        if self.errores:
            raise SemanticError('\n'.join(self.errores))
    
    def registrar_funcion(self, func: DeclaracionFuncion):
        """Registra una función en la tabla de símbolos global"""
        if func.nombre in self.funciones:
            self.error(f"Función '{func.nombre}' ya está definida", func)
            return
        
        # Crear tipos de parámetros
        tipos_params = []
        for nombre_param, tipo_nombre in func.parametros:
            if tipo_nombre:
                tipo = Tipo.desde_nombre(tipo_nombre)
            else:
                tipo = TIPO_DESCONOCIDO  # Inferir más tarde
            tipos_params.append((nombre_param, tipo))
        
        tipo_retorno = TIPO_DESCONOCIDO
        if func.tipo_retorno:
            tipo_retorno = Tipo.desde_nombre(func.tipo_retorno)
        
        self.funciones[func.nombre] = (tipos_params, tipo_retorno)
    
    def analizar_funcion(self, func: DeclaracionFuncion):
        """Analiza una función"""
        self.en_funcion = func.nombre
        
        # Crear nuevo scope para la función
        self.scope_actual = self.scope_actual.crear_hijo()
        
        # Definir parámetros en el scope
        tipos_params, _ = self.funciones[func.nombre]
        for (nombre, tipo) in tipos_params:
            self.scope_actual.definir(nombre, tipo)
        
        # Analizar cuerpo
        for stmt in func.cuerpo:
            self.analizar_statement(stmt)
        
        # Restaurar scope
        self.scope_actual = self.scope_actual.padre
        self.en_funcion = None
    
    def analizar_statement(self, stmt: Statement):
        """Analiza un statement"""
        if isinstance(stmt, DeclaracionVariable):
            self.analizar_declaracion_variable(stmt)
        elif isinstance(stmt, Asignacion):
            self.analizar_asignacion(stmt)
        elif isinstance(stmt, Si):
            self.analizar_si(stmt)
        elif isinstance(stmt, Mientras):
            self.analizar_mientras(stmt)
        elif isinstance(stmt, Para):
            self.analizar_para(stmt)
        elif isinstance(stmt, Retornar):
            self.analizar_retornar(stmt)
        elif isinstance(stmt, Romper):
            if not self.en_bucle:
                self.error("'romper' solo puede usarse dentro de un bucle", stmt)
        elif isinstance(stmt, Continuar):
            if not self.en_bucle:
                self.error("'continuar' solo puede usarse dentro de un bucle", stmt)
        elif isinstance(stmt, ExpresionStatement):
            self.analizar_expresion(stmt.expresion)
    
    def analizar_declaracion_variable(self, decl: DeclaracionVariable):
        """Analiza declaración de variable"""
        # Inferir tipo del valor inicial
        tipo_valor = self.analizar_expresion(decl.valor_inicial)
        
        # Si se especificó tipo, verificar compatibilidad
        if decl.tipo_dato:
            tipo_declarado = Tipo.desde_nombre(decl.tipo_dato)
            if not puede_convertir(tipo_valor, tipo_declarado):
                self.error(
                    f"No se puede asignar {tipo_valor} a variable de tipo {tipo_declarado}",
                    decl
                )
            tipo_final = tipo_declarado
        else:
            tipo_final = tipo_valor
        
        # Definir variable en scope actual
        self.scope_actual.definir(decl.nombre, tipo_final, decl.es_constante)
    
    def analizar_asignacion(self, asig: Asignacion):
        """Analiza asignación a variable"""
        # Verificar que la variable existe
        tipo_var = self.scope_actual.buscar(asig.nombre)
        if tipo_var is None:
            self.error(f"Variable '{asig.nombre}' no está definida", asig)
            return
        
        # Verificar que no es constante
        if self.scope_actual.es_constante(asig.nombre):
            self.error(f"No se puede asignar a constante '{asig.nombre}'", asig)
        
        # Analizar valor
        tipo_valor = self.analizar_expresion(asig.valor)
        
        # Verificar compatibilidad
        if asig.operador.tipo == TokenType.ASIGNAR:
            if not puede_convertir(tipo_valor, tipo_var):
                self.error(
                    f"No se puede asignar {tipo_valor} a variable de tipo {tipo_var}",
                    asig
                )
    
    def analizar_si(self, si: Si):
        """Analiza statement condicional"""
        # Analizar condición
        tipo_cond = self.analizar_expresion(si.condicion)
        if tipo_cond.tipo_base != TipoDato.BOOLEANO:
            self.error(f"Condición debe ser booleana, no {tipo_cond}", si)
        
        # Analizar bloque entonces
        self.scope_actual = self.scope_actual.crear_hijo()
        for stmt in si.bloque_entonces:
            self.analizar_statement(stmt)
        self.scope_actual = self.scope_actual.padre
        
        # Analizar bloque sino si existe
        if si.bloque_sino:
            self.scope_actual = self.scope_actual.crear_hijo()
            for stmt in si.bloque_sino:
                self.analizar_statement(stmt)
            self.scope_actual = self.scope_actual.padre
    
    def analizar_mientras(self, mientras: Mientras):
        """Analiza bucle mientras"""
        tipo_cond = self.analizar_expresion(mientras.condicion)
        if tipo_cond.tipo_base != TipoDato.BOOLEANO:
            self.error(f"Condición debe ser booleana, no {tipo_cond}", mientras)
        
        self.en_bucle = True
        self.scope_actual = self.scope_actual.crear_hijo()
        for stmt in mientras.cuerpo:
            self.analizar_statement(stmt)
        self.scope_actual = self.scope_actual.padre
        self.en_bucle = False
    
    def analizar_para(self, para: Para):
        """Analiza bucle para"""
        # Analizar expresiones de inicio y fin
        tipo_inicio = self.analizar_expresion(para.inicio)
        tipo_fin = self.analizar_expresion(para.fin)
        
        if tipo_inicio.tipo_base != TipoDato.ENTERO:
            self.error("Valor inicial del bucle 'para' debe ser entero", para)
        if tipo_fin.tipo_base != TipoDato.ENTERO:
            self.error("Valor final del bucle 'para' debe ser entero", para)
        
        # Crear scope con variable de bucle
        self.en_bucle = True
        self.scope_actual = self.scope_actual.crear_hijo()
        self.scope_actual.definir(para.variable, TIPO_ENTERO)
        
        for stmt in para.cuerpo:
            self.analizar_statement(stmt)
        
        self.scope_actual = self.scope_actual.padre
        self.en_bucle = False
    
    def analizar_retornar(self, ret: Retornar):
        """Analiza statement retornar"""
        if not self.en_funcion:
            self.error("'retornar' solo puede usarse dentro de una función", ret)
            return
        
        if ret.valor:
            tipo_valor = self.analizar_expresion(ret.valor)
        else:
            tipo_valor = TIPO_NULO
    
    def analizar_expresion(self, expr: Expresion) -> Tipo:
        """Analiza una expresión y retorna su tipo"""
        tipo_resultado = TIPO_DESCONOCIDO
        
        if isinstance(expr, ExpresionBinaria):
            tipo_resultado = self.analizar_expresion_binaria(expr)
        elif isinstance(expr, ExpresionUnaria):
            tipo_resultado = self.analizar_expresion_unaria(expr)
        elif isinstance(expr, LiteralEntero):
            tipo_resultado = TIPO_ENTERO
        elif isinstance(expr, LiteralFlotante):
            tipo_resultado = TIPO_FLOTANTE
        elif isinstance(expr, LiteralBooleano):
            tipo_resultado = TIPO_BOOLEANO
        elif isinstance(expr, LiteralTexto):
            tipo_resultado = TIPO_TEXTO
        elif isinstance(expr, LiteralNulo):
            tipo_resultado = TIPO_NULO
        elif isinstance(expr, Identificador):
            var_info = self.scope_actual.buscar(expr.nombre)
            if var_info:
                tipo_resultado = var_info
            else:
                self.error(f"Variable no definida: '{expr.nombre}'", expr)
                tipo_resultado = TIPO_DESCONOCIDO
        elif isinstance(expr, LlamadaFuncion):
            tipo_resultado = self.analizar_llamada(expr)
        elif isinstance(expr, LiteralLista):
            tipo_elemento = None
            for elem in expr.elementos:
                tipo_actual = self.analizar_expresion(elem)
                if tipo_elemento is None:
                    tipo_elemento = tipo_actual
                elif tipo_actual != tipo_elemento:
                    # Por ahora permitimos listas heterogéneas como lista[desconocido]
                    tipo_elemento = TIPO_DESCONOCIDO
            
            if tipo_elemento is None:
                tipo_resultado = TipoLista(TIPO_DESCONOCIDO) # Lista vacía
            else:
                tipo_resultado = TipoLista(tipo_elemento)
            
        elif isinstance(expr, LiteralMapa):
            tipo_clave = None
            tipo_valor = None
            
            for k, v in expr.pares:
                t_k = self.analizar_expresion(k)
                t_v = self.analizar_expresion(v)
                
                if tipo_clave is None: tipo_clave = t_k
                elif t_k != tipo_clave: tipo_clave = TIPO_DESCONOCIDO
                
                if tipo_valor is None: tipo_valor = t_v
                elif t_v != tipo_valor: tipo_valor = TIPO_DESCONOCIDO
            
            if tipo_clave is None:
                tipo_resultado = TipoMapa(TIPO_DESCONOCIDO, TIPO_DESCONOCIDO)
            else:
                tipo_resultado = TipoMapa(tipo_clave, tipo_valor)

        elif isinstance(expr, AccesoIndice):
            tipo_obj = self.analizar_expresion(expr.objeto)
            tipo_indice = self.analizar_expresion(expr.indice)
            
            if isinstance(tipo_obj, TipoLista):
                if tipo_indice.tipo_base != TipoDato.ENTERO:
                    self.error(f"Índice de lista debe ser entero, no {tipo_indice}", expr)
                tipo_resultado = tipo_obj.tipo_elemento
            
            elif isinstance(tipo_obj, TipoMapa):
                if tipo_indice != tipo_obj.tipo_clave and tipo_obj.tipo_clave.tipo_base != TipoDato.DESCONOCIDO:
                     # Permitir si es compatible (ej. int -> float? no para claves)
                     if tipo_indice.tipo_base != TipoDato.DESCONOCIDO:
                        self.error(f"Clave de mapa debe ser {tipo_obj.tipo_clave}, no {tipo_indice}", expr)
                tipo_resultado = tipo_obj.tipo_valor
            
            else:
                tipo_resultado = TIPO_DESCONOCIDO
            
        elif isinstance(expr, LlamadaMetodo):
            tipo_resultado = self.analizar_metodo(expr)
            
        else:
            tipo_resultado = TIPO_DESCONOCIDO
            
        # Adjuntar tipo al nodo AST para uso posterior (codegen)
        expr.tipo = tipo_resultado
        return tipo_resultado

    def analizar_metodo(self, llamada: LlamadaMetodo) -> Tipo:
        """Analiza llamada a método"""
        tipo_obj = self.analizar_expresion(llamada.objeto)
        
        # Analizar argumentos
        for arg in llamada.argumentos:
            self.analizar_expresion(arg)
        
        if tipo_obj.tipo_base == TipoDato.LISTA:
            if llamada.nombre_metodo == 'agregar':
                if len(llamada.argumentos) != 1:
                    self.error("Método 'agregar' requiere 1 argumento", llamada)
                return TIPO_NULO
            
            elif llamada.nombre_metodo == 'longitud':
                if len(llamada.argumentos) != 0:
                    self.error("Método 'longitud' no acepta argumentos", llamada)
                return TIPO_ENTERO
            
            elif llamada.nombre_metodo == 'eliminar':
                if len(llamada.argumentos) != 1:
                    self.error("Método 'eliminar' requiere 1 argumento", llamada)
                return tipo_obj.tipo_elemento if isinstance(tipo_obj, TipoLista) else TIPO_DESCONOCIDO
            
            elif llamada.nombre_metodo == 'contiene':
                if len(llamada.argumentos) != 1:
                    self.error("Método 'contiene' requiere 1 argumento", llamada)
                return TIPO_BOOLEANO
            
            else:
                self.error(f"Lista no tiene método '{llamada.nombre_metodo}'", llamada)
                return TIPO_DESCONOCIDO
        
        elif tipo_obj.tipo_base == TipoDato.MAPA:
            if llamada.nombre_metodo == 'claves':
                if len(llamada.argumentos) != 0:
                    self.error("Método 'claves' no acepta argumentos", llamada)
                return TipoLista(tipo_obj.tipo_clave if isinstance(tipo_obj, TipoMapa) else TIPO_DESCONOCIDO)
            
            elif llamada.nombre_metodo == 'valores':
                if len(llamada.argumentos) != 0:
                    self.error("Método 'valores' no acepta argumentos", llamada)
                return TipoLista(tipo_obj.tipo_valor if isinstance(tipo_obj, TipoMapa) else TIPO_DESCONOCIDO)
            
            elif llamada.nombre_metodo == 'longitud':
                if len(llamada.argumentos) != 0:
                    self.error("Método 'longitud' no acepta argumentos", llamada)
                return TIPO_ENTERO
            
            elif llamada.nombre_metodo == 'eliminar':
                if len(llamada.argumentos) != 1:
                    self.error("Método 'eliminar' requiere 1 argumento", llamada)
                return tipo_obj.tipo_valor if isinstance(tipo_obj, TipoMapa) else TIPO_DESCONOCIDO
            
            elif llamada.nombre_metodo == 'contiene':
                if len(llamada.argumentos) != 1:
                    self.error("Método 'contiene' requiere 1 argumento", llamada)
                return TIPO_BOOLEANO
            
            else:
                self.error(f"Mapa no tiene método '{llamada.nombre_metodo}'", llamada)
                return TIPO_DESCONOCIDO
        
        self.error(f"Tipo {tipo_obj} no soporta métodos", llamada)
        return TIPO_DESCONOCIDO
    
    def analizar_expresion_binaria(self, expr: ExpresionBinaria) -> Tipo:
        """Analiza expresión binaria"""
        tipo_izq = self.analizar_expresion(expr.izquierda)
        tipo_der = self.analizar_expresion(expr.derecha)
        
        operador = expr.operador.valor
        tipo_resultado = inferir_tipo_binario(tipo_izq, operador, tipo_der)
        
        if tipo_resultado.tipo_base == TipoDato.DESCONOCIDO:
            self.error(
                f"Operador '{operador}' no válido para tipos {tipo_izq} y {tipo_der}",
                expr
            )
        
        return tipo_resultado
    
    def analizar_expresion_unaria(self, expr: ExpresionUnaria) -> Tipo:
        """Analiza expresión unaria"""
        tipo_expr = self.analizar_expresion(expr.expresion)
        
        if expr.operador.tipo == TokenType.MENOS:
            if not tipo_expr.es_numerico():
                self.error(f"Operador '-' no válido para tipo {tipo_expr}", expr)
            return tipo_expr
        elif expr.operador.tipo == TokenType.NO:
            if tipo_expr.tipo_base != TipoDato.BOOLEANO:
                self.error(f"Operador 'no' requiere tipo booleano, no {tipo_expr}", expr)
            return TIPO_BOOLEANO
        
        return TIPO_DESCONOCIDO
    
    def analizar_llamada(self, llamada: LlamadaFuncion) -> Tipo:
        """Analiza llamada a función"""
        # Verificar si es función built-in
        if es_funcion_builtin(llamada.nombre):
            builtin = obtener_funcion_builtin(llamada.nombre)
            
            # Verificar número de argumentos (más permisivo para built-ins)
            if builtin.nombre != 'convertir_a_texto':  # Esta acepta cualquier tipo
                if len(llamada.argumentos) != len(builtin.parametros):
                    self.error(
                        f"Función '{llamada.nombre}' espera {len(builtin.parametros)} argumentos, "
                        f"pero se pasaron {len(llamada.argumentos)}",
                        llamada
                    )
            
            # Analizar argumentos
            for arg in llamada.argumentos:
                self.analizar_expresion(arg)
            
            return builtin.tipo_retorno
        
        # Verificar funciones definidas por usuario
        if llamada.nombre not in self.funciones:
            self.error(f"Función '{llamada.nombre}' no está definida", llamada)
            return TIPO_DESCONOCIDO
        
        tipos_params, tipo_retorno = self.funciones[llamada.nombre]
        
        # Verificar número de argumentos
        if len(llamada.argumentos) != len(tipos_params):
            self.error(
                f"Función '{llamada.nombre}' espera {len(tipos_params)} argumentos, "
                f"pero se pasaron {len(llamada.argumentos)}",
                llamada
            )
        
        # Analizar argumentos
        for arg in llamada.argumentos:
            self.analizar_expresion(arg)
        
        return tipo_retorno


class SemanticError(Exception):
    """Excepción para errores semánticos"""
    pass
