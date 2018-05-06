<?php
$token = $_GET['token'];
$expire = time()+43200; //Makes the cookie expire after 12 hours
setcookie('token',$token,$expire); //sets the token as a cookie
header("Location:dashboard/dashboard.php");
?>
