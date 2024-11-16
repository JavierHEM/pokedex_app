# Esquema de la base de datos

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS pokedex_app;
USE pokedex_app;

-- Tabla de roles
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

-- Tabla de usuarios
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Tabla de entrenadores (personajes)
CREATE TABLE trainers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(50) NOT NULL,
    age INT,
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabla de pokémon del equipo
CREATE TABLE team_pokemon (
    id INT PRIMARY KEY AUTO_INCREMENT,
    trainer_id INT,
    pokemon_id INT,
    nickname VARCHAR(50),
    pokemon_name VARCHAR(50) NOT NULL,
    pokemon_type VARCHAR(50),
    height FLOAT,
    weight FLOAT,
    base_experience INT,
    sprite_url TEXT,
    stats_hp INT,
    stats_attack INT,
    stats_defense INT,
    stats_sp_attack INT,
    stats_sp_defense INT,
    stats_speed INT,
    moves TEXT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trainer_id) REFERENCES trainers(id)
);

-- Tabla de historial de búsquedas
CREATE TABLE search_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    search_term VARCHAR(100),
    pokemon_id INT,
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insertar roles básicos
INSERT INTO roles (name) VALUES ('user'), ('admin');