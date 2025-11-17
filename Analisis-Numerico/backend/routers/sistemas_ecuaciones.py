from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from services.sistemas_service import (
    GaussPiv, GaussPiv_verbose,
    jacobi, gauss_seidel, sor,
    comparar_metodos_iterativos
)
from models.schemas import (
    SistemaIterativoRequest, SORRequest, SistemaIterativoResponse,
    ComparacionSistemasIterativosRequest, ComparacionSistemasIterativosResponse
)

router = APIRouter()

class MatrizSistema(BaseModel):
    A: List[List[float]]
    b: List[float]
    tipo_pivoteo: int = 0  # 0: sin pivoteo, 1: parcial, 2: total
    mostrar_proceso: bool = False

class RespuestaSistema(BaseModel):
    exito: bool
    solucion: List[float]
    marcador: List[int]
    mensaje: str
    proceso: Optional[str] = None

@router.post("/gauss-pivoteo", response_model=RespuestaSistema)
async def resolver_sistema_gauss(sistema: MatrizSistema):
    """
    Resuelve un sistema de ecuaciones lineales usando eliminación de Gauss con pivoteo
    
    - **A**: Matriz de coeficientes (n x n)
    - **b**: Vector de términos independientes (n x 1) 
    - **tipo_pivoteo**: 0 = sin pivoteo, 1 = pivoteo parcial, 2 = pivoteo total
    - **mostrar_proceso**: Si mostrar el proceso paso a paso
    """
    try:
        # Validar dimensiones
        A = np.array(sistema.A)
        b = np.array(sistema.b)
        
        if A.shape[0] != A.shape[1]:
            raise HTTPException(
                status_code=400, 
                detail="La matriz A debe ser cuadrada"
            )
        
        if len(b) != A.shape[0]:
            raise HTTPException(
                status_code=400, 
                detail="El vector b debe tener la misma cantidad de filas que A"
            )
        
        n = A.shape[0]
        
        # Validar tipo de pivoteo
        if sistema.tipo_pivoteo not in [0, 1, 2]:
            raise HTTPException(
                status_code=400, 
                detail="Tipo de pivoteo debe ser 0, 1 o 2"
            )
        
        proceso_str = None
        
        if sistema.mostrar_proceso:
            # Capturar la salida del proceso
            import io
            import contextlib
            
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                x, mark = GaussPiv_verbose(A, b, n, sistema.tipo_pivoteo, verbose=True)
            proceso_str = f.getvalue()
        else:
            x, mark = GaussPiv(A, b, n, sistema.tipo_pivoteo)
        
        # Si hubo pivoteo total, reordenar la solución
        if sistema.tipo_pivoteo == 2:
            x_ordenada = np.zeros(n)
            for i in range(n):
                x_ordenada[mark[i]] = x[i]
            x = x_ordenada
        
        return RespuestaSistema(
            exito=True,
            solucion=x.tolist(),
            marcador=mark,
            mensaje=f"Sistema resuelto exitosamente usando {'sin pivoteo' if sistema.tipo_pivoteo == 0 else 'pivoteo parcial' if sistema.tipo_pivoteo == 1 else 'pivoteo total'}",
            proceso=proceso_str
        )
        
    except ValueError as e:
        error_msg = str(e)
        if "Pivote cero" in error_msg:
            raise HTTPException(
                status_code=400,
                detail=f"Error en el método: {error_msg}. El sistema puede no tener solución única."
            )
        else:
            raise HTTPException(status_code=400, detail=f"Error en los datos: {error_msg}")
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/info")
async def info_sistemas():
    """
    Información sobre los métodos de sistemas de ecuaciones disponibles
    """
    return {
        "metodos": {
            "gauss_pivoteo": {
                "descripcion": "Eliminación de Gauss con diferentes tipos de pivoteo",
                "tipos_pivoteo": {
                    "0": "Sin pivoteo",
                    "1": "Pivoteo parcial",
                    "2": "Pivoteo total"
                },
                "uso": "Resolver sistemas de ecuaciones lineales Ax = b"
            }
        },
        "formatos": {
            "matriz_A": "Lista de listas con los coeficientes [[a11, a12, ...], [a21, a22, ...], ...]",
            "vector_b": "Lista con los términos independientes [b1, b2, ...]"
        },
        "ejemplo": {
            "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
            "b": [8, -11, -3],
            "tipo_pivoteo": 1,
            "mostrar_proceso": False
        }
    }

