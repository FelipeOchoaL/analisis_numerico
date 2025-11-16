import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def newton_raphson_method():
    """
    Implementación del Método de Newton-Raphson
    
    El método de Newton-Raphson es un algoritmo iterativo para encontrar raíces de funciones.
    Fórmula: x_{i+1} = x_i - f(x_i)/f'(x_i)
    
    El procedimiento es:
    PASO 0: Calcular f'(x)
    PASO 1: Evaluar f(xi) y f'(xi)
    PASO 2: Calcular la raíz aproximada x_{i+1} = x_i - f(x_i)/f'(x_i)
    PASO 3: Calcular el error: E = |x_{i+1} - x_i| / |x_{i+1}|
    """
    
    print("=== MÉTODO DE NEWTON-RAPHSON ===")
    print("Formato de funciones: use 'x' como variable (ej: x**3 - 2*x - 5)")
    print("Funciones disponibles: sin, cos, tan, exp, log, sqrt, etc.")
    print("-" * 50)
    
    # Entradas del usuario
    try:
        print("Valor inicial x0:")
        x0 = float(input())
        print("Función f(x):")
        fx_str = input()
        print("Derivada f'(x):")
        dfx_str = input()
        print("Tolerancia:")
        tol = float(input())
        print("Número máximo de iteraciones:")
        niter = int(input())
        print("¿Incluir columna de error? (s/n):")
        incluir_error = input().lower().startswith('s')
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
        return
    
    # Preprocesar funciones para notaciones matemáticas comunes
    def preprocess_function(func_str):
        func_str = func_str.replace('ln(', 'log(')
        func_str = func_str.replace('sin(', 'math.sin(')
        func_str = func_str.replace('cos(', 'math.cos(')
        func_str = func_str.replace('tan(', 'math.tan(')
        func_str = func_str.replace('exp(', 'math.exp(')
        func_str = func_str.replace('log(', 'math.log(')
        func_str = func_str.replace('sqrt(', 'math.sqrt(')
        func_str = func_str.replace('^', '**')
        return func_str
    
    # Funciones lambda para evaluación segura
    try:
        fx_processed = preprocess_function(fx_str)
        dfx_processed = preprocess_function(dfx_str)
        
        f = lambda x: eval(fx_processed, {"__builtins__": {}}, 
                          {"x": x, "math": math, "sin": math.sin, "cos": math.cos, 
                           "tan": math.tan, "exp": math.exp, "log": math.log, 
                           "sqrt": math.sqrt, "pi": math.pi, "e": math.e})
        
        df = lambda x: eval(dfx_processed, {"__builtins__": {}}, 
                           {"x": x, "math": math, "sin": math.sin, "cos": math.cos, 
                            "tan": math.tan, "exp": math.exp, "log": math.log, 
                            "sqrt": math.sqrt, "pi": math.pi, "e": math.e})
    except Exception as e:
        print(f"Error en la función: {e}")
        return
    
    # Verificar que la derivada no sea cero en x0
    try:
        df_x0 = df(x0)
        if abs(df_x0) < 1e-12:
            print(f"Error: f'({x0}) ≈ 0. El método no converge con este valor inicial.")
            return
    except Exception as e:
        print(f"Error evaluando la derivada en x0: {e}")
        return
    
    # Variables para el algoritmo
    xi = x0
    iteraciones = []
    
    # PASO 0: Mostrar las funciones
    print(f"\nFunción f(x) = {fx_str}")
    print(f"Derivada f'(x) = {dfx_str}")
    print(f"Valor inicial x0 = {x0}")
    print(f"Tolerancia = {tol}")
    print("-" * 50)
    
    # Inicializar tabla de resultados
    columnas = ["i", "xi", "f(xi)", "f'(xi)"]
    if incluir_error:
        columnas.append("E")
    
    for i in range(niter + 1):
        try:
            # PASO 1: Evaluar f(xi) y f'(xi)
            fxi = f(xi)
            dfxi = df(xi)
            
            # Verificar si f'(xi) es muy pequeño
            if abs(dfxi) < 1e-12:
                print(f"Error: f'({xi}) ≈ 0 en la iteración {i}. El método no puede continuar.")
                break
            
            # Crear fila de datos
            fila = [i, xi, fxi, dfxi]
            
            # Verificar convergencia
            if abs(fxi) <= tol:
                if incluir_error and i > 0:
                    error = abs(xi - xi_anterior) / abs(xi) if abs(xi) > 1e-12 else abs(xi - xi_anterior)
                    fila.append(error)
                iteraciones.append(fila)
                print(f"¡Convergencia alcanzada en iteración {i}!")
                print(f"Raíz encontrada: x = {xi:.10f}")
                print(f"f({xi:.10f}) = {fxi:.2e}")
                break
            
            # PASO 2: Calcular la siguiente aproximación
            xi_nuevo = xi - fxi / dfxi
            
            # PASO 3: Calcular error si no es la primera iteración
            if i > 0 and incluir_error:
                error = abs(xi - xi_anterior) / abs(xi) if abs(xi) > 1e-12 else abs(xi - xi_anterior)
                fila.append(error)
                
                # Verificar convergencia por error
                if error <= tol:
                    iteraciones.append(fila)
                    print(f"¡Convergencia por error alcanzada en iteración {i}!")
                    print(f"Raíz encontrada: x = {xi:.10f}")
                    print(f"Error relativo = {error:.2e}")
                    break
            elif i == 0 and incluir_error:
                fila.append("-")  # No hay error en la primera iteración
            
            iteraciones.append(fila)
            
            # Preparar para siguiente iteración
            xi_anterior = xi
            xi = xi_nuevo
            
        except Exception as e:
            print(f"Error en iteración {i}: {e}")
            break
    else:
        print(f"Método alcanzó el límite de {niter} iteraciones sin convergencia.")
        print(f"Última aproximación: x = {xi:.10f}")
        print(f"f({xi:.10f}) = {f(xi):.2e}")
    
    # Crear y mostrar tabla de resultados
    df_resultados = pd.DataFrame(iteraciones, columns=columnas)
    
    print("\n=== TABLA DE RESULTADOS ===")
    print(df_resultados.to_string(index=False, float_format=lambda x: f"{x:.6f}" if isinstance(x, (int, float)) and x != "-" else str(x)))
    
    # Guardar resultados en archivo CSV
    try:
        df_resultados.to_csv('newton_raphson_resultados.csv', index=False)
        print(f"\nResultados guardados en 'newton_raphson_resultados.csv'")
    except Exception as e:
        print(f"Error guardando archivo: {e}")
    
    # Opcional: Gráfica del método
    try:
        respuesta = input("\n¿Desea ver la gráfica del método? (s/n): ")
        if respuesta.lower().startswith('s'):
            plot_newton_raphson(f, df, x0, iteraciones, fx_str)
    except:
        pass

