USE hotels;

DELIMITER //

CREATE TRIGGER hotels_trigger3
AFTER DELETE ON hotels
FOR EACH ROW
BEGIN
    INSERT INTO hotel_history (action, name_hotel, price, star, link)
    VALUES ('delete', OLD.name_hotel, OLD.price, OLD.star, OLD.link);
END //

DELIMITER ;

