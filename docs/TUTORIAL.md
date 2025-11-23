# Tutorial de LenguajeES

Bienvenido al tutorial de **LenguajeES**, un lenguaje de programación moderno con sintaxis completamente en español.

## Índice

1. [Instalación](#instalación)
2. [Tu Primer Programa](#tu-primer-programa)
3. [Variables y Tipos](#variables-y-tipos)
4. [Operadores](#operadores)
5. [Control de Flujo](#control-de-flujo)
6. [Funciones](#funciones)
7. [Estructuras de Datos](#estructuras-de-datos)
8. [Ejercicios](#ejercicios)

---

## Instalación

### Requisitos previos
- Python 3.8 o superior
- LLVM 14 o superior
- Compilador C (gcc o clang)

### Instalación del compilador

```bash
git clone https://github.com/tu-usuario/lenguaje-espanol
cd lenguaje-espanol
pip install -r requirements.txt
```

---

## Tu Primer Programa

Crea un archivo llamado `hola.les`:

```
funcion main()
    mostrar("¡Hola, Mundo!")
fin
```

Compila y ejecuta:

```bash
lescompilador hola.les
./hola
```

Salida:
```
¡Hola, Mundo!
```

### Explicación

- `funcion main()` - Todo programa necesita una función principal llamada `main`
- `mostrar(...)` - Función que imprime texto en la consola
- `fin` - Marca el final del bloque de la función

---

## Variables y Tipos

### Declaración de variables

```
funcion main()
    // Variable con inferencia de tipo
    variable nombre = "María"
    variable edad = 25
    variable altura = 1.65
    variable activo = verdadero
    
    mostrar(nombre)
    mostrar(convertir_a_texto(edad))
fin
```

### Tipos explícitos

```
funcion main()
    entero x = 10
    flotante pi = 3.14159
    texto mensaje = "Hola"
    booleano esMayorDeEdad = verdadero
    
    mostrar(mensaje)
fin
```

### Constantes

```
funcion main()
    constante PI = 3.14159
    constante GRAVEDAD = 9.81
    
    // PI = 3.0  // ¡Error! No se puede modificar una constante
fin
```

### Tipos disponibles

- `entero` - números enteros: -100, 0, 42, 1000
- `flotante` - números decimales: 3.14, -0.5, 2.71828
- `texto` - cadenas de caracteres: "hola", "mundo"
- `booleano` - verdadero o falso
- `caracter` - un solo carácter: 'a', 'Z', '5'

---

## Operadores

### Aritméticos

```
funcion main()
    variable a = 10
    variable b = 3
    
    mostrar(convertir_a_texto(a + b))   // 13 - suma
    mostrar(convertir_a_texto(a - b))   // 7  - resta
    mostrar(convertir_a_texto(a * b))   // 30 - multiplicación
    mostrar(convertir_a_texto(a / b))   // 3  - división
    mostrar(convertir_a_texto(a % b))   // 1  - módulo (resto)
fin
```

### Comparación

```
funcion main()
    variable x = 5
    variable y = 10
    
    mostrar(convertir_a_texto(x == y))   // falso - igual
    mostrar(convertir_a_texto(x != y))   // verdadero - diferente
    mostrar(convertir_a_texto(x < y))    // verdadero - menor que
    mostrar(convertir_a_texto(x > y))    // falso - mayor que
    mostrar(convertir_a_texto(x <= 5))   // verdadero - menor o igual
    mostrar(convertir_a_texto(y >= 10))  // verdadero - mayor o igual
fin
```

### Lógicos

```
funcion main()
    variable a = verdadero
    variable b = falso
    
    mostrar(convertir_a_texto(a y b))    // falso - AND
    mostrar(convertir_a_texto(a o b))    // verdadero - OR
    mostrar(convertir_a_texto(no a))     // falso - NOT
fin
```

---

## Control de Flujo

### Condicionales: si/entonces/sino

```
funcion main()
    variable edad = 18
    
    si edad >= 18 entonces
        mostrar("Eres mayor de edad")
    sino
        mostrar("Eres menor de edad")
    fin
fin
```

### Múltiples condiciones

```
funcion main()
    variable nota = 85
    
    si nota >= 90 entonces
        mostrar("Excelente")
    sino si nota >= 80 entonces
        mostrar("Muy bien")
    sino si nota >= 70 entonces
        mostrar("Bien")
    sino
        mostrar("Necesitas mejorar")
    fin
fin
```

### Bucle mientras

```
funcion main()
    variable contador = 0
    
    mientras contador < 5 hacer
        mostrar(convertir_a_texto(contador))
        contador = contador + 1
    fin
fin
```

### Bucle para (for)

```
funcion main()
    // Bucle numérico
    para i desde 0 hasta 5 hacer
        mostrar(convertir_a_texto(i))
    fin
    
    // Salida: 0, 1, 2, 3, 4
fin
```

### Control de bucles

```
funcion main()
    para i desde 0 hasta 10 hacer
        si i == 3 entonces
            continuar  // Salta a la siguiente iteración
        fin
        
        si i == 7 entonces
            romper  // Sale del bucle
        fin
        
        mostrar(convertir_a_texto(i))
    fin
    // Salida: 0, 1, 2, 4, 5, 6
fin
```

---

## Funciones

### Definición básica

```
funcion saludar()
    mostrar("¡Hola!")
fin

funcion main()
    saludar()
fin
```

### Funciones con parámetros

```
funcion saludar(nombre)
    mostrar("¡Hola, " + nombre + "!")
fin

funcion main()
    saludar("Ana")
    saludar("Carlos")
fin
```

### Funciones con retorno

```
funcion suma(a, b)
    retornar a + b
fin

funcion main()
    variable resultado = suma(5, 3)
    mostrar(convertir_a_texto(resultado))  // 8
fin
```

### Recursión

```
funcion factorial(n)
    si n == 0 entonces
        retornar 1
    sino
        retornar n * factorial(n - 1)
    fin
fin

funcion main()
    variable resultado = factorial(5)
    mostrar("5! = " + convertir_a_texto(resultado))  // 5! = 120
fin
```

---

## Estructuras de Datos

### Listas

```
funcion main()
    variable numeros = [1, 2, 3, 4, 5]
    variable nombres = ["Ana", "Luis", "María"]
    
    // Acceder a elementos
    mostrar(convertir_a_texto(numeros[0]))  // 1
    mostrar(nombres[1])  // Luis
    
    // Modificar elementos
    numeros[2] = 10
    mostrar(convertir_a_texto(numeros[2]))  // 10
fin
```

### Mapas (Diccionarios)

```
funcion main()
    variable persona = {
        nombre: "Carlos",
        edad: 30,
        ciudad: "Madrid"
    }
    
    mostrar(persona["nombre"])  // Carlos
    mostrar(convertir_a_texto(persona["edad"]))  // 30
fin
```

### Tuplas

```
funcion main()
    variable punto = (10, 20)
    variable persona = ("Ana", 25, "Barcelona")
    
    mostrar(convertir_a_texto(punto[0]))  // 10
    mostrar(persona[0])  // Ana
fin
```

---

## Ejercicios

### Ejercicio 1: Número par o impar

Escribe una función que determine si un número es par o impar.

```
funcion es_par(numero)
    si numero % 2 == 0 entonces
        retornar verdadero
    sino
        retornar falso
    fin
fin

funcion main()
    si es_par(10) entonces
        mostrar("10 es par")
    fin
    
    si no es_par(7) entonces
        mostrar("7 es impar")
    fin
fin
```

### Ejercicio 2: Suma de números

Calcula la suma de los números del 1 al 100.

```
funcion main()
    variable suma = 0
    
    para i desde 1 hasta 101 hacer
        suma = suma + i
    fin
    
    mostrar("La suma es: " + convertir_a_texto(suma))
fin
```

### Ejercicio 3: Serie de Fibonacci

Imprime los primeros N números de la serie de Fibonacci.

```
funcion fibonacci(n)
    si n <= 1 entonces
        retornar n
    fin
    retornar fibonacci(n - 1) + fibonacci(n - 2)
fin

funcion main()
    para i desde 0 hasta 10 hacer
        variable fib = fibonacci(i)
        mostrar(convertir_a_texto(fib))
    fin
fin
```

### Ejercicio 4: Búsqueda en lista

Busca un elemento en una lista y devuelve su posición.

```
funcion buscar(lista, valor, indice, fin_lista)
    si indice >= fin_lista entonces
        retornar -1
    fin
    
    si lista[indice] == valor entonces
        retornar indice
    fin
    
    retornar buscar(lista, valor, indice + 1, fin_lista)
fin

funcion main()
    variable numeros = [10, 20, 30, 40, 50]
    variable posicion = buscar(numeros, 30, 0, 5)
    mostrar("Encontrado en posición: " + convertir_a_texto(posicion))
fin
```

---

## Próximos Pasos

1. Consulta la [Especificación del Lenguaje](../ESPECIFICACION.md) para detalles técnicos
2. Revisa la [Referencia Completa](REFERENCIA.md) para funciones avanzadas
3. Explora los ejemplos en la carpeta `/examples`
4. ¡Crea tus propios programas!

---

## Recursos Adicionales

- Repositorio oficial: https://github.com/tu-usuario/lenguaje-espanol
- Documentación completa: https://lenguajees.org
- Comunidad: Discord/Foros

¡Feliz programación en español! 🇪🇸
