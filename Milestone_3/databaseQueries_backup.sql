-- a) Print the series names that have the highest number of issues which contain a story whose type (e.g., cartoon) is not the one occurring most frequently in the database (e.g, illustration).

-- version 1 execution time: 5.59s


SELECT SER.name FROM
(
	SELECT  I.series_id FROM (
				SELECT DISTINCT S1.issue_id, S1.type_id FROM  Story S1 LEFT JOIN
		(
			SELECT T.id FROM Story_Type T, Story S WHERE S.`type_id` = T.id GROUP BY T.id ORDER BY COUNT(*) DESC LIMIT 1) A
		ON S1.type_id = A.id WHERE A.id IS NULL   ) X
	INNER JOIN Issue I ON X.issue_id = I.id GROUP BY I.series_id ORDER BY COUNT(*) DESC LIMIT  1 ) Z
INNER JOIN Series SER ON Z.series_id = SER.id ;

-- version 2 execution time: 11.3s

SELECT SER.name FROM
(
	SELECT  I.series_id FROM
	(
		SELECT DISTINCT S1.issue_id, S1.type_id FROM  Story S1 LEFT JOIN
		(
			SELECT T.id FROM Story_Type T, Story S WHERE S.`type_id` = T.id GROUP BY T.id ORDER BY COUNT(*) DESC LIMIT 1) A
		ON S1.type_id = A.id WHERE A.id IS NULL   ) X
	INNER JOIN Issue I ON X.issue_id = I.id GROUP BY I.series_id HAVING COUNT(*) >=
	(
		SELECT MAX(counted) FROM
		(
			SELECT  COUNT(*) AS counted FROM
			(
				SELECT DISTINCT S2.issue_id, S2.type_id FROM  Story S2 LEFT JOIN
				(
					SELECT T1.id FROM Story_Type T1, Story S3 WHERE S3.`type_id` = T1.id GROUP BY T1.id ORDER BY COUNT(*) DESC LIMIT 1) A1
				ON S2.type_id = A1.id WHERE A1.id IS NULL   ) X1
			INNER JOIN Issue I1 ON X1.issue_id = I1.id GROUP BY I1.series_id) AS counts
		)
	) Z
INNER JOIN Series SER ON Z.series_id = SER.id ;



-- b) Print the names of publishers who have series with all series types.

-- to undertand this query refer to the following website which explains how to do a divide operation in mysql : https://www.simple-talk.com/sql/t-sql-programming/divided-we-stand-the-sql-of-relational-division/

SELECT DISTINCT Y.name FROM
(
	SELECT X.name, SP.id FROM(
		SELECT DISTINCT  P.name, S.publication_type_id FROM Publisher P
		INNER JOIN Series S ON P.id = S.publisher_id WHERE S.publication_type_id IS NOT NULL) X
INNER JOIN Series_Publication_Type SP ON SP.id = X.publication_type_id ) AS Y
WHERE NOT EXISTS
		(
			SELECT * FROM Series_Publication_Type
			WHERE NOT EXISTS
			(
				SELECT *
				FROM  (
					SELECT X.name, SP.id FROM (
						SELECT DISTINCT  P.name, S.publication_type_id FROM Publisher P
						INNER JOIN Series S ON P.id = S.publisher_id WHERE S.publication_type_id IS NOT NULL) X
					INNER JOIN Series_Publication_Type SP ON SP.id = X.publication_type_id ) AS Z
				WHERE (Y.name = Z.name ) AND Z.id = Series_Publication_type.id));

-- 0.175 sec --> 0.173 sec
CREATE INDEX publisher_name ON Publisher(name) USING HASH;

 -- c) Print the 10 most-reprinted characters from Alan Moore's stories. execution time : 0.019 s
SELECT C1.name FROM
(
	SELECT C.character_id,COUNT(*) FROM (
		SELECT DISTINCT S.title, S.id  FROM  Story_Has_Scripts H, Story_Artists A, Story S , Story_Reprint R
		WHERE A.name = 'Alan Moore' AND H.artist_id = A.id  AND H.story_id = R.target_id AND R.target_id = S.id ) X
	INNER JOIN Story_Has_Characters C ON X.id = C.story_id GROUP BY C.character_id ORDER BY COUNT(*) DESC LIMIT 10 ) Y
INNER JOIN Story_Characters C1
ON Y.character_id = C1.id ;

CREATE INDEX name_index ON Story_Artists (name) USING HASH;

