import sqlite3
import json
from models import Comments, User, Post

def get_comments_per_post(postId):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT 
        *
        
        
        from Comments c
        Join Users u
            on u.id = c.author_id
        WHERE c.post_id = ?
        """, (postId, ))
        
    comments = []
    
    dataset = db_cursor.fetchall()
    
    for row in dataset:
        comment = Comments(row['id'], row['post_id'], row['author_id'], row['content'])
        
        
        user = User(row['author_id'], row['first_name'], row['last_name'], row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])

        comment.author = user.__dict__
        
        comments.append(comment.__dict__)
        
    return json.dumps(comments)

def delete_comment(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id,))
        
def create_comment(new_comment):
    """create new comment"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        conn.row_factory = sqlite3.Row
        
        db_cursor.execute("""
        INSERT INTO comments (post_id, author_id, content)
        VALUES ( ?, ?, ?)
        """, (new_comment['postId'], new_comment['authorId'], new_comment['content']))
        
        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid
        
        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id
        
    return json.dumps(new_comment)
