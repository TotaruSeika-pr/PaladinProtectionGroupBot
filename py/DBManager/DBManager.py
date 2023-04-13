import sqlite3


class DBManager:
    
    def __init__(self):
        self.con = sqlite3.connect('DataBase/DataBase.db', check_same_thread=False)
        self.cur = self.con.cursor()
        DBManager.CreatingTable(self)



    def CreatingTable(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS telegram_users(
        id INT,
        telegram_id INT,
        username TEXT
        )""")
        self.con.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS workers(
        id INT,
        telegram_id INT,
        real_name TEXT,
        specialization TEXT,
        official_progress INT,
        quest_progress INT
        )""")
        self.con.commit()
