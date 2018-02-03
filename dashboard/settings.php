<?php
include('get_data.php');
$result = $conn->query("SELECT log_whitelist,log_msgchanges,entry_text,entry_text_pm,goodbye_text,max_warns FROM servers WHERE server_id='$server_id'");
$result = mysqli_fetch_all($result);
$log_whitelist = $result[0][0];
$logging = $result[0][1];
$entry_text = $result[0][2];
$entry_text_pm = $result[0][3];
$goodbye_text = $result[0][4];
$max_warnings = $result[0][5];
?>
<head>
<title>Settings-<?=$server_name?></title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous"></head>
</head>
<body background="bg.png">3
<div class="container" align="center">
<style>
#panel{
    opacity: 0.5;
}
#bottom {
    position: relative;
    left: -250px;
    opacity: 0.8;
}
#top {
    position: relative;
    bottom: 570px;
    right: -450px;
    opacity: 0.8;
}
#submit1 {
    position: relative;
    right: 250px;
}
#submit2 {
    position: relative;
    bottom: -150px;
}
</style>

<h1 id="bottom"><font color="white">Welcome/Goodbye Setup</h1></font>
<div class="panel-group" id="bottom">
  <div class="panel panel-info" style="width: 50%;">
    <div class="panel-heading"><h2>Welcome Message</h2></div>
    <div class="form-group">
    <form action="/pbot/submit1.php?sid=<?=$token?>" id="usrform" method="post">
   <textarea class="form-control" rows="5" form="usrform" name="entry_text"><?=$entry_text?></textarea>
  <div class="panel panel-info" style="width: 100%;">
    <div class="panel-heading"><h2>Welcome Message for PM</h2></div>
    <textarea class="form-control" rows="5" form="usrform" name="entry_text_pm"><?=$entry_text_pm?></textarea>
  </div>
  <div class="panel panel-info" style="width: 100%;">
    <div class="panel-heading"><h2>Goodbye Message</h2></div>
    <textarea class="form-control" rows="5" form="usrform" name="goodbye_text"><?=$goodbye_text?></textarea>
  </div>
</div>
</div>
</div>
<h2 id="bottom"><font color="white">
    Note:<br>
    {0} = User Name<br>
    {1} = Server Name<br>
</h2></font><br><br>
<button id="submit1" type="submit" class="btn btn-primary"><span class="glyphicon">&#xe013;</span> Save Changes</button>
</form>

<h1 id="top"><font color="white">Message Logging Setup</h1></font>
<div class="panel-group" id="top">
  <div class="panel panel-info" style="width: 50%;">
    <div class="form-group">
    <form action="/pbot/submit2.php?sid=<?=$token?>" id="usrform2" method="post">
  <div class="panel panel-info" style="width: 100%;">
    <div class="panel-heading"><h2>Logging</h2></div>
<?php
if($logging == "1"){
    echo'
    <div class="radio">
      <label><input type="radio" name="logging" value="1" checked>On</label>
    </div>
    <div class="radio">
      <label><input type="radio" name="logging" value="0">Off</label>
    </div>
    ';
}
else{
    echo'
    <div class="radio">
      <label><input type="radio" name="logging" value="1">On</label>
    </div>
    <div class="radio">
      <label><input type="radio" name="logging" value="0" checked>Off</label>
    </div>
    ';
}
if(empty($log_whitelist == false)){
    $whitelist = json_decode($log_whitelist,$assoc=true);
    $whitelist = implode(",",$whitelist);
    echo'
    </div>
    <div class="panel panel-info" style="width: 100%;">
      <div class="panel-heading"><h2>Whitelist</h2></div>
      <input type="text" class="form-control" id="whitelist" value="'.$whitelist.'" name="whitelist"><br>
      <left>Seperate entries with a "," (NO SPACES)</left>
    </div>
    ';
}
else{
    echo'
    </div>
    <div class="panel panel-info" style="width: 100%;">
      <div class="panel-heading"><h2>Whitelist</h2></div>
      <input type="text" class="form-control" id="whitelist" value="" placeholder="Enter the discord IDs of the users whose messages you dont want logged (Seperate them with a comma)" name="whitelist"><br>
      <left>Seperate entries with a "," (NO SPACES)</left>
    </div>
    ';
}

 ?>
  <div class="panel panel-info">
      <div class="panel-heading"><h2>Max warnings before ban</h2></div>
      <input type="text" class="form-control" id="whitelist" value="<?=$max_warnings?>" name="max_warns"><br>
    </div>
  <button id="submit2" type="submit" class="btn btn-primary"><span class="glyphicon">&#xe013;</span> Save Changes</button>
</form>
</div>
</div>
</div>
