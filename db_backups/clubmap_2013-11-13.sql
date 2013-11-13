# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.32-MariaDB)
# Database: clubmap
# Generation Time: 2013-11-12 23:45:02 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_group_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_permission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`)
VALUES
	(1,'Can add log entry',1,'add_logentry'),
	(2,'Can change log entry',1,'change_logentry'),
	(3,'Can delete log entry',1,'delete_logentry'),
	(4,'Can add permission',2,'add_permission'),
	(5,'Can change permission',2,'change_permission'),
	(6,'Can delete permission',2,'delete_permission'),
	(7,'Can add group',3,'add_group'),
	(8,'Can change group',3,'change_group'),
	(9,'Can delete group',3,'delete_group'),
	(10,'Can add user',4,'add_user'),
	(11,'Can change user',4,'change_user'),
	(12,'Can delete user',4,'delete_user'),
	(13,'Can add content type',5,'add_contenttype'),
	(14,'Can change content type',5,'change_contenttype'),
	(15,'Can delete content type',5,'delete_contenttype'),
	(16,'Can add session',6,'add_session'),
	(17,'Can change session',6,'change_session'),
	(18,'Can delete session',6,'delete_session'),
	(19,'Can add migration history',7,'add_migrationhistory'),
	(20,'Can change migration history',7,'change_migrationhistory'),
	(21,'Can delete migration history',7,'delete_migrationhistory'),
	(22,'Can add artist',8,'add_artist'),
	(23,'Can change artist',8,'change_artist'),
	(24,'Can delete artist',8,'delete_artist'),
	(25,'Can add genre',9,'add_genre'),
	(26,'Can change genre',9,'change_genre'),
	(27,'Can delete genre',9,'delete_genre'),
	(28,'Can add event',10,'add_event'),
	(29,'Can change event',10,'change_event'),
	(30,'Can delete event',10,'delete_event'),
	(31,'Can add location',11,'add_location'),
	(32,'Can change location',11,'change_location'),
	(33,'Can delete location',11,'delete_location'),
	(34,'Can add artist names',12,'add_artistnames'),
	(35,'Can change artist names',12,'change_artistnames'),
	(36,'Can delete artist names',12,'delete_artistnames');

/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`)
VALUES
	(1,'pbkdf2_sha256$12000$ORJpBwhr99hE$XmSqv9WluG42dlbJ6jOYrRw3DTwTBw5FbFQIHp+nAIw=','2013-11-11 23:09:34',1,'alan','','','rainer.beckerpgp@googlemail.com',1,1,'2013-11-11 23:09:07');

/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_user_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_user_user_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_admin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`)
VALUES
	(1,'log entry','admin','logentry'),
	(2,'permission','auth','permission'),
	(3,'group','auth','group'),
	(4,'user','auth','user'),
	(5,'content type','contenttypes','contenttype'),
	(6,'session','sessions','session'),
	(7,'migration history','south','migrationhistory'),
	(8,'artist','events','artist'),
	(9,'genre','events','genre'),
	(10,'event','events','event'),
	(11,'location','events','location'),
	(12,'artist names','events','artistnames');

/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`)
VALUES
	('1zlbss30dtegk6ovsls8m0kk4ge9vsdn','Nzc5ZTc1MmU4Y2VkMmI1NDVlMGYxNTQ3MzYyODFjNzBmZWIyODc1MTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2013-11-25 23:09:34');

/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table events_artist
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_artist`;

CREATE TABLE `events_artist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `label` varchar(200) NOT NULL,
  `soundcloud_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_artistnames
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_artistnames`;

CREATE TABLE `events_artistnames` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_artistnames_artist
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_artistnames_artist`;

CREATE TABLE `events_artistnames_artist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `artistnames_id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `artistnames_id` (`artistnames_id`,`artist_id`),
  KEY `events_artistnames_artist_c809a5c0` (`artistnames_id`),
  KEY `events_artistnames_artist_7904f807` (`artist_id`),
  CONSTRAINT `artistnames_id_refs_id_40024bba` FOREIGN KEY (`artistnames_id`) REFERENCES `events_artistnames` (`id`),
  CONSTRAINT `artist_id_refs_id_8ec99a29` FOREIGN KEY (`artist_id`) REFERENCES `events_artist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_event
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_event`;

CREATE TABLE `events_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_name` varchar(200) NOT NULL,
  `event_date` datetime NOT NULL,
  `pub_date` datetime NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_event_artists
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_event_artists`;

CREATE TABLE `events_event_artists` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `artist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_id` (`event_id`,`artist_id`),
  KEY `events_event_artists_a41e20fe` (`event_id`),
  KEY `events_event_artists_7904f807` (`artist_id`),
  CONSTRAINT `event_id_refs_id_a731eaa7` FOREIGN KEY (`event_id`) REFERENCES `events_event` (`id`),
  CONSTRAINT `artist_id_refs_id_8e901e25` FOREIGN KEY (`artist_id`) REFERENCES `events_artist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_event_genres
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_event_genres`;

CREATE TABLE `events_event_genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_id` (`event_id`,`genre_id`),
  KEY `events_event_genres_a41e20fe` (`event_id`),
  KEY `events_event_genres_33e6008b` (`genre_id`),
  CONSTRAINT `event_id_refs_id_1c4a0f37` FOREIGN KEY (`event_id`) REFERENCES `events_event` (`id`),
  CONSTRAINT `genre_id_refs_id_9cea92e4` FOREIGN KEY (`genre_id`) REFERENCES `events_genre` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_genre
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_genre`;

CREATE TABLE `events_genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `genre_name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_genre_parent_id
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_genre_parent_id`;

CREATE TABLE `events_genre_parent_id` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_genre_id` int(11) NOT NULL,
  `to_genre_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_genre_id` (`from_genre_id`,`to_genre_id`),
  KEY `events_genre_parent_id_838fdaa6` (`from_genre_id`),
  KEY `events_genre_parent_id_2b2e0a45` (`to_genre_id`),
  CONSTRAINT `to_genre_id_refs_id_e3747f9b` FOREIGN KEY (`to_genre_id`) REFERENCES `events_genre` (`id`),
  CONSTRAINT `from_genre_id_refs_id_e3747f9b` FOREIGN KEY (`from_genre_id`) REFERENCES `events_genre` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table events_location
# ------------------------------------------------------------

DROP TABLE IF EXISTS `events_location`;

CREATE TABLE `events_location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pub_date` datetime NOT NULL,
  `location_name` varchar(200) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `street` varchar(200) NOT NULL,
  `postal_code` int(10) unsigned NOT NULL,
  `city` varchar(200) NOT NULL,
  `country_code` varchar(2) NOT NULL,
  `website` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table south_migrationhistory
# ------------------------------------------------------------

DROP TABLE IF EXISTS `south_migrationhistory`;

CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
