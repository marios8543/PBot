<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<style>
body {
    font-family: "Lato", sans-serif;
}

.sidenav {
    height: 100%;
    width: 250px;
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    background-color: #111;
    overflow-x: hidden;
    transition: 0.5s;
    padding-top: 10px;
    opacity: 0.8;
}

.sidenav a {
    padding: 8px 8px 8px 32px;
    text-decoration: none;
    font-size: 25px;
    color: #818181;
    display: block;
    transition: 0.3s;
}

.sidenav a:hover {
    color: #f1f1f1;
}

@media screen and (max-height: 450px) {
  .sidenav {padding-top: 15px;}
  .sidenav a {font-size: 18px;}
}
</style>
</head>
<body>

<div align="left" id="mySidenav" class="sidenav">
  <a href="#"><img src="https://raw.githubusercontent.com/marios8543/kamina-backend/master/kamina_white.png" alt="Kamina" height="55" width="55">&nbsp>PBot
  <a href="dashboard.php"><span class="glyphicon">&#xe141;</span> Dashboard</a>
  <a href="members.php"><span class="glyphicon">&#xe008;</span> Members</a>
  <a href="warnings.php"><span class="glyphicon">&#xe107;</span> Warnings</a>
  <a href="forms.php"><span class="glyphicon">&#xe056;</span> Forms</a>
  <a href="settings.php"><span class="glyphicon">&#xe136;</span> Settings</a>
  <br><br>
  <a href="#" onclick="myFunction();"><span class="glyphicon">&#xe163;</span> Exit</a>
  <br><br><br>
<div align="center">
  <font size="3" color="grey">
  Server: <?=$server_name?><br>
  Requested by: <?=$admin_name?><br>
  Timestamp: <?=$timestamp?>
</font>
</div>
</div>
<script>
function myFunction() {
    if (confirm("This will invalidate the current session. You will need to create a new one by executing >>dashboard in your server.") == true) {
        window.location = "/pbot/kill_session.php";
    } else {
        txt = "You pressed Cancel!";
    }
}
</script>
</body>
