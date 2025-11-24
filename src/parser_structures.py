"""
Parser methods for Structures/Classes - TO BE INTEGRATED INTO parser.py

INTEGRATION INSTRUCTIONS:
=========================

1. Add these methods to the Parser class in src/parser.py
2. Modify declaracion_alto_nivel() - add after line 69:
        elif self.verificar(TokenType.ESTRUCTURA):
            return self.declaracion_estructura()

3. Modify expresion_primaria() - add after line 493 (before identificador check):
        # Este (self-reference)
        if self.verificar(TokenType.ESTE):
            token = self.token_actual
            self.avanzar()
            return IdentificadorEste(token)

4. Modify expresion_primaria() - modify IDENTIFICADOR section (around line 498):
        if self.verificar(TokenType.IDENTIFICADOR):
            token = self.token_actual
            nombre = token.valor
            self.avanzar()
            
            # Verificar si es instancia de estructura: NombreEstructura { ... }
            if self.verificar(TokenType.LLAVE_IZQ):
                return self.instancia_estructura(nombre, token)
            
            return Identificador(nombre, token)

5. Modify expresion_postfija() - change PUNTO handling (around line 434):
        elif self.verificar(TokenType.PUNTO):
            # Acceso a campo o método
            self.avanzar()
            token_nombre = self.esperar(TokenType.IDENTIFICADOR)
            nombre = token_nombre.valor
            
            # Verificar si es método (tiene paréntesis) o campo
            if self.verificar(TokenType.PARENTESIS_IZQ):
                # Llamada a método
                self.avanzar()
                argumentos = []
                if not self.verificar(TokenType.PARENTESIS_DER):
                    argumentos.append(self.expresion())
                    while self.verificar(TokenType.COMA):
                        self.avanzar()
                        argumentos.append(self.expresion())
                self.esperar(TokenType.PARENTESIS_DER)
                expr = LlamadaMetodo(expr, nombre, argumentos, token_nombre)
            else:
                # Acceso a campo
                expr = AccesoCampo(expr, nombre, token_nombre)
"""

from typing import List
from token_types import Token, TokenType
from ast_nodes import DeclaracionEstructura, InstanciaEstructura, DeclaracionFuncion

# ============================================================================
# METHODS TO ADD TO Parser CLASS
# ============================================================================

def declaracion_estructura(self) -> DeclaracionEstructura:
    """Parsea una declaración de estructura
    
    Sintaxis:
        estructura NombreEstructura {
            campo1: tipo1
            campo2: tipo2
            
            funcion metodo1()
                # cuerpo
            fin
        }
    """
    token = self.esperar(TokenType.ESTRUCTURA)
    nombre_token = self.esperar(TokenType.IDENTIFICADOR)
    nombre = nombre_token.valor
    
    self.esperar(TokenType.LLAVE_IZQ)
    
    campos = []
    metodos = []
    
    # Parsear campos y métodos hasta encontrar }
    while not self.verificar(TokenType.LLAVE_DER):
        if self.verificar(TokenType.FUNCION):
            # Es un método
            metodos.append(self.declaracion_funcion())
        elif self.verificar(TokenType.IDENTIFICADOR):
            # Es un campo: nombre_campo: tipo
            nombre_campo_token = self.token_actual
            nombre_campo = nombre_campo_token.valor
            self.avanzar()
            
            self.esperar(TokenType.DOS_PUNTOS)
            
            # Tipo puede ser cualquier identificador (entero, texto, o un tipo custom)
            tipo_token = self.esperar(TokenType.IDENTIFICADOR)
            tipo_nombre = tipo_token.valor
            
            campos.append((nombre_campo, tipo_nombre))
        else:
            self.error(f"Se esperaba campo o método en estructura, encontrado: {self.token_actual.valor if self.token_actual else 'EOF'}")
    
    self.esperar(TokenType.LLAVE_DER)
    
    return DeclaracionEstructura(nombre, campos, metodos, token)


def instancia_estructura(self, nombre_estructura: str, token: Token) -> InstanciaEstructura:
    """Parsea instanciación de estructura
    
    Sintaxis:
        Persona { nombre: "Juan", edad: 30 }
    
    Args:
        nombre_estructura: nombre de la estructura a instanciar
        token: token del identificador de la estructura
    """
    # Ya avanzamos el identificador y estamos en {
    self.esperar(TokenType.LLAVE_IZQ)
    
    inicializadores = []
    
    if not self.verificar(TokenType.LLAVE_DER):
        # Primer inicializador: nombre_campo: valor
        nombre_campo_token = self.esperar(TokenType.IDENTIFICADOR)
        nombre_campo = nombre_campo_token.valor
        self.esperar(TokenType.DOS_PUNTOS)
        valor = self.expresion()
        inicializadores.append((nombre_campo, valor))
        
        # Siguientes inicializadores separados por comas
        while self.verificar(TokenType.COMA):
            self.avanzar()
            
            # Coma final opcional
            if self.verificar(TokenType.LLAVE_DER):
                break
                
            nombre_campo_token = self.esperar(TokenType.IDENTIFICADOR)
            nombre_campo = nombre_campo_token.valor
            self.esperar(TokenType.DOS_PUNTOS)
            valor = self.expresion()
            inicializadores.append((nombre_campo, valor))
    
    self.esperar(TokenType.LLAVE_DER)
    
    return InstanciaEstructura(nombre_estructura, inicializadores, token)


# ============================================================================
# EXAMPLE USAGE (for testing)
# ============================================================================

if __name__ == "__main__":
    print("Este archivo contiene métodos para agregar a src/parser.py")
    print("Ver instrucciones de integración al inicio del archivo")
