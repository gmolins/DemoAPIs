-- Drop tables if they already exist
DROP TABLE IF EXISTS entry;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS "user";

-- Create the author table
CREATE TABLE author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Create the entry table
CREATE TABLE entry (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author (id) ON DELETE CASCADE
);

-- Create the user table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

-- Insert sample data into the author table
INSERT INTO author (name, email) VALUES
('Author One', 'author1@example.com'),
('Author Two', 'author2@example.com');

-- Insert sample data into the entry table
INSERT INTO entry (title, content, author_id) VALUES
('Entry One', 'Content for entry one', 1),
('Entry Two', 'Content for entry two', 2),
('Entry Three', 'Content for entry three', 1);

-- Insert sample data into the user table
INSERT INTO "user" (username, email, hashed_password) VALUES
('user1', 'user1@example.com', '$2b$12$examplehashedpassword1'),
('user2', 'user2@example.com', '$2b$12$examplehashedpassword2');

-- Query to fetch all authors
SELECT * FROM author;

-- Query to fetch all entries
SELECT * FROM entry;

-- Query to fetch entries by a specific author
SELECT entry.* 
FROM entry
JOIN author ON entry.author_id = author.id
WHERE author.name = 'Author One';

-- Query to delete an author by ID
DELETE FROM author WHERE id = 1;

-- Query to update an entry's title
UPDATE entry
SET title = 'Updated Entry Title'
WHERE id = 1;
