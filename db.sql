-- db.sql
CREATE DATABASE bakery_management;

USE bakery_management;

-- Table for storing users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('cashier', 'manager') NOT NULL
);

-- Table for storing bakery items
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- Table for storing sales records
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255),
    quantity INT,
    price DECIMAL(10, 2),
    total DECIMAL(10, 2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
