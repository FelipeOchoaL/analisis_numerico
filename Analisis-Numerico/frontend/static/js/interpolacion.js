// Contador de puntos
let puntosCount = 0;
const MAX_PUNTOS = 8;

// Inicializar con 2 puntos al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    agregarPunto();
    agregarPunto();
    
    // Event listener para el formulario
    document.getElementById('vandermondeForm').addEventListener('submit', calcularVandermonde);
    
    // Event listener para agregar puntos
    document.getElementById('addPuntoBtn').addEventListener('click', agregarPunto);
});

// Función para agregar un punto a la tabla
function agregarPunto() {
    if (puntosCount >= MAX_PUNTOS) {
        alert(`Solo se permiten máximo ${MAX_PUNTOS} puntos`);
        return;
    }
    
    puntosCount++;
    const tbody = document.getElementById('puntosBody');
    const row = tbody.insertRow();
    row.id = `punto-${puntosCount}`;
    
    row.innerHTML = `
        <td>${puntosCount}</td>
        <td>
            <input type="number" step="any" class="form-control punto-input" 
                   id="x-${puntosCount}" placeholder="x${puntosCount}" required>
        </td>
        <td>
            <input type="number" step="any" class="form-control punto-input" 
                   id="y-${puntosCount}" placeholder="y${puntosCount}" required>
        </td>
        <td>
            <button type="button" class="btn btn-danger btn-remove-punto" 
                    onclick="eliminarPunto(${puntosCount})">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    `;
    
    actualizarContador();
    actualizarBotonAgregar();
}

// Función para eliminar un punto
function eliminarPunto(id) {
    if (puntosCount <= 2) {
        alert('Debe mantener al menos 2 puntos para interpolación');
        return;
    }
    
    const row = document.getElementById(`punto-${id}`);
    if (row) {
        row.remove();
        puntosCount--;
        renumerarPuntos();
        actualizarContador();
        actualizarBotonAgregar();
    }
}

// Función para renumerar los puntos después de eliminar
function renumerarPuntos() {
    const tbody = document.getElementById('puntosBody');
    const rows = tbody.getElementsByTagName('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const numero = i + 1;
        rows[i].cells[0].textContent = numero;
    }
}

// Actualizar el contador de puntos
function actualizarContador() {
    document.getElementById('puntosCount').textContent = `Puntos: ${puntosCount}/${MAX_PUNTOS}`;
}

// Actualizar estado del botón agregar
function actualizarBotonAgregar() {
    const btn = document.getElementById('addPuntoBtn');
    btn.disabled = puntosCount >= MAX_PUNTOS;
}

// Función para obtener todos los puntos
function obtenerPuntos() {
    const x = [];
    const y = [];
    
    for (let i = 1; i <= puntosCount; i++) {
        const xInput = document.getElementById(`x-${i}`);
        const yInput = document.getElementById(`y-${i}`);
        
        if (xInput && yInput) {
            const xVal = parseFloat(xInput.value);
            const yVal = parseFloat(yInput.value);
            
            if (isNaN(xVal) || isNaN(yVal)) {
                throw new Error(`Punto ${i}: Los valores deben ser numéricos`);
            }
            
            x.push(xVal);
            y.push(yVal);
        }
    }
    
    return { x, y };
}

