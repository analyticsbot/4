-- phpMyAdmin SQL Dump
-- version 4.4.13.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 27, 2016 at 06:59 PM
-- Server version: 5.6.27-0ubuntu1
-- PHP Version: 5.6.11-1ubuntu3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce_url`
--

-- --------------------------------------------------------

--
-- Table structure for table `table_n`
--

CREATE TABLE IF NOT EXISTS `table_n` (
  `Pid` varchar(50) DEFAULT NULL,
  `URL_raw` varchar(255) NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Brand` varchar(255) NOT NULL,
  `IMG_medium` varchar(255) NOT NULL,
  `IMG_large` varchar(255) NOT NULL,
  `Price_mrp` varchar(9) NOT NULL,
  `Price_selling` varchar(9) NOT NULL,
  `Price_shipping` varchar(9) NOT NULL,
  `Delivery` varchar(50) NOT NULL,
  `COD` varchar(5) NOT NULL,
  `EMI` varchar(5) NOT NULL,
  `Category_path` text NOT NULL,
  `Description` text NOT NULL,
  `Offers` text NOT NULL,
  `Average_rating` varchar(10) NOT NULL,
  `Reviews` longtext NOT NULL,
  `Status` varchar(50) NOT NULL,
  `Condition` varchar(50) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Shop` varchar(50) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `table_n`
--
ALTER TABLE `table_n`
  ADD PRIMARY KEY (`id`),
  ADD KEY `PID` (`Pid`,`URL_raw`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `table_n`
--
ALTER TABLE `table_n`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
