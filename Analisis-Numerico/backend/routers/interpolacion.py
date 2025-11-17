from fastapi import APIRouter, HTTPException
from models.schemas import VandermondeRequest, NewtonRequest, LagrangeRequest, SplineRequest, ComparacionRequest, InterpolacionResponse, SplineResponse, ComparacionResponse
from services.interpolacion_service import InterpolacionService
import time

router = APIRouter()
service = InterpolacionService()

@router.post("/vandermonde", response_model=InterpolacionResponse)
async def interpolar_vandermonde(request: VandermondeRequest):
    """
    Interpolación polinomial usando el método de Vandermonde.
    
    El método de Vandermonde construye una matriz especial para resolver
    el sistema de ecuaciones lineales que determina los coeficientes del
    polinomio interpolante.
    
    **Parámetros:**
    - **x**: Lista de valores x (hasta 8 puntos). Los valores deben ser únicos.
    - **y**: Lista de valores y correspondientes (mismo tamaño que x).
    - **grado**: Grado del polinomio interpolante (debe ser al menos len(x) - 1).
    
    **Retorna:**
    - Polinomio interpolante en formato legible
    - Gráfico con los puntos y el polinomio
    - Coeficientes del polinomio
    
    **Notas:**
    - Los valores de x deben ser distintos entre sí
    - Se necesitan al menos (grado + 1) puntos para un polinomio de grado n
    - El método puede ser inestable numéricamente para grados altos o valores muy separados
    """
    try:
        # Validación básica
        if len(request.x) > 8:
            raise HTTPException(
                status_code=400,
                detail="Se permiten máximo 8 puntos para interpolación"
            )
        
        if len(request.x) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 2 puntos para interpolación"
            )
        
        if request.grado < 0:
            raise HTTPException(
                status_code=400,
                detail="El grado del polinomio debe ser un número positivo"
            )
        
        # Ejecutar el método de Vandermonde
        start_time = time.time()
        resultado = service.vandermonde(
            x=request.x,
            y=request.y,
            grado=request.grado
        )
        end_time = time.time()
        
        # Agregar tiempo de ejecución al mensaje si fue exitoso
        if resultado["exito"]:
            tiempo = end_time - start_time
            resultado["mensaje"] += f" (Tiempo de ejecución: {tiempo:.6f} segundos)"
        
        return resultado
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/newton", response_model=InterpolacionResponse)
async def interpolar_newton(request: NewtonRequest):
    """
    Interpolación polinomial usando el método de Newton (Diferencias Divididas).
    
    El método de Newton utiliza diferencias divididas para construir el polinomio
    interpolante de manera eficiente. Es más estable numéricamente que Vandermonde
    y permite agregar nuevos puntos de manera incremental.
    
    **Parámetros:**
    - **x**: Lista de valores x (hasta 8 puntos). Los valores deben ser únicos.
    - **y**: Lista de valores y correspondientes (mismo tamaño que x).
    
    **Retorna:**
    - Polinomio interpolante en formato legible
    - Gráfico con los puntos y el polinomio
    - Coeficientes del polinomio
    - Tabla de diferencias divididas
    
    **Ventajas:**
    - Más estable numéricamente que Vandermonde
    - Permite agregar puntos nuevos sin recalcular todo
    - No requiere especificar el grado (usa todos los puntos)
    
    **Notas:**
    - Los valores de x deben ser distintos entre sí
    - El grado del polinomio será len(x) - 1
    - El polinomio pasa exactamente por todos los puntos dados
    """
    try:
        # Validación básica
        if len(request.x) > 8:
            raise HTTPException(
                status_code=400,
                detail="Se permiten máximo 8 puntos para interpolación"
            )
        
        if len(request.x) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 2 puntos para interpolación"
            )
        
        # Ejecutar el método de Newton
        start_time = time.time()
        resultado = service.newton_interpolante(
            x=request.x,
            y=request.y
        )
        end_time = time.time()
        
        # Agregar tiempo de ejecución al mensaje si fue exitoso
        if resultado["exito"]:
            tiempo = end_time - start_time
            resultado["mensaje"] += f" (Tiempo de ejecución: {tiempo:.6f} segundos)"
        
        return resultado
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/lagrange", response_model=InterpolacionResponse)
async def interpolar_lagrange(request: LagrangeRequest):
    """
    Interpolación polinomial usando el método de Lagrange.
    
    El método de Lagrange construye el polinomio interpolante como una combinación
    lineal de polinomios base de Lagrange. Es conceptualmente más simple que otros
    métodos y tiene propiedades matemáticas elegantes.
    
    **Parámetros:**
    - **x**: Lista de valores x (hasta 8 puntos). Los valores deben ser únicos.
    - **y**: Lista de valores y correspondientes (mismo tamaño que x).
    
    **Retorna:**
    - Polinomio interpolante en formato legible
    - Gráfico con los puntos y el polinomio
    - Coeficientes del polinomio
    
    **Ventajas:**
    - Conceptualmente simple y elegante
    - Fácil de entender y programar
    - No requiere especificar el grado (usa todos los puntos)
    - Buena estabilidad numérica
    
    **Notas:**
    - Los valores de x deben ser distintos entre sí
    - El grado del polinomio será len(x) - 1
    - El polinomio pasa exactamente por todos los puntos dados
    """
    try:
        # Validación básica
        if len(request.x) > 8:
            raise HTTPException(
                status_code=400,
                detail="Se permiten máximo 8 puntos para interpolación"
            )
        
        if len(request.x) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 2 puntos para interpolación"
            )
        
        # Ejecutar el método de Lagrange
        start_time = time.time()
        resultado = service.lagrange(
            x=request.x,
            y=request.y
        )
        end_time = time.time()
        
        # Agregar tiempo de ejecución al mensaje si fue exitoso
        if resultado["exito"]:
            tiempo = end_time - start_time
            resultado["mensaje"] += f" (Tiempo de ejecución: {tiempo:.6f} segundos)"
        
        return resultado
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/info")
async def obtener_info():
    """
    Proporciona información sobre los métodos de interpolación disponibles.
    
    Retorna información útil sobre:
    - Métodos implementados
    - Límites y restricciones
    - Ejemplos de uso
    """
    return {
        "metodos_disponibles": {
            "vandermonde": {
                "nombre": "Método de Vandermonde",
                "descripcion": "Utiliza una matriz de Vandermonde para encontrar el polinomio interpolante",
                "ventajas": [
                    "Implementación directa y conceptualmente simple",
                    "Resuelve directamente el sistema de ecuaciones lineales"
                ],
                "desventajas": [
                    "Puede ser numéricamente inestable para grados altos",
                    "Requiere resolver un sistema de ecuaciones lineales completo"
                ],
                "complejidad": "O(n³) por la resolución del sistema lineal"
            }
        },
        "restricciones": {
            "max_puntos": 8,
            "min_puntos": 2,
            "valores_x_unicos": True,
            "mismo_tamano_xy": True
        },
        "recomendaciones": {
            "grado_optimo": "Usar grado = len(x) - 1 para que el polinomio pase exactamente por todos los puntos",
            "puntos_equidistantes": "Para mejor estabilidad numérica, usar puntos relativamente equidistantes",
            "grado_bajo": "Evitar grados muy altos (> 10) para prevenir oscilaciones (fenómeno de Runge)"
        },
        "ejemplo": {
            "x": [0, 1, 2, 3],
            "y": [1, 2, 0, 4],
            "grado": 3,
            "descripcion": "Este ejemplo interpola 4 puntos con un polinomio de grado 3"
        }
    }

