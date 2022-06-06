USE `bus_system`;

DROP TRIGGER IF EXISTS `CheckEmptySeat`;
DELIMITER $$
CREATE  TRIGGER `CheckEmptySeat` BEFORE INSERT ON `Passenger_ticket`
FOR EACH ROW
BEGIN
	DECLARE done INT DEFAULT FALSE;
    DECLARE check_trip_id, check_seat_num, a, b INT;
	DECLARE get_trip_id CURSOR FOR SELECT Ticket.ticket_id, Ticket.trip_id FROM Ticket;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	SELECT trip_id
		INTO check_trip_id 
		FROM Ticket
		WHERE Ticket.ticket_id = new.ticket_id;
    OPEN get_trip_id;
	my_loop: LOOP
		FETCH get_trip_id INTO a, b;
        IF done THEN
			LEAVE my_loop;
		END IF;
		IF (b = check_trip_id AND a != new.ticket_id) THEN
			SELECT Passenger_ticket.seat_num INTO check_seat_num FROM Passenger_ticket WHERE a = Passenger_ticket.ticket_id;
			IF check_seat_num = new.seat_num THEN
				SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CANNOT INSERT (EXISTED SEAT NUM)';
			END IF;
		END IF;
	END LOOP;
    -- SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CAN INSERT';
    CLOSE get_trip_id;
END; $$
DELIMITER ;

/* 
DELETE FROM Ticket WHERE ticket_id = 32;
INSERT INTO `Ticket` VALUES
  (32, 1, 'Passenger', 'Ben xe Phu Lam, TP Tuy Hoa, Phu Yen',true,1,1,1,176000);
INSERT INTO `Passenger_ticket` VALUE
	(32, 2);    -- ==> Error
INSERT INTO `Passenger_ticket` VALUE
	(32, 4);    -- ==> Success
*/ 

DROP TRIGGER IF EXISTS check_empty_weight;
DELIMITER $$
CREATE TRIGGER check_empty_weight BEFORE INSERT ON `Luggage_ticket`
FOR EACH ROW
BEGIN
	DECLARE done INT DEFAULT FALSE;
    DECLARE check_trip_id, max_weight, a, b, loop_weight INT;
    DECLARE check_bus_id VARCHAR(10);
    DECLARE sum_weight INT DEFAULT 0;
	DECLARE get_weight_current CURSOR FOR SELECT Ticket.ticket_id, Ticket.trip_id FROM Ticket;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    SELECT trip_id INTO check_trip_id FROM Ticket WHERE ticket_id = new.ticket_id;
    SELECT bus_id INTO check_bus_id FROM Trip WHERE check_trip_id = trip_id;
    SELECT maxload INTO max_weight FROM bus WHERE check_bus_id = bus_id;
    
    OPEN get_weight_current; 
    my_loop: LOOP
		FETCH get_weight_current INTO a, b;
        IF done THEN LEAVE my_loop; 
		END IF;
        IF (b = check_trip_id AND a != new.ticket_id) THEN
			SELECT weight INTO loop_weight FROM Luggage_ticket WHERE a = ticket_id;
            SET sum_weight = sum_weight + loop_weight;
		END IF;
        IF (sum_weight + new.weight > max_weight) THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CANNOT INSERT (OVERLOAD)';
		END IF;
    END LOOP;
    CLOSE get_weight_current;
END $$
DELIMITER ;

/*
DELETE FROM Ticket WHERE ticket_id = 33;
INSERT INTO `Ticket` VALUES
  (33, 2, 'Luggage', 'Ben xe Phu Lam, TP Tuy Hoa, Phu Yen',true,1,1,1,176000);
INSERT INTO `Luggage_ticket` VALUE
	(33, 11997, 'De vo');  -- ==> Error
INSERT INTO `Luggage_ticket` VALUE
	(33, 100, 'De vo');    -- ==> Success
*/