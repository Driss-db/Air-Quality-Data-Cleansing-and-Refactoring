-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema pollution_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pollution_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pollution_db` DEFAULT CHARACTER SET utf8 ;
USE `pollution_db` ;

-- -----------------------------------------------------
-- Table `pollution_db`.`stations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution_db`.`stations` (
  `idstations` INT NOT NULL,
  `location` VARCHAR(48) NULL DEFAULT NULL,
  `geo_point_2d` VARCHAR(32) NULL DEFAULT NULL,
  PRIMARY KEY (`idstations`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `pollution_db`.`readings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution_db`.`readings` (
  `idreadings` INT NOT NULL AUTO_INCREMENT,
  `datetime` DATETIME NULL DEFAULT NULL,
  `nox` FLOAT NULL DEFAULT NULL,
  `no2` FLOAT NULL DEFAULT NULL,
  `no` FLOAT NULL DEFAULT NULL,
  `pm10` FLOAT NULL DEFAULT NULL,
  `nvpm10` FLOAT NULL DEFAULT NULL,
  `vpm10` FLOAT NULL DEFAULT NULL,
  `nvpm2.5` FLOAT NULL DEFAULT NULL,
  `pm2.5` FLOAT NULL DEFAULT NULL,
  `vpm2.5` FLOAT NULL DEFAULT NULL,
  `co` FLOAT NULL DEFAULT NULL,
  `o3` FLOAT NULL DEFAULT NULL,
  `so2` FLOAT NULL DEFAULT NULL,
  `temperature` DOUBLE NULL DEFAULT NULL,
  `rh` INT NULL DEFAULT NULL,
  `airpressure` INT NULL DEFAULT NULL,
  `datestart` DATETIME NULL DEFAULT NULL,
  `dateend` DATETIME NULL DEFAULT NULL,
  `current` TEXT NULL DEFAULT NULL,
  `instrumenttype` VARCHAR(32) NULL DEFAULT NULL,
  `stationid` INT NOT NULL,
  PRIMARY KEY (`idreadings`),
  INDEX `stationid_idx` (`stationid` ASC) VISIBLE,
  CONSTRAINT `stationid`
    FOREIGN KEY (`stationid`)
    REFERENCES `pollution_db`.`stations` (`idstations`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `pollution_db`.`schema`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution_db`.`schema` (
  `measure` VARCHAR(32) NOT NULL,
  `description` LONGTEXT NULL DEFAULT NULL,
  `unit` VARCHAR(24) NULL DEFAULT NULL,
  PRIMARY KEY (`measure`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
