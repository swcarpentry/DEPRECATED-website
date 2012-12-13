-- $Id: create-null-table.sql 1825 2011-04-27 18:26:27Z gvw $
-- Create the double-table database used in databases.html#s:databases:select

CREATE TABLE Experiments(PersonID TEXT, Project TEXT, Hours REAL);
INSERT INTO Experiments VALUES("skol", "Antigravity", 6.5);
INSERT INTO Experiments VALUES("skol", "Teleportation", NULL);
INSERT INTO Experiments VALUES("skol", "Teleportation", 5.0);
INSERT INTO Experiments VALUES("mlom", "Antigravity", 4.0);
INSERT INTO Experiments VALUES("mlom", "Time Travel", NULL);
INSERT INTO Experiments VALUES("dmen", "Antigravity", 9.0);
INSERT INTO Experiments VALUES("ipav", "Teleportation", 9.0);
INSERT INTO Experiments VALUES("ipav", "Time Travel", NULL);
