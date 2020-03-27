-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`costo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`costo` (
  `idCosto` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `precio` DECIMAL(10,2) NULL DEFAULT NULL,
  `esFijo` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idCosto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`simulation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`simulation` (
  `idSimulation` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idSimulation`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 30
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`stage`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`stage` (
  `idStage` INT NOT NULL AUTO_INCREMENT,
  `media` DECIMAL(10,2) NULL DEFAULT NULL,
  `probability` DECIMAL(10,2) NULL DEFAULT NULL,
  `persons` INT NULL DEFAULT NULL,
  `costHour` DECIMAL(10,2) NULL DEFAULT NULL,
  `utilityHour` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idStage`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`detail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`detail` (
  `idDetail` INT NOT NULL,
  `hour` INT NULL DEFAULT NULL,
  `personNumber` INT NULL DEFAULT NULL,
  `idSimulation` INT NOT NULL AUTO_INCREMENT,
  `costo` DECIMAL(10,2) NULL DEFAULT NULL,
  `productos` VARCHAR(105) NULL DEFAULT NULL,
  `idStage` INT NOT NULL,
  PRIMARY KEY (`idDetail`),
  INDEX `fk_detail_simulation1_idx` (`idSimulation` ASC) VISIBLE,
  INDEX `fk_detail_stage_idx` (`idStage` ASC) VISIBLE,
  CONSTRAINT `fk_detail_simulation1`
    FOREIGN KEY (`idSimulation`)
    REFERENCES `mydb`.`simulation` (`idSimulation`),
  CONSTRAINT `fk_detail_stage`
    FOREIGN KEY (`idStage`)
    REFERENCES `mydb`.`stage` (`idStage`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`producto` (
  `idProducto` INT NOT NULL AUTO_INCREMENT,
  `nomProducto` VARCHAR(45) NULL DEFAULT NULL,
  `precio` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idProducto`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8
COMMENT = '		';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
