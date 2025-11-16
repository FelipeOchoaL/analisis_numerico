// Error Absoluto
document.getElementById('errorAbsolutoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x_aproximado: parseFloat(document.getElementById('ea_aproximado').value),
        x_exacto: parseFloat(document.getElementById('ea_exacto').value)
    };
    
    try {
        showLoading('errorAbsolutoResultados', 'errorAbsolutoOutput');
        
        const response = await fetch('/api/error-absoluto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoErrorAbsoluto(resultado);
        } else {
            mostrarError('errorAbsolutoOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('errorAbsolutoOutput', 'Error de conexión: ' + error.message);
    }
});

// Error Relativo
document.getElementById('errorRelativoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x_aproximado: parseFloat(document.getElementById('er_aproximado').value),
        x_exacto: parseFloat(document.getElementById('er_exacto').value)
    };
    
    try {
        showLoading('errorRelativoResultados', 'errorRelativoOutput');
        
        const response = await fetch('/api/error-relativo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoErrorRelativo(resultado);
        } else {
            mostrarError('errorRelativoOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('errorRelativoOutput', 'Error de conexión: ' + error.message);
    }
});

// Propagación de Errores
document.getElementById('propagacionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x: parseFloat(document.getElementById('pe_x').value),
        ex: parseFloat(document.getElementById('pe_ex').value),
        y: parseFloat(document.getElementById('pe_y').value),
        ey: parseFloat(document.getElementById('pe_ey').value),
        operacion: document.getElementById('pe_operacion').value
    };
    
    try {
        showLoading('propagacionResultados', 'propagacionOutput');
        
        const response = await fetch('/api/propagacion-error', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoPropagacion(resultado);
        } else {
            mostrarError('propagacionOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('propagacionOutput', 'Error de conexión: ' + error.message);
    }
});

function mostrarResultadoErrorAbsoluto(resultado) {
    const outputDiv = document.getElementById('errorAbsolutoOutput');
    
    let html = `
        <div class="alert alert-success resultado-aparicion" role="alert">
            <h6><i class="fas fa-check-circle"></i> Resultado del Error Absoluto:</h6>
            <div class="resultado-resumen">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Valor Aproximado:</strong> <span class="numero-destacado">${resultado.x_aproximado}</span></p>
                        <p><strong>Valor Exacto:</strong> <span class="numero-destacado">${resultado.x_exacto}</span></p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Error Absoluto:</strong> <span class="numero-destacado">${resultado.error_absoluto.toExponential(6)}</span></p>
                        <p><strong>Fórmula:</strong> <code>|${resultado.x_exacto} - ${resultado.x_aproximado}|</code></p>
                    </div>
                </div>
            </div>
            ${resultado.tiempo_ejecucion ? `<p><small>Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(6)} segundos</small></p>` : ''}
        </div>
    `;
    
    outputDiv.innerHTML = html;
    document.getElementById('errorAbsolutoResultados').style.display = 'block';
}

function mostrarResultadoErrorRelativo(resultado) {
    const outputDiv = document.getElementById('errorRelativoOutput');
    
    let html = `
        <div class="alert alert-success resultado-aparicion" role="alert">
            <h6><i class="fas fa-check-circle"></i> Resultado del Error Relativo:</h6>
            <div class="resultado-resumen">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Valor Aproximado:</strong> <span class="numero-destacado">${resultado.x_aproximado}</span></p>
                        <p><strong>Valor Exacto:</strong> <span class="numero-destacado">${resultado.x_exacto}</span></p>
                        <p><strong>Error Absoluto:</strong> <span class="numero-destacado">${resultado.error_absoluto.toExponential(6)}</span></p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Error Relativo:</strong> <span class="numero-destacado">${resultado.error_relativo.toExponential(6)}</span></p>
                        <p><strong>Error Porcentual:</strong> <span class="numero-destacado">${resultado.error_porcentual.toFixed(4)}%</span></p>
                        <p><strong>Fórmula:</strong> <code>|${resultado.x_exacto} - ${resultado.x_aproximado}| / |${resultado.x_exacto}|</code></p>
                    </div>
                </div>
            </div>
            ${resultado.tiempo_ejecucion ? `<p><small>Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(6)} segundos</small></p>` : ''}
        </div>
    `;
    
    outputDiv.innerHTML = html;
    document.getElementById('errorRelativoResultados').style.display = 'block';
}

function mostrarResultadoPropagacion(resultado) {
    const outputDiv = document.getElementById('propagacionOutput');
    
    // Determinar símbolo de operación
    let simbolo = '';
    switch(resultado.operacion.toLowerCase()) {
        case 'suma': simbolo = '+'; break;
        case 'resta': simbolo = '-'; break;
        case 'producto': simbolo = '×'; break;
        case 'division': simbolo = '÷'; break;
    }
    
    let html = `
        <div class="alert alert-success resultado-aparicion" role="alert">
            <h6><i class="fas fa-check-circle"></i> Resultado de Propagación de Errores:</h6>
            <div class="resultado-resumen">
                <div class="row">
                    <div class="col-md-6">
                        <h6>Datos de entrada:</h6>
                        <p><strong>X =</strong> <span class="numero-destacado">${resultado.x}</span> ± <span class="numero-destacado">${resultado.ex}</span></p>
                        <p><strong>Y =</strong> <span class="numero-destacado">${resultado.y}</span> ± <span class="numero-destacado">${resultado.ey}</span></p>
                        <p><strong>Operación:</strong> X ${simbolo} Y</p>
                    </div>
                    <div class="col-md-6">
                        <h6>Resultados:</h6>
                        <p><strong>Resultado:</strong> <span class="numero-destacado">${resultado.resultado.toFixed(8)}</span></p>
                        <p><strong>Error Propagado:</strong> <span class="numero-destacado">${resultado.error_propagado.toExponential(6)}</span></p>
                        <p><strong>Error Relativo:</strong> <span class="numero-destacado">${(resultado.error_relativo_propagado * 100).toFixed(4)}%</span></p>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12">
                        <h6>Resultado Final:</h6>
                        <p class="text-center"><strong>Z = ${resultado.resultado.toFixed(6)} ± ${resultado.error_propagado.toExponential(4)}</strong></p>
                    </div>
                </div>
            </div>
            ${resultado.tiempo_ejecucion ? `<p><small>Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(6)} segundos</small></p>` : ''}
        </div>
    `;
    
    outputDiv.innerHTML = html;
    document.getElementById('propagacionResultados').style.display = 'block';
}

function mostrarError(elementId, mensaje) {
    document.getElementById(elementId).innerHTML = `
        <div class="alert alert-danger resultado-aparicion" role="alert">
            <h6><i class="fas fa-exclamation-triangle"></i> Error:</h6>
            <p>${mensaje}</p>
        </div>
    `;
}

function showLoading(resultadosId, outputId) {
    document.getElementById(resultadosId).style.display = 'block';
    document.getElementById(outputId).innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">Calculando...</span>
            </div>
            <p class="mt-2">Calculando...</p>
        </div>
    `;
}
