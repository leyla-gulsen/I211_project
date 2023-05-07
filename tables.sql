DROP TABLE IF EXISTS trip_members;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS members;

CREATE TABLE trips (
    trip_id INT PRIMARY KEY AUTO_INCREMENT,
    trip_name VARCHAR(50),
    level VARCHAR(15),
    start_date DATE,
    location VARCHAR(50),
    length INT,
    leader VARCHAR(255),
    cost INT,
    description TEXT
) ENGINE INNODB AUTO_INCREMENT=1;

CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    fname VARCHAR(20),
    lname VARCHAR(20),
    address VARCHAR(50),
    email VARCHAR(25),
    phone VARCHAR(12),
    dob DATE
) ENGINE INNODB AUTO_INCREMENT=100;

CREATE TABLE trip_members (
    trip_id INT,
    member_id INT,
    PRIMARY KEY (trip_id, member_id),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
) ENGINE INNODB;

INSERT INTO trips (trip_name, level, start_date, location, length, leader, cost, description)
VALUES
('Hot-Air Ballooning','Beginner','2023-06-15','Cappadocia',2,'Emre Kaya',500,'A standard hot-air balloon experience here includes hotel, pickup and drop-off (from hotels across the Cappadocia village region) and breakfast.'),
('Hike the Lycian Way','Intermediate','2023-05-09','Antalya',1,'Aylin Aksoy',30,'Turkeys most famous long-distance walking trail (540-kilometer length) winds along the Mediterranean Coast from Fethiye down to Antalya.'),
('Explore Ephesus','Beginner','2023-06-23','Selçuk',1,'Tolga Demir',20,'One of the worlds best preserved Roman ruins, Ephesus was once home to a population of approximately 250,000 and was capital of Asia Minor in the regions Roman era.'),
('Yacht Cruising','Beginner','2023-07-16','Fethiye',3,'Elif Yilmaz',100,'This trip takes three nights to sail along the coastline from Fethiye to Olympos, with stops at Butterfly Valley, Gemiler (St. Nicholas) Island, Kaş, and the Kekova Island area.'),
('Kayaking at Kekova','Advanced','2023-05-30','Uçağiz',1,'Baran Öztürk',50,'Skim along the Kekova Island shoreline to see the underwater Sunken City ruins. Cross the Kekova Strait to the village of Kaleköy to see the ruins of Ancient Simena, before paddling back along the coast to Uçağiz.'),
('Boating in Bodrum','Beginner','2023-07-03','Bodrum',4,'Dilara Şahin',350,'Cruise around Bodrum Bay, anchoring off islands for swimming between puttering along, admiring the craggy coastline of the Bodrum Peninsula with its hidden coves and lush forest.');

INSERT INTO members (fname, lname, address, email, phone, dob)
VALUES
('Aylin','Şahin','3121 Walnut St Ellettsville','aylin.sahin@hotmail.com','876-543-2735','1995-10-12'),
('Tolga','Yilmaz','4530 Park Blvd Indianapolis','tolga.demir@yahoo.com','321-098-7535','1982-2-5'),
('Elif','Demir','225 Main St Bloomington','elif.yilmaz@outlook.com','987-654-3210','1990-9-19'),
('Dilara','Kaya','1507 S King St Indianapoolis','dilara.kaya@gmail.com','908-734-1840','1985-12-31'),
('Deniz','Gulsen','1017 Olive St Ellettsville','deniz.gulsen@yahoo.com','432-950-5942','1993-9-8'),
('Cemal','Akin','6785 Elmwood Ave Bloomington','cemal.akin@gmail.com','210-987-6435','1989-5-23');

INSERT INTO trip_members (trip_id, member_id)
VALUES
(1,100),
(1,102),
(1,104),
(2,101),
(2,103),
(2,105),
(3,100),
(3,102),
(4,102),
(4,104),
(5,101),
(5,103),
(6,103),
(6,105);