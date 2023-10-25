<?php 
include '../init.php'; 

$noteId = $_GET['note'] ?: NULL;
$isValidId = $noteId && is_string($noteId);
$note = $isValidId ? get_note(get_user_id(), $noteId) : NULL;

if(!$note){
    store_message(true, "Is hard to report a non-existing note!");
    redirect("/");
}

if($note['is_reported'] || $note['is_blocked']){
    store_message(true, "Note has already been reported!");
    redirect("/");
}

if(report_note($note['id']))
    store_message(false, "Note has been reported. An administrator will review it shortly");
else
    store_message(true, "Failed to report the note. Please try again or contact support. This is not intended");

redirect("/");