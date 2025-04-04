import sqlite3


def connect_db(db_name="music.db"):
    return sqlite3.connect(db_name)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255),
        description TEXT,
        year INTEGER
    );

    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255),
        duration INTEGER,
        album_id INTEGER,
        FOREIGN KEY (album_id) REFERENCES albums(id)
    );

    CREATE TABLE IF NOT EXISTS song_authors (
        song_id INTEGER,
        author_id INTEGER,
        PRIMARY KEY (song_id, author_id),
        FOREIGN KEY (song_id) REFERENCES songs(id),
        FOREIGN KEY (author_id) REFERENCES authors(id)
    );

    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Таблицы успешно созданы.")


def add_album(title, description, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO albums (title, description, year) VALUES (?, ?, ?)", (title, description, year))
    conn.commit()
    conn.close()
    print(f"✅ Альбом '{title}' добавлен.")


def add_author(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print(f"✅ Автор '{name}' добавлен.")


def add_song(title, duration, album_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs (title, duration, album_id) VALUES (?, ?, ?)", (title, duration, album_id))
    song_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"✅ Песня '{title}' добавлена.")
    return song_id


def add_song_author(song_id, author_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO song_authors (song_id, author_id) VALUES (?, ?)", (song_id, author_id))
    conn.commit()
    conn.close()
    print(f"✅ Автор ID {author_id} связан с песней ID {song_id}.")


if __name__ == "__main__":
    create_tables()


    add_album("Album 1", "First album", 2020)
    add_album("Album 2", "Second album", 2021)

    
    add_author("Author 1")
    add_author("Author 2")

    
    song1 = add_song("Song 1", 200, 1)
    song2 = add_song("Song 2", 180, 1)

    add_song_author(song1, 1)
    add_song_author(song2, 1)
