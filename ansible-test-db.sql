CREATE DATABASE `ansible-test`;

USE `ansible-test`;

CREATE TABLE IF NOT EXISTS `key_value_example` (
  `id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `value` int(11) NOT NULL
) ENGINE=InnoDB;

ALTER TABLE `key_value_example` ADD PRIMARY KEY (`id`);

ALTER TABLE `key_value_example` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

