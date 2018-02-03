<?php
include("get_data.php");
$result = $conn->query("SELECT discord_name,join_date,real_name,email,reason_join,warns,in_server FROM members WHERE server_id='$server_id'");
$result = mysqli_fetch_all($result);
?>
<head>
<title>Members-<?=$server_name?></title>
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
  <th>Join Date</th>
  <th>Real Name</th>
  <th>E-Mail</th>
  <th>Join Reason</th>
  <th>Warning Count</th>
</tr>
</thread>
<?php
foreach($result as $array){
    $name = $array[0];
    $join_date = $array[1];
    $real_name = $array[2];
    $email = $array[3];
    $join_reason = $array[4];
    $warnings = $array[5];
    $in_server = $array[6];
if($in_server === '0'){
echo"
<tr class='danger'>
<td>$name</td>
<td>$join_date</td>
<td>$real_name</td>
<td>$email</td>
<td>$join_reason</td>
<td>$warnings</td>
</tr>
";
}
else{
echo"
<tr class='active'>
<td>$name</td>
<td>$join_date</td>
<td>$real_name</td>
<td>$email</td>
<td>$join_reason</td>
<td>$warnings</td>
</tr>
";
}
}
?>
</center>
