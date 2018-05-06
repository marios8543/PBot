<script defer src="/static/fontawesome/fontawesome-all.js"></script>
<link type="text/css" rel="stylesheet" href="/static/css/bootstrap.css">
<script src="/static/js/jquery-3.3.1.min.js"></script>
<script src="/static/js/bootstrap.js"></script>
<?php
include('utils.php');
class Dashboard{
	public $admin_id=0;
	public $admin_name = 0;
	public $server = 0;
	public $timestamp = 0;
	public $time_remaining = 0;

	public function __construct($time_remaining,$conn,$client,$admin_id,$server_id,$timestamp){
		$this->admin_id = $admin_id;
		$user = $client->user->getUser(['user.id'=>$admin_id+0]);
		$this->admin_name = $user->username.'#'.$user->discriminator;
		$this->server = get_server($client,$conn,$server_id);
		$this->timestamp = $timestamp;
		$this->time_remaining = date("H",$time_remaining).' hours and '.date("i",$time_remaining).' minutes';
	}
}

$token = $conn->escape_string($_COOKIE['token']);
$result = $conn->query("SELECT server_id,admin_id,valid,timestamp FROM setting_sessions WHERE token='$token'");
$result = mysqli_fetch_all($result);
$valid = $result[0][2];
$time_remaining = time()-strtotime($result[0][3]);
if($valid == 1 && $time_remaining<0 ){
	$dashboard = new Dashboard($time_remaining,$conn,$client,$result[0][1],$result[0][0],$result[0][3]);
}
else{
    header("Location:invalid.html");
}
 ?>