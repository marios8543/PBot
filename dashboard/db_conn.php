<?php
include 'C:\Users\marios\vendor\autoload.php';
use RestCord\DiscordClient;
$client = new DiscordClient(['token' => '']);
$conn = mysqli_connect("localhost", "root", "", "pbot");
$conn->set_charset("utf8");
?>
