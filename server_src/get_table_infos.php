<?php
include_once("Utils.php");
include_once("TablesInformations.php");
$request_body = file_get_contents('php://input');
$data = json_decode($request_body, true);
$tableId = $data["tableId"];

if ($tableId != null) {
    error_log("tableId : " . $tableId . "\n", 3, "error_log.txt");
    $fieldList = [];
    $connection_mysql = Utils::connect_to_db();
    $fieldList = Utils::execute_request($connection_mysql, "DESCRIBE " . $tableId . ";", $fieldList, $tableId, $tableId);
    error_log(json_encode($fieldList), 3, "error_log.txt");
    echo json_encode($fieldList);
}
?>
