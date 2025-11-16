import math
from typing import Dict, Tuple
from models.schemas import ErrorResponse

class ErroresService:
    
    def error_absoluto(self, x_aproximado: float, x_exacto: float) -> Dict[str, float]:
        """Calcula el error absoluto"""
        error_abs = abs(x_exacto - x_aproximado)
        return {
            "error_absoluto": error_abs,
            "x_aproximado": x_aproximado,
            "x_exacto": x_exacto
        }
    
    def error_relativo(self, x_aproximado: float, x_exacto: float) -> Dict[str, float]:
        """Calcula el error relativo"""
        if x_exacto == 0:
            raise ValueError("El valor exacto no puede ser cero para el cálculo del error relativo")
        
        error_abs = abs(x_exacto - x_aproximado)
        error_rel = error_abs / abs(x_exacto)
        error_porcentual = error_rel * 100
        
        return {
            "error_absoluto": error_abs,
            "error_relativo": error_rel,
            "error_porcentual": error_porcentual,
            "x_aproximado": x_aproximado,
            "x_exacto": x_exacto
        }
    
    def propagacion_error(self, x: float, ex: float, y: float, ey: float, operacion: str) -> Dict[str, float]:
        """Calcula la propagación de errores para operaciones básicas"""
        resultado = 0
        error_propagado = 0
        
        if operacion.lower() == "suma":
            resultado = x + y
            # Error absoluto: √(ex² + ey²)
            error_propagado = math.sqrt(ex**2 + ey**2)
            
        elif operacion.lower() == "resta":
            resultado = x - y
            # Error absoluto: √(ex² + ey²)
            error_propagado = math.sqrt(ex**2 + ey**2)
            
        elif operacion.lower() == "producto":
            resultado = x * y
            # Error relativo: √((ex/x)² + (ey/y)²)
            if x == 0 or y == 0:
                raise ValueError("Los valores no pueden ser cero para el producto")
            error_relativo = math.sqrt((ex/x)**2 + (ey/y)**2)
            error_propagado = abs(resultado) * error_relativo
            
        elif operacion.lower() == "division":
            if y == 0:
                raise ValueError("No se puede dividir por cero")
            resultado = x / y
            # Error relativo: √((ex/x)² + (ey/y)²)
            if x == 0:
                raise ValueError("El dividendo no puede ser cero para el cálculo del error")
            error_relativo = math.sqrt((ex/x)**2 + (ey/y)**2)
            error_propagado = abs(resultado) * error_relativo
            
        else:
            raise ValueError("Operación no soportada. Use: suma, resta, producto, division")
        
        return {
            "x": x,
            "ex": ex,
            "y": y,
            "ey": ey,
            "operacion": operacion,
            "resultado": resultado,
            "error_propagado": error_propagado,
            "error_relativo_propagado": error_propagado / abs(resultado) if resultado != 0 else 0
        }
