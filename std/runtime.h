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

/* Inicialización */
void jade_init_runtime(void);

#endif /* JADE_RUNTIME_H */
