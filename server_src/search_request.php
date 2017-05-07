<?php
	$request_body = file_get_contents('php://input');
   	$data = json_decode($request_body, true);
	$tables = explode(",",$data['Tables']);

	$tableToAttributes = array("Story" => ["title", "letters", "editing", "synopsis", "reprint_notes", "notes"], "Story_Artists" => ["name"], "Story_Characters" => ["name"]);

	$connection_mysql = connectToDb();

	makeSQLQuery($tables, $data['Request'], $connection_mysql, $tableToAttributes);

	mysqli_close($connection_mysql);

	function connectToDb() {
		$user = 'charles';
		$password = 'some_pass';
		$db = 'comics';
		$host = '127.0.0.1';
		$port = 3306;
		$socket = 'localhost:/tmp/mysql.sock';

		$connection_mysql = mysqli_init();

		if (!$connection_mysql) {
		    die('mysqli_init failed');
		}

		$success = mysqli_real_connect(
		    $connection_mysql, 
		    $host,
		    $user, 
		    $password, 
		    $db,
		    $port,
		    $socket
		);

		if (!$success) {
			die("Connection failed");
		}

		return $connection_mysql;
	}

	function makeSQLQuery($tables, $requestedAttributes, $connection_mysql, $tableToAttributes) {
		if (is_numeric($requestedAttributes)) {
			queryID($tables, $requestedAttributes, $connection_mysql);
		} else {
			queryOnStandardAttributes($tables, $requestedAttributes, $connection_mysql, $tableToAttributes);
		}
	}

	function queryID($tables, $requestedAttributes, $connection_mysql) {
		$tableToRow = [];
		foreach ($tables as $table) {
		    if ($result = $connection_mysql->query("SELECT * FROM " . $table . " WHERE id = " . $requestedAttributes . ";")) {
		    	$tableToRow[$table] = [];
		    	$result_array = $result->fetch_array(MYSQLI_ASSOC);
		    	if ($result_array != null) {
		    		array_push($tableToRow[$table], $result_array);
		    	}
			} else {
				printf("Error: %s\n", $connection_mysql->error);
			}
		}
		echo json_encode($tableToRow);		
	}

	function queryOnStandardAttributes($tables, $requestedAttributes, $connection_mysql, $tableToAttributes) {
		$tableToRow = [];
		$myfile = fopen("newfile.txt", "a") or die("Unable to open file!");
		foreach ($tables as $table) {
			$attributes = $tableToAttributes[$table];
			$request = "SELECT * FROM " . $table . " WHERE " . $attributes[0] . " LIKE \"" . $requestedAttributes . "\"";
			unset($attributes[0]);
			foreach ($attributes as $attribute) {
				$request .= " OR " . $attribute . " LIKE \"" . $requestedAttributes ."\"";
			}
			$request .= ";";
			fwrite($myfile, $request);
		    if ($result = $connection_mysql->query($request)) {
		    	$row = $result->fetch_array(MYSQLI_ASSOC);
		    	if ($row != null) {
		    		$tableToRow[$table] = [];
		    	}
		    	while ($row != null) {
		    		array_push($tableToRow[$table], $row);
		    		$row = $result->fetch_array(MYSQLI_ASSOC);
		    	}
			} else {
				printf("Error: %s\n", $connection_mysql->error);
			}
		}
		$rowfile = fopen("rowfile.txt", "w") or die("Unable to open rowfile ! ");
		fwrite($rowfile, json_encode($tableToRow));
		fclose($rowfile);
		echo json_encode($tableToRow);
	}
?>