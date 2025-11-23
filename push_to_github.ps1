# 🚀 Script de Push a GitHub

# Configuración (REEMPLAZA CON TUS DATOS)
$GITHUB_USER = "TU-USUARIO"
$REPO_NAME = "jade"

# Paso 1: Configurar Git (si no lo has hecho)
Write-Host "📋 Configurando Git..." -ForegroundColor Cyan
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# Paso 2: Crear commit si hay cambios pendientes
Write-Host "📦 Creando commit..." -ForegroundColor Cyan
git add .
git commit -m "feat: initial commit - Jade compiler v0.9.0

- Compilador completo con lexer, parser, semantic analyzer
- Generador de código LLVM nativo
- Intérprete Python 100% funcional
- Runtime library en C con operaciones básicas
- Soporte para concatenación de strings
- Ejemplos funcionando: hola_mundo, factorial, fibonacci, bucle
- Documentación completa en español
- Licencia MIT - Proyecto Open Source"

# Paso 3: Añadir remote de GitHub
Write-Host "🔗 Conectando con GitHub..." -ForegroundColor Cyan
$REPO_URL = "https://github.com/$GITHUB_USER/$REPO_NAME.git"
Write-Host "URL: $REPO_URL" -ForegroundColor Yellow

# Verificar si ya existe el remote
$remotes = git remote
if ($remotes -contains "origin") {
    Write-Host "⚠️  Remote 'origin' ya existe, actualizando..." -ForegroundColor Yellow
    git remote set-url origin $REPO_URL
} else {
    git remote add origin $REPO_URL
}

# Paso 4: Renombrar branch a main
Write-Host "🌿 Configurando branch main..." -ForegroundColor Cyan
git branch -M main

# Paso 5: Push inicial
Write-Host "🚀 Haciendo push a GitHub..." -ForegroundColor Green
Write-Host "Se te pedirá autenticación..." -ForegroundColor Yellow
git push -u origin main

Write-Host "✅ ¡Listo! Tu código está en GitHub" -ForegroundColor Green
Write-Host "🌐 Visita: https://github.com/$GITHUB_USER/$REPO_NAME" -ForegroundColor Cyan
