// Método de Bisección
document.getElementById('biseccionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        xi: parseFloat(document.getElementById('biseccion_xi').value),
        xs: parseFloat(document.getElementById('biseccion_xs').value),
        tolerancia: parseFloat(document.getElementById('biseccion_tol').value),
        niter: parseInt(document.getElementById('biseccion_niter').value),
        funcion: document.getElementById('biseccion_funcion').value,
        tipo_error: document.getElementById('biseccion_tipo_error').value
    };
    
    try {
        showLoading('biseccionResultados', 'biseccionOutput');
        
        const response = await fetch('/api/biseccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoBiseccion(resultado);
        } else {
            mostrarError('biseccionOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('biseccionOutput', 'Error de conexión: ' + error.message);
    }
});

// Método de Punto Fijo
document.getElementById('puntoFijoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x0: parseFloat(document.getElementById('pf_x0').value),
        tolerancia: parseFloat(document.getElementById('pf_tol').value),
        niter: parseInt(document.getElementById('pf_niter').value),
        funcion_f: document.getElementById('pf_funcion_f').value,
        funcion_g: document.getElementById('pf_funcion_g').value,
        tipo_error: document.getElementById('pf_tipo_error').value
    };
    
    try {
        showLoading('puntoFijoResultados', 'puntoFijoOutput');
        
        const response = await fetch('/api/punto-fijo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoPuntoFijo(resultado);
        } else {
            mostrarError('puntoFijoOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('puntoFijoOutput', 'Error de conexión: ' + error.message);
    }
});

// Método de Regla Falsa
document.getElementById('reglaFalsaForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x0: parseFloat(document.getElementById('rf_x0').value),
        x1: parseFloat(document.getElementById('rf_x1').value),
        tolerancia: parseFloat(document.getElementById('rf_tol').value),
        niter: parseInt(document.getElementById('rf_niter').value),
        funcion: document.getElementById('rf_funcion').value,
        tipo_error: document.getElementById('rf_tipo_error').value
    };
    
    try {
        showLoading('reglaFalsaResultados', 'reglaFalsaOutput');
        
        const response = await fetch('/api/regla-falsa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoReglaFalsa(resultado);
        } else {
            mostrarError('reglaFalsaOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('reglaFalsaOutput', 'Error de conexión: ' + error.message);
    }
});

// Búsqueda Incremental
document.getElementById('busquedaForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x0: parseFloat(document.getElementById('bi_x0').value),
        delta: parseFloat(document.getElementById('bi_delta').value),
        niter: parseInt(document.getElementById('bi_niter').value),
        funcion: document.getElementById('bi_funcion').value
    };
    
    try {
        showLoading('busquedaResultados', 'busquedaOutput');
        
        const response = await fetch('/api/busqueda-incremental', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoBusqueda(resultado);
        } else {
            mostrarError('busquedaOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('busquedaOutput', 'Error de conexión: ' + error.message);
    }
});

// Método de Newton-Raphson
document.getElementById('newtonRaphsonForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x0: parseFloat(document.getElementById('nr_x0').value),
        tolerancia: parseFloat(document.getElementById('nr_tol').value),
        niter: parseInt(document.getElementById('nr_niter').value),
        funcion_f: document.getElementById('nr_funcion_f').value,
        funcion_df: document.getElementById('nr_funcion_df').value,
        incluir_error: document.getElementById('nr_incluir_error').checked,
        tipo_error: document.getElementById('nr_tipo_error').value,
        tipo_precision: document.getElementById('nr_tipo_precision').value,
        precision: parseInt(document.getElementById('nr_precision').value)
    };
    
    try {
        showLoading('newtonRaphsonResultados', 'newtonRaphsonOutput');
        
        const response = await fetch('/api/newton-raphson', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoNewtonRaphson(resultado);
        } else {
            mostrarError('newtonRaphsonOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('newtonRaphsonOutput', 'Error de conexión: ' + error.message);
    }
});