// Función principal para calcular interpolación con Vandermonde
async function calcularVandermonde(event) {
    event.preventDefault();
    
    // Ocultar resultados previos y errores
    document.getElementById('resultado').style.display = 'none';
    document.getElementById('errorDiv').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    
    try {
        // Obtener puntos
        const { x, y } = obtenerPuntos();
        
        // Validar que x e y tengan el mismo tamaño
        if (x.length !== y.length) {
            throw new Error('Las listas x e y deben tener el mismo tamaño');
        }
        
        // Validar que haya al menos 2 puntos
        if (x.length < 2) {
            throw new Error('Se necesitan al menos 2 puntos para interpolación');
        }
        
        // Validar que no haya valores x repetidos
        const xSet = new Set(x);
        if (xSet.size !== x.length) {
            throw new Error('Los valores de x deben ser únicos (no repetidos)');
        }
        
        // Obtener grado
        const grado = parseInt(document.getElementById('grado').value);
        
        if (isNaN(grado) || grado < 1) {
            throw new Error('El grado debe ser un número entero positivo');
        }
        
        // Validar que el grado sea compatible con el número de puntos
        if (grado >= x.length) {
            const sugerencia = x.length - 1;
            throw new Error(
                `Para ${x.length} puntos, el grado máximo recomendado es ${sugerencia}. ` +
                `Si usa grado ${grado}, necesita al menos ${grado + 1} puntos.`
            );
        }
        
        // Preparar datos para enviar
        const data = {
            x: x,
            y: y,
            grado: grado
        };
        
        // Enviar petición al backend
        const response = await fetch('/api/vandermonde', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        // Ocultar loading
        document.getElementById('loading').style.display = 'none';
        
        // Verificar si fue exitoso
        if (result.exito) {
            mostrarResultado(result);
        } else {
            mostrarError(result.mensaje, result.grafico);
        }
        
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        mostrarError(error.message);
    }
}

// Función para mostrar el resultado
function mostrarResultado(result) {
    const resultadoDiv = document.getElementById('resultado');
    
    // Mostrar polinomio
    document.getElementById('polinomioResultado').textContent = result.polinomio || 'No disponible';
    
    // Mostrar gráfico
    if (result.grafico) {
        document.getElementById('graficoResultado').src = result.grafico;
    }
    
    // Mostrar información
    document.getElementById('gradoInfo').textContent = result.grado || 'N/A';
    document.getElementById('mensajeInfo').textContent = result.mensaje || '';
    
    // Mostrar coeficientes
    const coefDiv = document.getElementById('coeficientesInfo');
    if (result.coeficientes && result.coeficientes.length > 0) {
        let html = '<small>';
        result.coeficientes.forEach((coef, index) => {
            const power = result.grado - index;
            html += `<div>a<sub>${power}</sub> = ${coef.toFixed(6)}</div>`;
        });
        html += '</small>';
        coefDiv.innerHTML = html;
    } else {
        coefDiv.innerHTML = '<small class="text-muted">No disponibles</small>';
    }
    
    // Mostrar el div de resultados
    resultadoDiv.style.display = 'block';
    
    // Scroll suave hacia los resultados
    resultadoDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Función para mostrar errores
function mostrarError(mensaje, grafico = null) {
    const errorDiv = document.getElementById('errorDiv');
    document.getElementById('errorMensaje').textContent = mensaje;
    
    if (grafico) {
        document.getElementById('graficoError').src = grafico;
        document.getElementById('errorGrafico').style.display = 'block';
    } else {
        document.getElementById('errorGrafico').style.display = 'none';
    }
    
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Función para limpiar el formulario
function limpiarFormulario() {
    // Limpiar la tabla de puntos
    document.getElementById('puntosBody').innerHTML = '';
    puntosCount = 0;
    
    // Agregar 2 puntos por defecto
    agregarPunto();
    agregarPunto();
    
    // Resetear grado
    document.getElementById('grado').value = 2;
    
    // Ocultar resultados y errores
    document.getElementById('resultado').style.display = 'none';
    document.getElementById('errorDiv').style.display = 'none';
}

// Funciones para cargar ejemplos
function cargarEjemploLineal() {
    limpiarFormulario();
    
    // Ejemplo lineal: y = 2x + 2
    document.getElementById('x-1').value = 0;
    document.getElementById('y-1').value = 2;
    document.getElementById('x-2').value = 5;
    document.getElementById('y-2').value = 12;
    document.getElementById('grado').value = 1;
}

function cargarEjemploCuadratico() {
    limpiarFormulario();
    
    // Agregar un punto más (necesitamos 3 para cuadrática)
    agregarPunto();
    
    // Ejemplo cuadrático: y = x²
    document.getElementById('x-1').value = 0;
    document.getElementById('y-1').value = 0;
    document.getElementById('x-2').value = 1;
    document.getElementById('y-2').value = 1;
    document.getElementById('x-3').value = 2;
    document.getElementById('y-3').value = 4;
    document.getElementById('grado').value = 2;
}

function cargarEjemploCubico() {
    limpiarFormulario();
    
    // Agregar puntos necesarios (4 para cúbica)
    agregarPunto();
    agregarPunto();
    
    // Ejemplo cúbico
    document.getElementById('x-1').value = -1;
    document.getElementById('y-1').value = 0;
    document.getElementById('x-2').value = 0;
    document.getElementById('y-2').value = 1;
    document.getElementById('x-3').value = 1;
    document.getElementById('y-3').value = 0;
    document.getElementById('x-4').value = 2;
    document.getElementById('y-4').value = -3;
    document.getElementById('grado').value = 3;
}

