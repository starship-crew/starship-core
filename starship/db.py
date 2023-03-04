import os

MYSQL_HOST_FALLBACK = "localhost"
MYSQL_USER_FALLBACK = "root"
MYSQL_PASSWORD_FALLBACK = "toor"
MYSQL_DATABASE_FALLBACK = "starship"

MYSQL_USER = os.getenv("MYSQL_USER", MYSQL_USER_FALLBACK)
MYSQL_HOST = os.getenv("MYSQL_HOST", MYSQL_HOST_FALLBACK)
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", MYSQL_DATABASE_FALLBACK)
MYSQL_PASSWORD_FILE = os.getenv("MYSQL_PASSWORD_FILE")


def get_mysql_password():
    if MYSQL_PASSWORD_FILE:
        with open(MYSQL_PASSWORD_FILE) as file:
            return file.read().rstrip()
    return MYSQL_PASSWORD_FALLBACK


def connect():
    from mysql.connector import connect

    return connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=get_mysql_password(),
        database=MYSQL_DATABASE,
    )
