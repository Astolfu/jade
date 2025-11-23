"""
Token types para el lenguaje Jade
Define todos los tipos de tokens reconocidos por el lexer
"""

from enum import Enum, auto


class TokenType(Enum):
    """Tipos de tokens en Jade"""
    
    # Palabras reservadas - Control de flujo
    SI = auto()              # si
    ENTONCES = auto()        # entonces
    SINO = auto()            # sino
    MIENTRAS = auto()        # mientras
    PARA = auto()            # para
    DESDE = auto()           # desde
    HASTA = auto()           # hasta
    HACER = auto()           # hacer
    ROMPER = auto()          # romper
    CONTINUAR = auto()       # continuar
    FIN = auto()             # fin
    
    # Palabras reservadas - Funciones
    FUNCION = auto()         # funcion
    RETORNAR = auto()        # retornar
    
    # Palabras reservadas - Declaraciones
    VARIABLE = auto()        # variable
    CONSTANTE = auto()       # constante
    
    # Palabras reservadas - Tipos
    ENTERO = auto()          # entero
    FLOTANTE = auto()        # flotante
    BOOLEANO = auto()        # booleano
    TEXTO = auto()           # texto
    CARACTER = auto()        # caracter
    LISTA = auto()           # lista
    MAPA = auto()            # mapa
    TUPLA = auto()           # tupla
    
    # Palabras reservadas - Valores literales
    VERDADERO = auto()       # verdadero
    FALSO = auto()           # falso
    NULO = auto()            # nulo
    
    # Palabras  reservadas - Módulos
    IMPORTAR = auto()        # importar
    MODULO_KW = auto()       # modulo (palabra reservada)
    
    # Palabras reservadas - Manejo de errores
    INTENTAR = auto()        # intentar
    CAPTURAR = auto()        # capturar
    LANZAR = auto()          # lanzar
    
    # Operadores lógicos (palabras)
    Y = auto()               # y
    O = auto()               # o
    NO = auto()              # no
    EN = auto()              # en
    
    # Literales
    LITERAL_ENTERO = auto()
    LITERAL_FLOTANTE = auto()
    LITERAL_TEXTO = auto()
    LITERAL_CARACTER = auto()
    
    # Identificadores
    IDENTIFICADOR = auto()
    
    # Operadores aritméticos
    MAS = auto()             # +
    MENOS = auto()           # -
    MULTIPLICAR = auto()     # *
    DIVIDIR = auto()         # /
    MODULO = auto()          # %
    POTENCIA = auto()        # ^
    
    # Operadores de comparación
    IGUAL = auto()           # ==
    DIFERENTE = auto()       # !=
    MENOR = auto()           # <
    MAYOR = auto()           # >
    MENOR_IGUAL = auto()     # <=
    MAYOR_IGUAL = auto()     # >=
    
    # Operadores de asignación
    ASIGNAR = auto()         # =
    MAS_IGUAL = auto()       # +=
    MENOS_IGUAL = auto()     # -=
    MULTIPLICAR_IGUAL = auto() # *=
    DIVIDIR_IGUAL = auto()   # /=
    
    # Delimitadores
    PARENTESIS_IZQ = auto()  # (
    PARENTESIS_DER = auto()  # )
    LLAVE_IZQ = auto()       # {
    LLAVE_DER = auto()       # }
    CORCHETE_IZQ = auto()    # [
    CORCHETE_DER = auto()    # ]
    
    # Puntuación
    COMA = auto()            # ,
    PUNTO = auto()           # .
    DOS_PUNTOS = auto()      # :
    PUNTO_Y_COMA = auto()    # ;
    
    # Especiales
    NUEVA_LINEA = auto()
    EOF = auto()             # End of file
    

class Token:
    """Representa un token con su tipo, valor y posición"""
    
    def __init__(self, tipo: TokenType, valor: str, linea: int, columna: int):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def __repr__(self):
        return f"Token({self.tipo.name}, '{self.valor}', {self.linea}:{self.columna})"
    
    def __str__(self):
        return self.__repr__()


# Mapeo de palabras reservadas a sus tipos de token
PALABRAS_RESERVADAS = {
    # Control de flujo
    'si': TokenType.SI,
    'entonces': TokenType.ENTONCES,
    'sino': TokenType.SINO,
    'mientras': TokenType.MIENTRAS,
    'para': TokenType.PARA,
    'desde': TokenType.DESDE,
    'hasta': TokenType.HASTA,
    'hacer': TokenType.HACER,
    'romper': TokenType.ROMPER,
    'continuar': TokenType.CONTINUAR,
    'fin': TokenType.FIN,
    
    # Funciones
    'funcion': TokenType.FUNCION,
    'retornar': TokenType.RETORNAR,
    
    # Declaraciones
    'variable': TokenType.VARIABLE,
    'constante': TokenType.CONSTANTE,
    
    # Tipos
    'entero': TokenType.ENTERO,
    'flotante': TokenType.FLOTANTE,
    'booleano': TokenType.BOOLEANO,
    'texto': TokenType.TEXTO,
    'caracter': TokenType.CARACTER,
    'lista': TokenType.LISTA,
    'mapa': TokenType.MAPA,
    'tupla': TokenType.TUPLA,
    
    # Valores literales
    'verdadero': TokenType.VERDADERO,
    'falso': TokenType.FALSO,
    'nulo': TokenType.NULO,
    
    # Módulos
    'importar': TokenType.IMPORTAR,
    'modulo': TokenType.MODULO_KW,
    
    # Manejo de errores
    'intentar': TokenType.INTENTAR,
    'capturar': TokenType.CAPTURAR,
    'lanzar': TokenType.LANZAR,
    
    # Operadores lógicos
    'y': TokenType.Y,
    'o': TokenType.O,
    'no': TokenType.NO,
    'en': TokenType.EN,
}
