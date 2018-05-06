<?php
include('db_conn.php');

function get_server($client,$conn,$id){
    $id = $conn->escape_string($id);
    $sql="SELECT added_on,entry_text,entry_text_pm,
    goodbye_text,log_whitelist,welcome_channel,
    goodbye_channel,event_channel,log_channel,
    log_active,max_warns FROM servers WHERE id='$id'";
    $res = $conn->query($sql);
    $disc_guild = $client->guild->getGuild(['guild.id'=>(int)$id]);
    if($res->num_rows > 0){
        $res=mysqli_fetch_all($res);
        $server = new Server();
        $server->id = $id;
        $server->name = $disc_guild->name;
        $server->added_on = $res[0][0];
        $server->entry_text = $res[0][1];
        $server->entry_text_pm = $res[0][2];
        $server->goodbye_text = $res[0][3];
        $server->log_whitelist = json_decode($res[0][4]);
        $server->welcome_channel = $res[0][5];
        $server->goodbye_channel = $res[0][6];
        $server->event_channel = $res[0][7];
        $server->log_channel = $res[0][8];
        $server->log_active = json_decode($res[0][9]);
        $server->max_warnings = $res[0][10];
        $server->disc_server = $disc_guild;
        $server->member_count = count($client->guild->listGuildMembers(['guild.id'=>$id+0]));
        return $server;
    }
}

class Server{
    public $id=0;
    public $name=0;
    public $added_on=0;
    public $welcome_channel=0;
    public $goodbye_channel=0;
    public $event_channel=0;
    public $log_channel=0;
    public $log_active=0;
    public $log_whitelist=0;
    public $entry_text=0;
    public $entry_text_pm=0;
    public $goodbye_text=0;
    public $max_warnings=0;
    public $disc_server=0;
    public $member_count=0;

    public function update(){
        $welcome_channel=$conn->escape_string($this->welcome_channel);
        $goodbye_channel=$conn->escape_string($this->goodbye_channel);
        $event_channel=$conn->escape_string($this->event_channel);
        $log_channel=$conn->escape_string($this->log_channel);
        $entry_text=$conn->escape_string($this->entry_text);
        $entry_text_pm=$conn->escape_string($this->entry_text_pm);
        $goodbye_text=$conn->escape_string($this->goodbye_text);
        $max_warnings=$conn->escape_string($this->max_warnings);
        $log_active=json_encode($this->log_active);
        $log_whitelist=json_encode($this->log_whitelist);

        $sql = "UPDATE servers SET 
        welcome_channel='$welcome_channel',
        goodbye_channel='$goodbye_channel',
        event_channel='$event_channel',
        log_channel='$log_channel',
        log_active='$log_active',
        log_whitelist='$log_whitelist',
        entry_text='$entry_text',
        entry_text_pm='$entry_text_pm',
        goodbye_text='$goodbye_text',
        max_warns='$max_warnings'
        ";
        if ($conn->query($sql)){
            echo 'Server updated successfully';
        } else {
            echo 'alert("An error occured! '.$conn->error.'")';
        }
    }
}

?>