<?php
include_once("TablesInformations.php");
$request_body = file_get_contents('php://input');

echo json_encode(TablesInformations::getIdToName());
?>
