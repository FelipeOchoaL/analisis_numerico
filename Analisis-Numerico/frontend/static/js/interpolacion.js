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

// ==================== SPLINE LINEAL ====================

let puntosCountSplineLineal = 0;

// Inicializar Spline Lineal cuando se active el tab
document.getElementById('spline-lineal-tab').addEventListener('shown.bs.tab', function() {
    if (puntosCountSplineLineal === 0) {
        agregarPuntoSplineLineal();
        agregarPuntoSplineLineal();
    }
});

function agregarPuntoSplineLineal() {
    if (puntosCountSplineLineal >= MAX_PUNTOS) {
        alert(`Solo se permiten máximo ${MAX_PUNTOS} puntos`);
        return;
    }
    
    puntosCountSplineLineal++;
    const container = document.getElementById('puntosContainerSplineLineal');
    const puntoDiv = document.createElement('div');
    puntoDiv.className = 'input-group mb-2';
    puntoDiv.id = `punto-splinelin-${puntosCountSplineLineal}`;
    
    puntoDiv.innerHTML = `
        <span class="input-group-text">#${puntosCountSplineLineal}</span>
        <span class="input-group-text">x:</span>
        <input type="number" step="any" class="form-control punto-input" 
               id="x-splinelin-${puntosCountSplineLineal}" placeholder="x${puntosCountSplineLineal}" required>
        <span class="input-group-text">y:</span>
        <input type="number" step="any" class="form-control punto-input" 
               id="y-splinelin-${puntosCountSplineLineal}" placeholder="y${puntosCountSplineLineal}" required>
        <button type="button" class="btn btn-danger btn-sm" 
                onclick="eliminarPuntoSplineLineal(${puntosCountSplineLineal})">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    container.appendChild(puntoDiv);
    actualizarContadorSplineLineal();
    actualizarBotonAgregarSplineLineal();
}

function eliminarPuntoSplineLineal(id) {
    if (puntosCountSplineLineal <= 2) {
        alert('Debe haber al menos 2 puntos');
        return;
    }
    
    const punto = document.getElementById(`punto-splinelin-${id}`);
    if (punto) {
        punto.remove();
        puntosCountSplineLineal--;
        renumerarPuntosSplineLineal();
        actualizarContadorSplineLineal();
        actualizarBotonAgregarSplineLineal();
    }
}

function renumerarPuntosSplineLineal() {
    const container = document.getElementById('puntosContainerSplineLineal');
    const puntos = container.children;
    puntosCountSplineLineal = 0;
    
    Array.from(puntos).forEach((punto, index) => {
        puntosCountSplineLineal++;
        const newId = puntosCountSplineLineal;
        punto.id = `punto-splinelin-${newId}`;
        
        const number = punto.querySelector('.input-group-text');
        number.textContent = `#${newId}`;
        
        const xInput = punto.querySelector('input[id^="x-splinelin-"]');
        const yInput = punto.querySelector('input[id^="y-splinelin-"]');
        const xValue = xInput.value;
        const yValue = yInput.value;
        
        xInput.id = `x-splinelin-${newId}`;
        yInput.id = `y-splinelin-${newId}`;
        xInput.value = xValue;
        yInput.value = yValue;
        xInput.placeholder = `x${newId}`;
        yInput.placeholder = `y${newId}`;
        
        const deleteBtn = punto.querySelector('button');
        deleteBtn.setAttribute('onclick', `eliminarPuntoSplineLineal(${newId})`);
    });
}

function actualizarContadorSplineLineal() {
    document.getElementById('contadorPuntosSplineLineal').textContent = puntosCountSplineLineal;
}

function actualizarBotonAgregarSplineLineal() {
    const btn = document.getElementById('btnAgregarPuntoSplineLineal');
    btn.disabled = puntosCountSplineLineal >= MAX_PUNTOS;
}

// Event listener para el botón de agregar punto
document.addEventListener('DOMContentLoaded', function() {
    const btnAgregar = document.getElementById('btnAgregarPuntoSplineLineal');
    if (btnAgregar) {
        btnAgregar.addEventListener('click', agregarPuntoSplineLineal);
    }
});

