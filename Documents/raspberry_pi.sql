-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 26, 2018 at 09:13 AM
-- Server version: 10.1.23-MariaDB-9+deb9u1
-- PHP Version: 7.0.30-0+deb9u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `raspberry_pi`
--

-- --------------------------------------------------------

--
-- Table structure for table `sense_hat_data`
--

CREATE TABLE `sense_hat_data` (
  `ID` int(11) NOT NULL,
  `temp_humidity` float NOT NULL,
  `temp_pressure` float NOT NULL,
  `pressure` float NOT NULL,
  `humidity` float NOT NULL,
  `pitch` float NOT NULL,
  `roll` float NOT NULL,
  `yaw` float NOT NULL,
  `compass_x` float NOT NULL,
  `compass_y` float NOT NULL,
  `compass_z` float NOT NULL,
  `acc_x` float NOT NULL,
  `acc_y` float NOT NULL,
  `acc_z` float NOT NULL,
  `gyro_x` float NOT NULL,
  `gyro_y` float NOT NULL,
  `gyro_z` float NOT NULL,
  `capture_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `capture_timestamp` bigint(20) NOT NULL,
  `comment` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_data`
--

CREATE TABLE `vehicle_data` (
  `VehicleID` varchar(10) NOT NULL,
  `FuelLevel` float NOT NULL,
  `ChangedOn` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sense_hat_data`
--
ALTER TABLE `sense_hat_data`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `vehicle_data`
--
ALTER TABLE `vehicle_data`
  ADD PRIMARY KEY (`VehicleID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sense_hat_data`
--
ALTER TABLE `sense_hat_data`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
