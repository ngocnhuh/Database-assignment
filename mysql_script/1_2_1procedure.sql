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
    if(@age_customer IS NULL) THEN
		SET message_error = '';
	ELSEIF (NOT check_age_customer(@age_customer)) THEN
		SET message_error = 'AGE IS NOT VALID';
	ELSEIF @age_customer < 14 THEN
		SET message_error = 'NOT ENOUGH AGE';
    ELSEIF (check_phone_customer(phone) != 'TRUE') THEN
		SET message_error = check_phone_customer(phone);
    ELSEIF (check_email_customer(email) != 'TRUE') THEN
		SET message_error = check_email_customer(email);
	END IF;
    IF message_error = '' THEN
		INSERT INTO Customer (fname, lname, birth_date, phone, address, email) VALUES (fname, lname, birth_date, phone, address, email);
    ELSE
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = message_error;
	END IF;
    END $$
DELIMITER ;

CALL insertCustomerData('Le','Minh Cong','1982-05-22','0902005932','12 Le Duan, Tuy Hoa', 'minhcongth123@gmail.com');

DROP PROCEDURE IF EXISTS updateCustomerData;
DELIMITER $$
CREATE PROCEDURE updateCustomerData (IN up_customer_id int(11), IN up_fname varchar(50) , IN up_lname varchar(50), IN up_birth_date date,
IN up_phone varchar(20), IN up_address varchar(50), IN up_email varchar(50))
BEGIN
	DECLARE done INT DEFAULT FALSE;
	DECLARE message_error VARCHAR(1000) DEFAULT '';
    DECLARE flag BOOL DEFAULT FALSE;
    DECLARE current_cus_id INT(11);
    DECLARE get_customer_id CURSOR FOR SELECT Customer.customer_id FROM Customer;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	OPEN get_customer_id;
    my_loop: LOOP
		FETCH get_customer_id INTO current_cus_id;
        IF done THEN LEAVE my_loop;
        END IF;
        IF (current_cus_id = up_customer_id) THEN
			SET flag = TRUE;
        END IF;
    END LOOP;
    CLOSE get_customer_id;
    SET @age_customer = TIMESTAMPDIFF(YEAR, up_birth_date, CURDATE());
    IF (flag = FALSE) THEN
		SET message_error = 'NOT EXIST CUSTOMER ID';
	ELSEIF (up_birth_date IS NULL) THEN
		SET message_error = '';
	ELSEIF (NOT check_age_customer(@age_customer)) THEN
		SET message_error = 'AGE IS NOT VALID';
	ELSEIF @age_customer < 14 THEN
		SET message_error = 'NOT ENOUGH AGE';
    ELSEIF (check_phone_customer(up_phone) != 'TRUE') THEN
		SET message_error = check_phone_customer(up_phone);
    ELSEIF (check_email_customer(up_email) != 'TRUE') THEN
		SET message_error = check_email_customer(up_email);
	END IF;
    IF message_error = '' THEN
		UPDATE Customer 
        SET
            fname = up_fname,
            lname = up_lname,
            birth_date = up_birth_date,
            phone = up_phone,
            address = up_address,
            email = up_email
        WHERE 
			customer_id = up_customer_id;
    ELSE
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = message_error;
	END IF;
END $$
DELIMITER ;

/*
CALL updateCustomerData(12, 'Le','Minh Cong', '2000-12-15','01234567u9','Dak Lak', 'minhcongth123@@gmail.com');
CALL updateCustomerData(100, 'Le','Minh Cong', '2000-12-15','01234567u9','Dak Lak', 'minhcongth123@@gmail.com');
-- => Error Code: 1644. NOT EXIST CUSTOMER ID
CALL updateCustomerData(12, 'Le','Minh Cong', '1799-12-15','01234567u9','Dak Lak', 'minhcongth123@@gmail.com');
-- => Error Code: 1644. AGE IS NOT VALID
CALL updateCustomerData(12, 'Le','Minh Cong', '2010-12-15','01234567u9','Dak Lak', 'minhcongth123@@gmail.com');
-- => Error Code: 1644. NOT ENOUGH AGE
CALL updateCustomerData(12, 'Le','Minh Cong', '1999-12-15','01234567u9','Dak Lak', 'minhcongth123@@gmail.com');
-- => Error Code: 1644. PHONE IS NOT VALID (HAVE CHARACTER NOT NUMBER)
CALL updateCustomerData(12, 'Le','Minh Cong', '1999-12-15','01234567119','Dak Lak', 'minhcongth123@@gmail.com');
-- => Error Code: 1644. PHONE IS NOT VALID (THE LENGTH OF PHONE IS FALSE)
CALL updateCustomerData(12, 'Le','Minh Cong', '1999-12-15','0987654321','Dak Lak', 'minhcongth123@@gmail.com');
-- => Error Code: 1644. EMAIL IS NOT VALID
CALL updateCustomerData(12, 'Le','Minh Cong', NULL,'0987654321','Dak Lak', 'minhcongth123@gmail.com');
-- => Success : Accept NULL for column `birth_date`
*/

DROP PROCEDURE IF EXISTS deleteCustomerData;
DELIMITER $$
CREATE PROCEDURE deleteCustomerData (IN customer_id_input INT)
BEGIN
	DELETE FROM Customer WHERE customer_id = customer_id_input;
END $$

DELIMITER ;
CALL deleteCustomerData(11);
/* Phan 1.2.1 - End */