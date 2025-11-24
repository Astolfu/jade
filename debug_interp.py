import sys
sys.path.insert(0, 'src')
try:
    print("Importing interpreter...")
    from interpreter import InterpreteJade
    print("Interpreter imported")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
