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
