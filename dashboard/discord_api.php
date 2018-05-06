<?php

function request($url, $token)
{
    $curl = curl_init($url);
	curl_setopt($curl, CURLOPT_POST, true);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Authorization: Bot $token"));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($curl);
    curl_close($curl);
    return $response;
}

class Guild{
	public $id=0;
	public $name=0;
	public $icon=0;
	public $owner_id=0;
	public $region=0;
}