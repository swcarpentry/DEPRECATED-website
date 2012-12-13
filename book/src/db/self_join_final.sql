SELECT DISTINCT a.PersonID
FROM            Experiments a JOIN Experiments b
WHERE           (a.PersonID = b.PersonID) AND (a.Project != b.Project)
ORDER BY        a.PersonID ASC;
