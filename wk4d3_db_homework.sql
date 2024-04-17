CREATE DATABASE fitness_tracker;

USE fitness_tracker;

CREATE TABLE Members (
    member_id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    bench_amount INT,
    membership_type VARCHAR(30)
); 

CREATE TABLE Dank_sesh (
    sesh_id INT AUTO_INCREMENT PRIMARY KEY, 
    date DATE, 
    member_id INT,
    workout_type VARCHAR(50),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

INSERT INTO Members (name, email, phone, bench_amount, membership_type)
VALUES 
    ("Goku", "sonofgoku@gmail.com", "6309875677", 9001, "Platinum Enhanced Gravity"),
    ("Vegeta", "princevegeta@gmail.com", "6309875678", 8500, "Royal Saiyan"),
    ("Frieza", "frieza@gmail.com", "6309875679", 8000, "Galactic Emperor"),
    ("Majin Buu", "majinbuu@gmail.com", "6309875680", 7500, "Pink Terror"),
    ("Trunks", "trunks@gmail.com", "6309875681", 8500, "Future Warrior"),
    ("Cell", "cell@gmail.com", "6309875682", 9000, "Perfect Being");

INSERT INTO Dank_sesh (date, member_id, workout_type)
VALUES ("2024-04-10", 1, "Strength"),
       ("2024-04-11", 2, "Powerlifting"),
       ("2024-04-13", 1, "Power Level Testing"),
       ("2024-04-14", 2, "Chocolate Eating Contest"),
       ("2024-04-12", 3, "Sword Training"),
       ("2024-04-15", 4, "Cell Games");
SELECT *
FROM Dank_sesh;

SELECT *
FROM Members;




