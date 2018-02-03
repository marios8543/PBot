<?php
include("dbconn.php");
if(isset($_COOKIE['token'])){
$token = $_COOKIE['token'];
$result = $conn->query("SELECT server_id,admin_name,admin_id,timestamp,valid FROM setting_sessions WHERE token='$token'");
$result = mysqli_fetch_all($result);
if($result[0][4] === '1'){
$server_id = $result[0][0];
$admin_name = $result[0][1];
$admin_id = $result[0][2];
$timestamp = $result[0][3];
$result2 = $conn->query("SELECT server_name FROM servers WHERE server_id='$server_id'");
$result2 = mysqli_fetch_all($result2);
$server_name = $result2[0][0];
include("sidenav.php");
}
else{
    header("Location:/invalid.html");
}}
?>
