// Variables globales
let currentDimension = 3;

// Inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    updateMatrixSize();
});

// Establecer dimensión predefinida
function setDimension(n) {
    document.getElementById('dimension').value = n;
    updateMatrixSize();
}

// Actualizar el tamaño de la matriz
function updateMatrixSize() {
    const dimension = parseInt(document.getElementById('dimension').value);
    if (dimension < 2 || dimension > 10) {
        mostrarError('La dimensión debe estar entre 2 y 10');
        return;
    }
    
    currentDimension = dimension;
    generarMatriz();
}

// Generar la matriz visual
function generarMatriz() {
    const container = document.getElementById('sistemaContainer');
    container.innerHTML = '';
    
    // Crear estructura: [A] {x} = {b}
    const sistemaDiv = document.createElement('div');
    sistemaDiv.className = 'd-flex align-items-center justify-content-center flex-wrap gap-3';
    
    // Matriz A con corchetes
    const matrizAContainer = document.createElement('div');
    matrizAContainer.className = 'matrix-container d-flex align-items-center';
    
    const bracketLeft = document.createElement('span');
    bracketLeft.className = 'bracket text-primary';
    bracketLeft.textContent = '[';
    
    const matrizA = document.createElement('div');
    matrizA.className = 'mx-2';
    
    for (let i = 0; i < currentDimension; i++) {
        const fila = document.createElement('div');
        fila.className = 'd-flex gap-1 mb-1';
        
        for (let j = 0; j < currentDimension; j++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.step = 'any';
            input.className = 'form-control form-control-sm matrix-input';
            input.id = `a_${i}_${j}`;
            input.placeholder = '0';
            fila.appendChild(input);
        }
        matrizA.appendChild(fila);
    }
    
    const bracketRight = document.createElement('span');
    bracketRight.className = 'bracket text-primary';
    bracketRight.textContent = ']';
    
    matrizAContainer.appendChild(bracketLeft);
    matrizAContainer.appendChild(matrizA);
    matrizAContainer.appendChild(bracketRight);
    
    // Vector x
    const vectorX = document.createElement('div');
    vectorX.className = 'matrix-container d-flex align-items-center';
    
    const bracketLeftX = document.createElement('span');
    bracketLeftX.className = 'bracket text-success';
    bracketLeftX.textContent = '[';
    
    const matrizX = document.createElement('div');
    matrizX.className = 'mx-2';
    
    for (let i = 0; i < currentDimension; i++) {
        const fila = document.createElement('div');
        fila.className = 'mb-1';
        fila.innerHTML = `<span class="badge bg-success">x<sub>${i+1}</sub></span>`;
        matrizX.appendChild(fila);
    }
    
    const bracketRightX = document.createElement('span');
    bracketRightX.className = 'bracket text-success';
    bracketRightX.textContent = ']';
    
    vectorX.appendChild(bracketLeftX);
    vectorX.appendChild(matrizX);
    vectorX.appendChild(bracketRightX);
    
    // Signo igual
    const equalsSign = document.createElement('span');
    equalsSign.className = 'equals-sign text-dark';
    equalsSign.textContent = '=';
    
    // Vector b
    const vectorB = document.createElement('div');
    vectorB.className = 'matrix-container d-flex align-items-center';
    
    const bracketLeftB = document.createElement('span');
    bracketLeftB.className = 'bracket text-warning';
    bracketLeftB.textContent = '[';
    
    const matrizB = document.createElement('div');
    matrizB.className = 'mx-2';
    
    for (let i = 0; i < currentDimension; i++) {
        const fila = document.createElement('div');
        fila.className = 'mb-1';
        
        const input = document.createElement('input');
        input.type = 'number';
        input.step = 'any';
        input.className = 'form-control form-control-sm matrix-input';
        input.id = `b_${i}`;
        input.placeholder = '0';
        fila.appendChild(input);
        
        matrizB.appendChild(fila);
    }
    
    const bracketRightB = document.createElement('span');
    bracketRightB.className = 'bracket text-warning';
    bracketRightB.textContent = ']';
    
    vectorB.appendChild(bracketLeftB);
    vectorB.appendChild(matrizB);
    vectorB.appendChild(bracketRightB);
    
    // Ensamblar todo
    sistemaDiv.appendChild(matrizAContainer);
    sistemaDiv.appendChild(vectorX);
    sistemaDiv.appendChild(equalsSign);
    sistemaDiv.appendChild(vectorB);
    
    container.appendChild(sistemaDiv);
}

