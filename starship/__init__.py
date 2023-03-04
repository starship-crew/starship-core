from flask import Flask

app = Flask(__name__)


def get_mysql_password():
    with open("/run/secrets/mysql_root_password") as file:
        return file.read().rstrip()


@app.route("/")
def index():
    from mysql.connector import connect, Error

    try:
        with connect(
            host="mysqldb",
            user="root",
            password=get_mysql_password(),
            database="starship",
        ) as connection:
            print()
            print()
            show_db_query = "SHOW DATABASES"
            with connection.cursor() as cursor:
                cursor.execute(show_db_query)
                for db in cursor:
                    print(db)
            print()
            print()
    except Error as e:
        print(e)
    return "Hi"


if __name__ == "__main__":
    import pyruvate

    pyruvate.serve(app, "0.0.0.0:80", 2)
