<?php
	include_once("Utils.php");
    include_once("TablesInformations.php");
	$request_body = file_get_contents('php://input');
    $data = json_decode($request_body, true);
	$table = $data['Table'];
    $attributes = $data['Attributes'];

	$connection_mysql = Utils::connect_to_db();

    if ($attributes != null && $table != null) {
        $p = print_r($attributes, true);
        error_log($p . "\n", 3, "test.txt");
        $request = "DELETE FROM " . $table . " WHERE ";
        $conditions = "";

        //point to end of the array
        end($attributes);
        //fetch key of the last element of the array.
        $lastElementKey = key($attributes);
        //iterate the array

        error_log($lastElementKey . "\n", 3, "test.txt");

        foreach($attributes as $k => $v) {
			if (is_numeric($v)) {
				$value = $v;
			} else {
				$value = "\"$v\"";
			}
            if($k == $lastElementKey) {
                $conditions .= $k . " = " . $value;
            } else {
                $conditions .= $k . " = " . $value . " AND ";
            }
        }

        $request .= $conditions . ";";
        error_log($request . "\n", 3, "test.txt");

        if ($connection_mysql->query($request) === TRUE) {
			http_response_code(200);
            echo "Deletion finished successfully";
        } else {
			http_response_code(500);
            echo "Error: " . $request . "<br>" . $connection_mysql->error;
        }
    }

	mysqli_close($connection_mysql);
?>
