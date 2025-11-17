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

// ================== MÉTODO DE NEWTON ==================

// Contador de puntos para Newton
let puntosCountNewton = 0;

// Inicializar Newton cuando se cambie al tab
document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que el DOM esté completamente cargado
    const newtonTab = document.getElementById('newton-tab');
    if (newtonTab) {
        newtonTab.addEventListener('shown.bs.tab', function() {
            if (puntosCountNewton === 0) {
                agregarPuntoNewton();
                agregarPuntoNewton();
            }
        });
    }
    
    // Event listeners para Newton
    const newtonForm = document.getElementById('newtonForm');
    if (newtonForm) {
        newtonForm.addEventListener('submit', calcularNewton);
    }
    
    const addBtnNewton = document.getElementById('addPuntoNewtonBtn');
    if (addBtnNewton) {
        addBtnNewton.addEventListener('click', agregarPuntoNewton);
    }
});

// Función para agregar un punto a la tabla de Newton
function agregarPuntoNewton() {
    if (puntosCountNewton >= MAX_PUNTOS) {
        alert(`Solo se permiten máximo ${MAX_PUNTOS} puntos`);
        return;
    }
    
    puntosCountNewton++;
    const tbody = document.getElementById('puntosBodyNewton');
    const row = tbody.insertRow();
    row.id = `punto-newton-${puntosCountNewton}`;
    
    row.innerHTML = `
        <td>${puntosCountNewton}</td>
        <td>
            <input type="number" step="any" class="form-control punto-input" 
                   id="x-newton-${puntosCountNewton}" placeholder="x${puntosCountNewton}" required>
        </td>
        <td>
            <input type="number" step="any" class="form-control punto-input" 
                   id="y-newton-${puntosCountNewton}" placeholder="y${puntosCountNewton}" required>
        </td>
        <td>
            <button type="button" class="btn btn-danger btn-remove-punto" 
                    onclick="eliminarPuntoNewton(${puntosCountNewton})">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    `;
    
    actualizarContadorNewton();
    actualizarBotonAgregarNewton();
}

// Función para eliminar un punto de Newton
function eliminarPuntoNewton(id) {
    if (puntosCountNewton <= 2) {
        alert('Debe mantener al menos 2 puntos para interpolación');
        return;
    }
    
    const row = document.getElementById(`punto-newton-${id}`);
    if (row) {
        row.remove();
        puntosCountNewton--;
        renumerarPuntosNewton();
        actualizarContadorNewton();
        actualizarBotonAgregarNewton();
    }
}

// Función para renumerar los puntos de Newton
function renumerarPuntosNewton() {
    const tbody = document.getElementById('puntosBodyNewton');
    const rows = tbody.getElementsByTagName('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const numero = i + 1;
        rows[i].cells[0].textContent = numero;
    }
}

// Actualizar el contador de puntos de Newton
function actualizarContadorNewton() {
    document.getElementById('puntosCountNewton').textContent = `Puntos: ${puntosCountNewton}/${MAX_PUNTOS}`;
}

// Actualizar estado del botón agregar de Newton
function actualizarBotonAgregarNewton() {
    const btn = document.getElementById('addPuntoNewtonBtn');
    if (btn) {
        btn.disabled = puntosCountNewton >= MAX_PUNTOS;
    }
}

