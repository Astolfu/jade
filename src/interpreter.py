"""
Intérprete simple de Jade
Ejecuta programas Jade directamente sin compilar
"""

import sys
import os
from lexer import tokenizar_codigo
from parser import parsear_codigo
from semantic_analyzer import AnalizadorSemantico
from ast_nodes import *
from type_system import *
from token_types import TokenType


class InterpreteJade:
    """Intérprete que ejecuta código Jade directamente"""
    
    def __init__(self, archivo_actual: str = ""):
        self.variables = {}  # Scope global
        self.funciones = {}  # Funciones definidas
        self.valor_retorno = None
        self.debe_retornar = False
        
        # Sistema de módulos
        self.archivo_actual = os.path.abspath(archivo_actual) if archivo_actual else os.getcwd()
        self.archivos_importados = {self.archivo_actual}
    
    def ejecutar_programa(self, programa: Programa):
        """Ejecuta un programa Jade"""
        # Registrar todas las funciones e imports primero
        for decl in programa.declaraciones:
            if isinstance(decl, DeclaracionFuncion):
                self.funciones[decl.nombre] = decl
            elif isinstance(decl, Importar):
                self.ejecutar_importar(decl)
            elif isinstance(decl, DeclaracionEnum):
                # Guardamos la definición del enum en variables globales
                # Usamos un dict simple para representar el Enum en runtime
                # { 'VAL1': 'VAL1', 'VAL2': 'VAL2' }
                enum_dict = {val: val for val in decl.valores}
                self.variables[decl.nombre] = enum_dict
        
        # Ejecutar función main
        if 'main' in self.funciones:
            self.ejecutar_funcion('main', [])
        else:
            print("Error: No se encontró función 'main'")
    
    def ejecutar_importar(self, imp: Importar):
        """Ejecuta una importación"""
        # Resolver ruta absoluta
        dir_actual = os.path.dirname(self.archivo_actual)
        ruta_abs = os.path.abspath(os.path.join(dir_actual, imp.ruta))
        
        # Verificar existencia
        if not os.path.exists(ruta_abs):
            raise FileNotFoundError(f"No se encuentra el módulo '{imp.ruta}'")
            
        # Evitar ciclos y re-importaciones
        if ruta_abs in self.archivos_importados:
            return
        
        self.archivos_importados.add(ruta_abs)
        
        try:
            # Cargar y parsear módulo
            with open(ruta_abs, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            # Importaciones locales
            from lexer import tokenizar_codigo
            from parser import parsear_codigo
            
            tokens = tokenizar_codigo(codigo)
            modulo_ast = parsear_codigo(tokens)
            
            # Ejecutar módulo recursivamente
            interprete_modulo = InterpreteJade(ruta_abs)
            interprete_modulo.archivos_importados = self.archivos_importados
            
            # Registrar funciones del módulo
            for decl in modulo_ast.declaraciones:
                if isinstance(decl, DeclaracionFuncion):
                    interprete_modulo.funciones[decl.nombre] = decl
                elif isinstance(decl, Importar):
                    interprete_modulo.ejecutar_importar(decl)
            
            # Fusionar funciones
            for nombre, func in interprete_modulo.funciones.items():
                if nombre not in self.funciones:
                    self.funciones[nombre] = func
                elif nombre != 'main':
                    pass
                    
        except Exception as e:
            raise RuntimeError(f"Error al importar '{imp.ruta}': {str(e)}")

    def ejecutar_funcion(self, nombre: str, argumentos: list):
        """Ejecuta una función"""
        if nombre not in self.funciones:
            raise NameError(f"Función '{nombre}' no definida")
        
        func = self.funciones[nombre]
        
        # Crear scope local
        scope_anterior = self.variables.copy()
        
        # Asignar parámetros
        for i, (param_nombre, _) in enumerate(func.parametros):
            if i < len(argumentos):
                self.variables[param_nombre] = argumentos[i]
        
        # Ejecutar cuerpo
        self.debe_retornar = False
        for stmt in func.cuerpo:
            self.ejecutar_statement(stmt)
            if self.debe_retornar:
                break
        
        # Restaurar scope
        resultado = self.valor_retorno
        self.valor_retorno = None
        self.debe_retornar = False
        self.variables = scope_anterior
        
        return resultado
    
    def ejecutar_statement(self, stmt: Statement):
        """Ejecuta un statement"""
        if isinstance(stmt, DeclaracionVariable):
            valor = self.evaluar_expresion(stmt.valor_inicial)
            self.variables[stmt.nombre] = valor
        
        elif isinstance(stmt, Asignacion):
            valor = self.evaluar_expresion(stmt.valor)
            self.variables[stmt.nombre] = valor
        
        elif isinstance(stmt, AsignacionIndice):
            objeto = self.evaluar_expresion(stmt.objeto)
            indice = self.evaluar_expresion(stmt.indice)
            valor = self.evaluar_expresion(stmt.valor)
            objeto[indice] = valor
        
        elif isinstance(stmt, Si):
            condicion = self.evaluar_expresion(stmt.condicion)
            if condicion:
                for s in stmt.bloque_entonces:
                    self.ejecutar_statement(s)
                    if self.debe_retornar:
                        return
            elif stmt.bloque_sino:
                for s in stmt.bloque_sino:
                    self.ejecutar_statement(s)
                    if self.debe_retornar:
                        return
        
        elif isinstance(stmt, Mientras):
            while self.evaluar_expresion(stmt.condicion):
                for s in stmt.cuerpo:
                    self.ejecutar_statement(s)
                    if self.debe_retornar:
                        return
        
        elif isinstance(stmt, Para):
            inicio = self.evaluar_expresion(stmt.inicio)
            fin = self.evaluar_expresion(stmt.fin)
            
            for i in range(inicio, fin):
                self.variables[stmt.variable] = i
                for s in stmt.cuerpo:
                    self.ejecutar_statement(s)
                    if self.debe_retornar:
                        return
        
        elif isinstance(stmt, Retornar):
            if stmt.valor:
                self.valor_retorno = self.evaluar_expresion(stmt.valor)
            self.debe_retornar = True
        
        elif isinstance(stmt, ExpresionStatement):
            self.evaluar_expresion(stmt.expresion)
    
    def evaluar_expresion(self, expr: Expresion):
        """Evalúa una expresión"""
        if isinstance(expr, LiteralEntero):
            return expr.valor
        
        elif isinstance(expr, LiteralFlotante):
            return expr.valor
        
        elif isinstance(expr, LiteralTexto):
            return expr.valor
        
        elif isinstance(expr, LiteralBooleano):
            return expr.valor
        
        elif isinstance(expr, LiteralNulo):
            return None
        
        elif isinstance(expr, Identificador):
            if expr.nombre in self.variables:
                return self.variables[expr.nombre]
            raise NameError(f"Variable '{expr.nombre}' no definida")
        
        elif isinstance(expr, ExpresionBinaria):
            izq = self.evaluar_expresion(expr.izquierda)
            der = self.evaluar_expresion(expr.derecha)
            op = expr.operador.valor
            
            if op == '+':
                return izq + der
            elif op == '-':
                return izq - der
            elif op == '*':
                return izq * der
            elif op == '/':
                return izq // der if isinstance(izq, int) else izq / der
            elif op == '%':
                return izq % der
            elif op == '^':
                return izq ** der
            elif op == '==':
                return izq == der
            elif op == '!=':
                return izq != der
            elif op == '<':
                return izq < der
            elif op == '>':
                return izq > der
            elif op == '<=':
                return izq <= der
            elif op == '>=':
                return izq >= der
            elif op == 'y':
                return izq and der
            elif op == 'o':
                return izq or der
        
        elif isinstance(expr, ExpresionUnaria):
            val = self.evaluar_expresion(expr.expresion)
            if expr.operador.tipo == TokenType.MENOS:
                return -val
            elif expr.operador.tipo == TokenType.NO:
                return not val
        
        elif isinstance(expr, LlamadaFuncion):
            return self.ejecutar_llamada(expr)
        
        elif isinstance(expr, LiteralLista):
            return [self.evaluar_expresion(elem) for elem in expr.elementos]
        
        elif isinstance(expr, LiteralMapa):
            return {self.evaluar_expresion(k): self.evaluar_expresion(v) for k, v in expr.pares}
        
        elif isinstance(expr, AccesoIndice):
            objeto = self.evaluar_expresion(expr.objeto)
            indice = self.evaluar_expresion(expr.indice)
            return objeto[indice]
        
        elif isinstance(expr, LlamadaMetodo):
            return self.ejecutar_metodo(expr)
        
        elif isinstance(expr, AccesoPropiedad):
            # Evaluar el objeto (debería ser el dict del Enum)
            objeto = self.evaluar_expresion(expr.objeto)
            
            # Verificar si es un dict (nuestra representación de Enum)
            if isinstance(objeto, dict):
                if expr.propiedad in objeto:
                    return objeto[expr.propiedad]
                raise AttributeError(f"Propiedad '{expr.propiedad}' no encontrada en objeto")
            
            raise TypeError(f"No se puede acceder a propiedad en objeto de tipo {type(objeto)}")
        
        return None
    
    def ejecutar_metodo(self, llamada: LlamadaMetodo):
        """Ejecuta llamada a método de objeto"""
        objeto = self.evaluar_expresion(llamada.objeto)
        args = [self.evaluar_expresion(arg) for arg in llamada.argumentos]
        
        # Métodos de listas
        if isinstance(objeto, list):
            if llamada.nombre_metodo == 'agregar':
                if len(args) != 1:
                    raise TypeError("agregar() requiere 1 argumento")
                objeto.append(args[0])
                return None
            
            elif llamada.nombre_metodo == 'longitud':
                return len(objeto)
            
            elif llamada.nombre_metodo == 'eliminar':
                if len(args) != 1:
                    raise TypeError("eliminar() requiere 1 argumento")
                return objeto.pop(args[0])
            
            elif llamada.nombre_metodo == 'contiene':
                if len(args) != 1:
                    raise TypeError("contiene() requiere 1 argumento")
                return args[0] in objeto
            
            else:
                raise AttributeError(f"Lista no tiene método '{llamada.nombre_metodo}'")
        
        # Métodos de mapas
        elif isinstance(objeto, dict):
            if llamada.nombre_metodo == 'claves':
                return list(objeto.keys())
            
            elif llamada.nombre_metodo == 'valores':
                return list(objeto.values())
            
            elif llamada.nombre_metodo == 'longitud':
                return len(objeto)
            
            elif llamada.nombre_metodo == 'eliminar':
                if len(args) != 1:
                    raise TypeError("eliminar() requiere 1 argumento")
                return objeto.pop(args[0], None)
            
            elif llamada.nombre_metodo == 'contiene':
                if len(args) != 1:
                    raise TypeError("contiene() requiere 1 argumento")
                return args[0] in objeto
            
            else:
                raise AttributeError(f"Mapa no tiene método '{llamada.nombre_metodo}'")
        
        raise TypeError(f"Objeto de tipo {type(objeto)} no soporta métodos")

    def ejecutar_llamada(self, llamada: LlamadaFuncion):
        """Ejecuta llamada a función"""
        # Funciones built-in
        if llamada.nombre == 'mostrar':
            arg = self.evaluar_expresion(llamada.argumentos[0])
            print(arg)
            return None
        
        elif llamada.nombre == 'leer':
            return input()
        
        elif llamada.nombre == 'convertir_a_texto':
            arg = self.evaluar_expresion(llamada.argumentos[0])
            return str(arg)
        
        elif llamada.nombre == 'convertir_a_entero':
            arg = self.evaluar_expresion(llamada.argumentos[0])
            return int(arg)
        
        elif llamada.nombre == 'convertir_a_flotante':
            arg = self.evaluar_expresion(llamada.argumentos[0])
            return float(arg)
        
        # Funciones matemáticas
        elif llamada.nombre == 'abs':
            arg = self.evaluar_expresion(llamada.argumentos[0])
            return abs(arg)
        
        elif llamada.nombre == 'max':
            a = self.evaluar_expresion(llamada.argumentos[0])
            b = self.evaluar_expresion(llamada.argumentos[1])
            return max(a, b)
        
        elif llamada.nombre == 'min':
            a = self.evaluar_expresion(llamada.argumentos[0])
            b = self.evaluar_expresion(llamada.argumentos[1])
            return min(a, b)
        
        # String formatting/interpolation  
        elif llamada.nombre == 'f':
            if len(llamada.argumentos) < 1:
                raise TypeError("f() requiere al menos 1 argumento")
            template = self.evaluar_expresion(llamada.argumentos[0])
            valores = [self.evaluar_expresion(arg) for arg in llamada.argumentos[1:]]
            resultado = template
            for valor in valores:
                resultado = resultado.replace('{}', str(valor), 1)
            return resultado
        # Funciones definidas por usuario
        else:
            args = [self.evaluar_expresion(arg) for arg in llamada.argumentos]
            return self.ejecutar_funcion(llamada.nombre, args)


def main():
    """Función principal del intérprete"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Intérprete de Jade - Ejecuta programas Jade directamente',
        prog='jade-interpreter'
    )
    
    parser.add_argument('archivo', help='Archivo .jde a ejecutar')
    parser.add_argument('--debug', action='store_true',
                       help='Mostrar información de debug')
    
    args = parser.parse_args()
    
    try:
        # Leer archivo
        with open(args.archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        if args.debug:
            print(f">>> Ejecutando {args.archivo}...\n")
        
        # Tokenizar
        tokens = tokenizar_codigo(codigo)
        
        # Parsear
        programa = parsear_codigo(tokens)
        
        # Análisis semántico
        analizador = AnalizadorSemantico()
        analizador.analizar(programa)
        
        if args.debug:
            print(">>> Análisis completado, ejecutando...\n")
        
        # Ejecutar
        interprete = InterpreteJade()
        interprete.ejecutar_programa(programa)
        
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: {args.archivo}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        if args.debug:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
