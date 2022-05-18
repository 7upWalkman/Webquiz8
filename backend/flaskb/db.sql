DELIMITER //

-- CREATE USER 'admin'@'localhost' IDENTIFIED BY 'abc'
-- //
-- CREATE USER 'admin'@'%' IDENTIFIED BY 'abc'
-- //
-- GRANT ALL PRIVILEGES on WebQuiz.* TO 'admin'@'localhost' 
-- //
-- GRANT ALL PRIVILEGES on WebQuiz.* TO 'admin'@'%' 
-- //

DROP DATABASE IF EXISTS WebQuiz
//
CREATE DATABASE WebQuiz
//
USE WebQuiz
//

DROP TABLE IF EXISTS `User`
//
CREATE TABLE `User` (
    id                  INTEGER PRIMARY KEY AUTO_INCREMENT
    , username            VARCHAR(150) NOT NULL UNIQUE COMMENT 'Username for login'
    , `password`          BINARY(32) NOT NULL COMMENT  'Hashed password SHA256 (TODO: add salt)'
    , first_name          VARCHAR(50) NOT NULL COMMENT 'First (personal) name'
    , middle_names        VARCHAR(250) NOT NULL COMMENT 'Middle names'
    , last_name           VARCHAR(250) NOT NULL COMMENT 'Last name (surname)'
    , email_addr          VARCHAR(255) NOT NULL UNIQUE DEFAULT 'Lisboa'
    , birth_date          DATE
    , account_datetime    DATETIME NOT NULL DEFAULT (NOW()) COMMENT 'Date/time of creation'

    , CONSTRAINT Email_chk CHECK(email_addr REGEXP "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
)
//

DROP TRIGGER IF EXISTS ValidateClient
//
CREATE TRIGGER ValidateClient BEFORE INSERT ON `User`
FOR EACH ROW
BEGIN
    DECLARE INVALID_DATA CONDITION FOR SQLSTATE '45000';

    -- We have to this, and not with CHECK CONSTRAINT because
    -- by that time, the password is already hashed (see below)
    -- The password can only be hashed here, in this trigger.

    IF NOT NEW.`password` REGEXP "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!$#?%]).{6,}" THEN
        SIGNAL INVALID_DATA 
        SET MESSAGE_TEXT = 'Invalid User data';
    END IF;

    -- We're doing this here for simplicity, but we shouldn't. 
    -- SHA2 is too fast for password hashing purposes. 
    -- Also, we should salt the password

    SET NEW.`password` = UNHEX(SHA2(NEW.`password`, 256));
    SET NEW.account_datetime = NOW();
END 
//


DROP TRIGGER IF EXISTS NotifyClientCreation
//
CREATE TRIGGER NotifyClientCreation AFTER INSERT ON `User`
FOR EACH ROW
BEGIN
    INSERT INTO Notification 
        (`event`, event_desc)
    VALUES 
        ("NEW_USER", CONCAT(NEW.id, ", ", NEW.first_name, " ", NEW.last_name))
    ;
END
//

DROP TABLE IF EXISTS `Notification`
//
CREATE TABLE `Notification` (
    id              INTEGER PRIMARY KEY AUTO_INCREMENT,
    `event`            VARCHAR(500) NOT NULL COMMENT 'Event to report',
    event_desc         VARCHAR(500) NOT NULL COMMENT 'Event to report',
    date_time        DATETIME NOT NULL DEFAULT (NOW())
)
//

DROP PROCEDURE IF EXISTS AuthenticateUser
//
CREATE PROCEDURE AuthenticateUser (
        IN user_name VARCHAR(100)
        , IN user_password VARCHAR(100)
)
BEGIN
    SELECT  id, username, first_name, last_name, email_addr
    FROM    `User`
    WHERE   username = user_name AND `password` = UNHEX(SHA2(user_password, 256));
END
//

DROP PROCEDURE IF EXISTS GetUserInfo
//
CREATE PROCEDURE GetUserInfo (IN user_id INTEGER)
BEGIN
    SELECT  id, username, first_name, last_name, email_addr
    FROM    `User`
    WHERE   id = user_id;
END
//

    -- , username            VARCHAR(150) NOT NULL UNIQUE COMMENT 'Username for login'
    -- , `password`          BINARY(32) NOT NULL COMMENT  'Hashed password SHA256 (TODO: add salt)'
    -- , first_name          VARCHAR(50) NOT NULL COMMENT 'First (personal) name'
    -- , middle_names        VARCHAR(250) NOT NULL COMMENT 'Middle names'
    -- , last_name           VARCHAR(250) NOT NULL COMMENT 'Last name (surname)'
    -- , email_addr          VARCHAR(255) NOT NULL UNIQUE DEFAULT 'Lisboa'
    -- , birth_date          DATE NOT NULL
    -- , account_datetime    DATETIME NOT NULL DEFAULT (NOW()) COMMENT 'Date/time of creation'

DROP PROCEDURE IF EXISTS CreateUser
//
CREATE PROCEDURE CreateUser (
    IN username     VARCHAR(150)
    , IN `password`   VARCHAR(100)
    , IN first_name   VARCHAR(50)
    , IN first_name   VARCHAR(250)
    , IN last_name    VARCHAR(250)
    , IN email_addr   VARCHAR(250)
    , IN birth_date   DATE
)
BEGIN
    --- ACABAR DEF. DO SP
END
//

INSERT INTO `User`
    (username, `password`, first_name, middle_names, last_name, email_addr, birth_date)
VALUES 
    ('alb', 'Abc!123', 'Alberto', '', 'Antunes', 'alb@mail.com', '2001-05-05'),
    ('arm', 'Abc!123', 'Armando', '', 'Almeida', 'arm@mail.com', '1999-12-14'),
    ('arn', 'Abc!123', 'Arnaldo', '', 'Avelar', 'arn@mail.com', '2001-08-23')
//

/* JUST FOR TESTING PURPOSES */ 
UPDATE `User` 
    SET `password` = UNHEX(SHA2('abc', 256))
WHERE username = 'alb'
//

-- INSERT INTO `User`
--     (username, `password`, first_name, middle_names, last_name, email_addr, birth_date)
-- VALUES 
--     ('bademail1', 'Abc!123', 'Bad', '', 'Email1', 'email_com', '1997-10-12'),
--     ('bademail2', 'Abc!123', 'Bad', '', 'Email2', 'email@c', '1997-10-12'),
--     ('bademail3', 'Abc!123', 'Bad', '', 'Email2', '', '1997-10-12')
-- //

-- INSERT INTO `User`
--     (username, `password`, first_name, middle_names, last_name, email_addr, birth_date)
-- VALUES 
--     ('badpwd1', 'Abc!123', 'Bad', '', 'Password1', 'bad1@pwd.com', '1997-10-12'),
--     ('badpwd2', 'Abc!Um$', 'Bad', '', 'Password2', 'bad2@pwd.com', '1997-10-12'),
--     ('badpwd3', 'abc!123$', 'Bad', '', 'Password3', 'bad3@pwd.com', '1997-10-12'),
--     ('badpwd4', 'a1%A', 'Bad', '', 'Password4', 'bad4@pwd.com', '1997-10-12')
-- //

-- CALL GetUserInfo(4)
-- //

-- SELECT * FROM `User`
-- //

-- DELETE FROM `User`
-- //

-- DELIMITER //
-- USE WebQuiz
-- //