// Función para obtener todos los puntos de Newton
function obtenerPuntosNewton() {
    const x = [];
    const y = [];
    
    for (let i = 1; i <= puntosCountNewton; i++) {
        const xInput = document.getElementById(`x-newton-${i}`);
        const yInput = document.getElementById(`y-newton-${i}`);
        
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

// Función principal para calcular interpolación con Newton
async function calcularNewton(event) {
    event.preventDefault();
    
    // Ocultar resultados previos y errores
    document.getElementById('resultadoNewton').style.display = 'none';
    document.getElementById('errorDivNewton').style.display = 'none';
    document.getElementById('loadingNewton').style.display = 'block';
    
    try {
        // Obtener puntos
        const { x, y } = obtenerPuntosNewton();
        
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
        
        // Preparar datos para enviar
        const data = {
            x: x,
            y: y
        };
        
        // Enviar petición al backend
        const response = await fetch('/api/newton', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        // Ocultar loading
        document.getElementById('loadingNewton').style.display = 'none';
        
        // Verificar si fue exitoso
        if (result.exito) {
            mostrarResultadoNewton(result);
        } else {
            mostrarErrorNewton(result.mensaje, result.grafico);
        }
        
    } catch (error) {
        document.getElementById('loadingNewton').style.display = 'none';
        mostrarErrorNewton(error.message);
    }
}

// Función para mostrar el resultado de Newton
function mostrarResultadoNewton(result) {
    const resultadoDiv = document.getElementById('resultadoNewton');
    
    // Mostrar polinomio
    document.getElementById('polinomioResultadoNewton').textContent = result.polinomio || 'No disponible';
    
    // Mostrar gráfico
    if (result.grafico) {
        document.getElementById('graficoResultadoNewton').src = result.grafico;
    }
    
    // Mostrar información
    document.getElementById('gradoInfoNewton').textContent = result.grado || 'N/A';
    document.getElementById('mensajeInfoNewton').textContent = result.mensaje || '';
    
    // Mostrar coeficientes
    const coefDiv = document.getElementById('coeficientesInfoNewton');
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

// Función para mostrar errores de Newton
function mostrarErrorNewton(mensaje, grafico = null) {
    const errorDiv = document.getElementById('errorDivNewton');
    document.getElementById('errorMensajeNewton').textContent = mensaje;
    
    if (grafico) {
        document.getElementById('graficoErrorNewton').src = grafico;
        document.getElementById('errorGraficoNewton').style.display = 'block';
    } else {
        document.getElementById('errorGraficoNewton').style.display = 'none';
    }
    
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Función para limpiar el formulario de Newton
function limpiarFormularioNewton() {
    // Limpiar la tabla de puntos
    document.getElementById('puntosBodyNewton').innerHTML = '';
    puntosCountNewton = 0;
    
    // Agregar 2 puntos por defecto
    agregarPuntoNewton();
    agregarPuntoNewton();
    
    // Ocultar resultados y errores
    document.getElementById('resultadoNewton').style.display = 'none';
    document.getElementById('errorDivNewton').style.display = 'none';
}

// Funciones para cargar ejemplos de Newton
function cargarEjemploNewtonLineal() {
    limpiarFormularioNewton();
    
    // Ejemplo lineal: y = 2x + 2
    document.getElementById('x-newton-1').value = 0;
    document.getElementById('y-newton-1').value = 2;
    document.getElementById('x-newton-2').value = 5;
    document.getElementById('y-newton-2').value = 12;
}

function cargarEjemploNewtonCuadratico() {
    limpiarFormularioNewton();
    
    // Agregar un punto más (necesitamos 3 para cuadrática)
    agregarPuntoNewton();
    
    // Ejemplo cuadrático: y = x²
    document.getElementById('x-newton-1').value = 0;
    document.getElementById('y-newton-1').value = 0;
    document.getElementById('x-newton-2').value = 1;
    document.getElementById('y-newton-2').value = 1;
    document.getElementById('x-newton-3').value = 2;
    document.getElementById('y-newton-3').value = 4;
}

function cargarEjemploNewtonCubico() {
    limpiarFormularioNewton();
    
    // Agregar puntos necesarios (4 para cúbica)
    agregarPuntoNewton();
    agregarPuntoNewton();
    
    // Ejemplo cúbico
    document.getElementById('x-newton-1').value = -1;
    document.getElementById('y-newton-1').value = 0;
    document.getElementById('x-newton-2').value = 0;
    document.getElementById('y-newton-2').value = 1;
    document.getElementById('x-newton-3').value = 1;
    document.getElementById('y-newton-3').value = 0;
    document.getElementById('x-newton-4').value = 2;
    document.getElementById('y-newton-4').value = -3;
}

// ================== MÉTODO DE LAGRANGE ==================

// Contador de puntos para Lagrange
let puntosCountLagrange = 0;

// Inicializar Lagrange cuando se cambie al tab
document.addEventListener('DOMContentLoaded', function() {
    const lagrangeTab = document.getElementById('lagrange-tab');
    if (lagrangeTab) {
        lagrangeTab.addEventListener('shown.bs.tab', function() {
            if (puntosCountLagrange === 0) {
                agregarPuntoLagrange();
                agregarPuntoLagrange();
            }
        });
    }
    
    // Event listeners para Lagrange
    const lagrangeForm = document.getElementById('lagrangeForm');
    if (lagrangeForm) {
        lagrangeForm.addEventListener('submit', calcularLagrange);
    }
    
    const addBtnLagrange = document.getElementById('addPuntoLagrangeBtn');
    if (addBtnLagrange) {
        addBtnLagrange.addEventListener('click', agregarPuntoLagrange);
    }
});

// Función para agregar un punto a la tabla de Lagrange
function agregarPuntoLagrange() {
    if (puntosCountLagrange >= MAX_PUNTOS) {
        alert(`Solo se permiten máximo ${MAX_PUNTOS} puntos`);
        return;
    }
    
    puntosCountLagrange++;
    const tbody = document.getElementById('puntosBodyLagrange');
    const row = tbody.insertRow();
    row.id = `punto-lagrange-${puntosCountLagrange}`;
    
    row.innerHTML = `
        <td>${puntosCountLagrange}</td>
        <td>
            <input type="number" step="any" class="form-control punto-input" 
                   id="x-lagrange-${puntosCountLagrange}" placeholder="x${puntosCountLagrange}" required>
        </td>
        <td>
            <input type="number" step="any" class="form-control punto-input" 
                   id="y-lagrange-${puntosCountLagrange}" placeholder="y${puntosCountLagrange}" required>
        </td>
        <td>
            <button type="button" class="btn btn-danger btn-remove-punto" 
                    onclick="eliminarPuntoLagrange(${puntosCountLagrange})">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    `;
    
    actualizarContadorLagrange();
    actualizarBotonAgregarLagrange();
}

// Función para eliminar un punto de Lagrange
function eliminarPuntoLagrange(id) {
    if (puntosCountLagrange <= 2) {
        alert('Debe mantener al menos 2 puntos para interpolación');
        return;
    }
    
    const row = document.getElementById(`punto-lagrange-${id}`);
    if (row) {
        row.remove();
        puntosCountLagrange--;
        renumerarPuntosLagrange();
        actualizarContadorLagrange();
        actualizarBotonAgregarLagrange();
    }
}

// Función para renumerar los puntos de Lagrange
function renumerarPuntosLagrange() {
    const tbody = document.getElementById('puntosBodyLagrange');
    const rows = tbody.getElementsByTagName('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const numero = i + 1;
        rows[i].cells[0].textContent = numero;
    }
}

// Actualizar el contador de puntos de Lagrange
function actualizarContadorLagrange() {
    document.getElementById('puntosCountLagrange').textContent = `Puntos: ${puntosCountLagrange}/${MAX_PUNTOS}`;
}

// Actualizar estado del botón agregar de Lagrange
function actualizarBotonAgregarLagrange() {
    const btn = document.getElementById('addPuntoLagrangeBtn');
    if (btn) {
        btn.disabled = puntosCountLagrange >= MAX_PUNTOS;
    }
}

// Función para obtener todos los puntos de Lagrange
function obtenerPuntosLagrange() {
    const x = [];
    const y = [];
    
    for (let i = 1; i <= puntosCountLagrange; i++) {
        const xInput = document.getElementById(`x-lagrange-${i}`);
        const yInput = document.getElementById(`y-lagrange-${i}`);
        
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

// Función principal para calcular interpolación con Lagrange
async function calcularLagrange(event) {
    event.preventDefault();
    
    // Ocultar resultados previos y errores
    document.getElementById('resultadoLagrange').style.display = 'none';
    document.getElementById('errorDivLagrange').style.display = 'none';
    document.getElementById('loadingLagrange').style.display = 'block';
    
    try {
        // Obtener puntos
        const { x, y } = obtenerPuntosLagrange();
        
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
        
        // Preparar datos para enviar
        const data = {
            x: x,
            y: y
        };
        
        // Enviar petición al backend
        const response = await fetch('/api/lagrange', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        // Ocultar loading
        document.getElementById('loadingLagrange').style.display = 'none';
        
        // Verificar si fue exitoso
        if (result.exito) {
            mostrarResultadoLagrange(result);
        } else {
            mostrarErrorLagrange(result.mensaje, result.grafico);
        }
        
    } catch (error) {
        document.getElementById('loadingLagrange').style.display = 'none';
        mostrarErrorLagrange(error.message);
    }
}

// Función para mostrar el resultado de Lagrange
function mostrarResultadoLagrange(result) {
    const resultadoDiv = document.getElementById('resultadoLagrange');
    
    // Mostrar polinomio
    document.getElementById('polinomioResultadoLagrange').textContent = result.polinomio || 'No disponible';
    
    // Mostrar gráfico
    if (result.grafico) {
        document.getElementById('graficoResultadoLagrange').src = result.grafico;
    }
    
    // Mostrar información
    document.getElementById('gradoInfoLagrange').textContent = result.grado || 'N/A';
    document.getElementById('mensajeInfoLagrange').textContent = result.mensaje || '';
    
    // Mostrar coeficientes
    const coefDiv = document.getElementById('coeficientesInfoLagrange');
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

// Función para mostrar errores de Lagrange
function mostrarErrorLagrange(mensaje, grafico = null) {
    const errorDiv = document.getElementById('errorDivLagrange');
    document.getElementById('errorMensajeLagrange').textContent = mensaje;
    
    if (grafico) {
        document.getElementById('graficoErrorLagrange').src = grafico;
        document.getElementById('errorGraficoLagrange').style.display = 'block';
    } else {
        document.getElementById('errorGraficoLagrange').style.display = 'none';
    }
    
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Función para limpiar el formulario de Lagrange
function limpiarFormularioLagrange() {
    // Limpiar la tabla de puntos
    document.getElementById('puntosBodyLagrange').innerHTML = '';
    puntosCountLagrange = 0;
    
    // Agregar 2 puntos por defecto
    agregarPuntoLagrange();
    agregarPuntoLagrange();
    
    // Ocultar resultados y errores
    document.getElementById('resultadoLagrange').style.display = 'none';
    document.getElementById('errorDivLagrange').style.display = 'none';
}

// Funciones para cargar ejemplos de Lagrange
function cargarEjemploLagrangeLineal() {
    limpiarFormularioLagrange();
    
    // Ejemplo lineal: y = 2x + 2
    document.getElementById('x-lagrange-1').value = 0;
    document.getElementById('y-lagrange-1').value = 2;
    document.getElementById('x-lagrange-2').value = 5;
    document.getElementById('y-lagrange-2').value = 12;
}

function cargarEjemploLagrangeCuadratico() {
    limpiarFormularioLagrange();
    
    // Agregar un punto más (necesitamos 3 para cuadrática)
    agregarPuntoLagrange();
    
    // Ejemplo cuadrático: y = x²
    document.getElementById('x-lagrange-1').value = 0;
    document.getElementById('y-lagrange-1').value = 0;
    document.getElementById('x-lagrange-2').value = 1;
    document.getElementById('y-lagrange-2').value = 1;
    document.getElementById('x-lagrange-3').value = 2;
    document.getElementById('y-lagrange-3').value = 4;
}

function cargarEjemploLagrangeCubico() {
    limpiarFormularioLagrange();
    
    // Agregar puntos necesarios (4 para cúbica)
    agregarPuntoLagrange();
    agregarPuntoLagrange();
    
    // Ejemplo cúbico
    document.getElementById('x-lagrange-1').value = -1;
    document.getElementById('y-lagrange-1').value = 0;
    document.getElementById('x-lagrange-2').value = 0;
    document.getElementById('y-lagrange-2').value = 1;
    document.getElementById('x-lagrange-3').value = 1;
    document.getElementById('y-lagrange-3').value = 0;
    document.getElementById('x-lagrange-4').value = 2;
    document.getElementById('y-lagrange-4').value = -3;
}

