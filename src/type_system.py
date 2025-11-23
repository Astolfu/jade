"""
Sistema de tipos para Jade
"""

from enum import Enum, auto


class TipoDato(Enum):
    """Tipos de datos en Jade"""
    ENTERO = auto()
    FLOTANTE = auto()
    BOOLEANO = auto()
    TEXTO = auto()
    CARACTER = auto()
    LISTA = auto()
    MAPA = auto()
    TUPLA = auto()
    NULO = auto()
    FUNCION = auto()
    DESCONOCIDO = auto()


class Tipo:
    """Representa un tipo de dato"""
    
    def __init__(self, tipo_base: TipoDato, tipo_elemento=None):
        self.tipo_base = tipo_base
        self.tipo_elemento = tipo_elemento  # Para listas, mapas, etc.
    
    def __eq__(self, otro):
        if not isinstance(otro, Tipo):
            return False
        return (self.tipo_base == otro.tipo_base and 
                self.tipo_elemento == otro.tipo_elemento)
    
    def __repr__(self):
        if self.tipo_elemento:
            return f"Tipo({self.tipo_base.name}[{self.tipo_elemento}])"
        return f"Tipo({self.tipo_base.name})"
    
    def __str__(self):
        return self.tipo_base.name.lower()
    
    @staticmethod
    def desde_nombre(nombre: str):
        """Crea un tipo desde un nombre de tipo"""
        mapeo = {
            'entero': TipoDato.ENTERO,
            'flotante': TipoDato.FLOTANTE,
            'booleano': TipoDato.BOOLEANO,
            'texto': TipoDato.TEXTO,
            'caracter': TipoDato.CARACTER,
            'lista': TipoDato.LISTA,
            'mapa': TipoDato.MAPA,
            'tupla': TipoDato.TUPLA,
        }
        tipo_base = mapeo.get(nombre, TipoDato.DESCONOCIDO)
        return Tipo(tipo_base)
    
    def es_numerico(self):
        """Verifica si el tipo es numérico"""
        return self.tipo_base in (TipoDato.ENTERO, TipoDato.FLOTANTE)
    
    def es_comparable(self):
        """Verifica si el tipo puede ser comparado"""
        return self.tipo_base in (TipoDato.ENTERO, TipoDato.FLOTANTE, 
                                  TipoDato.TEXTO, TipoDato.BOOLEANO)


# Tipos predefinidos para conveniencia
TIPO_ENTERO = Tipo(TipoDato.ENTERO)
TIPO_FLOTANTE = Tipo(TipoDato.FLOTANTE)
TIPO_BOOLEANO = Tipo(TipoDato.BOOLEANO)
TIPO_TEXTO = Tipo(TipoDato.TEXTO)
TIPO_CARACTER = Tipo(TipoDato.CARACTER)
TIPO_NULO = Tipo(TipoDato.NULO)
TIPO_DESCONOCIDO = Tipo(TipoDato.DESCONOCIDO)


def inferir_tipo_binario(tipo_izq: Tipo, operador: str, tipo_der: Tipo) -> Tipo:
    """Infiere el tipo resultante de una operación binaria"""
    # Operadores aritméticos
    if operador in ('+', '-', '*', '/', '%', '^'):
        if tipo_izq.es_numerico() and tipo_der.es_numerico():
            # Si alguno es flotante, el resultado es flotante
            if tipo_izq.tipo_base == TipoDato.FLOTANTE or tipo_der.tipo_base == TipoDato.FLOTANTE:
                return TIPO_FLOTANTE
            return TIPO_ENTERO
        elif operador == '+' and tipo_izq.tipo_base == TipoDato.TEXTO:
            # Concatenación de strings
            return TIPO_TEXTO
    
    # Operadores de comparación
    if operador in ('==', '!=', '<', '>', '<=', '>='):
        return TIPO_BOOLEANO
    
    # Operadores lógicos
    if operador in ('y', 'o'):
        return TIPO_BOOLEANO
    
    return TIPO_DESCONOCIDO


def puede_convertir(desde: Tipo, hacia: Tipo) -> bool:
    """Verifica si se puede convertir un tipo a otro"""
    # Mismo tipo
    if desde == hacia:
        return True
    
    # Entero a flotante
    if desde.tipo_base == TipoDato.ENTERO and hacia.tipo_base == TipoDato.FLOTANTE:
        return True
    
    # Cualquier tipo a texto (toString)
    if hacia.tipo_base == TipoDato.TEXTO:
        return True
    
    return False
