"""
Compilador principal de Jade
Coordina todas las fases de compilación
"""

import sys
import os
from pathlib import Path

from lexer import Lexer
from parser import Parser
from semantic_analyzer import AnalizadorSemantico
try:
    from codegen_llvm import GeneradorLLVM, inicializar_llvm
    LLVM_DISPONIBLE = True
except ImportError:
    LLVM_DISPONIBLE = False
    print("Advertencia: llvmlite no esta instalado. Generacion de codigo LLVM deshabilitada.", file=sys.stderr)


class Compilador:
    """Compilador principal de Jade"""
    
    def __init__(self, archivo_entrada: str):
        self.archivo_entrada = archivo_entrada
        self.codigo_fuente = ""
        self.tokens = []
        self.ast = None
        self.errores = []
    
    def leer_archivo(self):
        """Lee el archivo fuente"""
        try:
            with open(self.archivo_entrada, 'r', encoding='utf-8') as f:
                self.codigo_fuente = f.read()
            return True
        except FileNotFoundError:
            self.error(f"Archivo no encontrado: {self.archivo_entrada}")
            return False
        except Exception as e:
            self.error(f"Error al leer archivo: {e}")
            return False
    
    def error(self, mensaje: str):
        """Registra un error"""
        self.errores.append(mensaje)
        print(f"Error: {mensaje}", file=sys.stderr)
    
    def fase_lexica(self):
        """Fase de análisis léxico"""
        print("=== Fase 1: Analisis Lexico ===")
        try:
            lexer = Lexer(self.codigo_fuente)
            self.tokens = lexer.tokenizar()
            print(f"[OK] Generados {len(self.tokens)} tokens")
            return True
        except SyntaxError as e:
            self.error(f"Error léxico: {e}")
            return False
    
    def fase_sintactica(self):
        """Fase de análisis sintáctico"""
        print("=== Fase 2: Analisis Sintactico ===")
        try:
            parser = Parser(self.tokens)
            self.ast = parser.parsear()
            print(f"[OK] AST generado con {len(self.ast.declaraciones)} declaraciones")
            return True
        except SyntaxError as e:
            self.error(f"Error de sintaxis: {e}")
            return False
    
    def fase_semantica(self):
        """Fase de análisis semántico"""
        print("=== Fase 3: Analisis Semantico ===")
        try:
            analizador = AnalizadorSemantico()
            analizador.analizar(self.ast)
            print("[OK] Analisis semantico completado")
            print(f"  - {len(analizador.funciones)} funciones verificadas")
            return True
        except Exception as e:
            self.error(f"Error semántico: {e}")
            return False
    
    def fase_codegen(self, mostrar_ir=False):
        """Fase de generación de código LLVM"""
        print("\n=== Fase 4: Generacion de Codigo LLVM ===")
        
        if not LLVM_DISPONIBLE:
            print("[!] llvmlite no instalado - Generacion de codigo deshabilitada")
            print("    Instalar con: pip install llvmlite")
            return True  # No es error fatal
        
        try:
            # Inicializar LLVM
            inicializar_llvm()
            
            # Asegurar que el análisis semántico se ejecutó (para anotar tipos)
            # Si ya se ejecutó en fase_semantica, self.ast ya tiene tipos?
            # No necesariamente, porque fase_semantica podría no haberse llamado si solo pedimos codegen.
            # Pero compilar() llama a todas en orden.
            # Sin embargo, para estar seguros y si se usa fase_codegen aisladamente:
            # Re-ejecutar análisis semántico sobre el AST actual para garantizar anotaciones
            analizador = AnalizadorSemantico()
            analizador.analizar(self.ast)
            
            # Generar LLVM IR
            generador = GeneradorLLVM()
            llvm_ir = generador.generar(self.ast)
            
            # Guardar IR a archivo
            nombre_base = os.path.splitext(self.archivo_entrada)[0]
            archivo_ll = nombre_base + ".ll"
            
            with open(archivo_ll, 'w') as f:
                f.write(llvm_ir)
            
            print(f"[OK] LLVM IR generado: {archivo_ll}")
            
            if mostrar_ir:
                print("\n=== LLVM IR Generado ===")
                print(llvm_ir[:500])  # Mostrar primeras líneas
                if len(llvm_ir) > 500:
                    print(f"... ({len(llvm_ir)} caracteres totales)")
            
            return True
            
        except Exception as e:
            self.error(f"Error en generacion de codigo: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def mostrar_ast(self):
        """Muestra el AST"""
        print("\n=== Árbol de Sintaxis Abstracta ===")
        self._mostrar_nodo(self.ast, 0)
    
    def _mostrar_nodo(self, nodo, nivel):
        """Muestra un nodo del AST con indentación"""
        indent = "  " * nivel
        print(f"{indent}{nodo}")
        
        # Mostrar hijos según el tipo de nodo
        if hasattr(nodo, 'declaraciones'):
            for decl in nodo.declaraciones:
                self._mostrar_nodo(decl, nivel + 1)
        elif hasattr(nodo, 'cuerpo'):
            for stmt in nodo.cuerpo:
                self._mostrar_nodo(stmt, nivel + 1)
    
    def compilar(self, mostrar_tokens=False, mostrar_ast=False):
        """Ejecuta todas las fases de compilación"""
        print(f"\n>>> Compilando {self.archivo_entrada}...\n")
        
        # Leer archivo
        if not self.leer_archivo():
            return False
        
        # Fase léxica
        if not self.fase_lexica():
            return False
        
        if mostrar_tokens:
            print("\n=== Tokens Generados ===")
            for token in self.tokens[:20]:  # Mostrar solo los primeros 20
                print(f"  {token}")
            if len(self.tokens) > 20:
                print(f"  ... y {len(self.tokens) - 20} más")
        
        # Fase sintáctica
        if not self.fase_sintactica():
            return False
        
        if mostrar_ast:
            self.mostrar_ast()
        
        # Fase semántica
        if not self.fase_semantica():
            return False
        
        # Fase de generación de código LLVM
        print("\n=== Fase 4: Generacion de Codigo LLVM ===")
        
        if not LLVM_DISPONIBLE:
            print("[!] llvmlite no instalado - Generacion de codigo deshabilitada")
            print("    Instalar con: pip install llvmlite")
        else:
            try:
                # Inicializar LLVM
                inicializar_llvm()
                
                # Generar LLVM IR
                generador = GeneradorLLVM()
                llvm_ir = generador.generar(self.ast)
                
                # Guardar IR a archivo
                nombre_base = os.path.splitext(self.archivo_entrada)[0]
                archivo_ll = nombre_base + ".ll"
                
                with open(archivo_ll, 'w') as f:
                    f.write(llvm_ir)
                
                print(f"[OK] LLVM IR generado: {archivo_ll}")
                
                if mostrar_ir:
                    print("\n=== LLVM IR Generado ===")
                    print(llvm_ir[:500])  # Mostrar primeras líneas
                    if len(llvm_ir) > 500:
                        print(f"... ({len(llvm_ir)} caracteres totales)")
                
            except Exception as e:
                self.error(f"Error en generacion de codigo: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        if not self.errores:
            print("\n[OK] Compilacion completada sin errores")
            if LLVM_DISPONIBLE:
                print(f"\nPara generar ejecutable:")
                print(f"  1. Compilar runtime: gcc -c std/runtime.c -o runtime.o")
                print(f"  2. Generar objeto:   llc {nombre_base}.ll -filetype=obj -o {nombre_base}.o")
                print(f"  3. Enlazar:          gcc {nombre_base}.o runtime.o -o {nombre_base}.exe")
            return True
        else:
            print(f"\n[ERROR] Compilacion fallo con {len(self.errores)} errores")
            return False
    
    def compilar(self, mostrar_tokens=False, mostrar_ast=False, mostrar_ir=False):
        """Ejecuta todas las fases de compilación"""
        print(f"\n>>> Compilando {self.archivo_entrada}...\n")
        
        # Leer archivo
        if not self.leer_archivo():
            return False
        
        # Fase léxica
        if not self.fase_lexica():
            return False
        
        if mostrar_tokens:
            print("\n=== Tokens Generados ===")
            for token in self.tokens[:20]:  # Mostrar solo los primeros 20
                print(f"  {token}")
            if len(self.tokens) > 20:
                print(f"  ... y {len(self.tokens) - 20} más")
        
        # Fase sintáctica
        if not self.fase_sintactica():
            return False
        
        if mostrar_ast:
            self.mostrar_ast()
        
        # Fase semántica
        if not self.fase_semantica():
            return False
        
        # Fase de generación de código LLVM
        return self.fase_codegen(mostrar_ir)


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Compilador de Jade - Lenguaje de Programación en Español',
        prog='jade'
    )
    
    parser.add_argument('archivo', help='Archivo .jde a compilar')
    parser.add_argument('--tokens', action='store_true', 
                       help='Mostrar tokens generados')
    parser.add_argument('--ast', action='store_true',
                       help='Mostrar árbol de sintaxis abstracta')
    parser.add_argument('--ir', action='store_true',
                       help='Mostrar LLVM IR generado')
    parser.add_argument('--version', action='version',
                       version='Jade 0.1.0')
    
    args = parser.parse_args()
    
    # Verificar extensión
    if not args.archivo.endswith('.jde'):
        print("Advertencia: El archivo no tiene extensión .jde", file=sys.stderr)
    
    # Compilar
    compilador = Compilador(args.archivo)
    exito = compilador.compilar(
        mostrar_tokens=args.tokens,
        mostrar_ast=args.ast,
        mostrar_ir=args.ir
    )
    
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
