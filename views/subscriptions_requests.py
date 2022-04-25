import sqlite3
import json
from models import Subscription

def create_subscription(new_subscription):
    """create new subscription"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        conn.row_factory = sqlite3.Row

        db_cursor.execute("""
        INSERT INTO Subscriptions ( follower_id, author_id, created_on )
        VALUES ( ?, ?, ? )
        """, (new_subscription['followerId'], new_subscription['authorId'], new_subscription['createdOn']))

        id = db_cursor.lastrowid
        new_subscription['id'] = id

    return json.dumps(new_subscription)

def get_all_subscriptions():
    """get all subscriptions"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
        FROM Subscriptions s
        """)

        subscriptions = []

        dataset = db_cursor.fetchall()
        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            subscriptions.append(subscription.__dict__)

    return json.dumps(subscriptions)


def delete_subscription(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM subscriptions
        WHERE id = ?
        """, (id, ))
