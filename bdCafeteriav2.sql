-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema bdcafeteria
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bdcafeteria
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bdcafeteria` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci ;
USE `bdcafeteria` ;

-- -----------------------------------------------------
-- Table `bdcafeteria`.`costo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdcafeteria`.`costo` (
  `idCosto` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(250) NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `esFijo` INT(1) NOT NULL,
  PRIMARY KEY (`idCosto`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_spanish2_ci;


-- -----------------------------------------------------
-- Table `bdcafeteria`.`producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdcafeteria`.`producto` (
  `idProducto` INT(11) NOT NULL AUTO_INCREMENT,
  `nomProducto` VARCHAR(40) NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idProducto`))
ENGINE = InnoDB
AUTO_INCREMENT = 69
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_spanish2_ci;


-- -----------------------------------------------------
-- Table `bdcafeteria`.`simulation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdcafeteria`.`simulation` (
  `idSimulation` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`idSimulation`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdcafeteria`.`stage`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdcafeteria`.`stage` (
  `idStage` INT NOT NULL,
  `media` DECIMAL(10,2) NULL,
  `probability` DECIMAL(10,2) NULL,
  `persons` INT NULL,
  `costHour` DECIMAL(10,2) NULL,
  `utilityHour` DECIMAL(10,2) NULL,
  `idSimulation` INT NOT NULL,
  PRIMARY KEY (`idStage`),
  INDEX `fk_stage_simulation1_idx` (`idSimulation` ASC) VISIBLE,
  CONSTRAINT `fk_stage_simulation1`
    FOREIGN KEY (`idSimulation`)
    REFERENCES `bdcafeteria`.`simulation` (`idSimulation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bdcafeteria`.`detail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bdcafeteria`.`detail` (
  `idDetail` INT NOT NULL,
  `hour` INT NULL,
  `personNumber` INT NULL,
  `idProducto` INT NOT NULL,
  `idSimulation` INT NOT NULL,
  PRIMARY KEY (`idDetail`),
  INDEX `fk_detail_producto_idx` (`idProducto` ASC) VISIBLE,
  INDEX `fk_detail_simulation1_idx` (`idSimulation` ASC) VISIBLE,
  CONSTRAINT `fk_detail_producto`
    FOREIGN KEY (`idProducto`)
    REFERENCES `bdcafeteria`.`producto` (`idProducto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detail_simulation1`
    FOREIGN KEY (`idSimulation`)
    REFERENCES `bdcafeteria`.`simulation` (`idSimulation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
