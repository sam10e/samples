USE testBYUathletics;

CREATE TABLE nbaInjuryTest (
	injuryID INT PRIMARY KEY auto_increment,
    playerID VARCHAR(25),
    season YEAR NOT NULL,
    injuryDate DATE NOT NULL, 
    returnDate DATE,
    side VARCHAR(5),
    bodyPart VARCHAR(30) NOT NULL,
    description VARCHAR(255),
    occurrence VARCHAR(100),
    surgery VARCHAR(3),
    seasonEnding VARCHAR(3),
    rest INT,
    gamesMissed INT,
    minutesPrior INT,
    severity VARCHAR(100),
    surgeryDate DATE,
	FOREIGN KEY(playerID) REFERENCES nbaProfile(id)
);