import math
import sys
from typing import Tuple

# Error de máquina
EPSILON_MAQUINA = sys.float_info.epsilon

def error_relativo_binario(X, Ex, Y, Ey, operacion):
    """Calcula el error relativo para operaciones básicas."""
    if operacion == '+':
        resultado = X + Y
        e_rel = abs((X / resultado) * Ex + (Y / resultado) * Ey) + EPSILON_MAQUINA
    elif operacion == '-':
        resultado = X - Y
        e_rel = abs((X / resultado) * Ex - (Y / resultado) * Ey) + EPSILON_MAQUINA
    elif operacion == '*':
        resultado = X * Y
        e_rel = abs(Ex + Ey) + EPSILON_MAQUINA
    elif operacion == '/':
        resultado = X / Y
        e_rel = abs(Ex - Ey) + EPSILON_MAQUINA
    else:
        raise ValueError(f"Operación '{operacion}' no soportada.")
    return resultado, e_rel

def error_potencia(X, Ex, n):
    """Error relativo para potencias X**n."""
    resultado = X ** n
    e_rel = abs(n * Ex) + EPSILON_MAQUINA
    return resultado, e_rel

# Ejemplo para Z = X**2 + Y**2
if __name__ == "__main__":
    X = 0.80
    Ex = 0.5e-2
    Y = 0.95
    Ey = 0.7e-3

    # Paso 1: calcular X^2 y Y^2 con sus errores
    X2, EX2 = error_potencia(X, Ex, 2)
    Y2, EY2 = error_potencia(Y, Ey, 2)

    # Paso 2: sumar X^2 + Y^2
    Z, EZ = error_relativo_binario(X2, EX2, Y2, EY2, '+')

    print(f"Z = {Z:.6f}")
    print(f"Error relativo de Z = {EZ:.6e}")
    print(f"Error absoluto de Z = {EZ * abs(Z):.6e}")