async function calcularSplineLineal() {
    // Ocultar resultados y errores anteriores
    document.getElementById('resultadoSplineLineal').style.display = 'none';
    document.getElementById('errorDivSplineLineal').style.display = 'none';
    document.getElementById('loadingSplineLineal').style.display = 'block';
    
    // Obtener valores
    const x = [];
    const y = [];
    
    for (let i = 1; i <= puntosCountSplineLineal; i++) {
        const xVal = parseFloat(document.getElementById(`x-splinelin-${i}`).value);
        const yVal = parseFloat(document.getElementById(`y-splinelin-${i}`).value);
        x.push(xVal);
        y.push(yVal);
    }
    
    try {
        const response = await fetch('/api/spline-lineal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ x, y })
        });
        
        const data = await response.json();
        document.getElementById('loadingSplineLineal').style.display = 'none';
        
        if (data.exito) {
            mostrarResultadoSplineLineal(data);
        } else {
            mostrarErrorSplineLineal(data.mensaje, data.grafico);
        }
    } catch (error) {
        document.getElementById('loadingSplineLineal').style.display = 'none';
        mostrarErrorSplineLineal('Error de conexión con el servidor: ' + error.message);
    }
}

function mostrarResultadoSplineLineal(data) {
    // Mostrar polinomios por tramo
    const polinomiosDiv = document.getElementById('polinomioResultadoSplineLineal');
    polinomiosDiv.innerHTML = data.polinomios.map(pol => `<div class="mb-1">${pol}</div>`).join('');
    
    // Mostrar gráfico
    if (data.grafico) {
        document.getElementById('graficoResultadoSplineLineal').src = data.grafico;
    }
    
    // Mostrar información
    document.getElementById('numTramosSplineLineal').textContent = data.tramos ? data.tramos.length : 'N/A';
    document.getElementById('mensajeInfoSplineLineal').textContent = data.mensaje;
    
    // Mostrar resultados
    document.getElementById('resultadoSplineLineal').style.display = 'block';
}

function mostrarErrorSplineLineal(mensaje, grafico = null) {
    document.getElementById('errorMensajeSplineLineal').textContent = mensaje;
    
    if (grafico) {
        document.getElementById('graficoErrorSplineLineal').src = grafico;
        document.getElementById('errorGraficoSplineLineal').style.display = 'block';
    } else {
        document.getElementById('errorGraficoSplineLineal').style.display = 'none';
    }
    
    document.getElementById('errorDivSplineLineal').style.display = 'block';
}

function limpiarFormularioSplineLineal() {
    // Eliminar todos los puntos
    const container = document.getElementById('puntosContainerSplineLineal');
    container.innerHTML = '';
    puntosCountSplineLineal = 0;
    
    // Agregar 2 puntos por defecto
    agregarPuntoSplineLineal();
    agregarPuntoSplineLineal();
    
    // Ocultar resultados y errores
    document.getElementById('resultadoSplineLineal').style.display = 'none';
    document.getElementById('errorDivSplineLineal').style.display = 'none';
}

// Funciones para cargar ejemplos de Spline Lineal
function cargarEjemploSplineLinealLineal() {
    limpiarFormularioSplineLineal();
    
    document.getElementById('x-splinelin-1').value = 0;
    document.getElementById('y-splinelin-1').value = 2;
    document.getElementById('x-splinelin-2').value = 5;
    document.getElementById('y-splinelin-2').value = 12;
}

function cargarEjemploSplineLinealCuadratico() {
    limpiarFormularioSplineLineal();
    agregarPuntoSplineLineal();
    
    document.getElementById('x-splinelin-1').value = 0;
    document.getElementById('y-splinelin-1').value = 0;
    document.getElementById('x-splinelin-2').value = 1;
    document.getElementById('y-splinelin-2').value = 1;
    document.getElementById('x-splinelin-3').value = 2;
    document.getElementById('y-splinelin-3').value = 4;
}

function cargarEjemploSplineLinealCubico() {
    limpiarFormularioSplineLineal();
    agregarPuntoSplineLineal();
    agregarPuntoSplineLineal();
    
    document.getElementById('x-splinelin-1').value = -1;
    document.getElementById('y-splinelin-1').value = 0;
    document.getElementById('x-splinelin-2').value = 0;
    document.getElementById('y-splinelin-2').value = 1;
    document.getElementById('x-splinelin-3').value = 1;
    document.getElementById('y-splinelin-3').value = 0;
    document.getElementById('x-splinelin-4').value = 2;
    document.getElementById('y-splinelin-4').value = -3;
}

