<?php
	// ini_set('display_errors', 'On');
	// error_reporting(E_ALL);
	// error_reporting(E_ALL | E_STRICT);
	$request_body = file_get_contents('php://input');
   	$data = json_decode($request_body, true);
    $myfile = fopen("search_request_log.txt", "a") or die("Unable to open file!");
	fwrite($myfile,"Request : " . $data['Request'] . "\n" );
	fwrite($myfile,"Tables : " . $data['Tables'] . "\n" );
	fclose($myfile);

	$tables = explode(",",$data['Tables']);
	foreach ($tables as $table) {
		fwrite($myfile, $table);
	}

	$result_file = fopen("log.txt", "a") or die("Unable to open file!");

	fwrite($result_file, "NEW REQUEST:\n");

	$user = 'charles';
	$password = 'some_pass';
	$db = 'comics';
	$host = '127.0.0.1';
	$port = 3306;
	$socket = 'localhost:/tmp/mysql.sock';

	$connection_mysql = mysqli_init();

	if (!$connection_mysql) {
		fwrite($result_file, "mysqli_init failed\n");
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

	if ($success) {
		fwrite($result_file, "Connection Works !!\n\n");
	} else {
		fwrite($result_file, "Connection failed : " . mysqli_connect_error() ."\n");
	    die("Connection failed");
	}

	foreach ($tables as $table) {
	    if ($result = $connection_mysql->query("SELECT name FROM " . $table . " WHERE id = " . $data['Request'])) {
			$name = $result->fetch_array()['name'];
		    printf("Query result : \n\tnumber of rows returned = %d\n\tResult : %s\n\n", $result->num_rows, $name);
		    fwrite($result_file, "Query result : \n");
		    fwrite($result_file, "\tnumber of rows returned = " . $result->num_rows);
		    fwrite($result_file, "\n\tResult : " . $name . "\n\n");
		} else {
			printf("Error: %s\n", $connection_mysql->error);
		    fwrite($result_file, "Error: " . $connection_mysql->error .  " when querying in table " . $table . "\n\n");
		}
	}

	// if ($result = $connection_mysql->query("SELECT name FROM Story_Artists WHERE id = 0")) {
	// 	$name = $result->fetch_array()['name'];
	//     printf("Query result : \n\tnumber of rows returned = %d\n\tResult : %s\n\n", $result->num_rows, $name);
	//     fwrite($result_file, "Query result : \n");
	//     fwrite($result_file, "\tnumber of rows returned = " . $result->num_rows);
	//     fwrite($result_file, "\n\tResult : " . $name . "\n\n");
	// } else {
	// 	printf("Error: %s\n", $mysqli->error);
	//     fwrite($result_file, "Error: " . $mysqli->error);
	// }
	// $result->close();


	mysqli_close($connection_mysql);

	fclose($result_file);
?>