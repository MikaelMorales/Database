<?php
	include_once("Utils.php");
	include_once("TablesInformations.php");
	$request_body = file_get_contents('php://input');
    $data = json_decode($request_body, true);
	$tables = explode(",",$data['Tables']);
	if ($tables[0] == null) {
		$tables = TablesInformations::getTables();
	}
	// $limit = $data["MaxLineNb"];
	$limit = 2;

	// $offset = $data["Offset"];
	$offset = 0;

	$connection_mysql = Utils::connect_to_db();

	makeSQLQuery($tables, $data['Request'], $connection_mysql, $offset, $limit);

	mysqli_close($connection_mysql);

	function makeSQLQuery($tables, $requestedAttributes, $connection_mysql, $offset, $limit) {
		if ($requestedAttributes != null) {
			if (is_numeric($requestedAttributes)) {
				// queryID($tables, $requestedAttributes, $connection_mysql);
				queryID($tables, $requestedAttributes, $connection_mysql, $offset, $limit);
			} else {
				queryOnStandardAttributes($tables, $requestedAttributes, $connection_mysql, $offset, $limit);
			}
		}
	}

	// function queryID($tables, $requestedAttributes, $connection_mysql) {
	// 	$tableToRows = [];
	// 	foreach ($tables as $table) {
	// 			$request = "SELECT * FROM " . $table . " WHERE id = " . $requestedAttributes . ";";
	// 			$tableToRows = Utils::execute_request($connection_mysql, $request, $tableToRows, $table);
	// 	}
	// 	echo json_encode($tableToRows);
	// }

	function queryID($tables, $requestedAttributes, $connection_mysql, $offset, $limit) {
		$tableToRows = [];
		foreach ($tables as $table) {
			$attributes = TablesInformations::getNumericAttributes($table);
			$request = "SELECT * FROM " . $table . " WHERE " . $attributes[0] . " LIKE \"" . $requestedAttributes . "\"";
			unset($attributes[0]);
			foreach ($attributes as $attribute) {
				$request .= " OR " . $attribute . " LIKE \"" . $requestedAttributes ."\"";
			}
			$request .= "LIMIT " . $limit . " OFFSET " . $offset . ";";

			// error_log($request, 3, "te.txt");
			$tableToRows = Utils::execute_request($connection_mysql, $request, $tableToRows, $table, TablesInformations::getNicerNames($table));
		}
		echo json_encode($tableToRows);
	}

	function queryOnStandardAttributes($tables, $requestedAttributes, $connection_mysql, $offset, $limit) {
		$tableToRows = [];
		foreach ($tables as $table) {
			$attributes = TablesInformations::getAttributesOfTable($table);
			$request = "SELECT * FROM " . $table . " WHERE " . $attributes[0] . " LIKE \"" . $requestedAttributes . "\"";
			unset($attributes[0]);
			foreach ($attributes as $attribute) {
				$request .= " OR " . $attribute . " LIKE \"" . $requestedAttributes ."\"";
			}
			$request .= "LIMIT " . $limit . " OFFSET " . $offset . ";";

			$tableToRows = Utils::execute_request($connection_mysql, $request, $tableToRows, $table, TablesInformations::getNicerNames($table));
		}
		echo json_encode($tableToRows);
	}
?>
