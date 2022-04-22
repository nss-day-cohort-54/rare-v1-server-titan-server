import sqlite3
import json
from models import User

def get_all_users():
    """get all users"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.email,
            u.first_name,
            u.last_name,
            u.username
        FROM Users u
        ORDER BY username
        """)

        users = []

        dataset = db_cursor.fetchall()
        for row in dataset:
            user = User(row['id'], row['first_name'], row['last_name'], row['email'], "null", row['username'], "null", "null", "null", "null")
            users.append(user.__dict__)

    return json.dumps(users)

def get_single_user(id):
    """get single user"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
        FROM Users
        WHERE id = ?
        """, (id, ))

        data = db_cursor.fetchone()
        user = User(data['id'], data['first_name'], data['last_name'], data['email'], data['bio'], data['username'], data['password'], data['profile_image_url'], data['created_on'], data['active'])

    return json.dumps(user.__dict__)

