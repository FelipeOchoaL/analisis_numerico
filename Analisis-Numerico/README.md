# 🧮 API de Análisis Numérico

Este proyecto implementa una **API REST completa** usando **FastAPI** con todas las funciones de análisis numérico desarrolladas en clase, junto con un **frontend web interactivo** usando **Flask**. Incluye métodos para resolución de ecuaciones no lineales, cálculo de errores y series de Taylor.

## 📁 Estructura del Proyecto

```
analisis_numerico/
├── 📂 Analisis-Numerico/           # 🔥 REPOSITORIO GIT PRINCIPAL
│   ├── 📂 backend/                 # API FastAPI
│   │   ├── main.py                # Servidor principal de la API
│   │   ├── models/                # Modelos Pydantic para validación
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── routers/               # Endpoints organizados por módulos
│   │   │   ├── __init__.py
│   │   │   ├── ecuaciones_no_lineales.py
│   │   │   ├── errores.py
│   │   │   └── series_taylor.py
│   │   ├── services/              # Lógica de negocio refactorizada
│   │   │   ├── __init__.py
│   │   │   ├── ecuaciones_service.py
│   │   │   ├── errores_service.py
│   │   │   └── taylor_service.py
│   │   └── requirements.txt       # Dependencias del backend
│   ├── 📂 frontend/                # Frontend Flask
│   │   ├── app.py                # Servidor del frontend
│   │   ├── static/               # Archivos estáticos
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   └── js/
│   │   │       ├── ecuaciones.js
│   │   │       ├── errores.js
│   │   │       └── taylor.js
│   │   ├── templates/            # Templates HTML
│   │   │   ├── index.html
│   │   │   ├── ecuaciones_no_lineales.html
│   │   │   ├── errores.html
│   │   │   └── series_taylor.html
│   │   └── requirements.txt      # Dependencias del frontend
│   ├── 📂 ecuaciones_no_lineales/  # Código original de métodos
│   ├── 📂 errores/                # Código original de errores  
│   └── 📂 serie_de_taylor/        # Código original de series
├── 📄 start_project.py            # 🚀 SCRIPT DE INICIO AUTOMÁTICO
└── 📄 README.md                   # Esta documentación
```

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### ⚡ **OPCIÓN 1: Inicio Automático (Recomendado)**

```bash
# Ejecutar desde la carpeta raíz del proyecto
python start_project.py
```

**🎉 ¡Eso es todo!** El script automáticamente:
- ✅ Verifica que todos los archivos estén presentes
- ✅ Instala las dependencias necesarias (solo si faltan)
- ✅ Inicia el backend (FastAPI) en http://127.0.0.1:8000
- ✅ Inicia el frontend (Flask) en http://127.0.0.1:3000
- ✅ Abre tu navegador automáticamente
- ✅ Muestra el estado de ambos servidores

**Para detener:** Presiona `Ctrl+C` y ambos servidores se detendrán automáticamente.

### 🔧 **OPCIÓN 2: Configuración Manual**

Si prefieres configurar manualmente cada parte:

#### 1. Backend (FastAPI)

```bash
# Navegar al directorio del backend
cd Analisis-Numerico/backend

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor FastAPI
python main.py
```

#### 2. Frontend (Flask)

**En una nueva terminal:**

```bash
# Navegar al directorio del frontend
cd Analisis-Numerico/frontend

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor Flask
python app.py
```

### 🌐 **URLs del Proyecto**

Una vez iniciado, tendrás acceso a:

- **🏠 Frontend Principal**: http://127.0.0.1:3000
- **🔧 API Backend**: http://127.0.0.1:8000
- **📚 Documentación API**: http://127.0.0.1:8000/docs
- **📖 ReDoc**: http://127.0.0.1:8000/redoc
- **❤️ Health Check**: http://127.0.0.1:8000/health

## ✨ Características del Proyecto

### 🎯 **Backend (FastAPI)**
- ✅ **API REST** completa con documentación automática
- ✅ **Validación automática** de datos con Pydantic  
- ✅ **Arquitectura modular** (routers, services, models)
- ✅ **Manejo de errores** robusto
- ✅ **CORS** configurado para desarrollo
- ✅ **Documentación interactiva** (Swagger + ReDoc)

### 🎨 **Frontend (Flask)**
- ✅ **Interfaz responsive** con Bootstrap 5
- ✅ **JavaScript moderno** para interactividad
- ✅ **Formularios inteligentes** con validación
- ✅ **Resultados en tiempo real** sin recargar página
- ✅ **Tablas de iteraciones** detalladas
- ✅ **Indicadores visuales** de convergencia

