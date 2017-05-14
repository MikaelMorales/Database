<?php
include("Utils.php");
$request_body = file_get_contents('php://input');
$data = json_decode($request_body, true);
$id = explode(",",$data['QueryId'])[0];

$idToQuery = array(
  0 => array("SELECT G.id, G.name FROM Brand_Group G WHERE G.publisher_id IN (SELECT I2.publisher_id FROM Indicia_Publisher I2, Country C1 WHERE C1.name = \"Belgium\" AND I2.country_id = C1.id GROUP BY I2.publisher_id HAVING COUNT(*) >= (SELECT MAX(counted) FROM (SELECT COUNT(I3.id) AS counted FROM Indicia_Publisher I3, Country C2 WHERE C2.name = \"Belgium\" AND I3.country_id = C2.id GROUP BY I3.publisher_id) AS counts));", "Brand Group"),
  1 => array("SELECT DISTINCT(P.id), P.name FROM Publisher P WHERE P.id IN (SELECT S.publisher_id FROM Series S, Country C WHERE C.name = \"Denmark\" AND S.country_id = C.id);", "Publisher"),
  2 => array("SELECT S.id, S.name FROM Series S, Country C, Series_Publication_Type T WHERE C.name = \"Switzerland\" AND C.id = S.country_id AND T.name = \"magazine\" AND S.publication_type_id = T.id;", "Series"),
  3 => array("SELECT I.publication_date, COUNT(I.id) FROM Issue I WHERE I.publication_date >= 1990 GROUP BY I.publication_date;", "Issues per years"),
  4 => array("SELECT IndiPubli.id, IndiPubli.name, COUNT(DISTINCT(I.series_id)) FROM Issue I, Indicia_Publisher IndiPubli WHERE I.indicia_publisher_id = IndiPubli.id AND IndiPubli.name LIKE \"DC comics\" GROUP BY I.indicia_publisher_id;", "Indicia Publisher"),
  5 => array("SELECT S.id, S.title, count FROM (SELECT SR.origin_id, COUNT(*) AS count FROM Story_Reprint SR GROUP BY SR.origin_id ORDER BY COUNT(*) DESC) S1 JOIN Story S ON S.id = S1.origin_id WHERE S.title IS NOT NULL LIMIT 10;", "Story"),
  6 => array("SELECT id, name FROM Story_Artists A WHERE A.id IN (SELECT DISTINCT C.artist_id FROM Story_Has_Scripts H, Story_Has_Colors C, Story_Has_Pencils P WHERE H.story_id = C.story_id AND C.story_id = P.story_id AND H.artist_id = C.artist_id AND C.artist_id = P.artist_id);", "Story_Artists"),
  7 => array("SELECT DISTINCT S.id, S.title FROM Story_Characters SC, Story_Has_Characters SHC, Story S WHERE SC.name = \"Batman\" AND SHC.character_id = SC.id AND S.id = SHC.story_id AND S.title IS NOT NULL AND S.id NOT IN (SELECT SR.origin_id FROM Story_Reprint SR) AND S.id NOT IN (SELECT DISTINCT SHF.story_id FROM Story_Has_Features SHF, Story_Features SF WHERE SF.name = \"Batman\" AND SHF.feature_id = SF.id);", "Story")
);

$connection_mysql = Utils::connect_to_db();

executeQuery($connection_mysql, $idToQuery[$id][0], $idToQuery[$id][1]);

mysqli_close($connection_mysql);

function executeQuery($connection_mysql, $query, $table) {
  $tableToRows = [];
  $tableToRows = Utils::execute_request($connection_mysql, $query, $tableToRows);
  echo json_encode($tableToRows);
}
?>
