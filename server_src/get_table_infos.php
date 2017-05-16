<?php
include("Utils.php");
include("TablesInformations.php");
$request_body = file_get_contents('php://input');
$data = json_decode($request_body, true);
$tableId = $data["tableId"];

if ($tableId != null) {
    error_log("tableId : " . $tableId . "\n", 3, "error_log.txt");
    $fieldList = [];
    $connection_mysql = Utils::connect_to_db();
    error_log(TablesInformations::getName($tableId) . "\n", 3, "error_log.txt");
    $fieldList = Utils::execute_request($connection_mysql, "DESCRIBE " . TablesInformations::getName($tableId) . ";", $fieldList, $tableId);
    error_log(json_encode($fieldList), 3, "error_log.txt");
    echo json_encode($fieldList);
}
?>
