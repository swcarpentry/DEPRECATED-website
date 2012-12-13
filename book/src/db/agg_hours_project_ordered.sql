SELECT   Project, SUM(Hours) FROM Experiments
GROUP BY Project
ORDER BY Project ASC;
