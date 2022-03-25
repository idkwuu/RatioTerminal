import sqlite3

con = sqlite3.connect('leaderboard.db', check_same_thread=False)
cur = con.cursor()


def lb_db_init():
    cur.execute("CREATE TABLE IF NOT EXISTS leaderboard ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id TEXT, "
                "server_id TEXT, "
                "score INTEGER)")
    con.commit()


def lb_db_get_user_score(user_id: str):
    scores = cur.execute("SELECT score FROM leaderboard WHERE user_id = ?", [user_id]).fetchall()
    final_score = 0
    for r in scores:
        final_score += r[0]
    return final_score


def lb_db_get_user_server_record(user_id: str, server_id: str):
    return cur.execute("SELECT * FROM leaderboard WHERE user_id = ? AND server_id = ?", [user_id, server_id]).fetchone()


def lb_db_get_server_leaderboard(server_id: str):
    return cur.execute("SELECT user_id, score FROM leaderboard WHERE server_id = ? ORDER BY score DESC", [server_id]).fetchall()


def lb_db_change_score(user_id: str, server_id: str, score: int):
    sqlite_record = lb_db_get_user_server_record(user_id, server_id)
    if sqlite_record is None:
        current_score = score
        cur.execute("INSERT INTO leaderboard VALUES(NULL, ?, ?, ?)", [user_id, server_id, current_score])
    else:
        current_score = sqlite_record[3] + score
        cur.execute('UPDATE leaderboard SET score = ? WHERE id = ?', [current_score, sqlite_record[0]])
    con.commit()
    return current_score
