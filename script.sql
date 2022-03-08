SHOW databases;
CREATE DATABASE pte;
USE pte;
DROP TABLE scores;
CREATE TABLE scores 
					(
						userid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255),
                        useremail VARCHAR(255),
                        userpassword VARCHAR(255),
                        speaking VARCHAR(255),
                        listening VARCHAR(255),
                        writing VARCHAR(255),
                        reading VARCHAR(255)
                        );
                        
SELECT * FROM scores;

SELECT * FROM scores WHERE useremail = "broc@gmail.com"
                    