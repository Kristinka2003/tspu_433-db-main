import sqlite3
import csv

def create_tables():
    conn = sqlite3.connect('students.db')  # Название базы данных для SQLite
    cursor = conn.cursor()

    # Таблица факультетов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Таблица групп
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Таблица студентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            course INTEGER NOT NULL,
            specialty TEXT NOT NULL,
            phone TEXT NOT NULL,
            gender TEXT NOT NULL,
            faculty_id INTEGER,
            group_id INTEGER,
            FOREIGN KEY (faculty_id) REFERENCES faculties(id),
            FOREIGN KEY (group_id) REFERENCES groups(id)
        )
    ''')

    conn.commit()
    conn.close()

def import_from_csv(filename='БД - Студент.csv'):
    conn = sqlite3.connect('students.db')  # Подключение к базе данных SQLite
    cursor = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Стандартизация ключей: они могут быть с пробелами и в разном регистре
            row = {k.strip().lower(): v.strip() for k, v in row.items()}

            faculty = row['факультет']
            group = row['группа']

            # Добавление факультета, если не существует
            cursor.execute('SELECT id FROM faculties WHERE name = ?', (faculty,))
            faculty_row = cursor.fetchone()
            if faculty_row is None:
                cursor.execute('INSERT INTO faculties (name) VALUES (?)', (faculty,))
                faculty_id = cursor.lastrowid
            else:
                faculty_id = faculty_row[0]

            # Добавление группы, если не существует
            cursor.execute('SELECT id FROM groups WHERE name = ?', (group,))
            group_row = cursor.fetchone()
            if group_row is None:
                cursor.execute('INSERT INTO groups (name) VALUES (?)', (group,))
                group_id = cursor.lastrowid
            else:
                group_id = group_row[0]

            # Добавление студента
            cursor.execute('''
                INSERT INTO students (
                    full_name, birth_date, course, specialty, phone, gender, faculty_id, group_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['фио'],
                row['дата рождения'],
                int(row['курс']),
                row['специальность'],
                row['номер тел.'].replace(' ', ''),
                row['пол'],
                faculty_id,
                group_id
            ))

    conn.commit()
    conn.close()

# Создаем таблицы
create_tables()

# Импортируем данные из CSV файла
import_from_csv('БД - Студент.csv')

