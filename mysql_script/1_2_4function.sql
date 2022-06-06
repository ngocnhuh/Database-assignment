
USE `bus_system`;
DELIMITER $$
DROP FUNCTION IF EXISTS `total_money`;
CREATE  FUNCTION `total_money`(customer_id_real INT) 
RETURNS INT
    DETERMINISTIC
BEGIN
	DECLARE length INT DEFAULT 0;
	DECLARE counter INT DEFAULT 0;
	DECLARE sum INT DEFAULT 0;
	DECLARE customer_id_1 INT;
	DECLARE total_cost_1 INT;
	SET counter=0;
	SET sum=0;
	SELECT COUNT(*) FROM ticket INTO length;
	WHILE (counter < length) DO
		SELECT customer_id,total_cost INTO customer_id_1,total_cost_1
		FROM ticket LIMIT counter,1;
		IF customer_id_real = customer_id_1 THEN
			SET sum = sum + total_cost_1;
		END IF;
		SET counter = counter + 1;
	END WHILE;
	RETURN sum;
END; $$
DELIMITER ;


DELIMITER $$
DROP FUNCTION IF EXISTS `check_ve`;
CREATE FUNCTION `check_ve`(
	ticket_id_1 INT
) RETURNS decimal(10,0)
    DETERMINISTIC
BEGIN
  DECLARE customer_id_1 INT;
  DECLARE program_id_1 INT;
  DECLARE total_cost_1 INT;
  DECLARE is_right BOOL;
  DECLARE my_level INT default -1;
  DECLARE trip_id_1 INT;
  DECLARE ticket_type_1 VARCHAR(20);
  DECLARE price_1 INT;
  DECLARE price_2 INT;
  DECLARE sched_id_1 INT;
  DECLARE require_is INT;
  DECLARE discount FLOAT;
    
  SELECT 	customer_id,program_id,trip_id,ticket_type
		INTO customer_id_1,program_id_1,trip_id_1,ticket_type_1
  FROM ticket
  WHERE ticket_id_1=ticket_id;
    
  SELECT sched_id
	  INTO sched_id_1
	FROM trip
  WHERE (trip_id_1 = trip_id);
    
  SELECT passenger_price,luggage_price
  	INTO price_1,price_2
	FROM trip_schedule
  WHERE (sched_id_1 = sched_id);
		
  IF ticket_type_1 = 'Luggage' THEN
		SET price_1 = price_2;
	END IF;
    
  SELECT level
		INTO my_level
	FROM membership
  WHERE (customer_id_1 = membership.customer_id);
    
  SELECT discount_rate,require_level
		INTO discount,require_is
	FROM sales_promotion
	WHERE (program_id = program_id_1);
    
    
  IF my_level IS NULL THEN
		RETURN price_1;
	ELSEIF my_level >= require_is THEN
		RETURN price_1*(1-discount);
	ELSE RETURN price_1;
	END IF;    
    RETURN price_1;
END; $$
DELIMITER ;

/*SELECT ticket_id, check_ve(ticket_id) AS paid
FROM `Ticket`
ORDER BY ticket_id ASC;*/


/*SELECT customer_id, total_money(customer_id) AS total_money
FROM `Customer`
ORDER BY total_money DESC;*/