@router.post("/validar-sistema")
async def validar_sistema(sistema: MatrizSistema):
    """
    Valida si un sistema de ecuaciones está bien formado
    """
    try:
        A = np.array(sistema.A)
        b = np.array(sistema.b)
        
        validaciones = {
            "matriz_cuadrada": A.shape[0] == A.shape[1],
            "dimensiones_correctas": len(b) == A.shape[0],
            "determinante_no_cero": np.linalg.det(A) != 0 if A.shape[0] == A.shape[1] else False,
            "tamaño_sistema": A.shape[0]
        }
        
        es_valido = all([
            validaciones["matriz_cuadrada"], 
            validaciones["dimensiones_correctas"],
            validaciones["determinante_no_cero"]
        ])
        
        return {
            "es_valido": es_valido,
            "detalles": validaciones,
            "determinante": float(np.linalg.det(A)) if validaciones["matriz_cuadrada"] else None,
            "recomendacion": "Sin pivoteo" if abs(np.linalg.det(A)) > 0.1 else "Pivoteo parcial o total recomendado"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error al validar el sistema: {str(e)}"
        )

@router.post("/jacobi", response_model=SistemaIterativoResponse)
async def resolver_jacobi(sistema: SistemaIterativoRequest):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Jacobi
    
    - **A**: Matriz de coeficientes (n x n), preferiblemente diagonalmente dominante
    - **b**: Vector de términos independientes
    - **x0**: Vector inicial para comenzar la iteración
    - **tolerancia**: Criterio de convergencia
    - **niter**: Número máximo de iteraciones
    - **modo**: Tipo de error ("absoluto" o "relativo")
    
    El método converge si el radio espectral de la matriz de iteración es < 1
    """
    try:
        resultado = jacobi(
            x0=sistema.x0,
            A=sistema.A,
            b=sistema.b,
            tol=sistema.tolerancia,
            niter=sistema.niter,
            modo=sistema.modo
        )
        return SistemaIterativoResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en Jacobi: {str(e)}")

@router.post("/gauss-seidel", response_model=SistemaIterativoResponse)
async def resolver_gauss_seidel(sistema: SistemaIterativoRequest):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Gauss-Seidel
    
    - **A**: Matriz de coeficientes (n x n), preferiblemente simétrica y definida positiva
    - **b**: Vector de términos independientes
    - **x0**: Vector inicial para comenzar la iteración
    - **tolerancia**: Criterio de convergencia
    - **niter**: Número máximo de iteraciones
    - **modo**: Tipo de error ("absoluto" o "relativo")
    
    Generalmente converge más rápido que Jacobi si la matriz cumple las condiciones
    """
    try:
        resultado = gauss_seidel(
            x0=sistema.x0,
            A=sistema.A,
            b=sistema.b,
            tol=sistema.tolerancia,
            niter=sistema.niter,
            modo=sistema.modo
        )
        return SistemaIterativoResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en Gauss-Seidel: {str(e)}")

@router.post("/sor", response_model=SistemaIterativoResponse)
async def resolver_sor(sistema: SORRequest):
    """
    Resuelve un sistema de ecuaciones lineales usando el método SOR (Successive Over-Relaxation)
    
    - **A**: Matriz de coeficientes (n x n)
    - **b**: Vector de términos independientes
    - **x0**: Vector inicial para comenzar la iteración
    - **tolerancia**: Criterio de convergencia
    - **niter**: Número máximo de iteraciones
    - **w**: Parámetro de relajación (0 < w < 2)
        - w = 1: Equivale a Gauss-Seidel
        - w < 1: Sub-relajación
        - w > 1: Sobre-relajación (acelera convergencia si se elige bien)
    - **modo**: Tipo de error ("absoluto" o "relativo")
    
    El parámetro w óptimo depende de las propiedades de la matriz
    """
    try:
        resultado = sor(
            x0=sistema.x0,
            A=sistema.A,
            b=sistema.b,
            tol=sistema.tolerancia,
            niter=sistema.niter,
            w=sistema.w,
            modo=sistema.modo
        )
        return SistemaIterativoResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en SOR: {str(e)}")

@router.post("/comparar-iterativos", response_model=ComparacionSistemasIterativosResponse)
async def comparar_metodos_iterativos_endpoint(sistema: ComparacionSistemasIterativosRequest):
    """
    Compara los tres métodos iterativos (Jacobi, Gauss-Seidel y SOR) para el mismo sistema
    
    Ejecuta los tres métodos con los mismos parámetros y genera:
    - Comparación de tiempos de ejecución
    - Comparación de número de iteraciones
    - Gráfico de evolución del error
    - Análisis de convergencia (radio espectral)
    - Recomendaciones sobre cuál método usar
    
    Parámetros:
    - **A**: Matriz de coeficientes
    - **b**: Vector de términos independientes
    - **x0**: Vector inicial
    - **tolerancia**: Criterio de convergencia
    - **niter**: Número máximo de iteraciones
    - **w**: Parámetro de relajación para SOR
    - **modo**: Tipo de error
    """
    try:
        resultado = comparar_metodos_iterativos(
            A=sistema.A,
            b=sistema.b,
            x0=sistema.x0,
            tol=sistema.tolerancia,
            niter=sistema.niter,
            w=sistema.w,
            modo=sistema.modo
        )
        return ComparacionSistemasIterativosResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en comparación: {str(e)}")

