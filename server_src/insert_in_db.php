<?php
	include_once("Utils.php");
    include_once("TablesInformations.php");
	$request_body = file_get_contents('php://input');
    $data = json_decode($request_body, true);
	$table = $data['Table'];
    $attributes = $data['Attributes'];

	$connection_mysql = Utils::connect_to_db();

    if ($attributes != null && $table != null) {
        $request = "INSERT INTO " . $table . " ";
        $fieldNames = "(";
        $values = "VALUES (";

        //point to end of the array
        end($attributes);
        //fetch key of the last element of the array.
        $lastElementKey = key($attributes);
        //iterate the array

        foreach($attributes as $k => $v) {
			if (is_numeric($v)) {
				$value = $v;
			} else {
				$value = "\"$v\"";
			}
            if($k == $lastElementKey) {
                $fieldNames .= $k . ")";
                $values .= $value . ")";
            } else {
                $fieldNames .= $k . ", ";
                $values .= $value . ", ";
            }
        }

        $request .= $fieldNames . " " . $values . ";";

        if ($connection_mysql->query($request) === TRUE) {
			http_response_code(200);
            echo "New record created successfully";
        } else {
			http_response_code(404);
            echo "Error: " . $request . "<br>" . $connection_mysql->error;
        }
    }

	mysqli_close($connection_mysql);
?>
