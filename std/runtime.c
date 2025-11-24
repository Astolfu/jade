/*
 * Runtime de Jade - Biblioteca estándar en C
 * Funciones básicas de entrada/salida y conversión
 */

#include "runtime.h"
#include <math.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* ============================================================================
 * GESTIÓN DE MEMORIA
 * ============================================================================
 */

void *jade_malloc(size_t size) {
  void *ptr = malloc(size);
  if (!ptr) {
    fprintf(stderr, "Error: No se pudo asignar memoria\n");
    exit(1);
  }
  return ptr;
}

void jade_free(void *ptr) {
  if (ptr) {
    free(ptr);
  }
}

/* ============================================================================
 * ENTRADA/SALIDA
 * ============================================================================
 */

void jade_mostrar(const char *texto) {
  printf("%s\n", texto);
  fflush(stdout);
}

char *jade_leer(void) {
  char buffer[1024];
  if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
    // Eliminar newline
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len - 1] == '\n') {
      buffer[len - 1] = '\0';
      len--;
    }
    char *result = (char *)jade_malloc(len + 1);
    strcpy(result, buffer);
    return result;
  }
  char *empty = (char *)jade_malloc(1);
  empty[0] = '\0';
  return empty;
}

/* ============================================================================
 * CONVERSIONES
 * ============================================================================
 */

char *jade_convertir_a_texto_entero(int64_t n) {
  char buffer[32];
  snprintf(buffer, sizeof(buffer), "%lld", (long long)n);
  char *result = (char *)jade_malloc(strlen(buffer) + 1);
  strcpy(result, buffer);
  return result;
}

char *jade_convertir_a_texto_flotante(double n) {
  char buffer[32];
  snprintf(buffer, sizeof(buffer), "%g", n);
  char *result = (char *)jade_malloc(strlen(buffer) + 1);
  strcpy(result, buffer);
  return result;
}

char *jade_convertir_a_texto_booleano(int b) {
  const char *str = b ? "verdadero" : "falso";
  char *result = (char *)jade_malloc(strlen(str) + 1);
  strcpy(result, str);
  return result;
}

int64_t jade_convertir_a_entero(const char *str) { return (int64_t)atoll(str); }

double jade_convertir_a_flotante(const char *str) { return atof(str); }

/* ============================================================================
 * OPERACIONES DE CADENAS
 * ============================================================================
 */

char *jade_concatenar(const char *a, const char *b) {
  if (!a || !b)
    return NULL;

  size_t len_a = strlen(a);
  size_t len_b = strlen(b);
  char *result = (char *)jade_malloc(len_a + len_b + 1);

  strcpy(result, a);
  strcat(result, b);

  return result;
}

int64_t jade_longitud(const char *str) {
  if (!str)
    return 0;
  return (int64_t)strlen(str);
}

/* ============================================================================
 * FUNCIONES MATEMÁTICAS
 * ============================================================================
 */

int64_t jade_abs_entero(int64_t x) { return x < 0 ? -x : x; }

double jade_abs_flotante(double x) { return fabs(x); }

int64_t jade_max_entero(int64_t a, int64_t b) { return a > b ? a : b; }

int64_t jade_min_entero(int64_t a, int64_t b) { return a < b ? a : b; }

double jade_potencia(double base, double exp) { return pow(base, exp); }

double jade_raiz(double x) { return sqrt(x); }

double jade_aleatorio(void) { return (double)rand() / (double)RAND_MAX; }

/* ============================================================================
 * LISTAS
 * ============================================================================
 */

JadeList *jade_lista_nueva(void) {
  JadeList *lista = (JadeList *)jade_malloc(sizeof(JadeList));
  lista->size = 0;
  lista->capacity = 8; /* Capacidad inicial */
  lista->data = (void **)jade_malloc(sizeof(void *) * lista->capacity);
  return lista;
}

void jade_lista_agregar(JadeList *lista, void *elemento) {
  if (lista->size >= lista->capacity) {
    lista->capacity *= 2;
    void **new_data =
        (void **)realloc(lista->data, sizeof(void *) * lista->capacity);
    if (!new_data) {
      fprintf(stderr, "Error: No se pudo redimensionar la lista\n");
      exit(1);
    }
    lista->data = new_data;
  }
  lista->data[lista->size++] = elemento;
}

void *jade_lista_obtener(JadeList *lista, int64_t indice) {
  if (indice < 0 || indice >= lista->size) {
    fprintf(stderr, "Error: Índice de lista fuera de rango: %lld\n",
            (long long)indice);
    exit(1);
  }
  return lista->data[indice];
}

void jade_lista_asignar(JadeList *lista, int64_t indice, void *valor) {
  if (indice < 0 || indice >= lista->size) {
    fprintf(stderr, "Error: Índice de lista fuera de rango: %lld\n",
            (long long)indice);
    exit(1);
  }
  lista->data[indice] = valor;
}

int64_t jade_lista_longitud(JadeList *lista) { return lista->size; }

void *jade_lista_eliminar(JadeList *lista, int64_t indice) {
  if (indice < 0 || indice >= lista->size) {
    fprintf(stderr, "Error: Índice de lista fuera de rango: %lld\n",
            (long long)indice);
    exit(1);
  }

  void *elemento = lista->data[indice];

  /* Desplazar elementos */
  for (int64_t i = indice; i < lista->size - 1; i++) {
    lista->data[i] = lista->data[i + 1];
  }

  lista->size--;
  return elemento;
}

