CREATE DATABASE IF NOT EXISTS `cricketwc` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cricketwc`;

-- Create independent tables first
CREATE TABLE `admin` (
  `user_id` varchar(12) NOT NULL,
  `password` varchar(30) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stadium` (
  `stadium_id` varchar(10) NOT NULL,
  `stadium_name` varchar(30) DEFAULT NULL,
  `pitch_type` char(10) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`stadium_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `team` (
  `team_id` varchar(3) NOT NULL,
  `no_of_batsmen` int DEFAULT NULL,
  `no_of_bowlers` int DEFAULT NULL,
  `country_name` char(30) DEFAULT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `matches` (
  `match_id` varchar(5) NOT NULL,
  `match_time` time DEFAULT NULL,
  `match_date` date DEFAULT NULL,
  `result` char(30) NOT NULL,
  `team1` char(30) NOT NULL,
  `team2` char(30) NOT NULL,
  PRIMARY KEY (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `player` (
  `player_id` varchar(10) NOT NULL,
  `player_name` char(30) NOT NULL,
  `dob` date DEFAULT NULL,
  `type_of_player` char(10) DEFAULT NULL,
  `t20` int DEFAULT NULL,
  `test` int DEFAULT NULL,
  `odi` int DEFAULT NULL,
  `batting_average` int DEFAULT NULL,
  `no_of_sixes` int DEFAULT NULL,
  `no_of_fours` int DEFAULT NULL,
  `economy` int DEFAULT NULL,
  `no_of_wickets` int DEFAULT NULL,
  `highest_run_scored` int DEFAULT NULL,
  `total_runs` int DEFAULT NULL,
  `team_id` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`player_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `player_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create dependent tables
CREATE TABLE `captain` (
  `name` char(30) DEFAULT NULL,
  `years_of_captaincy` int DEFAULT NULL,
  `no_of_wins` int DEFAULT NULL,
  `player_id` varchar(10) DEFAULT NULL,
  KEY `player_id` (`player_id`),
  CONSTRAINT `captain_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `contains` (
  `team_id` varchar(3) DEFAULT NULL,
  `player_id` varchar(10) DEFAULT NULL,
  KEY `team_id` (`team_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `contains_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`),
  CONSTRAINT `contains_ibfk_2` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `played_in` (
  `stadium_id` varchar(10) DEFAULT NULL,
  `match_id` varchar(5) DEFAULT NULL,
  KEY `stadium_id` (`stadium_id`),
  KEY `match_id` (`match_id`),
  CONSTRAINT `played_in_ibfk_1` FOREIGN KEY (`stadium_id`) REFERENCES `stadium` (`stadium_id`),
  CONSTRAINT `played_in_ibfk_2` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `plays` (
  `team_id` varchar(3) DEFAULT NULL,
  `match_id` varchar(5) DEFAULT NULL,
  KEY `team_id` (`team_id`),
  KEY `match_id` (`match_id`),
  CONSTRAINT `plays_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`),
  CONSTRAINT `plays_ibfk_2` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `umpire` (
  `umpire_id` varchar(10) NOT NULL,
  `umpire_name` char(30) DEFAULT NULL,
  `no_of_matches` int DEFAULT NULL,
  `country` char(30) DEFAULT NULL,
  PRIMARY KEY (`umpire_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `umpired_by` (
  `umpire_id` varchar(10) DEFAULT NULL,
  `match_id` varchar(5) DEFAULT NULL,
  KEY `umpire_id` (`umpire_id`),
  KEY `match_id` (`match_id`),
  CONSTRAINT `umpired_by_ibfk_1` FOREIGN KEY (`umpire_id`) REFERENCES `umpire` (`umpire_id`),
  CONSTRAINT `umpired_by_ibfk_2` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert data after tables are created
INSERT INTO `admin` VALUES ('user1','user1password'),('user2','user2password');
INSERT INTO `stadium` VALUES ('S001','Eden Gardens','Grass','Kolkata'),('S002','MCG','Turf','Melbourne'),('S003','Lords','Grass','London'),('S004','Dubai Int. Cricket Stadium','Turf','Dubai'),('S005','SuperSport Park','Grass','Centurion');
INSERT INTO `team` VALUES ('AFG',6,5,'Afghanistan'),('AUS',6,5,'Australia'),('ENG',8,3,'England'),('IND',7,4,'India'),('PAK',7,4,'Pakistan'),('SA',6,5,'South Africa');
INSERT INTO `matches` VALUES ('M001', '14:00:00', '2024-11-20', 'Pending', 'IND', 'AUS'), ('M002', '18:00:00', '2024-11-21', 'Pending', 'ENG', 'PAK');

-- Insert umpires
INSERT INTO umpire (umpire_id, umpire_name, no_of_matches, country) 
VALUES ('UMP046', 'Anil Chaudhary', 106, 'India'),
       ('UMP101', 'Aleem Dar', 42, 'Pakistan'),
       ('UMP115', 'Tony Hill', 96, 'New Zealand');

-- Insert umpired_by
INSERT INTO umpired_by (umpire_id, match_id) 
VALUES ('UMP046', 'M001'),
       ('UMP101', 'M002');

-- Create the function to calculate batting average
DELIMITER //

CREATE FUNCTION calculate_batting_average(total_runs INT, odi INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE batting_avg INT;
    -- Calculate batting average
    IF odi > 0 THEN
        SET batting_avg = total_runs / odi;
    ELSE
        SET batting_avg = 0; -- Default if odi is 0 or NULL
    END IF;
    RETURN batting_avg;
END//

DELIMITER ;

-- Insert into player using the function to calculate batting_average
INSERT INTO player 
(player_id, player_name, dob, type_of_player, t20, test, odi, total_runs, batting_average, team_id) 
VALUES 
('P001', 'Virat Kohli', '1988-11-05', 'Batsman', 75, 95, 254, 11867, calculate_batting_average(11867, 254), 'IND'),
('P002', 'Jasprit Bumrah', '1993-12-06', 'Bowler', 14, 21, 64, 543, calculate_batting_average(543, 64), 'IND'),
('P003', 'AB de Villiers', '1984-02-17', 'Batsman', 78, 114, 228, 9876, calculate_batting_average(9876, 228), 'SA');


DELIMITER //

CREATE TRIGGER check_player_exists_before_insert
BEFORE INSERT ON player
FOR EACH ROW
BEGIN
    DECLARE player_exists INT;

    -- Check if player with the same name already exists
    SELECT COUNT(*) INTO player_exists
    FROM player
    WHERE player_name = NEW.player_name;

    -- If player exists, signal an error
    IF player_exists > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Player already exists with the same name';
    END IF;
END//

DELIMITER ;