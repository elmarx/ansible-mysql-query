CREATE TABLE IF NOT EXISTS `simple_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `identifier1` int(11) NOT NULL,
  `identifier2` varchar(255) NOT NULL,
  `value1` int(11) NOT NULL,
  `value2` varchar(255) NOT NULL,
  `default1` int(11) NOT NULL,
  `default2` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO `simple_table` (`id`, `identifier1`, `identifier2`, `value1`, `value2`, `default1`, `default2`) VALUES (NULL, 4, 'eight', 15, 'sixteen', 23, 'forty-two');