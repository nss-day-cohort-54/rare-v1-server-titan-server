import sqlite3
import json
from models import Tag

def get_all_tags():
    """get all tags"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        ORDER BY label
        """)

        tags = []

        dataset = db_cursor.fetchall()
        for row in dataset:
            tag = Tag(row['id'], row['label'])
            tags.append(tag.__dict__)

    return json.dumps(tags)

def get_single_tag(id):
    """get single tag"""
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE t.id = ?
        """, (id,))

        data = db_cursor.fetchone()
        tag = Tag(data['id'], data['label'])

        return json.dumps(tag.__dict__)