// Método de la Secante
document.getElementById('secanteForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x0: parseFloat(document.getElementById('sec_x0').value),
        x1: parseFloat(document.getElementById('sec_x1').value),
        tolerancia: parseFloat(document.getElementById('sec_tol').value),
        niter: parseInt(document.getElementById('sec_niter').value),
        funcion: document.getElementById('sec_funcion').value,
        incluir_error: document.getElementById('sec_incluir_error').checked,
        tipo_error: document.getElementById('sec_tipo_error').value,
        tipo_precision: document.getElementById('sec_tipo_precision').value,
        precision: parseInt(document.getElementById('sec_precision').value)
    };
    
    try {
        showLoading('secanteResultados', 'secanteOutput');
        
        const response = await fetch('/api/secante', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoSecante(resultado);
        } else {
            mostrarError('secanteOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('secanteOutput', 'Error de conexión: ' + error.message);
    }
});

function mostrarResultadoBiseccion(resultado) {
    const outputDiv = document.getElementById('biseccionOutput');
    
    let html = `
        <div class="alert ${resultado.exito ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-info-circle"></i> Resultado:</h6>
            <p><strong>${resultado.mensaje || 'Sin mensaje disponible'}</strong></p>
            ${Number.isFinite(resultado.resultado) ? `<p>Valor aproximado: <span class="numero-destacado">${resultado.resultado.toFixed(8)}</span></p>` : ''}
            ${resultado.tiempo_ejecucion ? `<p><i class="fas fa-clock"></i> Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(4)} segundos</p>` : ''}
        </div>
    `;

    if (resultado.tabla_html) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones:</h6>
            <div class="table-responsive resultado-tabla">
                ${resultado.tabla_html}
            </div>
        `;
    } else if (resultado.iteraciones && resultado.iteraciones.length > 0) {
        html += generarTablaIteraciones(resultado.iteraciones);
    }

    if (resultado.grafico) {
        html += `
            <h6><i class="fas fa-chart-area"></i> Gráfico de la función:</h6>
            <div class="text-center">
                <img src="${resultado.grafico}" alt="Gráfico del método" class="img-fluid rounded shadow-sm">
            </div>
        `;
    }

    if (resultado.ayuda) {
        html += `
            <div class="alert alert-info mt-3" role="alert">
                <i class="fas fa-lightbulb"></i> ${resultado.ayuda}
            </div>
        `;
    }

    outputDiv.innerHTML = html;
    document.getElementById('biseccionResultados').style.display = 'block';
}

function mostrarResultadoPuntoFijo(resultado) {
    const outputDiv = document.getElementById('puntoFijoOutput');
    
    let html = `
        <div class="alert ${resultado.exito ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-info-circle"></i> Resultado:</h6>
            <p><strong>${resultado.mensaje || 'Sin mensaje disponible'}</strong></p>
            ${Number.isFinite(resultado.resultado) ? `<p>Valor aproximado: <span class="numero-destacado">${resultado.resultado.toFixed(8)}</span></p>` : ''}
            ${resultado.tiempo_ejecucion ? `<p><i class="fas fa-clock"></i> Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(4)} segundos</p>` : ''}
        </div>
    `;
    
    if (resultado.tabla_html) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones:</h6>
            <div class="table-responsive resultado-tabla">
                ${resultado.tabla_html}
            </div>
        `;
    } else if (resultado.iteraciones && resultado.iteraciones.length > 0) {
        html += generarTablaIteraciones(resultado.iteraciones);
    }

    if (resultado.grafico) {
        html += `
            <h6><i class="fas fa-chart-area"></i> Gráfico de la función:</h6>
            <div class="text-center">
                <img src="${resultado.grafico}" alt="Gráfico del método" class="img-fluid rounded shadow-sm">
            </div>
        `;
    }

    if (resultado.ayuda) {
        html += `
            <div class="alert alert-info mt-3" role="alert">
                <i class="fas fa-lightbulb"></i> ${resultado.ayuda}
            </div>
        `;
    }
    
    outputDiv.innerHTML = html;
    document.getElementById('puntoFijoResultados').style.display = 'block';
}

