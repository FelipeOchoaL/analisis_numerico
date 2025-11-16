import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def fixed_point_method():
    """
    Implementación del Método de Punto Fijo según el Teorema de Punto Fijo
    
    Teorema: Si g es una función continua en [a,b] y g(x) ∈ [a,b] para todo x ∈ [a,b],
    y si |g'(x)| ≤ k < 1 para todo x ∈ (a,b), entonces g tiene un único punto fijo p en [a,b].
    """
    
    print("=== MÉTODO DE PUNTO FIJO ===")
    print("Formato de funciones: use 'x' como variable (ej: x**2 + 2*x - 1)")
    print("Funciones disponibles: sin, cos, tan, exp, log, sqrt, etc.")
    print("-" * 50)
    
    # Entradas del usuario
    try:
        print("Valor inicial X0:")
        X0 = float(input())
        print("Tolerancia:")
        tol = float(input())
        print("Número máximo de iteraciones:")
        niter = int(input())
        print("Función f(x) original:")
        fun_str = input()
        print("Función de iteración g(x):")
        g_str = input()
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
        return
    
    # Preprocesar funciones para notaciones matemáticas comunes
    def preprocess_function(func_str):
        # Reemplazar notaciones matemáticas comunes
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
        fun_processed = preprocess_function(fun_str)
        g_processed = preprocess_function(g_str)
        
        f = lambda x: eval(fun_processed)
        g = lambda x: eval(g_processed)
        
        # Verificar que las funciones son válidas
        test_val = f(X0)
        test_val = g(X0)
        
        print(f"Función f(x) procesada: {fun_processed}")
        print(f"Función g(x) procesada: {g_processed}")
        
    except Exception as e:
        print(f"Error: Funciones inválidas. {e}")
        print("Verifique la sintaxis. Ejemplos válidos:")
        print("- x**2 + 2*x - 1")
        print("- ln(x) + x - 2")
        print("- sin(x) - x/2")
        return
    
    # Inicialización de variables
    iterations = []
    x_values = []
    f_values = []
    errors = []
    
    x_current = X0
    error = float('inf')
    i = 0
    
    # Valores iniciales
    f_current = f(x_current)
    iterations.append(i)
    x_values.append(x_current)
    f_values.append(f_current)
    errors.append("-")
    
    print(f"\n=== ITERACIONES ===")
    print(f"{'i':>3} | {'Xi':>12} | {'f(Xi)':>12} | {'Error':>12}")
    print("-" * 50)
    print(f"{i:>3} | {x_current:>12.6f} | {f_current:>12.6f} | {'-':>12}")
    
    # Algoritmo de Punto Fijo: xn = g(xn-1)
    while error > tol and abs(f_current) > tol and i < niter:
        x_previous = x_current
        x_current = g(x_previous)  # xn = g(xn-1)
        f_current = f(x_current)
        i += 1
        
        # Cálculo del error: E = |xn - xn-1|
        error = abs(x_current - x_previous)
        
        # Almacenar valores
        iterations.append(i)
        x_values.append(x_current)
        f_values.append(f_current)
        errors.append(error)
        
        # Mostrar iteración actual
        print(f"{i:>3} | {x_current:>12.6f} | {f_current:>12.6f} | {error:>12.6e}")
    
    # Crear DataFrame para mejor visualización
    df = pd.DataFrame({
        'Iteración': iterations,
        'Xi': x_values,
        'f(Xi)': f_values,
        'Error': errors
    })
    
    print(f"\n=== RESULTADOS ===")
    print(df.to_string(index=False, float_format=lambda x: f'{x:.6f}' if isinstance(x, (int, float)) else str(x)))
    
    # Análisis de convergencia
    if abs(f_current) <= tol:
        print(f"\n✓ Raíz encontrada: x = {x_current:.6f}")
        print(f"✓ f({x_current:.6f}) = {f_current:.6f}")
    elif error <= tol:
        print(f"\n✓ Punto fijo encontrado: x = {x_current:.6f}")
        print(f"✓ Error = {error:.6e} < Tolerancia = {tol}")
        print(f"✓ g({x_current:.6f}) ≈ {x_current:.6f}")
    else:
        print(f"\n✗ Método falló después de {niter} iteraciones")
        print(f"✗ Error final = {error:.6e}")
        print(f"✗ Puede no cumplir condiciones de convergencia |g'(x)| < 1")
    
    # Visualización gráfica
    plot_fixed_point(x_values, g, f, X0, x_current if error <= tol else None)
    
    return x_current, error, i

