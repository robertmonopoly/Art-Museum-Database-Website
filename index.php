<?php
    // Initialize connection variables.
	$host = "team8.postgres.database.azure.com";
	$database = "postgres";
	$user = "team8";
	$password = "server1234!";

	// Initialize connection object.
	$connection = pg_connect("host=$host dbname=$database user=$user password=$password") 
		or die("Failed to create connection to database: ". pg_last_error(). "<br/>");
	print "Successfully created connection to database.<br/>";
?>
