"""
REPL (Read-Eval-Print Loop) Interactivo para Jade
Permite ejecutar código Jade de forma interactiva
"""

import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


class JadeREPL:
    """REPL interactivo para Jade"""
    
    def __init__(self):
        self.interpreter = Interpreter()
        self.historial = []
        self.buffer_multilinea = []
        
    def banner(self):
        """Muestra el banner de bienvenida"""
        print("╔═══════════════════════════════════════╗")
        print("║     Jade REPL v1.0                    ║")
        print("║     Lenguaje de Programación en      ║")
        print("║     Español                           ║")
        print("╚═══════════════════════════════════════╝")
        print()
        print("Escribe código Jade o usa comandos:")
        print("  :ayuda  - Mostrar ayuda")
        print("  :salir  - Salir del REPL")
        print("  :vars   - Ver variables definidas")
        print("  :limpiar - Limpiar variables")
        print()
    
    def run(self):
        """Loop principal del REPL"""
        self.banner()
        
        while True:
            try:
                # Determinar prompt
                if self.buffer_multilinea:
                    prompt = "... "
                else:
                    prompt = ">>> "
                
                # Leer línea
                linea = input(prompt).strip()
                
                # Agregar al historial
                if linea:
                    self.historial.append(linea)
                
                # Procesar
                if self.buffer_multilinea:
                    # Modo multi-línea
                    self.buffer_multilinea.append(linea)
                    codigo_completo = '\n'.join(self.buffer_multilinea)
                    
                    # Verificar si ya está completo
                    if not self.necesita_mas_lineas(codigo_completo):
                        self.evaluar(codigo_completo)
                        self.buffer_multilinea = []
                else:
                    # Comando especial o código normal
                    if linea.startswith(':'):
                        self.procesar_comando(linea)
                    elif linea:
                        # Verificar si necesita más líneas
                        if self.necesita_mas_lineas(linea):
                            self.buffer_multilinea.append(linea)
                        else:
                            self.evaluar(linea)
                            
            except KeyboardInterrupt:
                print("\n(Usa :salir para salir)")
                self.buffer_multilinea = []
            except EOFError:
                print("\n¡Adiós!")
                break
    
    def procesar_comando(self, comando):
        """Procesa comandos especiales del REPL"""
        cmd = comando.lower()
        
        if cmd in [':salir', ':q', ':quit', ':exit']:
            print("¡Adiós!")
            sys.exit(0)
            
        elif cmd in [':ayuda', ':h', ':help']:
            self.mostrar_ayuda()
            
        elif cmd in [':vars', ':variables']:
            self.mostrar_variables()
            
        elif cmd in [':limpiar', ':c', ':clear']:
            self.interpreter = Interpreter()
            print("Variables limpiadas")
            
        elif cmd in [':reset', ':r']:
            self.interpreter = Interpreter()
            self.historial = []
            print("REPL reiniciado")
            
        elif cmd in [':historial', ':hist']:
            self.mostrar_historial()
            
        else:
            print(f"Comando desconocido: {comando}")
            print("Usa :ayuda para ver comandos disponibles")
    
    def mostrar_ayuda(self):
        """Muestra ayuda de comandos"""
        print("\n=== Comandos del REPL ===")
        print(":salir, :q        - Salir del REPL")
        print(":ayuda, :h        - Mostrar esta ayuda")
        print(":vars             - Ver variables definidas")
        print(":limpiar, :c      - Limpiar todas las variables")
        print(":reset, :r        - Reiniciar REPL completamente")
        print(":historial, :hist - Ver historial de comandos")
        print()
        print("=== Ejemplos ===")
        print(">>> variable x = 5")
        print(">>> x + 10")
        print("15")
        print()
        print(">>> funcion doble(n)")
        print("...   retornar n * 2")
        print("... fin")
        print()
    
    def mostrar_variables(self):
        """Muestra variables definidas"""
        if not self.interpreter.entorno.valores:
            print("No hay variables definidas")
            return
            
        print("\n=== Variables Definidas ===")
        for nombre, valor in self.interpreter.entorno.valores.items():
            # Evitar mostrar funciones built-in
            if not nombre.startswith('_'):
                tipo_val = type(valor).__name__
                print(f"{nombre}: {tipo_val} = {valor}")
        print()
    
    def mostrar_historial(self):
        """Muestra historial de comandos"""
        if not self.historial:
            print("No hay historial")
            return
            
        print("\n=== Historial ===")
        for i, cmd in enumerate(self.historial[-20:], 1):  # Últimos 20
            print(f"{i:2}. {cmd}")
        print()
    
    def necesita_mas_lineas(self, codigo):
        """Detecta si el código necesita más líneas para completarse"""
        # Contar palabras clave de apertura y cierre
        palabras = codigo.lower().split()
        
        aperturas = palabras.count('funcion') + palabras.count('si') + \
                   palabras.count('mientras') + palabras.count('para')
        cierres = palabras.count('fin')
        
        # Si hay más aperturas que cierres, necesita más líneas
        return aperturas > cierres
    
    def evaluar(self, codigo):
        """Evalúa código Jade"""
        try:
            # Tokenizar
            lexer = Lexer(codigo)
            tokens = lexer.tokenizar()
            
            # Parsear
            parser = Parser(tokens)
            ast = parser.parsear()
            
            # Interpretar
            resultado = self.interpreter.interpretar(ast)
            
            # Si hay resultado y no es None, mostrarlo
            if resultado is not None:
                print(resultado)
                
        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Punto de entrada para el REPL"""
    repl = JadeREPL()
    repl.run()


if __name__ == '__main__':
    main()
