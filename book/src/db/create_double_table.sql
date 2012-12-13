-- $Id: create-double-table.sql 1825 2011-04-27 18:26:27Z gvw $
-- Create the double-table database used in databases.html#s:databases:select

CREATE TABLE Experiments(PersonID TEXT, Project TEXT, Hours REAL);
INSERT INTO Experiments VALUES("skol", "Antigravity", 6.5);
INSERT INTO Experiments VALUES("skol", "Teleportation", 11.0);
INSERT INTO Experiments VALUES("skol", "Teleportation", 5.0);
INSERT INTO Experiments VALUES("mlom", "Antigravity", 4.0);
INSERT INTO Experiments VALUES("mlom", "Time Travel", -2.0);
INSERT INTO Experiments VALUES("dmen", "Antigravity", 9.0);
INSERT INTO Experiments VALUES("ipav", "Teleportation", 9.0);
INSERT INTO Experiments VALUES("ipav", "Time Travel", -7.0);

CREATE TABLE Scientists(PersonID TEXT, FamilyName TEXT, PersonalName TEXT, Email TEXT);
INSERT INTO Scientists VALUES("skol", "Kovalevskaya", "Sofia", "skol@euphoric.edu");
INSERT INTO Scientists VALUES("mlom", "Lomonosov", "Mikhail", "mikki@freesci.org");
INSERT INTO Scientists VALUES("dmen", "Mendeleev", "Dmitri", "mendeleev@euphoric.edu");
INSERT INTO Scientists VALUES("ipav", "Pavlov", "Ivan", "pablum@euphoric.edu");
