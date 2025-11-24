import sys
sys.path.insert(0, 'src')
try:
    from lexer import tokenizar_codigo
    from parser import Parser
    print("Imports OK")
    tokens = tokenizar_codigo('importar "hola"')
    parser = Parser(tokens)
    ast = parser.parsear()
    print(ast)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
