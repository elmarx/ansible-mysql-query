CREATE TABLE IF NOT EXISTS `simple_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `some_id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL,
  `department_id` int(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_login` int(11) NOT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO `simple_table`
  (`id`, `some_id`, `email`, `role`, `department_id`, `password`, `last_login`)
  VALUES (NULL, 23, 'john@example.com', 'admin', 42, PASSWORD('CHANGE_ME'), 1472070012);
