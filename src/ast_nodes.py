"""
Nodos del Árbol de Sintaxis Abstracta (AST) para Jade
"""

from typing import List, Optional, Any
from token_types import Token


class NodoAST:
    """Clase base para todos los nodos del AST"""
    pass


# ============================================================================
# EXPRESIONES
# ============================================================================

class Expresion(NodoAST):
    """Clase base para expresiones"""
    pass


class LiteralEntero(Expresion):
    """Literal numérico entero"""
    def __init__(self, valor: int, token: Token):
        self.valor = valor
        self.token = token
    
    def __repr__(self):
        return f"LiteralEntero({self.valor})"


class LiteralFlotante(Expresion):
    """Literal numérico flotante"""
    def __init__(self, valor: float, token: Token):
        self.valor = valor
        self.token = token
    
    def __repr__(self):
        return f"LiteralFlotante({self.valor})"


class LiteralTexto(Expresion):
    """Literal de cadena de texto"""
    def __init__(self, valor: str, token: Token):
        self.valor = valor
        self.token = token
    
    def __repr__(self):
        return f"LiteralTexto('{self.valor}')"


class LiteralBooleano(Expresion):
    """Literal booleano (verdadero/falso)"""
    def __init__(self, valor: bool, token: Token):
        self.valor = valor
        self.token = token
    
    def __repr__(self):
        return f"LiteralBooleano({self.valor})"


class LiteralNulo(Expresion):
    """Literal nulo"""
    def __init__(self, token: Token):
        self.token = token
    
    def __repr__(self):
        return "LiteralNulo()"


class Identificador(Expresion):
    """Referencia a una variable"""
    def __init__(self, nombre: str, token: Token):
        self.nombre = nombre
        self.token = token
    
    def __repr__(self):
        return f"Identificador({self.nombre})"


class ExpresionBinaria(Expresion):
    """Expresión binaria (a + b, a * b, etc.)"""
    def __init__(self, izquierda: Expresion, operador: Token, derecha: Expresion):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha
    
    def __repr__(self):
        return f"ExpresionBinaria({self.izquierda} {self.operador.valor} {self.derecha})"


class ExpresionUnaria(Expresion):
    """Expresión unaria (-a, no b)"""
    def __init__(self, operador: Token, expresion: Expresion):
        self.operador = operador
        self.expresion = expresion
    
    def __repr__(self):
        return f"ExpresionUnaria({self.operador.valor} {self.expresion})"


class LlamadaFuncion(Expresion):
    """Llamada a función"""
    def __init__(self, nombre: str, argumentos: List[Expresion], token: Token):
        self.nombre = nombre
        self.argumentos = argumentos
        self.token = token
    
    def __repr__(self):
        args = ', '.join(str(arg) for arg in self.argumentos)
        return f"LlamadaFuncion({self.nombre}({args}))"


class AccesoIndice(Expresion):
    """Acceso a elemento de lista/mapa por índice (arr[0])"""
    def __init__(self, objeto: Expresion, indice: Expresion, token: Token):
        self.objeto = objeto
        self.indice = indice
        self.token = token
    
    def __repr__(self):
        return f"AccesoIndice({self.objeto}[{self.indice}])"


class LiteralLista(Expresion):
    """Literal de lista [1, 2, 3]"""
    def __init__(self, elementos: List[Expresion], token: Token):
        self.elementos = elementos
        self.token = token
    
    def __repr__(self):
        elems = ', '.join(str(e) for e in self.elementos)
        return f"LiteralLista([{elems}])"


class LiteralMapa(Expresion):
    """Literal de mapa {clave: valor}"""
    def __init__(self, pares: List[tuple], token: Token):
        self.pares = pares  # Lista de (clave_expr, valor_expr)
        self.token = token
    
    def __repr__(self):
        items = ', '.join(f"{k}: {v}" for k, v in self.pares)
        return f"LiteralMapa({{{items}}})"


# ============================================================================
# STATEMENTS (DECLARACIONES)
# ============================================================================

class Statement(NodoAST):
    """Clase base para statements"""
    pass


