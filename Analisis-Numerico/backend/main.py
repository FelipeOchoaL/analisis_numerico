from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from routers import (
    ecuaciones_no_lineales,
    errores,
    series_taylor,
    sistemas_ecuaciones
)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Análisis Numérico",
    description="API para métodos de análisis numérico",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(
    ecuaciones_no_lineales.router,
    prefix="/api/ecuaciones-no-lineales",
    tags=["Ecuaciones No Lineales"]
)

app.include_router(
    errores.router,
    prefix="/api/errores",
    tags=["Cálculo de Errores"]
)

app.include_router(
    series_taylor.router,
    prefix="/api/series-taylor",
    tags=["Series de Taylor"]
)

app.include_router(
    sistemas_ecuaciones.router,
    prefix="/api/sistemas-ecuaciones",
    tags=["Sistemas de Ecuaciones"]
)

@app.get("/")
async def root():
    return {
        "message": "API de Análisis Numérico",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
