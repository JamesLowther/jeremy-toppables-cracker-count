DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Images;
DROP TABLE IF EXISTS Scans;

PRAGMA foreign_keys = ON;

CREATE TABLE Posts (
    uuid        text,
    title       text,
    updated_at  text,
    url         text,
    html        text,
    scanned     integer,
    PRIMARY KEY (uuid)
);

CREATE TABLE Images (
    image_path  text,
    uuid        text,
    image_order integer,
    PRIMARY KEY (image_path),
    FOREIGN KEY (uuid) REFERENCES Posts
);

CREATE TABLE Scans (
    scan_path   text,
    uuid        text,
    image_path  text,
    scan_order  integer,
    version     integer,
    PRIMARY KEY (scan_path),
    FOREIGN KEY (uuid) REFERENCES Posts,
    FOREIGN KEY (image_path) REFERENCES Images
);
