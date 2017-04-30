
SELECT name FROM Story_Artists A, (SELECT DISTINCT C.artist_id FROM Story_Has_Scripts H, Story_Has_Colors C, `Story_Has_Pencils` P    WHERE  
H.`story_id` = C.`story_id` AND C.`story_id` = P.`story_id`  AND
H.`artist_id` = C.`artist_id` AND C.`artist_id` = P.`artist_id`) X WHERE A.id = X.`artist_id`;

-- 4150 line.

-- Print all non-reprinted stories involving Batman as a non-featured character.

-- VERSION 1
SELECT DISTINCT  S.title FROM Story S
WHERE S.id NOT IN
(SELECT DISTINCT X.story_id FROM `Story_Reprint` R, (SELECT DISTINCT story_id FROM Story_Has_Characters H, `Story_Characters` C WHERE C.`name` = 'Batman') X WHERE  
(R.origin_id = X.story_id OR R.target_id = X.story_id));

-- 823303 line