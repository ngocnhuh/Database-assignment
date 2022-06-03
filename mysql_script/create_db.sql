DROP DATABASE IF EXISTS `bus_system`;
CREATE DATABASE `bus_system`; 
USE `bus_system`;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;
CREATE TABLE `Employee` (
  `ee_id` int(5) ZEROFILL NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `sex` enum('F','M'),
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `salary`  decimal(10,2),
  `manager_id` int(5) ZEROFILL,
  PRIMARY KEY (`ee_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Driver`(
  `ee_id` int(5) ZEROFILL NOT NULL,
  `license_id` varchar(20) NOT NULL,
  `exp_year` tinyint NOT NULL,
  PRIMARY KEY (`ee_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Bus_staff`(
  `ee_id` int(5) ZEROFILL NOT NULL,
  `vaccine`tinyint(1) NOT NULL,
  PRIMARY KEY (`ee_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Manager`(
  `ee_id` int(5) ZEROFILL NOT NULL,
  `certificate_id` varchar(20),
  PRIMARY KEY (`ee_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Telephone_staff`(
  `ee_id` int(5) ZEROFILL NOT NULL,
  PRIMARY KEY (`ee_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Tele_shift`(
  `shift_id` int(7) ZEROFILL NOT NULL AUTO_INCREMENT,
  `ee_id` int(5) ZEROFILL NOT NULL,
  `date` enum('MON','TUE','WED','THU','FRI','SAT','SUN') NOT NULL,
  `start` time NOT NULL,
  `till`  time NOT NULL,
  PRIMARY KEY (`shift_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Bus`(
  `bus_id` varchar(10) NOT NULL,
  `bustype` enum('NORMAL','LIMO','VIP'),
  `total_seat` tinyint NOT NULL,
  `maxload` int NOT NULL,
  `sleeper_type` enum('SINGLE','DOUBLE','CABIN'),
  PRIMARY KEY (`bus_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Route`(
  `route_id` int(3) ZEROFILL NOT NULL AUTO_INCREMENT,
  `starting_point` varchar(30) NOT NULL,
  `destination` varchar(30) NOT NULL,
  `distance` int,
  `total_time` time,
  PRIMARY KEY (`route_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Stop`(
  `stop_id` int(5) ZEROFILL NOT NULL AUTO_INCREMENT,
  `route_id` int(3) ZEROFILL NOT NULL,
  `stop_address` varchar(100) NOT NULL,
  PRIMARY KEY (`stop_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Trip_schedule`(
  `sched_id` int(2) ZEROFILL NOT NULL AUTO_INCREMENT,
  `route_id` int(3) ZEROFILL NOT NULL,
  `passenger_price` decimal(10,2) NOT NULL,
  `luggage_price`   decimal(10,2) NOT NULL,
  `date` enum('MON','TUE','WED','THU','FRI','SAT','SUN') NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_time` time,
  `bustype` enum('NORMAL','LIMO','VIP'),
  PRIMARY KEY (`sched_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Trip`(
  `trip_id` int(9) ZEROFILL NOT NULL AUTO_INCREMENT,
  `sched_id` int(2) ZEROFILL NOT NULL,
  `departure_time`timestamp NOT NULL,
  `arrival_time`  timestamp,
  `bus_id` varchar(10) NOT NULL,
  `driver_id` int(5) ZEROFILL,
  `empty_seats` tinyint NOT NULL,
  PRIMARY KEY (`trip_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Trip_staff`(
  `staff_id` int(11) ZEROFILL NOT NULL AUTO_INCREMENT,
  `trip_id` int(9) ZEROFILL NOT NULL,
  `ee_id` int(5) ZEROFILL ,
  PRIMARY KEY ( `staff_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Customer`(
  `customer_id` int(11) ZEROFILL NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `phone` varchar(20),
  `address` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customer_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Membership_level` (
  `level_id` tinyint(1) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Membership`(
  `member_id` int(11) ZEROFILL NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) ZEROFILL NOT NULL UNIQUE,
  `start` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `end` datetime DEFAULT NULL,
  `level` tinyint(1) DEFAULT 1 NOT NULL,
  `points` int DEFAULT 0 NOT NULL,
  PRIMARY KEY (`member_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Sales_promotion`(
  `program_id` int(9) NOT NULL AUTO_INCREMENT,
  `description` varchar(100),
  `discount_rate` float(5, 2) NOT NULL,
  `require_level` tinyint(1) DEFAULT 0,
  `start` timestamp NOT NULL,
  `end` timestamp NOT NULL,
  PRIMARY KEY (`program_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Payment_methods` (
  `method_id` tinyint(1) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`method_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Ticket`(
  `ticket_id` int(11) ZEROFILL NOT NULL AUTO_INCREMENT,
  `trip_id` int(9) ZEROFILL NOT NULL,
  `ticket_type` enum('Passenger','Luggage') NOT NULL,
  `start_location` varchar(50) NOT NULL,
  `paid`     boolean NOT NULL,
  `payment_method` tinyint(1),
  `customer_id` int(11) ZEROFILL NOT NULL,
  `program_id` int(9),
  `total_cost` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ticket_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Passenger_ticket`(
  `ticket_id` int(11) ZEROFILL NOT NULL,
  `seat_num` tinyint NOT NULL,
  PRIMARY KEY (`ticket_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Luggage_ticket`(
  `ticket_id` int(11) ZEROFILL NOT NULL,
  `weight` int NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*ADD CONSTRAINT*/

ALTER TABLE `Employee`
ADD CONSTRAINT  `fk_ee_managerid` FOREIGN KEY (`manager_id`) REFERENCES `Manager` (`ee_id`) ON DELETE SET NULL;
  
ALTER TABLE `Driver`
ADD ( CONSTRAINT  `fk_driver_eeid` FOREIGN KEY (`ee_id`) REFERENCES `Employee` (`ee_id`) ON DELETE CASCADE ON UPDATE CASCADE,
      CONSTRAINT `chk_exp_driver` CHECK (`exp_year`>=5),
      CONSTRAINT `chk_license_driver` CHECK (`license_id`LIKE 'E%' OR `license_id`LIKE 'F%') );

ALTER TABLE `Bus_staff`
ADD ( CONSTRAINT  `fk_staff_eeid` FOREIGN KEY (`ee_id`) REFERENCES `Employee` (`ee_id`) ON DELETE CASCADE ON UPDATE CASCADE,
      CONSTRAINT `chk_require_staff` CHECK (`vaccine`>=2));

ALTER TABLE `Manager`
ADD CONSTRAINT  `fk_manager_eeid` FOREIGN KEY (`ee_id`) REFERENCES `Employee` (`ee_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Telephone_staff`
ADD CONSTRAINT  `fk_tele_eeid` FOREIGN KEY (`ee_id`) REFERENCES `Employee` (`ee_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Tele_shift`
ADD CONSTRAINT  `fk_teleshift_eeid` FOREIGN KEY (`ee_id`) REFERENCES `Telephone_staff` (`ee_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Stop`
ADD CONSTRAINT  `fk_stop_routeid` FOREIGN KEY (`route_id`) REFERENCES `Route` (`route_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Trip_schedule`
ADD CONSTRAINT  `fk_sched_routeid` FOREIGN KEY (`route_id`) REFERENCES `Route` (`route_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `Trip`
ADD ( CONSTRAINT  `fk_trip_routeid` FOREIGN KEY (`sched_id`) REFERENCES `Trip_schedule` (`sched_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
      CONSTRAINT  `fk_trip_busid` FOREIGN KEY (`bus_id`) REFERENCES `Bus` (`bus_id`) ON DELETE NO ACTION ON UPDATE CASCADE,
	    CONSTRAINT  `fk_trip_driverid` FOREIGN KEY (`driver_id`) REFERENCES `Driver` (`ee_id`) ON DELETE SET NULL);

ALTER TABLE `Trip_staff`
ADD ( CONSTRAINT  `fk_tripstaff_tripid` FOREIGN KEY (`trip_id`) REFERENCES `Trip` (`trip_id`) ON DELETE CASCADE ON UPDATE CASCADE,
      CONSTRAINT  `fk_tripstaff_eeid` FOREIGN KEY (`ee_id`) REFERENCES `Bus_staff` (`ee_id`) ON DELETE SET NULL);
  
ALTER TABLE `Membership`
ADD (CONSTRAINT  `fk_member_customerid` FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
     CONSTRAINT  `fk_member_level` FOREIGN KEY (`level`) REFERENCES `Membership_level` (`level_id`) ON DELETE RESTRICT ON UPDATE CASCADE);
  
ALTER TABLE `Ticket`
ADD ( CONSTRAINT  `fk_ticket_tripid` FOREIGN KEY (`trip_id`) REFERENCES `Trip` (`trip_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
      CONSTRAINT  `fk_ticket_customerid` FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
      CONSTRAINT  `fk_ticket_paymethod` FOREIGN KEY (`payment_method`) REFERENCES `Payment_methods` (`method_id`) ON DELETE SET NULL, 
      CONSTRAINT  `fk_ticket_programid` FOREIGN KEY (`program_id`) REFERENCES `Sales_promotion` (`program_id`) ON DELETE SET NULL);

ALTER TABLE `Passenger_ticket`
ADD CONSTRAINT  `fk_passenger_ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`ticket_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Luggage_ticket`
ADD CONSTRAINT  `fk_luggage_ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `Ticket` (`ticket_id`) ON DELETE CASCADE ON UPDATE CASCADE;

DELIMITER $$
CREATE  TRIGGER `EmptySeat` AFTER INSERT ON `Passenger_ticket`
FOR EACH ROW
BEGIN
	UPDATE `Trip` 
    SET empty_seats = empty_seats -1
    WHERE `Trip`.trip_id IN (SELECT trip_id FROM  `Ticket` WHERE ticket_id= new.ticket_id);
END; $$
DELIMITER ;

/*INSERT DATA*/

INSERT INTO `Employee` VALUES
  (1,'Le','Van Anh','2002-11-04','F','0905682025','123 Kha Van Can, BINH DUONG', 5000000, NULL),
  (2,'Nguyen','Thi Bao','1992-01-01','F','0935992016','123 Nguyen Van Cu, TPHCM', 7000000, NULL),
  (3,'Tran','Cong','1987-11-11','M','0124987654','1A Le Do, TPHCM ', 15000000, NULL),
  (4,'Do','Thi Danh','2000-10-05','F','0902540136','12 Tran Hung Dao, TPHCM', 7000000, NULL),
  (5,'Nguyen','Thanh Binh','1991-02-28','M','0211456897','56B Nguyen Trai, TPHCM', 8000000, NULL),
  (6,'Ha','Phi Dung','1995-05-01','M','0905467792','78 Le Loi, TPHCM', 15000000, NULL),
  (7,'Tran','Ngoc Duong','1999-12-01','M','0126527867','34 Le Quy Don, TPTHUDUC ', 5000000, NULL),
  (8,'Tran','Thi Huong','1995-10-24','F','0902111324','56 Vo Van Tan, TPHCM', 7000000, NULL),
  (9,'Hoang','Van Nguyen ','1996-07-03','M','0905246438','26 Luy Ban Bich, BINH DUONG', 8000000, NULL),
  (10,'Nguyen','Phi Hung','1992-09-01','F','0935782022','224 Nguyen Van Bang, TPHCM', 10000000, NULL);

INSERT INTO `Telephone_staff` VALUES
  (1),
  (7);
  
INSERT INTO `Manager` VALUES
  (3,'4678-7253-3554'),
  (6,'4623-9675-2136');

UPDATE `Employee`
SET `manager_id` = 3
WHERE `ee_id` IN (1,5,7,9);

UPDATE `Employee`
SET `manager_id` = 6
WHERE `ee_id` IN (2,4,8,10);

INSERT INTO `Driver` VALUES
  (2,'E14518775952457',5),
  (10,'F1231967521366',10);

INSERT INTO `Bus_staff` VALUES
  (4,3),
  (5,2),
  (8,2),
  (9,3);

INSERT INTO `Tele_shift` VALUES
  (1,1,'MON','7:00','10:00'),
  (2,1,'MON','16:00','19:00'),
  (3,7,'MON','10:00','13:00'),
  (4,7,'MON','13:00','16:00'),
  (5,1,'WED','7:00','10:00'),
  (6,1,'WED','16:00','19:00'),
  (7,7,'WED','10:00','13:00'),
  (8,7,'WED','13:00','16:00'),
  (9,1,'FRI','7:00','10:00'),
  (10,1,'FRI','16:00','19:00'),
  (11,7,'FRI','10:00','13:00'),
  (12,7,'FRI','13:00','16:00');

INSERT INTO `Bus` VALUES 
  ('51B-001.72','NORMAL',30, 16000,'DOUBLE'),
  ('60B-745.98','LIMO',20, 12000,NULL),
  ('51B-273.39','NORMAL',25, 20000,'SINGLE'),
  ('51B-021.99','VIP',15, 16000,'CABIN'),
  ('51B-001.18','LIMO',30, 25000,'SINGLE');
  
INSERT INTO `Route` VALUES 
  (1,'TUYHOA','DANANG','410','8:30'),
  (2,'DALAT','TPHCM','310','6:40'),
  (3,'TPHCM','DAKLAK','348','7:10'),
  (4,'NINHTHUAN','BINHDUONG','385','7:25'),
  (5,'TPHCM','NHATRANG','435','8:45');
  
INSERT INTO `Stop` VALUES
  (1, 1, '227 Nguyen Tat Thanh TP Tuy Hoa, Phu Yen'),
  (2, 1, 'Ben xe Phu Lam, TP Tuy Hoa, Phu Yen'),
  (3, 1, 'Ben xe khach Da Nang, Cam Le, Da Nang'),
  (4, 2, 'Buu dien thanh pho Da Lat'),
  (5, 2, 'Hoa An, Dau Giay, Dong Nai'),
  (6, 2, 'Hoi cho trien lam Tan Binh'),
  (7, 3, '266 Dong Den, P10, Tan Binh, TPHCM'),
  (8, 3, 'Cho Dau Moi Tan Hoa 555 Pham Van Dong, Buon Ma Thuot'),
  (9, 3, '134 Hai Ba Trung, Buon Ma Thuot'),
  (10, 4, 'Ben Xe Mien Dong, TPHCM'),
  (11, 4, '248 Le Duan, Phan Rang-Thap Cham, Ninh Thuan'),
  (12, 5, '138 Nguyen Cu Trinh, Quan 1, TPHCM'),
  (13, 5, 'Kiot 8 Khach san Muong Thanh 4 Tran Phu, Nha Trang');
  
INSERT INTO `Trip_schedule` VALUES
  (1, 1, 220000,75000, 'MON', '7:00','15:30','NORMAL'),
  (2, 1, 280000,90000, 'TUE', '12:00','20:30','LIMO'),
  (3, 2, 380000,90000, 'MON', '8:00','22:00','LIMO'),
  (4, 2, 300000,80000, 'TUE', '8:00','22:00','NORMAL'),
  (5, 2, 350000,80000, 'SAT', '8:00','22:00','NORMAL'),
  (6, 3, 300000,75000, 'WED', '11:30','18:40','VIP'),
  (7, 4, 180000,55000, 'MON', '7:00','14:30','NORMAL'),
  (8, 4, 160000,55000, 'THU', '7:00','14:30','NORMAL'),
  (9, 5, 350000,80000, 'MON', '6:00','14:45','LIMO'),
  (10, 5, 350000,80000, 'SUN', '12:00','20:45','LIMO');

INSERT INTO `Trip` VALUES
  (1,1,'2022-05-30 7:00:00','2022-05-30 15:30:00','51B-001.72',2,30),
  (2,2,'2022-05-31 12:00:00','2022-05-31 20:30:00','60B-745.98',10,20),
  (3,3,'2022-05-30 8:00:00','2022-05-30 22:00:00','51B-001.18',2,30);
  
INSERT INTO `Trip_staff` VALUES
  (1, 1,4),
  (2, 1,8),
  (3, 2,5),
  (4, 2,9),
  (5, 3,4),
  (6, 3,9);

INSERT INTO `Customer` VALUES
  (1,'Le','Duc Hai','1997-01-10','0902005505','170/04 Duong so 204 Cao Lo, P.04, Quan 8, TPHCM', 'haiduc123@gmail.com'),
  (2,'Le','Hoang Son','1999-07-27','0905124506','615 KP2 To Hieu, TPHCM', 'hoangsonle@gmail.com'),
  (3,'Phan','Thi Truc Vy','1991-03-04','0902312446','6 Tran Huy Hieu, P.12, Quan Phu Nhuan, TPHCM', 'vy345@yahoo.com'),
  (4,'Truong','Thi Minh','2000-02-14','0901329909','274 Ngo Quyen, P.01, Quan 10, TPHCM', 'minhtruong34563@gmail.com'),
  (5,'Tran','Thi Anh Nguyet','1978-01-17','0902464945','180B Le Van Sy, Tuy Hoa', 'nguyetmoon@gmail.com'),
  (6,'Le','Tuan Kiet','1969-05-25','0905212378','128 Hai Phong, Hai Chau, Da Nang', 'kietmail123@gmail.com'),
  (7,'Nguyen','Doan Quan','1998-06-19','0905682025','1188 Pham The Hien, Tuy Hoa', 'quandoan1998@gmail.com'),
  (8,'Tran','Anh Tuan','1995-02-27','0935679431','140 Tran Dai Nghia, Lam Dong', 'tuanld@gmail.com'),
  (9,'Vo','Thi Thi','1994-04-20','0902813471','269A Tan Huong, P. Tan Quy, Quan Tan Phu, TPHCM', 'thithi0420@gmail.com'),
  (10,'Le','Minh Cong','1982-05-22','0902005932','12 Le Duan, Tuy Hoa', 'minhcongth123@gmail.com');

INSERT INTO `Membership_level` VALUES
  (1,'Dong'),
  (2,'Bac'),
  (3,'Vang');

INSERT INTO `Membership` VALUES
  (1,1,'2020-01-01 12:00:00', '2025-01-01 12:00:00', 2,150),
  (2,10,'2019-02-12 15:30:00', '2024-02-12 15:30:00',1,30);
  
INSERT INTO `Sales_promotion` VALUES
  (1,'SummerSale', 0.2, 2, '2022-05-01 00:00:00', '2022-06-01 00:00:00');

INSERT INTO `Payment_methods` VALUES  
  (1,'Transfer'),
  (2,'Cash');
  
INSERT INTO `Ticket` VALUES
  (1, 1, 'Passenger', 'Ben xe Phu Lam, TP Tuy Hoa, Phu Yen',true,1,1,1,176000),
  (2, 1, 'Passenger', 'Ben xe Phu Lam, TP Tuy Hoa, Phu Yen',true,2,4,1,220000),
  (3, 1, 'Passenger', '227 Nguyen Tat Thanh TP Tuy Hoa, Phu Yen', true, 2, 3, 1,220000),
  (4, 2, 'Luggage' ,'Ben xe Phu Lam, TP Tuy Hoa, Phu Yen',true,2,2,1,90000),
  (5, 2, 'Passenger', '227 Nguyen Tat Thanh TP Tuy Hoa, Phu Yen', true,1,5,1,280000),
  (6, 2, 'Passenger', '227 Nguyen Tat Thanh TP Tuy Hoa, Phu Yen',true,1,6,1,280000),
  (7, 3, 'Passenger', 'Da Lat', true,2, 7, 1,380000),
  (8, 3, 'Passenger', 'Da Lat', true,2, 8, 1,380000),
  (9, 3, 'Passenger', 'Da Lat', true, 2, 9, 1,380000),
  (10, 3, 'Luggage', 'Hoa An, Dau Giay, Dong Nai', true, 1, 10, 1,90000);

INSERT INTO `Passenger_ticket` VALUES
  (1,'1'),
  (2,'2'),
  (3,'3'),
  (5, '1'),
  (6,'2'),
  (7,'1'),
  (8,'2'),
  (9,'3');

INSERT INTO `Luggage_ticket` VALUES
  (4,5,'Rau xanh'),
  (9,20,'Hang hoa');