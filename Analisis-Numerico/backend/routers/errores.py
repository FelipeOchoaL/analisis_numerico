from fastapi import APIRouter, HTTPException
from models.schemas import (
    ErrorAbsolutoRequest, ErrorRelativoRequest, PropagacionErrorRequest,
    ErrorResponse
)
from services.errores_service import ErroresService
import time

router = APIRouter()
service = ErroresService()

@router.post("/error-absoluto")
async def calcular_error_absoluto(request: ErrorAbsolutoRequest):
    """
    Calcula el error absoluto entre un valor aproximado y uno exacto.
    
    Error absoluto = |x_exacto - x_aproximado|
    
    - **x_aproximado**: Valor aproximado
    - **x_exacto**: Valor exacto
    """
    try:
        start_time = time.time()
        resultado = service.error_absoluto(
            x_aproximado=request.x_aproximado,
            x_exacto=request.x_exacto
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/error-relativo")
async def calcular_error_relativo(request: ErrorRelativoRequest):
    """
    Calcula el error relativo entre un valor aproximado y uno exacto.
    
    Error relativo = |x_exacto - x_aproximado| / |x_exacto|
    
    - **x_aproximado**: Valor aproximado
    - **x_exacto**: Valor exacto (no puede ser cero)
    """
    try:
        start_time = time.time()
        resultado = service.error_relativo(
            x_aproximado=request.x_aproximado,
            x_exacto=request.x_exacto
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/propagacion-error")
async def calcular_propagacion_error(request: PropagacionErrorRequest):
    """
    Calcula la propagación de errores para operaciones básicas.
    
    - **x**: Valor de X
    - **ex**: Error en X
    - **y**: Valor de Y
    - **ey**: Error en Y
    - **operacion**: Tipo de operación (suma, resta, producto, division)
    
    Fórmulas:
    - Suma/Resta: √(ex² + ey²)
    - Producto/División: |resultado| * √((ex/x)² + (ey/y)²)
    """
    try:
        start_time = time.time()
        resultado = service.propagacion_error(
            x=request.x,
            ex=request.ex,
            y=request.y,
            ey=request.ey,
            operacion=request.operacion
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
