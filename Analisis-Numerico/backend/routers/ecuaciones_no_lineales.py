from fastapi import APIRouter, HTTPException
from models.schemas import (
    BiseccionRequest, PuntoFijoRequest, ReglaFalsaRequest, 
    BusquedaIncrementalRequest, NewtonRaphsonRequest, SecanteRequest, 
    RaicesMultiplesRequest, MetodoResponse
)
from services.ecuaciones_service import EcuacionesService
import time

router = APIRouter()
service = EcuacionesService()

@router.post("/biseccion", response_model=MetodoResponse)
async def metodo_biseccion(request: BiseccionRequest):
    """
    Implementa el método de bisección para encontrar raíces de ecuaciones no lineales.
    
    - **xi**: Extremo izquierdo del intervalo
    - **xs**: Extremo derecho del intervalo  
    - **tolerancia**: Tolerancia del método
    - **niter**: Número máximo de iteraciones
    - **funcion**: Función f(x) como string (usar 'x' como variable)
    """
    try:
        start_time = time.time()
        resultado = service.biseccion(
            xi=request.xi,
            xs=request.xs,
            tolerancia=request.tolerancia,
            niter=request.niter,
            funcion=request.funcion,
            tipo_error=request.tipo_error
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/punto-fijo", response_model=MetodoResponse)
async def metodo_punto_fijo(request: PuntoFijoRequest):
    """
    Implementa el método de punto fijo para encontrar raíces de ecuaciones no lineales.
    
    - **x0**: Valor inicial
    - **tolerancia**: Tolerancia del método
    - **niter**: Número máximo de iteraciones
    - **funcion_f**: Función f(x) original
    - **funcion_g**: Función de iteración g(x)
    """
    try:
        start_time = time.time()
        resultado = service.punto_fijo(
            x0=request.x0,
            tolerancia=request.tolerancia,
            niter=request.niter,
            funcion_f=request.funcion_f,
            funcion_g=request.funcion_g,
            tipo_error=request.tipo_error
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/regla-falsa", response_model=MetodoResponse)
async def metodo_regla_falsa(request: ReglaFalsaRequest):
    """
    Implementa el método de regla falsa para encontrar raíces de ecuaciones no lineales.
    
    - **x0**: Extremo izquierdo del intervalo
    - **x1**: Extremo derecho del intervalo
    - **tolerancia**: Tolerancia del método
    - **niter**: Número máximo de iteraciones
    - **funcion**: Función f(x) como string
    """
    try:
        start_time = time.time()
        resultado = service.regla_falsa(
            x0=request.x0,
            x1=request.x1,
            tolerancia=request.tolerancia,
            niter=request.niter,
            funcion=request.funcion,
            tipo_error=request.tipo_error
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/busqueda-incremental", response_model=MetodoResponse)
async def busqueda_incremental(request: BusquedaIncrementalRequest):
    """
    Implementa la búsqueda incremental para encontrar intervalos con cambio de signo.
    
    - **x0**: Valor inicial
    - **delta**: Incremento
    - **niter**: Número máximo de iteraciones
    - **funcion**: Función f(x) como string
    """
    try:
        start_time = time.time()
        resultado = service.busqueda_incremental(
            x0=request.x0,
            delta=request.delta,
            niter=request.niter,
            funcion=request.funcion
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/newton-raphson", response_model=MetodoResponse)
async def metodo_newton_raphson(request: NewtonRaphsonRequest):
    """
    Implementa el método de Newton-Raphson para encontrar raíces de ecuaciones no lineales.
    
    El método utiliza la fórmula: x_{i+1} = x_i - f(x_i)/f'(x_i)
    
    - **x0**: Valor inicial
    - **tolerancia**: Tolerancia del método
    - **niter**: Número máximo de iteraciones
    - **funcion_f**: Función f(x) como string (usar 'x' como variable)
    - **funcion_df**: Derivada f'(x) como string (usar 'x' como variable)
    - **incluir_error**: Si incluir columna de error en la tabla (opcional, por defecto True)
    
    La tabla de salida incluye: i, xi, f(xi), f'(xi) y opcionalmente E (error)
    """
    try:
        start_time = time.time()
        resultado = service.newton_raphson(
            x0=request.x0,
            tolerancia=request.tolerancia,
            niter=request.niter,
            funcion_f=request.funcion_f,
            funcion_df=request.funcion_df,
            incluir_error=request.incluir_error,
            tipo_error=request.tipo_error,
            tipo_precision=request.tipo_precision,
            precision=request.precision
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/secante", response_model=MetodoResponse)
async def metodo_secante(request: SecanteRequest):
    """
    Implementa el método de la secante para encontrar raíces de ecuaciones no lineales.
    
    El método utiliza la fórmula: x_{i+1} = x_i - f(x_i) * (x_i - x_{i-1}) / (f(x_i) - f(x_{i-1}))
    
    - **x0**: Primer valor inicial
    - **x1**: Segundo valor inicial
    - **tolerancia**: Tolerancia del método
    - **niter**: Número máximo de iteraciones
    - **funcion**: Función f(x) como string (usar 'x' como variable)
    - **incluir_error**: Si incluir columna de error en la tabla (opcional, por defecto True)
    - **tipo_precision**: Tipo de precisión: "decimales" o "significativas" (opcional, por defecto "decimales")
    - **precision**: Número de decimales o cifras significativas (opcional, por defecto 6)
    
    La tabla de salida incluye: i, xi-1, xi, f(xi-1), f(xi) y opcionalmente E (error)
    """
    try:
        start_time = time.time()
        resultado = service.secante(
            x0=request.x0,
            x1=request.x1,
            tolerancia=request.tolerancia,
            niter=request.niter,
            funcion=request.funcion,
            incluir_error=request.incluir_error,
            tipo_error=request.tipo_error,
            tipo_precision=request.tipo_precision,
            precision=request.precision
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/raices-multiples", response_model=MetodoResponse)
async def metodo_raices_multiples(request: RaicesMultiplesRequest):
    """
    Implementa el método de raíces múltiples para encontrar raíces con multiplicidad mayor a 1.
    
    El método utiliza la fórmula: x_{i+1} = x_i - (f(x_i) * f'(x_i)) / (f'(x_i)^2 - f(x_i) * f''(x_i))
    
    Este método es especialmente útil cuando la función tiene raíces múltiples, donde f(x), f'(x) y f''(x)
    se anulan en el mismo punto.
    
    - **x0**: Valor inicial X₀
    - **tolerancia**: Tolerancia del método
    - **niter**: Número máximo de iteraciones
    - **funcion_f**: Función f(x) como string (usar 'x' como variable)
    - **funcion_df**: Primera derivada f'(x) como string (usar 'x' como variable)
    - **funcion_ddf**: Segunda derivada f''(x) como string (usar 'x' como variable)
    - **modo**: Modo de cálculo de error: 'cs' (cifras significativas) o 'dc' (decimales correctos)
    
    La tabla de salida incluye: Iteración, xi, f(xi), f'(xi), f''(xi), Denominador, Error
    """
    try:
        start_time = time.time()
        resultado = service.raices_multiples(
            x0=request.x0,
            tolerancia=request.tolerancia,
            niter=request.niter,
            funcion_f=request.funcion_f,
            funcion_df=request.funcion_df,
            funcion_ddf=request.funcion_ddf,
            tipo_error=request.tipo_error,
            modo=request.modo
        )
        end_time = time.time()
        
        resultado["tiempo_ejecucion"] = end_time - start_time
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
