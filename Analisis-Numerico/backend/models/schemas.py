from pydantic import BaseModel, Field
from typing import List, Optional, Union

# Modelos para Ecuaciones No Lineales
class BiseccionRequest(BaseModel):
    xi: float = Field(..., description="Extremo izquierdo del intervalo")
    xs: float = Field(..., description="Extremo derecho del intervalo")
    tolerancia: float = Field(..., gt=0, description="Tolerancia del método")
    niter: int = Field(..., gt=0, description="Número máximo de iteraciones")
    funcion: str = Field(..., description="Función f(x) como string")
    tipo_error: str = Field(default="absoluto", description="Tipo de error: 'absoluto' o 'relativo'")

class PuntoFijoRequest(BaseModel):
    x0: float = Field(..., description="Valor inicial")
    tolerancia: float = Field(..., gt=0, description="Tolerancia del método")
    niter: int = Field(..., gt=0, description="Número máximo de iteraciones")
    funcion_f: str = Field(..., description="Función f(x) original")
    funcion_g: str = Field(..., description="Función de iteración g(x)")
    tipo_error: str = Field(default="absoluto", description="Tipo de error: 'absoluto' o 'relativo'")

class ReglaFalsaRequest(BaseModel):
    x0: float = Field(..., description="Extremo izquierdo del intervalo")
    x1: float = Field(..., description="Extremo derecho del intervalo")
    tolerancia: float = Field(..., gt=0, description="Tolerancia del método")
    niter: int = Field(..., gt=0, description="Número máximo de iteraciones")
    funcion: str = Field(..., description="Función f(x) como string")
    tipo_error: str = Field(default="absoluto", description="Tipo de error: 'absoluto' o 'relativo'")

class BusquedaIncrementalRequest(BaseModel):
    x0: float = Field(..., description="Valor inicial")
    delta: float = Field(..., gt=0, description="Incremento")
    niter: int = Field(..., gt=0, description="Número máximo de iteraciones")
    funcion: str = Field(..., description="Función f(x) como string")

class NewtonRaphsonRequest(BaseModel):
    x0: float = Field(..., description="Valor inicial")
    tolerancia: float = Field(..., gt=0, description="Tolerancia del método")
    niter: int = Field(..., gt=0, description="Número máximo de iteraciones")
    funcion_f: str = Field(..., description="Función f(x) como string")
    funcion_df: str = Field(..., description="Derivada f'(x) como string")
    incluir_error: bool = Field(default=True, description="Incluir columna de error en la tabla")
    tipo_error: str = Field(default="absoluto", description="Tipo de error: 'absoluto' o 'relativo'")
    tipo_precision: str = Field(default="decimales", description="Tipo de precisión: 'decimales' o 'significativas'")
    precision: int = Field(default=6, gt=0, description="Número de decimales o cifras significativas")

class SecanteRequest(BaseModel):
    x0: float = Field(..., description="Primer valor inicial")
    x1: float = Field(..., description="Segundo valor inicial")
    tolerancia: float = Field(..., gt=0, description="Tolerancia del método")
    niter: int = Field(..., gt=0, description="Número máximo de iteraciones")
    funcion: str = Field(..., description="Función f(x) como string")
    incluir_error: bool = Field(default=True, description="Incluir columna de error en la tabla")
    tipo_error: str = Field(default="absoluto", description="Tipo de error: 'absoluto' o 'relativo'")
    tipo_precision: str = Field(default="decimales", description="Tipo de precisión: 'decimales' o 'significativas'")
    precision: int = Field(default=6, gt=0, description="Número de decimales o cifras significativas")

class RaicesMultiplesRequest(BaseModel):
    x0: float = Field(..., description="Valor inicial X₀")
    tolerancia: float = Field(..., gt=0, description="Tolerancia del método")
    niter: int = Field(..., gt=0, description="Número máximo de iteraciones")
    funcion_f: str = Field(..., description="Función f(x) como string")
    funcion_df: str = Field(..., description="Primera derivada f'(x) como string")
    funcion_ddf: str = Field(..., description="Segunda derivada f''(x) como string")
    tipo_error: str = Field(default="absoluto", description="Tipo de error: 'absoluto' o 'relativo'")
    modo: str = Field(default="dc", description="Modo de error: 'cs' (cifras significativas) o 'dc' (decimales correctos)")

# Modelos para Errores
class ErrorAbsolutoRequest(BaseModel):
    x_aproximado: float = Field(..., description="Valor aproximado")
    x_exacto: float = Field(..., description="Valor exacto")

class ErrorRelativoRequest(BaseModel):
    x_aproximado: float = Field(..., description="Valor aproximado")
    x_exacto: float = Field(..., description="Valor exacto")

class PropagacionErrorRequest(BaseModel):
    x: float = Field(..., description="Valor de X")
    ex: float = Field(..., description="Error en X")
    y: float = Field(..., description="Valor de Y")
    ey: float = Field(..., description="Error en Y")
    operacion: str = Field(..., description="Tipo de operación: suma, resta, producto, division")

# Modelos para Series de Taylor
class TaylorCosRequest(BaseModel):
    theta: float = Field(..., description="Ángulo en radianes")
    tolerancia: float = Field(default=1e-8, gt=0, description="Tolerancia para detener la suma")
    niter: int = Field(default=1000, gt=0, description="Número máximo de términos")
    error_relativo: bool = Field(default=False, description="Usar error relativo en lugar de absoluto")

class TaylorSenRequest(BaseModel):
    theta: float = Field(..., description="Ángulo en radianes")
    tolerancia: float = Field(default=1e-8, gt=0, description="Tolerancia para detener la suma")
    niter: int = Field(default=1000, gt=0, description="Número máximo de términos")
    error_relativo: bool = Field(default=False, description="Usar error relativo en lugar de absoluto")

# Modelos de Respuesta
class IteracionData(BaseModel):
    iteracion: int
    valores: dict
    error: Optional[float] = None
    observacion: Optional[str] = None

class MetodoResponse(BaseModel):
    exito: bool
    resultado: Optional[float] = None
    iteraciones: List[IteracionData]
    mensaje: str
    tiempo_ejecucion: Optional[float] = None
    tabla_html: Optional[str] = None
    grafico: Optional[str] = None
    ayuda: Optional[str] = None
    resumen: Optional[dict] = None

class ErrorResponse(BaseModel):
    error_absoluto: Optional[float] = None
    error_relativo: Optional[float] = None
    error_porcentual: Optional[float] = None

class TaylorResponse(BaseModel):
    aproximacion: float
    valor_exacto: float
    sumas_parciales: List[float]
    errores: List[float]
    terminos_utilizados: int
    convergencia: bool

# Modelos para Interpolación
class VandermondeRequest(BaseModel):
    x: List[float] = Field(..., description="Lista de valores x (hasta 8 puntos)")
    y: List[float] = Field(..., description="Lista de valores y (hasta 8 puntos)")
    grado: int = Field(..., ge=1, description="Grado del polinomio interpolante")

class NewtonRequest(BaseModel):
    x: List[float] = Field(..., description="Lista de valores x (hasta 8 puntos)")
    y: List[float] = Field(..., description="Lista de valores y (hasta 8 puntos)")

class LagrangeRequest(BaseModel):
    x: List[float] = Field(..., description="Lista de valores x (hasta 8 puntos)")
    y: List[float] = Field(..., description="Lista de valores y (hasta 8 puntos)")

class InterpolacionResponse(BaseModel):
    exito: bool
    polinomio: Optional[str] = None
    grafico: Optional[str] = None
    mensaje: str
    coeficientes: Optional[List[float]] = None
    grado: Optional[int] = None
