import sqlite3


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('tasks.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force=False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS tasks')

    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL, 
            date TEXT NOT NULL
        )
    """)
    conn.commit()


@ensure_connection
def add_task(conn, user_id, task, date):
    c = conn.cursor()
    c.execute('INSERT INTO tasks (user_id, task, date) VALUES (?, ?, ?)', (user_id, task, date))
    conn.commit()


@ensure_connection
def delete_task(conn, user_id, task, date):
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE rowid = (SELECT rowid FROM tasks WHERE user_id = ? AND task = ? AND date = ? LIMIT 1 )", (user_id, task, date))
    conn.commit()


@ensure_connection
def change_task(conn, user_id, task, date, update):
    c = conn.cursor()
    c.execute("""
        UPDATE tasks
        SET task = ?
        WHERE task = ? AND user_id = ? AND date = ?
    """, (update, task, user_id, date))


@ensure_connection
def show_week(conn, user_id):
    c = conn.cursor()
    c.execute("""
        SELECT task, date
        FROM tasks
        WHERE date <= DATE('now', '+7 days') and tasks.user_id == ?
        ORDER BY date 
    """, (user_id,))
    return c.fetchall()


@ensure_connection
def show_month(conn, user_id):
    c = conn.cursor()
    c.execute("""
        SELECT task, date
        FROM tasks
        WHERE date <= DATE('now', '+1 month') and tasks.user_id == ?
        ORDER BY date 
    """, (user_id,))
    return c.fetchall()


@ensure_connection
def show_all(conn, user_id):
    c = conn.cursor()
    c.execute('SELECT task, date FROM tasks WHERE tasks.user_id == ? ORDER BY date', (user_id,))
    return c.fetchall()

# if __name__ == '__main__':
#     init_db()
#     add_task(user_id=1234, task='do dishes', date='2022-08-27')
#     add_task(user_id=1234, task='read a book', date='2022-08-25')
#     add_task(user_id=5678, task='go shopping', date='2022-05-15')
#     add_task(user_id=1234, task='chill with friends', date='2022-09-31')
#     print(show_month(user_id=1234))
#     print(show_all(user_id=1234))
#     change_task(task='do chores', update='wash dishes')
