-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 05, 2018 at 05:20 AM
-- Server version: 10.2.12-MariaDB
-- PHP Version: 5.6.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `server_id` bigint(255) DEFAULT NULL,
  `discord_name` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `discord_id` bigint(255) DEFAULT NULL,
  `join_date` timestamp NULL DEFAULT NULL,
  `verified` tinyint(4) DEFAULT NULL,
  `in_server` tinyint(4) DEFAULT NULL,
  `real_name` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `reason_join` text COLLATE utf8_bin DEFAULT NULL,
  `in_group` varchar(5) COLLATE utf8_bin DEFAULT NULL,
  `ip_addr` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `warns` int(11) DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `servers`
--

CREATE TABLE `servers` (
  `server_id` bigint(255) DEFAULT NULL,
  `server_name` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `added_on` timestamp NULL DEFAULT NULL,
  `welcome_channel` bigint(255) DEFAULT NULL,
  `goodbye_channel` bigint(255) DEFAULT NULL,
  `event_channel` bigint(255) DEFAULT NULL,
  `log_channel` bigint(255) DEFAULT NULL,
  `log_msgchanges` tinyint(4) NOT NULL DEFAULT 0,
  `log_whitelist` mediumtext COLLATE utf8_bin DEFAULT NULL,
  `entry_form` tinyint(4) DEFAULT 0,
  `entry_text` text COLLATE utf8_bin DEFAULT NULL,
  `entry_text_pm` mediumtext COLLATE utf8_bin DEFAULT NULL,
  `goodbye_text` text COLLATE utf8_bin DEFAULT NULL,
  `max_warns` int(255) DEFAULT 3
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `setting_sessions`
--

CREATE TABLE `setting_sessions` (
  `ID` bigint(255) DEFAULT NULL,
  `token` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `server_id` bigint(255) DEFAULT NULL,
  `admin_id` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `admin_name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `valid` tinyint(4) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `warnings`
--

CREATE TABLE `warnings` (
  `discord_name` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `discord_id` bigint(255) DEFAULT NULL,
  `server_id` bigint(255) DEFAULT NULL,
  `warn_datetime` timestamp NULL DEFAULT NULL,
  `admin` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `reason` text COLLATE utf8_bin DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
