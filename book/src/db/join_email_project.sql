SELECT DISTINCT Experiments.Project, Scientists.Email
FROM            Scientists JOIN Experiments
ON              Scientists.PersonID = Experiments.PersonID;
