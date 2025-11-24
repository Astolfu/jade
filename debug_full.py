import sys
sys.path.insert(0, 'src')
try:
    from lexer import tokenizar_codigo
    from parser import parsear_codigo
    from interpreter import InterpreteJade
    
    archivo = 'examples/modulo_main.jde'
    print(f"Reading {archivo}...")
    codigo = open(archivo, encoding='utf-8').read()
    
    print("Tokenizing...")
    tokens = tokenizar_codigo(codigo)
    print(f"Tokens: {len(tokens)}")
    for t in tokens:
        print(t)
    
    print("Parsing...")
    ast = parsear_codigo(tokens)
    print("AST created")
    
    print("Executing...")
    interp = InterpreteJade(archivo)
    interp.ejecutar_programa(ast)
    print("Execution finished")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
