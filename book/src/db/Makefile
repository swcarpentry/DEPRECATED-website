select-scientist-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, Hours FROM Experiments;') \
	| sqlite3 :memory:

select-scientist-hours-project :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, Hours, Project FROM Experiments;') \
	| sqlite3 :memory:

select-project-scientist-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT Project, Scientist, Hours FROM Experiments;') \
	| sqlite3 :memory:

select-project-project :
	@(cat create-single-table.sql; \
	echo 'SELECT Project, Project FROM Experiments;') \
	| sqlite3 :memory:

select-star :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments;') \
	| sqlite3 :memory:

select-project :
	@(cat create-single-table.sql; \
	echo 'SELECT Project FROM Experiments;') \
	| sqlite3 :memory:

select-distinct-project :
	@(cat create-single-table.sql; \
	echo 'SELECT DISTINCT Project FROM Experiments;') \
	| sqlite3 :memory:

select-distinct-project-scientist :
	@(cat create-single-table.sql; \
	echo 'SELECT DISTINCT Project, Scientist FROM Experiments;') \
	| sqlite3 :memory:

select-simple-formula :
	@(cat create-single-table.sql; \
	echo 'SELECT *, 0.1 * Hours FROM Experiments;') \
	| sqlite3 :memory:

select-scientist-formula :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, ROUND(0.1 * Hours, 1) FROM Experiments;') \
	| sqlite3 :memory:

select-where-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT * From Experiments WHERE Hours > 2.0;') \
	| sqlite3 :memory:

select-where-pavlov :
	@(cat create-single-table.sql; \
	echo 'SELECT * From Experiments WHERE Scientist = "Ivan Pavlov";') \
	| sqlite3 :memory:

select-where-lomonosov-three-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments WHERE (Hours > 3) AND (Scientist = "Mikhail Lomonosov");') \
	| sqlite3 :memory:

select-where-lomonosov-or-pavlov :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments WHERE (Scientist = "Mikhail Lomonosov") OR (Scientist = "Ivan Pavlov");') \
	| sqlite3 :memory:

select-where-lomonosov-or-pavlov-three-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments WHERE (Hours > 3) AND ((Scientist = "Mikhail Lomonosov") OR (Scientist = "Ivan Pavlov"));') \
	| sqlite3 :memory:

select-where-badly-grouped :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments WHERE ((Hours > 3) AND (Scientist = "Mikhail Lomonosov")) OR (Scientist = "Ivan Pavlov");') \
	| sqlite3 :memory:

select-where-unparenthesized :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments WHERE Hours > 3 AND Scientist = "Mikhail Lomonosov" OR Scientist = "Ivan Pavlov";') \
	| sqlite3 :memory:

select-where-using-in :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments WHERE (Hours > 3) AND (Scientist IN ("Mikhail Lomonosov", "Ivan Pavlov"));') \
	| sqlite3 :memory:

select-order-project-asc :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments ORDER BY Project ASC;') \

select-order-project-desc :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments ORDER BY Project DESC;') \
	| sqlite3 :memory:

select-order-multiple :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments ORDER BY Project ASC, Scientist DESC;') \
	| sqlite3 :memory:

select-random :
	@(cat create-single-table.sql; \
	echo 'SELECT RANDOM() FROM Experiments;') \
	| sqlite3 :memory:

select-order-random :
	@(cat create-single-table.sql; \
	echo 'SELECT * FROM Experiments ORDER BY RANDOM();') \
	| sqlite3 :memory:

select-order-project-display-scientist-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT  Scientist, Hours FROM Experiments ORDER BY Project;') \
	| sqlite3 :memory:

select-all-options :
	@(cat create-single-table.sql; \
	echo 'SELECT *, ROUND(0.1 * Hours, 1) FROM Experiments WHERE Hours > 3 ORDER BY Project DESC;') \
	| sqlite3 :memory:

