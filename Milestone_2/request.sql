SELECT G.name
FROM Brand_Group G
WHERE G.publisher_id IN 
			(SELECT I2.publisher_id
			 FROM Indicia_Publisher I2
			 WHERE I2.country_id = 20
			 GROUP BY I2.publisher_id
			 HAVING COUNT(*) >= 
			 	(SELECT MAX(counted) FROM (SELECT COUNT(I3.id) AS counted
										   FROM Indicia_Publisher I3
										   WHERE I3.country_id = 20
										   GROUP BY I3.publisher_id) AS counts));
										   
										   
SELECT DISTINCT(P.id), P.name
FROM Publisher P
WHERE P.id IN (SELECT S.publisher_id
			   FROM Series S
			   WHERE S.language_id = 21);

-- Moins rapide			   
SELECT DISTINCT(P.id), P.name
FROM Publisher P JOIN Series S
WHERE P.id = S.publisher_id AND S.language_id = 21;
