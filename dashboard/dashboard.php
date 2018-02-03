<?php
include("/get_data.php");
$result = $conn->query("SELECT COUNT(discord_name) FROM members WHERE server_id='$server_id'");
$result = mysqli_fetch_all($result);
$member_count = $result[0][0];
$result2 = $conn->query("SELECT COUNT(*) FROM members");
$result2 = mysqli_fetch_all($result2);
$user_count = $result2[0][0];
$result3 = $conn->query("SELECT COUNT(discord_name) FROM members WHERE server_id='$server_id' AND in_server=0");
$result3 = mysqli_fetch_all($result3);
$left_count = $result3[0][0];
$result4 = $conn->query("SELECT COUNT(server_name) FROM servers");
$result4 = mysqli_fetch_all($result4);
$server_count = $result4[0][0];
$result5 = $conn->query("SELECT COUNT(*) FROM warnings WHERE server_id='$server_id'");
$result5 = mysqli_fetch_all($result5);
$warn_count = $result5[0][0];
$result6 = $conn->query("SELECT COUNT(*) FROM warnings");
$restult6 = mysqli_fetch_all($result6);
$total_warns = $restult6[0][0];
?>
<head>
<title>Dashboard-<?=$server_name?></title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous"></head>
</head>
<body background="bg.png">
<div class="container" align="center">
<style>
#server {
    position: absolute;
    right: 50px;
    width: 900px;
}
#pbot {
    position: absolute;
    width: 900px;
}
#panel{
    opacity: 0.5;
}
#bottom {
    position: relative;
    bottom: -600px;
    left: 50px;
    opacity: 0.5;
}
#opacity {
    opacity: 0.5;
}
</style>
    <div id="server">
  <h1 id="opacity"><font color="white">Server Stats</h1></font>
  <div class="panel-group" id="panel">
    <div class="panel panel-info" style="width: 30%;">
      <div class="panel-heading"><h2>Current members<font size="1">(logged by pbot)</h2></font></div>
      <div class="panel-body"><font size="7"><?=$member_count?></font></div>
    </div>
    <div class="panel panel-info" style="width: 30%;">
      <div class="panel-heading"><h2>Members that left</h2></div>
      <div class="panel-body"><font size="7"><?=$left_count?></font></div>
    </div>
    <div class="panel panel-warning" style="width: 30%;">
      <div class="panel-heading"><h2>Warnings issued</h2></div>
      <div class="panel-body"><font size="7"><?=$warn_count?></div>
    </div>
</div>
</div>
<div id="pbot">
  <h1 id="opacity"><font color="white">>PBot Stats</h1></font>
  <div class="panel-group" id="panel">
    <div class="panel panel-info" style="width: 30%;">
      <div class="panel-heading"><h2>Servers that utilise >PBot</h2></div>
      <div class="panel-body"><font size="7"><?=$server_count?></font></div>
    </div>
    <div class="panel panel-info" style="width: 30%;">
      <div class="panel-heading"><h2>Users served by >PBot</h2></div>
      <div class="panel-body"><font size="7"><?=$user_count?></font></div>
  </div>
      <div class="panel panel-warning" style="width: 30%;">
        <div class="panel-heading"><h2>Warnings issued</h2></div>
        <div class="panel-body"><font size="7"><?=$total_warns?></div>
      </div>
    </div>
  </div>
<div align="center" id="bottom"><h1 style="font-size:70px"><font color="white"><?=$server_name?></font></h1></div>
</div>
</div>
</body>
</html>
