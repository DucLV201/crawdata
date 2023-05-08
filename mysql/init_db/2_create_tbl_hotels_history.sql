USE hotels;
CREATE TABLE hotel_history (
    action VARCHAR(10) NOT NULL,
    name_hotel VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    star INT NOT NULL,
    link VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);