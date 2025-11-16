import numpy as np
import pandas as pd


def pivpar(Ab, n, k):
    """
    Pivoteo parcial - busca el mayor elemento en la columna k desde la fila k hacia abajo
    """
    mayor = abs(Ab[k, k])
    fila_mayor = k
    
    for i in range(k + 1, n):
        if abs(Ab[i, k]) > mayor:
            mayor = abs(Ab[i, k])
            fila_mayor = i
    
    # Intercambiar filas si es necesario
    if fila_mayor != k:
        Ab[[k, fila_mayor]] = Ab[[fila_mayor, k]]
    
    return Ab


def pivtot(Ab, mark, n, k):
    """
    Pivoteo total - busca el mayor elemento en la submatriz desde (k,k)
    """
    mayor = abs(Ab[k, k])
    fila_mayor = k
    col_mayor = k
    
    for i in range(k, n):
        for j in range(k, n):
            if abs(Ab[i, j]) > mayor:
                mayor = abs(Ab[i, j])
                fila_mayor = i
                col_mayor = j
    
    # Intercambiar filas si es necesario
    if fila_mayor != k:
        Ab[[k, fila_mayor]] = Ab[[fila_mayor, k]]
    
    # Intercambiar columnas si es necesario
    if col_mayor != k:
        Ab[:, [k, col_mayor]] = Ab[:, [col_mayor, k]]
        mark[k], mark[col_mayor] = mark[col_mayor], mark[k]
    
    return Ab, mark


def sustreg(Ab, n):
    """
    Sustitución regresiva para resolver sistema triangular superior
    """
    x = np.zeros(n)
    
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += Ab[i, j] * x[j]
        x[i] = (Ab[i, n] - suma) / Ab[i, i]
    
    return x


def GaussPiv(A, b, n, Piv):
    """
    Implementación del método de Gauss con pivoteo
    
    Parámetros:
    A: matriz de coeficientes (n x n)
    b: vector de términos independientes (n x 1)
    n: tamaño del sistema
    Piv: tipo de pivoteo (0: sin pivoteo, 1: pivoteo parcial, 2: pivoteo total)
    
    Retorna:
    x: vector solución
    mark: marcador de variables (útil para pivoteo total)
    """
    # Convertir a numpy arrays si no lo son
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    # Crear matriz aumentada
    Ab = np.column_stack([A, b])
    
    # Inicializar marcador de variables
    mark = list(range(n))
    
    # Proceso de eliminación
    for k in range(n - 1):
        # Aplicar pivoteo según el tipo especificado
        if Piv == 1:
            Ab = pivpar(Ab, n, k)
        elif Piv == 2:
            Ab, mark = pivtot(Ab, mark, n, k)
        
        # Verificar que el pivote no sea cero
        if abs(Ab[k, k]) < 1e-10:
            raise ValueError(f"Pivote cero o muy pequeño en la fila {k}")
        
        # Eliminación hacia adelante
        for i in range(k + 1, n):
            M = Ab[i, k] / Ab[k, k]
            for j in range(k, n + 1):
                Ab[i, j] = Ab[i, j] - M * Ab[k, j]
    
    # Verificar que el último pivote no sea cero
    if abs(Ab[n-1, n-1]) < 1e-10:
        raise ValueError(f"Pivote cero o muy pequeño en la última fila")
    
    # Resolver por sustitución regresiva
    x = sustreg(Ab, n)
    
    return x, mark


# Función auxiliar para mostrar el proceso paso a paso
def GaussPiv_verbose(A, b, n, Piv, verbose=True):
    """
    Versión verbose del método de Gauss con pivoteo que muestra el proceso
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    Ab = np.column_stack([A, b])
    mark = list(range(n))
    
    if verbose:
        print("Matriz aumentada inicial:")
        print(Ab)
        print()
    
    for k in range(n - 1):
        if Piv == 1:
            Ab = pivpar(Ab, n, k)
            if verbose:
                print(f"Después del pivoteo parcial en paso {k+1}:")
                print(Ab)
        elif Piv == 2:
            Ab, mark = pivtot(Ab, mark, n, k)
            if verbose:
                print(f"Después del pivoteo total en paso {k+1}:")
                print(Ab)
                print(f"Marcador de variables: {mark}")
        
        if abs(Ab[k, k]) < 1e-10:
            raise ValueError(f"Pivote cero o muy pequeño en la fila {k}")
        
        if verbose:
            print(f"\nEliminación en columna {k+1}:")
        
        for i in range(k + 1, n):
            M = Ab[i, k] / Ab[k, k]
            if verbose:
                print(f"M_{i+1},{k+1} = {M:.6f}")
            for j in range(k, n + 1):
                Ab[i, j] = Ab[i, j] - M * Ab[k, j]
        
        if verbose:
            print("Matriz después de la eliminación:")
            print(Ab)
            print()
    
    if abs(Ab[n-1, n-1]) < 1e-10:
        raise ValueError(f"Pivote cero o muy pequeño en la última fila")
    
    x = sustreg(Ab, n)
    
    if verbose:
        print("Solución:")
        if Piv == 2:
            # Reordenar la solución según el marcador de variables
            x_ordenada = np.zeros(n)
            for i in range(n):
                x_ordenada[mark[i]] = x[i]
            print(f"x = {x_ordenada}")
        else:
            print(f"x = {x}")
    
    return x, mark