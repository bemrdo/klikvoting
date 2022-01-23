/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `c_9skxEXwz`;
CREATE TABLE `c_9skxEXwz` (
  `id_candidate` varchar(40) NOT NULL,
  `id_voting` varchar(40) NOT NULL,
  `username` varchar(40) NOT NULL,
  `pass` varchar(40) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `avatar` varchar(40) DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  `validator` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_candidate`),
  KEY `id_voting` (`id_voting`),
  CONSTRAINT `c_9skxEXwz_ibfk_1` FOREIGN KEY (`id_voting`) REFERENCES `voting` (`id_voting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `c_EwMdQmrR`;
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

DROP TABLE IF EXISTS `h_9skxEXwz`;
CREATE TABLE `h_9skxEXwz` (
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
  CONSTRAINT `h_9skxEXwz_ibfk_1` FOREIGN KEY (`id_voting`) REFERENCES `voting` (`id_voting`),
  CONSTRAINT `h_9skxEXwz_ibfk_2` FOREIGN KEY (`id_candidate`) REFERENCES `c_9skxEXwz` (`id_candidate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `h_EwMdQmrR`;
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

DROP TABLE IF EXISTS `problem`;
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

DROP TABLE IF EXISTS `user`;
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

DROP TABLE IF EXISTS `v_9skxEXwz`;
CREATE TABLE `v_9skxEXwz` (
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
  CONSTRAINT `v_9skxEXwz_ibfk_1` FOREIGN KEY (`id_voting`) REFERENCES `voting` (`id_voting`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `v_EwMdQmrR`;
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

DROP TABLE IF EXISTS `voting`;
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

INSERT INTO `c_9skxEXwz` (`id_candidate`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('eDH7TEe5', '9skxEXwz', 'C-CtqmvqIm', '3cvzJ2xW23mK', 'Putu Ananda Widya Putra A. & I GD. Nyoman Sedana A.', '<p class=\"ql-align-center\"><strong class=\"ql-size-large\">VISI</strong></p><p class=\"ql-align-center\">Menjadikan BEM sebagai lembaga yang interaktif kepada mahasiswa kampus.</p><p><br></p><p class=\"ql-align-center\"><strong class=\"ql-size-large\">MISI</strong></p><p class=\"ql-align-center\">1. Membangun internal BEM berlandaskan kekeluargaan dan profesionalisme.</p><p class=\"ql-align-center\">2. Mengoptimalkan fungsi aspirasi antara mahasiswa dengan kampus.</p><p><br></p>', 'eDH7TEe5_2022-01-18_134920.529586', 'blocked', NULL, '2022-01-18 13:49:21');
INSERT INTO `c_9skxEXwz` (`id_candidate`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('oYv38cSh', '9skxEXwz', 'C-HggsKhdF', 'JVCkpZbId1Du', 'I Made Angga Saputra & Gusti Bagus Arya Dwipayana', '<p class=\"ql-align-center\"><strong class=\"ql-size-large\">VISI</strong></p><p class=\"ql-align-center\">Mempertahankan dan meningkatkan kinerja BEM ITB STIKOM Bali dalam mengayomi ORMAWA serta mempererat hubungan dengan manajemen dan aliansi BEM di luar kampus.</p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-center\"><strong class=\"ql-size-large\">MISI</strong></p><p class=\"ql-align-center\">1. Melibatkan ORMAWA sebagai wadah dalam memaksimalkan potensi mahasiswa dan meningkatkan kinerja organisasi.</p><p class=\"ql-align-center\">2. Meningkatkan kesadaran berorganisasi antar ORMAWA dan mahasiswa ITB STIKOM Bali.</p><p class=\"ql-align-center\">3. Mempererat hubungan komunikasi antar kampus di tingkat regional dan nasional.</p><p class=\"ql-align-center\">4. Mengoptimalisasi koordinasi antar BEM, ORMAWA, manajemen ITB STIKOM Bali.</p><p><br></p>', 'oYv38cSh_2022-01-18_135221.359160', 'blocked', NULL, '2022-01-18 13:52:21');


INSERT INTO `c_EwMdQmrR` (`id_candidate`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('G9mGwLDK', 'EwMdQmrR', 'C-3I4X9B8Q', 'oqqx4b5oK8So', 'Komang Bhargo Bhaskara & I Ketut Agus Sugiartha', '<p class=\"ql-align-center\"><strong class=\"ql-size-large\">VISI</strong></p><p class=\"ql-align-center\">Terwujudnya Badan Eksekutif Mahasiswa ITB STIKOM Bali sebagai wadah pelayanan yang interaktif bagi mahasiswa umum dan ORMAWA guna bersinergi dalam menciptakan inovasi</p><p><br></p><p class=\"ql-align-center\"><strong class=\"ql-size-large\">MISI</strong></p><ol><li>Menjalankan fungsi ORMAWA ITB STIKOM Bali berdasarkan Tri Dharma Perguruan Tinggi</li><li>Memetakan dan mengembangkan potensi mahasiswa ITB STIKOM Bali, serta memperkuat jaringan internal maupun eksternal</li><li>Membangun ruang kolaborasi dan gagasan antar ORMAWA guna menumbuhkan dan memperkuat rasa saling percaya satu sama lain</li><li>Membangun sikap profesionalisme di dalam organisasi guna meningkatkan produktivitas dalam semangat solidaritas</li></ol>', 'G9mGwLDK_2021-08-08_175526.523318', 'blocked', NULL, '2021-08-08 17:55:27');
INSERT INTO `c_EwMdQmrR` (`id_candidate`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('lDz7CGxF', 'EwMdQmrR', 'C-8LgTLc7e', 'QWw9V82OlHYy', 'I Made Yudi Setiawan & I.B. Agung Indra Putra Pidada', '<p class=\"ql-align-center\"><strong class=\"ql-size-large\">VISI</strong></p><p class=\"ql-align-center\">BEM ITB STIKOM Bali menjadi penyambung aspirasi dan inspirasi mahasiswa dan juga meningkatkan kualitas maupun elektabilitas dengan harapan BEM ITB STIKOM Bali mampu bersaing dengan kampus PTN/PTS di ranah Kota, Provinsi maupun Nasional</p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-center\"><strong class=\"ql-size-large\">Misi</strong></p><ol><li>Meningkatkan Kinerja dan Kualitas BEM dengan metode kolektif kolegial (gotong royong)</li><li>Menjalin hubungan yang harmonis dengan cara merangkul dan melayani ORMAWA yang ada di kampus ITB STIKOM Bali</li><li>Meningkatkan kualitas mahasiswa dan mahasiswi dengan memajukan dan memakmurkan ORMAWA yang ada di ITB STIKOM Bali</li><li>Menampung aspirasi dan memecahkan masalah mahasiswa dengan prinsip dialog intelektual dan prinsip kekeluargaan</li><li>Mampu menyelenggarakan dan merealisasikan kegiatan di dalam kampus maupun di luar kampus</li></ol>', 'lDz7CGxF_2021-08-13_091223.158439', 'blocked', NULL, '2021-08-13 09:12:23');


INSERT INTO `h_9skxEXwz` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('3cvzJ2xW', '9skxEXwz', 'eDH7TEe5', 'voter', 'LZOxdXxswEx5JmRCnS55QPA/ysH0z6SS3hrzKxBfNi4=', 'checked', '2022-01-19 06:36:35');
INSERT INTO `h_9skxEXwz` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('HNo2Qj7G', '9skxEXwz', 'eDH7TEe5', 'voter', 'GiFkcHlCMgS5DfJp/Yel6E0FLZdjoWZVI/rY6Y/l5s0=', 'rejected', '2022-01-19 06:39:23');
INSERT INTO `h_9skxEXwz` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('tl2vOVRZ', '9skxEXwz', 'eDH7TEe5', 'voter', 'PTGi1gPi/HM0XSizrpSD5K6EDIok56KsBPo1Qj3KxCM=', 'checked', '2022-01-19 06:37:37');

INSERT INTO `h_EwMdQmrR` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('3SdALMxl', 'EwMdQmrR', 'G9mGwLDK', 'voter', 'FRJWEWd7gRFS1jawfvNhjb3h3O+9so5qCtzGua0C/68=', 'checked', '2021-08-09 09:01:29');
INSERT INTO `h_EwMdQmrR` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('hBGfk2v7', 'EwMdQmrR', 'G9mGwLDK', 'voter', 'SwekNbYLyP3tEa5FkPLTIYG9CCx18/Fib6hkACrCl9c=', 'rejected', '2021-12-30 13:55:06');
INSERT INTO `h_EwMdQmrR` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('lBEOlHdK', 'EwMdQmrR', 'G9mGwLDK', 'voter', 'ExE8BLQ6VXEQBYgaEtmbzRamZoph2LGNZV9TD7Lr+Kc=', 'rejected', '2021-12-30 13:53:37');
INSERT INTO `h_EwMdQmrR` (`id_hash`, `id_voting`, `id_candidate`, `role`, `encrypted`, `status`, `created_at`) VALUES
('ncbgyTx4', 'EwMdQmrR', 'G9mGwLDK', 'voter', 'GLfLpNSjiiPPCtQWGCgnx+I6dzImv2YZ7UIQKUEG5mU=', 'rejected', '2021-08-08 18:55:56');

INSERT INTO `problem` (`id_problem`, `id_user`, `id_voting`, `msg_from`, `msg_to`, `message`, `respond`, `msg_created`, `rsp_created`) VALUES
('4FG1yqvD', 'f5wBDkVo', 'EwMdQmrR', 'Voter', 'Organizer', 'Bertanya dulu?', 'baik saya tanggapi', '2021-08-09 09:04:30', '2021-08-09 09:05:21');
INSERT INTO `problem` (`id_problem`, `id_user`, `id_voting`, `msg_from`, `msg_to`, `message`, `respond`, `msg_created`, `rsp_created`) VALUES
('iDv9WIwg', '5oSEXhdI', 'EwMdQmrR', 'Voter', 'Organizer', 'Bagaimana cara memilih Candidate?', 'Perubahan tanggapan baru', '2021-08-08 18:48:20', '2021-08-09 09:04:07');
INSERT INTO `problem` (`id_problem`, `id_user`, `id_voting`, `msg_from`, `msg_to`, `message`, `respond`, `msg_created`, `rsp_created`) VALUES
('sAwyOjDN', '8lZk8BRC', 'EwMdQmrR', 'Organizer', 'Admin', 'Bagaimana cara menambah Candidate?', 'Gunakan tombol Tambah Candidate', '2021-08-08 17:51:35', '2021-08-08 17:52:12');

INSERT INTO `user` (`id_user`, `name`, `email`, `number`, `pass`, `institution`, `address`, `card_id`, `role`, `created_at`, `status`, `message`) VALUES
('8lZk8BRC', 'Panitia Pemilu BEM', 'panitiabem@mail.com', '08123456789', 'pbkdf2:sha256:260000$UBkjVleszpGIWkWX$f4b98607eba2e3ab931bb2e1fcbd7b2711c9cb9dd2de89d8975220741dad3632', 'ITB STIKOM Bali', 'Jl. Raya Puputan No.86, Dangin Puri Klod, Kec. Denpasar Tim., Kota Denpasar, Bali 80234', '8lZk8BRC_2021-08-08_170807.925488', 'organizer', '2021-08-08 17:08:08', 'approved', '[Perubahan Profil]');
INSERT INTO `user` (`id_user`, `name`, `email`, `number`, `pass`, `institution`, `address`, `card_id`, `role`, `created_at`, `status`, `message`) VALUES
('9IP9swEO', 'Admin', 'admin@mail.com', '08123456789', 'pbkdf2:sha256:260000$2k3ag2qMfshNyeOo$b221cf77e7e03aa937b1d2107da82252ada0342ae3f1570e379045b14cb8b80c', 'klikvoting', 'di rumah', '9IP9swEO_2021-07-18_225103.227726', 'admin', '2021-07-18 22:51:03', 'approved', '[Akun Admin]');
INSERT INTO `user` (`id_user`, `name`, `email`, `number`, `pass`, `institution`, `address`, `card_id`, `role`, `created_at`, `status`, `message`) VALUES
('HNo2Qj7G', 'da', 'panitiapemilu@mail.com', '087762804369', 'pbkdf2:sha256:260000$senOOT6d5TIR8hSB$b7b80de6f328239d630ae87004ca8ebccf44ce3efe2db720f41523eab39d1cd8', 'klikvoting', 'Jl. Katrangan Gg. leli No. 5, Ds. Sumerta, Kec. Denpasar Timur', 'HNo2Qj7G_2022-01-19_145113.984417', 'organizer', '2022-01-19 14:51:14', 'pending', '[Akun Baru]');
INSERT INTO `user` (`id_user`, `name`, `email`, `number`, `pass`, `institution`, `address`, `card_id`, `role`, `created_at`, `status`, `message`) VALUES
('NJeRDBhi', 'Panitia Pemilu', 'panitiapemilu@mail.com', '087762804369', 'pbkdf2:sha256:260000$AnyOz9pXxuLuj4hm$8355f9f759bbace8b4b9fe1ded02d20e965ace939f3f47338d846d94689c0c63', 'BEM ITB STIKOM Bali', 'Ruang Sekretariat BEM lt. 1, Kampus ITB STIKOM Bali', 'NJeRDBhi_2022-01-18_004847.319446', 'organizer', '2022-01-18 00:48:47', 'approved', '[Akun Baru]'),
('PbKcAx51', 'Akun Baru', 'baru@mail.com', '087762804369', 'pbkdf2:sha256:260000$sbi2d6QcZJU4N7Qb$0b4b8a758e63a9c125ce7898232e99b70e2bad42ee2d9eeeaecf5ae7194c2b00', 'Baru', 'Alamat Baru', 'PbKcAx51_2022-01-18_124251.273833', 'organizer', '2022-01-18 12:42:51', 'pending', '[Akun Baru]');

INSERT INTO `v_9skxEXwz` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('3TTzlKpE', '9skxEXwz', 'V-bIgBOUV0', 'cT0OIuQdPrQQ', 'Mahasiswa 2', NULL, NULL, NULL, NULL, '2022-01-18 09:27:06');
INSERT INTO `v_9skxEXwz` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('8diV1vfY', '9skxEXwz', 'V-fRuaoJnr', 'Sg1YqCY8YUEA', 'Mahasiswa 6', NULL, NULL, '3cvzJ2xW', 'Cfz91CvsIsVMhRKStk+PVg==', '2022-01-18 09:27:32');
INSERT INTO `v_9skxEXwz` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('9pCjphgQ', '9skxEXwz', 'V-GJs0y9Id', 'kfoO5Fo8plbo', 'Mahasiswa 3', NULL, NULL, NULL, NULL, '2022-01-18 09:27:12');
INSERT INTO `v_9skxEXwz` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('MHNGkdi5', '9skxEXwz', 'V-q6kLaZDZ', 'NbtMbL5nnYWS', 'Mahasiswa 4', NULL, NULL, 'HNo2Qj7G', 'dFykWEt+CHRxhbvgrgoztw==', '2022-01-18 09:27:18'),
('YOxfcKlI', '9skxEXwz', 'V-r994Oa00', 'Po39nWHWKRve', 'Mahasiswa 5', NULL, NULL, 'tl2vOVRZ', '0bp82HVYwhAkL+klRXyyiQ==', '2022-01-18 09:27:24'),
('zhmezRVd', '9skxEXwz', 'V-WNUgYs2W', 'VCDt1AzirGqR', 'Mahasiswa 1', NULL, NULL, NULL, NULL, '2022-01-18 09:26:58');

INSERT INTO `v_EwMdQmrR` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('CwauGCy5', 'EwMdQmrR', 'V-iXnLGF5Y', 'EKoFXqoUf4jM', 'Mahasiswa 3', 'NIM : 170030020', NULL, 'lBEOlHdK', 'wYQVH7YmPY4wRt4BMsGU9Q==', '2021-08-13 09:13:21');
INSERT INTO `v_EwMdQmrR` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('f5wBDkVo', 'EwMdQmrR', 'V-vI8MYZXU', 'vr0bsaOf4deg', 'Mahasiswa 2', 'NIM : 170010002', NULL, '3SdALMxl', '6u5c7AUujBUbNGQ0z2xRbA==', '2021-08-09 08:56:24');
INSERT INTO `v_EwMdQmrR` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('HNo2Qj7G', 'EwMdQmrR', 'V-2K0ZxEIg', 'WBTzqrq2HaQ9', 'Voter Baru', '-', NULL, NULL, NULL, '2022-01-19 14:59:31');
INSERT INTO `v_EwMdQmrR` (`id_voter`, `id_voting`, `username`, `pass`, `name`, `description`, `avatar`, `status`, `validator`, `created_at`) VALUES
('yx3JjAN3', 'EwMdQmrR', 'V-VzMqWlFR', 'mdfsqBlgOVuc', 'Mahasiswa 4', 'NIM : 180030303', NULL, 'hBGfk2v7', '8+trWH3QdIiF8x/SGJPzFg==', '2021-08-13 09:13:57');

INSERT INTO `voting` (`id_voting`, `id_user`, `name`, `voting_desc`, `date_start`, `date_end`, `candidate`, `voter`, `viewer`, `created_at`, `last_checked`) VALUES
('9skxEXwz', 'NJeRDBhi', 'Pemilu BEM ITB STIKOM Bali', 'Pemilu Badan Eksekutif Mahasiswa ITB STIKOM Bali periode 2021/2022', '2022-01-19 14:00:00', '2022-01-19 14:20:00', '[\'cname\', \'cdesc\', \'cavatar\']', '[\'vname\']', 'on', '2022-01-18 09:08:05', '2022-01-19 14:54:51');
INSERT INTO `voting` (`id_voting`, `id_user`, `name`, `voting_desc`, `date_start`, `date_end`, `candidate`, `voter`, `viewer`, `created_at`, `last_checked`) VALUES
('CtqmvqIm', '8lZk8BRC', 'Voting Baru', 'deskripsi', '2022-01-19 15:00:00', '2022-01-20 15:00:00', '[\'cname\', \'cdesc\', \'cavatar\']', '[\'vname\', \'vdesc\']', 'on', '2022-01-19 14:33:07', '2022-01-19 06:33:07');
INSERT INTO `voting` (`id_voting`, `id_user`, `name`, `voting_desc`, `date_start`, `date_end`, `candidate`, `voter`, `viewer`, `created_at`, `last_checked`) VALUES
('eDH7TEe5', 'NJeRDBhi', 'Voting Baru', '-', '2022-01-19 15:00:00', '2022-01-20 15:00:00', '[\'cname\', \'cdesc\']', '[\'vname\']', 'on', '2022-01-19 14:31:42', '2022-01-19 06:31:42');
INSERT INTO `voting` (`id_voting`, `id_user`, `name`, `voting_desc`, `date_start`, `date_end`, `candidate`, `voter`, `viewer`, `created_at`, `last_checked`) VALUES
('EwMdQmrR', '8lZk8BRC', 'Pemilu Badan Eksekutif Mahasiswa', 'Pemilihan Ketua dan Wakil Ketua Badan Eksekutif Mahasiswa ITB STIKOM Bali Periode 2020/2021', '2021-12-29 17:00:00', '2021-12-29 23:00:00', '[\'cname\', \'cdesc\', \'cavatar\']', '[\'vname\', \'vdesc\']', 'on', '2021-08-08 17:48:49', '2022-01-19 15:12:42'),
('hBGfk2v7', '8lZk8BRC', 'oke', 'oke', '2022-01-23 12:00:00', '2022-01-24 12:00:00', '[\'cname\', \'cdesc\', \'cavatar\']', '[\'vname\', \'vdesc\']', 'off', '2022-01-23 11:34:21', '2022-01-23 03:34:20');

CREATE TRIGGER tr_dt_table BEFORE INSERT ON voting FOR EACH ROW BEGIN
  SET NEW.datetime_field = NOW() + INTERVAL 8 HOUR;
END

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
