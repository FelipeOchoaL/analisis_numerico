from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from services.sistemas_service import GaussPiv, GaussPiv_verbose

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

