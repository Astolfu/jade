"""
CLI        # 4. Generación de código
"""

from compiler import main

if __name__ == "__main__":
    main()
# The following code snippet was provided by the user, but its context (e.g., within the `main` function)
# is not available in this file. Inserting it directly would lead to syntax errors and undefined variables.
# It appears to be part of a larger compilation pipeline logic.
#
#         if args.ir or args.output:
#             # Asegurar que el análisis semántico se ejecutó (para anotar tipos)
#             if not args.eval:
#                 analizador = AnalizadorSemantico()
#                 analizador.analizar(programa)
#
#             generador = GeneradorLLVM()
#             codigo_ir = generador.generar(programa) # Corrected potential typo: 'in()' removed
