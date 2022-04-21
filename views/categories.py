import sqlite3
import json
from models import Categories, categories


def get_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            ca.id,
            ca.label
        FROM Categories AS ca
        ORDER BY ca.label ASC
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            cat = Categories(row['id'], row['label'])

            categories.append(cat.__dict__)

    return json.dumps(categories)


def get_single_category(id):
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            ca.id,
            ca.label
            FROM Categories AS ca
            WHERE ca.id = ?
            """, (id,))

        data = db_cursor.fetchone()

        categories = Categories(data['id'], data['label'])

        return json.dumps(categories.__dict__)