// ==================== SPLINE CÚBICO ====================

let puntosCountSplineCubico = 0;

// Inicializar Spline Cúbico cuando se active el tab
document.getElementById('spline-cubico-tab').addEventListener('shown.bs.tab', function() {
    if (puntosCountSplineCubico === 0) {
        agregarPuntoSplineCubico();
        agregarPuntoSplineCubico();
    }
});

function agregarPuntoSplineCubico() {
    if (puntosCountSplineCubico >= MAX_PUNTOS) {
        alert(`Solo se permiten máximo ${MAX_PUNTOS} puntos`);
        return;
    }
    
    puntosCountSplineCubico++;
    const container = document.getElementById('puntosContainerSplineCubico');
    const puntoDiv = document.createElement('div');
    puntoDiv.className = 'input-group mb-2';
    puntoDiv.id = `punto-splinecub-${puntosCountSplineCubico}`;
    
    puntoDiv.innerHTML = `
        <span class="input-group-text">#${puntosCountSplineCubico}</span>
        <span class="input-group-text">x:</span>
        <input type="number" step="any" class="form-control punto-input" 
               id="x-splinecub-${puntosCountSplineCubico}" placeholder="x${puntosCountSplineCubico}" required>
        <span class="input-group-text">y:</span>
        <input type="number" step="any" class="form-control punto-input" 
               id="y-splinecub-${puntosCountSplineCubico}" placeholder="y${puntosCountSplineCubico}" required>
        <button type="button" class="btn btn-danger btn-sm" 
                onclick="eliminarPuntoSplineCubico(${puntosCountSplineCubico})">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    container.appendChild(puntoDiv);
    actualizarContadorSplineCubico();
    actualizarBotonAgregarSplineCubico();
}

function eliminarPuntoSplineCubico(id) {
    if (puntosCountSplineCubico <= 2) {
        alert('Debe haber al menos 2 puntos');
        return;
    }
    
    const punto = document.getElementById(`punto-splinecub-${id}`);
    if (punto) {
        punto.remove();
        puntosCountSplineCubico--;
        renumerarPuntosSplineCubico();
        actualizarContadorSplineCubico();
        actualizarBotonAgregarSplineCubico();
    }
}

function renumerarPuntosSplineCubico() {
    const container = document.getElementById('puntosContainerSplineCubico');
    const puntos = container.children;
    puntosCountSplineCubico = 0;
    
    Array.from(puntos).forEach((punto, index) => {
        puntosCountSplineCubico++;
        const newId = puntosCountSplineCubico;
        punto.id = `punto-splinecub-${newId}`;
        
        const number = punto.querySelector('.input-group-text');
        number.textContent = `#${newId}`;
        
        const xInput = punto.querySelector('input[id^="x-splinecub-"]');
        const yInput = punto.querySelector('input[id^="y-splinecub-"]');
        const xValue = xInput.value;
        const yValue = yInput.value;
        
        xInput.id = `x-splinecub-${newId}`;
        yInput.id = `y-splinecub-${newId}`;
        xInput.value = xValue;
        yInput.value = yValue;
        xInput.placeholder = `x${newId}`;
        yInput.placeholder = `y${newId}`;
        
        const deleteBtn = punto.querySelector('button');
        deleteBtn.setAttribute('onclick', `eliminarPuntoSplineCubico(${newId})`);
    });
}

function actualizarContadorSplineCubico() {
    document.getElementById('contadorPuntosSplineCubico').textContent = puntosCountSplineCubico;
}

function actualizarBotonAgregarSplineCubico() {
    const btn = document.getElementById('btnAgregarPuntoSplineCubico');
    btn.disabled = puntosCountSplineCubico >= MAX_PUNTOS;
}

// Event listener para el botón de agregar punto
document.addEventListener('DOMContentLoaded', function() {
    const btnAgregar = document.getElementById('btnAgregarPuntoSplineCubico');
    if (btnAgregar) {
        btnAgregar.addEventListener('click', agregarPuntoSplineCubico);
    }
});

