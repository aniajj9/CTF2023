<?php

echo "<form><input placeholder=Command name=command maxlen=250 autofocus> <input type=submit value=Execute></form><br>";

if(!isset($_REQUEST['command'])){
    highlight_file(__FILE__);
    exit;
}

if(strpos($_REQUEST['command'], '&') !== false || preg_match('#[(<>)&;`$|]#', $_REQUEST['command']) || preg_match("{[^/\w./\-/\s]}", $_REQUEST['command'])){
    die("No no no!");
}

try
{
    @shell_exec($_REQUEST['command'] . " > /dev/null &");
} catch(Exception $e){
    // It's blind anyway!
}