agg-sum-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT SUM(Hours) FROM Experiments;') \

agg-functions-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT SUM(Hours), MAX(Hours), MIN(Hours), AVG(Hours) FROM Experiments;') \
	| sqlite3 :memory:

agg-count-hours :
	@(cat create-single-table.sql; \
	echo 'SELECT COUNT(Hours) FROM Experiments;') \
	| sqlite3 :memory:

agg-hours-mendeleev :
	@(cat create-single-table.sql; \
	echo 'SELECT SUM(Hours) FROM Experiments WHERE Scientist = "Dmitri Mendeleev";') \
	| sqlite3 :memory:

agg-per-scientist-wrong :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, SUM(Hours) FROM Experiments;') \
	| sqlite3 :memory:

group-by-scientist :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, Hours FROM Experiments GROUP BY Scientist;') \
	| sqlite3 :memory:

agg-sum-by-scientist :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, SUM(Hours) FROM Experiments GROUP BY Scientist;') \
	| sqlite3 :memory:

agg-sum-by-scientist-project :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, Project, SUM(Hours) FROM Experiments GROUP BY Scientist, Project;') \
	| sqlite3 :memory:

agg-count-scientist :
	@(cat create-single-table.sql; \
	echo 'SELECT Scientist, COUNT(*) FROM Experiments GROUP BY Scientist;') \
	| sqlite3 :memory:

agg-hours-project-ordered :
	@(cat create-single-table.sql; \
	echo 'SELECT Project, SUM(Hours) FROM Experiments GROUP BY Project ORDER BY Project ASC;') \
	| sqlite3 :memory:

agg-hours-order-agg :
	@(cat create-single-table.sql; \
	echo 'SELECT Project, SUM(Hours) FROM Experiments GROUP BY Project ORDER BY SUM(Hours) ASC;') \
	| sqlite3 :memory:

agg-hours-positive :
	@(cat create-single-table.sql; \
	echo 'SELECT Project, SUM(Hours) FROM Experiments WHERE Hours >= 0 GROUP BY Project ORDER BY SUM(Hours) ASC;') \
	| sqlite3 :memory:

select-distinct-names :
	@(cat create-halved-table.sql; \
	echo 'SELECT DISTINCT FamilyName || ", " || PersonalName FROM Experiments;') \
	| sqlite3 :memory:

select-rowid :
	@(cat create-double-table.sql; \
	echo 'SELECT ROWID, * FROM Experiments;') \
	| sqlite3 :memory:

join-scientists-experiments :
	@(cat create-double-table.sql; \
	echo 'SELECT * FROM Scientists JOIN Experiments;') \
	| sqlite3 :memory:

join-scientists-experiments-on :
	@(cat create-double-table.sql; \
	echo 'SELECT * FROM Scientists JOIN Experiments ON Scientists.PersonID = Experiments.PersonID;') \
	| sqlite3 :memory:

join-scientists-experiments-where :
	@(cat create-double-table.sql; \
	echo 'SELECT * FROM Scientists JOIN Experiments WHERE Scientists.PersonID = Experiments.PersonID;') \

join-email-project :
	@(cat create-double-table.sql; \
	echo 'SELECT DISTINCT Experiments.Project, Scientists.Email FROM Scientists JOIN Experiments ON Scientists.PersonID = Experiments.PersonID;') \
	| sqlite3 :memory:

join-using-alias :
	@(cat create-double-table.sql; \
	echo 'SELECT DISTINCT e.Project, s.Email FROM Experiments e JOIN Scientists s ON e.PersonID = s.PersonID;') \
	| sqlite3 :memory:

join-and-order :
	@(cat create-double-table.sql; \
	echo 'SELECT DISTINCT e.Project, s.Email FROM Experiments e JOIN Scientists s ON e.PersonID = s.PersonID ORDER BY e.Project, s.Email;') \
	| sqlite3 :memory:

