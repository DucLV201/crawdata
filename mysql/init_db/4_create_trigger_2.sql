USE hotels;

DELIMITER //

CREATE TRIGGER hotels_trigger2
AFTER UPDATE ON hotels
FOR EACH ROW
BEGIN
    INSERT INTO hotel_history (action, name_hotel, price, star, link)
    VALUES ('update', NEW.name_hotel, NEW.price, NEW.star, NEW.link);
END //

DELIMITER ;


