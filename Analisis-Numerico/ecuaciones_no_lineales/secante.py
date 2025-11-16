import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def secante_method():
    """
    Implementación del Método de la Secante
    
    El método de la secante es un algoritmo iterativo para encontrar raíces de funciones.
    Fórmula: x_{i+1} = x_i - f(x_i) * (x_i - x_{i-1}) / (f(x_i) - f(x_{i-1}))
    
    El procedimiento es:
    PASO 0: Establecer dos condiciones iniciales X0 y X1
    PASO 1: Evaluar f(x_{i-1}) y f(x_i)
    PASO 2: Calcular la raíz aproximada x_{i+1} = x_i - f(x_i) * (x_i - x_{i-1}) / (f(x_i) - f(x_{i-1}))
    PASO 3: Calcular el error: E = |x_{i+1} - x_i| / |x_{i+1}|
    """
    
    print("=== MÉTODO DE LA SECANTE ===")
    print("Formato de funciones: use 'x' como variable (ej: x**3 - 2*x - 5)")
    print("Funciones disponibles: sin, cos, tan, exp, log, sqrt, etc.")
    print("-" * 50)
    
    # Entradas del usuario
    try:
        print("Primer valor inicial x0:")
        x0 = float(input())
        print("Segundo valor inicial x1:")
        x1 = float(input())
        print("Función f(x):")
        fx_str = input()
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
    
    # Función lambda para evaluación segura
    try:
        fx_processed = preprocess_function(fx_str)
        
        f = lambda x: eval(fx_processed, {"__builtins__": {}}, 
                          {"x": x, "math": math, "sin": math.sin, "cos": math.cos, 
                           "tan": math.tan, "exp": math.exp, "log": math.log, 
                           "sqrt": math.sqrt, "pi": math.pi, "e": math.e})
        
    except Exception as e:
        print(f"Error en la función: {e}")
        return
    
    # Verificar que los valores iniciales sean diferentes
    if abs(x1 - x0) < 1e-12:
        print("Error: Los valores iniciales x0 y x1 deben ser diferentes.")
        return
    
    # Variables para el algoritmo
    xi_anterior = x0  # x_{i-1}
    xi = x1           # x_i
    iteraciones = []
    
    # PASO 0: Mostrar la función y valores iniciales
    print(f"\nFunción f(x) = {fx_str}")
    print(f"Valores iniciales: x0 = {x0}, x1 = {x1}")
    print(f"Tolerancia = {tol}")
    print("-" * 50)
    
    # Inicializar tabla de resultados
    columnas = ["i", "xi-1", "xi", "f(xi-1)", "f(xi)"]
    if incluir_error:
        columnas.append("E")
    
    # Evaluaciones iniciales
    try:
        fxi_anterior = f(xi_anterior)
        fxi = f(xi)
    except Exception as e:
        print(f"Error evaluando función en valores iniciales: {e}")
        return
    
    for i in range(niter + 1):
        try:
            # PASO 1: Ya tenemos f(x_{i-1}) y f(x_i)
            
            # Crear fila de datos
            fila = [i, xi_anterior, xi, fxi_anterior, fxi]
            
            # Verificar convergencia por función
            if abs(fxi) <= tol:
                if incluir_error and i > 0:
                    error = abs(xi - xi_anterior) / abs(xi) if abs(xi) > 1e-12 else abs(xi - xi_anterior)
                    fila.append(error)
                iteraciones.append(fila)
                print(f"¡Convergencia alcanzada en iteración {i}!")
                print(f"Raíz encontrada: x = {xi:.10f}")
                print(f"f({xi:.10f}) = {fxi:.2e}")
                break
            
            # Verificar si f(xi) - f(xi-1) es muy pequeño (evitar división por cero)
            denominador = fxi - fxi_anterior
            if abs(denominador) < 1e-12:
                print(f"Error: f(xi) - f(xi-1) ≈ 0 en la iteración {i}. El método no puede continuar.")
                if incluir_error:
                    fila.append("-")
                iteraciones.append(fila)
                break
            
            # PASO 2: Calcular la siguiente aproximación
            xi_nuevo = xi - fxi * (xi - xi_anterior) / denominador
            
            # PASO 3: Calcular error si incluir_error está habilitado
            if incluir_error:
                if i > 0:
                    error = abs(xi - xi_anterior) / abs(xi) if abs(xi) > 1e-12 else abs(xi - xi_anterior)
                    fila.append(error)
                    
                    # Verificar convergencia por error
                    if error <= tol:
                        iteraciones.append(fila)
                        print(f"¡Convergencia por error alcanzada en iteración {i}!")
                        print(f"Raíz encontrada: x = {xi:.10f}")
                        print(f"Error relativo = {error:.2e}")
                        break
                else:
                    fila.append("-")  # No hay error en la primera iteración
            
            iteraciones.append(fila)
            
            # Preparar para siguiente iteración
            xi_anterior = xi
            xi = xi_nuevo
            fxi_anterior = fxi
            fxi = f(xi)
            
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
        df_resultados.to_csv('secante_resultados.csv', index=False)
        print(f"\nResultados guardados en 'secante_resultados.csv'")
    except Exception as e:
        print(f"Error guardando archivo: {e}")
    
    # Opcional: Gráfica del método
    try:
        respuesta = input("\n¿Desea ver la gráfica del método? (s/n): ")
        if respuesta.lower().startswith('s'):
            plot_secante(f, x0, x1, iteraciones, fx_str)
    except:
        pass

def plot_secante(f, x0, x1, iteraciones, fx_str):
    """Grafica el método de la secante"""
    try:
        plt.figure(figsize=(12, 8))
        
        # Obtener los valores de x de las iteraciones
        x_vals = [x0, x1] + [iter_data[2] for iter_data in iteraciones]  # xi values
        
        # Rango para la gráfica
        x_min = min(x_vals) - 1
        x_max = max(x_vals) + 1
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
        colors = ['red', 'orange', 'green', 'purple', 'brown']
        for i, (iter_num, xi_anterior, xi, fxi_anterior, fxi, *error) in enumerate(iteraciones[:5]):  # Solo primeras 5 iteraciones
            color = colors[i % len(colors)]
            
            # Marcar los puntos
            plt.plot(xi_anterior, fxi_anterior, 'o', color=color, markersize=8)
            plt.plot(xi, fxi, 'o', color=color, markersize=8)
            
            plt.annotate(f'x{iter_num-1}' if iter_num > 0 else 'x0', (xi_anterior, fxi_anterior), 
                        xytext=(5, 5), textcoords='offset points', fontsize=10)
            plt.annotate(f'x{iter_num}', (xi, fxi), xytext=(5, 5), 
                        textcoords='offset points', fontsize=10)
            
            # Dibujar secante
            if abs(fxi - fxi_anterior) > 1e-12:
                x_sec = np.array([xi_anterior, xi])
                y_sec = np.array([fxi_anterior, fxi])
                plt.plot(x_sec, y_sec, '--', color=color, alpha=0.7, linewidth=2, 
                        label=f'Secante iter {iter_num}')
        
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Método de la Secante')
        plt.legend()
        
        # Gráfica de convergencia
        plt.subplot(2, 1, 2)
        if len(iteraciones) > 1:
            iter_nums = [iter_data[0] for iter_data in iteraciones]
            x_values = [iter_data[2] for iter_data in iteraciones]  # xi values
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
    secante_method()

