-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: 2020-11-03 14:04:30
-- 服务器版本： 5.7.21
-- PHP Version: 5.6.35

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `card`
--

-- --------------------------------------------------------

--
-- 表的结构 `datas`
--

DROP TABLE IF EXISTS `datas`;
CREATE TABLE IF NOT EXISTS `datas` (
  `id` int(11) NOT NULL,
  `key1` int(11) NOT NULL,
  `key2` int(11) NOT NULL,
  `key3` binary(11) NOT NULL,
  `key4` binary(11) NOT NULL,
  `key5` int(11) NOT NULL,
  `key6` int(11) NOT NULL,
  `key7` binary(11) NOT NULL,
  `key8` binary(11) NOT NULL,
  `key9` binary(11) NOT NULL,
  `key10` binary(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `texts`
--

DROP TABLE IF EXISTS `texts`;
CREATE TABLE IF NOT EXISTS `texts` (
  `isbuy` int(11) DEFAULT '0',
  `id` int(11) PRIMARY KEY,
  `name` varchar(110) NOT NULL,
  `content` varchar(10000) NOT NULL,
  `key1` varchar(110) DEFAULT NULL,
  `key2` varchar(110) DEFAULT NULL,
  `key3` varchar(110) DEFAULT NULL,
  `key4` varchar(110) DEFAULT NULL,
  `key5` varchar(110) DEFAULT NULL,
  `key6` varchar(110) DEFAULT NULL,
  `key7` varchar(110) DEFAULT NULL,
  `key8` varchar(110) DEFAULT NULL,
  `key9` varchar(110) DEFAULT NULL,
  `key10` varchar(110) DEFAULT NULL,
  `key11` varchar(110) DEFAULT NULL,
  `key12` varchar(110) DEFAULT NULL,
  `key13` varchar(110) DEFAULT NULL,
  `key14` varchar(110) DEFAULT NULL,
  `key15` varchar(110) DEFAULT NULL,
  `key16` varchar(110) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
