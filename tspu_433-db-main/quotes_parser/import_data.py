import sqlite3
import csv
import os

def create_tables(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Создаём таблицу authors
    cur.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    ''')

    # Создаём таблицу quotes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        );
    ''')

    # Создаём таблицу tags
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    ''')

    # Создаём таблицу для связи quote_tag
    cur.execute('''
        CREATE TABLE IF NOT EXISTS quote_tag (
            quote_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (quote_id) REFERENCES quotes(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (quote_id, tag_id)
        );
    ''')

    conn.commit()
    conn.close()

def import_data_from_csv(
    csv_file=os.path.join(os.path.dirname(__file__), 'quotes.csv'),
    db_file=os.path.join(os.path.dirname(__file__), 'quotes_books_db.sqlite3')
):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            author = row["author"]
            cur.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author,))
            cur.execute("SELECT id FROM authors WHERE name = ?", (author,))
            author_id = cur.fetchone()[0]

            text = row["text"]
            cur.execute("INSERT INTO quotes (text, author_id) VALUES (?, ?)", (text, author_id))
            quote_id = cur.lastrowid

            tags = row["tags"].split(",")
            for tag in tags:
                tag = tag.strip()
                if tag:
                    cur.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
                    cur.execute("SELECT id FROM tags WHERE name = ?", (tag,))
                    tag_id = cur.fetchone()[0]
                    cur.execute("INSERT OR IGNORE INTO quote_tag (quote_id, tag_id) VALUES (?, ?)", (quote_id, tag_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_file = os.path.join(os.path.dirname(__file__), 'quotes_books_db.sqlite3')
    
    # Создаём таблицы
    create_tables(db_file)
    
    # Импортируем данные
    import_data_from_csv()


