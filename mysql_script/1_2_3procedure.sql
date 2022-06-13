USE `bus_system`;
DELIMITER $$
DROP PROCEDURE IF EXISTS `StartingPointTrip`$$
CREATE PROCEDURE `StartingPointTrip`(IN starting_point varchar(30))
BEGIN
	IF (starting_point NOT IN (SELECT `starting_point` FROM `Route`))
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Starting location not found!';
    ELSE
	BEGIN
		SELECT *
		FROM `Trip`
		WHERE `Trip`.sched_id IN (SELECT S.sched_id FROM (`Trip_schedule` S INNER JOIN `Route` R ON S.route_id=R.route_id) WHERE R.starting_point= starting_point ) 
		ORDER BY  `departure_date` DESC ;
    END;
    END IF;
END; $$
DELIMITER ;


USE `bus_system`;
DELIMITER $$
DROP PROCEDURE IF EXISTS `DestinationTrip`$$
CREATE PROCEDURE `DestinationTrip`(IN destination varchar(30))
BEGIN
	IF (destination NOT IN (SELECT `destination` FROM `Route`))
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Destination not found!';
    ELSE
	BEGIN
		SELECT *
		FROM `Trip`
		WHERE `Trip`.sched_id IN (SELECT S.sched_id FROM (`Trip_schedule` S INNER JOIN `Route` R ON S.route_id=R.route_id) WHERE R.destination= destination) 
		ORDER BY  `departure_date` DESC ;
    END;
    END IF;
END; $$
DELIMITER ;

USE `bus_system`;
DELIMITER $$
DROP PROCEDURE IF EXISTS `FindTrip`$$
CREATE PROCEDURE `FindTrip`(IN starting_point varchar(30), IN destination varchar(30))
BEGIN
	IF (starting_point NOT IN (SELECT `starting_point` FROM `Route`))
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Starting location not found!';
    ELSEIF (destination NOT IN (SELECT `destination` FROM `Route`))
	THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Destination not found!';
    ELSE
	BEGIN
		SELECT *
		FROM `Trip`
		WHERE `Trip`.sched_id IN (SELECT S.sched_id FROM (`Trip_schedule` S INNER JOIN `Route` R ON S.route_id=R.route_id) WHERE R.starting_point= starting_point AND R.destination= destination) 
		ORDER BY  `departure_date` DESC ;
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

/*CALL `StartingPointTrip`('DALAT');
CALL `DestinationTrip`('BINHDUONG');
CALL `FindTrip`('TUYHOA','DANANG');
CALL `BestSellerTripSchedule`(2);*/