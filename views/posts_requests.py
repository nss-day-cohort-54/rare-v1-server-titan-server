from pickle import FALSE
import sqlite3
import json
from models import Post, Categories, User


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
            
        from Posts p
        Join Categories c
            ON c.id = p.category_id
        Join Users u
            on u.id = p.user_id
        ORDER BY p.publication_date DESC
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            category = Categories(
                row['id'], row['label']
            )

            post.category = category.__dict__

            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])

            post.user = user.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)

def get_user_posts(user_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
            
        from Posts p
        Join Categories c
            ON c.id = p.category_id
        Join Users u
            on u.id = p.user_id
        Where u.id = ?
        """, ( user_id, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            category = Categories(
                row['id'], row['label']
            )

            post.category = category.__dict__

            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])

            post.user = user.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)


def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
            
        from Posts p
        Join Categories c
            ON c.id = p.category_id
        Join Users u
            on u.id = p.user_id
            WHERE p.id = ?
            """, (id,))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                    data['publication_date'], data['image_url'], data['content'], data['approved'])

        category = Categories(
            data['id'], data['label']
        )

        post.category = category.__dict__

        user = User(data['id'], data['first_name'], data['last_name'], data['email'], data['bio'],
                    data['username'], data['password'], data['profile_image_url'], data['created_on'], data['active'])

        post.user = user.__dict__

        return json.dumps(post.__dict__)


def create_post(new_post):
    """create new post"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        conn.row_factory = sqlite3.Row

        db_cursor.execute("""
        INSERT INTO Posts ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES ( ?, ?, ?, ?, ?, ?, ? )
        """, (new_post['userId'], new_post['categoryId'], new_post['title'],
              new_post['publicationDate'], new_post['imageURL'], new_post['content'], new_post['approved']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id

    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id,))
        


def update_post(id, new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            UPDATE Posts
                SET
                    category_id = ?,
                    title = ?,
                    image_url = ?,
                    content = ?,
                    approved =?
            WHERE id = ?
            """, (new_post['categoryId'], new_post['title'], new_post['imageURL'], new_post['content'], new_post['approved'], id, ))
        
        rows_affected = db_cursor.rowcount
        
        if rows_affected == 0:
            return False
        else:
            return True
