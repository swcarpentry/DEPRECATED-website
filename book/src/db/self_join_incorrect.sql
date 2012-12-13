SELECT PersonID, COUNT(*) FROM Experiments GROUP BY PersonID WHERE COUNT(*) > 1;
