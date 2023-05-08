USE hotels;

DELIMITER //

CREATE TRIGGER hotels_trigger1
AFTER INSERT ON hotels
FOR EACH ROW
BEGIN
    INSERT INTO hotel_history (action, name_hotel, price, star, link)
    VALUES ('insert', NEW.name_hotel, NEW.price, NEW.star, NEW.link);
END //

DELIMITER ;