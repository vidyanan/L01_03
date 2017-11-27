CREATE DATABASE www;

CREATE USER 'www'@'localhost' IDENTIFIED BY 'www';

GRANT ALL PRIVILEGES ON www.* TO 'www'@'localhost';

USE www;

CREATE TABLE django_content_type (id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100) NOT NULL, app_label VARCHAR(100) NOT NULL, model varchar(100) NOT NULL);

Create table  django_session (session_key VARCHAR(40) NOT NULL PRIMARY KEY, session_data text NOT NULL, expire_date datetime NOT NULL);

create table user (ID int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT, name varchar(32), password varchar(32), email varchar(255), last_login datetime, enabled enum('yes', 'no') DEFAULT 'no', deleted enum('yes', 'no') default 'no', notes text, role varchar(100));

create table questions (id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(511), type VARCHAR(511) NOT NULL, question VARCHAR(511) NOT NULL, answer VARCHAR(511) NOT NULL, assignment int(11));

create table assignments (id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(511) NOT NULL, `start-date` VARCHAR(20), `end-date` VARCHAR(20));

create table answers (id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, user int(11) NOT NULL, assignment int(11) NOT NULL, question int(11) NOT NULL, answer VARCHAR(255));

CREATE TABLE grades (id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, user INT(11) NOT NULL, assignment INT(11) NOT NULL, grade FLOAT(5,2) DEFAULT 0.0);

INSERT INTO user (name, email, password, enabled, role) VALUES ('admin', 'admin', md5('admin'), 'yes', 'ta');

INSERT INTO user (name, email, password, enabled, role) VALUES ('student', 'student', md5('student'), 'yes', 'student');

