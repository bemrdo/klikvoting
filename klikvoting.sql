-- -------------------------------------------------------------
-- TablePlus 4.0.2(374)
--
-- https://tableplus.com/
--
-- Database: klikvoting
-- Generation Time: 2021-08-14 15:34:29.8230
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE TABLE `c_EwMdQmrR` (
  `id_candidate` varchar(40) NOT NULL,
  `id_voting` varchar(40) NOT NULL,
  `username` varchar(40) NOT NULL,
  `pass` varchar(40) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` longtext,
  `avatar` varchar(40) DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  `validator` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_candidate`),
  KEY `id_voting` (`id_voting`),
  CONSTRAINT `c_ewmdqmrr_ibfk_1` FOREIGN KEY (`id_voting`) REFERENCES `voting` (`id_voting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `h_EwMdQmrR` (
  `id_hash` varchar(40) NOT NULL,
  `id_voting` varchar(40) NOT NULL,
  `id_candidate` varchar(40) NOT NULL,
  `role` varchar(40) NOT NULL,
  `encrypted` varchar(255) NOT NULL,
  `status` varchar(40) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_hash`),
  KEY `id_voting` (`id_voting`),
  KEY `id_candidate` (`id_candidate`),
  CONSTRAINT `h_ewmdqmrr_ibfk_1` FOREIGN KEY (`id_voting`) REFERENCES `voting` (`id_voting`),
  CONSTRAINT `h_ewmdqmrr_ibfk_2` FOREIGN KEY (`id_candidate`) REFERENCES `c_EwMdQmrR` (`id_candidate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `problem` (
  `id_problem` varchar(40) NOT NULL,
  `id_user` varchar(40) NOT NULL,
  `id_voting` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `msg_from` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `msg_to` varchar(40) NOT NULL,
  `message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `respond` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `msg_created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `rsp_created` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_problem`),
  KEY `id_voting` (`id_voting`),
  CONSTRAINT `problem_ibfk_1` FOREIGN KEY (`id_voting`) REFERENCES `voting` (`id_voting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `user` (
  `id_user` varchar(40) NOT NULL DEFAULT '',
  `name` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  `number` varchar(40) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `institution` varchar(40) NOT NULL,
  `address` varchar(255) NOT NULL,
  `card_id` varchar(40) NOT NULL,
  `role` varchar(11) NOT NULL DEFAULT 'organizer',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'pending',
  `message` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '[Akun Baru]',
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `v_EwMdQmrR` (
  `id_voter` varchar(40) NOT NULL,
  `id_voting` varchar(40) NOT NULL,
  `username` varchar(40) NOT NULL,
  `pass` varchar(40) NOT NULL,
  `name` varchar(40) NOT NULL,
  `description` longtext,
  `avatar` varchar(40) DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  `validator` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_voter`),
  KEY `id_voting` (`id_voting`),
  CONSTRAINT `v_ewmdqmrr_ibfk_1` FOREIGN KEY (`id_voting`) REFERENCES `voting` (`id_voting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `voting` (
  `id_voting` varchar(40) NOT NULL,
  `id_user` varchar(40) NOT NULL,
  `name` varchar(255) NOT NULL,
  `voting_desc` longtext NOT NULL,
  `date_start` datetime NOT NULL,
  `date_end` datetime NOT NULL,
  `candidate` varchar(40) NOT NULL,
  `voter` varchar(40) NOT NULL,
  `viewer` varchar(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_checked` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_voting`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `voting_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `c_EwMdQmrR` (`id_candidate`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('G9mGwLDK', 'EwMdQmrR', 'C-3I4X9B8Q', 'oqqx4b5oK8So', 'Komang Bhargo Bhaskara & I Ketut Agus Sugiartha', '<p class=\"ql-align-center\"><strong class=\"ql-size-large\">VISI</strong></p><p class=\"ql-align-center\">Terwujudnya Badan Eksekutif Mahasiswa ITB STIKOM Bali sebagai wadah pelayanan yang interaktif bagi mahasiswa umum dan ORMAWA guna bersinergi dalam menciptakan inovasi</p><p><br></p><p class=\"ql-align-center\"><strong class=\"ql-size-large\">MISI</strong></p><ol><li>Menjalankan fungsi ORMAWA ITB STIKOM Bali berdasarkan Tri Dharma Perguruan Tinggi</li><li>Memetakan dan mengembangkan potensi mahasiswa ITB STIKOM Bali, serta memperkuat jaringan internal maupun eksternal</li><li>Membangun ruang kolaborasi dan gagasan antar ORMAWA guna menumbuhkan dan memperkuat rasa saling percaya satu sama lain</li><li>Membangun sikap profesionalisme di dalam organisasi guna meningkatkan produktivitas dalam semangat solidaritas</li></ol>', 'G9mGwLDK_2021-08-08_175526.523318', 'blocked', NULL, '2021-08-08 17:55:27'),
('lDz7CGxF', 'EwMdQmrR', 'C-8LgTLc7e', 'QWw9V82OlHYy', 'I Made Yudi Setiawan & I.B. Agung Indra Putra Pidada', '<p class=\"ql-align-center\"><strong class=\"ql-size-large\">VISI</strong></p><p class=\"ql-align-center\">BEM ITB STIKOM Bali menjadi penyambung aspirasi dan inspirasi mahasiswa dan juga meningkatkan kualitas maupun elektabilitas dengan harapan BEM ITB STIKOM Bali mampu bersaing dengan kampus PTN/PTS di ranah Kota, Provinsi maupun Nasional</p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-center\"><strong class=\"ql-size-large\">Misi</strong></p><ol><li>Meningkatkan Kinerja dan Kualitas BEM dengan metode kolektif kolegial (gotong royong)</li><li>Menjalin hubungan yang harmonis dengan cara merangkul dan melayani ORMAWA yang ada di kampus ITB STIKOM Bali</li><li>Meningkatkan kualitas mahasiswa dan mahasiswi dengan memajukan dan memakmurkan ORMAWA yang ada di ITB STIKOM Bali</li><li>Menampung aspirasi dan memecahkan masalah mahasiswa dengan prinsip dialog intelektual dan prinsip kekeluargaan</li><li>Mampu menyelenggarakan dan merealisasikan kegiatan di dalam kampus maupun di luar kampus</li></ol>', 'lDz7CGxF_2021-08-13_091223.158439', 'blocked', NULL, '2021-08-13 09:12:23');

INSERT INTO `h_EwMdQmrR` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('3SdALMxl', 'EwMdQmrR', 'G9mGwLDK', 'voter', 'FRJWEWd7gRFS1jawfvNhjb3h3O+9so5qCtzGua0C/68=', 'checked', '2021-08-09 09:01:29'),
('ncbgyTx4', 'EwMdQmrR', 'G9mGwLDK', 'voter', 'dXNX2AqlGiQK9UKD4gHimNPYCse9CxEoaVi0RJk6ejw=', 'checked', '2021-08-08 18:55:56');

INSERT INTO `problem` (`id_problem`, `id_user`, `id_voting`, `msg_from`, `msg_to`, `message`, `respond`, `msg_created`, `rsp_created`) VALUES
('4FG1yqvD', 'f5wBDkVo', 'EwMdQmrR', 'Voter', 'Organizer', 'Bertanya dulu?', 'baik saya tanggapi', '2021-08-09 09:04:30', '2021-08-09 09:05:21'),
('iDv9WIwg', '5oSEXhdI', 'EwMdQmrR', 'Voter', 'Organizer', 'Bagaimana cara memilih Candidate?', 'Perubahan tanggapan baru', '2021-08-08 18:48:20', '2021-08-09 09:04:07'),
('sAwyOjDN', '8lZk8BRC', 'EwMdQmrR', 'Organizer', 'Admin', 'Bagaimana cara menambah Candidate?', 'Gunakan tombol Tambah Candidate', '2021-08-08 17:51:35', '2021-08-08 17:52:12');

INSERT INTO `user` (`id_user`, `name`, `email`, `number`, `pass`, `institution`, `address`, `card_id`, `role`, `created_at`, `status`, `message`) VALUES
('8lZk8BRC', 'Panitia Pemilu BEM', 'panitiabem@mail.com', '08123456789', 'pbkdf2:sha256:260000$UBkjVleszpGIWkWX$f4b98607eba2e3ab931bb2e1fcbd7b2711c9cb9dd2de89d8975220741dad3632', 'ITB STIKOM Bali', 'Jl. Raya Puputan No.86, Dangin Puri Klod, Kec. Denpasar Tim., Kota Denpasar, Bali 80234', '8lZk8BRC_2021-08-08_170807.925488', 'organizer', '2021-08-08 17:08:08', 'approved', '[Perubahan Profil]'),
('9IP9swEO', 'Admin', 'admin@mail.com', '08123456789', 'pbkdf2:sha256:260000$2k3ag2qMfshNyeOo$b221cf77e7e03aa937b1d2107da82252ada0342ae3f1570e379045b14cb8b80c', 'klikvoting', 'di rumah', '9IP9swEO_2021-07-18_225103.227726', 'admin', '2021-07-18 22:51:03', 'approved', '[Akun Admin]');

INSERT INTO `v_EwMdQmrR` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('5oSEXhdI', 'EwMdQmrR', 'V-qIIcfAKU', 'wIdmjTYsROw1', 'Mahasiswa 1', 'NIM : 170010001', NULL, 'ncbgyTx4', 'dJWyaFNa4h32RzpLbKoS9Q==', '2021-08-08 17:57:49'),
('CwauGCy5', 'EwMdQmrR', 'V-iXnLGF5Y', 'EKoFXqoUf4jM', 'Mahasiswa 3', 'NIM : 170030020', NULL, NULL, NULL, '2021-08-13 09:13:21'),
('f5wBDkVo', 'EwMdQmrR', 'V-vI8MYZXU', 'vr0bsaOf4deg', 'Mahasiswa 2', 'NIM : 170010002', NULL, '3SdALMxl', '6u5c7AUujBUbNGQ0z2xRbA==', '2021-08-09 08:56:24'),
('yx3JjAN3', 'EwMdQmrR', 'V-VzMqWlFR', 'mdfsqBlgOVuc', 'Mahasiswa 4', 'NIM : 180030303', NULL, NULL, NULL, '2021-08-13 09:13:57');

INSERT INTO `voting` (`id_voting`, `id_user`, `name`, `voting_desc`, `date_start`, `date_end`, `candidate`, `voter`, `viewer`, `created_at`, `last_checked`) VALUES
('EwMdQmrR', '8lZk8BRC', 'Pemilu Badan Eksekutif Mahasiswa', 'Pemilihan Ketua dan Wakil Ketua Badan Eksekutif Mahasiswa ITB STIKOM Bali Periode 2020/2021', '2021-08-13 10:00:00', '2021-08-14 10:00:00', '[\'cname\', \'cdesc\', \'cavatar\']', '[\'vname\', \'vdesc\']', 'on', '2021-08-08 17:48:49', '2021-08-09 09:17:01');



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;