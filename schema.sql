CREATE DATABASE IF NOT EXISTS jella
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE jella;

CREATE TABLE IF NOT EXISTS student_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_number VARCHAR(30) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(120) NOT NULL,
    course VARCHAR(120) NOT NULL,
    year_level TINYINT UNSIGNED NOT NULL,
    section VARCHAR(30) NOT NULL,
    age TINYINT UNSIGNED NOT NULL,
    civil_status VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
