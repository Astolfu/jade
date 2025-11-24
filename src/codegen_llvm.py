"""
Generador de código LLVM IR para Jade
Traduce el AST a LLVM IR usando llvmlite
"""

from llvmlite import ir
from llvmlite import binding as llvm
from ast_nodes import *
from type_system import *
from builtin_functions import FUNCIONES_BUILTIN
import sys


class GeneradorLLVM:
    """Generador de código LLVM IR"""
    
    def __init__(self):
        # Módulo LLVM
        self.module = ir.Module(name="jade_module")
        self.module.triple = llvm.get_default_triple()
        
        # Builder para instrucciones
        self.builder = None
        
        # Tablas de símbolos
        self.variables = {}  # nombre -> alloca
        self.funciones = {}  # nombre -> ir.Function
        
        # Tipos LLVM
        self.tipos_llvm = {
            TipoDato.ENTERO: ir.IntType(64),
            TipoDato.FLOTANTE: ir.DoubleType(),
            TipoDato.BOOLEANO: ir.IntType(1),
            TipoDato.TEXTO: ir.IntType(8).as_pointer(),  # char*
            TipoDato.NULO: ir.VoidType(),
        }
        
        # Función actual
        self.funcion_actual = None
        
        # Declarar funciones del runtime
        self._declarar_runtime()
    
    def _declarar_runtime(self):
        """Declara funciones del runtime de C"""
        # void jade_mostrar(const char* texto)
        fnty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer()])
        self.runtime_mostrar = ir.Function(self.module, fnty, name="jade_mostrar")
        
        # char* jade_leer()
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [])
        self.runtime_leer = ir.Function(self.module, fnty, name="jade_leer")
        
        # char* jade_convertir_a_texto_entero(int64_t n)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(64)])
        self.runtime_conv_entero = ir.Function(self.module, fnty, name="jade_convertir_a_texto_entero")
        
        # char* jade_convertir_a_texto_flotante(double n)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.DoubleType()])
        self.runtime_conv_flotante = ir.Function(self.module, fnty, name="jade_convertir_a_texto_flotante")
        
        # void jade_init_runtime()
        fnty = ir.FunctionType(ir.VoidType(), [])
        self.runtime_init = ir.Function(self.module, fnty, name="jade_init_runtime")
        
        # char* jade_concatenar(const char* a, const char* b)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
        self.runtime_concatenar = ir.Function(self.module, fnty, name="jade_concatenar")
        
        # Listas
        # JadeList* jade_lista_nueva()
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [])
        self.runtime_lista_nueva = ir.Function(self.module, fnty, name="jade_lista_nueva")
        
        # void jade_lista_agregar(JadeList* lista, void* elemento)
        fnty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
        self.runtime_lista_agregar = ir.Function(self.module, fnty, name="jade_lista_agregar")
        
        # void* jade_lista_obtener(JadeList* lista, int64_t indice)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(8).as_pointer(), ir.IntType(64)])
        self.runtime_lista_obtener = ir.Function(self.module, fnty, name="jade_lista_obtener")
        
        # void jade_lista_asignar(JadeList* lista, int64_t indice, void* valor)
        fnty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer(), ir.IntType(64), ir.IntType(8).as_pointer()])
        self.runtime_lista_asignar = ir.Function(self.module, fnty, name="jade_lista_asignar")
        
        # int64_t jade_lista_longitud(JadeList* lista)
        fnty = ir.FunctionType(ir.IntType(64), [ir.IntType(8).as_pointer()])
        self.runtime_lista_longitud = ir.Function(self.module, fnty, name="jade_lista_longitud")
        
        # void* jade_lista_eliminar(JadeList* lista, int64_t indice)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(8).as_pointer(), ir.IntType(64)])
        self.runtime_lista_eliminar = ir.Function(self.module, fnty, name="jade_lista_eliminar")
        
        # int jade_lista_contiene(JadeList* lista, void* elemento)
        fnty = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
        self.runtime_lista_contiene = ir.Function(self.module, fnty, name="jade_lista_contiene")
        
        # Mapas
        # JadeMap* jade_mapa_nuevo()
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [])
        self.runtime_mapa_nuevo = ir.Function(self.module, fnty, name="jade_mapa_nuevo")
        
        # void jade_mapa_asignar(JadeMap* mapa, void* clave, void* valor)
        fnty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
        self.runtime_mapa_asignar = ir.Function(self.module, fnty, name="jade_mapa_asignar")
        
        # void* jade_mapa_obtener(JadeMap* mapa, void* clave)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
        self.runtime_mapa_obtener = ir.Function(self.module, fnty, name="jade_mapa_obtener")
        
        # void* jade_mapa_eliminar(JadeMap* mapa, void* clave)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
        self.runtime_mapa_eliminar = ir.Function(self.module, fnty, name="jade_mapa_eliminar")
        
        # int jade_mapa_contiene(JadeMap* mapa, void* clave)
        fnty = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer()])
        self.runtime_mapa_contiene = ir.Function(self.module, fnty, name="jade_mapa_contiene")
        
        # int64_t jade_mapa_longitud(JadeMap* mapa)
        fnty = ir.FunctionType(ir.IntType(64), [ir.IntType(8).as_pointer()])
        self.runtime_mapa_longitud = ir.Function(self.module, fnty, name="jade_mapa_longitud")
        
        # JadeList* jade_mapa_claves(JadeMap* mapa)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(8).as_pointer()])
        self.runtime_mapa_claves = ir.Function(self.module, fnty, name="jade_mapa_claves")
        
        # JadeList* jade_mapa_valores(JadeMap* mapa)
        fnty = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(8).as_pointer()])
        self.runtime_mapa_valores = ir.Function(self.module, fnty, name="jade_mapa_valores")
    
    def obtener_tipo_llvm(self, tipo: Tipo) -> ir.Type:
        """Convierte un tipo Jade a tipo LLVM"""
        return self.tipos_llvm.get(tipo.tipo_base, ir.IntType(64))
    
    def generar(self, programa: Programa) -> str:
        """Genera código LLVM IR para todo el programa"""
        # Generar declaraciones de funciones primero
        for decl in programa.declaraciones:
            if isinstance(decl, DeclaracionFuncion):
                self._declarar_funcion(decl)
        
        # Generar cuerpos de funciones
        for decl in programa.declaraciones:
            if isinstance(decl, DeclaracionFuncion):
                self._generar_funcion(decl)
        
        # Crear función de entrada que llama a main
        self._generar_entry_point()
        
        return str(self.module)
    
    def _declarar_funcion(self, func: DeclaracionFuncion):
        """Declara una función (firma solamente)"""
        # Determinar tipos de parámetros
        tipos_params = []
        for nombre, tipo_nombre in func.parametros:
            if tipo_nombre:
                tipo = Tipo.desde_nombre(tipo_nombre)
                tipos_params.append(self.obtener_tipo_llvm(tipo))
            else:
                # Por defecto i64
                tipos_params.append(ir.IntType(64))
        
        # Tipo de retorno
        if func.tipo_retorno:
            tipo_ret = self.obtener_tipo_llvm(Tipo.desde_nombre(func.tipo_retorno))
        else:
            # Inferir tipo de retorno: si tiene retornar con valor, usar i64
            tipo_ret = self._inferir_tipo_retorno(func.cuerpo)
        
        # Crear función
        fnty = ir.FunctionType(tipo_ret, tipos_params)
        fn = ir.Function(self.module, fnty, name=func.nombre)
        
        # Nombrar parámetros
        for i, (nombre_param, _) in enumerate(func.parametros):
            fn.args[i].name = nombre_param
        
        self.funciones[func.nombre] = fn
    
    def _inferir_tipo_retorno(self, cuerpo: List[Statement]):
        """Infiere el tipo de retorno de una función basándose en su cuerpo"""
        for stmt in cuerpo:
            if isinstance(stmt, Retornar) and stmt.valor:
                # Si hay un retornar con valor, asumir i64
                return ir.IntType(64)
            elif isinstance(stmt, Si):
                # Buscar en bloques if
                tipo_entonces = self._inferir_tipo_retorno(stmt.bloque_entonces)
                if tipo_entonces != ir.VoidType():
                    return tipo_entonces
                if stmt.bloque_sino:
                    tipo_sino = self._inferir_tipo_retorno(stmt.bloque_sino)
                    if tipo_sino != ir.VoidType():
                        return tipo_sino
            elif isinstance(stmt, Mientras):
                tipo = self._inferir_tipo_retorno(stmt.cuerpo)
                if tipo != ir.VoidType():
                    return tipo
            elif isinstance(stmt, Para):
                tipo = self._inferir_tipo_retorno(stmt.cuerpo)
                if tipo != ir.VoidType():
                    return tipo
        return ir.VoidType()
    
    def _generar_funcion(self, func: DeclaracionFuncion):
        """Genera el cuerpo de una función"""
        fn = self.funciones[func.nombre]
        self.funcion_actual = fn
        
        # Crear bloque de entrada
        bloque_entrada = fn.append_basic_block("entry")
        self.builder = ir.IRBuilder(bloque_entrada)
        
        # Crear nuevo scope de variables
        self.variables = {}
        
        # Asignar parámetros a variables locales
        for i, (nombre_param, tipo_nombre) in enumerate(func.parametros):
            if tipo_nombre:
                tipo = Tipo.desde_nombre(tipo_nombre)
                tipo_llvm = self.obtener_tipo_llvm(tipo)
            else:
                tipo_llvm = ir.IntType(64)
            
            # Crear alloca para el parámetro
            alloca = self.builder.alloca(tipo_llvm, name=nombre_param)
            self.builder.store(fn.args[i], alloca)
            self.variables[nombre_param] = alloca
        
        # Generar cuerpo
        tiene_retorno = False
        for stmt in func.cuerpo:
            if isinstance(stmt, Retornar):
                tiene_retorno = True
            self._generar_statement(stmt)
        
        # Si no hay retorno explícito, agregar ret void
        if not tiene_retorno and isinstance(fn.return_value.type, ir.VoidType):
            self.builder.ret_void()
        
        self.funcion_actual = None

    def _generar_entry_point(self):
        """Genera función principal que inicializa runtime y llama a main"""
        # int _jade_main() que llama a jade main()
        fnty = ir.FunctionType(ir.IntType(32), [])
        c_main_fn = ir.Function(self.module, fnty, name="_jade_main")
        
        bloque = c_main_fn.append_basic_block("entry")
        builder = ir.IRBuilder(bloque)
        
        # Llamar a jade_init_runtime()
        builder.call(self.runtime_init, [])
        
        # Llamar a la función main de Jade si existe
        if "main" in self.funciones:
            builder.call(self.funciones["main"], [])
        
        # Retornar 0
        builder.ret(ir.Constant(ir.IntType(32), 0))

    def _generar_statement(self, stmt: Statement):
        """Genera código para un statement"""
        if isinstance(stmt, DeclaracionVariable):
            self._generar_declaracion_variable(stmt)
        elif isinstance(stmt, Asignacion):
            self._generar_asignacion(stmt)
        elif isinstance(stmt, AsignacionIndice):
            self._generar_asignacion_indice(stmt)
        elif isinstance(stmt, Si):
            self._generar_si(stmt)
        elif isinstance(stmt, Mientras):
            self._generar_mientras(stmt)
        elif isinstance(stmt, Para):
            self._generar_para(stmt)
        elif isinstance(stmt, Retornar):
            self._generar_retornar(stmt)
        elif isinstance(stmt, ExpresionStatement):
            self._generar_expresion(stmt.expresion)
    
    def _generar_declaracion_variable(self, decl: DeclaracionVariable):
        """Genera código para declaración de variable"""
        # Evaluar valor inicial
        valor = self._generar_expresion(decl.valor_inicial)
        
        # Verificar si el valor es void
        if str(valor.type) == 'void':
            # Si es void, no podemos crear una variable con ese valor
            return
        
        # Crear alloca para la variable
        alloca = self.builder.alloca(valor.type, name=decl.nombre)
        self.builder.store(valor, alloca)
        
        # Guardar en tabla de símbolos
        self.variables[decl.nombre] = alloca
    
    def _generar_asignacion(self, asig: Asignacion):
        """Genera código para asignación"""
        valor = self._generar_expresion(asig.valor)
        alloca = self.variables.get(asig.nombre)
        if alloca:
            self.builder.store(valor, alloca)
            
    def _generar_asignacion_indice(self, stmt: AsignacionIndice):
        """Genera código para asignación a índice: arr[i] = val"""
        objeto = self._generar_expresion(stmt.objeto)
        indice = self._generar_expresion(stmt.indice)
        valor = self._generar_expresion(stmt.valor)
        
        val_ptr = self._cast_to_void_ptr(valor)
        
        # Usar info de tipos
        tipo_obj = getattr(stmt.objeto, 'tipo', None)
        es_mapa = False
        
        if tipo_obj and isinstance(tipo_obj, TipoMapa):
            es_mapa = True
        elif tipo_obj and isinstance(tipo_obj, TipoLista):
            es_mapa = False
        else:
            # Fallback
            if str(indice.type) == 'i8*':
                es_mapa = True
            
        if es_mapa:
            indice_ptr = self._cast_to_void_ptr(indice)
            self.builder.call(self.runtime_mapa_asignar, [objeto, indice_ptr, val_ptr])
        else:
            if str(indice.type) != 'i64':
                 indice = self.builder.zext(indice, ir.IntType(64))
            self.builder.call(self.runtime_lista_asignar, [objeto, indice, val_ptr])
    
    def _generar_si(self, si: Si):
        """Genera código para condicional si/entonces/sino"""
        # Evaluar condición
        cond = self._generar_expresion(si.condicion)
        
        # Crear bloques
        bloque_entonces = self.funcion_actual.append_basic_block("then")
        bloque_sino = self.funcion_actual.append_basic_block("else") if si.bloque_sino else None
        bloque_merge = self.funcion_actual.append_basic_block("merge")
        
        # Branch condicional
        if bloque_sino:
            self.builder.cbranch(cond, bloque_entonces, bloque_sino)
        else:
            self.builder.cbranch(cond, bloque_entonces, bloque_merge)
        
        # Generar bloque entonces
        self.builder.position_at_end(bloque_entonces)
        for stmt in si.bloque_entonces:
            self._generar_statement(stmt)
        if not self.builder.block.is_terminated:
            self.builder.branch(bloque_merge)
        
        # Generar bloque sino si existe
        if bloque_sino:
            self.builder.position_at_end(bloque_sino)
            for stmt in si.bloque_sino:
                self._generar_statement(stmt)
            if not self.builder.block.is_terminated:
                self.builder.branch(bloque_merge)
        
        # Continuar en bloque merge
        self.builder.position_at_end(bloque_merge)
    
    def _generar_mientras(self, mientras: Mientras):
        """Genera código para bucle mientras"""
        bloque_cond = self.funcion_actual.append_basic_block("while.cond")
        bloque_body = self.funcion_actual.append_basic_block("while.body")
        bloque_end = self.funcion_actual.append_basic_block("while.end")
        
        # Saltar a condición
        self.builder.branch(bloque_cond)
        
        # Bloque de condición
        self.builder.position_at_end(bloque_cond)
        cond = self._generar_expresion(mientras.condicion)
        self.builder.cbranch(cond, bloque_body, bloque_end)
        
        # Bloque del cuerpo
        self.builder.position_at_end(bloque_body)
        for stmt in mientras.cuerpo:
            self._generar_statement(stmt)
        if not self.builder.block.is_terminated:
            self.builder.branch(bloque_cond)
        
        # Continuar después del bucle
        self.builder.position_at_end(bloque_end)
    
    def _generar_para(self, para: Para):
        """Genera código para bucle para"""
        # Crear variable de iteración
        iter_alloca = self.builder.alloca(ir.IntType(64), name=para.variable)
        inicio = self._generar_expresion(para.inicio)
        fin = self._generar_expresion(para.fin)
        self.builder.store(inicio, iter_alloca)
        self.variables[para.variable] = iter_alloca
        
        # Bloques
        bloque_cond = self.funcion_actual.append_basic_block("for.cond")
        bloque_body = self.funcion_actual.append_basic_block("for.body")
        bloque_inc = self.funcion_actual.append_basic_block("for.inc")
        bloque_end = self.funcion_actual.append_basic_block("for.end")
        
        self.builder.branch(bloque_cond)
        
        # Condición: i < fin
        self.builder.position_at_end(bloque_cond)
        i_val = self.builder.load(iter_alloca)
        cond = self.builder.icmp_signed('<', i_val, fin)
        self.builder.cbranch(cond, bloque_body, bloque_end)
        
        # Cuerpo
        self.builder.position_at_end(bloque_body)
        for stmt in para.cuerpo:
            self._generar_statement(stmt)
        self.builder.branch(bloque_inc)
        
        # Incremento
        self.builder.position_at_end(bloque_inc)
        i_val = self.builder.load(iter_alloca)
        i_inc = self.builder.add(i_val, ir.Constant(ir.IntType(64), 1))
        self.builder.store(i_inc, iter_alloca)
        self.builder.branch(bloque_cond)
        
        # Fin
        self.builder.position_at_end(bloque_end)
    
    def _generar_retornar(self, ret: Retornar):
        """Genera código para retorno"""
        if ret.valor:
            valor = self._generar_expresion(ret.valor)
            self.builder.ret(valor)
        else:
            self.builder.ret_void()
    
    def _generar_expresion(self, expr: Expresion):
        """Genera código para una expresión"""
        if isinstance(expr, LiteralEntero):
            return ir.Constant(ir.IntType(64), expr.valor)
        
        elif isinstance(expr, LiteralFlotante):
            return ir.Constant(ir.DoubleType(), expr.valor)
        
        elif isinstance(expr, LiteralBooleano):
            return ir.Constant(ir.IntType(1), 1 if expr.valor else 0)
        
        elif isinstance(expr, LiteralTexto):
            # Crear string constante global
            texto_bytes = bytearray((expr.valor + '\0').encode('utf-8'))
            texto_const = ir.Constant(ir.ArrayType(ir.IntType(8), len(texto_bytes)), texto_bytes)
            global_str = ir.GlobalVariable(self.module, texto_const.type, self.module.get_unique_name("str"))
            global_str.initializer = texto_const
            global_str.global_constant = True
            # Obtener puntero al primer elemento
            return self.builder.bitcast(global_str, ir.IntType(8).as_pointer())
        
        elif isinstance(expr, Identificador):
            alloca = self.variables.get(expr.nombre)
            if alloca:
                return self.builder.load(alloca, expr.nombre)
            return ir.Constant(ir.IntType(64), 0)
        
        elif isinstance(expr, ExpresionBinaria):
            return self._generar_binaria(expr)
        
        elif isinstance(expr, ExpresionUnaria):
            return self._generar_unaria(expr)
        
        elif isinstance(expr, LlamadaFuncion):
            return self._generar_llamada(expr)
            
        elif isinstance(expr, AccesoIndice):
            objeto = self._generar_expresion(expr.objeto)
            indice = self._generar_expresion(expr.indice)
            
            # Usar info de tipos
            tipo_obj = getattr(expr.objeto, 'tipo', None)
            es_mapa = False
            
            if tipo_obj and isinstance(tipo_obj, TipoMapa):
                es_mapa = True
            elif tipo_obj and isinstance(tipo_obj, TipoLista):
                es_mapa = False
            else:
                # Fallback
                if str(indice.type) == 'i8*': 
                    es_mapa = True
            
            if es_mapa:
                indice_ptr = self._cast_to_void_ptr(indice)
                val_ptr = self.builder.call(self.runtime_mapa_obtener, [objeto, indice_ptr])
            else:
                # Asumir lista
                if str(indice.type) != 'i64':
                     indice = self.builder.zext(indice, ir.IntType(64))
                val_ptr = self.builder.call(self.runtime_lista_obtener, [objeto, indice])
            
            # Determinar tipo de retorno basado en análisis semántico
            tipo_retorno = ir.IntType(64) # Default
            tipo_expr = getattr(expr, 'tipo', None)
            
            if tipo_expr:
                if tipo_expr.tipo_base == TipoDato.TEXTO:
                    tipo_retorno = ir.IntType(8).as_pointer()
                elif tipo_expr.tipo_base == TipoDato.FLOTANTE:
                    tipo_retorno = ir.DoubleType()
            
            return self._cast_from_void_ptr(val_ptr, tipo_retorno)
        
        elif isinstance(expr, LlamadaMetodo):
            return self._generar_metodo(expr)
        
        elif isinstance(expr, LiteralLista):
            # Crear nueva lista
            lista = self.builder.call(self.runtime_lista_nueva, [])
            
            # Agregar elementos
            for elem in expr.elementos:
                val = self._generar_expresion(elem)
                # Convertir valor a void* (i8*)
                val_ptr = self._cast_to_void_ptr(val)
                self.builder.call(self.runtime_lista_agregar, [lista, val_ptr])
            
            return lista
            
        elif isinstance(expr, LiteralMapa):
            # Crear nuevo mapa
            mapa = self.builder.call(self.runtime_mapa_nuevo, [])
            
            # Agregar pares
            for k, v in expr.pares:
                clave = self._generar_expresion(k)
                valor = self._generar_expresion(v)
                
                clave_ptr = self._cast_to_void_ptr(clave)
                valor_ptr = self._cast_to_void_ptr(valor)
                
                self.builder.call(self.runtime_mapa_asignar, [mapa, clave_ptr, valor_ptr])
            
            return mapa
            
        else:
            return ir.Constant(ir.IntType(64), 0)
    
    def _generar_metodo(self, expr: LlamadaMetodo):
        """Genera código para llamada a método"""
        objeto = self._generar_expresion(expr.objeto)
        args = [self._generar_expresion(arg) for arg in expr.argumentos]
        
        # Usar información de tipos adjunta por el analizador semántico
        tipo_obj = getattr(expr.objeto, 'tipo', None)
        
        # Si no hay info de tipos (ej. si no se corrió el semántico), usar hacks o fallar
        es_mapa = False
        if tipo_obj and isinstance(tipo_obj, TipoMapa):
            es_mapa = True
        elif tipo_obj and isinstance(tipo_obj, TipoLista):
            es_mapa = False
        else:
            # Fallback heurístico (hack)
            if expr.nombre_metodo in ['claves', 'valores']:
                es_mapa = True
            elif len(args) > 0 and str(args[0].type) == 'i8*':
                es_mapa = True
        
        if expr.nombre_metodo == 'agregar':
            val_ptr = self._cast_to_void_ptr(args[0])
            self.builder.call(self.runtime_lista_agregar, [objeto, val_ptr])
            return ir.Constant(ir.IntType(64), 0)
            
        elif expr.nombre_metodo == 'claves':
            return self.builder.call(self.runtime_mapa_claves, [objeto])
            
        elif expr.nombre_metodo == 'valores':
            return self.builder.call(self.runtime_mapa_valores, [objeto])
            
        elif expr.nombre_metodo == 'longitud':
            if es_mapa:
                return self.builder.call(self.runtime_mapa_longitud, [objeto])
            else:
                return self.builder.call(self.runtime_lista_longitud, [objeto])
            
        elif expr.nombre_metodo == 'eliminar':
            if es_mapa:
                arg_ptr = self._cast_to_void_ptr(args[0])
                return self.builder.call(self.runtime_mapa_eliminar, [objeto, arg_ptr])
            else:
                return self.builder.call(self.runtime_lista_eliminar, [objeto, args[0]])
            
        elif expr.nombre_metodo == 'contiene':
            val_ptr = self._cast_to_void_ptr(args[0])
            if es_mapa:
                res = self.builder.call(self.runtime_mapa_contiene, [objeto, val_ptr])
            else:
                res = self.builder.call(self.runtime_lista_contiene, [objeto, val_ptr])
            
            return self.builder.zext(res, ir.IntType(64))
        
        return ir.Constant(ir.IntType(64), 0)
    
    def _generar_binaria(self, expr: ExpresionBinaria):
        """Genera código para expresión binaria"""
        izq = self._generar_expresion(expr.izquierda)
        der = self._generar_expresion(expr.derecha)
        
        op = expr.operador.valor
        
        # Operadores aritméticos
        if op == '+':
            # Verificar si son strings (i8*)
            if str(izq.type) == 'i8*' and str(der.type) == 'i8*':
                # Concatenación de strings
                return self.builder.call(self.runtime_concatenar, [izq, der])
            else:
                # Suma aritmética
                return self.builder.add(izq, der)
        elif op == '-':
            return self.builder.sub(izq, der)
        elif op == '*':
            return self.builder.mul(izq, der)
        elif op == '/':
            return self.builder.sdiv(izq, der)
        elif op == '%':
            return self.builder.srem(izq, der)
        
        # Operadores de comparación
        elif op == '==':
            return self.builder.icmp_signed('==', izq, der)
        elif op == '!=':
            return self.builder.icmp_signed('!=', izq, der)
        elif op == '<':
            return self.builder.icmp_signed('<', izq, der)
        elif op == '>':
            return self.builder.icmp_signed('>', izq, der)
        elif op == '<=':
            return self.builder.icmp_signed('<=', izq, der)
        elif op == '>=':
            return self.builder.icmp_signed('>=', izq, der)
        
        # Operadores lógicos
        elif op == 'y':
            return self.builder.and_(izq, der)
        elif op == 'o':
            return self.builder.or_(izq, der)
        
        return ir.Constant(ir.IntType(64), 0)
    
    def _generar_unaria(self, expr: ExpresionUnaria):
        """Genera código para expresión unaria"""
        val = self._generar_expresion(expr.expresion)
        
        if expr.operador.tipo == TokenType.MENOS:
            return self.builder.neg(val)
        elif expr.operador.tipo == TokenType.NO:
            return self.builder.not_(val)
        
        return val
    
    def _generar_llamada(self, llamada: LlamadaFuncion):
        """Genera código para llamada a función"""
        # Verificar si es built-in
        if llamada.nombre == "mostrar":
            arg = self._generar_expresion(llamada.argumentos[0])
            return self.builder.call(self.runtime_mostrar, [arg])
        
        elif llamada.nombre == "convertir_a_texto":
            arg_expr = llamada.argumentos[0]
            arg = self._generar_expresion(arg_expr)
            
            # Usar información semántica si está disponible
            tipo_sem = getattr(arg_expr, 'tipo', None)
            
            if tipo_sem:
                if tipo_sem.tipo_base == TipoDato.ENTERO:
                    # Si viene como void* (de una lista/mapa), convertir a entero
                    if str(arg.type) == 'i8*':
                        arg = self.builder.ptrtoint(arg, ir.IntType(64))
                    return self.builder.call(self.runtime_conv_entero, [arg])
                    
                elif tipo_sem.tipo_base == TipoDato.FLOTANTE:
                    # Si viene como void*, convertir a double
                    if str(arg.type) == 'i8*':
                        # Asumimos que se guardó bitcasteado
                        arg_int = self.builder.ptrtoint(arg, ir.IntType(64))
                        arg = self.builder.bitcast(arg_int, ir.DoubleType())
                    return self.builder.call(self.runtime_conv_flotante, [arg])
                    
                elif tipo_sem.tipo_base == TipoDato.TEXTO:
                    # Ya es i8*, devolver tal cual
                    return arg
            
            # Fallback: inferencia por tipo LLVM
            if isinstance(arg.type, ir.PointerType) and arg.type.pointee == ir.IntType(8):
                return arg
            elif isinstance(arg.type, ir.DoubleType):
                return self.builder.call(self.runtime_conv_flotante, [arg])
            else:
                return self.builder.call(self.runtime_conv_entero, [arg])
        
        # Función definida por usuario
        elif llamada.nombre in self.funciones:
            fn = self.funciones[llamada.nombre]
            args = [self._generar_expresion(arg) for arg in llamada.argumentos]
            return self.builder.call(fn, args)
        
        return ir.Constant(ir.IntType(64), 0)


    def _cast_to_void_ptr(self, val):
        """Convierte un valor a void* (i8*)"""
        if isinstance(val.type, ir.PointerType) and val.type.pointee == ir.IntType(8):
            return val
        if isinstance(val.type, ir.IntType):
            return self.builder.inttoptr(val, ir.IntType(8).as_pointer())
        return self.builder.bitcast(val, ir.IntType(8).as_pointer())

    def _cast_from_void_ptr(self, val, target_type):
        """Convierte de void* (i8*) al tipo destino"""
        if target_type == ir.IntType(8).as_pointer():
            return val
        if isinstance(target_type, ir.IntType):
            return self.builder.ptrtoint(val, target_type)
        return self.builder.bitcast(val, target_type)


def inicializar_llvm():
    """Inicializa el backend de LLVM"""
    # En llvmlite >= 0.40, la inicialización es automática
    # Solo inicializar target nativo
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
