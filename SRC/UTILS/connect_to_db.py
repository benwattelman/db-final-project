import logging
# TODO: pip install mysql-connector-python
import mysql.connector as mysql

database_username = database_password = database_name = 'DbMysql26'

def mysql_connect():
    """Connect to a MySQL server using the SSH tunnel connection
        TODO: make sure you have a running putty with ssh tunnel
    :return connection: Global MySQL database connection
    """

    connection = mysql.connect(
        host='localhost',
        port=3305,
        user=database_username,
        passwd=database_password,
        db=database_name
    )

    return connection


def mysql_disconnect(connection):
    """Closes the MySQL database connection.
    """
    connection.close()
