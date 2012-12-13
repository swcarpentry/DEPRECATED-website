CREATE TABLE JustEmail(PersonID TEXT, Email TEXT);
INSERT INTO JustEmail SELECT PersonId, Email FROM Scientists;
