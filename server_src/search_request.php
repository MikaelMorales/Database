<?php
	$request_body = file_get_contents('php://input');
   	$data = json_decode($request_body, true);
	$tables = explode(",",$data['Tables']);

	$connection_mysql = connectToDb();

	makeSQLQuery($tables, $data['Request'], $connection_mysql);

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

	function makeSQLQuery($tables, $requestedAttributes, $connection_mysql) {
		if (is_numeric($requestedAttributes)) {
			queryID($tables, $requestedAttributes, $connection_mysql);
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
?>