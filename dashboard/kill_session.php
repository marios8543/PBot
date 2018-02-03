<?php
include("dbconn.php");
$token = $_COOKIE['token'];
$conn->query("UPDATE setting_sessions SET valid=0 WHERE token='$token'");
header("Location:/index.html");
 ?>
