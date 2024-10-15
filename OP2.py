import cv2 as cv
import os
import numpy as np
import time
from utils import TwoColorPyrometry, CalcularErrorSistematico, CalcularErrorAleatorio

temp_ref_celsius = 1485 # Temperatura de referencia en Celsius
temp_ref_kelvin = temp_ref_celsius + 273.15 # Temperatura de referencia en Kelvin

# Iniciar el timer
start_time = time.time()

op2_folder = './OP2'
img_op2 = [f for f in os.listdir(op2_folder) if f.endswith('.tiff')]

# Limitar a las primeras 100 imágenes
img_op2 = img_op2[:100]

# Lista para almacenar los valores de temperatura por imagen
calores_por_imagen = []

# Lista para almacenar los promedios de temperatura por imagen
promedios_temperatura = []

for i, imagen in enumerate(img_op2):
    # Cargar la imagen
    print(f"Procesando imagen {i}")
    ruta_imagen = os.path.join(op2_folder, imagen)
    imagen = cv.imread(ruta_imagen)
    
    # Verificar si la imagen se cargó correctamente
    if imagen is None:
        print(f"Error al cargar la imagen: {ruta_imagen}")
        continue

    # Obtener el canal rojo y verde de la imagen
    canal_rojo = imagen[:, :, 2].flatten()
    canal_verde = imagen[:, :, 1].flatten()

    # Calcular las temperaturas para cada par de píxeles rojo y verde
    calores_actuales = [TwoColorPyrometry(verde, rojo) for verde, rojo in zip(canal_verde, canal_rojo)]
    
    # Filtrar los valores de temperatura que sean 0
    calores_filtrados = [temp for temp in calores_actuales if temp != 0]
    
    # Agregar la lista de calores de la imagen actual a la lista principal
    calores_por_imagen.append(calores_filtrados)

    # Calcular el promedio de temperatura de la imagen actual
    if calores_filtrados:
        promedio_actual = np.mean(calores_filtrados)
    else:
        promedio_actual = 0

    promedios_temperatura.append(promedio_actual)

# Calcular el error sistemático entre la temperatura de referencia y los promedios de temperatura
errores_sistematicos = CalcularErrorSistematico(temp_ref_kelvin, promedios_temperatura)

# Guardar los errores sistemáticos en un archivo de texto
with open('OP2_errores_sistematicos.txt', 'w') as f:
    for error in errores_sistematicos:
        f.write(f"{error};\n")

# Calcular el error aleatorio entre la temperatura de referencia y los valores de temperatura por imagen
errores_aleatorios = [CalcularErrorAleatorio(temp_ref_kelvin, calores) for calores in calores_por_imagen]

# Guardar los errores aleatorios en un archivo de texto
with open('OP2_errores_aleatorios.txt', 'w') as f:
    for error in errores_aleatorios:
        f.write(f"{error};\n")