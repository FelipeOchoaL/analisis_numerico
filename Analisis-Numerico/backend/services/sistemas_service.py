import numpy as np
import pandas as pd
import base64
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Dict, List, Any
import time


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


# ====================================
# MÉTODOS ITERATIVOS
# ====================================

def jacobi(x0, A, b, tol, niter, modo="absoluto"):
    """
    Método iterativo de Jacobi para resolver sistemas lineales Ax = b
    
    Parámetros:
    x0 (numpy.ndarray): Vector inicial
    A (numpy.ndarray): Matriz de coeficientes
    b (numpy.ndarray): Vector de términos independientes
    tol (float): Tolerancia de convergencia
    niter (int): Número máximo de iteraciones
    modo (str): "relativo" o "absoluto" para cálculo de error
    
    Retorna:
    dict: Diccionario con resultados del método
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        x0 = np.array(x0, dtype=float)
        
        n = len(A)
        c = 0
        error = tol + 1
        errores = []
        soluciones = []
        
        # Descomponer la matriz A = D + L + U
        D = np.diag(np.diag(A))
        L = np.tril(A, -1)
        U = np.triu(A, 1)
        
        # Calcular matriz de iteración T = -D^(-1) * (L + U)
        D_inv = np.linalg.inv(D)
        T = -D_inv @ (L + U)
        C = D_inv @ b
        sp_radius = max(abs(np.linalg.eigvals(T)))
        
        while error > tol and c < niter:
            x1 = T.dot(x0) + C
            
            if modo == "relativo":
                error = np.linalg.norm((x1 - x0) / x1, np.inf)
            else:
                error = np.linalg.norm(x1 - x0, np.inf)
            
            errores.append(error)
            soluciones.append(x1.copy())
            x0 = x1
            c += 1
        
        # Crear tabla de iteraciones
        tabla_data = {'Iteración': np.arange(1, c + 1)}
        for i in range(len(A)):
            tabla_data[f'x{i+1}'] = [x[i] for x in soluciones]
        tabla_data['Error'] = errores
        
        df_resultado = pd.DataFrame(tabla_data)
        tabla_html = df_resultado.to_html(index=False, classes='table table-striped text-center', float_format=lambda x: f'{x:.8f}')
        
        exito = error < tol
        converge_teorico = sp_radius < 1
        
        # Mensaje con información de convergencia
        if exito:
            mensaje = f"✅ Jacobi convergió en {c} iteraciones con tolerancia {tol}. Radio espectral: {sp_radius:.6f}"
        else:
            mensaje = f"⚠️ Jacobi fracasó en {niter} iteraciones. Radio espectral: {sp_radius:.6f}"
        
        if converge_teorico:
            mensaje += " - El método SÍ debería converger teóricamente (ρ < 1)."
        else:
            mensaje += " - El método NO debería converger teóricamente (ρ ≥ 1)."
        
        return {
            "exito": exito,
            "solucion": x0.tolist() if exito else None,
            "iteraciones": c,
            "error_final": float(error),
            "radio_espectral": float(sp_radius),
            "tabla_html": tabla_html,
            "mensaje": mensaje,
            "errores": [float(e) for e in errores],
            "converge_teorico": converge_teorico
        }
        
    except np.linalg.LinAlgError as e:
        return {
            "exito": False,
            "solucion": None,
            "iteraciones": 0,
            "error_final": None,
            "radio_espectral": None,
            "tabla_html": None,
            "mensaje": f"Error en el método: {str(e)}. La matriz puede ser singular.",
            "errores": [],
            "converge_teorico": False
        }
    except Exception as e:
        return {
            "exito": False,
            "solucion": None,
            "iteraciones": 0,
            "error_final": None,
            "radio_espectral": None,
            "tabla_html": None,
            "mensaje": f"Error: {str(e)}",
            "errores": [],
            "converge_teorico": False
        }


def gauss_seidel(x0, A, b, tol, niter, modo="absoluto"):
    """
    Método iterativo de Gauss-Seidel para resolver sistemas lineales Ax = b
    
    Parámetros:
    x0 (numpy.ndarray): Vector inicial
    A (numpy.ndarray): Matriz de coeficientes
    b (numpy.ndarray): Vector de términos independientes
    tol (float): Tolerancia de convergencia
    niter (int): Número máximo de iteraciones
    modo (str): "relativo" o "absoluto" para cálculo de error
    
    Retorna:
    dict: Diccionario con resultados del método
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        x0 = np.array(x0, dtype=float)
        
        n = len(A)
        c = 0
        error = tol + 1
        errores = []
        soluciones = []
        
        # Descomponer la matriz A = D + L + U
        D = np.diag(np.diag(A))
        L = np.tril(A, -1)
        U = np.triu(A, 1)
        
        # Calcular matriz de iteración T = -(D + L)^(-1) * U
        DL_inv = np.linalg.inv(D + L)
        T = -DL_inv @ U
        C = DL_inv @ b
        sp_radius = max(abs(np.linalg.eigvals(T)))
        
        while error > tol and c < niter:
            x1 = T @ x0 + C
            
            if modo == "relativo":
                error = np.linalg.norm((x1 - x0) / x1, np.inf)
            else:
                error = np.linalg.norm(x1 - x0, np.inf)
            
            errores.append(error)
            soluciones.append(x1.copy())
            x0 = x1
            c += 1
        
        # Crear tabla de iteraciones
        tabla_data = {'Iteración': np.arange(1, c + 1)}
        for i in range(len(A)):
            tabla_data[f'x{i+1}'] = [x[i] for x in soluciones]
        tabla_data['Error'] = errores
        
        df_resultado = pd.DataFrame(tabla_data)
        tabla_html = df_resultado.to_html(index=False, classes='table table-striped text-center', float_format=lambda x: f'{x:.8f}')
        
        exito = error < tol
        converge_teorico = sp_radius < 1
        
        # Mensaje con información de convergencia
        if exito:
            mensaje = f"✅ Gauss-Seidel convergió en {c} iteraciones con tolerancia {tol}. Radio espectral: {sp_radius:.6f}"
        else:
            mensaje = f"⚠️ Gauss-Seidel fracasó en {niter} iteraciones. Radio espectral: {sp_radius:.6f}"
        
        if converge_teorico:
            mensaje += " - El método SÍ debería converger teóricamente (ρ < 1)."
        else:
            mensaje += " - El método NO debería converger teóricamente (ρ ≥ 1)."
        
        return {
            "exito": exito,
            "solucion": x0.tolist() if exito else None,
            "iteraciones": c,
            "error_final": float(error),
            "radio_espectral": float(sp_radius),
            "tabla_html": tabla_html,
            "mensaje": mensaje,
            "errores": [float(e) for e in errores],
            "converge_teorico": converge_teorico
        }
        
    except np.linalg.LinAlgError as e:
        return {
            "exito": False,
            "solucion": None,
            "iteraciones": 0,
            "error_final": None,
            "radio_espectral": None,
            "tabla_html": None,
            "mensaje": f"Error en el método: {str(e)}. La matriz puede ser singular.",
            "errores": [],
            "converge_teorico": False
        }
    except Exception as e:
        return {
            "exito": False,
            "solucion": None,
            "iteraciones": 0,
            "error_final": None,
            "radio_espectral": None,
            "tabla_html": None,
            "mensaje": f"Error: {str(e)}",
            "errores": [],
            "converge_teorico": False
        }


