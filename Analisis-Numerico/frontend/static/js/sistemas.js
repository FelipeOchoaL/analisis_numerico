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

// ====================================
// MÉTODOS ITERATIVOS
// ====================================

// Generar matriz para métodos iterativos
function generarMatrizIterativa(metodo) {
    const n = parseInt(document.getElementById(`${metodo}_dimension`).value);
    const container = document.getElementById(`${metodo}_matriz_container`);
    
    let html = '<h6>Sistema de ecuaciones: Ax = b</h6>';
    html += '<div class="row">';
    html += '<div class="col-md-8"><label class="form-label">Matriz A:</label><div class="mb-3">';
    
    for(let i = 0; i < n; i++) {
        for(let j = 0; j < n; j++) {
            html += `<input type="number" step="any" class="form-control d-inline-block matrix-input me-1 mb-1" 
                     id="${metodo}_a_${i}_${j}" value="0" required>`;
        }
        html += '<br>';
    }
    
    html += '</div></div>';
    html += '<div class="col-md-2"><label class="form-label">Vector b:</label><div class="mb-3">';
    
    for(let i = 0; i < n; i++) {
        html += `<input type="number" step="any" class="form-control matrix-input mb-1" 
                 id="${metodo}_b_${i}" value="0" required><br>`;
    }
    
    html += '</div></div>';
    html += '<div class="col-md-2"><label class="form-label">X0 inicial:</label><div class="mb-3">';
    
    for(let i = 0; i < n; i++) {
        html += `<input type="number" step="any" class="form-control matrix-input mb-1" 
                 id="${metodo}_x0_${i}" value="0" required><br>`;
    }
    
    html += '</div></div></div>';
    container.innerHTML = html;
}

// Inicializar matrices al cargar
document.addEventListener('DOMContentLoaded', function() {
    generarMatrizIterativa('jacobi');
    generarMatrizIterativa('gs');
    generarMatrizIterativa('sor');
    generarMatrizIterativa('comp');
});

// Event listener para Jacobi
document.getElementById('jacobiForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const n = parseInt(document.getElementById('jacobi_dimension').value);
    
    const A = [], b = [], x0 = [];
    for(let i = 0; i < n; i++) {
        A[i] = [];
        for(let j = 0; j < n; j++) {
            A[i][j] = parseFloat(document.getElementById(`jacobi_a_${i}_${j}`).value);
        }
        b[i] = parseFloat(document.getElementById(`jacobi_b_${i}`).value);
        x0[i] = parseFloat(document.getElementById(`jacobi_x0_${i}`).value);
    }
    
    const datos = {
        A: A,
        b: b,
        x0: x0,
        tolerancia: parseFloat(document.getElementById('jacobi_tolerancia').value),
        niter: parseInt(document.getElementById('jacobi_niter').value),
        modo: document.getElementById('jacobi_modo').value
    };
    
    try {
        const response = await fetch('/api/sistemas/jacobi', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(datos)
        });
        
        const resultado = await response.json();
        mostrarResultadoIterativo('jacobi', resultado);
    } catch (error) {
        mostrarErrorIterativo('jacobi', 'Error de conexión: ' + error.message);
    }
});

// Event listener para Gauss-Seidel
document.getElementById('gaussSeidelForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const n = parseInt(document.getElementById('gs_dimension').value);
    
    const A = [], b = [], x0 = [];
    for(let i = 0; i < n; i++) {
        A[i] = [];
        for(let j = 0; j < n; j++) {
            A[i][j] = parseFloat(document.getElementById(`gs_a_${i}_${j}`).value);
        }
        b[i] = parseFloat(document.getElementById(`gs_b_${i}`).value);
        x0[i] = parseFloat(document.getElementById(`gs_x0_${i}`).value);
    }
    
    const datos = {
        A: A,
        b: b,
        x0: x0,
        tolerancia: parseFloat(document.getElementById('gs_tolerancia').value),
        niter: parseInt(document.getElementById('gs_niter').value),
        modo: document.getElementById('gs_modo').value
    };
    
    try {
        const response = await fetch('/api/sistemas/gauss-seidel', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(datos)
        });
        
        const resultado = await response.json();
        mostrarResultadoIterativo('gs', resultado);
    } catch (error) {
        mostrarErrorIterativo('gs', 'Error de conexión: ' + error.message);
    }
});