--  d) Print the writers of nature-related stories that have also done the pencilwork in all their nature-related stories.

SELECT DISTINCT Y.name FROM
(
	SELECT DISTINCT A.id, A.name FROM
	(
		SELECT DISTINCT S.id  FROM Story S, Story_Genres G, Story_Has_Genres HG
		WHERE G.name = 'nature' AND HG.genre_id = G.id AND HG.story_id = S.id) X,
		Story_Has_Scripts HS , Story_Artists A
	WHERE X.id = HS.story_id AND HS.artist_id = A.id) Y
INNER JOIN Story_Has_Pencils HP
ON Y.id = HP.artist_id;

-- 0.012 sec --> 0.011 sec
CREATE INDEX story_genre_name ON Story_Genres(name) USING HASH;

-- e) For each of the top-10 publishers in terms of published series, print the 3 most popular languages of their series.

SELECT P.name, L.name FROM
(
	SELECT * FROM (SELECT Y.id, Y.language_id , COUNT(*) as count FROM
	(
		SELECT  X.id,S1.language_id FROM
		(
			SELECT P.id FROM Publisher P INNER JOIN Series S ON P.id = S.publisher_id
			GROUP BY S.publisher_id ORDER BY COUNT(*) DESC LIMIT 10) X
		JOIN Series S1 ON X.id = S1.publisher_id) Y
	GROUP BY Y.id, Y.language_id) Z WHERE
	(
		SELECT COUNT(*) as counted FROM
		(
			SELECT S3.publisher_id, S3.language_id, COUNT(*) as count1 FROM Series S3 GROUP BY S3.publisher_id, S3.language_id) W
		WHERE W.publisher_id = Z.id  AND count1 >= count

	) <= 3 ) R,
Publisher P, Language L WHERE R.id = P.id AND R.language_id = L.id ;



-- f) Print the languages that have more than 10000 original stories published in magazines, along with the number of those stories.
SELECT L.name, COUNT(*)
FROM Language L,
	 (SELECT ST.issue_id FROM Story ST) S1 JOIN
	 (SELECT S.language_id, I.id as issueId
	  FROM Issue I, Series S, Series_Publication_Type SPT
	  WHERE I.series_id = S.id AND S.publication_type_id = SPT.id AND SPT.name = 'magazine') S2
	  ON S1.issue_id = S2.issueId
WHERE L.id = S2.language_id
GROUP BY S2.language_id
HAVING COUNT(*) > 10000;

-- 2.079 sec --> 1.899 sec after index
CREATE INDEX publication_type_name ON Series_Publication_Type(name) USING HASH;

-- g) Print all story types that have not been published as a part of Italian magazine series.
SELECT DISTINCT(STP.id), STP.name
FROM Story ST, Story_Type STP
WHERE ST.type_id = STP.id AND
ST.issue_id NOT IN (SELECT S1.id
					FROM (SELECT I.series_id, I.id FROM Issue I) S1 JOIN
				 		 (SELECT S.id as seriesId
					      FROM Series S, Series_Publication_Type SPT, Publisher P, Country C
					 	  WHERE S.publisher_id = P.id AND P.country_id = C.id AND C.name = 'Italy' AND
	  	  			     	    S.publication_type_id = SPT.id AND SPT.name = 'magazine') S2
				 		  ON S1.series_id = S2.seriesId);
-- 0.134 sec --> 0.018 sec
CREATE INDEX country_name ON Country(name) USING HASH;

-- h) Print the writers of cartoon stories who have worked as writers for more than one indicia publisher.
SELECT S2.name
FROM (SELECT I.indicia_publisher_id, I.id as issueId FROM Issue I) S1 JOIN
	 (SELECT ST.id as storyId, ST.issue_id, STA.name
	  FROM Story ST, Story_Has_Scripts STS, Story_Artists STA, Story_Type STP
	  WHERE ST.type_id = STP.id AND STP.name = 'cartoon' AND ST.id = STS.story_id AND STS.artist_id = STA.id) S2
	  ON S1.issueId = S2.issue_id
GROUP BY S2.name
HAVING COUNT(DISTINCT(S1.indicia_publisher_id)) >= 2;

-- From 2.0 sec to 0.423 sec
CREATE INDEX type_name_has ON Story_Type(name) USING HASH;

