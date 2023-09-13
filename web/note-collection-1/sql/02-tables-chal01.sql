
CREATE TABLE IF NOT EXISTS chal01.users (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    `name` VARCHAR(255) NOT NULL, 
    `password` VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_name (`name`)
    );

CREATE TABLE IF NOT EXISTS chal01.notes (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    `title` TEXT NOT NULL, 
    `content` TEXT NOT NULL,
    `owner` INT NOT NULL,
    `is_public` INT(1) NOT NULL DEFAULT 0,
    `is_blocked` INT(1) NOT NULL DEFAULT 0,
    `reported` DATETIME DEFAULT NULL,
    FOREIGN KEY (`owner`) REFERENCES chal01.users(`id`)
    );