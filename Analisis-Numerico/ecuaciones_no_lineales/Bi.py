import math
import pandas as pd
import numpy as np

print("X0:")
X0 = float(input())
print("Delta:")
Delta = float(input())

# Validar que Delta > 0
while Delta <= 0:
    print("Error: Delta debe ser mayor que 0. Ingrese un valor positivo:")
    Delta = float(input())

print("Niter:")
Niter = int(input())
print("Function:")
Fun = input()

# Lista para almacenar las iteraciones
iteraciones = []

x = X0
f0 = eval(Fun)

if f0 == 0:
    s = x
    print(X0, "es raiz de f(x)")
    # Agregar la única iteración a la tabla
    iteraciones.append({
        'Iteración': 0,
        'X0': X0,
        'X1': None,
        'f(X0)': f0,
        'f(X1)': None,
        'f(X0)*f(X1)': None,
        'Observación': 'Raíz exacta encontrada'
    })
else:
    X1 = X0 + Delta
    x = X1
    c = 1
    f1 = eval(Fun)
    
    # Registrar la primera iteración
    iteraciones.append({
        'Iteración': c,
        'X0': X0,
        'X1': X1,
        'f(X0)': f0,
        'f(X1)': f1,
        'f(X0)*f(X1)': f0 * f1,
        'Observación': 'Mismo signo' if f0 * f1 > 0 else 'Cambio de signo'
    })
    
    while f0 * f1 > 0 and c < Niter:
        X0 = X1
        f0 = f1
        X1 = X0 + Delta
        x = X1
        f1 = eval(Fun)
        c = c + 1
        
        # Registrar cada iteración
        iteraciones.append({
            'Iteración': c,
            'X0': X0,
            'X1': X1,
            'f(X0)': f0,
            'f(X1)': f1,
            'f(X0)*f(X1)': f0 * f1,
            'Observación': 'Mismo signo' if f0 * f1 > 0 else 'Cambio de signo'
        })
    if f1 == 0:
        s = x
        print(X1, "es raiz de f(x)")
        # Actualizar la observación de la última iteración
        if iteraciones:
            iteraciones[-1]['Observación'] = 'Raíz exacta encontrada'
    elif f0 * f1 < 0:
        s = x
        print("Existe una raiz de f(x) entre", X0, "y", X1)
        # Actualizar la observación de la última iteración
        if iteraciones:
            iteraciones[-1]['Observación'] = 'Cambio de signo - Raíz encontrada'
    else:
        s = x
        print("Fracaso en", Niter, "iteraciones")
        # Actualizar la observación de la última iteración
        if iteraciones:
            iteraciones[-1]['Observación'] = 'Límite de iteraciones alcanzado'

# Mostrar tabla de iteraciones
print("\n" + "="*80)
print("TABLA DE ITERACIONES")
print("="*80)
if iteraciones:
    df = pd.DataFrame(iteraciones)
    # Formatear los números para mejor visualización
    pd.set_option('display.float_format', '{:.6f}'.format)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df.to_string(index=False))
else:
    print("No se realizaron iteraciones.")
