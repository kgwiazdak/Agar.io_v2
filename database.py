import sqlite3


def sign_in(first_name, last_name, email, password, nick):
    con = sqlite3.connect("agarIo.db")
    cur = con.cursor()
    cur.execute("INSERT INTO players VALUES(?,?,?,?,?)",
                (first_name, last_name, email, password, nick))
    con.commit()
    con.close()


def log_in(email, password):
    con = sqlite3.connect("agarIo.db")
    cur = con.cursor()
    cur.execute("SELECT nick FROM players WHERE email=? AND password=?", (email, password))
    nick = cur.fetchone()
    con.commit()
    con.close()
    return nick if nick else False

# con = sqlite3.connect("agarIo.db")
# cur = con.cursor()
# cur.execute("""CREATE TABLE players(first_name text,
#                 last_name text,
#                 email text,
#                 password text,
#                  nick text)""")
# con.commit()
# con.close()
# sign_in("Jan", "Kowalski", "jan@gmail.com", "qwerty", "Janek")
# print(log_in("jan@gmail.com", "qwerty"))
