SELECT   Project, SUM(Hours) FROM Experiments
WHERE    Hours >= 0
GROUP BY Project
ORDER BY SUM(Hours) ASC;
