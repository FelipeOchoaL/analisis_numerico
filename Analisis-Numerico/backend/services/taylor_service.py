import math
from typing import Dict, List, Tuple
from models.schemas import TaylorResponse

class TaylorService:
    
    def taylor_cos(self, theta: float, tolerancia: float = 1e-8, niter: int = 1000,
                   error_relativo: bool = False) -> Dict:
        """
        Aproxima cos(theta) usando la serie de Taylor basado en el código original:
            cos(theta) = sum_{k=0}^∞ (-1)^k * theta^(2k) / (2k)!
        """
        sumas_parciales: List[float] = []
        errores: List[float] = []

        # primer término k = 0
        k = 0
        term = ((-1)**k) * (theta**(2*k)) / math.factorial(2*k)  # = 1
        sumas_parciales.append(term)

        # condición inicial de error grande para entrar al while
        E = float('inf')

        while E > tolerancia and k < niter - 1:  # niter términos máximo
            k += 1
            term = ((-1)**k) * (theta**(2*k)) / math.factorial(2*k)
            s_new = sumas_parciales[-1] + term
            sumas_parciales.append(s_new)

            if error_relativo:
                # evitar división por cero
                if s_new != 0:
                    E = abs((s_new - sumas_parciales[-2]) / s_new)
                else:
                    E = abs(s_new - sumas_parciales[-2])
            else:
                E = abs(s_new - sumas_parciales[-2])

            errores.append(E)

        aproximacion = sumas_parciales[-1]
        valor_exacto = math.cos(theta)
        convergencia = E <= tolerancia
        
        return {
            "aproximacion": aproximacion,
            "valor_exacto": valor_exacto,
            "sumas_parciales": sumas_parciales,
            "errores": errores,
            "terminos_utilizados": len(sumas_parciales),
            "convergencia": convergencia,
            "theta_radianes": theta,
            "tolerancia_usada": tolerancia,
            "error_final": E,
            "diferencia_con_exacto": abs(aproximacion - valor_exacto)
        }
    
    def taylor_sen(self, theta: float, tolerancia: float = 1e-8, niter: int = 1000,
                   error_relativo: bool = False) -> Dict:
        """
        Aproxima sen(theta) usando la serie de Taylor:
            sen(theta) = sum_{k=0}^∞ (-1)^k * theta^(2k+1) / (2k+1)!
        """
        sumas_parciales: List[float] = []
        errores: List[float] = []

        # primer término k = 0
        k = 0
        term = ((-1)**k) * (theta**(2*k+1)) / math.factorial(2*k+1)  # = theta
        sumas_parciales.append(term)

        # condición inicial de error grande para entrar al while
        E = float('inf')

        while E > tolerancia and k < niter - 1:  # niter términos máximo
            k += 1
            term = ((-1)**k) * (theta**(2*k+1)) / math.factorial(2*k+1)
            s_new = sumas_parciales[-1] + term
            sumas_parciales.append(s_new)

            if error_relativo:
                # evitar división por cero
                if s_new != 0:
                    E = abs((s_new - sumas_parciales[-2]) / s_new)
                else:
                    E = abs(s_new - sumas_parciales[-2])
            else:
                E = abs(s_new - sumas_parciales[-2])

            errores.append(E)

        aproximacion = sumas_parciales[-1]
        valor_exacto = math.sin(theta)
        convergencia = E <= tolerancia
        
        return {
            "aproximacion": aproximacion,
            "valor_exacto": valor_exacto,
            "sumas_parciales": sumas_parciales,
            "errores": errores,
            "terminos_utilizados": len(sumas_parciales),
            "convergencia": convergencia,
            "theta_radianes": theta,
            "tolerancia_usada": tolerancia,
            "error_final": E,
            "diferencia_con_exacto": abs(aproximacion - valor_exacto)
        }
