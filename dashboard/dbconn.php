<?php
include __DIR__.'/vendor/autoload.php';
use RestCord\DiscordClient;
$client = new DiscordClient(['token' => 'MzcxMzcwMzIxNDAxNjEwMjQx.Dc46Bw.of9e1ifoJD-G03rc1wVOi18fMJ4']);
$conn = mysqli_connect("localhost", "root", "", "pbot");
$conn->set_charset("utf8");
?>
