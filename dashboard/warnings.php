<?php
include("get_data.php");
$result = $conn->query("SELECT discord_id,discord_name,warn_datetime,admin,reason FROM warnings WHERE server_id='$server_id'");
$result = mysqli_fetch_all($result);
?>
<head>
<title>Warnings-<?=$server_name?></title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous"></head>
</head>
<style>
#members {
    opacity: 0.7;
    width: 84%;
    position:absolute;
    left: 253px;
}
</style>
<body background="bg.png">
<center>
<div class="container">
<table class="table table-striped" id="members">
<thread>
<tr class="info">
  <th>Discord Name</th>
  <th>Timestamp</th>
  <th>Enforcer admin</th>
  <th>Reason</th>
  <th>Warning Count</th>
</tr>
</thread>
<?php
foreach($result as $array){
    $d_id = $array[0];
    $name = $array[1];
    $timestamp = $array[2];
    $admin = $array[3];
    $reason = $array[4];
    echo"
    <tr class='warning'>
    <td>$name</td>
    <td>$timestamp</td>
    <td>$admin</td>
    <td>$reason</td>
    <td>Coming soon...</td>
    </tr>
    ";
}
