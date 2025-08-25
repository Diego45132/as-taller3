from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave-por-defecto-cambiar')

API_URL = os.getenv('API_URL', 'http://api:8000')

@app.route('/')
def index():
    # Obtener productos destacados de la API
    try:
        resp = api_request('/products/featured')
        featured_products = resp.json()
    except Exception:
        featured_products = []
        flash('No se pudieron cargar los productos destacados.', 'warning')
    return render_template('index.html', featured_products=featured_products)

@app.route('/products')
def products():
    search_query = request.args.get('q', '')
    params = {'q': search_query} if search_query else {}
    try:
        resp = api_request('/products', params=params)
        products = resp.json()
    except Exception:
        products = []
        flash('No se pudieron cargar los productos.', 'warning')
    return render_template('products.html', products=products, search_query=search_query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password'],
        }
        try:
            resp = api_request('/users/login', method='POST', json=data)
            if resp.status_code == 200:
                token = resp.json().get('access_token')
                session['token'] = token
                session['username'] = data['username']
                flash('Login exitoso', 'success')
                return redirect(url_for('index'))
            else:
                flash('Credenciales inválidas', 'danger')
        except Exception:
            flash('Error al conectarse con el servidor de autenticación', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'email': request.form['email'],
            'password': request.form['password'],
        }
        try:
            resp = api_request('/users/register', method='POST', json=data)
            if resp.status_code == 201:
                flash('Usuario registrado con éxito, por favor inicia sesión.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error al registrar usuario.', 'danger')
        except Exception:
            flash('Error al conectarse con el servidor de registro', 'danger')
    return render_template('register.html')

@app.route('/cart')
def cart():
    if not is_logged_in():
        flash('Debes iniciar sesión para ver el carrito', 'warning')
        return redirect(url_for('login'))
    headers = {'Authorization': f'Bearer {session["token"]}'}
    try:
        resp = api_request('/carts', headers=headers)
        cart = resp.json()
    except Exception:
        cart = {}
        flash('No se pudo cargar el carrito.', 'warning')
    return render_template('cart.html', cart=cart)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not is_logged_in():
        flash('Debes iniciar sesión para agregar productos al carrito', 'warning')
        return redirect(url_for('login'))
    headers = {'Authorization': f'Bearer {session["token"]}'}
    data = {'product_id': product_id, 'quantity': int(request.form.get('quantity', 1))}
    try:
        resp = api_request('/carts/items', method='POST', json=data, headers=headers)
        if resp.status_code == 201:
            flash('Producto agregado al carrito', 'success')
        else:
            flash('Error al agregar producto al carrito', 'danger')
    except Exception:
        flash('Error al conectar con el servidor', 'danger')
    return redirect(request.referrer or url_for('products'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))

def api_request(endpoint, method='GET', params=None, json=None, headers=None):
    url = API_URL + endpoint
    headers = headers or {}
    try:
        if method.upper() == 'GET':
            response = requests.get(url, params=params, headers=headers, timeout=5)
        elif method.upper() == 'POST':
            response = requests.post(url, json=json, headers=headers, timeout=5)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=json, headers=headers, timeout=5)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=5)
        else:
            raise ValueError("Método HTTP no soportado")
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise RuntimeError(f"Error en la petición API: {e}")

def is_logged_in():
    return 'token' in session

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
