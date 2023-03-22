<?php
    $host = "localhost";
    $port = "5432";
    $dbname = "postgres";
    $user = "postgres";
    $password = "0907";

    $dsn = "pgsql:host=$host;port=$port;dbname=$dbname;user=$user;password=$password";

    try {
        $pdo = new PDO($dsn);
        echo "good connection";
    } catch (PDOException $e) {
        echo "connection failed: " . $e->getMessage();
    }
?>
