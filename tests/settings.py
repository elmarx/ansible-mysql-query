import os


MYSQL_CONNECTION_PARAMS = {
        'host': os.getenv('MYSQL_HOST', '::1'),
        'user': os.getenv('MYSQL_USERNAME', 'root'),
        'passwd': os.getenv('MYSQL_PASSWORD', 'password'),
        'db': os.getenv('MYSQL_DB', 'ansible-mysql-query-test'),
}
