import numpy as np

def CalcularErrorSistematico(ref, mediciones):
    vec_error = []
    for medicion in mediciones:
      vec_error.append(np.abs(ref - medicion))
    return vec_error

def CalcularErrorAleatorio(ref, mediciones):
    error_total = 0
    # Suma de los errores cuadrados
    for i in range(len(mediciones)):
        error_total += np.sum((ref - mediciones[i])**2)

    # Promedio de errores cuadrados
    error_promedio = error_total / len(mediciones)
    
    # Raíz cuadrada del error promedio (Error cuadrático medio)
    raiz_error = np.sqrt(error_promedio)

    return raiz_error


def TwoColorPyrometry(verde, rojo):
    c2 = 0.014387
    lambda1 = 580 * (10**(-7))
    lambda2 = 620 * (10**(-7))

    E_est1 = rojo
    E_est2 = verde

    # Verificar que E_est1 y E_est2 no sean cero
    if E_est1 == 0 or E_est2 == 0:
        return 0

    parte_arriba = c2 * ((1/lambda1) - (1/lambda2))
    log_ratio = np.log(E_est1/E_est2)

    # Verificar que log_ratio no sea infinito
    if np.isinf(log_ratio):
        return 0

    parte_abajo = log_ratio + 5 * np.log(lambda1/lambda2)

    temperatura = parte_arriba/parte_abajo

    if 1000 <= temperatura <= 3000:
        return temperatura
    else:
        return 0