function mostrarResultadoReglaFalsa(resultado) {
    const outputDiv = document.getElementById('reglaFalsaOutput');
    
    let html = `
        <div class="alert ${resultado.exito ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-info-circle"></i> Resultado:</h6>
            <p><strong>${resultado.mensaje || 'Sin mensaje disponible'}</strong></p>
            ${Number.isFinite(resultado.resultado) ? `<p>Valor aproximado: <span class="numero-destacado">${resultado.resultado.toFixed(8)}</span></p>` : ''}
            ${resultado.tiempo_ejecucion ? `<p><i class="fas fa-clock"></i> Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(4)} segundos</p>` : ''}
        </div>
    `;
    
    if (resultado.tabla_html) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones:</h6>
            <div class="table-responsive resultado-tabla">
                ${resultado.tabla_html}
            </div>
        `;
    } else if (resultado.iteraciones && resultado.iteraciones.length > 0) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones:</h6>
            <div class="table-responsive resultado-tabla">
                <table class="table table-striped table-sm">
                    <thead class="table-dark">
                        <tr>
                            <th>Iteración</th>
                            <th>X0</th>
                            <th>X1</th>
                            <th>X2</th>
                            <th>f(X0)</th>
                            <th>f(X1)</th>
                            <th>f(X2)</th>
                            <th>Error</th>
                            <th>Observación</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        resultado.iteraciones.forEach(iter => {
            const valores = iter.valores;
            html += `
                <tr>
                    <td>${iter.iteracion}</td>
                    <td>${valores.x0 ? valores.x0.toFixed(8) : '-'}</td>
                    <td>${valores.x1 ? valores.x1.toFixed(8) : '-'}</td>
                    <td>${valores.x2 ? valores.x2.toFixed(8) : '-'}</td>
                    <td>${valores.f0 !== undefined ? valores.f0.toExponential(4) : '-'}</td>
                    <td>${valores.f1 !== undefined ? valores.f1.toExponential(4) : '-'}</td>
                    <td>${valores.f2 !== undefined ? valores.f2.toExponential(4) : '-'}</td>
                    <td>${iter.error ? iter.error.toExponential(4) : '-'}</td>
                    <td><small>${iter.observacion || '-'}</small></td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
    }

    if (resultado.grafico) {
        html += `
            <h6><i class="fas fa-chart-area"></i> Gráfico de la función:</h6>
            <div class="text-center">
                <img src="${resultado.grafico}" alt="Gráfico del método" class="img-fluid rounded shadow-sm">
            </div>
        `;
    }

    if (resultado.ayuda) {
        html += `
            <div class="alert alert-info mt-3" role="alert">
                <i class="fas fa-lightbulb"></i> ${resultado.ayuda}
            </div>
        `;
    }
    
    outputDiv.innerHTML = html;
    document.getElementById('reglaFalsaResultados').style.display = 'block';
}

