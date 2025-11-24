# CHECKLIST DE INTEGRACIÓN MANUAL - Parser Structures

Sigue estos pasos en orden. Cada cambio es pequeño y específico.

## ANTES DE EMPEZAR
1. Abre `src/parser.py` en tu editor
2. Asegúrate de tener guardado todo

## CAMBIO 1: declaracion_alto_nivel (línea ~70)

Busca:
```python
elif self.verificar(TokenType.VARIABLE, TokenType.CONSTANTE):
```

Agrega ANTES de esa línea:
```python
        elif self.verificar(TokenType.ESTRUCTURA):
            return self.declaracion_estructura()
```

## CAMBIO 2: expresion_primaria - ESTE keyword (línea ~497)

Busca el comentario:
```python
        # Identificadores
```

Agrega ANTES de ese comentario:
```python
        # Este (self-reference)
        if self.verificar(TokenType.ESTE):
            token = self.token_actual
            self.avanzar()
            return IdentificadorEste(token)
        
```

## CAMBIO 3: expresion_primaria - Instanciación (línea ~503)

Busca:
```python
            return Identificador(nombre, token)
```

REEMPLAZA con:
```python
            
            # Verificar si es instancia de estructura: NombreEstructura { ... }
            if self.verificar(TokenType.LLAVE_IZQ):
                return self.instancia_estructura(nombre, token)
            
            return Identificador(nombre, token)
```

## CAMBIO 4: expresion_postfija - Acceso a campos (línea ~434-450)

Busca la sección que empieza con:
```python
        elif self.verificar(TokenType.PUNTO):
            # Llamada a método
```

REEMPLAZA toda esa sección (hasta `expr = LlamadaMetodo(...)`) con:
```python
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
```

## CAMBIO 5 & 6: Agregar métodos nuevos (ANTES de línea 560)

Busca:
```python
def parsear_codigo(tokens: List[Token]) -> Programa:
```

Agrega ANTES de esa función (copia desde `src/parser_structures.py`):
- El método `declaracion_estructura()`
- El método `instancia_estructura()`

## VERIFICAR

Ejecuta:
```bash
python verify_parser.py
```

Si todo está bien, verás ✅ para cada check.

## PROBAR

```bash
python src/main.py examples/test_estructuras_basic.jde --parse
```

Debería parsear sin errores.
