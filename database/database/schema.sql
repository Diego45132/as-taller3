-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos  
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de carritos
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cart_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de items del carrito
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cart_item_cart FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    CONSTRAINT fk_cart_item_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Índices adicionales
CREATE INDEX idx_cart_user ON carts(user_id);
CREATE INDEX idx_cartitem_cart ON cart_items(cart_id);
CREATE INDEX idx_cartitem_product ON cart_items(product_id);

-- Usuarios de prueba
INSERT INTO users (username, email, password_hash)
VALUES 
('admin', 'admin@example.com', '$2b$12$EjemploDeHashEnBCrypt'),
('user1', 'user1@example.com', '$2b$12$OtroHashEjemplo');

-- Productos de prueba
INSERT INTO products (name, description, price, stock, image_url)
VALUES 
('Camiseta Azul', 'Camiseta 100% algodón', 19.99, 50, 'https://via.placeholder.com/150'),
('Pantalón Negro', 'Pantalón elegante de vestir', 39.99, 20, 'https://via.placeholder.com/150'),
('Zapatillas Deportivas', 'Zapatillas cómodas para correr', 59.99, 15, 'https://via.placeholder.com/150');
