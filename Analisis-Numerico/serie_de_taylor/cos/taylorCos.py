import math
from typing import Tuple, List

def taylor_cos(theta: float, tol: float = 1e-8, niter: int = 1000,
               relative_error: bool = False) -> Tuple[float, List[float], List[float]]:
    """
    Aproxima cos(theta) usando la serie de Taylor:
        cos(theta) = sum_{k=0}^∞ (-1)^k * theta^(2k) / (2k)!
    Parámetros:
        theta: valor en radianes
        tol: tolerancia para detener la suma
        niter: máximo de iteraciones (términos)
        relative_error: si True usa error relativo |(s_n - s_{n-1})/s_n|
                        si False usa error absoluto |s_n - s_{n-1}|
    Devuelve:
        aprox: valor aproximado de cos(theta)
        partial_sums: lista con las sumas parciales s_0, s_1, ...
        errors: lista con errores E_1, E_2, ... (E_i asociado a s_i)
    """
    partial_sums: List[float] = []
    errors: List[float] = []

    # primer término k = 0
    k = 0
    term = ((-1)**k) * (theta**(2*k)) / math.factorial(2*k)  # = 1
    partial_sums.append(term)

    # condición inicial de error grande para entrar al while
    E = float('inf')

    while E > tol and k < niter - 1:  # niter términos máximo
        k += 1
        term = ((-1)**k) * (theta**(2*k)) / math.factorial(2*k)
        s_new = partial_sums[-1] + term
        partial_sums.append(s_new)

        if relative_error:
            # evitar división por cero
            if s_new != 0:
                E = abs((s_new - partial_sums[-2]) / s_new)
            else:
                E = abs(s_new - partial_sums[-2])
        else:
            E = abs(s_new - partial_sums[-2])

        errors.append(E)

    aprox = partial_sums[-1]
    return aprox, partial_sums, errors

# Ejemplo de uso
if __name__ == "__main__":
    theta = 0.785398163  # radianes
    aprox, parcial, errs = taylor_cos(theta, tol=1e-10, niter=50)
    print("theta =", theta)
    print("Aproximación (Taylor):", aprox)
    print("cos(theta) (math.cos):", math.cos(theta))
    print("Último error (|s_n - s_{n-1}|):", errs[-1] if errs else 0.0)
    print("Términos usados:", len(parcial))