function mostrarResultadoBusqueda(resultado) {
    const outputDiv = document.getElementById('busquedaOutput');
    
    let html = `
        <div class="alert ${resultado.exito ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-info-circle"></i> Resultado:</h6>
            <p><strong>${resultado.mensaje}</strong></p>
            ${resultado.resultado ? `<p>Aproximación: <span class="numero-destacado">${resultado.resultado.toFixed(8)}</span></p>` : ''}
            ${resultado.tiempo_ejecucion ? `<p>Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(4)} segundos</p>` : ''}
        </div>
    `;
    
    if (resultado.iteraciones && resultado.iteraciones.length > 0) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones:</h6>
            <div class="table-responsive resultado-tabla">
                <table class="table table-striped table-sm">
                    <thead class="table-dark">
                        <tr>
                            <th>Iteración</th>
                            <th>X0</th>
                            <th>X1</th>
                            <th>f(X0)</th>
                            <th>f(X1)</th>
                            <th>f(X0)*f(X1)</th>
                            <th>Observación</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        resultado.iteraciones.forEach(iter => {
            const valores = iter.valores;
            html += `
                <tr class="${valores.producto < 0 ? 'table-success' : ''}">
                    <td>${iter.iteracion}</td>
                    <td>${valores.x0 ? valores.x0.toFixed(8) : '-'}</td>
                    <td>${valores.x1 ? valores.x1.toFixed(8) : '-'}</td>
                    <td>${valores.f0 !== undefined ? valores.f0.toExponential(4) : '-'}</td>
                    <td>${valores.f1 !== undefined ? valores.f1.toExponential(4) : '-'}</td>
                    <td>${valores.producto !== undefined ? valores.producto.toExponential(4) : '-'}</td>
                    <td><small>${iter.observacion || '-'}</small></td>
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
    document.getElementById('busquedaResultados').style.display = 'block';
}

function mostrarResultadoNewtonRaphson(resultado) {
    const outputDiv = document.getElementById('newtonRaphsonOutput');
    
    let html = `
        <div class="alert ${resultado.exito ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-info-circle"></i> Resultado:</h6>
            <p><strong>${resultado.mensaje}</strong></p>
            ${resultado.resultado ? `<p>Raíz aproximada: <span class="numero-destacado">${resultado.resultado.toFixed(10)}</span></p>` : ''}
            ${resultado.tiempo_ejecucion ? `<p><i class="fas fa-clock"></i> Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(4)} segundos</p>` : ''}
        </div>
    `;
    
    // Usar tabla HTML del backend si está disponible
    if (resultado.tabla_html) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones - Método de Newton-Raphson:</h6>
            <div class="alert alert-info" role="alert">
                <small><strong>Procedimiento:</strong> PASO 1: f(xi), f'(xi) → PASO 2: xi+1 = xi - f(xi)/f'(xi) → PASO 3: Calcular errores</small>
            </div>
            <div class="table-responsive resultado-tabla">
                ${resultado.tabla_html}
            </div>
        `;
    } else if (resultado.iteraciones && resultado.iteraciones.length > 0) {
        html += generarTablaIteraciones(resultado.iteraciones);
    }
    
    // Agregar gráfica si está disponible
    if (resultado.grafico) {
        html += `
            <h6><i class="fas fa-chart-area"></i> Gráfico de la función:</h6>
            <div class="text-center">
                <img src="${resultado.grafico}" alt="Gráfico del método de Newton-Raphson" class="img-fluid rounded shadow-sm">
            </div>
        `;
    }
    
    // Agregar ayuda si está disponible
    if (resultado.ayuda) {
        html += `
            <div class="alert alert-info mt-3" role="alert">
                <i class="fas fa-lightbulb"></i> ${resultado.ayuda}
            </div>
        `;
    }
    
    outputDiv.innerHTML = html;
    document.getElementById('newtonRaphsonResultados').style.display = 'block';
}