int jade_lista_contiene(JadeList *lista, void *elemento) {
  for (int64_t i = 0; i < lista->size; i++) {
    /* Comparación simple de punteros o valores enteros */
    if (lista->data[i] == elemento) {
      return 1;
    }
    /* TODO: Comparación profunda para strings/objetos si fuera necesario */
  }
  return 0;
}

void jade_lista_liberar(JadeList *lista) {
  if (lista) {
    if (lista->data) {
      jade_free(lista->data);
    }
    jade_free(lista);
  }
}

/* ============================================================================
 * MAPAS (Hash Map)
 * ============================================================================
 */

/* Hashing específico para strings si es necesario */
uint64_t _jade_hash_str(const char *str) {
  uint64_t hash = 5381;
  int c;
  while ((c = *str++))
    hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
  return hash;
}

/* Función de hash simple (djb2) */
uint64_t _jade_hash(void *ptr) {
  /* Asumimos que las claves son strings por defecto */
  return _jade_hash_str((const char *)ptr);
}

JadeMap *jade_mapa_nuevo(void) {
  JadeMap *mapa = (JadeMap *)jade_malloc(sizeof(JadeMap));
  mapa->capacity = 16;
  mapa->size = 0;
  mapa->entries =
      (JadeMapEntry *)jade_malloc(sizeof(JadeMapEntry) * mapa->capacity);
  memset(mapa->entries, 0, sizeof(JadeMapEntry) * mapa->capacity);
  return mapa;
}

void _jade_mapa_redimensionar(JadeMap *mapa) {
  int64_t old_capacity = mapa->capacity;
  JadeMapEntry *old_entries = mapa->entries;

  mapa->capacity *= 2;
  mapa->entries =
      (JadeMapEntry *)jade_malloc(sizeof(JadeMapEntry) * mapa->capacity);
  memset(mapa->entries, 0, sizeof(JadeMapEntry) * mapa->capacity);
  mapa->size = 0;

  for (int64_t i = 0; i < old_capacity; i++) {
    if (old_entries[i].ocupado) {
      jade_mapa_asignar(mapa, old_entries[i].clave, old_entries[i].valor);
    }
  }

  jade_free(old_entries);
}

void jade_mapa_asignar(JadeMap *mapa, void *clave, void *valor) {
  if (mapa->size >= mapa->capacity * 0.75) {
    _jade_mapa_redimensionar(mapa);
  }

  uint64_t hash = _jade_hash(clave);
  int64_t index = hash % mapa->capacity;

  while (mapa->entries[index].ocupado) {
    /* Usar strcmp para comparar claves strings */
    if (strcmp((const char *)mapa->entries[index].clave, (const char *)clave) ==
        0) {
      /* Actualizar existente */
      mapa->entries[index].valor = valor;
      return;
    }
    index = (index + 1) % mapa->capacity;
  }

  /* Insertar nuevo */
  mapa->entries[index].clave = clave;
  mapa->entries[index].valor = valor;
  mapa->entries[index].ocupado = 1;
  mapa->size++;
}

void *jade_mapa_obtener(JadeMap *mapa, void *clave) {
  uint64_t hash = _jade_hash(clave);
  int64_t index = hash % mapa->capacity;
  int64_t start_index = index;

  do {
    if (mapa->entries[index].ocupado &&
        strcmp((const char *)mapa->entries[index].clave, (const char *)clave) ==
            0) {
      return mapa->entries[index].valor;
    }
    if (!mapa->entries[index].ocupado && mapa->entries[index].clave == NULL) {
      /* Encontró hueco vacío (no borrado), no existe */
      return NULL;
    }
    index = (index + 1) % mapa->capacity;
  } while (index != start_index);

  return NULL;
}

int jade_mapa_contiene(JadeMap *mapa, void *clave) {
  return jade_mapa_obtener(mapa, clave) != NULL;
}

void *jade_mapa_eliminar(JadeMap *mapa, void *clave) {
  uint64_t hash = _jade_hash(clave);
  int64_t index = hash % mapa->capacity;
  int64_t start_index = index;

  do {
    if (mapa->entries[index].ocupado &&
        strcmp((const char *)mapa->entries[index].clave, (const char *)clave) ==
            0) {
      void *valor = mapa->entries[index].valor;
      mapa->entries[index].ocupado = 0;
      /* No limpiamos clave/valor para marcar como "borrado" (tombstone)
         pero simplificamos aquí poniendo ocupado=0 */
      mapa->size--;
      return valor;
    }
    index = (index + 1) % mapa->capacity;
  } while (index != start_index);

  return NULL;
}

int64_t jade_mapa_longitud(JadeMap *mapa) { return mapa->size; }

JadeList *jade_mapa_claves(JadeMap *mapa) {
  JadeList *lista = jade_lista_nueva();
  for (int64_t i = 0; i < mapa->capacity; i++) {
    if (mapa->entries[i].ocupado) {
      jade_lista_agregar(lista, mapa->entries[i].clave);
    }
  }
  return lista;
}

JadeList *jade_mapa_valores(JadeMap *mapa) {
  JadeList *lista = jade_lista_nueva();
  for (int64_t i = 0; i < mapa->capacity; i++) {
    if (mapa->entries[i].ocupado) {
      jade_lista_agregar(lista, mapa->entries[i].valor);
    }
  }
  return lista;
}

void jade_mapa_liberar(JadeMap *mapa) {
  if (mapa) {
    if (mapa->entries) {
      jade_free(mapa->entries);
    }
    jade_free(mapa);
  }
}

/* ============================================================================
 * INICIALIZACIÓN
 * ============================================================================
 */

void jade_init_runtime(void) {
  // Inicializar generador de números aleatorios
  srand((unsigned int)time(NULL));
}
