# Script para encontrar y configurar LLVM y GCC en Windows
# Ejecutar como administrador si es posible

Write-Host "=== Buscando LLVM y GCC ===" -ForegroundColor Cyan
Write-Host ""

# Función para verificar comando
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Verificar estado actual
Write-Host "[1] Verificando comandos actuales..." -ForegroundColor Yellow
$llcFound = Test-Command "llc"
$gccFound = Test-Command "gcc"

if ($llcFound) {
    Write-Host "  [OK] llc encontrado en PATH" -ForegroundColor Green
    llc --version | Select-Object -First 1
}
else {
    Write-Host "  [X] llc NO encontrado en PATH" -ForegroundColor Red
}

if ($gccFound) {
    Write-Host "  [OK] gcc encontrado en PATH" -ForegroundColor Green
    gcc --version | Select-Object -First 1
}
else {
    Write-Host "  [X] gcc NO encontrado en PATH" -ForegroundColor Red
}

Write-Host ""
Write-Host "[2] Buscando instalaciones..." -ForegroundColor Yellow

# Buscar LLVM
$llvmPaths = @(
    "C:\Program Files\LLVM\bin",
    "C:\Program Files (x86)\LLVM\bin",
    "C:\LLVM\bin"
)

$llvmBin = $null
foreach ($path in $llvmPaths) {
    if (Test-Path "$path\llc.exe") {
        $llvmBin = $path
        Write-Host "  [ENCONTRADO] LLVM en: $path" -ForegroundColor Green
        break
    }
}

if (-not $llvmBin) {
    Write-Host "  [NO ENCONTRADO] LLVM - Buscando en todo el disco..." -ForegroundColor Yellow
    $llcExe = Get-ChildItem "C:\Program Files" -Recurse -Filter "llc.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($llcExe) {
        $llvmBin = Split-Path $llcExe.FullName
        Write-Host "  [ENCONTRADO] LLVM en: $llvmBin" -ForegroundColor Green
    }
}

# Buscar GCC/MinGW
$gccPaths = @(
    "C:\msys64\mingw64\bin",
    "C:\msys64\ucrt64\bin",
    "C:\MinGW\bin",
    "C:\MinGW-w64\bin",
    "C:\Program Files\mingw-w64\bin",
    "C:\TDM-GCC-64\bin"
)

$gccBin = $null
foreach ($path in $gccPaths) {
    if (Test-Path "$path\gcc.exe") {
        $gccBin = $path
        Write-Host "  [ENCONTRADO] GCC en: $path" -ForegroundColor Green
        break
    }
}

if (-not $gccBin) {
    Write-Host "  [NO ENCONTRADO] GCC - Buscando MinGW..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3] Configuración del PATH" -ForegroundColor Yellow

# Mostrar PATH actual
$currentPath = $env:PATH
Write-Host "  PATH actual tiene $($currentPath.Split(';').Count) entradas" -ForegroundColor Gray

# Sugerencias
Write-Host ""
Write-Host "=== ACCIONES RECOMENDADAS ===" -ForegroundColor Cyan
Write-Host ""

if ($llvmBin) {
    Write-Host "Para añadir LLVM al PATH (esta sesión):" -ForegroundColor Yellow
    Write-Host "  `$env:PATH += `";$llvmBin`"" -ForegroundColor White
    Write-Host ""
    
    if ($llvmBin -and -not ($currentPath -like "*$llvmBin*")) {
        Write-Host "Añadiendo LLVM al PATH de esta sesión..." -ForegroundColor Green
        $env:PATH += ";$llvmBin"
        Write-Host "  [OK] LLVM añadido temporalmente" -ForegroundColor Green
    }
}
else {
    Write-Host "[!] LLVM no encontrado. Instalar desde:" -ForegroundColor Red
    Write-Host "    https://github.com/llvm/llvm-project/releases" -ForegroundColor White
}

if ($gccBin) {
    Write-Host "Para añadir GCC al PATH (esta sesión):" -ForegroundColor Yellow
    Write-Host "  `$env:PATH += `";$gccBin`"" -ForegroundColor White
    Write-Host ""
    
    if ($gccBin -and -not ($currentPath -like "*$gccBin*")) {
        Write-Host "Añadiendo GCC al PATH de esta sesión..." -ForegroundColor Green
        $env:PATH += ";$gccBin"
        Write-Host "  [OK] GCC añadido temporalmente" -ForegroundColor Green
    }
}
else {
    Write-Host "[!] GCC no encontrado. Instalar MSYS2:" -ForegroundColor Red
    Write-Host "    https://www.msys2.org/" -ForegroundColor White
    Write-Host "    Luego ejecutar: pacman -S mingw-w64-x86_64-gcc" -ForegroundColor White
}

Write-Host ""
Write-Host "Para hacerlo PERMANENTE:" -ForegroundColor Yellow
Write-Host "  1. Abrir 'Panel de Control' > 'Sistema' > 'Configuración avanzada'" -ForegroundColor White
Write-Host "  2. Click en 'Variables de entorno'" -ForegroundColor White
Write-Host "  3. Editar 'Path' en 'Variables del sistema'" -ForegroundColor White
Write-Host "  4. Añadir las rutas encontradas" -ForegroundColor White
Write-Host ""

# Verificar de nuevo
Write-Host "[4] Verificando de nuevo..." -ForegroundColor Yellow
$llcFound2 = Test-Command "llc"
$gccFound2 = Test-Command "gcc"

if ($llcFound2) {
    Write-Host "  [OK] llc ahora disponible" -ForegroundColor Green
}
if ($gccFound2) {
    Write-Host "  [OK] gcc ahora disponible" -ForegroundColor Green
}

if ($llcFound2 -and $gccFound2) {
    Write-Host ""
    Write-Host "✅ Todas las herramientas están disponibles!" -ForegroundColor Green
    Write-Host "   Puedes compilar programas Jade ahora:" -ForegroundColor Green
    Write-Host "   .\build.ps1 examples\hola_mundo.jde" -ForegroundColor White
}
else {
    Write-Host ""
    Write-Host "⚠ Algunas herramientas aún no están disponibles" -ForegroundColor Yellow
    Write-Host "  Usa el intérprete mientras tanto:" -ForegroundColor Yellow
    Write-Host "  python src/interpreter.py examples/hola_mundo.jde" -ForegroundColor White
}
