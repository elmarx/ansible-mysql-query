import MySQLdb as Db


class Fixture:
    def __init__(self):
        self._username = 'root'
        self._db = 'ansible-mysql-query-test'
        self._connection = None

    def cursor(self):
        if not self._connection:
            self._connection = Db.connect(user=self._username, db=self._db)

        return self._connection.cursor()

    def create_database(self):
        con = Db.connect(user=self._username)

        cur = con.cursor()
        cur.execute('DROP DATABASE IF EXISTS `{0}`;'.format(self._db))
        cur.execute('CREATE DATABASE `{0}`;'.format(self._db))
        cur.close()

    def create_key_value_example(self):
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS `key_value_example` (
                  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                  `name` varchar(128) NOT NULL UNIQUE,
                  `value` int(11) NOT NULL
                ) ENGINE=InnoDB;""")
        cur.close()

    def insert_into_key_value_example(self, key, value):
        cur = self.cursor()
        cur.execute('insert into `key_value_example` values (DEFAULT, %s, %s);', (key, value))
        self._connection.commit()
        cur.close()

    def count_key_value_example(self):
        cur = self.cursor()
        cur.execute('select COUNT(*) from `key_value_example`')
        (result,) = cur.fetchone()
        cur.close()
        return result

    def close(self):
        if self._connection:
            self._connection.close()