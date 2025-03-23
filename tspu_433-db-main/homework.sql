
CREATE TABLE IF NOT EXISTS albums (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(255),
description TEXT,
`year` INTEGER
);

CREATE TABLE IF NOT EXISTS authors (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS songs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(255),
duration INT(3),
album_id INTEGER,
FOREIGN KEY (album_id) REFERENCES albums(id)
);

CREATE TABLE IF NOT EXISTS song_authors (
song_id INTEGER,
author_id INTEGER,
PRIMARY KEY (song_id, author_id),
FOREIGN KEY (song_id) REFERENCES songs(id),
FOREIGN KEY (author_id) REFERENCES authors(id)
);


INSERT INTO albums (title, description, `year`) VALUES
('Album 1', 'First album', 2020),
('Album 2', 'Second album', 2021);


INSERT INTO authors (name) VALUES
('Author 1'),
('Author 2');


INSERT INTO songs (title, duration, album_id) VALUES
('Song 1', 200, 1),
('Song 2', 180, 1),
('Song 3', 220, 1),
('Song 4', 190, 1),
('Song 5', 210, 1),
('Song 6', 230, 2),
('Song 7', 240, 2),
('Song 8', 250, 2),
('Song 9', 260, 2),
('Song 10', 270, 2);


INSERT INTO song_authors (song_id, author_id) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 2),
(7, 2),
(8, 2),
(9, 2),
(10, 2);