def plot_fixed_point(x_values, g, f, x0, solution=None):
    """
    Visualiza el método de punto fijo gráficamente estilo GeoGebra
    """
    try:
        # Configurar el estilo similar a GeoGebra
        plt.style.use('default')
        
        # Determinar rango apropiado basado en las funciones y los valores
        if solution is not None:
            center = solution
        else:
            center = x_values[-1] if x_values else x0
            
        # Rango más amplio similar a GeoGebra 
        x_min = max(0.1, center - 30)  # Evitar x <= 0 para ln(x)
        x_max = center + 50
        
        # Para funciones logarítmicas, ajustar el rango
        if 'ln' in str(g) or 'log' in str(g):
            x_min = max(0.1, min(x_values) - 5)
            x_max = max(max(x_values) + 20, 80)
        
        x_range = np.linspace(x_min, x_max, 2000)
        
        # Evaluar funciones de manera segura
        g_values = []
        f_values = []
        
        for x in x_range:
            try:
                g_val = g(x)
                f_val = f(x)
                if not (np.isnan(g_val) or np.isinf(g_val)):
                    g_values.append(g_val)
                else:
                    g_values.append(None)
                    
                if not (np.isnan(f_val) or np.isinf(f_val)):
                    f_values.append(f_val)
                else:
                    f_values.append(None)
            except:
                g_values.append(None)
                f_values.append(None)
        
        # Crear figura estilo GeoGebra
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        fig.patch.set_facecolor('white')
        
        # Gráfica 1: Método de punto fijo (estilo GeoGebra)
        ax1.set_facecolor('#f8f8f8')
        
        # Dibujar funciones con colores similares a GeoGebra
        ax1.plot(x_range, g_values, color='#1f77b4', linewidth=2.5, label='g(x) = 7ln(x) + 12')
        ax1.plot(x_range, x_range, color='#d62728', linewidth=2, linestyle='--', label='y = x')
        
        # Mostrar el proceso iterativo con líneas más visibles
        if len(x_values) > 1:
            for i in range(min(len(x_values) - 1, 8)):  # Mostrar máximo 8 iteraciones
                x_curr = x_values[i]
                x_next = x_values[i + 1]
                
                # Líneas del método gráfico con colores distintos
                ax1.plot([x_curr, x_curr], [x_curr, x_next], 'green', alpha=0.8, linewidth=1.5)
                ax1.plot([x_curr, x_next], [x_next, x_next], 'green', alpha=0.8, linewidth=1.5)
                
                # Marcar los puntos de iteración
                ax1.plot(x_curr, x_curr, 'o', color='orange', markersize=4, alpha=0.7)
        
        # Puntos importantes con estilo GeoGebra
        ax1.plot(x0, g(x0), 'o', color='#2ca02c', markersize=10, label=f'Inicio: x₀ = {x0:.2f}')
        if solution is not None:
            ax1.plot(solution, solution, 'o', color='red', markersize=12, 
                    label=f'Punto fijo: x ≈ {solution:.3f}')
            # Líneas de referencia
            ax1.axhline(y=solution, color='red', linestyle=':', alpha=0.5)
            ax1.axvline(x=solution, color='red', linestyle=':', alpha=0.5)
        
        # Configuración de ejes estilo GeoGebra
        ax1.set_xlabel('x', fontsize=12)
        ax1.set_ylabel('y', fontsize=12)
        ax1.set_title('Método de Punto Fijo: g(x) vs y = x', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.4, linewidth=0.8)
        ax1.legend(fontsize=10, loc='best')
        ax1.set_xlim(x_min, min(x_max, 80))
        
        # Ajustar límites y para una mejor visualización
        if solution is not None:
            y_center = solution
            y_range = max(40, abs(solution) * 0.5)
            ax1.set_ylim(max(0, y_center - y_range), y_center + y_range)
        
        # Gráfica 2: Función original f(x) estilo GeoGebra
        ax2.set_facecolor('#f8f8f8')
        
        # Función f(x) con color distintivo
        ax2.plot(x_range, f_values, color='#ff7f0e', linewidth=2.5, label='f(x) = -7ln(x) + x - 12')
        ax2.axhline(y=0, color='black', linewidth=1.5, alpha=0.8, label='y = 0')
        
        # Mostrar evolución de las iteraciones
        f_iter_values = []
        for x in x_values:
            try:
                f_iter_values.append(f(x))
            except:
                f_iter_values.append(None)
        
        ax2.plot(x_values, f_iter_values, 'o-', color='#2ca02c', markersize=5, 
                linewidth=1.5, alpha=0.8, label='Iteraciones')
        
        # Marcar la raíz si existe
        if solution is not None:
            try:
                f_solution = f(solution)
                ax2.plot(solution, f_solution, 'o', color='red', markersize=12, 
                        label=f'Raíz: f({solution:.3f}) ≈ {f_solution:.2e}')
                ax2.axvline(x=solution, color='red', linestyle=':', alpha=0.5)
            except:
                pass
        
        # Configuración de ejes estilo GeoGebra
        ax2.set_xlabel('x', fontsize=12)
        ax2.set_ylabel('f(x)', fontsize=12)
        ax2.set_title('Función Original f(x)', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.4, linewidth=0.8)
        ax2.legend(fontsize=10, loc='best')
        ax2.set_xlim(x_min, min(x_max, 80))
        
        plt.tight_layout()
        plt.show()
        
        print("✓ Gráficas generadas con estilo similar a GeoGebra")
        
    except Exception as e:
        print(f"Error al generar gráfica: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fixed_point_method() 


