import sqlite3


class SQLAffiliate:
    def __init__(self):
        self.db_path = "./data/affiliate.db"

    def initialize_db(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT)"
        )
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uid_index ON users (uid)")
        db.commit()
        db.close()

    def add_user(self, uid):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (uid) VALUES (?)", (uid,))
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