-- i) Print the 10 brand groups with the highest number of indicia publishers
SELECT S1.id, S1.name, S2.counted
FROM (SELECT B.publisher_id, B.id, B.name FROM Brand_Group B) S1 JOIN
	 (SELECT P.publisher_id, COUNT(*) as counted
	 FROM Brand_Group B1, Indicia_Publisher P
	 WHERE B1.publisher_id = P.publisher_id
	 GROUP BY P.publisher_id) S2
	 ON S1.publisher_id = S2.publisher_id
	 ORDER BY S2.counted DESC
	 LIMIT 10;

-- j) Print the average series length (in terms of years) per indicia publisher.
SELECT S1.indicia_publisher_id, INDI.name, AVG(S2.year_ended - S2.year_began)
FROM Indicia_Publisher INDI,
	 (SELECT I.series_id, I.indicia_publisher_id FROM Issue I WHERE I.indicia_publisher_id IS NOT NULL AND I.series_id IS NOT NULL) S1 JOIN
	 (SELECT S.id, S.year_began, S.year_ended FROM Series S WHERE S.year_began IS NOT NULL AND S.year_ended IS NOT NULL) S2
	 ON S2.id = S1.series_id
	 WHERE INDI.id = S1.indicia_publisher_id
	 GROUP BY S1.indicia_publisher_id;

-- k) Print the top 10 indicia publishers that have published the most single-issue series.
SELECT S1.indicia_publisher_id, INDI.name
FROM Indicia_Publisher INDI,
	 (SELECT I.id, I.indicia_publisher_id FROM Issue I WHERE I.indicia_publisher_id IS NOT NULL) S1 JOIN
	 (SELECT S.first_issue_id FROM Series S WHERE S.first_issue_id IS NOT NULL AND S.first_issue_id = S.last_issue_id) S2
	 ON S2.first_issue_id = S1.id
	 WHERE INDI.id = S1.indicia_publisher_id
	 GROUP BY S1.indicia_publisher_id
	 ORDER BY COUNT(*) DESC
	 LIMIT 10;

-- l) Print the 10 indicia publishers with the highest number of script writers in a single story.
-- NEEDS TO BE FASTER !
SELECT S2.indicia_publisher_id, INDI.name
FROM Indicia_Publisher INDI,
	 (SELECT ST.issue_id, COUNT(*) as count FROM Story ST, Story_Has_Scripts STHS WHERE ST.id = STHS.story_id AND ST.issue_id IS NOT NULL GROUP BY STHS.story_id) S1 JOIN
	 (SELECT I.id, I.indicia_publisher_id FROM Issue I WHERE I.indicia_publisher_id IS NOT NULL) S2
	 ON S1.issue_id = S2.id
WHERE INDI.id = S2.indicia_publisher_id
GROUP BY S2.indicia_publisher_id
ORDER BY MAX(S1.count) DESC
LIMIT 10;

-- m) Print all Marvel heroes that appear in Marvel-DC story crossovers.
SELECT *
FROM (SELECT DISTINCT(STHC.character_id), STC.name FROM Issue I, Indicia_Publisher P, Story S, Story_Has_Characters STHC, Story_Characters STC
	 WHERE I.id = S.issue_id AND I.indicia_publisher_id = P.id AND
	 P.name LIKE '%marvel%' AND P.name NOT LIKE '%dc%' AND STHC.story_id = S.id AND STC.id = STHC.character_id) S1
WHERE S1.character_id IN (SELECT STHC.character_id FROM Issue I, Indicia_Publisher P, Story S, Story_Has_Characters STHC
	 					 WHERE I.id = S.issue_id AND I.indicia_publisher_id = P.id AND
						 P.name LIKE '%marvel%' AND P.name LIKE '%dc%' AND STHC.story_id = S.id);


-- n) Print the top 5 series with most issues
SELECT I.series_id, S.name
FROM Issue I, Series S
WHERE I.series_id IS NOT NULL AND I.series_id = S.id
GROUP BY I.series_id
ORDER BY COUNT(*) DESC
LIMIT 5;

-- o) Given an issue, print its most reprinted story.
-- REMPLACER 1268358 par l'id the l'issue donné.
SELECT S.id, S.title
FROM Issue I, Story S, Story_Reprint STR
WHERE I.id = 1268358 AND S.issue_id IS NOT NULL AND I.id = S.issue_id AND STR.origin_id = S.id
GROUP BY STR.origin_id
ORDER BY COUNT(*) DESC
LIMIT 1;
