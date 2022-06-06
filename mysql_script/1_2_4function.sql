
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
  DECLARE require_is INT;
  DECLARE discount FLOAT;
    
  SELECT 	customer_id,program_id,total_cost
		INTO customer_id_1,program_id_1,total_cost_1
  FROM ticket
  WHERE ticket_id_1=ticket_id;  
    
  SELECT level
	  INTO my_level
  FROM membership
  WHERE (customer_id_1 = membership.customer_id);
    
  SELECT discount_rate,require_level
    INTO discount,require_is
	FROM sales_promotion
  WHERE (program_id = program_id_1);  
    
    
  IF my_level IS NULL THEN
		RETURN total_cost_1;
	ELSEIF my_level >= require_is THEN
		RETURN total_cost_1*(1-discount);
	ELSE RETURN total_cost_1;
	END IF;    
  RETURN my_level;
END; $$
DELIMITER ;

/*SELECT ticket_id, check_ve(ticket_id) AS paid
FROM `Ticket`
ORDER BY ticket_id ASC;*/


/*SELECT customer_id, total_money(customer_id) AS total_money
FROM `Customer`
ORDER BY total_money DESC;*/