def sor(x0, A, b, tol, niter, w, modo="absoluto"):
    """
    Método de Sobre-Relajación Sucesiva (SOR) para resolver sistemas lineales Ax = b
    
    Parámetros:
    x0 (numpy.ndarray): Vector inicial
    A (numpy.ndarray): Matriz de coeficientes
    b (numpy.ndarray): Vector de términos independientes
    tol (float): Tolerancia de convergencia
    niter (int): Número máximo de iteraciones
    w (float): Parámetro de relajación (0 < w < 2)
    modo (str): "relativo" o "absoluto" para cálculo de error
    
    Retorna:
    dict: Diccionario con resultados del método
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        x0 = np.array(x0, dtype=float)
        
        # Validar parámetro w
        if not (0 < w < 2):
            return {
                "exito": False,
                "solucion": None,
                "iteraciones": 0,
                "error_final": None,
                "radio_espectral": None,
                "tabla_html": None,
                "mensaje": f"Error: El parámetro w debe estar en el rango (0, 2). Valor proporcionado: {w}",
                "errores": [],
                "converge_teorico": False
            }
        
        n = len(A)
        c = 0
        error = tol + 1
        errores = []
        soluciones = []
        
        # Descomponer la matriz A = D + L + U
        D = np.diag(np.diag(A))
        L = np.tril(A, -1)
        U = np.triu(A, 1)
        
        # Calcular matriz de iteración T = (D + wL)^(-1) * ((1-w)D - wU)
        DwL_inv = np.linalg.inv(D + w * L)
        T = DwL_inv @ ((1 - w) * D - w * U)
        C = w * DwL_inv @ b
        sp_radius = max(abs(np.linalg.eigvals(T)))
        
        while error > tol and c < niter:
            x1 = T @ x0 + C
            
            if modo == "relativo":
                error = np.linalg.norm((x1 - x0) / x1, ord=np.inf)
            else:
                error = np.linalg.norm(x1 - x0, ord=np.inf)
            
            errores.append(error)
            soluciones.append(x1.copy())
            x0 = x1
            c += 1
        
        # Crear tabla de iteraciones
        tabla_data = {'Iteración': np.arange(1, c + 1)}
        for i in range(len(A)):
            tabla_data[f'x{i+1}'] = [x[i] for x in soluciones]
        tabla_data['Error'] = errores
        
        df_resultado = pd.DataFrame(tabla_data)
        tabla_html = df_resultado.to_html(index=False, classes='table table-striped text-center', float_format=lambda x: f'{x:.8f}')
        
        exito = error < tol
        converge_teorico = sp_radius < 1
        
        # Mensaje con información de convergencia
        if exito:
            mensaje = f"✅ SOR (ω={w}) convergió en {c} iteraciones con tolerancia {tol}. Radio espectral: {sp_radius:.6f}"
        else:
            mensaje = f"⚠️ SOR (ω={w}) fracasó en {niter} iteraciones. Radio espectral: {sp_radius:.6f}"
        
        if converge_teorico:
            mensaje += " - El método SÍ debería converger teóricamente (ρ < 1)."
        else:
            mensaje += " - El método NO debería converger teóricamente (ρ ≥ 1)."
        
        return {
            "exito": exito,
            "solucion": x0.tolist() if exito else None,
            "iteraciones": c,
            "error_final": float(error),
            "radio_espectral": float(sp_radius),
            "tabla_html": tabla_html,
            "mensaje": mensaje,
            "errores": [float(e) for e in errores],
            "converge_teorico": converge_teorico,
            "omega": w
        }
        
    except np.linalg.LinAlgError as e:
        return {
            "exito": False,
            "solucion": None,
            "iteraciones": 0,
            "error_final": None,
            "radio_espectral": None,
            "tabla_html": None,
            "mensaje": f"Error en el método: {str(e)}. La matriz puede ser singular.",
            "errores": [],
            "converge_teorico": False
        }
    except Exception as e:
        return {
            "exito": False,
            "solucion": None,
            "iteraciones": 0,
            "error_final": None,
            "radio_espectral": None,
            "tabla_html": None,
            "mensaje": f"Error: {str(e)}",
            "errores": [],
            "converge_teorico": False
        }


def comparar_metodos_iterativos(A, b, x0, tol, niter, w=1.5, modo="absoluto"):
    """
    Compara los tres métodos iterativos: Jacobi, Gauss-Seidel y SOR
    
    Parámetros:
    A (numpy.ndarray): Matriz de coeficientes
    b (numpy.ndarray): Vector de términos independientes
    x0 (numpy.ndarray): Vector inicial
    tol (float): Tolerancia de convergencia
    niter (int): Número máximo de iteraciones
    w (float): Parámetro de relajación para SOR
    modo (str): "relativo" o "absoluto" para cálculo de error
    
    Retorna:
    dict: Diccionario con resultados comparativos
    """
    resultados = {}
    tiempos = {}
    
    # 1. Jacobi
    inicio = time.time()
    resultado_jacobi = jacobi(x0, A, b, tol, niter, modo)
    fin = time.time()
    tiempos["Jacobi"] = fin - inicio
    resultados["Jacobi"] = resultado_jacobi
    
    # 2. Gauss-Seidel
    inicio = time.time()
    resultado_gs = gauss_seidel(x0, A, b, tol, niter, modo)
    fin = time.time()
    tiempos["Gauss-Seidel"] = fin - inicio
    resultados["Gauss-Seidel"] = resultado_gs
    
    # 3. SOR
    inicio = time.time()
    resultado_sor = sor(x0, A, b, tol, niter, w, modo)
    fin = time.time()
    tiempos["SOR"] = fin - inicio
    resultados["SOR"] = resultado_sor
    
    # Filtrar métodos exitosos
    metodos_exitosos = {k: v for k, v in tiempos.items() if resultados[k]["exito"]}
    
    if not metodos_exitosos:
        return {
            "exito": False,
            "mensaje": "Ningún método convergió. Verifique la matriz y condiciones iniciales.",
            "resultados": resultados,
            "informe": None,
            "grafico_tiempos": None,
            "grafico_convergencia": None,
            "metodo_mas_rapido": None,
            "metodo_menos_iteraciones": None
        }
    
    # Encontrar el más rápido y el de menos iteraciones
    metodo_mas_rapido = min(metodos_exitosos, key=metodos_exitosos.get)
    tiempo_mas_rapido = metodos_exitosos[metodo_mas_rapido]
    
    iteraciones_dict = {k: resultados[k]["iteraciones"] for k in metodos_exitosos.keys()}
    metodo_menos_iteraciones = min(iteraciones_dict, key=iteraciones_dict.get)
    
    # Generar análisis comparativo
    analisis = _generar_analisis_iterativos(resultados, metodos_exitosos, metodo_mas_rapido, metodo_menos_iteraciones, w)
    
    # Crear gráficos
    try:
        grafico_tiempos = _crear_grafico_tiempos_iterativos(tiempos)
    except Exception as e:
        print(f"Error creando gráfico de tiempos: {e}")
        grafico_tiempos = None
    
    try:
        grafico_convergencia = _crear_grafico_convergencia_iterativos(resultados, metodos_exitosos)
    except Exception as e:
        print(f"Error creando gráfico de convergencia: {e}")
        grafico_convergencia = None
    
    return {
        "exito": True,
        "mensaje": f"Comparación completada. {len(metodos_exitosos)} de 3 métodos convergieron.",
        "resultados": resultados,
        "tiempos": {k: v * 1000 for k, v in tiempos.items()},  # Convertir a milisegundos
        "informe": analisis,
        "grafico_tiempos": grafico_tiempos,
        "grafico_convergencia": grafico_convergencia,
        "metodo_mas_rapido": metodo_mas_rapido,
        "tiempo_mas_rapido": tiempo_mas_rapido,
        "metodo_menos_iteraciones": metodo_menos_iteraciones,
        "mejor_metodo": analisis["mejor_metodo"],
        "total_metodos_exitosos": len(metodos_exitosos)
    }


def _generar_analisis_iterativos(resultados, metodos_exitosos, metodo_mas_rapido, metodo_menos_iteraciones, w):
    """Genera análisis comparativo para métodos iterativos"""
    
    # Crear tabla comparativa
    tabla_comparativa = _crear_tabla_comparativa_iterativos(resultados, metodos_exitosos)
    
    # Determinar el mejor método basado en múltiples criterios
    mejor_metodo = _determinar_mejor_metodo_iterativo(resultados, metodos_exitosos)
    
    analisis = {
        "resumen": f"Se ejecutaron 3 métodos iterativos, de los cuales {len(metodos_exitosos)} convergieron exitosamente.",
        "metodo_mas_rapido": metodo_mas_rapido,
        "metodo_menos_iteraciones": metodo_menos_iteraciones,
        "mejor_metodo": mejor_metodo["nombre"],
        "puntuacion_mejor": mejor_metodo["puntuacion"],
        "tabla_comparativa": tabla_comparativa,
        "recomendacion": "",
        "caracteristicas": {}
    }
    
    # Características de cada método ejecutado
    if "Jacobi" in resultados:
        analisis["caracteristicas"]["Jacobi"] = {
            "ventajas": ["Simple de implementar", "Fácilmente paralelizable", "Estable para matrices diagonalmente dominantes"],
            "desventajas": ["Convergencia más lenta que GS", "Requiere diagonal dominante"],
            "convergencia": "Lineal (si ρ(T) < 1)",
            "mejor_uso": "Matrices grandes y dispersas con diagonal dominante, computación paralela",
            "radio_espectral": round(resultados["Jacobi"]["radio_espectral"], 6) if resultados["Jacobi"]["exito"] else "N/A",
            "converge": "✅ Sí" if resultados["Jacobi"]["converge_teorico"] else "❌ No",
            "estado": "✅ Convergió" if resultados["Jacobi"]["exito"] else "❌ Falló"
        }
    
    if "Gauss-Seidel" in resultados:
        analisis["caracteristicas"]["Gauss-Seidel"] = {
            "ventajas": ["Más rápido que Jacobi (típicamente)", "Menor uso de memoria", "Mejor convergencia", "Usa valores actualizados inmediatamente"],
            "desventajas": ["No paralelizable", "Requiere matriz definida positiva o diagonal dominante"],
            "convergencia": "Lineal (más rápido que Jacobi si ρ(T_GS) < ρ(T_J))",
            "mejor_uso": "Sistemas con matriz simétrica y definida positiva, procesamiento secuencial",
            "radio_espectral": round(resultados["Gauss-Seidel"]["radio_espectral"], 6) if resultados["Gauss-Seidel"]["exito"] else "N/A",
            "converge": "✅ Sí" if resultados["Gauss-Seidel"]["converge_teorico"] else "❌ No",
            "estado": "✅ Convergió" if resultados["Gauss-Seidel"]["exito"] else "❌ Falló"
        }
    
    if "SOR" in resultados:
        analisis["caracteristicas"]["SOR"] = {
            "ventajas": ["Converge más rápido con ω óptimo", "Flexible con parámetro de relajación", "Generaliza Gauss-Seidel"],
            "desventajas": ["Requiere elegir ω adecuado", "Sensible al parámetro ω", "Puede divergir con ω mal elegido"],
            "convergencia": "Lineal (más rápido que GS con ω óptimo, típicamente 1 < ω < 2)",
            "mejor_uso": "Cuando se conoce el ω óptimo o se puede estimar, problemas elípticos",
            "radio_espectral": round(resultados["SOR"]["radio_espectral"], 6) if resultados["SOR"]["exito"] else "N/A",
            "converge": "✅ Sí" if resultados["SOR"]["converge_teorico"] else "❌ No",
            "omega_usado": w,
            "estado": "✅ Convergió" if resultados["SOR"]["exito"] else "❌ Falló"
        }
    
    # Recomendación mejorada
    if not metodos_exitosos:
        analisis["recomendacion"] = "❌ Ningún método convergió. Verifique que la matriz sea diagonalmente dominante o definida positiva."
    elif len(metodos_exitosos) == 1:
        unico_metodo = list(metodos_exitosos.keys())[0]
        analisis["recomendacion"] = f"⚠️ Solo {unico_metodo} convergió. Es la única opción viable para este sistema."
    else:
        # Comparación detallada
        if metodo_mas_rapido == metodo_menos_iteraciones == mejor_metodo["nombre"]:
            analisis["recomendacion"] = (
                f"🏆 **{mejor_metodo['nombre']}** es claramente el MEJOR método para este problema: "
                f"fue el más rápido, requirió menos iteraciones y obtuvo la mejor puntuación general ({mejor_metodo['puntuacion']:.1f}/100). "
                f"Es la opción óptima para sistemas similares."
            )
        else:
            analisis["recomendacion"] = (
                f"📊 **Análisis comparativo:**\n"
                f"- ⏱️ Más rápido: **{metodo_mas_rapido}**\n"
                f"- 🔄 Menos iteraciones: **{metodo_menos_iteraciones}**\n"
                f"- 🏆 Mejor puntuación general: **{mejor_metodo['nombre']}** ({mejor_metodo['puntuacion']:.1f}/100)\n\n"
                f"**Recomendación:** Use **{mejor_metodo['nombre']}** para el mejor balance entre velocidad, "
                f"eficiencia y convergencia en este tipo de sistema."
            )
    
    # Análisis de convergencia teórica
    radios_espectrales = [(k, resultados[k]["radio_espectral"]) for k in metodos_exitosos.keys()]
    radios_espectrales.sort(key=lambda x: x[1])
    
    if radios_espectrales:
        metodo_mejor_radio = radios_espectrales[0][0]
        radio_mejor = radios_espectrales[0][1]
        analisis["nota_convergencia"] = (
            f"📊 **Convergencia teórica:** {metodo_mejor_radio} tiene el menor radio espectral (ρ = {radio_mejor:.6f}), "
            f"lo que garantiza mejor tasa de convergencia asintótica. "
        )
        
        # Comparación de radios espectrales
        if len(radios_espectrales) > 1:
            comparacion_radios = []
            for metodo, radio in radios_espectrales:
                if radio < 1:
                    comparacion_radios.append(f"✅ {metodo}: ρ = {radio:.6f} (converge)")
                else:
                    comparacion_radios.append(f"❌ {metodo}: ρ = {radio:.6f} (no garantiza convergencia)")
            analisis["comparacion_radios"] = comparacion_radios
    
    # Análisis de errores finales
    errores_finales = [(k, resultados[k]["error_final"]) for k in metodos_exitosos.keys()]
    errores_finales.sort(key=lambda x: x[1])
    if errores_finales:
        metodo_menor_error = errores_finales[0][0]
        analisis["nota_error"] = (
            f"🎯 {metodo_menor_error} alcanzó el menor error final: {errores_finales[0][1]:.2e}"
        )
    
    return analisis


def _crear_tabla_comparativa_iterativos(resultados, metodos_exitosos):
    """Crea una tabla HTML comparativa de todos los métodos"""
    tabla_data = []
    
    for metodo in ["Jacobi", "Gauss-Seidel", "SOR"]:
        if metodo in resultados:
            r = resultados[metodo]
            fila = {
                "Método": metodo,
                "Estado": "✅ Convergió" if r["exito"] else "❌ Falló",
                "Iteraciones": r["iteraciones"] if r["exito"] else "-",
                "Error Final": f"{r['error_final']:.2e}" if r["exito"] and r["error_final"] else "-",
                "Radio Espectral": f"{r['radio_espectral']:.6f}" if r["radio_espectral"] is not None else "-",
                "Converge Teórico": "✅ Sí (ρ<1)" if r["converge_teorico"] else "❌ No (ρ≥1)"
            }
            tabla_data.append(fila)
    
    df = pd.DataFrame(tabla_data)
    tabla_html = df.to_html(index=False, classes='table table-striped table-bordered text-center', escape=False)
    
    return tabla_html


def _determinar_mejor_metodo_iterativo(resultados, metodos_exitosos):
    """
    Determina el mejor método basado en múltiples criterios:
    - Velocidad de convergencia (radio espectral)
    - Número de iteraciones
    - Error final
    - Convergencia teórica
    """
    if not metodos_exitosos:
        return {"nombre": "Ninguno", "puntuacion": 0}
    
    puntuaciones = {}
    
    for metodo in metodos_exitosos.keys():
        r = resultados[metodo]
        puntuacion = 0
        
        # Criterio 1: Radio espectral (30 puntos) - menor es mejor
        radios = [resultados[m]["radio_espectral"] for m in metodos_exitosos.keys()]
        radio_min = min(radios)
        if r["radio_espectral"] == radio_min:
            puntuacion += 30
        elif r["radio_espectral"] < 1:
            # Proporcional: más cercano al mínimo = más puntos
            puntuacion += 30 * (1 - (r["radio_espectral"] - radio_min) / (1 - radio_min)) if radio_min < 1 else 15
        
        # Criterio 2: Número de iteraciones (25 puntos) - menor es mejor
        iteraciones = [resultados[m]["iteraciones"] for m in metodos_exitosos.keys()]
        iter_min = min(iteraciones)
        iter_max = max(iteraciones)
        if r["iteraciones"] == iter_min:
            puntuacion += 25
        elif iter_max > iter_min:
            puntuacion += 25 * (1 - (r["iteraciones"] - iter_min) / (iter_max - iter_min))
        
        # Criterio 3: Error final (25 puntos) - menor es mejor
        errores = [resultados[m]["error_final"] for m in metodos_exitosos.keys()]
        error_min = min(errores)
        error_max = max(errores)
        if r["error_final"] == error_min:
            puntuacion += 25
        elif error_max > error_min and error_max != 0:
            puntuacion += 25 * (1 - (r["error_final"] - error_min) / (error_max - error_min))
        
        # Criterio 4: Convergencia teórica (20 puntos)
        if r["converge_teorico"]:
            puntuacion += 20
        
        puntuaciones[metodo] = puntuacion
    
    # Encontrar el método con mayor puntuación
    mejor = max(puntuaciones, key=puntuaciones.get)
    
    return {
        "nombre": mejor,
        "puntuacion": puntuaciones[mejor]
    }


def _crear_grafico_tiempos_iterativos(tiempos_dict: Dict[str, float]) -> str:
    """Crea gráfico de barras para tiempos de ejecución"""
    plt.figure(figsize=(10, 6))
    
    metodos = list(tiempos_dict.keys())
    tiempos = [t * 1000 for t in tiempos_dict.values()]  # Convertir a ms
    
    colores = ['#007bff', '#28a745', '#ffc107']
    
    barras = plt.bar(metodos, tiempos, color=colores[:len(metodos)], alpha=0.7, edgecolor='black')
    
    # Agregar valores sobre las barras
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura,
                f'{altura:.3f} ms',
                ha='center', va='bottom', fontweight='bold')
    
    plt.title('Comparación de Tiempos de Ejecución - Métodos Iterativos', fontsize=14, fontweight='bold')
    plt.xlabel('Método', fontsize=12)
    plt.ylabel('Tiempo (milisegundos)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    img_uri = f"data:image/png;base64,{string}"
    
    plt.close()
    
    return img_uri


def _crear_grafico_convergencia_iterativos(resultados, metodos_exitosos) -> str:
    """Crea gráfico de líneas para evolución del error"""
    plt.figure(figsize=(12, 6))
    
    colores = {'Jacobi': '#007bff', 'Gauss-Seidel': '#28a745', 'SOR': '#ffc107'}
    
    for metodo in metodos_exitosos.keys():
        errores = resultados[metodo]["errores"]
        iteraciones = list(range(1, len(errores) + 1))
        plt.semilogy(iteraciones, errores, marker='o', label=metodo, 
                    color=colores.get(metodo, '#000000'), linewidth=2, markersize=4)
    
    plt.title('Evolución del Error vs Iteraciones', fontsize=14, fontweight='bold')
    plt.xlabel('Iteración', fontsize=12)
    plt.ylabel('Error (escala logarítmica)', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3, which='both', linestyle='--')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    img_uri = f"data:image/png;base64,{string}"
    
    plt.close()
    
    return img_uri