USE `bus_system`;
/* Phan 1.2.1 - Start */


DROP FUNCTION IF EXISTS check_age_customer;
CREATE FUNCTION check_age_customer(age INT)
RETURNS BOOL DETERMINISTIC
RETURN 0 <= age AND age <= 150;

DROP FUNCTION IF EXISTS check_phone_customer;
DELIMITER $$
CREATE FUNCTION check_phone_customer(phone varchar(20))
RETURNS VARCHAR(1000) DETERMINISTIC
BEGIN 
	DECLARE x INT DEFAULT 1;
    DECLARE flag VARCHAR(1000) DEFAULT 'TRUE';
	IF char_length(phone) != 10 THEN
		SET flag = 'PHONE IS NOT VALID (THE LENGTH OF PHONE IS FALSE)';
	ELSE
		/* Index start = 1*/
		my_loop: WHILE (x <= 10)
        DO
			SET @check_char = SUBSTRING(phone, x, 1);
			IF '0' <= @check_char AND @check_char <= '9' THEN
				SET flag = 'TRUE';
			ELSE 
				SET flag = 'PHONE IS NOT VALID (HAVE CHARACTER NOT NUMBER)';
                LEAVE my_loop;
            END IF;
			SET x = x + 1;
        END WHILE my_loop;
    END IF;
    RETURN flag;
END $$
DELIMITER ;

DROP FUNCTION  IF EXISTS check_email_customer;
DELIMITER $$
CREATE FUNCTION check_email_customer(email varchar(50))
RETURNS VARCHAR(1000) DETERMINISTIC
BEGIN 
	IF (email REGEXP '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)') THEN 
		RETURN 'TRUE';
	ELSE 
		RETURN 'EMAIL IS NOT VALID';
    END IF;
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS insertCustomerData;
DELIMITER $$
CREATE PROCEDURE insertCustomerData (IN fname varchar(50) , IN lname varchar(50), IN birth_date date,
IN phone varchar(20), IN address varchar(50), IN email varchar(50))
	BEGIN
	DECLARE message_error VARCHAR(1000) DEFAULT '';
	SET @age_customer = TIMESTAMPDIFF(YEAR, birth_date, CURDATE());
	IF (NOT check_age_customer(@age_customer)) THEN
		SET message_error = 'AGE IS NOT VALID';
	ELSEIF @age_customer >= 14 THEN
		SET message_error = 'NOT ENOUGH AGE';
	END IF;
    IF (check_phone_customer(phone) != 'TRUE') THEN
		SET message_error = check_phone_customer(phone);
	END IF;
    IF (check_email_customer(email) != 'TRUE') THEN
		SET message_error = check_email_customer(email);
	END IF;
    IF message_error = '' THEN
		INSERT INTO Customer (fname, lname, birth_date, phone, address, email) VALUES (fname, lname, birth_date, phone, address, email);
    ELSE
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = message_error;
	END IF;
    END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS deleteCustomerData;
DELIMITER $$
CREATE PROCEDURE deleteCustomerData (IN customer_id_input INT)
BEGIN
	DELETE FROM Customer WHERE customer_id = customer_id_input;
END $$

DELIMITER ;

/* Phan 1.2.1 - End */