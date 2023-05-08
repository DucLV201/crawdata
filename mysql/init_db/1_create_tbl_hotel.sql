CREATE DATABASE hotels;
USE hotels;
CREATE TABLE hotels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_hotel VARCHAR(255),
    price DECIMAL(10,0),
    star INT,
    link VARCHAR(255)
);
