#ifndef CXMATH_H
#define CXMATH_H

#ifdef __cplusplus
extern "C" {
#endif

#define CX_GENERIC(a, A, fA, B, fB) \
    _Generic((a), A: fA, B: fB)

typedef struct{double real;double imag;} Complex;
typedef struct{long double real;long double imag;} longComplex;
typedef struct{double x;double y;} Vector2;
typedef struct{double x;double y;double z;} Vector3;
typedef struct{long double x;long double y;} longVector2;
typedef struct{long double x;long double y;long double z;} longVector3;

#define c_mod(a) CX_GENERIC(a, Complex, complex_mod, longComplex, long_complex_mod )(a)
#define c_arg(a) CX_GENERIC(a, Complex, complex_arg, longComplex, long_complex_arg )(a)
#define c_conj(a) CX_GENERIC(a, Complex, complex_conj, longComplex, long_complex_conj )(a)
#define c_square(a) CX_GENERIC(a, Complex, complex_square, longComplex, long_complex_square )(a)
#define c_add(a, b) CX_GENERIC(a, Complex, complex_add, longComplex, long_complex_add )(a, b)
#define c_sub(a, b) CX_GENERIC(a, Complex, complex_sub, longComplex, long_complex_sub )(a, b)
#define c_mult(a, b) CX_GENERIC(a, Complex, complex_mult, longComplex, long_complex_mult )(a, b)
#define c_div(a, b) CX_GENERIC(a, Complex, complex_div, longComplex, long_complex_div )(a, b)

#define v_norm(a) CX_GENERIC(a, Vector2, vector2_norm, longVector2, long_vector2_norm, Vector3, vector3_norm, longVector3, long_vector3_norm)(a)
#define v_dot(a, b) CX_GENERIC(a, Vector2, vector2_dot, longVector2, long_vector2_dot, Vector3, vector3_dot, longVector3, long_vector3_dot)(a, b)
#define v_add(a, b) CX_GENERIC(a, Vector2, vector2_add, longVector2, long_vector2_add, Vector3, vector3_add, longVector3, long_vector3_add)(a, b)
#define v_sub(a, b) CX_GENERIC(a, Vector2, vector2_sub, longVector2, long_vector2_sub, Vector3, vector3_sub, longVector3, long_vector3_sub)(a, b)
#define v_scale(a, b) CX_GENERIC(a, Vector2, vector2_scale, longVector2, long_vector2_scale, Vector3, vector3_scale, longVector3, long_vector3_scale)(a, b)
#define v_prod(a, b) CX_GENERIC(a, Vector3, vector3_prod, longVector3, long_vector3_prod)(a, b)

double complex_mod(const Complex c1);
double complex_arg(const Complex c1);
Complex complex_conj(const Complex c1);
Complex complex_square(const Complex c1);
Complex complex_add(const Complex c1, const Complex c2);
Complex complex_sub(const Complex c1, const Complex c2);
Complex complex_mult(const Complex c1, const Complex c2);
Complex complex_div(const Complex c1, const Complex c2);

long double long_complex_mod(const longComplex c1);
long double long_complex_arg(const longComplex c1);
longComplex long_complex_conj(const longComplex c1);
longComplex long_complex_square(const longComplex c1);
longComplex long_complex_add(const longComplex c1, const longComplex c2);
longComplex long_complex_sub(const longComplex c1, const longComplex c2);
longComplex long_complex_mult(const longComplex c1, const longComplex c2);
longComplex long_complex_div(const longComplex c1, const longComplex c2);

double vector2_norm(const Vector2 u);
double vector2_dot(const Vector2 u, const Vector2 v);
Vector2 vector2_add(const Vector2 u, const Vector2 v);
Vector2 vector2_sub(const Vector2 u, const Vector2 v);
Vector2 vector2_scale(const Vector2 u, const double k);

long double long_vector2_norm(const longVector2 u);
long double long_vector2_dot(const longVector2 u, const longVector2 v);
longVector2 long_vector2_add(const longVector2 u, const longVector2 v);
longVector2 long_vector2_sub(const longVector2 u, const longVector2 v);
longVector2 long_vector2_scale(const longVector2 u, const long double k);

double vector3_norm(const Vector3 u);
double vector3_dot(const Vector3 u, const Vector3 v);
Vector3 vector3_add(const Vector3 u, const Vector3 v);
Vector3 vector3_sub(const Vector3 u, const Vector3 v);
Vector3 vector3_prod(const Vector3 u, const Vector3 v);
Vector3 vector3_scale(const Vector3 u, const double k);

long double long_vector3_norm(const longVector3 u);
long double long_vector3_dot(const longVector3 u, const longVector3 v);
longVector3 long_vector3_add(const longVector3 u, const longVector3 v);
longVector3 long_vector3_sub(const longVector3 u, const longVector3 v);
longVector3 long_vector3_prod(const longVector3 u, const longVector3 v);
longVector3 long_vector3_scale(const longVector3 u, const long double k);

#ifdef __cplusplus
}
#endif
#endif