def plot_newton_raphson(f, df, x0, iteraciones, fx_str):
    """Grafica el método de Newton-Raphson"""
    try:
        plt.figure(figsize=(12, 8))
        
        # Obtener los valores de x de las iteraciones
        x_vals = [iter_data[1] for iter_data in iteraciones]
        
        # Rango para la gráfica
        x_min = min(x_vals + [x0]) - 1
        x_max = max(x_vals + [x0]) + 1
        x_range = np.linspace(x_min, x_max, 1000)
        
        # Evaluar función en el rango
        try:
            y_range = [f(x) for x in x_range]
        except:
            print("Error graficando la función")
            return
        
        # Gráfica de la función
        plt.subplot(2, 1, 1)
        plt.plot(x_range, y_range, 'b-', label=f'f(x) = {fx_str}', linewidth=2)
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        plt.grid(True, alpha=0.3)
        
        # Marcar las iteraciones
        for i, (iter_num, xi, fxi, dfxi, *error) in enumerate(iteraciones[:5]):  # Solo primeras 5 iteraciones
            plt.plot(xi, fxi, 'ro', markersize=8)
            plt.annotate(f'x{iter_num}', (xi, fxi), xytext=(5, 5), 
                        textcoords='offset points', fontsize=10)
            
            # Dibujar tangente
            if i < len(iteraciones) - 1 and abs(dfxi) > 1e-12:
                x_tang = np.array([xi - 0.5, xi + 0.5])
                y_tang = fxi + dfxi * (x_tang - xi)
                plt.plot(x_tang, y_tang, 'r--', alpha=0.7, linewidth=1)
        
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Método de Newton-Raphson')
        plt.legend()
        
        # Gráfica de convergencia
        plt.subplot(2, 1, 2)
        if len(iteraciones) > 1:
            iter_nums = [iter_data[0] for iter_data in iteraciones]
            x_values = [iter_data[1] for iter_data in iteraciones]
            plt.plot(iter_nums, x_values, 'go-', linewidth=2, markersize=6)
            plt.xlabel('Iteración')
            plt.ylabel('xi')
            plt.title('Convergencia de las aproximaciones')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error generando gráfica: {e}")

if __name__ == "__main__":
    newton_raphson_method()
