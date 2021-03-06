CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

Insert into Subscriptions (follower_id, author_id, created_on)
Values (1, 1, "");
Insert into Subscriptions (follower_id, author_id, created_on)
Values (1, 2, "");
Insert into Subscriptions (follower_id, author_id, created_on)
Values (2, 2, "");


CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Categories ('label') VALUES ('Sport');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Tags ('label') VALUES ('Python');
INSERT INTO Tags ('label') VALUES ('SQL');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date' ,'image_url', 'content', 'approved') VALUES (1, 1, 'Test Title', 0420222, 'https://i.kym-cdn.com/entries/icons/facebook/000/013/564/doge.jpg', 'this is a test of the post system', 1 );
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date' ,'image_url', 'content', 'approved') VALUES (1, 1, 'Test Title 2', 0420222, 'https://i.kym-cdn.com/entries/icons/facebook/000/013/564/doge.jpg', 'this is a test of the post system', 1 );

INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date' ,'image_url', 'content', 'approved') VALUES (1, 1, 1, 'Test Title', 0420222, 'https://i.kym-cdn.com/entries/icons/facebook/000/013/564/doge.jpg', 'this is a test of the post system', 1 );

DELETE FROM Tags
WHERE id > 3;


INSERT INTO Categories ('label') VALUES ('Sports');
INSERT INTO Categories ('label') VALUES ('Music');
INSERT INTO Categories ('label') VALUES ('Alchemy');
INSERT INTO Categories ('label') VALUES ('Whiskey');
INSERT INTO Categories ('label') VALUES ('Legos');
SELECT
            ca.id,
            ca.label
        FROM Categories AS ca
        ORDER BY ca.label ASC;


SELECT *
        from Comments c
        Join Users u
            on u.id = c.author_id
        Join Posts p
          on p.id = c.post_id;

DELETE FROM Subscriptions
WHERE id =20;

drop table Subscriptions;

update posts
set category_id = 2
where id in (1,5);
          on p.id = c.post_id


INSERT INTO PostTags ('post_id', 'tag_id' ) VALUES (1,1);
INSERT INTO PostTags ('post_id', 'tag_id' ) VALUES (1,2);
INSERT INTO PostTags ('post_id', 'tag_id' ) VALUES (3,1);

SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.label content_label,
            u.first_name,
            u.last_name,
            u.username,
            t.id,
            t.label tag_label

            
        from Posts p
        Join Categories c
            ON c.id = p.category_id
        Join Users u
            on u.id = p.user_id
        Join PostTags pt
            on pt.post_id = p.id
        Join Tags t
            on t.id = pt.tag_id
        Where t.id = 1

SELECT *
FROM Posts p
JOIN Users u ON u.id = p.user_id
JOIN Subscriptions s ON s.follower_id = p.user_id