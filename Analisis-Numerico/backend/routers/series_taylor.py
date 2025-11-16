from fastapi import APIRouter, HTTPException
from models.schemas import TaylorCosRequest, TaylorSenRequest, TaylorResponse
from services.taylor_service import TaylorService
import time

router = APIRouter()
service = TaylorService()

@router.post("/coseno")
async def taylor_coseno(request: TaylorCosRequest):
    """
    Aproxima cos(theta) usando la serie de Taylor.
    
    Serie: cos(theta) = Σ[k=0 to ∞] (-1)^k * theta^(2k) / (2k)!
    
    - **theta**: Ángulo en radianes
    - **tolerancia**: Tolerancia para detener la suma (default: 1e-8)
    - **niter**: Número máximo de términos (default: 1000)
    - **error_relativo**: Usar error relativo en lugar de absoluto (default: false)
    """
    try:
        start_time = time.time()
        resultado = service.taylor_cos(
            theta=request.theta,
            tolerancia=request.tolerancia,
            niter=request.niter,
            error_relativo=request.error_relativo
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/seno")
async def taylor_seno(request: TaylorSenRequest):
    """
    Aproxima sen(theta) usando la serie de Taylor.
    
    Serie: sen(theta) = Σ[k=0 to ∞] (-1)^k * theta^(2k+1) / (2k+1)!
    
    - **theta**: Ángulo en radianes
    - **tolerancia**: Tolerancia para detener la suma (default: 1e-8)
    - **niter**: Número máximo de términos (default: 1000)
    - **error_relativo**: Usar error relativo en lugar de absoluto (default: false)
    """
    try:
        start_time = time.time()
        resultado = service.taylor_sen(
            theta=request.theta,
            tolerancia=request.tolerancia,
            niter=request.niter,
            error_relativo=request.error_relativo
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ejemplos")
async def obtener_ejemplos():
    """
    Devuelve ejemplos de ángulos comunes en radianes para pruebas.
    """
    import math
    
    ejemplos = {
        "angulos_comunes": {
            "0_grados": {"radianes": 0, "grados": 0},
            "30_grados": {"radianes": math.pi/6, "grados": 30},
            "45_grados": {"radianes": math.pi/4, "grados": 45},
            "60_grados": {"radianes": math.pi/3, "grados": 60},
            "90_grados": {"radianes": math.pi/2, "grados": 90},
            "180_grados": {"radianes": math.pi, "grados": 180},
            "270_grados": {"radianes": 3*math.pi/2, "grados": 270},
            "360_grados": {"radianes": 2*math.pi, "grados": 360}
        },
        "valores_exactos": {
            "cos(0)": 1,
            "cos(π/6)": math.sqrt(3)/2,
            "cos(π/4)": math.sqrt(2)/2,
            "cos(π/3)": 0.5,
            "cos(π/2)": 0,
            "sin(0)": 0,
            "sin(π/6)": 0.5,
            "sin(π/4)": math.sqrt(2)/2,
            "sin(π/3)": math.sqrt(3)/2,
            "sin(π/2)": 1
        }
    }
    
    return ejemplos
