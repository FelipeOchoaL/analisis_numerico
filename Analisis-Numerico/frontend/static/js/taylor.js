// Serie de Taylor - Coseno
document.getElementById('cosenoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        theta: parseFloat(document.getElementById('cos_theta').value),
        tolerancia: parseFloat(document.getElementById('cos_tolerancia').value),
        niter: parseInt(document.getElementById('cos_niter').value),
        error_relativo: document.getElementById('cos_error_relativo').checked
    };
    
    try {
        showLoading('cosenoResultados', 'cosenoOutput');
        
        const response = await fetch('/api/taylor-coseno', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoCoseno(resultado);
        } else {
            mostrarError('cosenoOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('cosenoOutput', 'Error de conexión: ' + error.message);
    }
});

// Serie de Taylor - Seno
document.getElementById('senoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        theta: parseFloat(document.getElementById('sen_theta').value),
        tolerancia: parseFloat(document.getElementById('sen_tolerancia').value),
        niter: parseInt(document.getElementById('sen_niter').value),
        error_relativo: document.getElementById('sen_error_relativo').checked
    };
    
    try {
        showLoading('senoResultados', 'senoOutput');
        
        const response = await fetch('/api/taylor-seno', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoSeno(resultado);
        } else {
            mostrarError('senoOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('senoOutput', 'Error de conexión: ' + error.message);
    }
});

function mostrarResultadoCoseno(resultado) {
    const outputDiv = document.getElementById('cosenoOutput');
    
    let html = `
        <div class="alert ${resultado.convergencia ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-check-circle"></i> Resultado - Serie de Taylor (Coseno):</h6>
            <div class="resultado-resumen">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Ángulo (θ):</strong> <span class="numero-destacado">${resultado.theta_radianes.toFixed(6)} rad</span></p>
                        <p><strong>Aproximación Taylor:</strong> <span class="numero-destacado">${resultado.aproximacion.toFixed(12)}</span></p>
                        <p><strong>Valor Exacto (Math.cos):</strong> <span class="numero-destacado">${resultado.valor_exacto.toFixed(12)}</span></p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Términos utilizados:</strong> <span class="numero-destacado">${resultado.terminos_utilizados}</span></p>
                        <p><strong>Error final:</strong> <span class="numero-destacado">${resultado.error_final.toExponential(6)}</span></p>
                        <p><strong>Diferencia con exacto:</strong> <span class="numero-destacado">${resultado.diferencia_con_exacto.toExponential(6)}</span></p>
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-12">
                        <p><strong>Estado de convergencia:</strong> 
                            <span class="badge ${resultado.convergencia ? 'bg-success' : 'bg-warning'}">
                                ${resultado.convergencia ? 'Convergió' : 'No convergió completamente'}
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            ${resultado.tiempo_ejecucion ? `<p><small>Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(6)} segundos</small></p>` : ''}
        </div>
    `;
    
    // Mostrar tabla de sumas parciales (limitada a las primeras y últimas)
    if (resultado.sumas_parciales && resultado.sumas_parciales.length > 0) {
        const maxMostrar = 15;
        let sumasAMostrar = resultado.sumas_parciales;
        let erroresAMostrar = resultado.errores;
        
        if (resultado.sumas_parciales.length > maxMostrar) {
            sumasAMostrar = [
                ...resultado.sumas_parciales.slice(0, Math.floor(maxMostrar/2)),
                ...resultado.sumas_parciales.slice(-Math.floor(maxMostrar/2))
            ];
            erroresAMostrar = [
                ...resultado.errores.slice(0, Math.floor(maxMostrar/2) - 1),
                ...resultado.errores.slice(-Math.floor(maxMostrar/2))
            ];
        }
        
        html += `
            <h6><i class="fas fa-table"></i> Convergencia de la Serie (primeros y últimos términos):</h6>
            <div class="table-responsive resultado-tabla">
                <table class="table table-striped table-sm">
                    <thead class="table-dark">
                        <tr>
                            <th>Término (k)</th>
                            <th>Suma Parcial S_k</th>
                            <th>Error |S_k - S_{k-1}|</th>
                            <th>Diferencia con cos(θ)</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        sumasAMostrar.forEach((suma, index) => {
            const k = index < Math.floor(maxMostrar/2) ? index : (resultado.sumas_parciales.length - (maxMostrar - index));
            const error = index > 0 ? erroresAMostrar[index - 1] : '-';
            const difExacto = Math.abs(suma - resultado.valor_exacto);
            
            // Mostrar separador si pasamos de los primeros a los últimos
            if (index === Math.floor(maxMostrar/2) && resultado.sumas_parciales.length > maxMostrar) {
                html += `<tr><td colspan="4" class="text-center"><strong>...</strong></td></tr>`;
            }
            
            html += `
                <tr>
                    <td>${k}</td>
                    <td>${suma.toFixed(12)}</td>
                    <td>${error !== '-' ? error.toExponential(4) : '-'}</td>
                    <td>${difExacto.toExponential(4)}</td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
    }
    
    outputDiv.innerHTML = html;
    document.getElementById('cosenoResultados').style.display = 'block';
}

