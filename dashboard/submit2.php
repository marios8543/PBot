<?php
include("dbconn.php");
$token = $_GET['sid'];
$result = $conn->query("SELECT server_id FROM setting_sessions WHERE token='$token'");
$result = mysqli_fetch_all($result);
$server_id = $result[0][0];
if(isset($_POST['logging'])){
    var_dump($_POST['logging']);
    $logging_toggle = $_POST['logging'];
}

if(isset($_POST['whitelist'])){
    var_dump($_POST['whitelist']);
    $whitelist = $_POST['whitelist'];
}

if(isset($_POST['max_warns'])){
    var_dump($_POST['max_warns']);
    $max_warnings = $_POST['max_warns'];
}

$array = explode(",",$whitelist);
$json = json_encode($array);

$result = $conn->query("UPDATE servers SET log_whitelist='$json',log_msgchanges='$logging_toggle',max_warns='$max_warnings' WHERE server_id='$server_id'");
var_dump($result);
header("Location:/pbot/settings.php");
var_dump($conn->error);
?>
