<?php
	include("Utils.php");
	$request_body = file_get_contents('php://input');
    $data = json_decode($request_body, true);
    $statement = $data['Statement'];

	$connection_mysql = Utils::connect_to_db();

    if ($statement != null) {
        $tableToRows = [];
        $tableToRows = Utils::execute_request($connection_mysql, $statement, $tableToRows, "Result");
        echo json_encode($tableToRows);
    }

	mysqli_close($connection_mysql);
?>