// Cargar ejemplos predefinidos
function cargarEjemplo(tipo) {
    let A, b;
    
    switch(tipo) {
        case 'ejemplo1':
            // Sistema 3x3 bien condicionado
            setDimension(3);
            setTimeout(() => {
                A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]];
                b = [8, -11, -3];
                llenarMatriz(A, b);
            }, 100);
            break;
            
        case 'ejemplo2':
            // Otro sistema 3x3
            setDimension(3);
            setTimeout(() => {
                A = [[1, 2, 3], [2, -1, 1], [3, 0, -1]];
                b = [9, 8, 3];
                llenarMatriz(A, b);
            }, 100);
            break;
            
        case 'problema':
            // Sistema que puede requerir pivoteo
            setDimension(3);
            setTimeout(() => {
                A = [[0, 2, 3], [1, 1, 1], [2, 2, 1]];
                b = [1, 6, 10];
                llenarMatriz(A, b);
            }, 100);
            break;
    }
}

// Llenar la matriz con valores
function llenarMatriz(A, b) {
    for (let i = 0; i < A.length; i++) {
        for (let j = 0; j < A[i].length; j++) {
            const input = document.getElementById(`a_${i}_${j}`);
            if (input) input.value = A[i][j];
        }
        const inputB = document.getElementById(`b_${i}`);
        if (inputB) inputB.value = b[i];
    }
}

// Limpiar la matriz
function limpiarMatriz() {
    for (let i = 0; i < currentDimension; i++) {
        for (let j = 0; j < currentDimension; j++) {
            const input = document.getElementById(`a_${i}_${j}`);
            if (input) input.value = '';
        }
        const inputB = document.getElementById(`b_${i}`);
        if (inputB) inputB.value = '';
    }
    ocultarResultados();
}

// Obtener la matriz A del formulario
function obtenerMatrizA() {
    const A = [];
    for (let i = 0; i < currentDimension; i++) {
        const fila = [];
        for (let j = 0; j < currentDimension; j++) {
            const input = document.getElementById(`a_${i}_${j}`);
            const valor = parseFloat(input.value) || 0;
            fila.push(valor);
        }
        A.push(fila);
    }
    return A;
}

// Obtener el vector b del formulario
function obtenerVectorB() {
    const b = [];
    for (let i = 0; i < currentDimension; i++) {
        const input = document.getElementById(`b_${i}`);
        const valor = parseFloat(input.value) || 0;
        b.push(valor);
    }
    return b;
}

