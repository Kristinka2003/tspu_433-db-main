import sqlite3
from typing import List, Tuple

DB_PATH = "quotes_books_db.sqlite3"

def get_by_tags(tags: List[str]) -> List[Tuple[str, str]]:
    if not tags:
        return []
    placeholders = ','.join(['?'] * len(tags))
    query = f"""
        SELECT DISTINCT q.text, a.name
        FROM quotes q
        JOIN authors a ON q.author_id = a.id
        JOIN quote_tag qt ON q.id = qt.quote_id
        JOIN tags t ON t.id = qt.tag_id
        WHERE t.name IN ({placeholders})
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(query, tags)
        return cur.fetchall()

def get_by_authors(authors: List[str]) -> List[Tuple[str, str]]:
    if not authors:
        return []
    placeholders = ','.join(['?'] * len(authors))
    query = f"""
        SELECT q.text, a.name
        FROM quotes q
        JOIN authors a ON q.author_id = a.id
        WHERE a.name IN ({placeholders})
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(query, authors)
        return cur.fetchall()

