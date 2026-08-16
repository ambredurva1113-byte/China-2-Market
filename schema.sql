CREATE DATABASE IF NOT EXISTS china2market;
USE china2market;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    supplier VARCHAR(100),
    import_cost DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    reorder_threshold INT DEFAULT 50
);

CREATE TABLE IF NOT EXISTS sales (
    order_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100),
    city VARCHAR(50),
    supplier VARCHAR(100),
    import_cost DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    quantity_sold INT,
    shipment_delay_days INT,
    order_date DATE,
    delivery_date DATE,
    profit DECIMAL(10,2),
    damaged_goods BOOLEAN,
    month INT,
    year INT
);
