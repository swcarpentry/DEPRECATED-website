-- $Id: create-halved-table.sql 1832 2011-04-28 15:49:25Z gvw $
-- Create the single-table database used in databases.html#s:databases:select

CREATE TABLE Experiments(PersonalName TEXT, FamilyName TEXT, Project TEXT, Hours REAL);
INSERT INTO Experiments VALUES("Sofia", "Kovalevskaya", "Antigravity", 6.5);
INSERT INTO Experiments VALUES("Sofia", "Kovalevskaya", "Teleportation", 11.0);
INSERT INTO Experiments VALUES("Sofia", "Kovalevskaya", "Teleportation", 5.0);
INSERT INTO Experiments VALUES("Mikhail", "Lomonosov", "Antigravity", 4.0);
INSERT INTO Experiments VALUES("Mikhail", "Lomonosov", "Time Travel", -2.0);
INSERT INTO Experiments VALUES("Dmitri", "Mendeleev", "Antigravity", 9.0);
INSERT INTO Experiments VALUES("Ivan", "Pavlov", "Teleportation", 9.0);
INSERT INTO Experiments VALUES("Ivan", "Pavlov", "Time Travel", -7.0);
