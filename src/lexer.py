"""
Analizador léxico (Lexer) para Jade
Convierte código fuente en una secuencia de tokens
"""

from token_types import Token, TokenType, PALABRAS_RESERVADAS


class Lexer:
    """Analizador léxico que tokeniza código fuente Jade"""
    
    def __init__(self, codigo: str):
        self.codigo = codigo
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.caracter_actual = self.codigo[0] if len(self.codigo) > 0 else None
    
    def error(self, mensaje: str):
        """Lanza un error de lexer con información de posición"""
        raise SyntaxError(
            f"Error léxico en línea {self.linea}, columna {self.columna}: {mensaje}"
        )
    
    def avanzar(self):
        """Avanza al siguiente carácter"""
        if self.caracter_actual == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        
        self.posicion += 1
        if self.posicion >= len(self.codigo):
            self.caracter_actual = None
        else:
            self.caracter_actual = self.codigo[self.posicion]
    
    def ver_siguiente(self, offset=1):
        """Mira el siguiente carácter sin avanzar"""
        pos = self.posicion + offset
        if pos >= len(self.codigo):
            return None
        return self.codigo[pos]
    
    def saltar_espacios(self):
        """Salta espacios en blanco (pero no newlines)"""
        while self.caracter_actual and self.caracter_actual in ' \t\r':
            self.avanzar()
    
    def saltar_comentario_linea(self):
        """Salta comentario de una sola línea (//...)"""
        # Saltar //
        self.avanzar()
        self.avanzar()
        
        # Saltar hasta el final de la línea
        while self.caracter_actual and self.caracter_actual != '\n':
            self.avanzar()
    
    def saltar_comentario_bloque(self):
        """Salta comentario de múltiples líneas (/* ... */)"""
        # Saltar /*
        self.avanzar()
        self.avanzar()
        
        # Buscar */
        while self.caracter_actual:
            if self.caracter_actual == '*' and self.ver_siguiente() == '/':
                self.avanzar()  # *
                self.avanzar()  # /
                return
            self.avanzar()
        
        self.error("Comentario de bloque sin cerrar")
    
    def leer_numero(self):
        """Lee un número (entero o flotante)"""
        linea_inicio = self.linea
        columna_inicio = self.columna
        numero = ''
        es_flotante = False
        
        while self.caracter_actual and (self.caracter_actual.isdigit() or self.caracter_actual == '.'):
            if self.caracter_actual == '.':
                if es_flotante:
                    self.error("Número con múltiples puntos decimales")
                es_flotante = True
            numero += self.caracter_actual
            self.avanzar()
        
        # Verificar que no termine en punto
        if numero.endswith('.'):
            self.error("Número no puede terminar en punto decimal")
        
        tipo = TokenType.LITERAL_FLOTANTE if es_flotante else TokenType.LITERAL_ENTERO
        return Token(tipo, numero, linea_inicio, columna_inicio)
    
    def leer_texto(self, delimitador):
        """Lee una cadena de texto entre comillas"""
        linea_inicio = self.linea
        columna_inicio = self.columna
        
        # Saltar comilla inicial
        self.avanzar()
        
        texto = ''
        while self.caracter_actual and self.caracter_actual != delimitador:
            if self.caracter_actual == '\\':
                # Manejar caracteres de escape
                self.avanzar()
                if self.caracter_actual == 'n':
                    texto += '\n'
                elif self.caracter_actual == 't':
                    texto += '\t'
                elif self.caracter_actual == 'r':
                    texto += '\r'
                elif self.caracter_actual == '\\':
                    texto += '\\'
                elif self.caracter_actual == delimitador:
                    texto += delimitador
                else:
                    texto += self.caracter_actual
                self.avanzar()
            else:
                texto += self.caracter_actual
                self.avanzar()
        
        if not self.caracter_actual:
            self.error(f"Cadena sin cerrar (falta {delimitador})")
        
        # Saltar comilla final
        self.avanzar()
        
        return Token(TokenType.LITERAL_TEXTO, texto, linea_inicio, columna_inicio)
    
    def leer_caracter(self):
        """Lee un carácter entre comillas simples"""
        linea_inicio = self.linea
        columna_inicio = self.columna
        
        # Saltar comilla inicial
        self.avanzar()
        
        if not self.caracter_actual or self.caracter_actual == "'":
            self.error("Carácter vacío")
        
        caracter = self.caracter_actual
        
        # Manejar escape
        if caracter == '\\':
            self.avanzar()
            if self.caracter_actual == 'n':
                caracter = '\n'
            elif self.caracter_actual == 't':
                caracter = '\t'
            elif self.caracter_actual == '\\':
                caracter = '\\'
            elif self.caracter_actual == "'":
                caracter = "'"
            else:
                caracter = self.caracter_actual
        
        self.avanzar()
        
        if self.caracter_actual != "'":
            self.error("Carácter debe tener exactamente un carácter entre comillas simples")
        
        # Saltar comilla final
        self.avanzar()
        
        return Token(TokenType.LITERAL_CARACTER, caracter, linea_inicio, columna_inicio)
    
    def leer_identificador(self):
        """Lee un identificador o palabra reservada"""
        linea_inicio = self.linea
        columna_inicio = self.columna
        identificador = ''
        
        # Primer carácter debe ser letra o guión bajo
        while self.caracter_actual and (self.caracter_actual.isalnum() or self.caracter_actual == '_'):
            identificador += self.caracter_actual
            self.avanzar()
        
        # Verificar si es palabra reservada
        tipo = PALABRAS_RESERVADAS.get(identificador, TokenType.IDENTIFICADOR)
        
        return Token(tipo, identificador, linea_inicio, columna_inicio)
    
    def siguiente_token(self):
        """Obtiene el siguiente token del código"""
        while self.caracter_actual:
            # Saltar espacios en blanco
            if self.caracter_actual in ' \t\r':
                self.saltar_espacios()
                continue
            
            # Nueva línea
            if self.caracter_actual == '\n':
                token = Token(TokenType.NUEVA_LINEA, '\\n', self.linea, self.columna)
                self.avanzar()
                return token
            
            # Comentarios
            if self.caracter_actual == '/' and self.ver_siguiente() == '/':
                self.saltar_comentario_linea()
                continue
            
            if self.caracter_actual == '/' and self.ver_siguiente() == '*':
                self.saltar_comentario_bloque()
                continue
            
            # Números
            if self.caracter_actual.isdigit():
                return self.leer_numero()
            
            # Cadenas de texto
            if self.caracter_actual == '"':
                return self.leer_texto('"')
            
            # Caracteres
            if self.caracter_actual == "'":
                return self.leer_caracter()
            
            # Identificadores y palabras reservadas
            if self.caracter_actual.isalpha() or self.caracter_actual == '_':
                return self.leer_identificador()
            
            # Operadores de dos caracteres
            linea_actual = self.linea
            columna_actual = self.columna
            
            if self.caracter_actual == '=' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.IGUAL, '==', linea_actual, columna_actual)
            
            if self.caracter_actual == '!' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.DIFERENTE, '!=', linea_actual, columna_actual)
            
            if self.caracter_actual == '<' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.MENOR_IGUAL, '<=', linea_actual, columna_actual)
            
            if self.caracter_actual == '>' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.MAYOR_IGUAL, '>=', linea_actual, columna_actual)
            
            if self.caracter_actual == '+' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.MAS_IGUAL, '+=', linea_actual, columna_actual)
            
            if self.caracter_actual == '-' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.MENOS_IGUAL, '-=', linea_actual, columna_actual)
            
            if self.caracter_actual == '*' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.MULTIPLICAR_IGUAL, '*=', linea_actual, columna_actual)
            
            if self.caracter_actual == '/' and self.ver_siguiente() == '=':
                self.avanzar()
                self.avanzar()
                return Token(TokenType.DIVIDIR_IGUAL, '/=', linea_actual, columna_actual)
            
            # Operadores y símbolos de un carácter
            simbolos_simples = {
                '+': TokenType.MAS,
                '-': TokenType.MENOS,
                '*': TokenType.MULTIPLICAR,
                '/': TokenType.DIVIDIR,
                '%': TokenType.MODULO,
                '^': TokenType.POTENCIA,
                '=': TokenType.ASIGNAR,
                '<': TokenType.MENOR,
                '>': TokenType.MAYOR,
                '(': TokenType.PARENTESIS_IZQ,
                ')': TokenType.PARENTESIS_DER,
                '{': TokenType.LLAVE_IZQ,
                '}': TokenType.LLAVE_DER,
                '[': TokenType.CORCHETE_IZQ,
                ']': TokenType.CORCHETE_DER,
                ',': TokenType.COMA,
                '.': TokenType.PUNTO,
                ':': TokenType.DOS_PUNTOS,
                ';': TokenType.PUNTO_Y_COMA,
            }
            
            if self.caracter_actual in simbolos_simples:
                simbolo = self.caracter_actual
                tipo = simbolos_simples[simbolo]
                self.avanzar()
                return Token(tipo, simbolo, linea_actual, columna_actual)
            
            # Carácter desconocido
            self.error(f"Carácter inesperado: '{self.caracter_actual}'")
        
        # Fin del archivo
        return Token(TokenType.EOF, '', self.linea, self.columna)
    
    def tokenizar(self):
        """Tokeniza todo el código y retorna una lista de tokens"""
        tokens = []
        while True:
            token = self.siguiente_token()
            # Ignorar nueva línea en la lista de tokens (opcional)
            if token.tipo != TokenType.NUEVA_LINEA:
                tokens.append(token)
            if token.tipo == TokenType.EOF:
                break
        return tokens


# Función de utilidad para pruebas
def tokenizar_codigo(codigo: str):
    """Tokeniza código Jade y retorna lista de tokens"""
    lexer = Lexer(codigo)
    return lexer.tokenizar()


if __name__ == "__main__":
    # Prueba simple
    codigo_ejemplo = """
    funcion factorial(n)
        si n == 0 entonces
            retornar 1
        sino
            retornar n * factorial(n - 1)
        fin
    fin
    """
    
    try:
        tokens = tokenizar_codigo(codigo_ejemplo)
        for token in tokens:
            print(token)
    except SyntaxError as e:
        print(f"Error: {e}")
