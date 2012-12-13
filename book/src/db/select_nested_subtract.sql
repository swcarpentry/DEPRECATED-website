SELECT DISTINCT PersonID FROM Experiments WHERE PersonID NOT IN
       (SELECT DISTINCT PersonID FROM Experiments WHERE Project = "Time Travel");
