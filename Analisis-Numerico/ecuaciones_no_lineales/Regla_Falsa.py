import pandas as pd
import numpy as np
import math

print("=== MÉTODO DE LA REGLA FALSA (FALSE POSITION) ===")
print("Ingrese los datos del problema:")

print("X0 (extremo izquierdo del intervalo):")
X0 = float(input())
print("X1 (extremo derecho del intervalo):")
X1 = float(input())
print("Tolerancia:")
Tol = float(input())
print("Número máximo de iteraciones:")
Niter = int(input())
print("Función f(x) (usar 'x' como variable):")
Fun = input()

# Listas para almacenar iteraciones
iteraciones = []
c = 0  # contador de iteraciones

# Evaluación inicial
x = X0
f0 = eval(Fun)
x = X1  
f1 = eval(Fun)

print(f"\nEvaluación inicial:")
print(f"f({X0}) = {f0}")
print(f"f({X1}) = {f1}")
print(f"f(X0) * f(X1) = {f0 * f1}")

# Verificaciones iniciales según el algoritmo
if f0 == 0:
    print(f"\n{X0} es raíz exacta de f(x)")
    iteraciones.append({
        'Iteración': 0,
        'X0': X0,
        'X1': X1,
        'X2': X0,
        'f(X0)': f0,
        'f(X1)': f1,
        'f(X2)': f0,
        'Error': 0,
        'Observación': 'Raíz exacta en X0'
    })
elif f1 == 0:
    print(f"\n{X1} es raíz exacta de f(x)")
    iteraciones.append({
        'Iteración': 0,
        'X0': X0,
        'X1': X1,
        'X2': X1,
        'f(X0)': f0,
        'f(X1)': f1,
        'f(X2)': f1,
        'Error': 0,
        'Observación': 'Raíz exacta en X1'
    })
elif f0 * f1 >= 0:
    print(f"\nError: No hay cambio de signo en el intervalo [{X0}, {X1}]")
    print("El método de Regla Falsa requiere f(X0) * f(X1) < 0")
    iteraciones.append({
        'Iteración': 0,
        'X0': X0,
        'X1': X1,
        'X2': None,
        'f(X0)': f0,
        'f(X1)': f1,
        'f(X2)': None,
        'Error': None,
        'Observación': 'Intervalo inadecuado'
    })
else:
    print(f"\nHay cambio de signo. Iniciando método de Regla Falsa...")
    
    # Variables para el método
    X0_actual = X0
    X1_actual = X1
    f0_actual = f0
    f1_actual = f1
    Error = float('inf')
    
    while Error > Tol and c < Niter:
        # Step 2: Calcular X2 usando la fórmula de interpolación lineal
        # Usando Formula-1: X2 = X0 - f(X0) * (X1 - X0) / (f(X1) - f(X0))
        if abs(f1_actual - f0_actual) < 1e-12:  # Evitar división por cero
            print("Error: División por cero en la fórmula de interpolación")
            break
            
        X2 = X0_actual - f0_actual * (X1_actual - X0_actual) / (f1_actual - f0_actual)
        
        # Evaluar f(X2)
        x = X2
        f2 = eval(Fun)
        
        # Calcular error (distancia entre iteraciones consecutivas)
        if c > 0:
            Error = abs(X2 - X2_anterior)
        else:
            Error = abs(X2 - X0_actual)  # Primera iteración
        
        # Registrar iteración
        iteraciones.append({
            'Iteración': c + 1,
            'X0': X0_actual,
            'X1': X1_actual,
            'X2': X2,
            'f(X0)': f0_actual,
            'f(X1)': f1_actual,
            'f(X2)': f2,
            'Error': Error,
            'Observación': ''
        })
        
        # Step 3: Verificar condiciones y actualizar intervalo
        if f2 == 0:
            print(f"\n¡Raíz exacta encontrada! X2 = {X2}")
            iteraciones[-1]['Observación'] = 'Raíz exacta encontrada'
            break
        elif f0_actual * f2 < 0:
            # La raíz está entre X0 y X2, entonces X1 = X2
            X1_actual = X2
            f1_actual = f2
            iteraciones[-1]['Observación'] = 'Raíz en [X0, X2] → X1 = X2'
        elif f2 * f1_actual < 0:
            # La raíz está entre X2 y X1, entonces X0 = X2  
            X0_actual = X2
            f0_actual = f2
            iteraciones[-1]['Observación'] = 'Raíz en [X2, X1] → X0 = X2'
        else:
            print("Error: Pérdida de cambio de signo")
            iteraciones[-1]['Observación'] = 'Error: Pérdida de cambio de signo'
            break
        
        X2_anterior = X2
        c += 1
    
    # Step 4: Verificar condiciones de parada
    if c >= Niter:
        print(f"\nMétodo terminó por límite de iteraciones ({Niter})")
        print(f"Última aproximación: X = {X2}")
        print(f"Error final: {Error}")
        if iteraciones:
            iteraciones[-1]['Observación'] += ' - Límite de iteraciones'
    elif Error <= Tol:
        print(f"\nConvergencia alcanzada!")
        print(f"Raíz aproximada: X = {X2}")
        print(f"Error final: {Error}")
        print(f"Tolerancia: {Tol}")
        if iteraciones:
            iteraciones[-1]['Observación'] += ' - Convergencia alcanzada'

# Mostrar tabla de iteraciones
print("\n" + "="*100)
print("TABLA DE ITERACIONES - MÉTODO DE REGLA FALSA")
print("="*100)

if iteraciones:
    df = pd.DataFrame(iteraciones)
    # Configurar formato de pandas
    pd.set_option('display.float_format', '{:.8f}'.format)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(df.to_string(index=False))
else:
    print("No se realizaron iteraciones.")

print("\n" + "="*100)
