# Dado que las herramientas automáticas tienen problemas con parser.py,
# voy a crear un archivo de configuración simple con las líneas exactas donde hacer cada edit
# y después puede ser integrado manualmente o con un script más simple

EDIT_LOCATIONS = {
    'edit_1_declaracion_alto_nivel': {
        'search': 'elif self.verificar(TokenType.VARIABLE, TokenType.CONSTANTE):',
        'insert_before': '''        elif self.verificar(TokenType.ESTRUCTURA):
            return self.declaracion_estructura()
''',
        'line_approx': 70
    },
    
    'edit_2_este_keyword': {
        'search': '# Identificadores',
        'context': 'def expresion_primaria',
        'insert_before': '''        # Este (self-reference)
        if self.verificar(TokenType.ESTE):
            token = self.token_actual
            self.avanzar()
            return IdentificadorEste(token)
        
''',
        'line_approx': 497
    },
    
    'edit_3_struct_instance': {
        'search': 'return Identificador(nombre, token)',
       'context': 'def expresion_primaria',
        'replace_with': '''            
            # Verificar si es instancia de estructura: NombreEstructura { ... }
            if self.verificar(TokenType.LLAVE_IZQ):
                return self.instancia_estructura(nombre, token)
            
            return Identificador(nombre, token)''',
        'line_approx': 503
    },
   
    'edit_4_field_access': {
        'description': 'In expresion_postfija, around line 434, modify the PUNTO (.) handling',
        'old_section_start': 'elif self.verificar(TokenType.PUNTO):',
        'old_section_end': 'expr = LlamadaMetodo',
        'replace_section': '''        elif self.verificar(TokenType.PUNTO):
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
                expr = AccesoCampo(expr, nombre, token_nombre)''',
        'line_approx': 434
    }
}

# Las dos funciones nuevas se agregan al final, antes de "def parsear_codigo"
NEW_METHODS = '''    def declaracion_estructura(self) -> DeclaracionEstructura:
        """Parsea una declaración de estructura"""
        token = self.esperar(TokenType.ESTRUCTURA)
        nombre_token = self.esperar(TokenType.IDENTIFICADOR)
        nombre = nombre_token.valor
        
        self.esperar(TokenType.LLAVE_IZQ)
        
        campos = []
        metodos = []
        
        while not self.verificar(TokenType.LLAVE_DER):
            if self.verificar(TokenType.FUNCION):
                metodos.append(self.declaracion_funcion())
            elif self.verificar(TokenType.IDENTIFICADOR):
                nombre_campo_token = self.token_actual
                nombre_campo = nombre_campo_token.valor
                self.avanzar()
                self.esperar(TokenType.DOS_PUNTOS)
                tipo_token = self.esperar(TokenType.IDENTIFICADOR)
                tipo_nombre = tipo_token.valor
                campos.append((nombre_campo, tipo_nombre))
            else:
                self.error(f"Se esperaba campo o método en estructura")
        
        self.esperar(TokenType.LLAVE_DER)
        return DeclaracionEstructura(nombre, campos, metodos, token)
    
    def instancia_estructura(self, nombre_estructura: str, token: Token) -> InstanciaEstructura:
        """Parsea instanciación de estructura"""
        self.esperar(TokenType.LLAVE_IZQ)
        inicializadores = []
        if not self.verificar(TokenType.LLAVE_DER):
            nombre_campo_token = self.esperar(TokenType.IDENTIFICADOR)
            nombre_campo = nombre_campo_token.valor
            self.esperar(TokenType.DOS_PUNTOS)
            valor = self.expresion()
            inicializadores.append((nombre_campo, valor))
            while self.verificar(TokenType.COMA):
                self.avanzar()
                if self.verificar(TokenType.LLAVE_DER):
                    break
                nombre_campo_token = self.esperar(TokenType.IDENTIFICADOR)
                nombre_campo = nombre_campo_token.valor
                self.esperar(TokenType.DOS_PUNTOS)
                valor = self.expresion()
                inicializadores.append((nombre_campo, valor))
        self.esperar(TokenType.LLAVE_DER)
        return InstanciaEstructura(nombre_estructura, inicializadores, token)
    

'''

print("Parser edit configuration created")
print("See parser_structures.py for complete methods")
print("Follow parser_integration_guide.md for manual integration")
