USE `test`;
DROP procedure IF EXISTS `GetRSE`;

DELIMITER $$
USE `test`$$
CREATE PROCEDURE `test`.`GetRSE`()
BEGIN
    SELECT * FROM `rucio`.`rses`;
END$$

DELIMITER $$

