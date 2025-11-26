import sys
import os
import traceback

# Add src to path
sys.path.insert(0, 'src')

try:
    from interpreter import InterpreteJade
    from lexer import tokenizar_codigo
    from parser import parsear_codigo
except ImportError:
    print("Error: Could not import Jade modules. Make sure you are in the root directory.")
    sys.exit(1)

def run_test(filename):
    print(f"\n{'='*50}")
    print(f"Running test: {filename}")
    print(f"{'='*50}")
    
    try:
        filepath = os.path.join('examples', filename)
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} not found")
            return False
            
        with open(filepath, 'r', encoding='utf-8') as f:
            codigo = f.read()
            
        tokens = tokenizar_codigo(codigo)
        ast = parsear_codigo(tokens)
        
        interp = InterpreteJade(filepath)
        interp.ejecutar_programa(ast)
        
        print(f"\n[SUCCESS] {filename} passed")
        return True
        
    except Exception as e:
        print(f"\n[FAILURE] {filename} failed")
        print(f"Error: {e}")
        # traceback.print_exc()
        return False

def main():
    tests = [
        'hola_mundo.jde',
        'suma.jde',
        'listas.jde',
        'mapas.jde',
        'test_interpolation.jde',
        'modulo_main.jde',
        'test_enums.jde',
        'test_strings.jde'
    ]
    
    passed = 0
    failed = 0
    
    print("Starting Regression Tests...")
    
    for test in tests:
        if run_test(test):
            passed += 1
        else:
            failed += 1
            
    print(f"\n{'='*50}")
    print(f"Test Summary")
    print(f"{'='*50}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {len(tests)}")
    
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
