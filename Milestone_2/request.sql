-- Print the brand group names with the highest number of Belgian indicia publishers.
SELECT G.name
FROM Brand_Group G
WHERE G.publisher_id IN 
			(SELECT I2.publisher_id
			 FROM Indicia_Publisher I2, Country C1
			 WHERE C1.name = "Belgium" AND I2.country_id = C1.id
			 GROUP BY I2.publisher_id
			 HAVING COUNT(*) >= 
			 	(SELECT MAX(counted) FROM (SELECT COUNT(I3.id) AS counted
										   FROM Indicia_Publisher I3, Country C2
										   WHERE C2.name = "Belgium" AND I3.country_id = C2.id
										   GROUP BY I3.publisher_id) AS counts));
										   
-- Print the ids and names of publishers of Danish book series.								   
SELECT DISTINCT(P.id), P.name
FROM Publisher P
WHERE P.id IN (SELECT S.publisher_id
			   FROM Series S, Country C
			   WHERE C.name = "Denmark" AND S.country_id = C.id);

-- Print the ids and names of publishers of Danish book series.
-- But slower.		   
SELECT DISTINCT(P.id), P.name
FROM Publisher P JOIN Series S, Language L
WHERE P.id = S.publisher_id AND L.name = "Danish" AND S.language_id = L.id;

-- Print the names of all Swiss series that have been published in magazines.
SELECT S.name
FROM Series S, Country C, Series_Publication_Type T
WHERE C.name = "Switzerland" AND C.id = S.country_id AND T.name = "magazine" AND S.publication_type_id = T.id;

-- Starting from 1990, print the number of issues published each year.
SELECT I.publication_date, COUNT(I.id)
FROM Issue I
WHERE I.publication_date >= 1990
GROUP BY I.publication_date;

-- Print the number of series for each indicia publisher whose name resembles ‘DC comics’.
SELECT I.indicia_publisher_id, IndiPubli.name, COUNT(DISTINCT(I.series_id))
FROM Issue I, Indicia_Publisher IndiPubli
WHERE I.indicia_publisher_id = IndiPubli.id AND IndiPubli.name LIKE 'DC comics'
GROUP BY I.indicia_publisher_id;

-- Print the titles of the 10 most reprinted stories
SELECT S.title, count FROM 
(SELECT SR.origin_id, COUNT(*) AS count 
 FROM Story_Reprint SR 
 GROUP BY SR.origin_id 
 ORDER BY COUNT(*) DESC) S1
JOIN Story S
ON S.id = S1.origin_id
WHERE S.title IS NOT NULL
LIMIT 10;

-- Print the titles of the 10 most reprinted stories
-- But slower.
SELECT S.title, COUNT(*)
FROM Story_Reprint SR, Story S
WHERE S.title IS NOT NULL AND S.id = SR.origin_id
GROUP BY SR.origin_id 
ORDER BY COUNT(*) DESC
LIMIT 10;


-- Print the artists that have scripted, drawn, and colored at least one of the stories they were involved in.
SELECT name 
FROM Story_Artists A
WHERE A.id IN (SELECT DISTINCT C.artist_id 
			   FROM Story_Has_Scripts H, Story_Has_Colors C, Story_Has_Pencils P    
			   WHERE H.`story_id` = C.`story_id` AND 
		  		     C.`story_id` = P.`story_id`  AND 
		  			 H.`artist_id` = C.`artist_id` AND  
		 			 C.`artist_id` = P.`artist_id`);

-- Print all non-reprinted stories involving Batman as a non-featured character.
SELECT DISTINCT S.title
FROM Story_Has_Features SHF, Story_Features SF, Story_Characters SC, Story_Has_Characters SHC, Story S
WHERE SF.name != "Batman" AND 
	  SHF.feature_id = SF.id AND 
	  SC.name = "Batman" AND 
	  SHC.`character_id` = SC.`id` AND 
	  SHF.`story_id` = SHC.`story_id` AND 
	  S.id = SHF.story_id AND 
	  S.title IS NOT NULL AND S.id NOT IN (SELECT SR.`origin_id` FROM Story_Reprint SR);