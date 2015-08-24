import os


MYSQL_CONNECTION_PARAMS = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USERNAME', 'root'),
        'passwd': os.getenv('MYSQL_PASSWORD', ''),
        'db': os.getenv('MYSQL_DB', 'ansible-mysql-query-test'),
}
