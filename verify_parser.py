#!/usr/bin/env python3
"""
Verification script for parser integration
Checks that all necessary changes were made to parser.py
"""

def verify_parser_integration():
    print("🔍 Verificando integración del parser...\n")
    
    with open('src/parser.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("✓ ESTRUCTURA en declaracion_alto_nivel", 
         "TokenType.ESTRUCTURA" in content and "return self.declaracion_estructura()" in content),
        
        ("✓ ESTE keyword en expresion_primaria", 
         "TokenType.ESTE" in content and "return IdentificadorEste(token)" in content),
        
        ("✓ Instanciación de estructuras",
         "instancia_estructura(nombre, token)" in content),
        
        ("✓ Acceso a campos (AccesoCampo)",
         "AccesoCampo(expr, nombre, token_nombre)" in content),
        
        ("✓ Método declaracion_estructura existe",
         "def declaracion_estructura(self)" in content),
        
        ("✓ Método instancia_estructura existe",
         "def instancia_estructura(self, nombre_estructura" in content),
    ]
    
    all_passed = True
    for description, passed in checks:
        if passed:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 ¡Todos los checks pasaron! Parser integrado correctamente.")
        print("\nPrueba con:")
        print("  python src/main.py examples/test_estructuras_basic.jde --parse")
        return 0
    else:
        print("⚠️  Algunos checks fallaron. Revisa INTEGRATION_CHECKLIST.md")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(verify_parser_integration())