// Event listener para SOR
document.getElementById('sorForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const n = parseInt(document.getElementById('sor_dimension').value);
    
    const A = [], b = [], x0 = [];
    for(let i = 0; i < n; i++) {
        A[i] = [];
        for(let j = 0; j < n; j++) {
            A[i][j] = parseFloat(document.getElementById(`sor_a_${i}_${j}`).value);
        }
        b[i] = parseFloat(document.getElementById(`sor_b_${i}`).value);
        x0[i] = parseFloat(document.getElementById(`sor_x0_${i}`).value);
    }
    
    const datos = {
        A: A,
        b: b,
        x0: x0,
        tolerancia: parseFloat(document.getElementById('sor_tolerancia').value),
        niter: parseInt(document.getElementById('sor_niter').value),
        w: parseFloat(document.getElementById('sor_omega').value),
        modo: document.getElementById('sor_modo').value
    };
    
    try {
        const response = await fetch('/api/sistemas/sor', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(datos)
        });
        
        const resultado = await response.json();
        mostrarResultadoIterativo('sor', resultado);
    } catch (error) {
        mostrarErrorIterativo('sor', 'Error de conexión: ' + error.message);
    }
});

// Event listener para Comparación
document.getElementById('comparacionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const n = parseInt(document.getElementById('comp_dimension').value);
    
    const A = [], b = [], x0 = [];
    for(let i = 0; i < n; i++) {
        A[i] = [];
        for(let j = 0; j < n; j++) {
            A[i][j] = parseFloat(document.getElementById(`comp_a_${i}_${j}`).value);
        }
        b[i] = parseFloat(document.getElementById(`comp_b_${i}`).value);
        x0[i] = parseFloat(document.getElementById(`comp_x0_${i}`).value);
    }
    
    const datos = {
        A: A,
        b: b,
        x0: x0,
        tolerancia: parseFloat(document.getElementById('comp_tolerancia').value),
        niter: parseInt(document.getElementById('comp_niter').value),
        w: parseFloat(document.getElementById('comp_omega').value),
        modo: document.getElementById('comp_modo').value
    };
    
    try {
        const response = await fetch('/api/sistemas/comparar-iterativos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(datos)
        });
        
        const resultado = await response.json();
        mostrarResultadoComparacion(resultado);
    } catch (error) {
        mostrarErrorIterativo('comp', 'Error de conexión: ' + error.message);
    }
});