async function calcularSplineCubico() {
    // Ocultar resultados y errores anteriores
    document.getElementById('resultadoSplineCubico').style.display = 'none';
    document.getElementById('errorDivSplineCubico').style.display = 'none';
    document.getElementById('loadingSplineCubico').style.display = 'block';
    
    // Obtener valores
    const x = [];
    const y = [];
    
    for (let i = 1; i <= puntosCountSplineCubico; i++) {
        const xVal = parseFloat(document.getElementById(`x-splinecub-${i}`).value);
        const yVal = parseFloat(document.getElementById(`y-splinecub-${i}`).value);
        x.push(xVal);
        y.push(yVal);
    }
    
    try {
        const response = await fetch('/api/spline-cubico', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ x, y })
        });
        
        const data = await response.json();
        document.getElementById('loadingSplineCubico').style.display = 'none';
        
        if (data.exito) {
            mostrarResultadoSplineCubico(data);
        } else {
            mostrarErrorSplineCubico(data.mensaje, data.grafico);
        }
    } catch (error) {
        document.getElementById('loadingSplineCubico').style.display = 'none';
        mostrarErrorSplineCubico('Error de conexión con el servidor: ' + error.message);
    }
}

function mostrarResultadoSplineCubico(data) {
    // Mostrar polinomios por tramo
    const polinomiosDiv = document.getElementById('polinomioResultadoSplineCubico');
    polinomiosDiv.innerHTML = data.polinomios.map(pol => `<div class="mb-1">${pol}</div>`).join('');
    
    // Mostrar gráfico
    if (data.grafico) {
        document.getElementById('graficoResultadoSplineCubico').src = data.grafico;
    }
    
    // Mostrar información
    document.getElementById('numTramosSplineCubico').textContent = data.tramos ? data.tramos.length : 'N/A';
    document.getElementById('mensajeInfoSplineCubico').textContent = data.mensaje;
    
    // Mostrar resultados
    document.getElementById('resultadoSplineCubico').style.display = 'block';
}

function mostrarErrorSplineCubico(mensaje, grafico = null) {
    document.getElementById('errorMensajeSplineCubico').textContent = mensaje;
    
    if (grafico) {
        document.getElementById('graficoErrorSplineCubico').src = grafico;
        document.getElementById('errorGraficoSplineCubico').style.display = 'block';
    } else {
        document.getElementById('errorGraficoSplineCubico').style.display = 'none';
    }
    
    document.getElementById('errorDivSplineCubico').style.display = 'block';
}

function limpiarFormularioSplineCubico() {
    // Eliminar todos los puntos
    const container = document.getElementById('puntosContainerSplineCubico');
    container.innerHTML = '';
    puntosCountSplineCubico = 0;
    
    // Agregar 2 puntos por defecto
    agregarPuntoSplineCubico();
    agregarPuntoSplineCubico();
    
    // Ocultar resultados y errores
    document.getElementById('resultadoSplineCubico').style.display = 'none';
    document.getElementById('errorDivSplineCubico').style.display = 'none';
}

// Funciones para cargar ejemplos de Spline Cúbico
function cargarEjemploSplineCubicoLineal() {
    limpiarFormularioSplineCubico();
    
    document.getElementById('x-splinecub-1').value = 0;
    document.getElementById('y-splinecub-1').value = 2;
    document.getElementById('x-splinecub-2').value = 5;
    document.getElementById('y-splinecub-2').value = 12;
}

function cargarEjemploSplineCubicoCuadratico() {
    limpiarFormularioSplineCubico();
    agregarPuntoSplineCubico();
    
    document.getElementById('x-splinecub-1').value = 0;
    document.getElementById('y-splinecub-1').value = 0;
    document.getElementById('x-splinecub-2').value = 1;
    document.getElementById('y-splinecub-2').value = 1;
    document.getElementById('x-splinecub-3').value = 2;
    document.getElementById('y-splinecub-3').value = 4;
}

function cargarEjemploSplineCubicoCubico() {
    limpiarFormularioSplineCubico();
    agregarPuntoSplineCubico();
    agregarPuntoSplineCubico();
    
    document.getElementById('x-splinecub-1').value = -1;
    document.getElementById('y-splinecub-1').value = 0;
    document.getElementById('x-splinecub-2').value = 0;
    document.getElementById('y-splinecub-2').value = 1;
    document.getElementById('x-splinecub-3').value = 1;
    document.getElementById('y-splinecub-3').value = 0;
    document.getElementById('x-splinecub-4').value = 2;
    document.getElementById('y-splinecub-4').value = -3;
}

