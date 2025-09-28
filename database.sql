CREATE DATABASE IF NOT EXISTS client_query_db;
USE client_query_db;

drop DATABASE client_query_db;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('Client', 'Support') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select* from users;
truncate users;
drop table queries;
CREATE TABLE IF NOT EXISTS queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    query_heading VARCHAR(255) NOT NULL,
    query_description TEXT NOT NULL,
    query_created_time DATETIME NOT NULL,
    status ENUM('Open','Closed') DEFAULT 'Open',
    query_closed_time DATETIME DEFAULT NULL,
    image LONGBLOB
);
truncate queries;
select* from queries