### 🚀 **Script de Inicio**
- ✅ **Instalación automática** de dependencias
- ✅ **Verificación de archivos** necesarios
- ✅ **Inicio simultáneo** de ambos servidores
- ✅ **Monitoreo de estado** en tiempo real
- ✅ **Apertura automática** del navegador
- ✅ **Cierre limpio** con Ctrl+C

## 📊 Métodos Implementados

### 🔢 Ecuaciones No Lineales

#### 1. **Método de Bisección**
- **Descripción**: Encuentra raíces en un intervalo con cambio de signo
- **Entrada**: Xi, Xs, tolerancia, número de iteraciones, función f(x)
- **Condición**: f(Xi) × f(Xs) < 0

#### 2. **Método de Punto Fijo**
- **Descripción**: Encuentra puntos fijos de una función de iteración
- **Entrada**: X0, tolerancia, número de iteraciones, f(x), g(x)
- **Condición**: g(x) debe cumplir que la raíz de f(x) sea punto fijo de g(x)

#### 3. **Método de Regla Falsa**
- **Descripción**: Interpolación lineal para encontrar raíces
- **Entrada**: X0, X1, tolerancia, número de iteraciones, función f(x)
- **Fórmula**: X2 = X0 - f(X0) × (X1 - X0) / (f(X1) - f(X0))

#### 4. **Búsqueda Incremental**
- **Descripción**: Encuentra intervalos con cambio de signo
- **Entrada**: X0, delta (incremento), número de iteraciones, función f(x)

### 📏 Cálculo de Errores

#### 1. **Error Absoluto**
```
E_abs = |x_exacto - x_aproximado|
```

#### 2. **Error Relativo**
```
E_rel = |x_exacto - x_aproximado| / |x_exacto|
E_porcentual = E_rel × 100%
```

#### 3. **Propagación de Errores**
- **Suma/Resta**: `√(ex² + ey²)`
- **Producto/División**: `|resultado| × √((ex/x)² + (ey/y)²)`

### 🌊 Series de Taylor

#### 1. **Función Coseno**
```
cos(θ) = Σ[k=0 to ∞] (-1)^k × θ^(2k) / (2k)!
```

#### 2. **Función Seno**
```
sen(θ) = Σ[k=0 to ∞] (-1)^k × θ^(2k+1) / (2k+1)!
```

## 🔧 Uso de la API

### Ejemplo con Python (requests)

```python
import requests

# Método de Bisección
data = {
    "xi": -2,
    "xs": 2,
    "tolerancia": 0.001,
    "niter": 100,
    "funcion": "x**2 - 4"
}

response = requests.post("http://127.0.0.1:8000/api/ecuaciones-no-lineales/biseccion", json=data)
resultado = response.json()
print(f"Raíz encontrada: {resultado['resultado']}")

# Serie de Taylor (Coseno)
data = {
    "theta": 1.5708,  # π/2
    "tolerancia": 1e-8,
    "niter": 50,
    "error_relativo": false
}

response = requests.post("http://127.0.0.1:8000/api/series-taylor/coseno", json=data)
resultado = response.json()
print(f"cos(π/2) ≈ {resultado['aproximacion']}")
```

### Ejemplo con curl

```bash
# Error absoluto
curl -X POST "http://127.0.0.1:8000/api/errores/error-absoluto" \
     -H "Content-Type: application/json" \
     -d '{"x_aproximado": 3.14, "x_exacto": 3.141592653}'
```

## 📝 Funciones Matemáticas Soportadas

En las funciones string puede usar:

- **Operaciones básicas**: `+`, `-`, `*`, `/`, `**` (potencia)
- **Funciones trigonométricas**: `sin(x)`, `cos(x)`, `tan(x)`
- **Funciones exponenciales**: `exp(x)`, `log(x)`, `sqrt(x)`
- **Constantes**: `pi`, `e`

### Ejemplos de funciones válidas:
- `x**2 - 4`
- `sin(x) - x/2`
- `exp(x) - 2`
- `log(x) + x - 2`
- `x**3 - 2*x - 5`

## 🌐 Interfaz Web

El frontend web proporciona:

1. **🏠 Página principal**: Navegación entre módulos
2. **🔢 Ecuaciones No Lineales**: Formularios para cada método con resultados tabulados
3. **📏 Cálculo de Errores**: Herramientas para análisis de errores
4. **🌊 Series de Taylor**: Calculadora de series con ángulos comunes
5. **📊 Resultados visuales**: Tablas de iteraciones y análisis de convergencia

### Características del Frontend:
- ✅ Interfaz responsiva (Bootstrap 5)
- ✅ Validación de formularios
- ✅ Resultados en tiempo real
- ✅ Tablas de iteraciones detalladas
- ✅ Indicadores de convergencia
- ✅ Manejo de errores

