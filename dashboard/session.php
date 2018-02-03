<?php
$result = 0;
$token = $_GET['token']; //gets the token from the link
include('dbconn.php'); //makes db connection
$result = $conn->query("SELECT valid FROM setting_sessions WHERE token='$token'"); //preliminary validity check
$result = mysqli_fetch_all($result);
$valid = $result[0][0];
if($valid == 1){
    $expire = time()+43200; //Makes the cookie expire after 12 hours
    setcookie('token',$token,$expire); //sets the token as a cookie
    echo "The session is valid...<a href='/dashboard.php'>Redirecting</a>";
    sleep(2);
    header("Location:/pbot/dashboard.php");
}
else{
    echo "The session is invalid. Make a new one by typing >>settings in your server";
}
 ?>
