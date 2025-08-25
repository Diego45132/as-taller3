-- Crear la base de datos (solo si no existe)
CREATE DATABASE tienda_db
    WITH OWNER = tienda_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_CO.UTF-8'
    LC_CTYPE = 'es_CO.UTF-8'
    TEMPLATE = template0;

-- Conectar a la base de datos recién creada
\c tienda_db;

-- Crear extensión para UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Establecer la zona horaria por defecto
SET timezone = 'America/Bogota';

-- También puedes forzar la zona horaria en la configuración de la base de datos
ALTER DATABASE tienda_db SET timezone TO 'America/Bogota';


-- Crear usuario con contraseña
CREATE USER tienda_user WITH PASSWORD 'tienda_password';

-- Conceder permisos
GRANT ALL PRIVILEGES ON DATABASE tienda_db TO tienda_user;
