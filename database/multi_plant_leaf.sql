-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 25, 2025 at 09:52 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `multi_plant_leaf`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `leaf_data`
--

CREATE TABLE `leaf_data` (
  `id` int(11) NOT NULL,
  `disease` varchar(50) NOT NULL,
  `symptoms` text NOT NULL,
  `solution` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `leaf_data`
--

INSERT INTO `leaf_data` (`id`, `disease`, `symptoms`, `solution`) VALUES
(1, 'Bacterial Leaf Blight', 'Dark spots with concentric rings develop on older leaves first that touch infected soil. The surrounding leaf area may turn yellow. Affected leaves may die prematurely, exposing the fruits to sunscald. It also infects stems and fruit, presenting as black leathery spots on fruit. ', 'Pinch off leaves with leaf spots and bury them in the compost pile.\r\nIt is okay to remove up to a third of the plant''s leaves if you catch the disease early.\r\nDo not remove more than a third of the plant''s leaves.\r\nKeep leaves dry to reduce spreading the disease.'),
(2, 'Sheath Blight', 'The infection appears as small, dark spots that enlarge to 1/4-inch diameter. The spot develops a tan or gray center, and the leaves eventually wilt and fall off. Older leaves are affected first. ', 'Pinch off leaves with leaf spots and bury them in the compost pile.\r\nIt is okay to remove up to a third of the plant''s leaves if you catch the disease early.\r\nDo not remove more than a third of the plant''s leaves.\r\nKeep leaves dry to reduce spreading the disease.'),
(3, 'Blast', 'Dieback of twigs; premature leaf drop; dark staining on fruit; leaves and twigs covered in dark spores.', 'Pinch off leaves with leaf spots and bury them in the compost pile.\r\nIt is okay to remove up to a third of the plant''s leaves if you catch the disease early.'),
(4, 'Brown Spot', 'A highly contagious bacterial infection, citrus canker causes yellow halo-like lesions on fruit, leaves and twigs of citrus trees. If allowed to progress unchecked, this lemon tree problem will eventually result in dieback, fruit drop, and leaf loss.', 'Do not remove more than a third of the plant''s leaves.\r\nKeep leaves dry to reduce spreading the disease.'),
(5, 'Leaf Scald', 'Leaves become white-gray and dry, Entire leaf may appear scalded by hot water.', 'Many modern rice varieties are resistant to Leaf Scald, Avoid excess standing water for long periods, Avoid excess nitrogen (urea), Use balanced NPK.'),
(6, 'Bacterial Spot', 'Small water-soaked spots, Small, raised brown scabby spots, Rough surface, cracks appear.', 'Hot water treatment: 52 degree celsius for 30 minutes to kill bacteria, Remove infected leaves, Avoid overhead irrigation, Ensure good spacing for airflow.'),
(7, 'Early Blight', 'Small brown to black spots, Yellowing around the lesions', 'Mancozeb 75% WP – 2–2.5 g per liter, Remove infected lower leaves, Avoid overhead watering, Provide good plant spacing.'),
(8, 'Late Blight', 'Water-soaked pale green or dark lesions, Rapidly enlarge into irregular brown or black patche.', 'Plant Late Blight-resistant varieties, Check with local agriculture extension office.'),
(9, 'Septoria Leaf Spot', 'Small, circular gray or tan spots with dark brown margins,\r\nEach spot may have tiny black fruiting bodies (pycnidia) visible under magnification.', 'Start with healthy, certified seeds, Choose resistant or tolerant tomato varieties, Remove lower infected leaves regularly, Maintain good plant spacing for airflow, Avoid overhead irrigation, Mulch to reduce soil splashing on leaves'),
(10, 'Mosaic Virus', 'Mottled light and dark green patches (mosaic pattern), Leaves may be distorted, curled, or puckered, Stunted growth of new leaves', 'Many mosaic viruses are transmitted by insects (aphids, thrips, whiteflies), Use insect-proof nets or controlled insecticides if necessary, Remove weeds that may host the virus, Balanced fertilizer application improves plant vigor, which helps reduce the impact.'),
(11, ' Anthracnose', 'Small water-soaked dark spots, Spots enlarge to dark brown or black lesions, Sometimes surrounded by a yellow halo', 'Store harvested fruits in dry, ventilated conditions, Avoid bruising fruits - reduces infection, Use cultivars resistant or tolerant to Anthracnose where available.'),
(12, 'Phoma blight', 'Small, dark brown to black circular spots, Spots may have tan center and dark margins, Lesions often coalesce - large necrotic areas.', 'Treat seeds with fungicides like Thiram or Carbendazim, Only plant certified healthy seeds, Remove and destroy infected plant debris, Avoid planting in the same field continuously.'),
(13, 'Red rust', 'Small orange to reddish-brown spots on the leaf surface, Spots are usually circular or irregular, In severe infection, leaves may appear reddish and dry, Usually starts on older leaves.', 'Remove infected leaves and debris, Avoid dense planting to reduce humidity, Spray at early symptom appearance.'),
(14, 'Sooty mould', 'Leaves, stems, and fruits get covered with black powdery coating, The coating looks like soot - reduces photosynthesis, Leaves may appear dull, weak, and stunted.', 'Spray leaves with water to remove black fungal coating, Improves photosynthesis and appearance, Keep plants well-spaced, Prune dense foliage for better air circulation, Remove heavily infested leaves or debris.'),
(15, 'Scab', 'Usually minor symptoms, may show small lesions in severe cases, Leaves may have chlorotic spots (rare).', 'Use certified seed tubers or disease-free seedlings, Avoid planting in fields with history of scab, Remove infected fruits, tubers, and plant debris, Avoid moving contaminated soil between fields.'),
(16, 'Cordana', 'Small, elongated brown or reddish-brown lesions, Lesions are often linear or streaked along leaf veins, Margins of lesions may have a purple or dark border.', 'Remove and destroy infected leaves and crop residues, Avoid leaving straw and stubble in the field, Maintain proper plant spacing for air circulation.'),
(17, 'Pestalotiopsis', 'Small brown to black spots, Spots often have light-colored centers with dark margins, Sometimes gray or whitish specks appear in the center.', 'Remove and destroy infected leaves, twigs, and fruits, Avoid leaving infected debris on the ground, Ensure good plant spacing for airflow, Avoid overhead irrigation if possible.'),
(18, 'Sigatoka', 'Early symptoms: Small, light brown or yellow streaks along leaf veins, Black Sigatoka: causes extensive necrosis, black streaks, and leaf death, Leaves turn yellow, then brown, and dry.', 'Remove and destroy old and infected leaves, Prune lower leaves to reduce humidity inside canopy, Proper plant spacing for good air circulation.');

-- --------------------------------------------------------

--
-- Table structure for table `medicine`
--

CREATE TABLE `medicine` (
  `id` int(11) NOT NULL,
  `leaf` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `detail` text NOT NULL,
  `leaf_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `medicine`
--

INSERT INTO `medicine` (`id`, `leaf`, `title`, `detail`, `leaf_id`) VALUES
(1, 'Paddy Leaf', 'Fever Cooling Pads', 'Fresh paddy leaves are crushed slightly and soaked in cool water. Cloth is dipped and used as a cooling compress on forehead/body. Believed to help reduce body heat and mild fever.', 1),
(2, 'Paddy Leaf', 'Skin Cooling & Rashes', 'Paddy leaf juice for Heat rashes, Minor skin irritation, Mild sunburn', 1),
(3, 'Tomato Leaf', 'Anti-inflammatory Compress', 'Fresh tomato leaves are crushed and wrapped in a clean cloth. Applied externally on Swelling, Mild muscle pain, Insect bites', 2),
(4, 'Tomato Leaf', 'Insect Bite Relief', 'Mosquito bites, Ant bites, Bee sting area (after removing stinger) Reduces itching and redness.', 2),
(5, 'Mango Leaf', 'Controls Blood Sugar (Diabetes Support)', 'Tender mango leaves are boiled - used as morning drink. Improve insulin production, Reduce blood sugar spikes, Protect blood vessels', 3),
(6, 'Mango Leaf', 'Improves Digestion', 'Mango leaf tea helps reduce: Acidity, Stomach inflammation, Gas and bloating, It has mild anti-inflammatory properties.', 3),
(7, 'Banana Leaf', 'Wound Healing & Burns (Very Common Use)', 'Banana leaf is naturally cool and sterile. It is placed over:\r\nMinor burns, Cuts, Skin irritation, Reduces pain, prevents infection, and speeds healing.', 4),
(8, 'Banana Leaf', 'Skin Cooling & Anti-inflammatory', 'Applying fresh banana leaf on the skin helps: Reduce swelling, Calm rashes, Soothe insect bites, Treat mild eczema. Its cooling nature gives instant relief.', 4);

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `email`, `mobile`, `uname`, `pass`) VALUES
(1, 'Dinesh', 'dinesh@gmail.com', 9054621096, 'dinesh', '1234'),
(2, 'Suresh', 'suresh@gmail.com', 8956212155, 'suresh', '123456');
