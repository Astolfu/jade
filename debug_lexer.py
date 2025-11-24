import sys
sys.path.insert(0, 'src')
try:
    from lexer import tokenizar_codigo
    from token_types import TokenType
    print("Imports OK")
    tokens = tokenizar_codigo('importar "hola"')
    print(tokens)
    for t in tokens:
        print(f"{t.tipo}: {t.valor}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
