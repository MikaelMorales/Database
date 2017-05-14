<?php
final class Utils {
  static function connect_to_db() {
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

  static function execute_request($connection_mysql, $request, $tableToRows, $table) {
    if ($result = $connection_mysql->query($request)) {
      $row = $result->fetch_array(MYSQLI_ASSOC);
      if ($row != null) {
        $tableToRows[$table] = [];
      }
      while ($row != null) {
        array_push($tableToRows[$table], $row);
        $row = $result->fetch_array(MYSQLI_ASSOC);
      }

      return $tableToRows;
    } else {
        printf("Error: %s\n", $connection_mysql->error);
        error_log($connection_mysql->error . "\n", 3, "error_log.txt");
    }
  }
}
 ?>
