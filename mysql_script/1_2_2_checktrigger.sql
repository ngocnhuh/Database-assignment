Hướng đi 1:
DROP PROCEDURE IF EXISTS CheckEmptySeatProcedure;
DELIMITER $$
CREATE PROCEDURE CheckEmptySeatProcedure (IN new_ticket_id INT, IN new_seat_num INT)
BEGIN
	CREATE TABLE ticket_trip_id (ticket_id INT) AS
		(SELECT ticket_id FROM Ticket WHERE Ticket.trip_id IN (SELECT trip_id FROM Ticket WHERE ticket_id = new_ticket_id));
    CREATE TABLE ticket_seat_num AS (
		SELECT Passenger_ticket.seat_num 
		FROM Passenger_ticket, ticket_trip_id 
		WHERE 
			ticket_trip_id.ticket_id = Passenger_ticket.ticket_id
	);
	SELECT @seat_count := COUNT(*) FROM ticket_seat_num WHERE seat_num = new_seat_num;
    DROP TABLE ticket_trip_id;
    DROP TABLE ticket_seat_num;
    IF @seat_count != 0 THEN
		SIGNAL SQLSTATE '50001' SET MESSAGE_TEXT = 'CANNOT INSERT';
	ELSE
		SIGNAL SQLSTATE '50001' SET MESSAGE_TEXT = 'MAYBE INSERT';
	END IF;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS `CheckEmptySeat`;
DELIMITER $$
CREATE  TRIGGER `CheckEmptySeat` BEFORE INSERT ON `Passenger_ticket`
FOR EACH ROW
BEGIN
	CALL CheckEmptySeatProcedure(new.ticket_id, new.seat_num);
END; $$
DELIMITER ;

/* Check hướng đi 1: */
INSERT INTO `Ticket` VALUES
  (32, 1, 'Passenger', 'Ben xe Phu Lam, TP Tuy Hoa, Phu Yen',true,1,1,1,176000);
INSERT INTO `Passenger_ticket` VALUE
	(32, 2);
==> Đoạn này báo lỗi 

Hướng đi 2:

DROP TRIGGER IF EXISTS `CheckEmptySeat`;
DELIMITER $$
CREATE  TRIGGER `CheckEmptySeat` BEFORE INSERT ON `Passenger_ticket`
FOR EACH ROW
BEGIN
	CALL CheckEmptySeatProcedure(new.ticket_id, new.seat_num);

	CREATE TABLE ticket_trip_ id (ticket_id INT) AS
		(SELECT ticket_id FROM Ticket WHERE Ticket.trip_id IN (SELECT trip_id FROM Ticket WHERE ticket_id = new.ticket_id));
    CREATE TABLE ticket_seat_num AS (
		SELECT Passenger_ticket.seat_num 
		FROM Passenger_ticket, ticket_trip_id 
		WHERE 
			ticket_trip_id.ticket_id = Passenger_ticket.ticket_id
	);
	SELECT @seat_count := COUNT(*) FROM ticket_seat_num WHERE seat_num = new.seat_num;
    DROP TABLE ticket_trip_id;
    DROP TABLE ticket_seat_num;
    IF @seat_count != 0 THEN
		SIGNAL SQLSTATE '50001' SET MESSAGE_TEXT = 'CANNOT INSERT';
	ELSE
		SIGNAL SQLSTATE '50001' SET MESSAGE_TEXT = 'CAN INSERT';
	END IF;
    
END; $$
DELIMITER ;~
