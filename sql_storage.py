import sqlite3
import datetime
import sys


class SQLAffiliate:
    def __init__(self):
        if sys.platform == "linux":
            self.db_path = "/data/affiliate.db"
        elif sys.platform == "win32":
            self.db_path = "./data/affiliate.db"

    def initialize_db(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, approvalDatetime TEXT, username TEXT, deposit INTEGER, exchange TEXT)"
        )
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uid_index ON users (uid)")
        self.updated_users_table(cursor)
        db.commit()
        db.close()

    def add_user(self, uid, username, deposit, exchange):
        db = sqlite3.connect(self.db_path)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (uid, approvalDatetime, username, deposit, exchange) VALUES (?,?,?,?,?)",
            (uid, now, username, deposit, exchange),
        )
        db.commit()
        db.close()

    def check_user_exists(self, uid):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE uid=?", (uid,))
        user = cursor.fetchone()
        db.close()
        if user:
            return True
        return False

    def updated_users_table(self, cursor):
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        columns = [column[1] for column in columns]
        if "exchange" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN exchange TEXT")
        if "deposit" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN deposit INTEGER")
        if "username" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
        if "approvalDatetime" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN approvalDatetime TEXT")

    def get_users(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        db.close()
        return users


if __name__ == "__main__":
    sql_db = SQLAffiliate()
    print(sql_db.get_users())
