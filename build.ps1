# Script de compilación completa para Jade
# Compila un archivo .jde a ejecutable nativo

param(
    [Parameter(Mandatory=$true)]
    [string]$ArchivoJade
)

Write-Host "=== Compilador Jade - Compilacion Completa ===" -ForegroundColor Cyan
Write-Host ""

# Verificar que el archivo existe
if (-not (Test-Path $ArchivoJade)) {
    Write-Host "[ERROR] Archivo no encontrado: $ArchivoJade" -ForegroundColor Red
    exit 1
}

# Obtener nombre base
$nombreBase = [System.IO.Path]::GetFileNameWithoutExtension($ArchivoJade)
$dirBase = [System.IO.Path]::GetDirectoryName($ArchivoJade)
if ($dirBase -eq "") { $dirBase = "." }

Write-Host "[1/5] Compilando $ArchivoJade a LLVM IR..." -ForegroundColor Yellow
python src/main.py $ArchivoJade
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Compilacion de Jade fallo" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/5] Compilando runtime de C..." -ForegroundColor Yellow
gcc -c std/runtime.c -o std/runtime.o -O2
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Compilacion de runtime fallo" -ForegroundColor Red
    exit 1
}

$archivoLL = "$dirBase\$nombreBase.ll"
$archivoO = "$dirBase\$nombreBase.o"
$archivoExe = "$dirBase\$nombreBase.exe"

Write-Host ""
Write-Host "[3/5] Generando codigo objeto desde LLVM IR..." -ForegroundColor Yellow
llc $archivoLL -filetype=obj -o $archivoO
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] llc fallo. Asegurese de tener LLVM instalado" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[4/5] Enlazando ejecutable..." -ForegroundColor Yellow
gcc $archivoO std/runtime.o -o $archivoExe
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Enlazado fallo" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[5/5] Limpiando archivos temporales..." -ForegroundColor Yellow
Remove-Item $archivoO -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "[OK] Compilacion exitosa!" -ForegroundColor Green
Write-Host "Ejecutable generado: $archivoExe" -ForegroundColor Green
Write-Host ""
Write-Host "Para ejecutar:" -ForegroundColor Cyan
Write-Host "  .\$archivoExe" -ForegroundColor White
