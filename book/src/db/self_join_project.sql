SELECT * FROM Experiments a JOIN Experiments b
WHERE (a.PersonID = b.PersonID) AND (a.Project != b.Project);
