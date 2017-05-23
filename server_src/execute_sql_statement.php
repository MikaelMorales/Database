<?php
	include_once("Utils.php");
	$request_body = file_get_contents('php://input');
    $data = json_decode($request_body, true);
    $statement = $data['Statement'];
	// $statement = "select * from Story";
	$maxLineNb = $data['MaxLineNb'];
	// $maxLineNb = 50;
	$offset = $data['Offset'];
	// $offset = 0;
	$connection_mysql = Utils::connect_to_db();

    if ($statement != null) {
        $tableToRows = [];
		if (substr($statement, -1) == ";") {
			$statement = substr($statement, 0, -1);
		}
		$statement .= " LIMIT " . $maxLineNb . " OFFSET " . $offset ; ";";
        // $tableToRows = Utils::execute_request($connection_mysql, $statement, $tableToRows, "Result");
		error_log($statement, 3, "tes.txt");
		$tableToRows = Utils::execute_sql_statement($connection_mysql, $statement, $tableToRows);
        echo json_encode($tableToRows);
    }

	mysqli_close($connection_mysql);
?>
