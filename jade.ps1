# Script simple de compilación para Jade
# Uso: .\jade.ps1 archivo.jde

param(
    [Parameter(Mandatory=$true)]
    [string]$Archivo
)

python src/main.py $Archivo