@router.get("/ejemplos")
async def obtener_ejemplos():
    """
    Proporciona conjuntos de datos de ejemplo para probar los métodos de interpolación.
    """
    return {
        "ejemplo_lineal": {
            "nombre": "Interpolación Lineal",
            "descripcion": "Dos puntos que forman una línea recta",
            "x": [0, 5],
            "y": [2, 12],
            "grado": 1
        },
        "ejemplo_cuadratico": {
            "nombre": "Interpolación Cuadrática",
            "descripcion": "Tres puntos formando una parábola",
            "x": [0, 1, 2],
            "y": [0, 1, 4],
            "grado": 2
        },
        "ejemplo_cubico": {
            "nombre": "Interpolación Cúbica",
            "descripcion": "Cuatro puntos para un polinomio de grado 3",
            "x": [-1, 0, 1, 2],
            "y": [0, 1, 0, -3],
            "grado": 3
        },
        "ejemplo_complejo": {
            "nombre": "Interpolación de Grado Alto",
            "descripcion": "Seis puntos para demostrar interpolación de mayor grado",
            "x": [0, 1, 2, 3, 4, 5],
            "y": [0, 0.8, 0.9, 0.1, -0.8, -1.0],
            "grado": 5
        },
        "ejemplo_seno": {
            "nombre": "Aproximación de Función Seno",
            "descripcion": "Puntos muestreados de la función seno",
            "x": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            "y": [0, 0.479, 0.841, 0.997, 0.909, 0.598, 0.141],
            "grado": 6
        }
    }

