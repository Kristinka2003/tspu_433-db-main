import sqlite3

def setup_database(db_file='database.sqlite3'):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Создание таблицы authors
    cur.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Создание таблицы quotes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (id)
        )
    ''')

    # Создание таблицы tags
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Создание таблицы quote_tag (связующая таблица для связи quotes и tags)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS quote_tag (
            quote_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (quote_id, tag_id),
            FOREIGN KEY (quote_id) REFERENCES quotes (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()