function mostrarResultadoSecante(resultado) {
    const outputDiv = document.getElementById('secanteOutput');
    
    let html = `
        <div class="alert ${resultado.exito ? 'alert-success' : 'alert-warning'} resultado-aparicion" role="alert">
            <h6><i class="fas fa-info-circle"></i> Resultado:</h6>
            <p><strong>${resultado.mensaje}</strong></p>
            ${resultado.resultado ? `<p>Raíz aproximada: <span class="numero-destacado">${resultado.resultado.toFixed(10)}</span></p>` : ''}
            ${resultado.tiempo_ejecucion ? `<p><i class="fas fa-clock"></i> Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(4)} segundos</p>` : ''}
        </div>
    `;
    
    // Usar tabla HTML del backend si está disponible
    if (resultado.tabla_html) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones - Método de la Secante:</h6>
            <div class="alert alert-info" role="alert">
                <small><strong>Procedimiento:</strong> PASO 1: f(x_{i-1}), f(x_i) → PASO 2: x_{i+1} = x_i - f(x_i) * (x_i - x_{i-1}) / (f(x_i) - f(x_{i-1})) → PASO 3: Calcular errores</small>
            </div>
            <div class="table-responsive resultado-tabla">
                ${resultado.tabla_html}
            </div>
        `;
    } else if (resultado.iteraciones && resultado.iteraciones.length > 0) {
        html += generarTablaIteraciones(resultado.iteraciones);
    }
    
    // Agregar gráfica si está disponible
    if (resultado.grafico) {
        html += `
            <h6><i class="fas fa-chart-area"></i> Gráfico de la función:</h6>
            <div class="text-center">
                <img src="${resultado.grafico}" alt="Gráfico del método de la Secante" class="img-fluid rounded shadow-sm">
            </div>
        `;
    }
    
    // Agregar ayuda si está disponible
    if (resultado.ayuda) {
        html += `
            <div class="alert alert-info mt-3" role="alert">
                <i class="fas fa-lightbulb"></i> ${resultado.ayuda}
            </div>
        `;
    }
    
    outputDiv.innerHTML = html;
    document.getElementById('secanteResultados').style.display = 'block';
}

function mostrarError(elementId, mensaje) {
    document.getElementById(elementId).innerHTML = `
        <div class="alert alert-danger resultado-aparicion" role="alert">
            <h6><i class="fas fa-exclamation-triangle"></i> Error:</h6>
            <p>${mensaje}</p>
        </div>
    `;
}

// Método de Raíces Múltiples
document.getElementById('raicesMultiplesForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        x0: parseFloat(document.getElementById('rm_x0').value),
        tolerancia: parseFloat(document.getElementById('rm_tolerancia').value),
        niter: parseInt(document.getElementById('rm_niter').value),
        funcion_f: document.getElementById('rm_funcion_f').value,
        funcion_df: document.getElementById('rm_funcion_df').value,
        funcion_ddf: document.getElementById('rm_funcion_ddf').value,
        tipo_error: document.getElementById('rm_tipo_error').value,
        modo: document.getElementById('rm_modo').value
    };
    
    try {
        showLoading('raicesMultiplesResultados', 'raicesMultiplesOutput');
        
        const response = await fetch('/api/raices-multiples', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultadoRaicesMultiples(resultado);
        } else {
            mostrarError('raicesMultiplesOutput', resultado.detail || 'Error en el cálculo');
        }
    } catch (error) {
        mostrarError('raicesMultiplesOutput', 'Error de conexión: ' + error.message);
    }
});

function mostrarResultadoRaicesMultiples(resultado) {
    const outputDiv = document.getElementById('raicesMultiplesOutput');
    
    let html = '';
    
    // Mensaje de resultado
    const alertClass = resultado.exito ? 'alert-success' : 'alert-warning';
    const iconClass = resultado.exito ? 'fa-check-circle' : 'fa-exclamation-triangle';
    
    html += `
        <div class="alert ${alertClass} resultado-aparicion" role="alert">
            <h6><i class="fas ${iconClass}"></i> Resultado:</h6>
            <p>${resultado.mensaje}</p>
            ${resultado.resultado ? `<p>Raíz aproximada: <span class="numero-destacado">${resultado.resultado.toFixed(10)}</span></p>` : ''}
            ${resultado.tiempo_ejecucion ? `<p><i class="fas fa-clock"></i> Tiempo de ejecución: ${resultado.tiempo_ejecucion.toFixed(4)} segundos</p>` : ''}
        </div>
    `;
    
    // Usar tabla HTML del backend si está disponible
    if (resultado.tabla_html) {
        html += `
            <h6><i class="fas fa-table"></i> Tabla de Iteraciones - Método de Raíces Múltiples:</h6>
            <div class="alert alert-info" role="alert">
                <small><strong>Fórmula:</strong> x<sub>i+1</sub> = x<sub>i</sub> - [f(x<sub>i</sub>) × f'(x<sub>i</sub>)] / [f'(x<sub>i</sub>)<sup>2</sup> - f(x<sub>i</sub>) × f''(x<sub>i</sub>)]</small>
            </div>
            <div class="table-responsive resultado-tabla">
                ${resultado.tabla_html}
            </div>
        `;
    } else if (resultado.iteraciones && resultado.iteraciones.length > 0) {
        html += generarTablaIteraciones(resultado.iteraciones);
    }
    
    // Agregar gráfica si está disponible
    if (resultado.grafico) {
        html += `
            <h6><i class="fas fa-chart-area"></i> Gráfico de la función:</h6>
            <div class="text-center">
                <img src="${resultado.grafico}" alt="Gráfico del método de Raíces Múltiples" class="img-fluid rounded shadow-sm">
            </div>
        `;
    }
    
    // Agregar ayuda si está disponible
    if (resultado.ayuda) {
        html += `
            <div class="alert alert-info mt-3" role="alert">
                <i class="fas fa-lightbulb"></i> ${resultado.ayuda}
            </div>
        `;
    }
    
    outputDiv.innerHTML = html;
    document.getElementById('raicesMultiplesResultados').style.display = 'block';
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
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Calculando...</span>
            </div>
            <p class="mt-2">Calculando...</p>
        </div>
    `;
}

