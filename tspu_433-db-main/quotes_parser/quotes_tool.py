import sqlite3
from typing import List, Optional

DATABASE_NAME = r"C:\Users\Succubus\Downloads\tspu_433-db-main\tspu_433-db-main\quotes_parser\quotes_books_db.sqlite3"


def get_by_tags(tags: Optional[List[str]] = None) -> List[dict]:
    """
    Получение цитат по тегам.
    """
    if not tags:
        return []

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    placeholders = ', '.join(['?'] * len(tags))
    query = f"""
    SELECT quotes.id, quotes.text, authors.name
    FROM quotes
    JOIN quote_tag ON quotes.id = quote_tag.quote_id
    JOIN tags ON quote_tag.tag_id = tags.id
    JOIN authors ON quotes.author_id = authors.id
    WHERE tags.name IN ({placeholders})
    """

    cursor.execute(query, tags)
    results = cursor.fetchall()
    conn.close()

    return [{'id': row[0], 'text': row[1], 'author_name': row[2]} for row in results]


def get_by_authors(authors: Optional[List[str]] = None) -> List[dict]:
    """
    Получение цитат по авторам.
    """
    if not authors:
        return []

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    placeholders = ', '.join(['?'] * len(authors))
    query = f"""
    SELECT quotes.id, quotes.text, authors.name
    FROM quotes
    JOIN authors ON quotes.author_id = authors.id
    WHERE authors.name IN ({placeholders})
    """

    cursor.execute(query, authors)
    results = cursor.fetchall()
    conn.close()

    return [{'id': row[0], 'text': row[1], 'author_name': row[2]} for row in results]


def get_author_count_quotes(author: Optional[str] = None) -> int:
    """
    Получение количества цитат автора.
    """
    if not author:
        return 0

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM quotes
    JOIN authors ON quotes.author_id = authors.id
    WHERE authors.name = ?
    """

    cursor.execute(query, (author,))
    count = cursor.fetchone()[0]
    conn.close()

    return count


def get_top_authors(limit: int = 5) -> List[dict]:
    """
    Список топ авторов по количеству цитат.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = """
    SELECT authors.id, authors.name, COUNT(quotes.id) AS quote_count
    FROM authors
    LEFT JOIN quotes ON authors.id = quotes.author_id
    GROUP BY authors.id
    ORDER BY quote_count DESC
    LIMIT ?
    """

    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    conn.close()

    return [{'id': row[0], 'name': row[1], 'quote_count': row[2]} for row in results]


def get_top_tags(limit: int = 5) -> List[dict]:
    """
    Список топ тегов по количеству упоминаний.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = """
    SELECT tags.id, tags.name, COUNT(quote_tag.quote_id) AS tag_count
    FROM tags
    LEFT JOIN quote_tag ON tags.id = quote_tag.tag_id
    GROUP BY tags.id
    ORDER BY tag_count DESC
    LIMIT ?
    """

    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    conn.close()

    return [{'id': row[0], 'name': row[1], 'tag_count': row[2]} for row in results]


def get_author_tags(author: Optional[str] = None) -> List[dict]:
    """
    Список тегов, использованных автором.
    """
    if not author:
        return []

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = """
    SELECT DISTINCT tags.id, tags.name
    FROM tags
    JOIN quote_tag ON tags.id = quote_tag.tag_id
    JOIN quotes ON quote_tag.quote_id = quotes.id
    JOIN authors ON quotes.author_id = authors.id
    WHERE authors.name = ?
    """

    cursor.execute(query, (author,))
    results = cursor.fetchall()
    conn.close()

    return [{'id': row[0], 'name': row[1]} for row in results]


# Примеры вызова
if __name__ == '__main__':
    tags_example = ['life', 'love']
    authors_example = ['Albert Einstein', 'Jane Austen']
    single_author = 'Albert Einstein'

    print("Цитаты по тегам:", get_by_tags(tags_example))
    print("Цитаты по авторам:", get_by_authors(authors_example))
    print(f"Количество цитат у {single_author}:", get_author_count_quotes(single_author))
    print("Топ авторов:", get_top_authors(limit=3))
    print("Топ тегов:", get_top_tags(limit=3))
    print(f"Теги, используемые автором {single_author}:", get_author_tags(single_author))