// Validar el sistema
async function validarSistema() {
    try {
        const A = obtenerMatrizA();
        const b = obtenerVectorB();
        
        const datos = {
            A: A,
            b: b,
            tipo_pivoteo: parseInt(document.getElementById('tipoPivoteo').value)
        };
        
        const response = await fetch('/api/validar-sistema', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarValidacion(resultado);
        } else {
            mostrarError(resultado.detail || 'Error al validar el sistema');
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    }
}

// Mostrar resultado de validación
function mostrarValidacion(resultado) {
    const container = document.getElementById('resultadosContainer');
    const content = document.getElementById('resultadosContent');
    
    let html = '<h6><i class="fas fa-check-circle"></i> Validación del Sistema</h6>';
    
    if (resultado.es_valido) {
        html += '<div class="alert alert-success">';
        html += '<i class="fas fa-check"></i> <strong>Sistema válido</strong><br>';
        html += `Determinante: ${resultado.determinante.toFixed(6)}<br>`;
        html += `Recomendación: ${resultado.recomendacion}`;
        html += '</div>';
    } else {
        html += '<div class="alert alert-warning">';
        html += '<i class="fas fa-exclamation-triangle"></i> <strong>Sistema problemático</strong><br>';
        html += 'Detalles:<br>';
        html += `• Matriz cuadrada: ${resultado.detalles.matriz_cuadrada ? 'Sí' : 'No'}<br>`;
        html += `• Dimensiones correctas: ${resultado.detalles.dimensiones_correctas ? 'Sí' : 'No'}<br>`;
        html += `• Determinante no cero: ${resultado.detalles.determinante_no_cero ? 'Sí' : 'No'}<br>`;
        if (resultado.determinante !== null) {
            html += `• Determinante: ${resultado.determinante.toFixed(6)}`;
        }
        html += '</div>';
    }
    
    content.innerHTML = html;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

// Resolver el sistema
async function resolverSistema() {
    const btnResolver = document.getElementById('btnResolver');
    const originalText = btnResolver.innerHTML;
    
    try {
        // Mostrar estado de carga
        btnResolver.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Resolviendo...';
        btnResolver.disabled = true;
        
        const A = obtenerMatrizA();
        const b = obtenerVectorB();
        const tipoPivoteo = parseInt(document.getElementById('tipoPivoteo').value);
        const mostrarProceso = document.getElementById('mostrarProceso').checked;
        
        const datos = {
            A: A,
            b: b,
            tipo_pivoteo: tipoPivoteo,
            mostrar_proceso: mostrarProceso
        };
        
        const response = await fetch('/api/gauss-pivoteo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultados(resultado);
            if (mostrarProceso && resultado.proceso) {
                mostrarProceso(resultado.proceso);
            }
        } else {
            mostrarError(resultado.detail || 'Error al resolver el sistema');
        }
    } catch (error) {
        mostrarError('Error de conexión: ' + error.message);
    } finally {
        // Restaurar botón
        btnResolver.innerHTML = originalText;
        btnResolver.disabled = false;
    }
}

// Mostrar resultados
function mostrarResultados(resultado) {
    const container = document.getElementById('resultadosContainer');
    const content = document.getElementById('resultadosContent');
    
    let html = '<h6><i class="fas fa-check-circle text-success"></i> Solución del Sistema</h6>';
    
    html += '<div class="solution-highlight">';
    html += '<h6><i class="fas fa-trophy"></i> Vector Solución</h6>';
    html += '<div class="row">';
    
    resultado.solucion.forEach((valor, i) => {
        html += '<div class="col-md-2 col-4 text-center mb-2">';
        html += `<div class="card border-success">`;
        html += `<div class="card-body p-2">`;
        html += `<small class="text-muted">x<sub>${i+1}</sub></small><br>`;
        html += `<strong>${valor.toFixed(6)}</strong>`;
        html += `</div></div></div>`;
    });
    
    html += '</div></div>';
    
    html += '<div class="mt-3">';
    html += `<p><strong>Método:</strong> ${resultado.mensaje}</p>`;
    
    if (resultado.marcador && resultado.marcador.length > 0) {
        html += '<p><strong>Marcador de variables:</strong> [' + resultado.marcador.join(', ') + ']</p>';
    }
    
    // Verificación de la solución
    html += '<div class="mt-3">';
    html += '<h6><i class="fas fa-calculator"></i> Verificación</h6>';
    html += '<p class="small text-muted">Puedes verificar la solución sustituyendo los valores en el sistema original.</p>';
    html += '</div>';
    
    html += '</div>';
    
    content.innerHTML = html;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

// Mostrar proceso paso a paso
function mostrarProcesoPasos(proceso) {
    const container = document.getElementById('procesoContainer');
    const content = document.getElementById('procesoContent');
    
    content.textContent = proceso;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

// Mostrar errores
function mostrarError(mensaje) {
    const container = document.getElementById('resultadosContainer');
    const content = document.getElementById('resultadosContent');
    
    const html = `
        <div class="alert alert-danger" role="alert">
            <h6><i class="fas fa-exclamation-triangle"></i> Error</h6>
            <p class="mb-0">${mensaje}</p>
        </div>
    `;
    
    content.innerHTML = html;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

// Ocultar resultados
function ocultarResultados() {
    document.getElementById('resultadosContainer').style.display = 'none';
    document.getElementById('procesoContainer').style.display = 'none';
}

// Función auxiliar para mostrar proceso (corregida)
function mostrarProceso(proceso) {
    mostrarProcesoPasos(proceso);
}

