-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos  
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de carritos
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de items del carrito
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Índices adicionales para mejorar performance
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);
CREATE INDEX idx_carts_user_id ON carts(user_id);

-- Datos de prueba

-- Usuarios
INSERT INTO users (username, email, password_hash) VALUES
('juan123', 'juan@example.com', 'hashed_pw_juan'),
('maria456', 'maria@example.com', 'hashed_pw_maria');

-- Productos
INSERT INTO products (name, description, price, stock, image_url) VALUES
('Camiseta', 'Camiseta de algodón 100% orgánico', 19.99, 50, 'https://example.com/img/camiseta.jpg'),
('Pantalón', 'Pantalón vaquero azul oscuro', 39.99, 30, 'https://example.com/img/pantalon.jpg'),
('Zapatillas', 'Zapatillas deportivas unisex', 59.99, 20, 'https://example.com/img/zapatillas.jpg');

-- Carritos
INSERT INTO carts (user_id) VALUES
(1), (2);

-- Items en carritos
INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
(1, 1, 2),  -- Juan compra 2 camisetas
(1, 3, 1),  -- Juan compra 1 par de zapatillas
(2, 2, 1);  -- Maria compra 1 pantalón
