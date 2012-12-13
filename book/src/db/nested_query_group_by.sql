SELECT   PersonID, COUNT(*)
FROM     (SELECT DISTINCT PersonID, Project FROM Experiments)
GROUP BY PersonID;
