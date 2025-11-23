# Contribuyendo a Jade

¡Gracias por tu interés en contribuir a Jade! Este documento proporciona pautas para contribuir al proyecto.

## 🎯 Cómo Contribuir

### Reportar Bugs

Si encuentras un bug, por favor:

1. Verifica que el bug no haya sido reportado anteriormente
2. Abre un issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Tu entorno (OS, versión de Python, etc.)
   - Código de ejemplo mínimo

### Sugerir Mejoras

Para sugerir nuevas características:

1. Abre un issue etiquetado como "enhancement"
2. Describe claramente:
   - El problema que resuelve
   - La solución propuesta
   - Ejemplos de uso

### Pull Requests

1. **Fork** el repositorio
2. **Crea una rama** específica para tu feature
   ```bash
   git checkout -b feature/mi-nueva-caracteristica
   ```
3. **Escribe código limpio** siguiendo las convenciones del proyecto
4. **Añade tests** si es aplicable
5. **Actualiza documentación** si es necesario
6. **Commit** con mensajes descriptivos
   ```bash
   git commit -m "feat: añade soporte para listas dinámicas"
   ```
7. **Push** a tu fork
   ```bash
   git push origin feature/mi-nueva-caracteristica
   ```
8. **Abre un Pull Request** con descripción detallada

## 📋 Estilo de Código

### Python

- Sigue [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Nombres de variables en español donde tenga sentido
- Docstrings en español
- Máximo 100 caracteres por línea

### C (Runtime)

- Estilo K&R para llaves
- Nombres de funciones con prefijo `jade_`
- Comentarios en español

### Jade (Ejemplos)

- Indentación de 4 espacios
- Nombres descriptivos en español
- Comentarios explicativos

## 🧪 Testing

Antes de hacer un PR:

```bash
# Ejecutar todos los tests
pytest tests/

# Verificar ejemplos
python src/interpreter.py examples/hola_mundo.jde
python src/interpreter.py examples/factorial.jde
python src/interpreter.py examples/fibonacci.jde
```

## 📝 Mensajes de Commit

Usa el formato [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nueva característica
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `style:` formateo, sin cambios de código
- `refactor:` refactorización de código
- `test:` añadir o modificar tests
- `chore:` tareas de mantenimiento

Ejemplos:
```
feat: añade tipo de dato lista
fix: corrige error en parser de expresiones
docs: actualiza tutorial de instalación
```

## 🌟 Áreas de Contribución

### Prioritarias

- 🔥 Implementación de listas y mapas
- 🔥 Sistema de módulos
- 🔥 Clases y OOP
- 🔥 Manejo de excepciones

### Documentación

- 📖 Tutoriales en español
- 📖 Ejemplos de código
- 📖 Traducciones

### Tooling

- 🔧 Extensión VS Code
- 🔧 Syntax highlighting
- 🔧 LSP (Language Server Protocol)
- 🔧 Debugger

### Comunidad

- 💬 Responder preguntas en Discussions
- 💬 Revisar Pull Requests
- 💬 Crear contenido educativo

## ❓ Preguntas

Si tienes preguntas sobre cómo contribuir:

- Abre una discusión en GitHub Discussions
- Revisa issues existentes etiquetados como "good first issue"

## 📜 Código de Conducta

Se espera que todos los contribuyentes:

- Sean respetuosos y constructivos
- Acepten críticas constructivas
- Se enfoquen en lo mejor para la comunidad
- Muestren empatía hacia otros miembros

---

¡Gracias por hacer que Jade sea mejor! 🎉
