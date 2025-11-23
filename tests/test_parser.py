"""
Tests del Parser de Jade
"""

import sys
sys.path.insert(0, '../src')

import pytest
from lexer import tokenizar_codigo
from parser import parsear_codigo
from ast_nodes import *


def test_declaracion_funcion_simple():
    """Prueba parseo de función simple"""
    codigo = """
    funcion suma(a, b)
        retornar a + b
    fin
    """
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    assert len(programa.declaraciones) == 1
    func = programa.declaraciones[0]
    assert isinstance(func, DeclaracionFuncion)
    assert func.nombre == "suma"
    assert len(func.parametros) == 2
    assert len(func.cuerpo) == 1


def test_declaracion_variable():
    """Prueba parseo de declaración de variable"""
    codigo = "variable x = 10"
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    assert len(programa.declaraciones) == 1
    var = programa.declaraciones[0]
    assert isinstance(var, DeclaracionVariable)
    assert var.nombre == "x"
    assert isinstance(var.valor_inicial, LiteralEntero)


def test_expresion_binaria():
    """Prueba parseo de expresión binaria"""
    codigo = """
    funcion test()
        variable resultado = 2 + 3 * 4
    fin
    """
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    func = programa.declaraciones[0]
    var_decl = func.cuerpo[0]
    expr = var_decl.valor_inicial
    
    # Debería ser: 2 + (3 * 4) por precedencia
    assert isinstance(expr, ExpresionBinaria)
    assert expr.operador.tipo == TokenType.MAS


def test_condicional_si():
    """Prueba parseo de condicional si/entonces/sino"""
    codigo = """
    funcion test()
        si x > 0 entonces
            retornar 1
        sino
            retornar 0
        fin
    fin
    """
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    func = programa.declaraciones[0]
    si_stmt = func.cuerpo[0]
    
    assert isinstance(si_stmt, Si)
    assert isinstance(si_stmt.condicion, ExpresionBinaria)
    assert len(si_stmt.bloque_entonces) == 1
    assert len(si_stmt.bloque_sino) == 1


def test_bucle_mientras():
    """Prueba parseo de bucle mientras"""
    codigo = """
    funcion test()
        mientras x < 10 hacer
            x = x + 1
        fin
    fin
    """
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    func = programa.declaraciones[0]
    mientras_stmt = func.cuerpo[0]
    
    assert isinstance(mientras_stmt, Mientras)
    assert isinstance(mientras_stmt.condicion, ExpresionBinaria)
    assert len(mientras_stmt.cuerpo) == 1


def test_bucle_para():
    """Prueba parseo de bucle para"""
    codigo = """
    funcion test()
        para i desde 0 hasta 10 hacer
            mostrar(i)
        fin
    fin
    """
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    func = programa.declaraciones[0]
    para_stmt = func.cuerpo[0]
    
    assert isinstance(para_stmt, Para)
    assert para_stmt.variable == "i"
    assert isinstance(para_stmt.inicio, LiteralEntero)
    assert isinstance(para_stmt.fin, LiteralEntero)


def test_llamada_funcion():
    """Prueba parseo de llamada a función"""
    codigo = """
    funcion test()
        variable resultado = suma(5, 3)
    fin
    """
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    func = programa.declaraciones[0]
    var_decl = func.cuerpo[0]
    llamada = var_decl.valor_inicial
    
    assert isinstance(llamada, LlamadaFuncion)
    assert llamada.nombre == "suma"
    assert len(llamada.argumentos) == 2


def test_lista_literal():
    """Prueba parseo de lista literal"""
    codigo = """
    funcion test()
        variable numeros = [1, 2, 3, 4, 5]
    fin
    """
    tokens = tokenizar_codigo(codigo)
    programa = parsear_codigo(tokens)
    
    func = programa.declaraciones[0]
    var_decl = func.cuerpo[0]
    lista = var_decl.valor_inicial
    
    assert isinstance(lista, LiteralLista)
    assert len(lista.elementos) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
