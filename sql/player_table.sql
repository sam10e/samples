USE testBYUathletics;

CREATE TABLE nbaProfileTest (
	id VARCHAR(9) PRIMARY KEY NOT NULL,
	firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    height VARCHAR(10) NOT NULL,
    weight INT NOT NULL,
	positions VARCHAR(10) NOT NULL,
    shootingHand VARCHAR(10) NOT NULL,
    birthDate VARCHAR(20),
    birthPlace VARCHAR(100),
    college VARCHAR(200),
    highSchool VARCHAR(200),
    race VARCHAR(30),
    draftYear INT,
    draftNum INT
);
