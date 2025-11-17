from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# URL base de la API
API_BASE_URL = "http://127.0.0.1:8000/api"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ecuaciones-no-lineales')
def ecuaciones_no_lineales():
    return render_template('ecuaciones_no_lineales.html')

@app.route('/errores')
def errores():
    return render_template('errores.html')

@app.route('/series-taylor')
def series_taylor():
    return render_template('series_taylor.html')

@app.route('/sistemas-ecuaciones')
def sistemas_ecuaciones():
    return render_template('sistemas_ecuaciones.html')

@app.route('/interpolacion')
def interpolacion():
    return render_template('interpolacion.html')

# Rutas proxy para comunicarse con la API
@app.route('/api/biseccion', methods=['POST'])
def proxy_biseccion():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/biseccion",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/punto-fijo', methods=['POST'])
def proxy_punto_fijo():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/punto-fijo",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/regla-falsa', methods=['POST'])
def proxy_regla_falsa():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/regla-falsa",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/busqueda-incremental', methods=['POST'])
def proxy_busqueda_incremental():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/busqueda-incremental",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/newton-raphson', methods=['POST'])
def proxy_newton_raphson():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/newton-raphson",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/secante', methods=['POST'])
def proxy_secante():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/secante",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/raices-multiples', methods=['POST'])
def proxy_raices_multiples():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/raices-multiples",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/error-absoluto', methods=['POST'])
def proxy_error_absoluto():
    try:
        response = requests.post(
            f"{API_BASE_URL}/errores/error-absoluto",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/error-relativo', methods=['POST'])
def proxy_error_relativo():
    try:
        response = requests.post(
            f"{API_BASE_URL}/errores/error-relativo",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/propagacion-error', methods=['POST'])
def proxy_propagacion_error():
    try:
        response = requests.post(
            f"{API_BASE_URL}/errores/propagacion-error",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/taylor-coseno', methods=['POST'])
def proxy_taylor_coseno():
    try:
        response = requests.post(
            f"{API_BASE_URL}/series-taylor/coseno",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/taylor-seno', methods=['POST'])
def proxy_taylor_seno():
    try:
        response = requests.post(
            f"{API_BASE_URL}/series-taylor/seno",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gauss-pivoteo', methods=['POST'])
def proxy_gauss_pivoteo():
    try:
        response = requests.post(
            f"{API_BASE_URL}/sistemas-ecuaciones/gauss-pivoteo",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/validar-sistema', methods=['POST'])
def proxy_validar_sistema():
    try:
        response = requests.post(
            f"{API_BASE_URL}/sistemas-ecuaciones/validar-sistema",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sistemas/jacobi', methods=['POST'])
def proxy_jacobi():
    try:
        response = requests.post(
            f"{API_BASE_URL}/sistemas-ecuaciones/jacobi",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sistemas/gauss-seidel', methods=['POST'])
def proxy_gauss_seidel():
    try:
        response = requests.post(
            f"{API_BASE_URL}/sistemas-ecuaciones/gauss-seidel",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sistemas/sor', methods=['POST'])
def proxy_sor():
    try:
        response = requests.post(
            f"{API_BASE_URL}/sistemas-ecuaciones/sor",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sistemas/comparar-iterativos', methods=['POST'])
def proxy_comparar_iterativos():
    try:
        response = requests.post(
            f"{API_BASE_URL}/sistemas-ecuaciones/comparar-iterativos",
            json=request.json,
            timeout=60  # Más tiempo porque ejecuta 3 métodos
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/vandermonde', methods=['POST'])
def proxy_vandermonde():
    try:
        response = requests.post(
            f"{API_BASE_URL}/interpolacion/vandermonde",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/newton', methods=['POST'])
def proxy_newton():
    try:
        response = requests.post(
            f"{API_BASE_URL}/interpolacion/newton",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lagrange', methods=['POST'])
def proxy_lagrange():
    try:
        response = requests.post(
            f"{API_BASE_URL}/interpolacion/lagrange",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/spline-lineal', methods=['POST'])
def proxy_spline_lineal():
    try:
        response = requests.post(
            f"{API_BASE_URL}/interpolacion/spline-lineal",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/spline-cubico', methods=['POST'])
def proxy_spline_cubico():
    try:
        response = requests.post(
            f"{API_BASE_URL}/interpolacion/spline-cubico",
            json=request.json,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/comparar', methods=['POST'])
def proxy_comparar():
    try:
        response = requests.post(
            f"{API_BASE_URL}/interpolacion/comparar",
            json=request.json,
            timeout=60  # Más tiempo porque ejecuta 5 métodos
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ecuaciones/comparar', methods=['POST'])
def proxy_comparar_ecuaciones():
    try:
        response = requests.post(
            f"{API_BASE_URL}/ecuaciones-no-lineales/comparar",
            json=request.json,
            timeout=60  # Más tiempo porque ejecuta múltiples métodos
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
