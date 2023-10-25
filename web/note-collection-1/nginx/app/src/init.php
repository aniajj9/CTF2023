<?php

$pathCustomizations = "/customizations/";
$customizations = array_diff(scandir($pathCustomizations), array('..', '.'));
foreach($customizations as $filename)
{
    if(substr($filename, -4) === ".php"){
        include $pathCustomizations . $filename;
    }
}

function env(string $key, bool $required = true)
{
    $value = getenv($key);

    if(($value === false || $value === '') && $required){
        throw new Exception("Missing environment value '$key'");
    }

    return $value;
}

include 'dbo.php';
include 'form.php';
include 'messages.php';
include 'notes.php';
include 'users.php';

session_start();