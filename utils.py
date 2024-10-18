import numpy as np

def CalcularErrorSistematico(ref, mediciones):
    errores = []
    # Calcular el error cuadrático medio para cada medición
    for medicion in mediciones:
        error_cuadratico = 1/len(mediciones) * np.sum((ref - medicion)**2)
        errores.append(np.sqrt(error_cuadratico))
        
    # Convertir la lista de errores a un array de NumPy
    errores = np.array(errores)
    
    return errores

def CalcularErrorAleatorio(mediciones):
    t = 1.96
    error_estandar = np.std(mediciones) / np.sqrt(len(mediciones))
    error_aleatorio = t*error_estandar
    return error_aleatorio

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
