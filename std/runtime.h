/*
 * Runtime de Jade - Headers
 */

#ifndef JADE_RUNTIME_H
#define JADE_RUNTIME_H

#include <stddef.h>
#include <stdint.h>

/* Gestión de memoria */
void *jade_malloc(size_t size);
void jade_free(void *ptr);

/* Entrada/Salida */
void jade_mostrar(const char *texto);
char *jade_leer(void);

/* Conversiones */
char *jade_convertir_a_texto_entero(int64_t n);
char *jade_convertir_a_texto_flotante(double n);
char *jade_convertir_a_texto_booleano(int b);
int64_t jade_convertir_a_entero(const char *str);
double jade_convertir_a_flotante(const char *str);

/* Funciones matemáticas */
int64_t jade_abs_entero(int64_t x);
double jade_abs_flotante(double x);
int64_t jade_max_entero(int64_t a, int64_t b);
int64_t jade_min_entero(int64_t a, int64_t b);
double jade_potencia(double base, double exp);
double jade_raiz(double x);
double jade_aleatorio(void);

/* ============================================================================
 * ESTRUCTURAS DE DATOS
 * ============================================================================
 */

/* Listas dinámicas */
typedef struct {
  void **data;      /* Array de punteros a elementos */
  int64_t size;     /* Número actual de elementos */
  int64_t capacity; /* Capacidad reservada */
} JadeList;

JadeList *jade_lista_nueva(void);
void jade_lista_agregar(JadeList *lista, void *elemento);
void *jade_lista_obtener(JadeList *lista, int64_t indice);
void jade_lista_asignar(JadeList *lista, int64_t indice, void *valor);
int64_t jade_lista_longitud(JadeList *lista);
void *jade_lista_eliminar(JadeList *lista, int64_t indice);
int jade_lista_contiene(JadeList *lista, void *elemento);
void jade_lista_liberar(JadeList *lista);

/* Mapas (Hash Map simple) */
typedef struct {
  void *clave;
  void *valor;
  int ocupado; /* 1 si tiene valor, 0 si está vacío/borrado */
} JadeMapEntry;

typedef struct {
  JadeMapEntry *entries;
  int64_t capacity;
  int64_t size;
} JadeMap;

JadeMap *jade_mapa_nuevo(void);
void jade_mapa_asignar(JadeMap *mapa, void *clave, void *valor);
void *jade_mapa_obtener(JadeMap *mapa, void *clave);
void *jade_mapa_eliminar(JadeMap *mapa, void *clave);
int jade_mapa_contiene(JadeMap *mapa, void *clave);
int64_t jade_mapa_longitud(JadeMap *mapa);
JadeList *jade_mapa_claves(JadeMap *mapa);
JadeList *jade_mapa_valores(JadeMap *mapa);
void jade_mapa_liberar(JadeMap *mapa);

/* Operaciones de cadenas (faltantes) */
char *jade_concatenar(const char *a, const char *b);
int64_t jade_longitud(const char *str);

/* Inicialización */
void jade_init_runtime(void);

#endif /* JADE_RUNTIME_H */
