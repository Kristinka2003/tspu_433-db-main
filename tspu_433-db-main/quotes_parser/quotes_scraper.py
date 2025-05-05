import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def get_quotes():
    base_url = "http://quotes.toscrape.com/page/{}/"
    quotes_data = []

    for page_num in range(1, 11):  # Парсим 10 страниц
        url = base_url.format(page_num)
        print(f"📄 Парсинг страницы {page_num}...")

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Генерирует исключение, если статус-код не 200
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при подключении к {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            quotes_data.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        time.sleep(1)  # Пауза, чтобы не нагружать сайт

    return quotes_data

def insert_quotes_to_db(quotes_data):
    conn = sqlite3.connect('quotes.db')
    cur = conn.cursor()

    # Создание таблиц, если их ещё нет
    cur.execute('''CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        author_id INTEGER,
        FOREIGN KEY(author_id) REFERENCES authors(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS quote_tag (
        quote_id INTEGER,
        tag_id INTEGER,
        UNIQUE (quote_id, tag_id),
        FOREIGN KEY(quote_id) REFERENCES quotes(id),
        FOREIGN KEY(tag_id) REFERENCES tags(id)
    )''')

    for data in quotes_data:
        # Вставляем автора
        cur.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (data['author'],))
        cur.execute("SELECT id FROM authors WHERE name = ?", (data['author'],))
        author_id = cur.fetchone()[0]

        # Вставляем цитату
        cur.execute("INSERT INTO quotes (text, author_id) VALUES (?, ?)", (data['text'], author_id))
        quote_id = cur.lastrowid

        # Вставляем теги и связи
        for tag in data['tags']:
            cur.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
            cur.execute("SELECT id FROM tags WHERE name = ?", (tag,))
            tag_id = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO quote_tag (quote_id, tag_id) VALUES (?, ?)", (quote_id, tag_id))

    conn.commit()
    conn.close()
    print("✅ Данные успешно сохранены в базу данных.")

if __name__ == '__main__':
    print("🚀 Начинаем парсинг...")
    quotes_data = get_quotes()
    print(f"🔍 Получено {len(quotes_data)} цитат. Сохраняем в базу данных...")
    insert_quotes_to_db(quotes_data)
