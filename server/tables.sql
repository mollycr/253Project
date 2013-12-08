DROP TABLE IF EXISTS User;
CREATE TABLE User(username VARCHAR(32), email VARCHAR(128), hash CHAR(60));
DROP TABLE IF EXISTS Urls;
CREATE TABLE Urls(url VARCHAR(256), short VARCHAR(32), timesVisited INTEGER, username VARCHAR(32),timeCreated timestamp);
DROP TABLE IF EXISTS Tags;
CREATE TABLE Tags(id INTEGER PRIMARY KEY, tag VARCHAR(256), short VARCHAR(32), FOREIGN KEY(short) REFERENCES Urls(short));

