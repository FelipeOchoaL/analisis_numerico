from fastapi import APIRouter, HTTPException
from models.schemas import VandermondeRequest, InterpolacionResponse
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

