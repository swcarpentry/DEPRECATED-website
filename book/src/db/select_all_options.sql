SELECT   *, ROUND(0.1 * Hours, 1)
FROM     Experiments
WHERE    Hours > 3
ORDER BY Project DESC;
