# 🌟 Jade - Lenguaje de Programación en Español

![Estado](https://img.shields.io/badge/estado-beta-yellow)
![Licencia](https://img.shields.io/badge/licencia-MIT-blue)
![Versión](https://img.shields.io/badge/versión-0.9.0-green)

**Jade** es un lenguaje de programación moderno con sintaxis completamente en español, diseñado para ser accesible, educativo y potente. Utiliza LLVM para generar código nativo de alto rendimiento.

## ✨ Características

- 🇪🇸 **Sintaxis en español** - Palabras clave y sintaxis natural en español
- ⚡ **Alto rendimiento** - Compilación a código nativo mediante LLVM
- 🎯 **Tipado estático** - Con inferencia de tipos automática
- 🔧 **Intérprete integrado** - Ejecución directa durante el desarrollo
- 📚 **Biblioteca estándar** - Runtime en C con funciones esenciales
- 🎓 **Educativo** - Perfecto para aprender programación en tu idioma

## 🚀 Inicio Rápido

### Requisitos

- Python 3.8+
- LLVM 10+ (para compilación nativa)
- GCC/MinGW (para enlace final)

### Instalación

```bash
git clone https://github.com/tu-usuario/jade.git
cd jade
pip install -r requirements.txt
```

### Tu Primer Programa

Crea un archivo `hola.jde`:

```jade
funcion main()
    mostrar("¡Hola, Mundo!")
fin
```

**Ejecutar con intérprete:**
```bash
python src/interpreter.py hola.jde
```

**Compilar a ejecutable:**
```bash
python src/main.py hola.jde
llc hola.ll -filetype=obj -o hola.o
gcc hola.o std/runtime.o -o hola.exe
./hola.exe
```

## 📖 Ejemplos

### Factorial Iterativo

```jade
funcion factorial(n: entero) -> entero
    variable resultado = 1
    para i desde 2 hasta n + 1
        resultado = resultado * i
    fin
    retornar resultado
fin

funcion main()
    para i desde 1 hasta 11
        variable fact = factorial(i)
        mostrar(convertir_a_texto(i) + "! = " + convertir_a_texto(fact))
    fin
fin
```

### Números de Fibonacci

```jade
funcion fibonacci(n: entero) -> entero
    si n <= 1 entonces
        retornar n
    fin
    
    variable a = 0
    variable b = 1
    para i desde 2 hasta n + 1
        variable temp = a + b
        a = b
        b = temp
    fin
    retornar b
fin
```

Ver más ejemplos en [`examples/`](examples/)

## 🏗️ Arquitectura

```
jade/
├── src/
│   ├── lexer.py          # Análisis léxico
│   ├── parser.py         # Análisis sintáctico  
│   ├── semantic.py       # Análisis semántico
│   ├── codegen_llvm.py   # Generación de código LLVM
│   ├── interpreter.py    # Intérprete Python
│   └── main.py           # CLI principal
├── std/
│   ├── runtime.c         # Biblioteca estándar en C
│   └── runtime.h         # Headers del runtime
├── examples/             # Programas de ejemplo
└── docs/                 # Documentación
```

## 🎯 Sintaxis

### Tipos de Datos

- `entero` - Números enteros (64-bit)
- `flotante` - Números decimales (double)
- `texto` - Cadenas de caracteres
- `booleano` - verdadero/falso

### Estructuras de Control

```jade
# Condicionales
si condicion entonces
    # código
sino
    # código alternativo
fin

# Bucles
mientras condicion
    # código
fin

para variable desde inicio hasta fin
    # código
fin
```

### Funciones

```jade
funcion nombre(param1: tipo, param2: tipo) -> tipo_retorno
    # código
    retornar valor
fin
```

## 📚 Documentación

- [Guía de Instalación](INSTALACION.md)
- [Especificación del Lenguaje](docs/ESPECIFICACION.md)
- [Tutorial Completo](docs/TUTORIAL.md)
- [Referencia de API](docs/API.md)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 🗺️ Roadmap

- [x] Compilador básico funcional
- [x] Intérprete completo
- [x] Runtime en C
- [x] Compilación LLVM nativa
- [x] Operaciones de cadenas
- [ ] Listas dinámicas
- [ ] Mapas/Diccionarios
- [ ] Clases y OOP
- [ ] Manejo de excepciones
- [ ] Sistema de módulos
- [ ] Package manager

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👏 Agradecimientos

- Inspirado en lenguajes de programación en español como Latino y EsJS
- Construido con [llvmlite](https://github.com/numba/llvmlite)
- Documentación generada con amor ❤️

## 📞 Contacto

- **Issues:** [GitHub Issues](https://github.com/tu-usuario/jade/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/tu-usuario/jade/discussions)

---

Hecho con ❤️ para la comunidad hispanohablante
