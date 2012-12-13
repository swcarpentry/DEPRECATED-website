UPDATE Experiments
  SET Hours = 3.0 + (SELECT Hours FROM Experiments WHERE PersonID = "mlom" and Project = "Antigravity")
WHERE PersonID = "mlom" and Project = "Antigravity";
