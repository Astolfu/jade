"""
Parser (Analizador Sint├íctico) para Jade
Construye un AST a partir de tokens
"""

from typing import List, Optional
from token_types import Token, TokenType
from ast_nodes import *


class Parser:
    """Parser recursivo descendente para Jade"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.posicion = 0
        self.token_actual = self.tokens[0] if len(self.tokens) > 0 else None
    
    def error(self, mensaje: str):
        """Lanza un error de sintaxis"""
        if self.token_actual:
            raise SyntaxError(
                f"Error de sintaxis en l├¡nea {self.token_actual.linea}, "
                f"columna {self.token_actual.columna}: {mensaje}"
            )
        else:
            raise SyntaxError(f"Error de sintaxis: {mensaje}")
    
    def avanzar(self):
        """Avanza al siguiente token"""
        self.posicion += 1
        if self.posicion < len(self.tokens):
            self.token_actual = self.tokens[self.posicion]
        else:
            self.token_actual = None
    
    def esperar(self, tipo: TokenType) -> Token:
        """Verifica que el token actual sea del tipo esperado y avanza"""
        if not self.token_actual or self.token_actual.tipo != tipo:
            self.error(f"Se esperaba {tipo.name}, pero se encontr├│ {self.token_actual.tipo.name if self.token_actual else 'EOF'}")
        token = self.token_actual
        self.avanzar()
        return token
    
    def verificar(self, *tipos: TokenType) -> bool:
        """Verifica si el token actual es de uno de los tipos dados"""
        if not self.token_actual:
            return False
        return self.token_actual.tipo in tipos
    
    # ========================================================================
    # PROGRAMA Y DECLARACIONES
    # ========================================================================
    
    def parsear(self) -> Programa:
        """Parsea el programa completo"""
        declaraciones = []
        
        while self.token_actual and self.token_actual.tipo != TokenType.EOF:
            decl = self.declaracion_alto_nivel()
            if decl:
                declaraciones.append(decl)
        
        return Programa(declaraciones)
    
    def declaracion_alto_nivel(self):
        """Parsea declaraciones de alto nivel (funciones, variables globales)"""
        if self.verificar(TokenType.FUNCION):
            return self.declaracion_funcion()
        elif self.verificar(TokenType.VARIABLE, TokenType.CONSTANTE):
            return self.declaracion_variable()
        else:
            self.error(f"Declaraci├│n inesperada: {self.token_actual.valor}")
    
    def declaracion_funcion(self) -> DeclaracionFuncion:
        """Parsea una declaraci├│n de funci├│n"""
        token_funcion = self.esperar(TokenType.FUNCION)
        nombre_token = self.esperar(TokenType.IDENTIFICADOR)
        nombre = nombre_token.valor
        
        self.esperar(TokenType.PARENTESIS_IZQ)
        
        # Par├ímetros
        parametros = []
        if not self.verificar(TokenType.PARENTESIS_DER):
            parametros.append(self.parametro())
            while self.verificar(TokenType.COMA):
                self.avanzar()
                parametros.append(self.parametro())
        
        self.esperar(TokenType.PARENTESIS_DER)
        
        # Tipo de retorno opcional (futuro)
        tipo_retorno = None
        
        # Cuerpo de la funci├│n
        cuerpo = self.bloque()
        
        self.esperar(TokenType.FIN)
        
        return DeclaracionFuncion(nombre, parametros, tipo_retorno, cuerpo, token_funcion)
    
    def parametro(self) -> tuple:
        """Parsea un par├ímetro de funci├│n"""
        # Puede ser: nombre o tipo nombre
        tipo = None
        
        # Verificar si hay tipo expl├¡cito
        if self.verificar(TokenType.ENTERO, TokenType.FLOTANTE, TokenType.BOOLEANO, 
                          TokenType.TEXTO, TokenType.LISTA, TokenType.MAPA):
            tipo = self.token_actual.valor
            self.avanzar()
        
        nombre_token = self.esperar(TokenType.IDENTIFICADOR)
        nombre = nombre_token.valor
        
        return (nombre, tipo)
    
    def bloque(self) -> List[Statement]:
        """Parsea un bloque de statements"""
        statements = []
        
        while (self.token_actual and 
               not self.verificar(TokenType.FIN, TokenType.SINO, TokenType.EOF)):
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    # ========================================================================
    # STATEMENTS
    # ========================================================================
    
    def statement(self) -> Optional[Statement]:
        """Parsea un statement"""
        if self.verificar(TokenType.VARIABLE, TokenType.CONSTANTE):
            return self.declaracion_variable()
        elif self.verificar(TokenType.SI):
            return self.statement_si()
        elif self.verificar(TokenType.MIENTRAS):
            return self.statement_mientras()
        elif self.verificar(TokenType.PARA):
            return self.statement_para()
        elif self.verificar(TokenType.RETORNAR):
            return self.statement_retornar()
        elif self.verificar(TokenType.ROMPER):
            return self.statement_romper()
        elif self.verificar(TokenType.CONTINUAR):
            return self.statement_continuar()
        elif self.verificar(TokenType.IDENTIFICADOR):
            # Puede ser asignaci├│n o expresi├│n
            return self.asignacion_o_expresion()
        else:
            # Expresi├│n statement
            expr = self.expresion()
            return ExpresionStatement(expr)
    
    def declaracion_variable(self) -> DeclaracionVariable:
        """Parsea declaraci├│n de variable o constante"""
        es_constante = self.verificar(TokenType.CONSTANTE)
        token = self.token_actual
        self.avanzar()  # variable o constante
        
        # Puede ser: variable nombre = valor
        # O: tipo nombre = valor
        tipo_dato = None
        
        # Verificar tipo expl├¡cito
        if self.verificar(TokenType.ENTERO, TokenType.FLOTANTE, TokenType.BOOLEANO, 
                          TokenType.TEXTO, TokenType.LISTA, TokenType.MAPA):
            tipo_dato = self.token_actual.valor
            self.avanzar()
        
        nombre_token = self.esperar(TokenType.IDENTIFICADOR)
        nombre = nombre_token.valor
        
        # Valor inicial (requerido)
        self.esperar(TokenType.ASIGNAR)
        valor = self.expresion()
        
        return DeclaracionVariable(nombre, tipo_dato, valor, es_constante, token)
    
    def asignacion_o_expresion(self) -> Statement:
        """Parsea asignaci├│n o expresi├│n que empieza con identificador"""
        # Mirar adelante para ver si es asignaci├│n
        if self.posicion + 1 < len(self.tokens):
            siguiente = self.tokens[self.posicion + 1]
            if siguiente.tipo in (TokenType.ASIGNAR, TokenType.MAS_IGUAL, 
                                 TokenType.MENOS_IGUAL, TokenType.MULTIPLICAR_IGUAL, 
                                 TokenType.DIVIDIR_IGUAL):
                # Es asignaci├│n simple
                nombre = self.token_actual.valor
                self.avanzar()
                operador = self.token_actual
                self.avanzar()
                valor = self.expresion()
                return Asignacion(nombre, valor, operador)
            elif siguiente.tipo == TokenType.CORCHETE_IZQ:
                # Podr├¡a ser asignaci├│n a ├¡ndice: arr[i] = valor
                objeto = Identificador(self.token_actual.valor, self.token_actual)
                self.avanzar()
                self.esperar(TokenType.CORCHETE_IZQ)
                indice = self.expresion()
                self.esperar(TokenType.CORCHETE_DER)
                
                if self.verificar(TokenType.ASIGNAR):
                    token_asig = self.token_actual
                    self.avanzar()
                    valor = self.expresion()
                    return AsignacionIndice(objeto, indice, valor, token_asig)
                else:
                    # Es solo acceso a ├¡ndice como expresi├│n
                    acc = AccesoIndice(objeto, indice, objeto.token)
                    return ExpresionStatement(acc)
        
        # Es solo una expresi├│n
        expr = self.expresion()
        return ExpresionStatement(expr)
    
    def statement_si(self) -> Si:
        """Parsea statement si/entonces/sino"""
        token_si = self.esperar(TokenType.SI)
        condicion = self.expresion()
        self.esperar(TokenType.ENTONCES)
        
        bloque_entonces = []
        while not self.verificar(TokenType.SINO) and not self.verificar(TokenType.FIN):
            bloque_entonces.append(self.statement())
        
        bloque_sino = None
        if self.verificar(TokenType.SINO):
            self.avanzar()
            # Verificar si es "sino si"
            if self.verificar(TokenType.SI):
                # sino si... -> crear nuevo Si anidado
                bloque_sino = [self.statement_si()]
            else:
                bloque_sino = []
                while not self.verificar(TokenType.FIN):
                    bloque_sino.append(self.statement())
        
        self.esperar(TokenType.FIN)
        return Si(condicion, bloque_entonces, bloque_sino, token_si)
    
    def statement_mientras(self) -> Mientras:
        """Parsea statement mientras"""
        token_mientras = self.esperar(TokenType.MIENTRAS)
        condicion = self.expresion()
        self.esperar(TokenType.HACER)
        
        cuerpo = self.bloque()
        
        self.esperar(TokenType.FIN)
        
        return Mientras(condicion, cuerpo, token_mientras)
    
    def statement_para(self) -> Para:
        """Parsea statement para"""
        token_para = self.esperar(TokenType.PARA)
        
        nombre_var = self.esperar(TokenType.IDENTIFICADOR).valor
        
        self.esperar(TokenType.DESDE)
        inicio = self.expresion()
        
        self.esperar(TokenType.HASTA)
        fin = self.expresion()
        
        self.esperar(TokenType.HACER)
        
        cuerpo = self.bloque()
        
        self.esperar(TokenType.FIN)
        
        return Para(nombre_var, inicio, fin, cuerpo, token_para)
    
    def statement_retornar(self) -> Retornar:
        """Parsea statement retornar"""
        token = self.esperar(TokenType.RETORNAR)
        
        valor = None
        if not self.verificar(TokenType.FIN, TokenType.EOF, TokenType.SINO):
            valor = self.expresion()
        
        return Retornar(valor, token)
    
    def statement_romper(self) -> Romper:
        """Parsea statement romper"""
        token = self.esperar(TokenType.ROMPER)
        return Romper(token)
    
    def statement_continuar(self) -> Continuar:
        """Parsea statement continuar"""
        token = self.esperar(TokenType.CONTINUAR)
        return Continuar(token)
    
    # ========================================================================
    # EXPRESIONES (con precedencia)
    # ========================================================================
    
    def expresion(self) -> Expresion:
        """Parsea una expresi├│n (precedencia m├ís baja: or l├│gico)"""
        return self.expresion_logica_o()
    
    def expresion_logica_o(self) -> Expresion:
        """Parsea OR l├│gico"""
        izq = self.expresion_logica_y()
        
        while self.verificar(TokenType.O):
            op = self.token_actual
            self.avanzar()
            der = self.expresion_logica_y()
            izq = ExpresionBinaria(izq, op, der)
        
        return izq
    
    def expresion_logica_y(self) -> Expresion:
        """Parsea AND l├│gico"""
        izq = self.expresion_igualdad()
        
        while self.verificar(TokenType.Y):
            op = self.token_actual
            self.avanzar()
            der = self.expresion_igualdad()
            izq = ExpresionBinaria(izq, op, der)
        
        return izq
    
    def expresion_igualdad(self) -> Expresion:
        """Parsea comparaciones de igualdad"""
        izq = self.expresion_comparacion()
        
        while self.verificar(TokenType.IGUAL, TokenType.DIFERENTE):
            op = self.token_actual
            self.avanzar()
            der = self.expresion_comparacion()
            izq = ExpresionBinaria(izq, op, der)
        
        return izq
    
    def expresion_comparacion(self) -> Expresion:
        """Parsea comparaciones relacionales"""
        izq = self.expresion_aditiva()
        
        while self.verificar(TokenType.MENOR, TokenType.MAYOR, 
                            TokenType.MENOR_IGUAL, TokenType.MAYOR_IGUAL):
            op = self.token_actual
            self.avanzar()
            der = self.expresion_aditiva()
            izq = ExpresionBinaria(izq, op, der)
        
        return izq
    
    def expresion_aditiva(self) -> Expresion:
        """Parsea suma y resta"""
        izq = self.expresion_multiplicativa()
        
        while self.verificar(TokenType.MAS, TokenType.MENOS):
            op = self.token_actual
            self.avanzar()
            der = self.expresion_multiplicativa()
            izq = ExpresionBinaria(izq, op, der)
        
        return izq
    
    def expresion_multiplicativa(self) -> Expresion:
        """Parsea multiplicaci├│n, divisi├│n y m├│dulo"""
        izq = self.expresion_potencia()
        
        while self.verificar(TokenType.MULTIPLICAR, TokenType.DIVIDIR, TokenType.MODULO):
            op = self.token_actual
            self.avanzar()
            der = self.expresion_potencia()
            izq = ExpresionBinaria(izq, op, der)
        
        return izq
    
    def expresion_potencia(self) -> Expresion:
        """Parsea potenciaci├│n"""
        izq = self.expresion_unaria()
        
        if self.verificar(TokenType.POTENCIA):
            op = self.token_actual
            self.avanzar()
            # Potencia es asociativa a la derecha
            der = self.expresion_potencia()
            return ExpresionBinaria(izq, op, der)
        
        return izq
    
    def expresion_unaria(self) -> Expresion:
        """Parsea expresiones unarias"""
        if self.verificar(TokenType.MENOS, TokenType.NO):
            op = self.token_actual
            self.avanzar()
            expr = self.expresion_unaria()
            return ExpresionUnaria(op, expr)
        
        return self.expresion_postfija()
    
    def expresion_postfija(self) -> Expresion:
        """Parsea llamadas a funci├│n y acceso a ├¡ndice"""
        expr = self.expresion_primaria()
        
        while True:
            if self.verificar(TokenType.PARENTESIS_IZQ):
                # Llamada a funci├│n
                token = self.token_actual
                self.avanzar()
                
                argumentos = []
                if not self.verificar(TokenType.PARENTESIS_DER):
                    argumentos.append(self.expresion())
                    while self.verificar(TokenType.COMA):
                        self.avanzar()
                        argumentos.append(self.expresion())
                
                self.esperar(TokenType.PARENTESIS_DER)
                
                # expr debe ser un identificador
                if isinstance(expr, Identificador):
                    expr = LlamadaFuncion(expr.nombre, argumentos, token)
                else:
                    self.error("Solo se puede llamar a funciones con nombre")
            
            elif self.verificar(TokenType.CORCHETE_IZQ):
                # Acceso a ├¡ndice
                token = self.token_actual
                self.avanzar()
                indice = self.expresion()
                self.esperar(TokenType.CORCHETE_DER)
                expr = AccesoIndice(expr, indice, token)
            
            else:
                break
        
        return expr
    
    def expresion_primaria(self) -> Expresion:
        """Parsea expresiones primarias (literales, identificadores, etc.)"""
        # Literales num├®ricos
        if self.verificar(TokenType.LITERAL_ENTERO):
            token = self.token_actual
            valor = int(token.valor)
            self.avanzar()
            return LiteralEntero(valor, token)
        
        if self.verificar(TokenType.LITERAL_FLOTANTE):
            token = self.token_actual
            valor = float(token.valor)
            self.avanzar()
            return LiteralFlotante(valor, token)
        
        # Literales de texto
        if self.verificar(TokenType.LITERAL_TEXTO):
            token = self.token_actual
            self.avanzar()
            return LiteralTexto(token.valor, token)
        
        # Booleanos
        if self.verificar(TokenType.VERDADERO):
            token = self.token_actual
            self.avanzar()
            return LiteralBooleano(True, token)
        
        if self.verificar(TokenType.FALSO):
            token = self.token_actual
            self.avanzar()
            return LiteralBooleano(False, token)
        
        # Nulo
        if self.verificar(TokenType.NULO):
            token = self.token_actual
            self.avanzar()
            return LiteralNulo(token)
        
        # Identificadores
        if self.verificar(TokenType.IDENTIFICADOR):
            token = self.token_actual
            nombre = token.valor
            self.avanzar()
            return Identificador(nombre, token)
        
        # Listas
        if self.verificar(TokenType.CORCHETE_IZQ):
            return self.expresion_lista()
        
        # Mapas
        if self.verificar(TokenType.LLAVE_IZQ):
            return self.expresion_mapa()
        
        # Expresiones entre par├®ntesis
        if self.verificar(TokenType.PARENTESIS_IZQ):
            self.avanzar()
            expr = self.expresion()
            self.esperar(TokenType.PARENTESIS_DER)
            return expr
        
        self.error(f"Expresi├│n inesperada: {self.token_actual.valor if self.token_actual else 'EOF'}")
    
    def expresion_lista(self) -> LiteralLista:
        """Parsea literal de lista [1, 2, 3]"""
        token = self.esperar(TokenType.CORCHETE_IZQ)
        
        elementos = []
        if not self.verificar(TokenType.CORCHETE_DER):
            elementos.append(self.expresion())
            while self.verificar(TokenType.COMA):
                self.avanzar()
                if self.verificar(TokenType.CORCHETE_DER):  # Coma final opcional
                    break
                elementos.append(self.expresion())
        
        self.esperar(TokenType.CORCHETE_DER)
        return LiteralLista(elementos, token)
    
    def expresion_mapa(self) -> LiteralMapa:
        """Parsea literal de mapa {clave: valor}"""
        token = self.esperar(TokenType.LLAVE_IZQ)
        
        pares = []
        if not self.verificar(TokenType.LLAVE_DER):
            # Primer par
            clave = self.expresion()
            self.esperar(TokenType.DOS_PUNTOS)
            valor = self.expresion()
            pares.append((clave, valor))
            
            while self.verificar(TokenType.COMA):
                self.avanzar()
                if self.verificar(TokenType.LLAVE_DER):  # Coma final opcional
                    break
                clave = self.expresion()
                self.esperar(TokenType.DOS_PUNTOS)
                valor = self.expresion()
                pares.append((clave, valor))
        
        self.esperar(TokenType.LLAVE_DER)
        return LiteralMapa(pares, token)


def parsear_codigo(tokens: List[Token]) -> Programa:
    """Funci├│n de utilidad para parsear tokens"""
    parser = Parser(tokens)
    return parser.parsear()
