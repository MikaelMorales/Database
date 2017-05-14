<?php
	include("Utils.php");
	$request_body = file_get_contents('php://input');
  $data = json_decode($request_body, true);
	$tables = explode(",",$data['Tables']);

	$tableToAttributes = array("Story" => ["title", "letters", "editing", "synopsis", "reprint_notes", "notes"], "Story_Artists" => ["name"], "Story_Characters" => ["name"]);

	$connection_mysql = Utils::connect_to_db();

	makeSQLQuery($tables, $data['Request'], $connection_mysql, $tableToAttributes);

	mysqli_close($connection_mysql);

	function makeSQLQuery($tables, $requestedAttributes, $connection_mysql, $tableToAttributes) {
		if ($requestedAttributes != null) {
			if (is_numeric($requestedAttributes)) {
				queryID($tables, $requestedAttributes, $connection_mysql);
			} else {
				queryOnStandardAttributes($tables, $requestedAttributes, $connection_mysql, $tableToAttributes);
			}
		}
	}

	function queryID($tables, $requestedAttributes, $connection_mysql) {
		$tableToRows = [];
		foreach ($tables as $table) {
				$request = "SELECT * FROM " . $table . " WHERE id = " . $requestedAttributes . ";";

				$tableToRows = Utils::execute_request($connection_mysql, $request, $tableToRows);
		}
		echo json_encode($tableToRows);
	}

	function queryOnStandardAttributes($tables, $requestedAttributes, $connection_mysql, $tableToAttributes) {
		$tableToRows = [];
		foreach ($tables as $table) {
			$attributes = $tableToAttributes[$table];
			$request = "SELECT * FROM " . $table . " WHERE " . $attributes[0] . " LIKE \"" . $requestedAttributes . "\"";
			unset($attributes[0]);
			foreach ($attributes as $attribute) {
				$request .= " OR " . $attribute . " LIKE \"" . $requestedAttributes ."\"";
			}
			$request .= ";";

			$tableToRows = Utils::execute_request($connection_mysql, $request, $tableToRows);
		}
		echo json_encode($tableToRows);
	}
?>
