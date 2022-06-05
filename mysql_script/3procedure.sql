USE `bus_system`;
DELIMITER $$
DROP PROCEDURE IF EXISTS `AllStaffofTrip`$$
CREATE PROCEDURE `AllStaffofTrip`(IN id int(9) ZEROFILL)
BEGIN
	IF (id NOT IN (SELECT `trip_id` FROM `Trip`))
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Trip_id not found!';
    ELSE
	BEGIN
		SELECT E.ee_id, fname, lname, birth_date, sex,  phone, address, salary,  manager_id, vaccine
		FROM (`Employee` E INNER JOIN `Bus_staff` S ON E.ee_id=S.ee_id)
		WHERE E.ee_id IN (SELECT ee_id FROM `Trip_staff` WHERE trip_id=id)
		ORDER BY vaccine DESC ;
    END;
    END IF;
END; $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS `BestSellerTripSchedule`$$
CREATE PROCEDURE `BestSellerTripSchedule` (IN id int(3) ZEROFILL)
BEGIN
	IF (id NOT IN (SELECT `route_id` FROM `Route`))
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Route_id not found!';
    ELSE
	BEGIN
		SELECT R.route_id, S.sched_id, S.date, S.departure_time, S.arrival_time, COUNT(`ticket_id`) AS total_ticket
		FROM `Trip_schedule` S, `Trip` TR, `Ticket` T, `Route` R
		WHERE S.sched_id= TR.sched_id AND TR.trip_id= T.trip_id AND  R.route_id=S.route_id
		GROUP BY  S.sched_id
		HAVING R.route_id= id
		ORDER BY total_ticket DESC;
    END;
    END IF;
END; $$
DELIMITER ;

/*CALL `AllStaffofTrip`(5);
CALL `BestSellerTripSchedule`(2);*/