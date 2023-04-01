-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 01, 2023 at 08:22 AM
-- Server version: 8.0.32-0ubuntu0.22.04.2
-- PHP Version: 8.1.2-1ubuntu2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `205CDE`
--

-- --------------------------------------------------------

--
-- Table structure for table `design`
--

CREATE TABLE `design` (
  `productNo` varchar(4) NOT NULL,
  `author` varchar(20) NOT NULL,
  `photoName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `design`
--

INSERT INTO `design` (`productNo`, `author`, `photoName`) VALUES
('p1', 'Staff1', 'cake1.jpg'),
('p2', 'internet', 'chocolate.jpg'),
('p3', 'internet', 'chp.jpg'),
('p4', 'internet', 'star-angle.jpg'),
('P7', 'Special Cake ', ' none'),
('P8', 'Special Cake ', ' none');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `orderNo` int NOT NULL,
  `WayToPay` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Date` date NOT NULL,
  `payment` int NOT NULL,
  `productNo` varchar(4) NOT NULL,
  `userNo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`orderNo`, `WayToPay`, `Date`, `payment`, `productNo`, `userNo`) VALUES
(1, 'other', '2023-04-04', 260, 'p1', 100000001),
(2, 'credit card', '2023-04-04', 260, 'p1', 100000001),
(4, 'credit card', '2023-04-05', 260, 'p2', 100000001),
(7, 'other', '2023-04-07', 260, 'p1', 100000003),
(8, 'credit card', '2023-03-31', 260, 'p2', 100000003),
(9, 'credit card', '2023-04-05', 310, 'P7', 100000004),
(10, 'other', '2023-04-13', 260, 'p4', 100000004);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `productNo` varchar(4) NOT NULL,
  `size` int NOT NULL,
  `type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `taste` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `decorate` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `theme` varchar(30) NOT NULL,
  `chocolate word` varchar(30) NOT NULL,
  `price` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`productNo`, `size`, `type`, `taste`, `decorate`, `theme`, `chocolate word`, `price`) VALUES
('p1', 8, 'Mousse cake', 'mango', 'mango', 'none', 'none', 260),
('p2', 8, 'Butter cake', 'chocolate', 'chocolate', 'none', 'none', 260),
('p3', 8, 'Pound cake', 'chocolate', 'none', 'none', 'none', 250),
('p4', 8, 'Angel cake', 'starberry', 'starberry', 'none', 'none', 260),
('P5', 6, 'Butter cake', 'chocolate', ' mango', 'none', '', 240),
('P6', 6, 'Sponge cake', 'mango', ' mango', 'none', '', 240),
('P7', 10, 'Mousse cake', 'chocolate', ' mango orange lenmo strawberry', 'birthday', '', 310),
('P8', 12, 'Butter cake', 'lenmo', ' orange lenmo', 'Birthday', '', 310);

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `try` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `UserInformation`
--

CREATE TABLE `UserInformation` (
  `userNo` int NOT NULL,
  `username` varchar(20) NOT NULL,
  `TelNo` int NOT NULL,
  `email` varchar(30) NOT NULL,
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `UserInformation`
--

INSERT INTO `UserInformation` (`userNo`, `username`, `TelNo`, `email`, `address`) VALUES
(100000001, 'Jack', 50000468, 'iamjoker@jack.com', 'Ming Wah Dai Ha Block B 3/F flat 5'),
(100000002, 'qwerty', 12345678, 'qwertyui@qwert', 'wert'),
(100000003, 'test', 12358746, 'wertyuiop@qwery', 'qw345yuiokjhgfdsa'),
(100000004, 'Mary', 95555444, 'Mary954@gmail.com', 'Hong Kong ming hau block B 4/F flat 4023');

-- --------------------------------------------------------

--
-- Table structure for table `userlogin`
--

CREATE TABLE `userlogin` (
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `userlogin`
--

INSERT INTO `userlogin` (`username`, `password`) VALUES
('Jack', 'joker'),
('Mary', '888888'),
('admin', 'asd'),
('qwerty', '1234'),
('test', '123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `design`
--
ALTER TABLE `design`
  ADD PRIMARY KEY (`productNo`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`orderNo`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`productNo`);

--
-- Indexes for table `UserInformation`
--
ALTER TABLE `UserInformation`
  ADD PRIMARY KEY (`userNo`);

--
-- Indexes for table `userlogin`
--
ALTER TABLE `userlogin`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
