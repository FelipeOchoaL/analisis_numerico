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

