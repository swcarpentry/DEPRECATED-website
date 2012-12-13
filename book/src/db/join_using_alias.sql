SELECT DISTINCT e.Project, s.Email
FROM            Experiments e JOIN Scientists s
ON              e.PersonID = s.PersonID;
