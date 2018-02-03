<?php
include("dbconn.php");
$token = $_GET['sid'];
$result = $conn->query("SELECT server_id FROM setting_sessions WHERE token='$token'");
$result = mysqli_fetch_all($result);
$server_id = $result[0][0];
if(isset($_POST['entry_text'])){
    var_dump($_POST['entry_text']);
    $entry_text = $_POST['entry_text'];
}

if(isset($_POST['entry_text_pm'])){
    var_dump($_POST['entry_text_pm']);
    $entry_text_pm = $_POST['entry_text_pm'];
}

if(isset($_POST['goodbye_text'])){
    var_dump($_POST['goodbye_text']);
    $goodbye_text = $_POST['goodbye_text'];
}

$result = $conn->query('UPDATE servers SET entry_text="'.$entry_text.'", entry_text_pm="'.$entry_text_pm.'", goodbye_text="'.$goodbye_text.'" WHERE server_id='.$server_id);
var_dump($result);
echo $conn->error;
header("Location:/pbot/settings.php")
?>
