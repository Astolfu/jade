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
 * INICIALIZACIÓN
 * ============================================================================
 */

void jade_init_runtime(void) {
  // Inicializar generador de números aleatorios
  srand((unsigned int)time(NULL));
}
