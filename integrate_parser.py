#!/usr/bin/env python3
"""
Script to integrate structure support into parser.py
This script makes precise edits to avoid file corruption.
"""

def integrate_structures():
    # Read the original parser.py
    with open('src/parser.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Track modifications
    modified_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Edit 1: Add ESTRUCTURA case in declaracion_alto_nivel (around line 70)
        if 'elif self.verificar(TokenType.VARIABLE, TokenType.CONSTANTE):' in line and i > 65 and i < 75:
            # Insert before this line
            modified_lines.append('        elif self.verificar(TokenType.ESTRUCTURA):\r\n')
            modified_lines.append('            return self.declaracion_estructura()\r\n')
            modified_lines.append(line)
            i += 1
            continue
        
        # Edit 2 & 3: Modify expresion_primaria for ESTE and struct instantiation
        if '# Identificadores' in line and 'expresion_primaria' in ''.join(lines[max(0,i-20):i]):
            # Add ESTE check before Identificadores
            modified_lines.append('        # Este (self-reference)\r\n')
            modified_lines.append('        if self.verificar(TokenType.ESTE):\r\n')
            modified_lines.append('            token = self.token_actual\r\n')
            modified_lines.append('            self.avanzar()\r\n')
            modified_lines.append('            return IdentificadorEste(token)\r\n')
            modified_lines.append('        \r\n')
            modified_lines.append(line)
            i += 1
            
            # Now modify the IDENTIFICADOR section (next few lines)
            while i < len(lines) and 'return Identificador(nombre, token)' not in lines[i]:
                modified_lines.append(lines[i])
                i += 1
            
            # Replace the return with struct check
            if i < len(lines):
                modified_lines.append('            \r\n')
                modified_lines.append('            # Verificar si es instancia de estructura: NombreEstructura { ... }\r\n')
                modified_lines.append('            if self.verificar(TokenType.LLAVE_IZQ):\r\n')
                modified_lines.append('                return self.instancia_estructura(nombre, token)\r\n')
                modified_lines.append('            \r\n')
                modified_lines.append(lines[i])  # Original return Identificador
                i += 1
            continue
        
        # Edit 4: Modify expresion_postfija PUNTO handling for field access
        if '# Llamada a método' in line and 'elif self.verificar(TokenType.PUNTO):' in ''.join(lines[max(0,i-2):i+1]):
            # Replace method call section with field/method distinction
            modified_lines.append('            # Acceso a campo o método\r\n')
            i += 1
            # Skip to nombre_metodo line
            while i < len(lines) and 'nombre_metodo = token_nombre.valor' not in lines[i]:
                if 'self.avanzar()' in lines[i] or 'token_nombre = self.esperar' in lines[i]:
                    modified_lines.append(lines[i])
                i += 1
            
            # Replace nombre_metodo with nombre
            modified_lines.append('            nombre = token_nombre.valor\r\n')
            modified_lines.append('            \r\n')
            modified_lines.append('            # Verificar si es método (tiene paréntesis) o campo\r\n')
            modified_lines.append('            if self.verificar(TokenType.PARENTESIS_IZQ):\r\n')
            modified_lines.append('                # Llamada a método\r\n')
            i += 1
            
            # Skip self.esperar(PARENTESIS_IZQ) since we check it above
            if i < len(lines) and 'self.esperar(TokenType.PARENTESIS_IZQ)' in lines[i]:
                modified_lines.append('                self.avanzar()\r\n')
                i += 1
            
            # Copy the rest of method call handling with proper indentation
            while i < len(lines) and 'expr = LlamadaMetodo' not in lines[i]:
                modified_lines.append('    ' + lines[i])  # Add extra indent
                i += 1
            
            if i < len(lines):
                # Modify LlamadaMetodo to use 'nombre' instead of 'nombre_metodo'
                method_line = lines[i].replace('nombre_metodo', 'nombre')
                modified_lines.append('    ' + method_line)
                i += 1
            
            # Add field access case
            modified_lines.append('            else:\r\n')
            modified_lines.append('                # Acceso a campo\r\n')
            modified_lines.append('                expr = AccesoCampo(expr, nombre, token_nombre)\r\n')
            continue
        
        # Default: keep line as-is
        modified_lines.append(line)
        i += 1
    
    # Find where to add new methods (before def parsear_codigo)
    final_lines = []
    for i, line in enumerate(modified_lines):
        if 'def parsear_codigo(tokens: List[Token])' in line:
            # Insert new methods here
            final_lines.append('    def declaracion_estructura(self) -> DeclaracionEstructura:\r\n')
            final_lines.append('        """Parsea una declaración de estructura"""\r\n')
            final_lines.append('        token = self.esperar(TokenType.ESTRUCTURA)\r\n')
            final_lines.append('        nombre_token = self.esperar(TokenType.IDENTIFICADOR)\r\n')
            final_lines.append('        nombre = nombre_token.valor\r\n')
            final_lines.append('        \r\n')
            final_lines.append('        self.esperar(TokenType.LLAVE_IZQ)\r\n')
            final_lines.append('        \r\n')
            final_lines.append('        campos = []\r\n')
            final_lines.append('        metodos = []\r\n')
            final_lines.append('        \r\n')
            final_lines.append('        while not self.verificar(TokenType.LLAVE_DER):\r\n')
            final_lines.append('            if self.verificar(TokenType.FUNCION):\r\n')
            final_lines.append('                metodos.append(self.declaracion_funcion())\r\n')
            final_lines.append('            elif self.verificar(TokenType.IDENTIFICADOR):\r\n')
            final_lines.append('                nombre_campo_token = self.token_actual\r\n')
            final_lines.append('                nombre_campo = nombre_campo_token.valor\r\n')
            final_lines.append('                self.avanzar()\r\n')
            final_lines.append('                self.esperar(TokenType.DOS_PUNTOS)\r\n')
            final_lines.append('                tipo_token = self.esperar(TokenType.IDENTIFICADOR)\r\n')
            final_lines.append('                tipo_nombre = tipo_token.valor\r\n')
            final_lines.append('                campos.append((nombre_campo, tipo_nombre))\r\n')
            final_lines.append('            else:\r\n')
            final_lines.append('                self.error(f"Se esperaba campo o método en estructura")\r\n')
            final_lines.append('        \r\n')
            final_lines.append('        self.esperar(TokenType.LLAVE_DER)\r\n')
            final_lines.append('        return DeclaracionEstructura(nombre, campos, metodos, token)\r\n')
            final_lines.append('    \r\n')
            final_lines.append('    def instancia_estructura(self, nombre_estructura: str, token: Token) -> InstanciaEstructura:\r\n')
            final_lines.append('        """Parsea instanciación de estructura"""\r\n')
            final_lines.append('        self.esperar(TokenType.LLAVE_IZQ)\r\n')
            final_lines.append('        inicializadores = []\r\n')
            final_lines.append('        if not self.verificar(TokenType.LLAVE_DER):\r\n')
            final_lines.append('            nombre_campo_token = self.esperar(TokenType.IDENTIFICADOR)\r\n')
            final_lines.append('            nombre_campo = nombre_campo_token.valor\r\n')
            final_lines.append('            self.esperar(TokenType.DOS_PUNTOS)\r\n')
            final_lines.append('            valor = self.expresion()\r\n')
            final_lines.append('            inicializadores.append((nombre_campo, valor))\r\n')
            final_lines.append('            while self.verificar(TokenType.COMA):\r\n')
            final_lines.append('                self.avanzar()\r\n')
            final_lines.append('                if self.verificar(TokenType.LLAVE_DER):\r\n')
            final_lines.append('                    break\r\n')
            final_lines.append('                nombre_campo_token = self.esperar(TokenType.IDENTIFICADOR)\r\n')
            final_lines.append('                nombre_campo = nombre_campo_token.valor\r\n')
            final_lines.append('                self.esperar(TokenType.DOS_PUNTOS)\r\n')
            final_lines.append('                valor = self.expresion()\r\n')
            final_lines.append('                inicializadores.append((nombre_campo, valor))\r\n')
            final_lines.append('        self.esperar(TokenType.LLAVE_DER)\r\n')
            final_lines.append('        return InstanciaEstructura(nombre_estructura, inicializadores, token)\r\n')
            final_lines.append('    \r\n')
            final_lines.append('\r\n')
        
        final_lines.append(line)
    
    # Write modified parser.py
    with open('src/parser.py', 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    
    print("✅ Parser successfully modified!")
    print("Changes made:")
    print("  1. Added ESTRUCTURA case in declaracion_alto_nivel()")
    print("  2. Added ESTE keyword support in expresion_primaria()")
    print("  3. Added struct instantiation check in expresion_primaria()")
    print("  4. Modified PUNTO handling for field vs method access")
    print("  5. Added declaracion_estructura() method")
    print("  6. Added instancia_estructura() method")

if __name__ == '__main__':
    try:
        integrate_structures()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