function generarTablaIteraciones(iteraciones) {
    if (!Array.isArray(iteraciones) || iteraciones.length === 0) {
        return '';
    }

    const columnas = new Set(['Iteración']);
    iteraciones.forEach(iter => {
        if (iter.valores) {
            Object.keys(iter.valores).forEach(key => columnas.add(key));
        }
        if (iter.error !== undefined) columnas.add('Error');
        if (iter.observacion) columnas.add('Observación');
    });

    const columnasArray = Array.from(columnas);

    let html = `
        <h6><i class="fas fa-table"></i> Tabla de Iteraciones:</h6>
        <div class="table-responsive resultado-tabla">
            <table class="table table-striped table-sm">
                <thead class="table-dark">
                    <tr>
                        ${columnasArray.map(col => `<th>${col}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
    `;

    iteraciones.forEach(iter => {
        html += '<tr>';
        columnasArray.forEach(col => {
            let valor = '';
            if (col === 'Iteración') {
                valor = iter.iteracion ?? '';
            } else if (col === 'Error') {
                valor = iter.error ?? (iter.valores && iter.valores.error);
            } else if (col === 'Observación') {
                valor = iter.observacion ?? '';
            } else if (iter.valores && Object.prototype.hasOwnProperty.call(iter.valores, col)) {
                valor = iter.valores[col];
            }

            if (typeof valor === 'number') {
                const absVal = Math.abs(valor);
                if (absVal !== 0 && (absVal < 1e-4 || absVal >= 1e4)) {
                    valor = valor.toExponential(4);
                } else {
                    valor = valor.toFixed(8);
                }
            }

            html += `<td>${valor !== undefined && valor !== null ? valor : ''}</td>`;
        });
        html += '</tr>';
    });

    html += `
                </tbody>
            </table>
        </div>
    `;

    return html;
}

// ====================================
// COMPARACIÓN DE MÉTODOS
// ====================================

document.getElementById('comparacionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Mostrar loading
    document.getElementById('comparacionResultados').style.display = 'block';
    document.getElementById('comparacionLoading').style.display = 'block';
    document.getElementById('comparacionError').style.display = 'none';
    document.getElementById('comparacionResumen').innerHTML = '';
    document.getElementById('comparacionTabla').innerHTML = '';
    document.getElementById('comparacionRecomendacion').innerHTML = '';
    document.getElementById('comparacionCaracteristicas').innerHTML = '';
    document.getElementById('comparacionGraficoTiempos').innerHTML = '';
    document.getElementById('comparacionGraficoConvergencia').innerHTML = '';
    
    const data = {
        funcion: document.getElementById('comp_funcion').value,
        x0: document.getElementById('comp_x0').value ? parseFloat(document.getElementById('comp_x0').value) : null,
        x1: document.getElementById('comp_x1').value ? parseFloat(document.getElementById('comp_x1').value) : null,
        xi: document.getElementById('comp_xi').value ? parseFloat(document.getElementById('comp_xi').value) : null,
        xs: document.getElementById('comp_xs').value ? parseFloat(document.getElementById('comp_xs').value) : null,
        tolerancia: parseFloat(document.getElementById('comp_tolerancia').value),
        niter: parseInt(document.getElementById('comp_niter').value),
        funcion_g: document.getElementById('comp_funcion_g').value || null,
        funcion_df: document.getElementById('comp_funcion_df').value || null,
        funcion_ddf: document.getElementById('comp_funcion_ddf').value || null,
        tipo_error: document.getElementById('comp_tipo_error').value
    };
    
    try {
        const response = await fetch('/api/ecuaciones/comparar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resultado = await response.json();
        document.getElementById('comparacionLoading').style.display = 'none';
        
        if (response.ok && resultado.exito) {
            mostrarResultadoComparacion(resultado);
        } else {
            mostrarErrorComparacion(resultado.mensaje || resultado.detail || 'Error en la comparación');
        }
    } catch (error) {
        document.getElementById('comparacionLoading').style.display = 'none';
        mostrarErrorComparacion('Error de conexión: ' + error.message);
    }
});

function mostrarResultadoComparacion(data) {
    // Resumen
    const resumenHTML = `
        <div class="alert alert-success">
            <h5><i class="fas fa-check-circle"></i> ${data.mensaje}</h5>
            <hr>
            <div class="row">
                <div class="col-md-6">
                    <p><strong><i class="fas fa-bolt text-warning"></i> Método más rápido:</strong> 
                    ${data.metodo_mas_rapido} (${(data.tiempo_mas_rapido * 1000).toFixed(3)} ms)</p>
                </div>
                <div class="col-md-6">
                    <p><strong><i class="fas fa-compress-arrows-alt text-primary"></i> Menos iteraciones:</strong> 
                    ${data.metodo_menos_iteraciones}</p>
                </div>
            </div>
            <p class="mb-0"><strong><i class="fas fa-check text-success"></i> Métodos exitosos:</strong> 
            ${data.total_metodos_exitosos} de ${data.total_metodos_ejecutados}</p>
        </div>
    `;
    document.getElementById('comparacionResumen').innerHTML = resumenHTML;
    
    // Gráficos
    if (data.grafico_comparativo_tiempos) {
        document.getElementById('comparacionGraficoTiempos').innerHTML = `
            <h6><i class="fas fa-clock"></i> Tiempos de Ejecución</h6>
            <img src="${data.grafico_comparativo_tiempos}" class="img-fluid" alt="Gráfico de Tiempos">
        `;
    }
    
    if (data.grafico_comparativo_convergencia) {
        document.getElementById('comparacionGraficoConvergencia').innerHTML = `
            <h6><i class="fas fa-chart-line"></i> Iteraciones hasta Convergencia</h6>
            <img src="${data.grafico_comparativo_convergencia}" class="img-fluid" alt="Gráfico de Convergencia">
        `;
    }
    
    // Tabla de resultados
    let tablaHTML = `
        <h6><i class="fas fa-table"></i> Resultados Detallados</h6>
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Método</th>
                        <th>Estado</th>
                        <th>Tiempo (ms)</th>
                        <th>Iteraciones</th>
                        <th>Resultado</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    for (const [metodo, resultado] of Object.entries(data.resultados)) {
        const esRapido = metodo === data.metodo_mas_rapido;
        const esMenosIteraciones = metodo === data.metodo_menos_iteraciones;
        const claseRow = esRapido ? 'table-success' : (esMenosIteraciones ? 'table-info' : '');
        
        tablaHTML += `
            <tr class="${claseRow}">
                <td><strong>${metodo}</strong>
                    ${esRapido ? ' <i class="fas fa-trophy text-warning"></i>' : ''}
                    ${esMenosIteraciones ? ' <i class="fas fa-medal text-info"></i>' : ''}
                </td>
                <td>${resultado.exito ? '<span class="badge bg-success">Exitoso</span>' : '<span class="badge bg-danger">Error</span>'}</td>
                <td>${resultado.exito ? (resultado.tiempo * 1000).toFixed(3) : 'N/A'}</td>
                <td>${resultado.exito ? resultado.iteraciones : 'N/A'}</td>
                <td>${resultado.exito && resultado.resultado !== null ? resultado.resultado.toFixed(8) : 'N/A'}</td>
            </tr>
        `;
    }
    
    tablaHTML += `
                </tbody>
            </table>
        </div>
    `;
    document.getElementById('comparacionTabla').innerHTML = tablaHTML;
    
    // Recomendación
    let recomendacionHTML = `
        <div class="alert alert-info">
            <h5><i class="fas fa-lightbulb"></i> Recomendación</h5>
            <p>${data.informe.recomendacion}</p>
    `;
    
    if (data.informe.nota_convergencia) {
        recomendacionHTML += `<p><em>${data.informe.nota_convergencia}</em></p>`;
    }
    
    recomendacionHTML += `</div>`;
    document.getElementById('comparacionRecomendacion').innerHTML = recomendacionHTML;
    
    // Características detalladas (Accordion)
    let caracteristicasHTML = `
        <h6><i class="fas fa-info-circle"></i> Características Detalladas de los Métodos</h6>
        <div class="accordion" id="accordionCaracteristicas">
    `;
    
    let index = 0;
    for (const [metodo, caracteristicas] of Object.entries(data.informe.caracteristicas)) {
        const accordionId = `accordion${index}`;
        caracteristicasHTML += `
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading${index}">
                    <button class="accordion-button ${index === 0 ? '' : 'collapsed'}" type="button" 
                            data-bs-toggle="collapse" data-bs-target="#${accordionId}" 
                            aria-expanded="${index === 0 ? 'true' : 'false'}" aria-controls="${accordionId}">
                        <strong>${metodo}</strong>
                    </button>
                </h2>
                <div id="${accordionId}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}" 
                     aria-labelledby="heading${index}" data-bs-parent="#accordionCaracteristicas">
                    <div class="accordion-body">
                        <p><strong><i class="fas fa-check-circle text-success"></i> Ventajas:</strong></p>
                        <ul>
                            ${caracteristicas.ventajas.map(v => `<li>${v}</li>`).join('')}
                        </ul>
                        <p><strong><i class="fas fa-times-circle text-danger"></i> Desventajas:</strong></p>
                        <ul>
                            ${caracteristicas.desventajas.map(d => `<li>${d}</li>`).join('')}
                        </ul>
                        <p><strong><i class="fas fa-chart-line"></i> Tipo de convergencia:</strong> ${caracteristicas.convergencia}</p>
                        <p><strong><i class="fas fa-thumbs-up"></i> Mejor uso:</strong> ${caracteristicas.mejor_uso}</p>
                    </div>
                </div>
            </div>
        `;
        index++;
    }
    
    caracteristicasHTML += `</div>`;
    document.getElementById('comparacionCaracteristicas').innerHTML = caracteristicasHTML;
}