class DeclaracionVariable(Statement):
    """Declaración de variable"""
    def __init__(self, nombre: str, tipo_dato: Optional[str], valor_inicial: Optional[Expresion], 
                 es_constante: bool, token: Token):
        self.nombre = nombre
        self.tipo_dato = tipo_dato
        self.valor_inicial = valor_inicial
        self.es_constante = es_constante
        self.token = token
    
    def __repr__(self):
        tipo = self.tipo_dato if self.tipo_dato else "inferido"
        const = "constante" if self.es_constante else "variable"
        return f"DeclaracionVariable({const} {self.nombre}: {tipo} = {self.valor_inicial})"


class Asignacion(Statement):
    """Asignación a variable"""
    def __init__(self, nombre: str, valor: Expresion, operador: Token):
        self.nombre = nombre
        self.valor = valor
        self.operador = operador  # =, +=, -=, etc.
    
    def __repr__(self):
        return f"Asignacion({self.nombre} {self.operador.valor} {self.valor})"


class AsignacionIndice(Statement):
    """Asignación a elemento de lista/mapa (arr[0] = valor)"""
    def __init__(self, objeto: Expresion, indice: Expresion, valor: Expresion, token: Token):
        self.objeto = objeto
        self.indice = indice
        self.valor = valor
        self.token = token
    
    def __repr__(self):
        return f"AsignacionIndice({self.objeto}[{self.indice}] = {self.valor})"


class Si(Statement):
    """Statement condicional si/entonces/sino"""
    def __init__(self, condicion: Expresion, bloque_entonces: List[Statement], 
                 bloque_sino: Optional[List[Statement]], token: Token):
        self.condicion = condicion
        self.bloque_entonces = bloque_entonces
        self.bloque_sino = bloque_sino
        self.token = token
    
    def __repr__(self):
        return f"Si({self.condicion})"


class Mientras(Statement):
    """Bucle mientras"""
    def __init__(self, condicion: Expresion, cuerpo: List[Statement], token: Token):
        self.condicion = condicion
        self.cuerpo = cuerpo
        self.token = token
    
    def __repr__(self):
        return f"Mientras({self.condicion})"


class Para(Statement):
    """Bucle para"""
    def __init__(self, variable: str, inicio: Expresion, fin: Expresion, 
                 cuerpo: List[Statement], token: Token):
        self.variable = variable
        self.inicio = inicio
        self.fin = fin
        self.cuerpo = cuerpo
        self.token = token
    
    def __repr__(self):
        return f"Para({self.variable} desde {self.inicio} hasta {self.fin})"


class Retornar(Statement):
    """Statement de retorno"""
    def __init__(self, valor: Optional[Expresion], token: Token):
        self.valor = valor
        self.token = token
    
    def __repr__(self):
        return f"Retornar({self.valor})"


class Romper(Statement):
    """Statement break"""
    def __init__(self, token: Token):
        self.token = token
    
    def __repr__(self):
        return "Romper()"


class Continuar(Statement):
    """Statement continue"""
    def __init__(self, token: Token):
        self.token = token
    
    def __repr__(self):
        return "Continuar()"


class ExpresionStatement(Statement):
    """Una expresión usada como statement (ej: llamada a función)"""
    def __init__(self, expresion: Expresion):
        self.expresion = expresion
    
    def __repr__(self):
        return f"ExpresionStatement({self.expresion})"


# ============================================================================
# DECLARACIONES DE ALTO NIVEL
# ============================================================================

class DeclaracionFuncion(NodoAST):
    """Declaración de función"""
    def __init__(self, nombre: str, parametros: List[tuple], tipo_retorno: Optional[str],
                 cuerpo: List[Statement], token: Token):
        self.nombre = nombre
        self.parametros = parametros  # Lista de (nombre, tipo_opcional)
        self.tipo_retorno = tipo_retorno
        self.cuerpo = cuerpo
        self.token = token
    
    def __repr__(self):
        params = ', '.join(f"{n}:{t if t else '?'}" for n, t in self.parametros)
        return f"DeclaracionFuncion({self.nombre}({params}))"


class Programa(NodoAST):
    """Nodo raíz del programa"""
    def __init__(self, declaraciones: List[NodoAST]):
        self.declaraciones = declaraciones
    
    def __repr__(self):
        return f"Programa({len(self.declaraciones)} declaraciones)"
