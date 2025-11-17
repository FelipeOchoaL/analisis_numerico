import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import base64
import io
from typing import Dict, List, Tuple

class InterpolacionService:
    
    def vandermonde(self, x: List[float], y: List[float], grado: int) -> Dict:
        """
        Implementa el método de interpolación usando la matriz de Vandermonde.
        
        Args:
            x: Lista de valores x (coordenadas)
            y: Lista de valores y (coordenadas)
            grado: Grado del polinomio interpolante
            
        Returns:
            Diccionario con el polinomio, gráfico y metadatos
        """
        # Validación: verificar que no hay valores x repetidos
        if len(set(x)) != len(x):
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Vandermonde')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": "Error: Los valores de x deben ser únicos. Se encontraron valores repetidos.",
                "coeficientes": None,
                "grado": None
            }
        
        # Validación: verificar que x e y tienen el mismo tamaño
        if len(x) != len(y):
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Vandermonde')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error: Las listas x e y deben tener el mismo tamaño. x tiene {len(x)} elementos y y tiene {len(y)} elementos.",
                "coeficientes": None,
                "grado": None
            }
        
        # Validación: verificar que hay suficientes puntos
        if len(x) < grado + 1:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Vandermonde')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error: Para un polinomio de grado {grado} se necesitan al menos {grado + 1} puntos. Se proporcionaron {len(x)} puntos.",
                "coeficientes": None,
                "grado": None
            }
        
        try:
            # Convertir a arrays de numpy
            x_arr = np.array(x)
            y_arr = np.array(y)
            
            # Crear la matriz de Vandermonde y resolver el sistema
            A = np.vander(x_arr, N=grado + 1, increasing=False)
            coeficientes = np.linalg.solve(A, y_arr)
            
        except np.linalg.LinAlgError as e:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Vandermonde')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error al resolver el sistema de ecuaciones: La matriz es singular o mal condicionada. {str(e)}",
                "coeficientes": None,
                "grado": None
            }
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Vandermonde')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error inesperado en el cálculo: {str(e)}",
                "coeficientes": None,
                "grado": None
            }
        
        # Construcción de la cadena que representa el polinomio
        try:
            poly_str = self._construir_polinomio(coeficientes, grado)
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Vandermonde')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error al construir el polinomio: {str(e)}",
                "coeficientes": None,
                "grado": None
            }
        
        # Crear el gráfico
        try:
            img_uri = self._crear_grafico(x_arr, y_arr, coeficientes, grado)
        except Exception as e:
            return {
                "exito": False,
                "polinomio": poly_str,
                "grafico": None,
                "mensaje": f"Polinomio calculado correctamente, pero error al crear el gráfico: {str(e)}",
                "coeficientes": coeficientes.tolist(),
                "grado": grado
            }
        
        return {
            "exito": True,
            "polinomio": poly_str,
            "grafico": img_uri,
            "mensaje": "Interpolación exitosa usando el método de Vandermonde",
            "coeficientes": coeficientes.tolist(),
            "grado": grado
        }
    
    def _construir_polinomio(self, coeficientes: np.ndarray, grado: int) -> str:
        """
        Construye la representación en string del polinomio.
        
        Args:
            coeficientes: Array con los coeficientes del polinomio
            grado: Grado del polinomio
            
        Returns:
            String representando el polinomio
        """
        terms = []
        for i, coef in enumerate(coeficientes):
            power = grado - i
            
            # Omitir términos muy pequeños (prácticamente cero)
            if abs(coef) < 1e-10:
                continue
            
            # Formatear el coeficiente
            if power == 0:
                # Término constante
                term = f"{coef:.6f}"
            elif power == 1:
                # Término lineal
                if abs(coef - 1.0) < 1e-10:
                    term = "x"
                elif abs(coef + 1.0) < 1e-10:
                    term = "-x"
                else:
                    term = f"{coef:.6f}*x"
            else:
                # Términos de orden superior
                if abs(coef - 1.0) < 1e-10:
                    term = f"x^{power}"
                elif abs(coef + 1.0) < 1e-10:
                    term = f"-x^{power}"
                else:
                    term = f"{coef:.6f}*x^{power}"
            
            terms.append(term)
        
        if not terms:
            return "0"
        
        # Unir los términos con signos apropiados
        poly_str = terms[0]
        for term in terms[1:]:
            if term.startswith("-"):
                poly_str += f" - {term[1:]}"
            else:
                poly_str += f" + {term}"
        
        return poly_str
    
    def _crear_grafico(self, x: np.ndarray, y: np.ndarray, coeficientes: np.ndarray, grado: int) -> str:
        """
        Crea el gráfico del polinomio interpolante y los puntos.
        
        Args:
            x: Array de valores x
            y: Array de valores y
            coeficientes: Coeficientes del polinomio
            grado: Grado del polinomio
            
        Returns:
            String con la imagen en formato base64
        """
        plt.figure(figsize=(10, 6))
        
        # Crear valores para graficar el polinomio
        x_min, x_max = min(x) - 1, max(x) + 1
        xpol = np.linspace(x_min, x_max, 500)
        p = np.polyval(coeficientes, xpol)
        
        # Graficar puntos y polinomio
        plt.plot(x, y, 'r*', markersize=15, label='Puntos dados', zorder=5)
        plt.plot(xpol, p, 'b-', linewidth=2, label=f'Polinomio de grado {grado}')
        
        plt.title('Interpolación con Matriz de Vandermonde', fontsize=14, fontweight='bold')
        plt.xlabel('x', fontsize=12)
        plt.ylabel('P(x)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def _crear_grafico_error(self, x: List[float], y: List[float], titulo: str) -> str:
        """
        Crea un gráfico simple solo con los puntos cuando hay un error.
        
        Args:
            x: Lista de valores x
            y: Lista de valores y
            titulo: Título del gráfico
            
        Returns:
            String con la imagen en formato base64
        """
        plt.figure(figsize=(10, 6))
        
        # Graficar solo los puntos
        plt.plot(x, y, 'r*', markersize=15, label='Puntos dados')
        
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def newton_interpolante(self, x: List[float], y: List[float]) -> Dict:
        """
        Implementa el método de interpolación usando diferencias divididas de Newton.
        
        Args:
            x: Lista de valores x (coordenadas)
            y: Lista de valores y (coordenadas)
            
        Returns:
            Diccionario con el polinomio, gráfico y metadatos
        """
        # Validación: verificar que no hay valores x repetidos
        if len(set(x)) != len(x):
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Newton')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": "Error: Los valores de x deben ser únicos. Se encontraron valores repetidos.",
                "coeficientes": None,
                "grado": None,
                "tabla_diferencias": None
            }
        
        # Validación: verificar que x e y tienen el mismo tamaño
        if len(x) != len(y):
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Newton')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error: Las listas x e y deben tener el mismo tamaño. x tiene {len(x)} elementos y y tiene {len(y)} elementos.",
                "coeficientes": None,
                "grado": None,
                "tabla_diferencias": None
            }
        
        # Validación: verificar que hay al menos 2 puntos
        if len(x) < 2:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Newton')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": "Error: Se necesitan al menos 2 puntos para interpolación.",
                "coeficientes": None,
                "grado": None,
                "tabla_diferencias": None
            }
        
        try:
            n = len(x)
            x_arr = np.array(x, dtype=float)
            y_arr = np.array(y, dtype=float)
            
            # Tabla de diferencias divididas
            tabla = np.zeros((n, n))
            tabla[:, 0] = y_arr
            
            for j in range(1, n):
                for i in range(j, n):
                    tabla[i, j] = (tabla[i, j-1] - tabla[i-1, j-1]) / (x_arr[i] - x_arr[i-j])
            
            # Coeficientes de la forma de Newton (diagonal de la tabla)
            coef_newton = tabla[np.arange(n), np.arange(n)]
            
            # Convertir a forma estándar (coeficientes para np.polyval)
            poly_std = np.array([0.])
            base = np.array([1.])
            
            for i in range(n):
                term = coef_newton[i] * base
                poly_std = np.pad(poly_std, (len(term) - len(poly_std), 0), 'constant')
                term = np.pad(term, (len(poly_std) - len(term), 0), 'constant')
                poly_std = poly_std + term
                base = np.convolve(base, [1, -x_arr[i]])  # (x - x_i)
            
            coeficientes = poly_std
            grado = len(coeficientes) - 1
            
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Newton')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error en el cálculo de diferencias divididas: {str(e)}",
                "coeficientes": None,
                "grado": None,
                "tabla_diferencias": None
            }
        
        # Construcción de la cadena que representa el polinomio
        try:
            poly_str = self._construir_polinomio(coeficientes, grado)
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Newton')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error al construir el polinomio: {str(e)}",
                "coeficientes": None,
                "grado": None,
                "tabla_diferencias": None
            }
        
        # Crear el gráfico
        try:
            img_uri = self._crear_grafico_newton(x_arr, y_arr, coeficientes, grado)
        except Exception as e:
            return {
                "exito": False,
                "polinomio": poly_str,
                "grafico": None,
                "mensaje": f"Polinomio calculado correctamente, pero error al crear el gráfico: {str(e)}",
                "coeficientes": coeficientes.tolist(),
                "grado": grado,
                "tabla_diferencias": tabla.tolist()
            }
        
        return {
            "exito": True,
            "polinomio": poly_str,
            "grafico": img_uri,
            "mensaje": "Interpolación exitosa usando el método de Newton (Diferencias Divididas)",
            "coeficientes": coeficientes.tolist(),
            "grado": grado,
            "tabla_diferencias": tabla.tolist(),
            "coeficientes_newton": coef_newton.tolist()
        }
    
    def _crear_grafico_newton(self, x: np.ndarray, y: np.ndarray, coeficientes: np.ndarray, grado: int) -> str:
        """
        Crea el gráfico del polinomio interpolante de Newton y los puntos.
        
        Args:
            x: Array de valores x
            y: Array de valores y
            coeficientes: Coeficientes del polinomio en forma estándar
            grado: Grado del polinomio
            
        Returns:
            String con la imagen en formato base64
        """
        plt.figure(figsize=(10, 6))
        
        # Crear valores para graficar el polinomio
        x_min, x_max = min(x) - 1, max(x) + 1
        xpol = np.linspace(x_min, x_max, 500)
        p = np.polyval(coeficientes, xpol)
        
        # Graficar puntos y polinomio
        plt.plot(x, y, 'ro', markersize=12, label='Puntos dados', zorder=5)
        plt.plot(xpol, p, 'b-', linewidth=2, label=f'Polinomio de grado {grado}')
        
        plt.title('Interpolación por Diferencias Divididas de Newton', fontsize=14, fontweight='bold')
        plt.xlabel('x', fontsize=12)
        plt.ylabel('P(x)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def lagrange(self, x: List[float], y: List[float]) -> Dict:
        """
        Implementa el método de interpolación de Lagrange.
        
        Args:
            x: Lista de valores x (coordenadas)
            y: Lista de valores y (coordenadas)
            
        Returns:
            Diccionario con el polinomio, gráfico y metadatos
        """
        # Validación: verificar que no hay valores x repetidos
        if len(set(x)) != len(x):
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Lagrange')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": "Error: Los valores de x deben ser únicos. Se encontraron valores repetidos.",
                "coeficientes": None,
                "grado": None
            }
        
        # Validación: verificar que x e y tienen el mismo tamaño
        if len(x) != len(y):
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Lagrange')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error: Las listas x e y deben tener el mismo tamaño. x tiene {len(x)} elementos y y tiene {len(y)} elementos.",
                "coeficientes": None,
                "grado": None
            }
        
        # Validación: verificar que hay al menos 2 puntos
        if len(x) < 2:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Lagrange')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": "Error: Se necesitan al menos 2 puntos para interpolación.",
                "coeficientes": None,
                "grado": None
            }
        
        try:
            n = len(x)
            x_arr = np.array(x, dtype=float)
            y_arr = np.array(y, dtype=float)
            
            # Tabla para almacenar los polinomios de Lagrange
            tabla = np.zeros((n, n))
            
            # Construir cada polinomio base de Lagrange Li(x)
            for i in range(n):
                Li = np.array([1.0])
                den = 1.0
                
                for j in range(n):
                    if j != i:
                        # (x - x_j)
                        paux = np.array([1.0, -x_arr[j]])
                        Li = np.convolve(Li, paux)
                        den *= (x_arr[i] - x_arr[j])
                
                # y_i * Li(x) / denominador
                tabla[i, :len(Li)] = y_arr[i] * Li / den
            
            # Sumar todos los polinomios base para obtener el polinomio interpolante
            coeficientes = np.sum(tabla, axis=0)
            
            # Eliminar ceros a la izquierda (por si el grado es menor a n-1)
            coeficientes = np.trim_zeros(coeficientes, 'f')
            grado = len(coeficientes) - 1
            
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Lagrange')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error en el cálculo de polinomios de Lagrange: {str(e)}",
                "coeficientes": None,
                "grado": None
            }
        
        # Construcción de la cadena que representa el polinomio
        try:
            poly_str = self._construir_polinomio(coeficientes, grado)
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Interpolación por Lagrange')
            return {
                "exito": False,
                "polinomio": None,
                "grafico": img_uri,
                "mensaje": f"Error al construir el polinomio: {str(e)}",
                "coeficientes": None,
                "grado": None
            }
        
        # Crear el gráfico
        try:
            img_uri = self._crear_grafico_lagrange(x_arr, y_arr, coeficientes, grado)
        except Exception as e:
            return {
                "exito": False,
                "polinomio": poly_str,
                "grafico": None,
                "mensaje": f"Polinomio calculado correctamente, pero error al crear el gráfico: {str(e)}",
                "coeficientes": coeficientes.tolist(),
                "grado": grado
            }
        
        return {
            "exito": True,
            "polinomio": poly_str,
            "grafico": img_uri,
            "mensaje": "Interpolación exitosa usando el método de Lagrange",
            "coeficientes": coeficientes.tolist(),
            "grado": grado
        }
    
    def _crear_grafico_lagrange(self, x: np.ndarray, y: np.ndarray, coeficientes: np.ndarray, grado: int) -> str:
        """
        Crea el gráfico del polinomio interpolante de Lagrange y los puntos.
        
        Args:
            x: Array de valores x
            y: Array de valores y
            coeficientes: Coeficientes del polinomio
            grado: Grado del polinomio
            
        Returns:
            String con la imagen en formato base64
        """
        plt.figure(figsize=(10, 6))
        
        # Crear valores para graficar el polinomio
        x_min, x_max = min(x) - 1, max(x) + 1
        xpol = np.linspace(x_min, x_max, 500)
        p = np.polyval(coeficientes, xpol)
        
        # Graficar puntos y polinomio
        plt.plot(x, y, 'r*', markersize=15, label='Puntos dados', zorder=5)
        plt.plot(xpol, p, 'b-', linewidth=2, label=f'Polinomio de grado {grado}')
        
        plt.title('Interpolación por Lagrange', fontsize=14, fontweight='bold')
        plt.xlabel('x', fontsize=12)
        plt.ylabel('P(x)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def spline_lineal(self, x: List[float], y: List[float]) -> Dict:
        """
        Implementa interpolación por Spline Lineal.
        
        Args:
            x: Lista de valores x (coordenadas)
            y: Lista de valores y (coordenadas)
            
        Returns:
            Diccionario con los polinomios por tramos, gráfico y metadatos
        """
        # Validación: verificar que no hay valores x repetidos
        if len(set(x)) != len(x):
            img_uri = self._crear_grafico_error(x, y, 'Spline Lineal')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": "Error: Los valores de x deben ser únicos. Se encontraron valores repetidos.",
                "tramos": None
            }
        
        # Validación: verificar que x e y tienen el mismo tamaño
        if len(x) != len(y):
            img_uri = self._crear_grafico_error(x, y, 'Spline Lineal')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": f"Error: Las listas x e y deben tener el mismo tamaño. x tiene {len(x)} elementos y y tiene {len(y)} elementos.",
                "tramos": None
            }
        
        # Validación: verificar que hay al menos 2 puntos
        if len(x) < 2:
            img_uri = self._crear_grafico_error(x, y, 'Spline Lineal')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": "Error: Se necesitan al menos 2 puntos para interpolación.",
                "tramos": None
            }
        
        try:
            n = len(x)
            x_arr = np.array(x, dtype=float)
            y_arr = np.array(y, dtype=float)
            
            # Construir el sistema de ecuaciones para spline lineal
            # Cada tramo tiene 2 coeficientes (m, b) en y = m*x + b
            A = np.zeros((2*(n-1), 2*(n-1)))
            b_vec = np.zeros(2*(n-1))
            
            # Primera condición: cada spline pasa por el punto inicial del tramo
            c = 0
            h = 0
            for i in range(n - 1):
                A[h, c] = x_arr[i]
                A[h, c+1] = 1
                b_vec[h] = y_arr[i]
                c += 2
                h += 1
            
            # Segunda condición: cada spline pasa por el punto final del tramo
            c = 0
            for i in range(1, n):
                A[h, c] = x_arr[i]
                A[h, c+1] = 1
                b_vec[h] = y_arr[i]
                c += 2
                h += 1
            
            # Resolver el sistema
            coef = np.linalg.solve(A, b_vec)
            tabla = coef.reshape((n-1, 2))
            
            # Construir strings de polinomios por tramo
            polinomios_str = []
            tramos_info = []
            
            for i in range(n-1):
                m, b = tabla[i]
                tramo = f"{x_arr[i]:.4f} ≤ x ≤ {x_arr[i+1]:.4f}"
                pol = f"{m:.4f}*x + {b:.4f}"
                polinomios_str.append(f"Tramo {i+1} ({tramo}): y = {pol}")
                tramos_info.append({
                    "tramo": i+1,
                    "rango": tramo,
                    "polinomio": pol,
                    "coeficientes": [m, b]
                })
            
        except np.linalg.LinAlgError as e:
            img_uri = self._crear_grafico_error(x, y, 'Spline Lineal')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": f"Error al resolver el sistema de ecuaciones: {str(e)}",
                "tramos": None
            }
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Spline Lineal')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": f"Error en el cálculo: {str(e)}",
                "tramos": None
            }
        
        # Crear el gráfico
        try:
            img_uri = self._crear_grafico_spline_lineal(x_arr, y_arr, tabla)
        except Exception as e:
            return {
                "exito": False,
                "polinomios": polinomios_str,
                "grafico": None,
                "mensaje": f"Polinomios calculados correctamente, pero error al crear el gráfico: {str(e)}",
                "tramos": tramos_info
            }
        
        return {
            "exito": True,
            "polinomios": polinomios_str,
            "grafico": img_uri,
            "mensaje": "Interpolación exitosa usando Spline Lineal",
            "tramos": tramos_info
        }
    
    def spline_cubico(self, x: List[float], y: List[float]) -> Dict:
        """
        Implementa interpolación por Spline Cúbico.
        
        Args:
            x: Lista de valores x (coordenadas)
            y: Lista de valores y (coordenadas)
            
        Returns:
            Diccionario con los polinomios por tramos, gráfico y metadatos
        """
        # Validación: verificar que no hay valores x repetidos
        if len(set(x)) != len(x):
            img_uri = self._crear_grafico_error(x, y, 'Spline Cúbico')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": "Error: Los valores de x deben ser únicos. Se encontraron valores repetidos.",
                "tramos": None
            }
        
        # Validación: verificar que x e y tienen el mismo tamaño
        if len(x) != len(y):
            img_uri = self._crear_grafico_error(x, y, 'Spline Cúbico')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": f"Error: Las listas x e y deben tener el mismo tamaño. x tiene {len(x)} elementos y y tiene {len(y)} elementos.",
                "tramos": None
            }
        
        # Validación: verificar que hay al menos 2 puntos
        if len(x) < 2:
            img_uri = self._crear_grafico_error(x, y, 'Spline Cúbico')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": "Error: Se necesitan al menos 2 puntos para interpolación.",
                "tramos": None
            }
        
        try:
            n = len(x)
            x_arr = np.array(x, dtype=float)
            y_arr = np.array(y, dtype=float)
            
            # Construir el sistema de ecuaciones para spline cúbico
            # Cada tramo tiene 4 coeficientes (a, b, c, d) en y = a*x³ + b*x² + c*x + d
            A = np.zeros((4*(n-1), 4*(n-1)))
            b_vec = np.zeros(4*(n-1))
            
            # Primera condición: cada spline pasa por el punto inicial del tramo
            c = 0
            h = 0
            for i in range(n - 1):
                A[h, c] = x_arr[i]**3
                A[h, c+1] = x_arr[i]**2
                A[h, c+2] = x_arr[i]
                A[h, c+3] = 1
                b_vec[h] = y_arr[i]
                c += 4
                h += 1
            
            # Segunda condición: cada spline pasa por el punto final del tramo
            c = 0
            for i in range(1, n):
                A[h, c] = x_arr[i]**3
                A[h, c+1] = x_arr[i]**2
                A[h, c+2] = x_arr[i]
                A[h, c+3] = 1
                b_vec[h] = y_arr[i]
                c += 4
                h += 1
            
            # Tercera condición: continuidad de la primera derivada
            c = 0
            for i in range(1, n - 1):
                A[h, c] = 3*x_arr[i]**2
                A[h, c+1] = 2*x_arr[i]
                A[h, c+2] = 1
                A[h, c+4] = -3*x_arr[i]**2
                A[h, c+5] = -2*x_arr[i]
                A[h, c+6] = -1
                b_vec[h] = 0
                c += 4
                h += 1
            
            # Cuarta condición: continuidad de la segunda derivada
            c = 0
            for i in range(1, n - 1):
                A[h, c] = 6*x_arr[i]
                A[h, c+1] = 2
                A[h, c+4] = -6*x_arr[i]
                A[h, c+5] = -2
                b_vec[h] = 0
                c += 4
                h += 1
            
            # Condiciones de frontera: segunda derivada = 0 en los extremos (spline natural)
            A[h, 0] = 6 * x_arr[0]
            A[h, 1] = 2
            b_vec[h] = 0
            h += 1
            
            A[h, -4] = 6 * x_arr[-1]
            A[h, -3] = 2
            b_vec[h] = 0
            
            # Resolver el sistema
            coef = np.linalg.solve(A, b_vec)
            tabla = coef.reshape((n-1, 4))
            
            # Construir strings de polinomios por tramo
            polinomios_str = []
            tramos_info = []
            
            for i in range(n-1):
                a, b, c, d = tabla[i]
                tramo = f"{x_arr[i]:.4f} ≤ x ≤ {x_arr[i+1]:.4f}"
                pol = f"{a:.4f}*x**3 + {b:.4f}*x**2 + {c:.4f}*x + {d:.4f}"
                polinomios_str.append(f"Tramo {i+1} ({tramo}): y = {pol}")
                tramos_info.append({
                    "tramo": i+1,
                    "rango": tramo,
                    "polinomio": pol,
                    "coeficientes": [a, b, c, d]
                })
            
        except np.linalg.LinAlgError as e:
            img_uri = self._crear_grafico_error(x, y, 'Spline Cúbico')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": f"Error al resolver el sistema de ecuaciones: {str(e)}",
                "tramos": None
            }
        except Exception as e:
            img_uri = self._crear_grafico_error(x, y, 'Spline Cúbico')
            return {
                "exito": False,
                "polinomios": None,
                "grafico": img_uri,
                "mensaje": f"Error en el cálculo: {str(e)}",
                "tramos": None
            }
        
        # Crear el gráfico
        try:
            img_uri = self._crear_grafico_spline_cubico(x_arr, y_arr, tabla)
        except Exception as e:
            return {
                "exito": False,
                "polinomios": polinomios_str,
                "grafico": None,
                "mensaje": f"Polinomios calculados correctamente, pero error al crear el gráfico: {str(e)}",
                "tramos": tramos_info
            }
        
        return {
            "exito": True,
            "polinomios": polinomios_str,
            "grafico": img_uri,
            "mensaje": "Interpolación exitosa usando Spline Cúbico (Natural)",
            "tramos": tramos_info
        }
    
    def _crear_grafico_spline_lineal(self, x: np.ndarray, y: np.ndarray, tabla: np.ndarray) -> str:
        """
        Crea el gráfico del spline lineal.
        
        Args:
            x: Array de valores x
            y: Array de valores y
            tabla: Tabla con coeficientes (m, b) para cada tramo
            
        Returns:
            String con la imagen en formato base64
        """
        plt.figure(figsize=(10, 6))
        
        # Graficar puntos
        plt.plot(x, y, 'r*', markersize=15, label='Puntos dados', zorder=5)
        
        # Graficar cada tramo lineal
        for i in range(len(tabla)):
            x_vals = np.linspace(x[i], x[i+1], 200)
            y_vals = tabla[i, 0] * x_vals + tabla[i, 1]
            plt.plot(x_vals, y_vals, linewidth=2, label=f'Tramo {i+1}')
        
        plt.title('Spline Lineal', fontsize=14, fontweight='bold')
        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def _crear_grafico_spline_cubico(self, x: np.ndarray, y: np.ndarray, tabla: np.ndarray) -> str:
        """
        Crea el gráfico del spline cúbico.
        
        Args:
            x: Array de valores x
            y: Array de valores y
            tabla: Tabla con coeficientes (a, b, c, d) para cada tramo
            
        Returns:
            String con la imagen en formato base64
        """
        plt.figure(figsize=(10, 6))
        
        # Graficar puntos
        plt.plot(x, y, 'r*', markersize=15, label='Puntos dados', zorder=5)
        
        # Graficar cada tramo cúbico
        for i in range(len(tabla)):
            x_vals = np.linspace(x[i], x[i+1], 200)
            y_vals = (tabla[i, 0]*x_vals**3 + tabla[i, 1]*x_vals**2 +
                      tabla[i, 2]*x_vals + tabla[i, 3])
            plt.plot(x_vals, y_vals, linewidth=2, label=f'Tramo {i+1}')
        
        plt.title('Spline Cúbico', fontsize=14, fontweight='bold')
        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def comparar_metodos(self, x: List[float], y: List[float], grado: int = None) -> Dict:
        """
        Ejecuta todos los métodos de interpolación y genera un informe comparativo.
        
        Args:
            x: Lista de valores x (coordenadas)
            y: Lista de valores y (coordenadas)
            grado: Grado para Vandermonde (opcional, por defecto usa len(x)-1)
            
        Returns:
            Diccionario con resultados de todos los métodos y análisis comparativo
        """
        import time
        
        # Si no se especifica grado, usar el máximo (interpolación exacta)
        if grado is None:
            grado = len(x) - 1
        
        # Validaciones básicas
        if len(set(x)) != len(x):
            return {
                "exito": False,
                "mensaje": "Error: Los valores de x deben ser únicos para realizar la comparación.",
                "resultados": None,
                "informe": None,
                "grafico_comparativo": None
            }
        
        if len(x) != len(y):
            return {
                "exito": False,
                "mensaje": f"Error: Las listas x e y deben tener el mismo tamaño.",
                "resultados": None,
                "informe": None,
                "grafico_comparativo": None
            }
        
        if len(x) < 2:
            return {
                "exito": False,
                "mensaje": "Error: Se necesitan al menos 2 puntos para interpolación.",
                "resultados": None,
                "informe": None,
                "grafico_comparativo": None
            }
        
        resultados = {}
        tiempos = {}
        
        # 1. Vandermonde
        try:
            inicio = time.time()
            resultado_vander = self.vandermonde(x, y, grado)
            fin = time.time()
            tiempos["Vandermonde"] = fin - inicio
            resultados["Vandermonde"] = {
                "exito": resultado_vander["exito"],
                "tiempo": tiempos["Vandermonde"],
                "polinomio": resultado_vander.get("polinomio", "Error"),
                "mensaje": resultado_vander["mensaje"]
            }
        except Exception as e:
            tiempos["Vandermonde"] = 0
            resultados["Vandermonde"] = {
                "exito": False,
                "tiempo": 0,
                "polinomio": "Error en ejecución",
                "mensaje": str(e)
            }
        
        # 2. Newton
        try:
            inicio = time.time()
            resultado_newton = self.newton_interpolante(x, y)
            fin = time.time()
            tiempos["Newton"] = fin - inicio
            resultados["Newton"] = {
                "exito": resultado_newton["exito"],
                "tiempo": tiempos["Newton"],
                "polinomio": resultado_newton.get("polinomio", "Error"),
                "mensaje": resultado_newton["mensaje"]
            }
        except Exception as e:
            tiempos["Newton"] = 0
            resultados["Newton"] = {
                "exito": False,
                "tiempo": 0,
                "polinomio": "Error en ejecución",
                "mensaje": str(e)
            }
        
        # 3. Lagrange
        try:
            inicio = time.time()
            resultado_lagrange = self.lagrange(x, y)
            fin = time.time()
            tiempos["Lagrange"] = fin - inicio
            resultados["Lagrange"] = {
                "exito": resultado_lagrange["exito"],
                "tiempo": tiempos["Lagrange"],
                "polinomio": resultado_lagrange.get("polinomio", "Error"),
                "mensaje": resultado_lagrange["mensaje"]
            }
        except Exception as e:
            tiempos["Lagrange"] = 0
            resultados["Lagrange"] = {
                "exito": False,
                "tiempo": 0,
                "polinomio": "Error en ejecución",
                "mensaje": str(e)
            }
        
        # 4. Spline Lineal
        try:
            inicio = time.time()
            resultado_spline_lin = self.spline_lineal(x, y)
            fin = time.time()
            tiempos["Spline Lineal"] = fin - inicio
            resultados["Spline Lineal"] = {
                "exito": resultado_spline_lin["exito"],
                "tiempo": tiempos["Spline Lineal"],
                "polinomio": f"{len(resultado_spline_lin.get('polinomios', []))} tramos lineales" if resultado_spline_lin["exito"] else "Error",
                "mensaje": resultado_spline_lin["mensaje"],
                "num_tramos": len(resultado_spline_lin.get("tramos", []))
            }
        except Exception as e:
            tiempos["Spline Lineal"] = 0
            resultados["Spline Lineal"] = {
                "exito": False,
                "tiempo": 0,
                "polinomio": "Error en ejecución",
                "mensaje": str(e),
                "num_tramos": 0
            }
        
        # 5. Spline Cúbico
        try:
            inicio = time.time()
            resultado_spline_cub = self.spline_cubico(x, y)
            fin = time.time()
            tiempos["Spline Cúbico"] = fin - inicio
            resultados["Spline Cúbico"] = {
                "exito": resultado_spline_cub["exito"],
                "tiempo": tiempos["Spline Cúbico"],
                "polinomio": f"{len(resultado_spline_cub.get('polinomios', []))} tramos cúbicos" if resultado_spline_cub["exito"] else "Error",
                "mensaje": resultado_spline_cub["mensaje"],
                "num_tramos": len(resultado_spline_cub.get("tramos", []))
            }
        except Exception as e:
            tiempos["Spline Cúbico"] = 0
            resultados["Spline Cúbico"] = {
                "exito": False,
                "tiempo": 0,
                "polinomio": "Error en ejecución",
                "mensaje": str(e),
                "num_tramos": 0
            }
        
        # Generar análisis comparativo
        metodos_exitosos = {k: v for k, v in tiempos.items() if resultados[k]["exito"] and v > 0}
        
        if not metodos_exitosos:
            return {
                "exito": False,
                "mensaje": "Ningún método se ejecutó correctamente.",
                "resultados": resultados,
                "informe": None,
                "grafico_comparativo": None
            }
        
        # Encontrar el más rápido
        metodo_mas_rapido = min(metodos_exitosos, key=metodos_exitosos.get)
        tiempo_mas_rapido = metodos_exitosos[metodo_mas_rapido]
        
        # Encontrar el más lento
        metodo_mas_lento = max(metodos_exitosos, key=metodos_exitosos.get)
        tiempo_mas_lento = metodos_exitosos[metodo_mas_lento]
        
        # Generar análisis y recomendaciones
        analisis = self._generar_analisis_comparativo(
            x, y, grado, resultados, metodos_exitosos, 
            metodo_mas_rapido, metodo_mas_lento
        )
        
        # Crear gráfico comparativo de tiempos
        try:
            grafico_tiempos = self._crear_grafico_comparativo_tiempos(metodos_exitosos)
        except:
            grafico_tiempos = None
        
        # Crear gráfico visual comparativo
        try:
            grafico_visual = self._crear_grafico_comparativo_visual(
                x, y, resultado_vander, resultado_newton, resultado_lagrange,
                resultado_spline_lin, resultado_spline_cub
            )
        except:
            grafico_visual = None
        
        return {
            "exito": True,
            "mensaje": f"Comparación completada. Se ejecutaron {len(metodos_exitosos)} de 5 métodos correctamente.",
            "resultados": resultados,
            "informe": analisis,
            "grafico_comparativo_tiempos": grafico_tiempos,
            "grafico_comparativo_visual": grafico_visual,
            "metodo_mas_rapido": metodo_mas_rapido,
            "tiempo_mas_rapido": tiempo_mas_rapido,
            "total_metodos_exitosos": len(metodos_exitosos)
        }
    
    def _generar_analisis_comparativo(self, x, y, grado, resultados, metodos_exitosos, 
                                      metodo_mas_rapido, metodo_mas_lento) -> Dict:
        """Genera un análisis detallado comparando los métodos."""
        n = len(x)
        
        analisis = {
            "resumen": f"Se interpolaron {n} puntos usando {len(metodos_exitosos)} métodos diferentes.",
            "metodo_mas_rapido": metodo_mas_rapido,
            "metodo_mas_lento": metodo_mas_lento,
            "diferencia_tiempo": metodos_exitosos[metodo_mas_lento] - metodos_exitosos[metodo_mas_rapido],
            "recomendacion": "",
            "caracteristicas": {}
        }
        
        # Análisis de características
        if "Vandermonde" in metodos_exitosos:
            analisis["caracteristicas"]["Vandermonde"] = {
                "ventajas": ["Implementación directa", "Resuelve sistema lineal"],
                "desventajas": ["Inestable para grados altos", "Matriz mal condicionada"],
                "complejidad": "O(n³)",
                "mejor_uso": "Pocos puntos (n < 10) y grados bajos"
            }
        
        if "Newton" in metodos_exitosos:
            analisis["caracteristicas"]["Newton"] = {
                "ventajas": ["Estable numéricamente", "Eficiente", "Incremental"],
                "desventajas": ["Requiere ordenamiento", "Tabla de diferencias"],
                "complejidad": "O(n²)",
                "mejor_uso": "Interpolación general, datos ordenados"
            }
        
        if "Lagrange" in metodos_exitosos:
            analisis["caracteristicas"]["Lagrange"] = {
                "ventajas": ["Conceptualmente simple", "No requiere resolver sistemas", "Estable"],
                "desventajas": ["Costoso para evaluación múltiple", "No es incremental"],
                "complejidad": "O(n²) para construcción, O(n²) para evaluación",
                "mejor_uso": "Pocas evaluaciones, fines didácticos"
            }
        
        if "Spline Lineal" in metodos_exitosos:
            analisis["caracteristicas"]["Spline Lineal"] = {
                "ventajas": ["Muy rápido", "Simple", "No oscila"],
                "desventajas": ["No suave (no derivable en nodos)", "Poco preciso"],
                "complejidad": "O(n)",
                "mejor_uso": "Datos con cambios abruptos, velocidad prioritaria"
            }
        
        if "Spline Cúbico" in metodos_exitosos:
            analisis["caracteristicas"]["Spline Cúbico"] = {
                "ventajas": ["Muy suave (C²)", "Estable", "No oscila", "Profesional"],
                "desventajas": ["Más costoso que lineal", "Requiere resolver sistema"],
                "complejidad": "O(n)",
                "mejor_uso": "Gráficos, CAD, datos suaves, producción"
            }
        
        # Generar recomendación basada en el contexto
        if n <= 4:
            analisis["recomendacion"] = (
                f"Con {n} puntos, cualquier método polinomial (Vandermonde, Newton, Lagrange) es adecuado. "
                f"Newton es el más equilibrado en velocidad y estabilidad. "
                f"Spline Cúbico ofrece la curva más suave."
            )
        elif n <= 8:
            analisis["recomendacion"] = (
                f"Con {n} puntos, se recomienda Newton o Lagrange para interpolación polinomial exacta. "
                f"Para curvas suaves, Spline Cúbico es la mejor opción. "
                f"Evitar Vandermonde por posibles problemas numéricos."
            )
        else:
            analisis["recomendacion"] = (
                f"Con {n} puntos, los métodos por tramos (Splines) son superiores. "
                f"Spline Cúbico ofrece el mejor balance entre suavidad y estabilidad. "
                f"Los métodos polinomiales pueden presentar oscilaciones (fenómeno de Runge)."
            )
        
        # Agregar análisis específico del caso
        if metodo_mas_rapido == "Spline Lineal":
            analisis["nota_velocidad"] = "Spline Lineal fue el más rápido debido a su simplicidad (conexiones lineales)."
        elif metodo_mas_rapido == "Newton":
            analisis["nota_velocidad"] = "Newton fue el más rápido gracias a su eficiencia algorítmica (diferencias divididas)."
        elif metodo_mas_rapido == "Spline Cúbico":
            analisis["nota_velocidad"] = "Spline Cúbico fue sorprendentemente rápido considerando su suavidad C²."
        
        return analisis
    
    def _crear_grafico_comparativo_tiempos(self, tiempos_dict: Dict[str, float]) -> str:
        """Crea un gráfico de barras comparando los tiempos de ejecución."""
        plt.figure(figsize=(10, 6))
        
        metodos = list(tiempos_dict.keys())
        tiempos = [t * 1000 for t in tiempos_dict.values()]  # Convertir a milisegundos
        
        colores = ['#dc3545', '#28a745', '#007bff', '#ffc107', '#6c757d']
        
        barras = plt.bar(metodos, tiempos, color=colores[:len(metodos)], alpha=0.7, edgecolor='black')
        
        # Agregar valores sobre las barras
        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2., altura,
                    f'{altura:.3f} ms',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title('Comparación de Tiempos de Ejecución', fontsize=14, fontweight='bold')
        plt.xlabel('Método de Interpolación', fontsize=12)
        plt.ylabel('Tiempo (milisegundos)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def _crear_grafico_comparativo_visual(self, x, y, res_vander, res_newton, res_lagrange,
                                         res_spline_lin, res_spline_cub) -> str:
        """Crea un gráfico visual comparando todas las curvas de interpolación."""
        plt.figure(figsize=(14, 8))
        
        x_arr = np.array(x)
        y_arr = np.array(y)
        
        # Puntos originales
        plt.plot(x, y, 'ko', markersize=10, label='Puntos Datos', zorder=10)
        
        # Rango para graficar
        x_min, x_max = min(x), max(x)
        x_plot = np.linspace(x_min, x_max, 300)
        
        # Vandermonde (si exitoso)
        if res_vander["exito"] and res_vander.get("coeficientes"):
            coef = res_vander["coeficientes"]
            y_vander = np.polyval(coef[::-1], x_plot)
            plt.plot(x_plot, y_vander, 'r-', linewidth=2, label='Vandermonde', alpha=0.7)
        
        # Newton y Lagrange producen el mismo polinomio, así que solo graficamos uno
        if res_newton["exito"] and res_newton.get("coeficientes"):
            coef = res_newton["coeficientes"]
            y_newton = np.polyval(coef[::-1], x_plot)
            plt.plot(x_plot, y_newton, 'g--', linewidth=2, label='Newton/Lagrange', alpha=0.7)
        elif res_lagrange["exito"] and res_lagrange.get("coeficientes"):
            coef = res_lagrange["coeficientes"]
            y_lagrange = np.polyval(coef[::-1], x_plot)
            plt.plot(x_plot, y_lagrange, 'b--', linewidth=2, label='Lagrange', alpha=0.7)
        
        # Spline Lineal
        if res_spline_lin["exito"] and res_spline_lin.get("tramos"):
            for tramo in res_spline_lin["tramos"]:
                coefs = tramo["coeficientes"]  # [m, b]
                idx = tramo["tramo"] - 1
                if idx < len(x) - 1:
                    x_tramo = np.linspace(x_arr[idx], x_arr[idx+1], 50)
                    y_tramo = coefs[0] * x_tramo + coefs[1]
                    if idx == 0:
                        plt.plot(x_tramo, y_tramo, 'orange', linewidth=2, label='Spline Lineal')
                    else:
                        plt.plot(x_tramo, y_tramo, 'orange', linewidth=2)
        
        # Spline Cúbico
        if res_spline_cub["exito"] and res_spline_cub.get("tramos"):
            for tramo in res_spline_cub["tramos"]:
                coefs = tramo["coeficientes"]  # [a, b, c, d]
                idx = tramo["tramo"] - 1
                if idx < len(x) - 1:
                    x_tramo = np.linspace(x_arr[idx], x_arr[idx+1], 50)
                    y_tramo = coefs[0]*x_tramo**3 + coefs[1]*x_tramo**2 + coefs[2]*x_tramo + coefs[3]
                    if idx == 0:
                        plt.plot(x_tramo, y_tramo, 'm-', linewidth=2.5, label='Spline Cúbico')
                    else:
                        plt.plot(x_tramo, y_tramo, 'm-', linewidth=2.5)
        
        plt.title('Comparación Visual de Métodos de Interpolación', fontsize=14, fontweight='bold')
        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)
        plt.legend(fontsize=10, loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri

