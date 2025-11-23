# Guía de Instalación - Jade

Esta guía te ayudará a instalar todas las herramientas necesarias para compilar programas Jade a ejecutables nativos.

## Opción 1: Solo Python (Más Fácil) ✅

Si solo quieres probar el compilador sin generar ejecutables nativos:

```bash
# Ya tienes Python instalado
pip install llvmlite
```

Con esto puedes:
- ✅ Compilar programas Jade a LLVM IR
- ✅ Ver el AST y tokens generados
- ✅ Verificar que tu código es correcto
- ❌ NO genera ejecutables .exe directamente

**Uso:**
```bash
python src/main.py examples/hola_mundo.jde --ir
```

---

## Opción 2: Compilación Completa (Avanzado)

Para generar ejecutables nativos necesitas instalar:

### 1. LLVM (Compilador)

**Windows:**

Opción A - Instalador oficial:
1. Descarga LLVM desde: https://github.com/llvm/llvm-project/releases
2. Busca `LLVM-<versión>-win64.exe`
3. Instala y añade al PATH:
   - Durante instalación marca "Add LLVM to system PATH"
   - O manualmente: Panel de Control > Sistema > Variables de entorno
   - Añadir `C:\Program Files\LLVM\bin` al PATH

Opción B - Chocolatey (si tienes instalado):
```powershell
choco install llvm
```

**Verificar instalación:**
```bash
llc --version
```

### 2. GCC (MinGW para Windows)

**Windows:**

Opción A - MSYS2 (Recomendado):
1. Descarga MSYS2: https://www.msys2.org/
2. Instala MSYS2
3. Abre MSYS2 terminal y ejecuta:
```bash
pacman -S mingw-w64-x86_64-gcc
```
4. Añade al PATH: `C:\msys64\mingw64\bin`

Opción B - MinGW-w64:
1. Descarga desde: https://sourceforge.net/projects/mingw-w64/
2. Instala y añade `bin` al PATH

Opción C - Chocolatey:
```powershell
choco install mingw
```

**Verificar instalación:**
```bash
gcc --version
```

### 3. Compilar Runtime de Jade

Una vez instalado GCC:

```bash
cd C:\Users\Moises\.gemini\antigravity\scratch\jade
gcc -c std/runtime.c -o std/runtime.o -O2
gcc -c std/main_wrapper.c -o std/main_wrapper.o -O2
```

---

## Proceso de Compilación Completo

Una vez tengas todo instalado:

### Método Automático (Script)

```powershell
.\build.ps1 examples\hola_mundo.jde
```

### Método Manual

```bash
# 1. Compilar Jade a LLVM IR
python src/main.py examples/hola_mundo.jde

# 2. Convertir LLVM IR a código objeto
llc examples/hola_mundo.ll -filetype=obj -o examples/hola_mundo.o

# 3. Enlazar con runtime
gcc examples/hola_mundo.o std/runtime.o std/main_wrapper.o -o examples/hola_mundo.exe

# 4. Ejecutar
.\examples\hola_mundo.exe
```

---

## Solución de Problemas

### Error: "gcc no se reconoce como comando"

- Verifica que GCC esté en el PATH
- Reinicia PowerShell/Terminal después de instalar
- Verifica con: `$env:PATH` (PowerShell) o `echo %PATH%` (CMD)

### Error: "llc no se reconoce como comando"

- Verifica que LLVM esté en el PATH
- Puede estar en: `C:\Program Files\LLVM\bin`
- Añádelo manualmente si es necesario

### Error: "No se encuentra archivo runtime.o"

- Primero compila el runtime con GCC
- Ver sección "Compilar Runtime de Jade"

---

## Verificación de Instalación

Ejecuta estos comandos para verificar:

```bash
# Python y llvmlite
python --version
python -c "import llvmlite; print('llvmlite OK')"

# LLVM
llc --version

# GCC
gcc --version
```

Si todos responden correctamente, ¡estás listo! Si no tienes LLVM/GCC y solo quieres probar el lenguaje, usa el intérprete Python incluido (ver siguiente sección).

---

## Alternativa: Intérprete Python

Si no quieres instalar LLVM/GCC, puedes usar el intérprete de Jade:

```bash
python src/interpreter.py examples/hola_mundo.jde
```

El intérprete ejecuta directamente el código Jade sin generar ejecutable.
