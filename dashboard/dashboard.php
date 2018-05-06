<head>
<?php include("get_data.php"); ?>
</head>
<body background="/static/img/bg.png">
<?php include("sidenav.php"); ?>
<div id="content">
<div class="card bg-primary text-white">
	<div class="card-body"><b>Server Name:</b> <?=$dashboard->server->name?>&nbsp&nbsp&nbsp<b>Member Count:</b> <?=$dashboard->server->member_count?>&nbsp&nbsp&nbsp
</div>
</div>
</div>