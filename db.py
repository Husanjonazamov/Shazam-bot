from sqlite3 import connect, Row
con = connect("db (2).db",check_same_thread=False)
con.row_factory = Row
# malumot qo'shish
class DB:
    @staticmethod
    def create(user_id):
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE user_id=?", [user_id])
        if len(cur.fetchall()) == 0:
            cur = con.cursor()
            cur.execute("INSERT INTO users(user_id) VALUES(?)", [user_id])
            con.commit()
            return True
        return False
    @staticmethod
    def all():
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    @staticmethod
    def clear():
        cur = con.cursor()
        cur.execute("DELETE FROM users")
        con.commit()
        return True
