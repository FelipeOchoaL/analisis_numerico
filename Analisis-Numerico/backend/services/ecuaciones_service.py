import base64
import io
import math
from typing import Dict, List, Any, Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from models.schemas import IteracionData, MetodoResponse

class EcuacionesService:
    
    def _evaluar_funcion(self, funcion: str, x: float) -> float:
        """Evalúa una función string de manera segura"""
        try:
            # Preparar el namespace para eval
            namespace = {
                'x': x,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'exp': math.exp,
                'log10': math.log10,
                'ln': math.log,
                'sqrt': math.sqrt,
                'pi': math.pi,
                'e': math.e,
                'abs': abs,
                'pow': pow,
                'math': math,
                'np': np
            }
            
            # Reemplazar ^ por **
            funcion = funcion.replace('^', '**')
            
            return eval(funcion, {"__builtins__": {}}, namespace)
        except Exception as e:
            raise ValueError(f"Error evaluando función '{funcion}' en x={x}: {str(e)}")
    
    def _calcular_error(self, x_actual: float, x_anterior: float, tipo_error: str = "absoluto") -> float:
        """
        Calcula el error según el tipo especificado.
        
        Args:
            x_actual: Valor actual de x
            x_anterior: Valor anterior de x
            tipo_error: 'absoluto' o 'relativo'
            
        Returns:
            El error calculado
        """
        if tipo_error == "relativo":
            # Error relativo: |x_actual - x_anterior| / |x_actual|
            if abs(x_actual) < 1e-12:
                # Si x_actual es muy pequeño, usar error absoluto
                return abs(x_actual - x_anterior)
            return abs(x_actual - x_anterior) / abs(x_actual)
        else:
            # Error absoluto: |x_actual - x_anterior|
            return abs(x_actual - x_anterior)

    def _formatear_valor_tabla(self, valor: Any) -> Any:
        if isinstance(valor, (int, float, np.floating)):
            if math.isnan(valor) or math.isinf(valor):
                return ""
            abs_val = abs(valor)
            if abs_val != 0 and (abs_val < 1e-4 or abs_val >= 1e5):
                return f"{valor:.6e}"
            return f"{valor:.10f}".rstrip("0").rstrip(".")
        return valor if valor is not None else ""

    def _iteraciones_a_tabla_html(
        self,
        iteraciones: List[IteracionData],
        orden_columnas: Iterable[str] | None = None,
        nombre_columnas: Dict[str, str] | None = None,
    ) -> str | None:
        if not iteraciones:
            return None

        filas = []
        for iteracion in iteraciones:
            fila = {"Iteración": iteracion.iteracion}
            for clave, valor in iteracion.valores.items():
                fila[clave] = valor
            if iteracion.error is not None:
                fila["Error"] = iteracion.error
            if iteracion.observacion:
                fila["Observación"] = iteracion.observacion
            filas.append(fila)

        df = pd.DataFrame(filas)

        if nombre_columnas:
            df = df.rename(columns=nombre_columnas)

        if orden_columnas:
            orden = [col for col in orden_columnas if col in df.columns]
            orden.extend([col for col in df.columns if col not in orden])
            df = df[orden]

        df = df.applymap(self._formatear_valor_tabla)

        return df.to_html(
            index=False,
            escape=False,
            classes=("table table-striped table-hover table-sm text-center"),
            justify="center",
        )

    def _extraer_puntos(self, iteraciones: List[IteracionData], claves: Iterable[str]) -> List[float]:
        valores = []
        for iteracion in iteraciones:
            for clave in claves:
                valor = iteracion.valores.get(clave)
                if isinstance(valor, (int, float, np.floating)) and np.isfinite(valor):
                    valores.append(float(valor))
        return valores

    def _generar_grafico_funcion(
        self,
        funcion: str,
        puntos: List[float],
        titulo: str,
        raiz: float | None = None,
    ) -> str | None:
        if not puntos:
            # Si no hay puntos, intentamos un rango genérico
            puntos = [-5.0, 5.0]

        xmin, xmax = min(puntos), max(puntos)

        if math.isclose(xmin, xmax, rel_tol=1e-9, abs_tol=1e-9):
            rango = abs(xmin) if xmin != 0 else 1.0
            xmin -= rango
            xmax += rango
        else:
            margen = 0.2 * (xmax - xmin)
            if margen == 0:
                margen = max(1.0, abs(xmin), abs(xmax)) * 0.2
            xmin -= margen
            xmax += margen

        x_vals = np.linspace(xmin, xmax, 400)
        y_vals = []
        todo_nan = True
        for x in x_vals:
            try:
                valor = self._evaluar_funcion(funcion, float(x))
                y_vals.append(valor)
                if np.isfinite(valor):
                    todo_nan = False
            except Exception:
                y_vals.append(np.nan)

        if todo_nan:
            return None

        plt.figure(figsize=(7, 4))
        plt.plot(x_vals, y_vals, label=f"f(x) = {funcion}", color="#1f77b4")
        plt.axhline(0, color="#333333", linewidth=1)

        if raiz is not None and np.isfinite(raiz):
            try:
                plt.scatter([raiz], [self._evaluar_funcion(funcion, raiz)], color="#d62728", zorder=5)
                plt.scatter([raiz], [0], color="#2ca02c", zorder=6, label=f"Raíz ≈ {raiz:.6f}")
            except Exception:
                plt.scatter([raiz], [0], color="#2ca02c", zorder=5, label=f"Raíz ≈ {raiz:.6f}")

        plt.title(titulo)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(loc="best")

        buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format="png", dpi=150)
        plt.close()
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/png;base64,{imagen_base64}"

    def _construir_respuesta_metodo(
        self,
        *,
        exito: bool,
        resultado: float | None,
        iteraciones: List[IteracionData],
        mensaje: str,
        funcion: str | None = None,
        claves_grafica: Iterable[str] | None = None,
        titulo_grafica: str = "Gráfico del método",
        ayuda: str | None = None,
    ) -> Dict[str, Any]:
        tabla_html = self._iteraciones_a_tabla_html(iteraciones)

        grafico = None
        if funcion and claves_grafica:
            try:
                puntos_grafica = self._extraer_puntos(iteraciones, claves_grafica)
                grafico = self._generar_grafico_funcion(
                    funcion,
                    puntos_grafica,
                    titulo_grafica,
                    raiz=resultado if exito else None,
                )
            except Exception:
                grafico = None

        respuesta = MetodoResponse(
            exito=exito,
            resultado=resultado,
            iteraciones=iteraciones,
            mensaje=mensaje
        ).dict()

        respuesta["tabla_html"] = tabla_html
        respuesta["grafico"] = grafico
        if ayuda:
            respuesta["ayuda"] = ayuda

        return respuesta
    
    def biseccion(self, xi: float, xs: float, tolerancia: float, niter: int, funcion: str, tipo_error: str = "absoluto") -> Dict[str, Any]:
        """Implementa el método de bisección basado en el código original"""
        iteraciones = []
        
        # Evaluación inicial
        fi = self._evaluar_funcion(funcion, xi)
        fs = self._evaluar_funcion(funcion, xs)
        
        ayuda_general = (
            "Recuerde que el intervalo inicial debe cumplir f(a)·f(b) < 0. "
            "Use la variable x y potencias con ** (ej: x**3)."
        )

        if fi == 0:
            iteraciones = [
                IteracionData(
                    iteracion=0,
                    valores={"xi": xi, "xs": xs, "xm": xi, "fi": fi, "fs": fs},
                    observacion=f"{xi} es raíz de f(x)"
                )
            ]
            return self._construir_respuesta_metodo(
                exito=True,
                resultado=xi,
                iteraciones=iteraciones,
                mensaje=f"{xi} es raíz de f(x)",
                funcion=funcion,
                claves_grafica=["xi", "xs", "xm"],
                titulo_grafica="Método de Bisección",
                ayuda=ayuda_general,
            )
            
        if fs == 0:
            iteraciones = [
                IteracionData(
                    iteracion=0,
                    valores={"xi": xi, "xs": xs, "xm": xs, "fi": fi, "fs": fs},
                    observacion=f"{xs} es raíz de f(x)"
                )
            ]
            return self._construir_respuesta_metodo(
                exito=True,
                resultado=xs,
                iteraciones=iteraciones,
                mensaje=f"{xs} es raíz de f(x)",
                funcion=funcion,
                claves_grafica=["xi", "xs", "xm"],
                titulo_grafica="Método de Bisección",
                ayuda=ayuda_general,
            )
            
        if fs * fi >= 0:
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=[],
                mensaje="El intervalo es inadecuado. Debe existir cambio de signo en f(a) y f(b).",
                funcion=funcion,
                claves_grafica=None,
                titulo_grafica="Método de Bisección",
                ayuda=(
                    "Verifique que f(a) y f(b) tengan signos opuestos. Puede usar la búsqueda incremental "
                    "para localizar un intervalo adecuado."
                ),
            )
        
        # Algoritmo de bisección - siguiendo la estructura original
        c = 0
        fm = []
        E = [100]  # Error inicial
        
        # Primera iteración
        xm = (xi + xs) / 2
        fe = self._evaluar_funcion(funcion, xm)
        fm.append(fe)
        
        iteraciones.append(IteracionData(
            iteracion=c + 1,
            valores={
                "xi": xi,
                "xs": xs,
                "xm": xm,
                "fi": fi,
                "fs": fs,
                "fm": fe,
                "error_absoluto": E[c],
                "error_relativo": E[c]
            },
            error=E[c],
            observacion="Primera iteración"
        ))
        
        while E[c] > tolerancia and fe != 0 and c < niter:
            if fi * fe < 0:
                xs = xm
                fs = self._evaluar_funcion(funcion, xs)
            else:
                xi = xm
                fi = self._evaluar_funcion(funcion, xi)
            
            xa = xm
            xm = (xi + xs) / 2
            fe = self._evaluar_funcion(funcion, xm)
            fm.append(fe)
            
            # Calcular ambos tipos de error
            error_absoluto = abs(xm - xa)
            error_relativo = abs(xm - xa) / abs(xm) if abs(xm) > 1e-12 else error_absoluto
            
            # Usar el error seleccionado para convergencia
            error = self._calcular_error(xm, xa, tipo_error)
            E.append(error)
            c = c + 1
            
            iteraciones.append(IteracionData(
                iteracion=c + 1,
                valores={
                    "xi": xi,
                    "xs": xs,
                    "xm": xm,
                    "fi": fi,
                    "fs": fs,
                    "fm": fe,
                    "error_absoluto": error_absoluto,
                    "error_relativo": error_relativo
                },
                error=error,
                observacion="Bisección"
            ))
        
        # Determinar resultado final
        if fe == 0:
            mensaje = f"{xm} es raíz de f(x)"
            exito = True
        elif E[c] < tolerancia:
            mensaje = f"{xm} es una aproximación de una raíz de f(x) con tolerancia {tolerancia}"
            exito = True
        else:
            mensaje = f"Fracaso en {niter} iteraciones"
            exito = False
            
        return self._construir_respuesta_metodo(
            exito=exito,
            resultado=xm,
            iteraciones=iteraciones,
            mensaje=mensaje,
            funcion=funcion,
            claves_grafica=["xi", "xs", "xm"],
            titulo_grafica="Método de Bisección",
            ayuda=ayuda_general,
        )
    
    def punto_fijo(self, x0: float, tolerancia: float, niter: int, 
                   funcion_f: str, funcion_g: str, tipo_error: str = "absoluto") -> Dict[str, Any]:
        """Implementa el método de punto fijo basado en el código original"""
        iteraciones = []
        
        x_actual = x0
        error = float('inf')
        i = 0
        
        # Primera evaluación
        f_actual = self._evaluar_funcion(funcion_f, x_actual)
        
        iteraciones.append(IteracionData(
            iteracion=i,
            valores={
                "xi": x_actual,
                "f_xi": f_actual,
                "error_absoluto": "",
                "error_relativo": ""
            },
            error=None,
            observacion="Valor inicial"
        ))
        
        # Algoritmo de punto fijo
        while error > tolerancia and abs(f_actual) > tolerancia and i < niter:
            x_anterior = x_actual
            x_actual = self._evaluar_funcion(funcion_g, x_anterior)
            f_actual = self._evaluar_funcion(funcion_f, x_actual)
            i += 1
            
            # Calcular ambos tipos de error
            error_absoluto = abs(x_actual - x_anterior)
            error_relativo = abs(x_actual - x_anterior) / abs(x_actual) if abs(x_actual) > 1e-12 else error_absoluto
            
            # Usar el error seleccionado para convergencia
            error = self._calcular_error(x_actual, x_anterior, tipo_error)
            
            iteraciones.append(IteracionData(
                iteracion=i,
                valores={
                    "xi": x_actual,
                    "f_xi": f_actual,
                    "g_xi_anterior": self._evaluar_funcion(funcion_g, x_anterior),
                    "error_absoluto": error_absoluto,
                    "error_relativo": error_relativo
                },
                error=error,
                observacion="Iteración punto fijo"
            ))
        
        if abs(f_actual) <= tolerancia:
            mensaje = f"Raíz encontrada: x = {x_actual:.6f}"
            exito = True
        elif error <= tolerancia:
            mensaje = f"Punto fijo encontrado: x = {x_actual:.6f}"
            exito = True
        else:
            mensaje = f"Método falló después de {niter} iteraciones"
            exito = False

        return self._construir_respuesta_metodo(
            exito=exito,
            resultado=x_actual,
            iteraciones=iteraciones,
            mensaje=mensaje,
            funcion=funcion_f,
            claves_grafica=["xi"],
            titulo_grafica="Método de Punto Fijo",
            ayuda=(
                "Verifique que la función g(x) cumpla |g'(x)| < 1 alrededor de la raíz "
                "para garantizar convergencia. Use la variable x y funciones disponibles (sin, cos, exp)."
            ),
        )
    
    def regla_falsa(self, x0: float, x1: float, tolerancia: float, 
                    niter: int, funcion: str, tipo_error: str = "absoluto") -> Dict[str, Any]:
        """Implementa el método de regla falsa basado en el código original"""
        iteraciones = []
        
        # Evaluación inicial
        f0 = self._evaluar_funcion(funcion, x0)
        f1 = self._evaluar_funcion(funcion, x1)
        
        print(f"Evaluación inicial:")
        print(f"f({x0}) = {f0}")
        print(f"f({x1}) = {f1}")
        print(f"f(X0) * f(X1) = {f0 * f1}")
        
        # Verificaciones iniciales según el algoritmo original
        ayuda_rf = (
            "Asegúrese de que f(x0) y f(x1) tengan signos opuestos. Use la variable x y funciones como sin, cos, exp."
        )

        if f0 == 0:
            iteraciones = [
                IteracionData(
                    iteracion=0,
                    valores={"x0": x0, "x1": x1, "x2": x0, "f0": f0, "f1": f1, "f2": f0, "error_absoluto": 0, "error_relativo": 0},
                    error=0,
                    observacion="Raíz exacta en X0"
                )
            ]
            return self._construir_respuesta_metodo(
                exito=True,
                resultado=x0,
                iteraciones=iteraciones,
                mensaje=f"{x0} es raíz exacta de f(x)",
                funcion=funcion,
                claves_grafica=["x0", "x1", "x2"],
                titulo_grafica="Método de Regla Falsa",
                ayuda=ayuda_rf,
            )
            
        if f1 == 0:
            iteraciones = [
                IteracionData(
                    iteracion=0,
                    valores={"x0": x0, "x1": x1, "x2": x1, "f0": f0, "f1": f1, "f2": f1, "error_absoluto": 0, "error_relativo": 0},
                    error=0,
                    observacion="Raíz exacta en X1"
                )
            ]
            return self._construir_respuesta_metodo(
                exito=True,
                resultado=x1,
                iteraciones=iteraciones,
                mensaje=f"{x1} es raíz exacta de f(x)",
                funcion=funcion,
                claves_grafica=["x0", "x1", "x2"],
                titulo_grafica="Método de Regla Falsa",
                ayuda=ayuda_rf,
            )
            
        if f0 * f1 >= 0:
            iteraciones = [
                IteracionData(
                    iteracion=0,
                    valores={"x0": x0, "x1": x1, "f0": f0, "f1": f1, "error_absoluto": "", "error_relativo": ""},
                    observacion="Intervalo inadecuado"
                )
            ]
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=iteraciones,
                mensaje="Error: No hay cambio de signo en el intervalo",
                funcion=funcion,
                claves_grafica=["x0", "x1"],
                titulo_grafica="Método de Regla Falsa",
                ayuda=ayuda_rf,
            )
        
        # Variables para el método
        x0_actual = x0
        x1_actual = x1
        f0_actual = f0
        f1_actual = f1
        error = float('inf')
        c = 0
        
        while error > tolerancia and c < niter:
            # Calcular X2 usando la fórmula de interpolación lineal
            if abs(f1_actual - f0_actual) < 1e-12:
                break
                
            x2 = x0_actual - f0_actual * (x1_actual - x0_actual) / (f1_actual - f0_actual)
            f2 = self._evaluar_funcion(funcion, x2)
            
            # Calcular ambos tipos de error
            if c > 0:
                error_absoluto = abs(x2 - x2_anterior)
                error_relativo = abs(x2 - x2_anterior) / abs(x2) if abs(x2) > 1e-12 else error_absoluto
                error = self._calcular_error(x2, x2_anterior, tipo_error)
            else:
                error_absoluto = abs(x2 - x0_actual)
                error_relativo = abs(x2 - x0_actual) / abs(x2) if abs(x2) > 1e-12 else error_absoluto
                error = self._calcular_error(x2, x0_actual, tipo_error)
            
            # Determinar observación
            observacion = ""
            if f2 == 0:
                observacion = "Raíz exacta encontrada"
            elif f0_actual * f2 < 0:
                observacion = "Raíz en [X0, X2] → X1 = X2"
            elif f2 * f1_actual < 0:
                observacion = "Raíz en [X2, X1] → X0 = X2"
            
            iteraciones.append(IteracionData(
                iteracion=c + 1,
                valores={
                    "x0": x0_actual,
                    "x1": x1_actual,
                    "x2": x2,
                    "f0": f0_actual,
                    "f1": f1_actual,
                    "f2": f2,
                    "error_absoluto": error_absoluto,
                    "error_relativo": error_relativo
                },
                error=error,
                observacion=observacion
            ))
            
            if f2 == 0:
                iteraciones.append(IteracionData(
                    iteracion=c + 1,
                    valores={
                        "x0": x0_actual,
                        "x1": x1_actual,
                        "x2": x2,
                        "f0": f0_actual,
                        "f1": f1_actual,
                        "f2": f2,
                        "error_absoluto": error_absoluto,
                        "error_relativo": error_relativo
                    },
                    error=error,
                    observacion="Raíz exacta encontrada"
                ))
                return self._construir_respuesta_metodo(
                    exito=True,
                    resultado=x2,
                    iteraciones=iteraciones,
                    mensaje=f"¡Raíz exacta encontrada! X2 = {x2}",
                    funcion=funcion,
                    claves_grafica=["x0", "x1", "x2"],
                    titulo_grafica="Método de Regla Falsa",
                    ayuda=ayuda_rf,
                )
                
            # Actualizar intervalo
            if f0_actual * f2 < 0:
                x1_actual = x2
                f1_actual = f2
            elif f2 * f1_actual < 0:
                x0_actual = x2
                f0_actual = f2
            else:
                break
                
            x2_anterior = x2
            c += 1
        
        if c >= niter:
            mensaje = f"Método terminó por límite de iteraciones ({niter})"
            exito = False
        elif error <= tolerancia:
            mensaje = f"Convergencia alcanzada! Raíz aproximada: X = {x2}"
            exito = True
        else:
            mensaje = "Error: Pérdida de cambio de signo"
            exito = False
            
        return self._construir_respuesta_metodo(
            exito=exito,
            resultado=x2 if 'x2' in locals() else None,
            iteraciones=iteraciones,
            mensaje=mensaje,
            funcion=funcion,
            claves_grafica=["x0", "x1", "x2"],
            titulo_grafica="Método de Regla Falsa",
            ayuda=ayuda_rf,
        )
    
    def busqueda_incremental(self, x0: float, delta: float, niter: int, 
                           funcion: str) -> Dict[str, Any]:
        """Implementa la búsqueda incremental basada en el código original"""
        iteraciones = []
        
        x = x0
        f0 = self._evaluar_funcion(funcion, x)
        
        if f0 == 0:
            iteraciones.append(IteracionData(
                iteracion=0,
                valores={"x0": x0, "f0": f0, "error_absoluto": "", "error_relativo": ""},
                observacion="Raíz exacta encontrada"
            ))
            return self._construir_respuesta_metodo(
                exito=True,
                resultado=x0,
                iteraciones=iteraciones,
                mensaje=f"{x0} es raíz de f(x)",
                funcion=funcion,
                claves_grafica=["x0"],
                titulo_grafica="Búsqueda Incremental",
                ayuda=(
                    "Utilice este método para encontrar un intervalo adecuado antes de aplicar Bisección o Regla Falsa. "
                    "Ingrese incrementos positivos y un número de iteraciones razonable."
                ),
            )
        
        x1 = x0 + delta
        c = 1
        f1 = self._evaluar_funcion(funcion, x1)
        
        # Registrar la primera iteración
        iteraciones.append(IteracionData(
            iteracion=c,
            valores={
                "x0": x0,
                "x1": x1,
                "f0": f0,
                "f1": f1,
                "producto": f0 * f1,
                "error_absoluto": "",
                "error_relativo": ""
            },
            observacion="Mismo signo" if f0 * f1 > 0 else "Cambio de signo"
        ))
        
        while f0 * f1 > 0 and c < niter:
            x0 = x1
            f0 = f1
            x1 = x0 + delta
            f1 = self._evaluar_funcion(funcion, x1)
            c = c + 1
            
            iteraciones.append(IteracionData(
                iteracion=c,
                valores={
                    "x0": x0,
                    "x1": x1,
                    "f0": f0,
                    "f1": f1,
                    "producto": f0 * f1,
                    "error_absoluto": "",
                    "error_relativo": ""
                },
                observacion="Mismo signo" if f0 * f1 > 0 else "Cambio de signo"
            ))
        
        if f1 == 0:
            mensaje = f"{x1} es raíz de f(x)"
            exito = True
            resultado = x1
        elif f0 * f1 < 0:
            mensaje = f"Existe una raíz de f(x) entre {x0} y {x1}"
            exito = True
            resultado = (x0 + x1) / 2  # Punto medio como aproximación
        else:
            mensaje = f"Fracaso en {niter} iteraciones"
            exito = False
            resultado = None
            
        return self._construir_respuesta_metodo(
            exito=exito,
            resultado=resultado,
            iteraciones=iteraciones,
            mensaje=mensaje,
            funcion=funcion,
            claves_grafica=["x0", "x1"],
            titulo_grafica="Búsqueda Incremental",
            ayuda=(
                "Utilice este método para encontrar un intervalo adecuado antes de aplicar Bisección o Regla Falsa. "
                "Ingrese incrementos positivos y un número de iteraciones razonable."
            ),
        )
    
    def newton_raphson(self, x0: float, tolerancia: float, niter: int, 
                      funcion_f: str, funcion_df: str, incluir_error: bool = True,
                      tipo_error: str = "absoluto", tipo_precision: str = "decimales", precision: int = 6) -> Dict[str, Any]:
        """Implementa el método de Newton-Raphson según el procedimiento de las imágenes"""
        iteraciones = []
        
        xi = x0
        
        # Verificar que la derivada no sea cero en x0
        try:
            dfx0 = self._evaluar_funcion(funcion_df, x0)
            if abs(dfx0) < 1e-12:
                iteraciones.append(IteracionData(
                    iteracion=0,
                    valores={
                        "xi": x0,
                        "fxi": self._evaluar_funcion(funcion_f, x0),
                        "dfxi": dfx0,
                        "error_absoluto": "",
                        "error_relativo": ""
                    },
                    observacion="Derivada casi nula en el punto inicial"
                ))
                ayuda_newton = (
                    "Seleccione un valor inicial donde la derivada no sea cero y la función sea suave. "
                    "Revise las derivadas simbólicas para confirmar la elección."
                )
                return self._construir_respuesta_metodo(
                    exito=False,
                    resultado=None,
                    iteraciones=iteraciones,
                    mensaje=f"Error: f'({x0}) ≈ 0. El método no converge con este valor inicial.",
                    funcion=funcion_f,
                    claves_grafica=["xi"],
                    titulo_grafica="Método de Newton-Raphson",
                    ayuda=ayuda_newton,
                )
        except Exception as e:
            ayuda_newton = (
                "Verifique la sintaxis de la derivada f'(x). Recuerde usar la variable x y operadores como ** para potencias."
            )
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=[],
                mensaje=f"Error evaluando la derivada en x0: {str(e)}",
                funcion=funcion_f,
                claves_grafica=None,
                titulo_grafica="Método de Newton-Raphson",
                ayuda=ayuda_newton,
            )
        
        # Variables para el algoritmo
        xi_anterior = None
        
        ayuda_newton = (
            "Asegúrese de que f(x) y f'(x) estén correctamente definidas. "
            "El método requiere un punto inicial cercano a la raíz y derivadas bien calculadas."
        )

        for i in range(niter + 1):
            try:
                # PASO 1: Evaluar f(xi) y f'(xi)
                fxi = self._evaluar_funcion(funcion_f, xi)
                dfxi = self._evaluar_funcion(funcion_df, xi)

                # Preparar valores para la iteración
                valores = {
                    "i": i,
                    "xi": xi,
                    "fxi": fxi,
                    "dfxi": dfxi
                }

                error = None

                # Verificar si f'(xi) es muy pequeño
                if abs(dfxi) < 1e-12:
                    iteraciones.append(IteracionData(
                        iteracion=i,
                        valores=valores,
                        error=error,
                        observacion="Derivada casi nula"
                    ))
                    return self._construir_respuesta_metodo(
                        exito=False,
                        resultado=xi,
                        iteraciones=iteraciones,
                        mensaje=f"Error: f'({xi}) ≈ 0 en la iteración {i}. El método no puede continuar.",
                        funcion=funcion_f,
                        claves_grafica=["xi"],
                        titulo_grafica="Método de Newton-Raphson",
                        ayuda=ayuda_newton,
                    )
                
                # PASO 3: Calcular error si no es la primera iteración
                if i > 0 and xi_anterior is not None:
                    error_absoluto = abs(xi - xi_anterior)
                    error_relativo = abs(xi - xi_anterior) / abs(xi) if abs(xi) > 1e-12 else error_absoluto
                    error = self._calcular_error(xi, xi_anterior, tipo_error)
                    valores["error"] = error
                    valores["error_absoluto"] = error_absoluto
                    valores["error_relativo"] = error_relativo
                else:
                    valores["error"] = None
                    valores["error_absoluto"] = ""
                    valores["error_relativo"] = ""
                
                # Verificar convergencia por función
                if abs(fxi) <= tolerancia:
                    iteraciones.append(IteracionData(
                        iteracion=i,
                        valores=valores,
                        error=error,
                        observacion="Convergencia por función"
                    ))
                    return self._construir_respuesta_metodo(
                        exito=True,
                        resultado=xi,
                        iteraciones=iteraciones,
                        mensaje=f"Convergencia alcanzada en iteración {i}. Raíz: x = {self._formatear_numero(xi, tipo_precision, precision)}",
                        funcion=funcion_f,
                        claves_grafica=["xi"],
                        titulo_grafica="Método de Newton-Raphson",
                        ayuda=ayuda_newton,
                    )
                
                # Verificar convergencia por error
                if i > 0 and incluir_error and error is not None and error <= tolerancia:
                    iteraciones.append(IteracionData(
                        iteracion=i,
                        valores=valores,
                        error=error,
                        observacion="Convergencia por error"
                    ))
                    return self._construir_respuesta_metodo(
                        exito=True,
                        resultado=xi,
                        iteraciones=iteraciones,
                        mensaje=f"Convergencia por error alcanzada en iteración {i}. Raíz: x = {self._formatear_numero(xi, tipo_precision, precision)}",
                        funcion=funcion_f,
                        claves_grafica=["xi"],
                        titulo_grafica="Método de Newton-Raphson",
                        ayuda=ayuda_newton,
                    )
                
                # Agregar iteración actual
                iteraciones.append(IteracionData(
                    iteracion=i,
                    valores=valores,
                    error=error,
                    observacion="Newton-Raphson"
                ))
                
                # PASO 2: Calcular la siguiente aproximación (si no es la última iteración)
                if i < niter:
                    xi_anterior = xi
                    xi = xi - fxi / dfxi
                
            except Exception as e:
                return self._construir_respuesta_metodo(
                    exito=False,
                    resultado=xi if 'xi' in locals() else None,
                    iteraciones=iteraciones,
                    mensaje=f"Error en iteración {i}: {str(e)}",
                    funcion=funcion_f,
                    claves_grafica=["xi"],
                    titulo_grafica="Método de Newton-Raphson",
                    ayuda=ayuda_newton,
                )
        
        # Si llegamos aquí, se alcanzó el límite de iteraciones
        return self._construir_respuesta_metodo(
            exito=False,
            resultado=xi,
            iteraciones=iteraciones,
            mensaje=f"Método alcanzó el límite de {niter} iteraciones sin convergencia. Última aproximación: x = {self._formatear_numero(xi, tipo_precision, precision)}",
            funcion=funcion_f,
            claves_grafica=["xi"],
            titulo_grafica="Método de Newton-Raphson",
            ayuda=ayuda_newton,
        )
    
    def secante(self, x0: float, x1: float, tolerancia: float, niter: int, 
                funcion: str, incluir_error: bool = True, tipo_error: str = "absoluto",
                tipo_precision: str = "decimales", precision: int = 6) -> Dict[str, Any]:
        """
        Implementa el método de la secante según el procedimiento matemático estándar
        
        Args:
            x0: Primer valor inicial
            x1: Segundo valor inicial  
            tolerancia: Tolerancia para convergencia
            niter: Número máximo de iteraciones
            funcion: Función f(x) como string
            incluir_error: Si incluir columna de error
            tipo_error: 'absoluto' o 'relativo'
            tipo_precision: "decimales" o "significativas"
            precision: Número de decimales o cifras significativas
        """
        iteraciones = []
        
        # Verificar que los valores iniciales sean diferentes
        ayuda_secante = (
            "Seleccione dos valores iniciales distintos y cercanos a la raíz estimada. "
            "Use funciones con la variable x y operadores válidos."
        )

        if abs(x1 - x0) < 1e-12:
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=[],
                mensaje="Error: Los valores iniciales x0 y x1 deben ser diferentes.",
                funcion=funcion,
                claves_grafica=None,
                titulo_grafica="Método de la Secante",
                ayuda=ayuda_secante,
            )
        
        # Variables para el algoritmo
        xi_anterior = x0  # x_{i-1}
        xi = x1           # x_i
        
        # Evaluaciones iniciales
        try:
            fxi_anterior = self._evaluar_funcion(funcion, xi_anterior)
            fxi = self._evaluar_funcion(funcion, xi)
        except Exception as e:
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=[],
                mensaje=f"Error evaluando función en valores iniciales: {str(e)}",
                funcion=funcion,
                claves_grafica=None,
                titulo_grafica="Método de la Secante",
                ayuda=ayuda_secante,
            )
        
        # Orden de columnas para la tabla
        orden_columnas = ["Iteración", "x(i-1)", "x(i)", "f(x(i-1))", "f(x(i))", "Error Absoluto", "Error Relativo", "Observación"]
        
        # Nombres de columnas para la tabla
        nombre_columnas = {
            "i": "Iteración",
            "xi_anterior": "x(i-1)",
            "xi": "x(i)",
            "fxi_anterior": "f(x(i-1))",
            "fxi": "f(x(i))",
            "error_absoluto": "Error Absoluto",
            "error_relativo": "Error Relativo"
        }
        
        for i in range(niter + 1):
            try:
                # Preparar valores para la iteración
                valores = {
                    "i": i,
                    "xi_anterior": xi_anterior,
                    "xi": xi,
                    "fxi_anterior": fxi_anterior,
                    "fxi": fxi
                }
                
                # Calcular error si no es la primera iteración
                error = None
                if i > 0:
                    error_absoluto = abs(xi - xi_anterior)
                    error_relativo = abs(xi - xi_anterior) / abs(xi) if abs(xi) > 1e-12 else error_absoluto
                    error = self._calcular_error(xi, xi_anterior, tipo_error)
                    valores["error_absoluto"] = error_absoluto
                    valores["error_relativo"] = error_relativo
                else:
                    valores["error_absoluto"] = ""
                    valores["error_relativo"] = ""
                
                # Verificar convergencia por función
                if abs(fxi) <= tolerancia:
                    iteraciones.append(IteracionData(
                        iteracion=i,
                        valores=valores,
                        error=error,
                        observacion="Convergencia por función"
                    ))
                    
                    # Generar tabla HTML con nombres de columnas
                    tabla_html = self._iteraciones_a_tabla_html(
                        iteraciones,
                        orden_columnas=orden_columnas,
                        nombre_columnas=nombre_columnas
                    )
                    
                    respuesta = self._construir_respuesta_metodo(
                        exito=True,
                        resultado=xi,
                        iteraciones=iteraciones,
                        mensaje=f"Convergencia alcanzada en iteración {i}. Raíz: x = {self._formatear_numero(xi, tipo_precision, precision)}",
                        funcion=funcion,
                        claves_grafica=["xi", "xi_anterior"],
                        titulo_grafica="Método de la Secante",
                        ayuda=ayuda_secante,
                    )
                    respuesta["tabla_html"] = tabla_html
                    return respuesta
                
                # Verificar convergencia por error
                if i > 0 and incluir_error and error is not None and error <= tolerancia:
                    iteraciones.append(IteracionData(
                        iteracion=i,
                        valores=valores,
                        error=error,
                        observacion="Convergencia por error"
                    ))
                    
                    # Generar tabla HTML con nombres de columnas
                    tabla_html = self._iteraciones_a_tabla_html(
                        iteraciones,
                        orden_columnas=orden_columnas,
                        nombre_columnas=nombre_columnas
                    )
                    
                    respuesta = self._construir_respuesta_metodo(
                        exito=True,
                        resultado=xi,
                        iteraciones=iteraciones,
                        mensaje=f"Convergencia por error alcanzada en iteración {i}. Raíz: x = {self._formatear_numero(xi, tipo_precision, precision)}",
                        funcion=funcion,
                        claves_grafica=["xi", "xi_anterior"],
                        titulo_grafica="Método de la Secante",
                        ayuda=ayuda_secante,
                    )
                    respuesta["tabla_html"] = tabla_html
                    return respuesta
                
                # Verificar si f(xi) - f(xi-1) es muy pequeño (evitar división por cero)
                denominador = fxi - fxi_anterior
                if abs(denominador) < 1e-12:
                    iteraciones.append(IteracionData(
                        iteracion=i,
                        valores=valores,
                        error=error,
                        observacion="Error: Denominador muy pequeño"
                    ))
                    
                    # Generar tabla HTML con nombres de columnas
                    tabla_html = self._iteraciones_a_tabla_html(
                        iteraciones,
                        orden_columnas=orden_columnas,
                        nombre_columnas=nombre_columnas
                    )
                    
                    respuesta = self._construir_respuesta_metodo(
                        exito=False,
                        resultado=xi,
                        iteraciones=iteraciones,
                        mensaje=f"Error: f(xi) - f(xi-1) ≈ 0 en la iteración {i}. El método no puede continuar.",
                        funcion=funcion,
                        claves_grafica=["xi", "xi_anterior"],
                        titulo_grafica="Método de la Secante",
                        ayuda=ayuda_secante,
                    )
                    respuesta["tabla_html"] = tabla_html
                    return respuesta
                
                # Agregar iteración actual
                iteraciones.append(IteracionData(
                    iteracion=i,
                    valores=valores,
                    error=error,
                    observacion="Secante"
                ))
                
                # Calcular la siguiente aproximación (si no es la última iteración)
                if i < niter:
                    xi_nuevo = xi - fxi * (xi - xi_anterior) / denominador
                    
                    # Preparar para siguiente iteración
                    xi_anterior = xi
                    xi = xi_nuevo
                    fxi_anterior = fxi
                    fxi = self._evaluar_funcion(funcion, xi)
                
            except Exception as e:
                # Generar tabla HTML con nombres de columnas
                tabla_html = self._iteraciones_a_tabla_html(
                    iteraciones,
                    orden_columnas=orden_columnas,
                    nombre_columnas=nombre_columnas
                ) if iteraciones else None
                
                respuesta = self._construir_respuesta_metodo(
                    exito=False,
                    resultado=xi if 'xi' in locals() else None,
                    iteraciones=iteraciones,
                    mensaje=f"Error en iteración {i}: {str(e)}",
                    funcion=funcion,
                    claves_grafica=["xi", "xi_anterior"],
                    titulo_grafica="Método de la Secante",
                    ayuda=ayuda_secante,
                )
                if tabla_html:
                    respuesta["tabla_html"] = tabla_html
                return respuesta
        
        # Si llegamos aquí, se alcanzó el límite de iteraciones
        # Generar tabla HTML con nombres de columnas
        tabla_html = self._iteraciones_a_tabla_html(
            iteraciones,
            orden_columnas=orden_columnas,
            nombre_columnas=nombre_columnas
        )
        
        respuesta = self._construir_respuesta_metodo(
            exito=False,
            resultado=xi,
            iteraciones=iteraciones,
            mensaje=f"Método alcanzó el límite de {niter} iteraciones sin convergencia. Última aproximación: x = {self._formatear_numero(xi, tipo_precision, precision)}",
            funcion=funcion,
            claves_grafica=["xi", "xi_anterior"],
            titulo_grafica="Método de la Secante",
            ayuda=ayuda_secante,
        )
        respuesta["tabla_html"] = tabla_html
        return respuesta
    
    def _formatear_numero(self, numero: float, tipo_precision: str, precision: int) -> str:
        """Formatea un número según el tipo de precisión especificado"""
        if tipo_precision == "significativas":
            # Formatear con cifras significativas
            if numero == 0:
                return "0"
            
            # Calcular el exponente para normalizar el número
            exponente = math.floor(math.log10(abs(numero)))
            factor = 10 ** (precision - 1 - exponente)
            numero_redondeado = round(numero * factor) / factor
            
            # Formatear según el exponente
            if exponente >= precision - 1 or exponente < -4:
                return f"{numero_redondeado:.{precision-1}e}"
            else:
                decimales_mostrar = max(0, precision - 1 - exponente)
                return f"{numero_redondeado:.{decimales_mostrar}f}"
        else:
            # Formatear con decimales fijos
            return f"{numero:.{precision}f}"
    
    def raices_multiples(self, x0: float, tolerancia: float, niter: int, 
                        funcion_f: str, funcion_df: str, funcion_ddf: str,
                        tipo_error: str = "absoluto", modo: str = "dc") -> Dict[str, Any]:
        """
        Implementa el método de raíces múltiples mejorado con validaciones robustas.
        
        Fórmula: x_{n+1} = x_n - (f(x_n) * f'(x_n)) / (f'(x_n)^2 - f(x_n) * f''(x_n))
        
        Args:
            x0: Valor inicial
            tolerancia: Tolerancia para convergencia
            niter: Número máximo de iteraciones
            funcion_f: Función f(x) como string
            funcion_df: Primera derivada f'(x) como string
            funcion_ddf: Segunda derivada f''(x) como string
            tipo_error: 'absoluto' o 'relativo'
            modo: "cs" para cifras significativas o "dc" para decimales correctos
        """
        iteraciones = []
        
        # Validar tolerancia
        ayuda_rm = (
            "Use funciones válidas en Python (sin, cos, exp, log). "
            "Recuerde ingresar también f'(x) y f''(x) correctamente; utilice calculadoras de derivadas si es necesario."
        )

        if tolerancia <= 0:
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=[],
                mensaje="La tolerancia debe ser un número positivo.",
                funcion=funcion_f,
                claves_grafica=None,
                titulo_grafica="Método de Raíces Múltiples",
                ayuda=ayuda_rm,
            )
        
        # Validar número de iteraciones
        if niter <= 0:
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=[],
                mensaje="El número máximo de iteraciones debe ser mayor que cero.",
                funcion=funcion_f,
                claves_grafica=None,
                titulo_grafica="Método de Raíces Múltiples",
                ayuda=ayuda_rm,
            )
        
        # Evaluación inicial
        try:
            f_value = self._evaluar_funcion(funcion_f, x0)
            df_value = self._evaluar_funcion(funcion_df, x0)
            ddf_value = self._evaluar_funcion(funcion_ddf, x0)
        except Exception as e:
            return self._construir_respuesta_metodo(
                exito=False,
                resultado=None,
                iteraciones=[],
                mensaje=f"No fue posible evaluar las funciones en el punto inicial X₀. {str(e)}",
                funcion=funcion_f,
                claves_grafica=None,
                titulo_grafica="Método de Raíces Múltiples",
                ayuda=ayuda_rm,
            )
        
        # Primera iteración (iteración 0)
        iteraciones.append(IteracionData(
            iteracion=0,
            valores={
                "xi": x0,
                "f_xi": f_value,
                "df_xi": df_value,
                "ddf_xi": ddf_value,
                "denominador": "",
                "error": "",
                "error_absoluto": "",
                "error_relativo": ""
            },
            error=None,
            observacion="Valores iniciales"
        ))
        
        error = float("inf")
        iter_count = 0
        x_actual = x0
        
        # Algoritmo iterativo
        while iter_count < niter and abs(f_value) > tolerancia and error > tolerancia:
            # Calcular denominador
            denominador = df_value**2 - f_value * ddf_value
            
            # Verificar denominador
            if abs(denominador) < 1e-12:
                iteraciones.append(IteracionData(
                    iteracion=iter_count + 1,
                    valores={
                        "xi": x_actual,
                        "f_xi": f_value,
                        "df_xi": df_value,
                        "ddf_xi": ddf_value,
                        "denominador": denominador,
                        "error": error if iter_count > 0 else "",
                        "error_absoluto": "",
                        "error_relativo": ""
                    },
                    error=error if iter_count > 0 else None,
                    observacion="El denominador se hizo cero"
                ))
                return self._construir_respuesta_metodo(
                    exito=False,
                    resultado=x_actual,
                    iteraciones=iteraciones,
                    mensaje="El denominador de la fórmula se hizo cero. Revise que f'(x) y f''(x) sean correctas para una raíz múltiple.",
                    funcion=funcion_f,
                    claves_grafica=["xi"],
                    titulo_grafica="Método de Raíces Múltiples",
                    ayuda=ayuda_rm,
                )
            
            # Calcular siguiente aproximación
            try:
                x_siguiente = x_actual - (f_value * df_value) / denominador
            except Exception as e:
                return self._construir_respuesta_metodo(
                    exito=False,
                    resultado=x_actual,
                    iteraciones=iteraciones,
                    mensaje=f"No fue posible calcular la siguiente aproximación. {str(e)}",
                    funcion=funcion_f,
                    claves_grafica=["xi"],
                    titulo_grafica="Método de Raíces Múltiples",
                    ayuda=ayuda_rm,
                )
            
            # Calcular ambos tipos de error
            error_absoluto = abs(x_siguiente - x_actual)
            error_relativo = abs(x_siguiente - x_actual) / abs(x_siguiente) if abs(x_siguiente) > 1e-12 else error_absoluto
            
            # Usar el error seleccionado para convergencia
            error = self._calcular_error(x_siguiente, x_actual, tipo_error)
            
            # Evaluar funciones en el nuevo punto
            try:
                f_value = self._evaluar_funcion(funcion_f, x_siguiente)
                df_value = self._evaluar_funcion(funcion_df, x_siguiente)
                ddf_value = self._evaluar_funcion(funcion_ddf, x_siguiente)
            except Exception as e:
                return self._construir_respuesta_metodo(
                    exito=False,
                    resultado=x_siguiente,
                    iteraciones=iteraciones,
                    mensaje=f"No fue posible evaluar las funciones en la iteración {iter_count + 1}. {str(e)}",
                    funcion=funcion_f,
                    claves_grafica=["xi"],
                    titulo_grafica="Método de Raíces Múltiples",
                    ayuda=ayuda_rm,
                )
            
            iter_count += 1
            x_actual = x_siguiente
            
            # Registrar iteración
            iteraciones.append(IteracionData(
                iteracion=iter_count,
                valores={
                    "xi": x_actual,
                    "f_xi": f_value,
                    "df_xi": df_value,
                    "ddf_xi": ddf_value,
                    "denominador": denominador,
                    "error": error,
                    "error_absoluto": error_absoluto,
                    "error_relativo": error_relativo
                },
                error=error,
                observacion="Iteración de raíces múltiples"
            ))
        
        # Determinar el resultado final
        if abs(f_value) <= tolerancia:
            mensaje = f"{x_actual:.10f} es raíz de f(x) con |f(x)| <= {tolerancia}."
            exito = True
        elif error <= tolerancia:
            mensaje = f"{x_actual:.10f} es una aproximación de una raíz múltiple con tolerancia {tolerancia}."
            exito = True
        else:
            mensaje = f"Se alcanzó el máximo de {niter} iteraciones sin cumplir la tolerancia solicitada."
            exito = False
        
        return self._construir_respuesta_metodo(
            exito=exito,
            resultado=x_actual,
            iteraciones=iteraciones,
            mensaje=mensaje,
            funcion=funcion_f,
            claves_grafica=["xi"],
            titulo_grafica="Método de Raíces Múltiples",
            ayuda=ayuda_rm,
        )
    
    def comparar_metodos_ecuaciones(self, 
                                    funcion: str,
                                    x0: float = None,
                                    x1: float = None,
                                    xi: float = None,
                                    xs: float = None,
                                    tolerancia: float = 1e-7,
                                    niter: int = 100,
                                    funcion_g: str = None,
                                    funcion_df: str = None,
                                    funcion_ddf: str = None,
                                    tipo_error: str = "absoluto") -> Dict[str, Any]:
        """
        Ejecuta todos los métodos aplicables de ecuaciones no lineales y genera un informe comparativo.
        
        Args:
            funcion: Función f(x) principal
            x0: Primer valor inicial (para punto fijo, newton, secante, raíces múltiples)
            x1: Segundo valor inicial (para regla falsa, secante)
            xi: Extremo izquierdo intervalo (para bisección)
            xs: Extremo derecho intervalo (para bisección)
            tolerancia: Tolerancia para todos los métodos
            niter: Número máximo de iteraciones
            funcion_g: Función g(x) para punto fijo (opcional)
            funcion_df: Derivada f'(x) para Newton y Raíces Múltiples (opcional)
            funcion_ddf: Segunda derivada f''(x) para Raíces Múltiples (opcional)
            tipo_error: Tipo de error a usar
            
        Returns:
            Diccionario con resultados comparativos
        """
        import time
        
        resultados = {}
        tiempos = {}
        
        # 1. Bisección (requiere xi y xs)
        if xi is not None and xs is not None:
            try:
                inicio = time.time()
                resultado_biseccion = self.biseccion(xi, xs, tolerancia, niter, funcion, tipo_error)
                fin = time.time()
                tiempos["Bisección"] = fin - inicio
                resultados["Bisección"] = {
                    "exito": resultado_biseccion["exito"],
                    "tiempo": tiempos["Bisección"],
                    "resultado": resultado_biseccion.get("resultado"),
                    "iteraciones": len(resultado_biseccion["iteraciones"]),
                    "mensaje": resultado_biseccion["mensaje"]
                }
            except Exception as e:
                resultados["Bisección"] = {
                    "exito": False,
                    "tiempo": 0,
                    "resultado": None,
                    "iteraciones": 0,
                    "mensaje": f"Error: {str(e)}"
                }
        
        # 2. Regla Falsa (requiere x0 y x1)
        if x0 is not None and x1 is not None:
            try:
                inicio = time.time()
                resultado_regla = self.regla_falsa(x0, x1, tolerancia, niter, funcion, tipo_error)
                fin = time.time()
                tiempos["Regla Falsa"] = fin - inicio
                resultados["Regla Falsa"] = {
                    "exito": resultado_regla["exito"],
                    "tiempo": tiempos["Regla Falsa"],
                    "resultado": resultado_regla.get("resultado"),
                    "iteraciones": len(resultado_regla["iteraciones"]),
                    "mensaje": resultado_regla["mensaje"]
                }
            except Exception as e:
                resultados["Regla Falsa"] = {
                    "exito": False,
                    "tiempo": 0,
                    "resultado": None,
                    "iteraciones": 0,
                    "mensaje": f"Error: {str(e)}"
                }
        
        # 3. Punto Fijo (requiere x0 y funcion_g)
        if x0 is not None and funcion_g is not None:
            try:
                inicio = time.time()
                resultado_punto_fijo = self.punto_fijo(x0, tolerancia, niter, funcion, funcion_g, tipo_error)
                fin = time.time()
                tiempos["Punto Fijo"] = fin - inicio
                resultados["Punto Fijo"] = {
                    "exito": resultado_punto_fijo["exito"],
                    "tiempo": tiempos["Punto Fijo"],
                    "resultado": resultado_punto_fijo.get("resultado"),
                    "iteraciones": len(resultado_punto_fijo["iteraciones"]),
                    "mensaje": resultado_punto_fijo["mensaje"]
                }
            except Exception as e:
                resultados["Punto Fijo"] = {
                    "exito": False,
                    "tiempo": 0,
                    "resultado": None,
                    "iteraciones": 0,
                    "mensaje": f"Error: {str(e)}"
                }
        
        # 4. Newton-Raphson (requiere x0 y funcion_df)
        if x0 is not None and funcion_df is not None:
            try:
                inicio = time.time()
                resultado_newton = self.newton_raphson(x0, tolerancia, niter, funcion, funcion_df, True, tipo_error)
                fin = time.time()
                tiempos["Newton-Raphson"] = fin - inicio
                resultados["Newton-Raphson"] = {
                    "exito": resultado_newton["exito"],
                    "tiempo": tiempos["Newton-Raphson"],
                    "resultado": resultado_newton.get("resultado"),
                    "iteraciones": len(resultado_newton["iteraciones"]),
                    "mensaje": resultado_newton["mensaje"]
                }
            except Exception as e:
                resultados["Newton-Raphson"] = {
                    "exito": False,
                    "tiempo": 0,
                    "resultado": None,
                    "iteraciones": 0,
                    "mensaje": f"Error: {str(e)}"
                }
        
        # 5. Secante (requiere x0 y x1)
        if x0 is not None and x1 is not None:
            try:
                inicio = time.time()
                resultado_secante = self.secante(x0, x1, tolerancia, niter, funcion, True, tipo_error)
                fin = time.time()
                tiempos["Secante"] = fin - inicio
                resultados["Secante"] = {
                    "exito": resultado_secante["exito"],
                    "tiempo": tiempos["Secante"],
                    "resultado": resultado_secante.get("resultado"),
                    "iteraciones": len(resultado_secante["iteraciones"]),
                    "mensaje": resultado_secante["mensaje"]
                }
            except Exception as e:
                resultados["Secante"] = {
                    "exito": False,
                    "tiempo": 0,
                    "resultado": None,
                    "iteraciones": 0,
                    "mensaje": f"Error: {str(e)}"
                }
        
        # 6. Raíces Múltiples (requiere x0, funcion_df y funcion_ddf)
        if x0 is not None and funcion_df is not None and funcion_ddf is not None:
            try:
                inicio = time.time()
                resultado_raices = self.raices_multiples(x0, tolerancia, niter, funcion, funcion_df, funcion_ddf, tipo_error)
                fin = time.time()
                tiempos["Raíces Múltiples"] = fin - inicio
                resultados["Raíces Múltiples"] = {
                    "exito": resultado_raices["exito"],
                    "tiempo": tiempos["Raíces Múltiples"],
                    "resultado": resultado_raices.get("resultado"),
                    "iteraciones": len(resultado_raices["iteraciones"]),
                    "mensaje": resultado_raices["mensaje"]
                }
            except Exception as e:
                resultados["Raíces Múltiples"] = {
                    "exito": False,
                    "tiempo": 0,
                    "resultado": None,
                    "iteraciones": 0,
                    "mensaje": f"Error: {str(e)}"
                }
        
        # Verificar que al menos un método se ejecutó
        if not resultados:
            return {
                "exito": False,
                "mensaje": "No se pudo ejecutar ningún método. Verifique los parámetros proporcionados.",
                "resultados": {},
                "informe": None,
                "grafico_comparativo_tiempos": None,
                "grafico_comparativo_convergencia": None
            }
        
        # Filtrar solo métodos exitosos
        metodos_exitosos = {k: v for k, v in tiempos.items() if resultados[k]["exito"]}
        
        if not metodos_exitosos:
            return {
                "exito": False,
                "mensaje": "Ningún método convergió exitosamente. Verifique los parámetros o intervalos.",
                "resultados": resultados,
                "informe": None,
                "grafico_comparativo_tiempos": None,
                "grafico_comparativo_convergencia": None
            }
        
        # Encontrar el más rápido
        metodo_mas_rapido = min(metodos_exitosos, key=metodos_exitosos.get)
        tiempo_mas_rapido = metodos_exitosos[metodo_mas_rapido]
        
        # Encontrar el de menos iteraciones
        iteraciones_dict = {k: resultados[k]["iteraciones"] for k in metodos_exitosos.keys()}
        metodo_menos_iteraciones = min(iteraciones_dict, key=iteraciones_dict.get)
        
        # Generar análisis
        analisis = self._generar_analisis_comparativo_ecuaciones(
            resultados, metodos_exitosos, metodo_mas_rapido, metodo_menos_iteraciones
        )
        
        # Crear gráficos
        try:
            grafico_tiempos = self._crear_grafico_tiempos_ecuaciones(metodos_exitosos)
        except:
            grafico_tiempos = None
        
        try:
            grafico_convergencia = self._crear_grafico_convergencia_ecuaciones(resultados, metodos_exitosos)
        except:
            grafico_convergencia = None
        
        return {
            "exito": True,
            "mensaje": f"Comparación completada. {len(metodos_exitosos)} de {len(resultados)} métodos convergieron.",
            "resultados": resultados,
            "informe": analisis,
            "grafico_comparativo_tiempos": grafico_tiempos,
            "grafico_comparativo_convergencia": grafico_convergencia,
            "metodo_mas_rapido": metodo_mas_rapido,
            "tiempo_mas_rapido": tiempo_mas_rapido,
            "metodo_menos_iteraciones": metodo_menos_iteraciones,
            "total_metodos_exitosos": len(metodos_exitosos),
            "total_metodos_ejecutados": len(resultados)
        }
    
    def _generar_analisis_comparativo_ecuaciones(self, resultados, metodos_exitosos, 
                                                 metodo_mas_rapido, metodo_menos_iteraciones) -> Dict:
        """Genera análisis comparativo para métodos de ecuaciones no lineales."""
        
        analisis = {
            "resumen": f"Se ejecutaron {len(resultados)} métodos, de los cuales {len(metodos_exitosos)} convergieron exitosamente.",
            "metodo_mas_rapido": metodo_mas_rapido,
            "metodo_menos_iteraciones": metodo_menos_iteraciones,
            "recomendacion": "",
            "caracteristicas": {}
        }
        
        # Características de cada método ejecutado
        if "Bisección" in metodos_exitosos:
            analisis["caracteristicas"]["Bisección"] = {
                "ventajas": ["Convergencia garantizada", "Robusto", "Simple"],
                "desventajas": ["Lento", "Requiere intervalo con cambio de signo"],
                "convergencia": "Lineal",
                "mejor_uso": "Cuando se tiene un intervalo con cambio de signo"
            }
        
        if "Regla Falsa" in metodos_exitosos:
            analisis["caracteristicas"]["Regla Falsa"] = {
                "ventajas": ["Más rápido que bisección", "Convergencia garantizada"],
                "desventajas": ["Puede ser lento en ciertos casos", "Requiere intervalo"],
                "convergencia": "Super-lineal",
                "mejor_uso": "Similar a bisección pero más eficiente"
            }
        
        if "Punto Fijo" in metodos_exitosos:
            analisis["caracteristicas"]["Punto Fijo"] = {
                "ventajas": ["Simple", "Versatil"],
                "desventajas": ["Requiere g(x) adecuada", "Convergencia no garantizada"],
                "convergencia": "Lineal (si |g'(x)| < 1)",
                "mejor_uso": "Cuando se puede despejar x = g(x) fácilmente"
            }
        
        if "Newton-Raphson" in metodos_exitosos:
            analisis["caracteristicas"]["Newton-Raphson"] = {
                "ventajas": ["Convergencia cuadrática", "Muy rápido cerca de la raíz"],
                "desventajas": ["Requiere derivada", "Puede diverger"],
                "convergencia": "Cuadrática",
                "mejor_uso": "Cuando se tiene buen punto inicial y derivada disponible"
            }
        
        if "Secante" in metodos_exitosos:
            analisis["caracteristicas"]["Secante"] = {
                "ventajas": ["No requiere derivada", "Rápido", "Convergencia super-lineal"],
                "desventajas": ["Requiere dos puntos iniciales", "Menos estable que Newton"],
                "convergencia": "Super-lineal (~1.618)",
                "mejor_uso": "Alternativa a Newton cuando no se tiene derivada"
            }
        
        if "Raíces Múltiples" in metodos_exitosos:
            analisis["caracteristicas"]["Raíces Múltiples"] = {
                "ventajas": ["Maneja raíces múltiples", "Convergencia cuadrática"],
                "desventajas": ["Requiere f', f''", "Más complejo"],
                "convergencia": "Cuadrática para raíces múltiples",
                "mejor_uso": "Cuando se sospecha raíz de multiplicidad > 1"
            }
        
        # Recomendación basada en resultados
        if metodo_mas_rapido == metodo_menos_iteraciones:
            analisis["recomendacion"] = (
                f"{metodo_mas_rapido} fue el método más eficiente: el más rápido Y el que requirió menos iteraciones. "
                f"Es la mejor opción para este problema específico."
            )
        else:
            analisis["recomendacion"] = (
                f"{metodo_mas_rapido} fue el más rápido, pero {metodo_menos_iteraciones} requirió menos iteraciones. "
                f"Dependiendo de la prioridad (velocidad vs. eficiencia computacional), elija el más adecuado."
            )
        
        # Análisis de convergencia
        if "Newton-Raphson" in metodos_exitosos and resultados["Newton-Raphson"]["iteraciones"] < 10:
            analisis["nota_convergencia"] = "Newton-Raphson mostró convergencia cuadrática típica (muy pocas iteraciones)."
        elif "Bisección" in metodos_exitosos and resultados["Bisección"]["iteraciones"] > 20:
            analisis["nota_convergencia"] = "Bisección requirió muchas iteraciones debido a su convergencia lineal."
        
        return analisis
    
    def _crear_grafico_tiempos_ecuaciones(self, tiempos_dict: Dict[str, float]) -> str:
        """Crea gráfico de barras para tiempos de ejecución."""
        plt.figure(figsize=(10, 6))
        
        metodos = list(tiempos_dict.keys())
        tiempos = [t * 1000 for t in tiempos_dict.values()]  # Convertir a ms
        
        colores = ['#dc3545', '#28a745', '#007bff', '#ffc107', '#17a2b8', '#6c757d']
        
        barras = plt.bar(metodos, tiempos, color=colores[:len(metodos)], alpha=0.7, edgecolor='black')
        
        # Agregar valores sobre las barras
        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2., altura,
                    f'{altura:.3f} ms',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title('Comparación de Tiempos de Ejecución', fontsize=14, fontweight='bold')
        plt.xlabel('Método', fontsize=12)
        plt.ylabel('Tiempo (milisegundos)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri
    
    def _crear_grafico_convergencia_ecuaciones(self, resultados, metodos_exitosos) -> str:
        """Crea gráfico de barras para número de iteraciones."""
        plt.figure(figsize=(10, 6))
        
        metodos = list(metodos_exitosos.keys())
        iteraciones = [resultados[m]["iteraciones"] for m in metodos]
        
        colores = ['#dc3545', '#28a745', '#007bff', '#ffc107', '#17a2b8', '#6c757d']
        
        barras = plt.bar(metodos, iteraciones, color=colores[:len(metodos)], alpha=0.7, edgecolor='black')
        
        # Agregar valores sobre las barras
        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2., altura,
                    f'{int(altura)}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title('Comparación de Iteraciones hasta Convergencia', fontsize=14, fontweight='bold')
        plt.xlabel('Método', fontsize=12)
        plt.ylabel('Número de Iteraciones', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        img_uri = f"data:image/png;base64,{string}"
        
        plt.close()
        
        return img_uri