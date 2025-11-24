"""
Funciones integradas (built-in) de Jade
Define las funciones de la biblioteca estándar
"""

from type_system import *


class FuncionBuiltIn:
    """Representa una función integrada"""
    
    def __init__(self, nombre: str, parametros: list, tipo_retorno: Tipo):
        self.nombre = nombre
        self.parametros = parametros  # Lista de (nombre_param, tipo)
        self.tipo_retorno = tipo_retorno


# Definir todas las funciones built-in
FUNCIONES_BUILTIN = {
    # Entrada/Salida
    'mostrar': FuncionBuiltIn(
        'mostrar',
        [('texto', TIPO_TEXTO)],
        TIPO_NULO
    ),
    'leer': FuncionBuiltIn(
        'leer',
        [],
        TIPO_TEXTO
    ),
    
    # Conversiones
    'convertir_a_texto': FuncionBuiltIn(
        'convertir_a_texto',
        [('valor', TIPO_DESCONOCIDO)],  # Acepta cualquier tipo
        TIPO_TEXTO
    ),
    'convertir_a_entero': FuncionBuiltIn(
        'convertir_a_entero',
        [('texto', TIPO_TEXTO)],
        TIPO_ENTERO
    ),
    'convertir_a_flotante': FuncionBuiltIn(
        'convertir_a_flotante',
        [('texto', TIPO_TEXTO)],
        TIPO_FLOTANTE
    ),
    
    # Matemáticas
    'abs': FuncionBuiltIn(
        'abs',
        [('x', TIPO_FLOTANTE)],
        TIPO_FLOTANTE
    ),
    'max': FuncionBuiltIn(
        'max',
        [('a', TIPO_ENTERO), ('b', TIPO_ENTERO)],
        TIPO_ENTERO
    ),
    'min': FuncionBuiltIn(
        'min',
        [('a', TIPO_ENTERO), ('b', TIPO_ENTERO)],
        TIPO_ENTERO
    ),
    'potencia': FuncionBuiltIn(
        'potencia',
        [('base', TIPO_FLOTANTE), ('exponente', TIPO_FLOTANTE)],
        TIPO_FLOTANTE
    ),
    'raiz': FuncionBuiltIn(
        'raiz',
        [('x', TIPO_FLOTANTE)],
        TIPO_FLOTANTE
    ),
    'aleatorio': FuncionBuiltIn(
        'aleatorio',
        [],
        TIPO_FLOTANTE
    ),
    
    # Cadenas
    'longitud': FuncionBuiltIn(
        'longitud',
        [('texto', TIPO_TEXTO)],
        TIPO_ENTERO
    ),
    'mayusculas': FuncionBuiltIn(
        'mayusculas',
        [('texto', TIPO_TEXTO)],
        TIPO_TEXTO
    ),
    'minusculas': FuncionBuiltIn(
        'minusculas',
        [('texto', TIPO_TEXTO)],
        TIPO_TEXTO
    ),
    'contiene': FuncionBuiltIn(
        'contiene',
        [('texto', TIPO_TEXTO), ('subcadena', TIPO_TEXTO)],
        TIPO_BOOLEANO
    ),
    # String interpolation
    'f': FuncionBuiltIn(
        'f',
        [('template', TIPO_TEXTO)],
        TIPO_TEXTO
    ),
}


def obtener_funcion_builtin(nombre: str):
    """Obtiene una función built-in por nombre"""
    return FUNCIONES_BUILTIN.get(nombre)


def es_funcion_builtin(nombre: str) -> bool:
    """Verifica si un nombre es una función built-in"""
    return nombre in FUNCIONES_BUILTIN