join-three :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT Scientists.PersonalName, Scientists.FamilyName, Papers.Title FROM Scientists JOIN Authors JOIN Papers ON (Scientists.PersonID = Authors.PersonID) AND (Authors.CiteKey = Papers.CiteKey);') \
	| sqlite3 :memory:

self-join-all :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT * FROM Experiments a JOIN Experiments b;') \
	| sqlite3 :memory:

self-join-personid :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT * FROM Experiments a JOIN Experiments b WHERE a.PersonID = b.PersonID;') \
	| sqlite3 :memory:

self-join-project :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT * FROM Experiments a JOIN Experiments b WHERE (a.PersonID = b.PersonID) AND (a.Project != b.Project);') \
	| sqlite3 :memory:

self-join-final :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT DISTINCT a.PersonID FROM Experiments a JOIN Experiments b WHERE (a.PersonID = b.PersonID) AND (a.Project != b.Project) ORDER BY a.PersonID ASC;') \
	| sqlite3 :memory:

select-null-equal-error :
	@(cat create-null-table.sql; \
	echo 'SELECT * FROM Experiments WHERE Hours = NULL;') \
	| sqlite3 :memory:

select-null-not-equal-error :
	@(cat create-null-table.sql; \
	echo 'SELECT * FROM Experiments WHERE Hours != NULL;') \
	| sqlite3 :memory:

select-null :
	@(cat create-null-table.sql; \
	echo 'SELECT * FROM Experiments WHERE Hours IS NULL;') \
	| sqlite3 :memory:

select-not-null :
	@(cat create-null-table.sql; \
	echo 'SELECT * FROM Experiments WHERE Hours IS NOT NULL;') \
	| sqlite3 :memory:

select-not-nine-hours :
	@(cat create-null-table.sql; \
	echo 'SELECT * FROM Experiments WHERE Hours != 9.0;') \
	| sqlite3 :memory:

select-not-nine-hours-keep-null :
	@(cat create-null-table.sql; \
	echo 'SELECT * FROM Experiments WHERE (Hours != 9.0) OR (Hours IS NULL);') \
	| sqlite3 :memory:

select-sum-hours-null :
	@(cat create-null-table.sql; \
	echo 'SELECT SUM(Hours) FROM Experiments;') \
	| sqlite3 :memory:

select-avg-hours-null :
	@(cat create-null-table.sql; \
	echo 'SELECT AVG(Hours) FROM Experiments;') \
	| sqlite3 :memory:

select-not-time-travel-flawed :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT DISTINCT PersonID FROM Experiments WHERE Project != "Time Travel";') \
	| sqlite3 :memory:

select-nested-subtract :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT DISTINCT PersonID FROM Experiments WHERE PersonID NOT IN (SELECT DISTINCT PersonID FROM Experiments WHERE Project = "Time Travel");') \
	| sqlite3 :memory:

select-nested-group-by :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT PersonID, COUNT(*) FROM (SELECT DISTINCT PersonID, Project FROM Experiments) GROUP BY PersonID;') \
	| sqlite3 :memory:

update-mlom-hours :
	@(cat create-quadruple-table.sql; \
	echo 'SELECT * FROM Experiments WHERE PersonID = "mlom" AND Project = "Antigravity";'; \
	echo 'UPDATE Experiments SET Hours = 3.0 + (SELECT Hours FROM Experiments WHERE PersonID = "mlom" and Project = "Antigravity") WHERE PersonID = "mlom" and Project = "Antigravity";'; \
	echo 'SELECT * FROM Experiments WHERE PersonID = "mlom" AND Project = "Antigravity";') \
	| sqlite3 :memory:

python-query :
	@rm -f lab.db
	@sqlite3 lab.db < create-quadruple-table.sql
	@python id-email.py
	@rm -f lab.db

python-prepared-statement :
	@rm -f lab.db
	@sqlite3 lab.db < create-quadruple-table.sql
	@echo 'mlom Antigravity' | python prepared-statement.py
	@rm -f lab.db
