-- C:\family_tree\schema.sql
DROP TABLE IF EXISTS persons;

CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    friends_name TEXT,
    image TEXT,
    father_id INTEGER,
    mother_id INTEGER,
    birth_date TEXT,
    death_date TEXT,
    birth_place TEXT,
    residence TEXT,
    external_link TEXT,
    image_url TEXT,
    mother TEXT,
    has_offspring BOOLEAN,
    alive BOOLEAN,
    death_reason TEXT,
    died_in_battle BOOLEAN,
    known_enemies TEXT,
    fitan TEXT,
    notes TEXT,
    photo_url TEXT,
    gender TEXT,
    FOREIGN KEY (father_id) REFERENCES persons(id) ON DELETE SET NULL,
    FOREIGN KEY (mother_id) REFERENCES persons(id) ON DELETE SET NULL
);

-- Grand-père 1
INSERT INTO persons (first_name, last_name, birth_date, birth_place) 
VALUES ('عبدالله', 'الفهيد', '1800-01-01', 'نجد');

-- Grand-père 2
INSERT INTO persons (first_name, last_name, birth_date, birth_place) 
VALUES ('محمد', 'السديري', '1805-01-01', 'الرياض');

-- Pères pour Grand-père 1 (3 fils)
INSERT INTO persons (first_name, last_name, father_id, birth_date, birth_place) 
VALUES 
('خالد', 'الفهيد', 1, '1825-01-01', 'الرياض'),
('علي', 'الفهيد', 1, '1830-01-01', 'الرياض'),
('فهد', 'الفهيد', 1, '1835-01-01', 'الرياض');

-- Pères pour Grand-père 2 (3 fils)
INSERT INTO persons (first_name, last_name, father_id, birth_date, birth_place) 
VALUES 
('سعود', 'السديري', 2, '1830-01-01', 'الخرج'),
('عبدالعزيز', 'السديري', 2, '1835-01-01', 'الخرج'),
('فيصل', 'السديري', 2, '1840-01-01', 'الخرج');

-- Fils pour chaque père (3 chacun)
-- Fils de خالد (id:3)
INSERT INTO persons (first_name, last_name, father_id, birth_date, birth_place) 
VALUES 
('نايف', 'الفهيد', 3, '1850-01-01', 'الرياض'),
('بندر', 'الفهيد', 3, '1855-01-01', 'الرياض'),
('تركي', 'الفهيد', 3, '1860-01-01', 'الرياض');

-- Fils de علي (id:4)
INSERT INTO persons (first_name, last_name, father_id, birth_date, birth_place) 
VALUES 
('عبدالرحمن', 'الفهيد', 4, '1855-01-01', 'الرياض'),
('مشعل', 'الفهيد', 4, '1860-01-01', 'الرياض'),
('سعد', 'الفهيد', 4, '1865-01-01', 'الرياض');