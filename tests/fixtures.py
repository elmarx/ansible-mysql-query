import MySQLdb as Db
from tests.settings import MYSQL_CONNECTION_PARAMS


class Fixture:
    def __init__(self):
        self._connection = None

    def cursor(self):
        if not self._connection:
            self._connection = Db.connect(**MYSQL_CONNECTION_PARAMS)

        return self._connection.cursor()

    def close(self):
        if self._connection:
            self._connection.close()

    def _count(self, table):
        cur = self.cursor()
        cur.execute('select COUNT(*) from `%s`' % table)
        # since autocommit is turned off reads reads do not 'see changes' from other connections
        self._connection.commit()
        (result,) = cur.fetchone()
        cur.close()
        return result

    def _insert(self, query, args):
        cur = self.cursor()
        cur.execute(query, args)
        self._connection.commit()
        cur.close()

    def create_database(self):
        create_connection_params = MYSQL_CONNECTION_PARAMS.copy()
        db = create_connection_params.pop('db')
        con = Db.connect(**create_connection_params)

        cur = con.cursor()
        cur.execute('DROP DATABASE IF EXISTS `{0}`;'.format(db))
        cur.execute('CREATE DATABASE `{0}`;'.format(db))
        cur.close()

    def create_key_value_example(self):
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS `key_value_example` (
                  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  `name` varchar(128) NOT NULL UNIQUE,
                  `value` int(11) NOT NULL
                ) ENGINE=InnoDB;""")
        cur.close()

    def create_multicolumn_example(self):
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS `multicolumn_example` (
                  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  `identifier1` varchar(128) NOT NULL UNIQUE,
                  `identifier2` int(11) NOT NULL UNIQUE,
                  `identifier3` varchar(128) NOT NULL UNIQUE,
                  `value1` int(11) NOT NULL,
                  `value2` varchar(255) NOT NULL,
                  `value3` text
                ) ENGINE=InnoDB;""")
        cur.close()

    def create_change_example(self):
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS `change_example` (
                  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  `setting_name` varchar(128) NOT NULL,
                  `setting_group_id` int(11) NOT NULL,
                  `value1` int(11) NOT NULL,
                  `value2` varchar(255) NOT NULL,
                  `default1` int(11) NOT NULL,
                  `default2` int(11) NOT NULL DEFAULT 42,
                  `default3` varchar(255) NOT NULL
                ) ENGINE=InnoDB;""")
        cur.close()

    def insert_into_key_value_example(self, key, value):
        self._insert('insert into `key_value_example` values (DEFAULT, %s, %s);', (key, value))

    def insert_into_multicolumn_example(self, ids, vals):
        self._insert("insert into `multicolumn_example` values (DEFAULT, %s, %s, %s, %s, %s, %s);", tuple(ids + vals))

    def insert_into_change_example(self, ids, vals, defaults):
        self._insert("insert into `change_example` values (DEFAULT, %s, %s, %s, %s, %s, %s, %s);",
                     tuple(ids + vals + defaults))

    def count_multicolumn_example(self):
        return self._count('multicolumn_example')

    def count_key_value_example(self):
        return self._count('key_value_example')

    def count_change_example(self):
        return self._count('change_example')

    def query_change_example(self, setting_name, setting_group_id):
        cur = self.cursor()
        cur.execute('select * from `change_example` where `setting_name` = %s and `setting_group_id` = %s', (setting_name, setting_group_id))
        result = cur.fetchone()
        cur.close()
        return result
