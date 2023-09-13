<?php

// Define functions
function error($msg){
    echo "<div class='sql-error'><b>ERROR: </b>" . $msg . "</div>";
}

function debug($val){
    echo "<pre>";
    if((is_array($val) || is_object($val)) && count($val) > 0)
        print_r($val);
    else
        var_dump($val);
    echo "</pre>";
}

function post($key, $default = "")
{
    return isset($_POST[$key]) ? $_POST[$key] : $default;
}

function get($key, $default = "")
{
    return isset($_GET[$key]) ? $_GET[$key] : $default;
}

function escape($val)
{
    return htmlentities($val, ENT_QUOTES);
}

function msg($val, $color = 'err')
{
    echo "<div class='msg color-{$color}'>" . $val . "</div>";
}

// Load misc files
define('PATH', dirname(__FILE__) . '/');

include_once PATH . 'pdo.php';