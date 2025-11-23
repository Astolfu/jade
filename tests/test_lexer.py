"""
Tests del Lexer de Jade
"""

import sys
sys.path.insert(0, '../src')

import pytest
from lexer import Lexer, tokenizar_codigo
from token_types import TokenType


def test_palabras_reservadas():
    """Prueba tokenización de palabras reservadas"""
    codigo = "funcion si entonces sino mientras para desde hasta hacer fin"
    tokens = tokenizar_codigo(codigo)
    
    tipos_esperados = [
        TokenType.FUNCION,
        TokenType.SI,
        TokenType.ENTONCES,
        TokenType.SINO,
        TokenType.MIENTRAS,
        TokenType.PARA,
        TokenType.DESDE,
        TokenType.HASTA,
        TokenType.HACER,
        TokenType.FIN,
        TokenType.EOF,
    ]
    
    assert len(tokens) == len(tipos_esperados)
    for token, tipo_esperado in zip(tokens, tipos_esperados):
        assert token.tipo == tipo_esperado


def test_numeros():
    """Prueba tokenización de números"""
    codigo = "42 3.14159 0 1000"
    tokens = tokenizar_codigo(codigo)
    
    assert tokens[0].tipo == TokenType.LITERAL_ENTERO
    assert tokens[0].valor == "42"
    
    assert tokens[1].tipo == TokenType.LITERAL_FLOTANTE
    assert tokens[1].valor == "3.14159"
    
    assert tokens[2].tipo == TokenType.LITERAL_ENTERO
    assert tokens[3].tipo == TokenType.LITERAL_ENTERO


def test_cadenas():
    """Prueba tokenización de cadenas"""
    codigo = '"Hola Mundo" "Texto con espacios"'
    tokens = tokenizar_codigo(codigo)
    
    assert tokens[0].tipo == TokenType.LITERAL_TEXTO
    assert tokens[0].valor == "Hola Mundo"
    
    assert tokens[1].tipo == TokenType.LITERAL_TEXTO
    assert tokens[1].valor == "Texto con espacios"


def test_identificadores():
    """Prueba tokenización de identificadores"""
    codigo = "variable nombre edad_usuario miVariable"
    tokens = tokenizar_codigo(codigo)
    
    assert tokens[0].tipo == TokenType.VARIABLE
    assert tokens[1].tipo == TokenType.IDENTIFICADOR
    assert tokens[1].valor == "nombre"
    assert tokens[2].tipo == TokenType.IDENTIFICADOR
    assert tokens[2].valor == "edad_usuario"


def test_operadores():
    """Prueba tokenización de operadores"""
    codigo = "+ - * / % ^ == != < > <= >= y o no"
    tokens = tokenizar_codigo(codigo)
    
    tipos_esperados = [
        TokenType.MAS,
        TokenType.MENOS,
        TokenType.MULTIPLICAR,
        TokenType.DIVIDIR,
        TokenType.MODULO,
        TokenType.POTENCIA,
        TokenType.IGUAL,
        TokenType.DIFERENTE,
        TokenType.MENOR,
        TokenType.MAYOR,
        TokenType.MENOR_IGUAL,
        TokenType.MAYOR_IGUAL,
        TokenType.Y,
        TokenType.O,
        TokenType.NO,
        TokenType.EOF,
    ]
    
    for token, tipo_esperado in zip(tokens, tipos_esperados):
        assert token.tipo == tipo_esperado


def test_comentarios():
    """Prueba que los comentarios se ignoren"""
    codigo = """
    // Este es un comentario
    variable x = 10
    /* Comentario
       de múltiples
       líneas */
    variable y = 20
    """
    tokens = tokenizar_codigo(codigo)
    
    # Solo deberían aparecer los tokens de las declaraciones
    assert tokens[0].tipo == TokenType.VARIABLE
    assert tokens[1].tipo == TokenType.IDENTIFICADOR
    assert tokens[1].valor == "x"


def test_expresion_compleja():
    """Prueba tokenización de expresión compleja"""
    codigo = "resultado = (a + b) * (c - d)"
    tokens = tokenizar_codigo(codigo)
    
    tipos_esperados = [
        TokenType.IDENTIFICADOR,  # resultado
        TokenType.ASIGNAR,        # =
        TokenType.PARENTESIS_IZQ, # (
        TokenType.IDENTIFICADOR,  # a
        TokenType.MAS,            # +
        TokenType.IDENTIFICADOR,  # b
        TokenType.PARENTESIS_DER, # )
        TokenType.MULTIPLICAR,    # *
        TokenType.PARENTESIS_IZQ, # (
        TokenType.IDENTIFICADOR,  # c
        TokenType.MENOS,          # -
        TokenType.IDENTIFICADOR,  # d
        TokenType.PARENTESIS_DER, # )
        TokenType.EOF,
    ]
    
    assert len(tokens) == len(tipos_esperados)
    for token, tipo_esperado in zip(tokens, tipos_esperados):
        assert token.tipo == tipo_esperado


def test_funcion_simple():
    """Prueba tokenización de función simple"""
    codigo = """
    funcion suma(a, b)
        retornar a + b
    fin
    """
    tokens = tokenizar_codigo(codigo)
    
    assert tokens[0].tipo == TokenType.FUNCION
    assert tokens[1].tipo == TokenType.IDENTIFICADOR
    assert tokens[1].valor == "suma"
    assert tokens[2].tipo == TokenType.PARENTESIS_IZQ
    assert tokens[3].tipo == TokenType.IDENTIFICADOR
    assert tokens[4].tipo == TokenType.COMA
    assert tokens[5].tipo == TokenType.IDENTIFICADOR
    assert tokens[6].tipo == TokenType.PARENTESIS_DER


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