## 🔍 Testing y Ejemplos

### Casos de prueba recomendados:

#### Bisección:
- f(x) = x² - 4, intervalo [-3, 3] → raíces: ±2
- f(x) = x³ - x - 1, intervalo [1, 2] → raíz: ≈1.324718

#### Series de Taylor:
- cos(0) = 1
- cos(π/2) ≈ 0 
- sen(π/2) = 1
- sen(π/6) = 0.5

#### Errores:
- Valor exacto: π = 3.141592653, aproximado: 3.14 → Error abs: 0.001593

## 🛠 Tecnologías Utilizadas

### Backend:
- **FastAPI**: Framework web moderno para APIs
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Pydantic**: Validación de datos y serialización
- **NumPy**: Computación numérica
- **Pandas**: Manipulación de datos

### Frontend:
- **Flask**: Framework web de Python
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript (ES6+)**: Interactividad del frontend
- **Font Awesome**: Iconografía

### API Documentation:
- **Swagger UI**: Documentación interactiva automática
- **ReDoc**: Documentación alternativa


## 📋 Control de Versiones (Git)

### 🌟 **Estructura del Repositorio**

El repositorio git está ubicado en la carpeta `Analisis-Numerico/`, que contiene:
- ✅ **Código original** de métodos numéricos (ecuaciones, errores, series)
- ✅ **Backend API** completo (FastAPI)
- ✅ **Frontend web** completo (Flask)

### 🔄 **Comandos Git Útiles**

```bash
# Navegar al repositorio
cd Analisis-Numerico

# Ver estado del repositorio
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push

# Ver historial de commits
git log --oneline
```

### 📁 **Estructura para Git**

```bash
# Todo lo que está dentro de Analisis-Numerico/ está en el repositorio:
Analisis-Numerico/
├── .git/                     # Control de versiones
├── backend/                  # ✅ Se puede hacer commit
├── frontend/                 # ✅ Se puede hacer commit  
├── ecuaciones_no_lineales/   # ✅ Se puede hacer commit
├── errores/                  # ✅ Se puede hacer commit
└── serie_de_taylor/          # ✅ Se puede hacer commit

# Archivos fuera del repositorio (no se incluyen en commits):
../start_project.py           # Script de inicio (opcional)
../README.md                  # Documentación externa
```

## 🐛 Troubleshooting

### Problemas comunes:

1. **"No se encuentra el archivo main.py"**:
   - Asegúrate de ejecutar `python start_project.py` desde la carpeta raíz
   - Verifica que existe `Analisis-Numerico/backend/main.py`

2. **Error de conexión entre frontend y backend**:
   - Verificar que ambos servidores estén ejecutándose
   - Backend: http://127.0.0.1:8000
   - Frontend: http://127.0.0.1:3000

3. **Error en funciones matemáticas**:
   - Usar 'x' como variable
   - Verificar sintaxis (ej: x**2, no x^2)
   - Verificar que las funciones estén en el namespace soportado

4. **Error de división por cero**:
   - Verificar valores de entrada
   - Para error relativo: el valor exacto no puede ser cero

5. **Falta de convergencia**:
   - Ajustar tolerancia o número de iteraciones
   - Verificar condiciones iniciales del método

6. **Dependencias no instaladas**:
   - El script `start_project.py` instala automáticamente las dependencias
   - Para instalación manual: revisar `requirements.txt` en cada carpeta

## 👨‍💻 Desarrollo y Extensiones

Para extender el proyecto:

1. **Agregar nuevos métodos numéricos**:
   - Crear servicio en `Analisis-Numerico/backend/services/`
   - Agregar router en `Analisis-Numerico/backend/routers/`
   - Crear modelo Pydantic en `Analisis-Numerico/backend/models/schemas.py`

2. **Mejorar el frontend**:
   - Crear template en `Analisis-Numerico/frontend/templates/`
   - Agregar JavaScript en `Analisis-Numerico/frontend/static/js/`
   - Actualizar CSS en `Analisis-Numerico/frontend/static/css/`

3. **Documentación automática**:
   - Usar docstrings en funciones para auto-documentación
   - Actualizar modelos Pydantic para descripción de endpoints

## 📄 Licencia

Este proyecto fue desarrollado para fines educativos en el curso de **Análisis Numérico**.

---

## 🎉 ¡Proyecto Listo!

### ⚡ **Inicio Rápido:**
```bash
python start_project.py
```

### 🌐 **URLs Importantes:**
- **Frontend**: http://127.0.0.1:3000
- **API Docs**: http://127.0.0.1:8000/docs

**¡Disfruta explorando métodos numéricos con una interfaz moderna! 🚀**
