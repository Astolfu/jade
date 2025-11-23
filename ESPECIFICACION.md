# Especificación del Lenguaje - LenguajeES

## 1. Palabras Reservadas

### Control de flujo
- `si` - condicional if
- `entonces` - after condition
- `sino` - else
- `mientras` - while loop
- `para` - for loop
- `desde` - from (in for loops)
- `hasta` - to (in for loops)
- `hacer` - do
- `romper` - break
- `continuar` - continue
- `fin` - end block

### Funciones y valores
- `funcion` - function definition
- `retornar` - return
- `variable` - variable declaration
- `constante` - constant declaration
- `nulo` - null
- `verdadero` - true
- `falso` - false

### Tipos
- `entero` - integer
- `flotante` - float
- `booleano` - boolean
- `texto` - string
- `caracter` - character
- `lista` - list/array
- `mapa` - dictionary/map
- `tupla` - tuple

### Otros
- `importar` - import
- `modulo` - module
- `clase` - class (futuro)
- `objeto` - object (futuro)
- `intentar` - try
- `capturar` - catch
- `lanzar` - throw

## 2. Operadores

### Aritméticos
- `+` suma
- `-` resta
- `*` multiplicación
- `/` división
- `%` módulo
- `^` potencia

### Comparación
- `==` igual
- `!=` no igual
- `<` menor que
- `>` mayor que
- `<=` menor o igual
- `>=` mayor o igual

### Lógicos
- `y` - AND
- `o` - OR
- `no` - NOT

### Asignación
- `=` asignación simple
- `+=` suma y asigna
- `-=` resta y asigna
- `*=` multiplica y asigna
- `/=` divide y asigna

## 3. Tipos de Datos

### Primitivos
- **entero**: números enteros con signo, 64 bits
- **flotante**: números de punto flotante, 64 bits
- **booleano**: verdadero o falso
- **caracter**: un carácter Unicode
- **texto**: cadena de caracteres UTF-8

### Compuestos
- **lista**: arreglo dinámico `[1, 2, 3]`
- **mapa**: diccionario clave-valor `{clave: valor}`
- **tupla**: tupla inmutable `(1, "dos", 3.0)`

## 4. Sintaxis

### Declaración de variables
```
variable x = 10              // inferencia de tipo
entero y = 20                // tipo explícito
constante PI = 3.14159       // constante
```

### Funciones
```
funcion nombre(parametro1, parametro2)
    // cuerpo
    retornar valor
fin
```

### Condicionales
```
si condicion entonces
    // código
sino si otra_condicion entonces
    // código
sino
    // código
fin
```

### Bucles
```
mientras condicion hacer
    // código
fin

para i desde 0 hasta 10 hacer
    // código
fin

para elemento en lista hacer
    // código
fin
```

### Comentarios
```
// comentario de una línea

/* comentario
   de múltiples
   líneas */
```

## 5. Biblioteca Estándar

### Módulo Sistema
- `mostrar(texto)` - imprime en consola
- `leer()` - lee entrada del usuario
- `convertir_a_texto(valor)` - convierte a string
- `convertir_a_entero(texto)` - convierte a entero
- `convertir_a_flotante(texto)` - convierte a flotante

### Módulo Matematicas
- `abs(x)` - valor absoluto
- `max(a, b)` - máximo
- `min(a, b)` - mínimo
- `potencia(base, exp)` - potenciación
- `raiz(x)` - raíz cuadrada
- `aleatorio()` - número aleatorio [0,1)

### Módulo Texto
- `longitud(texto)` - longitud de cadena
- `mayusculas(texto)` - convertir a mayúsculas
- `minusculas(texto)` - convertir a minúsculas
- `contiene(texto, subcadena)` - verifica si contiene
- `dividir(texto, separador)` - divide en lista

### Módulo Listas
- `agregar(lista, elemento)` - añade elemento
- `remover(lista, indice)` - elimina elemento
- `ordenar(lista)` - ordena lista
- `longitud(lista)` - tamaño de lista
- `vacio(lista)` - verifica si está vacía

## 6. Gestión de Errores

```
intentar
    // código que puede fallar
capturar error
    mostrar("Error: " + error)
fin
```

## 7. Módulos

```
// archivo: matematicas.les
modulo Matematicas

funcion suma(a, b)
    retornar a + b
fin

// archivo: principal.les
importar Matematicas

funcion main()
    variable resultado = Matematicas.suma(5, 3)
    mostrar(resultado)
fin
```

## 8. Ejemplos

### Hola Mundo
```
funcion main()
    mostrar("¡Hola, Mundo!")
fin
```

### Factorial
```
funcion factorial(n)
    si n == 0 entonces
        retornar 1
    sino
        retornar n * factorial(n - 1)
    fin
fin
```

### Fibonacci
```
funcion fibonacci(n)
    si n <= 1 entonces
        retornar n
    fin
    retornar fibonacci(n - 1) + fibonacci(n - 2)
fin
```

### Búsqueda en lista
```
funcion buscar(lista, valor)
    para i desde 0 hasta longitud(lista) hacer
        si lista[i] == valor entonces
            retornar i
        fin
    fin
    retornar -1
fin
```