function mostrarResultadoSeno(resultado) {
    const outputDiv = document.getElementById('senoOutput');
    
    let html = `
        <div class="alert ${resultado.convergencia ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-check-circle"></i> Resultado - Serie de Taylor (Seno):</h6>
            <div class="resultado-resumen">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Ángulo (θ):</strong> <span class="numero-destacado">${resultado.theta_radianes.toFixed(6)} rad</span></p>
                        <p><strong>Aproximación Taylor:</strong> <span class="numero-destacado">${resultado.aproximacion.toFixed(12)}</span></p>
                        <p><strong>Valor Exacto (Math.sin):</strong> <span class="numero-destacado">${resultado.valor_exacto.toFixed(12)}</span></p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Términos utilizados:</strong> <span class="numero-destacado">${resultado.terminos_utilizados}</span></p>
                        <p><strong>Error final:</strong> <span class="numero-destacado">${resultado.error_final.toExponential(6)}</span></p>
                        <p><strong>Diferencia con exacto:</strong> <span class="numero-destacado">${resultado.diferencia_con_exacto.toExponential(6)}</span></p>
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-12">
                        <p><strong>Estado de convergencia:</strong> 
                            <span class="badge ${resultado.convergencia ? 'bg-success' : 'bg-warning'}">
                                ${resultado.convergencia ? 'Convergió' : 'No convergió completamente'}
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            ${resultado.tiempo_ejecucion ? `<p><small>Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(6)} segundos</small></p>` : ''}
        </div>
    `;
    
    // Mostrar tabla de sumas parciales (similar a coseno)
    if (resultado.sumas_parciales && resultado.sumas_parciales.length > 0) {
        const maxMostrar = 15;
        let sumasAMostrar = resultado.sumas_parciales;
        let erroresAMostrar = resultado.errores;
        
        if (resultado.sumas_parciales.length > maxMostrar) {
            sumasAMostrar = [
                ...resultado.sumas_parciales.slice(0, Math.floor(maxMostrar/2)),
                ...resultado.sumas_parciales.slice(-Math.floor(maxMostrar/2))
            ];
            erroresAMostrar = [
                ...resultado.errores.slice(0, Math.floor(maxMostrar/2) - 1),
                ...resultado.errores.slice(-Math.floor(maxMostrar/2))
            ];
        }
        
        html += `
            <h6><i class="fas fa-table"></i> Convergencia de la Serie (primeros y últimos términos):</h6>
            <div class="table-responsive resultado-tabla">
                <table class="table table-striped table-sm">
                    <thead class="table-dark">
                        <tr>
                            <th>Término (k)</th>
                            <th>Suma Parcial S_k</th>
                            <th>Error |S_k - S_{k-1}|</th>
                            <th>Diferencia con sen(θ)</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        sumasAMostrar.forEach((suma, index) => {
            const k = index < Math.floor(maxMostrar/2) ? index : (resultado.sumas_parciales.length - (maxMostrar - index));
            const error = index > 0 ? erroresAMostrar[index - 1] : '-';
            const difExacto = Math.abs(suma - resultado.valor_exacto);
            
            // Mostrar separador si pasamos de los primeros a los últimos
            if (index === Math.floor(maxMostrar/2) && resultado.sumas_parciales.length > maxMostrar) {
                html += `<tr><td colspan="4" class="text-center"><strong>...</strong></td></tr>`;
            }
            
            html += `
                <tr>
                    <td>${k}</td>
                    <td>${suma.toFixed(12)}</td>
                    <td>${error !== '-' ? error.toExponential(4) : '-'}</td>
                    <td>${difExacto.toExponential(4)}</td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
    }
    
    outputDiv.innerHTML = html;
    document.getElementById('senoResultados').style.display = 'block';
}

// Función para establecer ángulos comunes desde la tabla
function setAngle(radianes, tipo) {
    if (tipo === 'cos') {
        document.getElementById('cos_theta').value = radianes;
        // Activar la pestaña de coseno
        const cosenoTab = new bootstrap.Tab(document.getElementById('coseno-tab'));
        cosenoTab.show();
    } else if (tipo === 'sen') {
        document.getElementById('sen_theta').value = radianes;
        // Activar la pestaña de seno
        const senoTab = new bootstrap.Tab(document.getElementById('seno-tab'));
        senoTab.show();
    }
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
            <div class="spinner-border text-info" role="status">
                <span class="visually-hidden">Calculando...</span>
            </div>
            <p class="mt-2">Calculando serie de Taylor...</p>
        </div>
    `;
}
