<style>
@import "https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700";
p {
    font-family: 'Poppins', sans-serif;
    font-size: 1.1em;
    font-weight: 300;
    line-height: 1.7em;
    color: #999;
}
a, a:hover, a:focus {
    color: inherit;
    text-decoration: none;
    transition: all 0.3s;
}
.navbar {
    padding: 15px 10px;
    background: #fff;
    border: none;
    border-radius: 0;
    margin-bottom: 40px;
    box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}
.navbar-btn {
    box-shadow: none;
    outline: none !important;
    border: none;
}
.line {
    width: 100%;
    height: 1px;
    border-bottom: 1px dashed #ddd;
    margin: 40px 0;
}
.wrapper {
    display: flex;
    align-items: stretch;
}

#sidebar {
    min-width: 250px;
    max-width: 250px;
    background: #7386D5;
    color: #fff;
    transition: all 0.3s;
}

#sidebar.active {
    margin-left: -250px;
}

#sidebar .sidebar-header {
    padding: 20px;
    background: #6d7fcc;
}
#sidebar ul.components {
    padding: 20px 0;
    border-bottom: 1px solid #47748b;
}
#sidebar ul p {
    color: #fff;
    padding: 10px;
}
#sidebar ul li a {
    padding: 10px;
    font-size: 1.1em;
    display: block;
}
#sidebar ul li a:hover {
    color: #7386D5;
    background: #fff;
}
#sidebar ul li.active > a, a[aria-expanded="true"] {
    color: #fff;
    background: #6d7fcc;
}
a[data-toggle="collapse"] {
    position: relative;
}
a[aria-expanded="false"]::before, a[aria-expanded="true"]::before {
    content: '\e259';
    display: block;
    position: absolute;
    right: 20px;
    font-family: 'Glyphicons Halflings';
    font-size: 0.6em;
}
a[aria-expanded="true"]::before {
    content: '\e260';
}
ul ul a {
    font-size: 0.9em !important;
    padding-left: 30px !important;
    background: #6d7fcc;
}

ul.CTAs {
    padding: 20px;
}

ul.CTAs a {
    text-align: center;
    font-size: 0.9em !important;
    display: block;
    border-radius: 5px;
    margin-bottom: 5px;
}

a.download {
    background: #fff;
    color: #7386D5;
}

a.article, a.article:hover {
    background: #6d7fcc !important;
    color: #fff !important;
}
#content {
    padding: 20px;
    min-height: 100vh;
    transition: all 0.3s;
}
@media (max-width: 768px) {
    #sidebar {
        margin-left: -250px;
    }
    #sidebar.active {
        margin-left: 0;
    }
    #sidebarCollapse span {
        display: none;
    }

}    
</style>
<div class="wrapper" id="sidenav">
            <nav id="sidebar">
                <div class="sidebar-header">
                    <h3><img src="/static/img/kamina.png" alt="Kamina" height="55" width="55">>PBot</h3>
                </div>

                <ul class="list-unstyled components">
                    <b>Server name:</b><br> <?=$dashboard->server->name?><br>
                    <b>Admin name:</b><br> <?=$dashboard->admin_name?><br>
                    <b>Time remaining:</b><br> <?=$dashboard->time_remaining?><br>
                    <li>
                        <a href="#"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
                        <a href="#pageSubmenu" data-toggle="collapse" aria-expanded="false"><i class="fas fa-wrench"></i> Settings</a>
                        <ul class="collapse list-unstyled" id="pageSubmenu">
                            <li><a href="#" onclick="$("set_channels").scrollIntoView();"><i class="fas fa-tv"></i> Channels</a></li>
                            <li><a href="#" onclick="$("set_messages").scrollIntoView();"><i class="fas fa-comment-alt"></i> Messages</a></li>
                            <li><a href="#" onclick="$("set_warnings").scrollIntoView();"><i class="fas fa-exclamation-triangle"></i> Warnings</a></li>
                            <li><a href="#" onclick="$("set_logging").scrollIntoView();"><i class="fas fa-folder-open"></i> Logging</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="#" onclick="exit();"><i class="fas fa-sign-out-alt"></i> Exit</a>
                    </li>
                    <li>
                        <a href="/help">Documentation</a>
                    </li>
                    <li>
                        <a href="https://discord.gg/XACSrhZ">Help Server</a>
                    </li>
                </ul>

                <ul class="list-unstyled CTAs">
                    <li><a href="https://github.com/marios8543/PBot" class="download"><i class="fab fa-github"></i> Fork on Github</a></li>
                    <li><a href="https://discordapp.com/api/oauth2/authorize?client_id=381066546535202816&permissions=8&scope=bot" class="article"><i class="fab fa-discord"></i> Invite link</a></li>
                </ul>
            </nav>         
<script>
    function exit(){
    if(confirm("This will invalidate the current session. You will need to create a new one by executing >>dashboard in your server.")){
        window.location = "/kill_session.php";
    }
}
         
</script>