// Mostrar resultado de método iterativo
function mostrarResultadoIterativo(metodo, resultado) {
    const container = document.getElementById(`${metodo}_resultado`);
    
    if (!resultado.exito) {
        container.innerHTML = `
            <div class="alert alert-danger">
                <h6><i class="fas fa-exclamation-triangle"></i> ${resultado.mensaje}</h6>
            </div>
        `;
        container.style.display = 'block';
        return;
    }
    
    let html = `
        <div class="card">
            <div class="card-header ${resultado.exito ? 'bg-success' : 'bg-warning'} text-white">
                <h6><i class="fas fa-check-circle"></i> ${resultado.mensaje}</h6>
            </div>
            <div class="card-body">
                <div class="solution-highlight">
                    <h6>Solución encontrada:</h6>
                    <p class="mb-0"><strong>x = [${resultado.solucion.map(v => v.toFixed(8)).join(', ')}]</strong></p>
                </div>
                <div class="row mt-3">
                    <div class="col-md-4">
                        <p><strong>Iteraciones:</strong> ${resultado.iteraciones}</p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Error final:</strong> ${resultado.error_final.toExponential(4)}</p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Radio espectral:</strong> ${resultado.radio_espectral.toFixed(6)}</p>
                    </div>
                </div>
                ${resultado.converge_teorico ? 
                    '<div class="alert alert-success">✓ Convergencia garantizada (ρ < 1)</div>' : 
                    '<div class="alert alert-warning">⚠ Convergencia no garantizada (ρ ≥ 1)</div>'}
                <h6 class="mt-3">Tabla de iteraciones:</h6>
                <div class="table-responsive">
                    ${resultado.tabla_html}
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

// Mostrar resultado de comparación
function mostrarResultadoComparacion(resultado) {
    const container = document.getElementById('comp_resultado');
    
    if (!resultado.exito) {
        container.innerHTML = `
            <div class="alert alert-danger">
                <h6><i class="fas fa-exclamation-triangle"></i> ${resultado.mensaje}</h6>
            </div>
        `;
        container.style.display = 'block';
        return;
    }
    
    let html = `
        <div class="card">
            <div class="card-header bg-info text-white">
                <h6><i class="fas fa-chart-bar"></i> ${resultado.mensaje}</h6>
            </div>
            <div class="card-body">
                <!-- Resumen Ejecutivo -->
                <div class="alert alert-success mb-4">
                    <h5 class="alert-heading"><i class="fas fa-trophy"></i> Resumen Ejecutivo</h5>
                    <div class="row">
                        <div class="col-md-4">
                            <p class="mb-1"><strong>🏆 MEJOR MÉTODO:</strong></p>
                            <h4 class="text-success">${resultado.mejor_metodo}</h4>
                            <small>Puntuación: ${resultado.informe.puntuacion_mejor.toFixed(1)}/100</small>
                        </div>
                        <div class="col-md-4">
                            <p class="mb-1"><strong>⏱️ Más rápido:</strong></p>
                            <h5>${resultado.metodo_mas_rapido}</h5>
                            <small>${(resultado.tiempo_mas_rapido * 1000).toFixed(3)} ms</small>
                        </div>
                        <div class="col-md-4">
                            <p class="mb-1"><strong>🔄 Menos iteraciones:</strong></p>
                            <h5>${resultado.metodo_menos_iteraciones}</h5>
                            <small>Métodos exitosos: ${resultado.total_metodos_exitosos}/3</small>
                        </div>
                    </div>
                </div>
                
                <!-- Gráficos -->
                <div class="row mb-4">
                    <div class="col-md-6">
                        <h6 class="text-center">Comparación de Tiempos</h6>
                        ${resultado.grafico_tiempos ? 
                            `<img src="${resultado.grafico_tiempos}" class="img-fluid" alt="Gráfico de tiempos">` : 
                            '<p class="text-muted text-center">No disponible</p>'}
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-center">Evolución del Error</h6>
                        ${resultado.grafico_convergencia ? 
                            `<img src="${resultado.grafico_convergencia}" class="img-fluid" alt="Gráfico de convergencia">` : 
                            '<p class="text-muted text-center">No disponible</p>'}
                    </div>
                </div>
                
                <!-- Tabla Comparativa Completa -->
                <h6 class="mt-4"><i class="fas fa-table"></i> Tabla Comparativa de Resultados</h6>
                <div class="table-responsive">
                    ${resultado.informe.tabla_comparativa}
                </div>
                
                <!-- Tiempos de Ejecución Detallados -->
                <div class="card mt-3">
                    <div class="card-header bg-light">
                        <strong><i class="fas fa-clock"></i> Tiempos de Ejecución Detallados</strong>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            ${Object.entries(resultado.tiempos).map(([metodo, tiempo]) => `
                                <div class="col-md-4">
                                    <div class="text-center p-2 ${metodo === resultado.metodo_mas_rapido ? 'bg-success text-white rounded' : ''}">
                                        <strong>${metodo}</strong><br>
                                        <span class="h5">${tiempo.toFixed(3)} ms</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
                
                <!-- Análisis de Convergencia -->
                ${resultado.informe.nota_convergencia || resultado.informe.nota_error ? `
                <div class="alert alert-info mt-3">
                    <h6><i class="fas fa-chart-line"></i> Análisis de Convergencia y Errores</h6>
                    ${resultado.informe.nota_convergencia ? `<p class="mb-2">${resultado.informe.nota_convergencia}</p>` : ''}
                    ${resultado.informe.nota_error ? `<p class="mb-2">${resultado.informe.nota_error}</p>` : ''}
                    ${resultado.informe.comparacion_radios ? `
                        <hr>
                        <p class="mb-1"><strong>Comparación de Radios Espectrales:</strong></p>
                        <ul class="mb-0">
                            ${resultado.informe.comparacion_radios.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
                ` : ''}
                
                <!-- Recomendación Final -->
                <div class="alert alert-warning mt-3">
                    <h6><i class="fas fa-lightbulb"></i> Recomendación y Análisis</h6>
                    <div style="white-space: pre-line;">${resultado.informe.recomendacion}</div>
                </div>
                
                <!-- Características por Método -->
                <h6 class="mt-4"><i class="fas fa-info-circle"></i> Características Detalladas de Cada Método</h6>
                <div class="accordion mt-3" id="accordionCaracteristicas">
                    ${Object.entries(resultado.informe.caracteristicas).map(([metodo, carac], index) => `
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button ${index !== 0 ? 'collapsed' : ''}" type="button" 
                                        data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                                    <strong>${metodo}</strong> ${carac.estado ? `<span class="ms-2">${carac.estado}</span>` : ''}
                                </button>
                            </h2>
                            <div id="collapse${index}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}" 
                                 data-bs-parent="#accordionCaracteristicas">
                                <div class="accordion-body">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><strong>✓ Ventajas:</strong></p>
                                            <ul>
                                                ${carac.ventajas.map(v => `<li>${v}</li>`).join('')}
                                            </ul>
                                        </div>
                                        <div class="col-md-6">
                                            <p><strong>✗ Desventajas:</strong></p>
                                            <ul>
                                                ${carac.desventajas.map(d => `<li>${d}</li>`).join('')}
                                            </ul>
                                        </div>
                                    </div>
                                    <hr>
                                    <p><strong>📈 Tipo de Convergencia:</strong> ${carac.convergencia}</p>
                                    <p><strong>💡 Mejor uso:</strong> ${carac.mejor_uso}</p>
                                    <div class="row mt-2">
                                        <div class="col-md-6">
                                            <p class="mb-0"><strong>Radio espectral (ρ):</strong> ${carac.radio_espectral}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p class="mb-0"><strong>¿Converge teóricamente?</strong> ${carac.converge}</p>
                                        </div>
                                    </div>
                                    ${carac.omega_usado ? `<p class="mt-2 mb-0"><strong>Parámetro ω usado:</strong> ${carac.omega_usado}</p>` : ''}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

// Mostrar error
function mostrarErrorIterativo(metodo, mensaje) {
    const container = document.getElementById(`${metodo}_resultado`);
    container.innerHTML = `
        <div class="alert alert-danger">
            <h6><i class="fas fa-exclamation-triangle"></i> Error</h6>
            <p class="mb-0">${mensaje}</p>
        </div>
    `;
    container.style.display = 'block';
}

// Cargar ejemplos para métodos iterativos
function cargarEjemploIterativo(metodo, ejemplo) {
    if (ejemplo === 'ejemplo1') {
        // Sistema 3x3 diagonalmente dominante
        document.getElementById(`${metodo}_dimension`).value = '3';
        generarMatrizIterativa(metodo);
        
        // Matriz A
        const A = [[4, -1, 0], [- 1, 4, -1], [0, -1, 4]];
        const b = [15, 10, 10];
        const x0 = [0, 0, 0];
        
        setTimeout(() => {
            for(let i = 0; i < 3; i++) {
                for(let j = 0; j < 3; j++) {
                    document.getElementById(`${metodo}_a_${i}_${j}`).value = A[i][j];
                }
                document.getElementById(`${metodo}_b_${i}`).value = b[i];
                document.getElementById(`${metodo}_x0_${i}`).value = x0[i];
            }
        }, 100);
    } else if (ejemplo === 'ejemplo2') {
        // Sistema 3x3
        document.getElementById(`${metodo}_dimension`).value = '3';
        generarMatrizIterativa(metodo);
        
        const A = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]];
        const b = [6, 25, -11];
        const x0 = [0, 0, 0];
        
        setTimeout(() => {
            for(let i = 0; i < 3; i++) {
                for(let j = 0; j < 3; j++) {
                    document.getElementById(`${metodo}_a_${i}_${j}`).value = A[i][j];
                }
                document.getElementById(`${metodo}_b_${i}`).value = b[i];
                document.getElementById(`${metodo}_x0_${i}`).value = x0[i];
            }
        }, 100);
    }
}

