SELECT   Scientist, Project, SUM(Hours)
FROM     Experiments
GROUP BY Scientist, Project;
