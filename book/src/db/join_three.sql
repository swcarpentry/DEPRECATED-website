SELECT Scientists.PersonalName, Scientists.FamilyName, Papers.Title
FROM   Scientists JOIN Authors JOIN Papers
ON     (Scientists.PersonID = Authors.PersonID) AND (Authors.CiteKey = Papers.CiteKey);
