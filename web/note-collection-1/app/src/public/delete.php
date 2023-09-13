<?php 
include '../init.php'; 
require_authentication();

$noteId = $_GET['note'] ?: NULL;
$isValidId = $noteId && is_string($noteId);
$note = $isValidId ? get_note(get_user_id(), $noteId) : NULL;

if(!$note){
    store_message(true, "Is hard to delete a non-existing note!");
    redirect("/");
}

if(!$note['owner'] || $note['owner'] != get_user_id()){
    store_message(true, "You are not the owner of said note!");
    redirect("/");
}

if(delete_note($note['id'])){
    store_message(false, "The note has been permanently deleted");
    redirect("/");
} else {
    store_message(true, "Failed to delete note");
    redirect("/view.php?note=" . urlencode($noteId));
}