function mostrarErrorComparacion(mensaje) {
    document.getElementById('comparacionResultados').style.display = 'none';
    document.getElementById('comparacionError').style.display = 'block';
    document.getElementById('comparacionMensajeError').textContent = mensaje;
}

function limpiarComparacion() {
    document.getElementById('comparacionForm').reset();
    document.getElementById('comparacionResultados').style.display = 'none';
    document.getElementById('comparacionError').style.display = 'none';
}

function cargarEjemploComparacion1() {
    // Ejemplo 1: f(x) = x^3 - 2x - 5
    document.getElementById('comp_funcion').value = 'x**3 - 2*x - 5';
    document.getElementById('comp_x0').value = '2';
    document.getElementById('comp_x1').value = '3';
    document.getElementById('comp_xi').value = '2';
    document.getElementById('comp_xs').value = '3';
    document.getElementById('comp_funcion_g').value = '(2*x + 5)**(1/3)';
    document.getElementById('comp_funcion_df').value = '3*x**2 - 2';
    document.getElementById('comp_funcion_ddf').value = '6*x';
    document.getElementById('comp_tolerancia').value = '0.0000001';
    document.getElementById('comp_niter').value = '100';
}

function cargarEjemploComparacion2() {
    // Ejemplo 2: f(x) = cos(x) - x
    document.getElementById('comp_funcion').value = 'cos(x) - x';
    document.getElementById('comp_x0').value = '0.5';
    document.getElementById('comp_x1').value = '1';
    document.getElementById('comp_xi').value = '0';
    document.getElementById('comp_xs').value = '1';
    document.getElementById('comp_funcion_g').value = 'cos(x)';
    document.getElementById('comp_funcion_df').value = '-sin(x) - 1';
    document.getElementById('comp_funcion_ddf').value = '-cos(x)';
    document.getElementById('comp_tolerancia').value = '0.0000001';
    document.getElementById('comp_niter').value = '100';
}
