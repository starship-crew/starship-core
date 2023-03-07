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


_connection = None


def connector(func):
    def with_connection(*args, **kwargs):
        from mysql.connector import Error

        if _connection:
            con = _connection
        else:
            con = connect()

        try:
            func_result = func(con, *args, **kwargs)
        except Error as error:
            con.rollback()
            raise error
        else:
            con.commit()
        finally:
            con.close()

        return func_result

    return with_connection


def get_url():
    return f"mysql+pymysql://{MYSQL_USER}:{get_mysql_password()}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"
