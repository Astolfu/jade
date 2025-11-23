# 📦 Workflow de Git para Jade

## Comandos Rápidos para Commits Futuros

### Cuando trabajemos en nuevas features:

```powershell
# Ver cambios
git status

# Añadir todos los cambios
git add .

# Commit con mensaje descriptivo
git commit -m "feat: descripción del cambio"

# Push a GitHub (con autenticación)
git push origin main
```

### Convención de Mensajes de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - Nueva característica
  - Ejemplo: `feat: añade soporte para listas dinámicas`
  
- `fix:` - Corrección de bug
  - Ejemplo: `fix: corrige error en parser de strings`
  
- `docs:` - Cambios en documentación
  - Ejemplo: `docs: actualiza tutorial de instalación`
  
- `refactor:` - Refactorización sin cambio de funcionalidad
  - Ejemplo: `refactor: simplifica generador LLVM`
  
- `test:` - Añadir o modificar tests
  - Ejemplo: `test: añade tests para operador +`
  
- `chore:` - Tareas de mantenimiento
  - Ejemplo: `chore: actualiza dependencias`

### Workflow Típico

1. **Hacer cambios** en archivos
2. **Probar** que funciona:
   ```powershell
   python src/interpreter.py examples/hola_mundo.jde
   ```
3. **Commit y push**:
   ```powershell
   git add .
   git commit -m "feat: tu cambio aquí"
   git push origin main
   ```

### Branches para Features Grandes

Para cambios grandes, crea una branch:

```powershell
# Crear y cambiar a nueva branch
git checkout -b feature/nombre-feature

# Hacer cambios y commit
git add .
git commit -m "feat: cambio descripción"
git push -u origin feature/nombre-feature

# Luego en GitHub, crear Pull Request
```

### Verificar Estado

```powershell
# Ver commits recientes
git log --oneline -5

# Ver diferencias
git diff

# Ver archivos modificados
git status
```

## 🔄 Respaldo Automático

Cada vez que hagamos cambios significativos, los subiré a GitHub automáticamente con:

```powershell
git add .
git commit -m "feat: [descripción]"
git push origin main
```

## 🌐 URLs Importantes

- Repositorio: https://github.com/Astolfu/jade
- Issues: https://github.com/Astolfu/jade/issues
- Actions: https://github.com/Astolfu/jade/actions

---

**Nota:** Para futuros pushes, puede que necesites autenticarte de nuevo si el sistema lo requiere.