@router.post("/spline-lineal", response_model=SplineResponse)
async def interpolar_spline_lineal(request: SplineRequest):
    """
    Interpolación usando Spline Lineal.
    
    El método de Spline Lineal construye una función polinomial a trozos donde cada
    segmento entre puntos consecutivos es una línea recta (polinomio de grado 1).
    Garantiza continuidad C⁰ (continuidad de la función).
    
    **Parámetros:**
    - **x**: Lista de valores x (hasta 8 puntos). Los valores deben ser únicos.
    - **y**: Lista de valores y correspondientes (mismo tamaño que x).
    
    **Retorna:**
    - Lista de polinomios por tramo
    - Gráfico con los puntos y los splines
    - Información de cada tramo (rango y coeficientes)
    
    **Características:**
    - Cada tramo es una línea recta (y = m*x + b)
    - Continuidad C⁰ (la función es continua)
    - Simple y rápido de calcular
    - No presenta oscilaciones
    
    **Notas:**
    - Los valores de x deben ser distintos entre sí
    - Se construyen (n-1) segmentos lineales para n puntos
    - Cada segmento conecta dos puntos consecutivos
    """
    try:
        # Validación básica
        if len(request.x) > 8:
            raise HTTPException(
                status_code=400,
                detail="Se permiten máximo 8 puntos para interpolación"
            )
        
        if len(request.x) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 2 puntos para interpolación"
            )
        
        # Ejecutar el método de Spline Lineal
        start_time = time.time()
        resultado = service.spline_lineal(
            x=request.x,
            y=request.y
        )
        end_time = time.time()
        
        # Agregar tiempo de ejecución al mensaje si fue exitoso
        if resultado["exito"]:
            tiempo = end_time - start_time
            resultado["mensaje"] += f" (Tiempo de ejecución: {tiempo:.6f} segundos)"
        
        return resultado
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/spline-cubico", response_model=SplineResponse)
async def interpolar_spline_cubico(request: SplineRequest):
    """
    Interpolación usando Spline Cúbico Natural.
    
    El método de Spline Cúbico construye una función polinomial a trozos donde cada
    segmento entre puntos consecutivos es un polinomio de grado 3. Garantiza continuidad
    C² (continuidad de la función, primera y segunda derivadas).
    
    **Parámetros:**
    - **x**: Lista de valores x (hasta 8 puntos). Los valores deben ser únicos.
    - **y**: Lista de valores y correspondientes (mismo tamaño que x).
    
    **Retorna:**
    - Lista de polinomios por tramo
    - Gráfico con los puntos y los splines
    - Información de cada tramo (rango y coeficientes)
    
    **Características:**
    - Cada tramo es un polinomio cúbico (y = a*x³ + b*x² + c*x + d)
    - Continuidad C² (función, primera y segunda derivadas son continuas)
    - Spline "natural": segunda derivada = 0 en los extremos
    - Suave y sin oscilaciones bruscas
    - Muy utilizado en gráficos por computadora y diseño
    
    **Ventajas:**
    - Curvas muy suaves y naturales
    - Buena estabilidad numérica
    - No presenta el fenómeno de Runge
    - Minimiza la curvatura total
    
    **Notas:**
    - Los valores de x deben ser distintos entre sí
    - Se construyen (n-1) segmentos cúbicos para n puntos
    - Requiere resolver un sistema de ecuaciones más grande que el spline lineal
    """
    try:
        # Validación básica
        if len(request.x) > 8:
            raise HTTPException(
                status_code=400,
                detail="Se permiten máximo 8 puntos para interpolación"
            )
        
        if len(request.x) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 2 puntos para interpolación"
            )
        
        # Ejecutar el método de Spline Cúbico
        start_time = time.time()
        resultado = service.spline_cubico(
            x=request.x,
            y=request.y
        )
        end_time = time.time()
        
        # Agregar tiempo de ejecución al mensaje si fue exitoso
        if resultado["exito"]:
            tiempo = end_time - start_time
            resultado["mensaje"] += f" (Tiempo de ejecución: {tiempo:.6f} segundos)"
        
        return resultado
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/comparar", response_model=ComparacionResponse)
async def comparar_metodos(request: ComparacionRequest):
    """
    Ejecuta todos los métodos de interpolación y genera un informe comparativo.
    
    Este endpoint ejecuta simultáneamente los 5 métodos de interpolación disponibles
    (Vandermonde, Newton, Lagrange, Spline Lineal, Spline Cúbico) con los mismos datos
    y genera un análisis comparativo detallado.
    
    **Parámetros:**
    - **x**: Lista de valores x (hasta 8 puntos). Los valores deben ser únicos.
    - **y**: Lista de valores y correspondientes (mismo tamaño que x).
    - **grado**: Grado del polinomio para Vandermonde (opcional, por defecto usa len(x)-1).
    
    **Retorna:**
    - Resultados de cada método con tiempos de ejecución
    - Gráfico comparativo de tiempos
    - Gráfico visual comparando todas las curvas
    - Análisis detallado con ventajas/desventajas de cada método
    - Recomendación basada en el número de puntos
    - Identificación del método más rápido
    
    **Características del Informe:**
    - Tiempos de ejecución en milisegundos
    - Complejidad algorítmica de cada método
    - Ventajas y desventajas específicas
    - Casos de uso recomendados
    - Análisis adaptado al número de puntos proporcionados
    
    **Notas:**
    - Los valores de x deben ser distintos entre sí
    - Se requieren al menos 2 puntos
    - El informe identifica el método más eficiente para el caso específico
    - Incluye recomendaciones basadas en el fenómeno de Runge y estabilidad numérica
    """
    try:
        # Validación básica
        if len(request.x) > 8:
            raise HTTPException(
                status_code=400,
                detail="Se permiten máximo 8 puntos para interpolación"
            )
        
        if len(request.x) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 2 puntos para interpolación"
            )
        
        # Ejecutar comparación
        start_time = time.time()
        resultado = service.comparar_metodos(
            x=request.x,
            y=request.y,
            grado=request.grado
        )
        end_time = time.time()
        
        # Agregar tiempo total de comparación al mensaje si fue exitoso
        if resultado["exito"]:
            tiempo_total = end_time - start_time
            resultado["mensaje"] += f" Tiempo total de comparación: {tiempo_total:.6f} segundos."
        
        return resultado
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

