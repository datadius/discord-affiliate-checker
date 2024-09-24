import psycopg2
import datetime
import os


class SQLAffiliate:
    def __init__(self):
        self.db_path = {
            "dbname": "railway",
            "user": os.getenv("PGUSER"),
            "password": os.getenv("PGPASSWORD"),
            "port": "5432",
            "host": os.getenv("PGHOST"),
        }

    def initialize_db(self):
        db = psycopg2.connect(**self.db_path)
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, uid TEXT, approvalDatetime TEXT, username TEXT, deposit INTEGER, exchange TEXT);"
        )
        db.commit()
        db.close()

    def add_user(self, uid, username, deposit, exchange):
        db = psycopg2.connect(**self.db_path)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (uid, approvalDatetime, username, deposit, exchange) VALUES (%s,%s,%s,%s,%s);",
            (str(uid), str(now), str(username), deposit, str(exchange)),
        )
        db.commit()
        db.close()

    def check_user_exists(self, uid):
        db = psycopg2.connect(**self.db_path)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE uid=%s;", (str(uid)))
        user = cursor.fetchone()
        db.close()
        if user:
            return True
        return False

    def get_users(self):
        db = psycopg2.connect(**self.db_path)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        db.close()
        return users


if __name__ == "__main__":
    sql_db = SQLAffiliate()
    print(sql_db.initialize_db())
    print(sql_db.get_users())
