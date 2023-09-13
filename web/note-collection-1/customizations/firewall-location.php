<?php

if(!is_array($_REQUEST)){
    return;
}

foreach($_REQUEST as $key => $value)
{
    if(strpos($value, '<script') !== false || stripos($value, "location") !== false || stripos($value, "<meta") !== false){
        header("Content-type: text/plain");
        die('"AI-based firewall detected malicious content: ' . htmlentities($value, ENT_SUBSTITUTE | ENT_HTML401 ) . '"');
    }
}