<?php

if(!function_exists('create_note')){
    function create_note(string $title, string $content, bool $public)
    {
        if(is_current_user_protected()){
            return false;
        }
        
        $db = getDB();
        $stmt = $db->prepare("INSERT INTO notes (title, is_public, content, `owner`) VALUES (?, ?, ?, ?)");
        $success = $stmt->execute([
            $title,
            $public ? 1 : 0,
            $content,
            get_user_id()
        ]);
        
        
        return $success ? $db->lastInsertId() : false;
    }
}

function update_note(string $note_id, string $title, string $content, bool $public)
{
    if(is_current_user_protected()){
        return false;
    }
    
    $db = getDB();
    $stmt = $db->prepare("UPDATE notes SET title=?, is_public=?, content=?, is_blocked=0, reported=NULL WHERE id=? AND owner=?");
    return (bool)$stmt->execute([
        $title,
        $public ? 1 : 0,
        $content,
        $note_id,
        get_user_id()
    ]);
}

function is_current_user_protected()
{
    return (get_user_id() === "1");
}

function report_note(string $id)
{
    if(is_current_user_protected()){
        return false;
    }

    return getDB()
            ->prepare("UPDATE notes SET reported=NOW() WHERE id=? AND is_blocked=0 AND reported IS NULL")
            ->execute([$id]);
}

function delete_note(string $id)
{
    $user = get_user_id();
    if(!$user){
        return false;
    }

    if(is_current_user_protected()){
        return false;
    }
    
    return getDB()
            ->prepare("DELETE FROM notes WHERE id=? AND owner=?")
            ->execute([$id, $user]);
}

function get_notes(string $owner)
{
    return query("SELECT id, title, is_public, content, owner, !ISNULL(reported) AS is_reported, is_blocked FROM notes WHERE `owner`=?", [$owner]);
}

function get_note(?string $owner, string $id)
{
    $owner = $owner === NULL ? -1 : $owner;
    $notes = query("SELECT id, title, is_public, content, owner, !ISNULL(reported) AS is_reported, is_blocked FROM notes WHERE (`owner`=? OR is_public=1) AND id=? LIMIT 1", [$owner, $id]);
    return ($notes ? end($notes) : $notes);
}

function get_my_note(string $owner, string $id)
{
    $notes = query("SELECT id, title, is_public, content, owner, !ISNULL(reported) AS is_reported, is_blocked FROM notes WHERE `owner`=? AND id=? LIMIT 1", [$owner, $id]);
    return ($notes ? end($notes) : $notes);
}

function get_note_for_admin(string $id)
{
    $notes = query("SELECT id, title, is_public, content, owner, !ISNULL(reported) AS is_reported, is_blocked FROM notes WHERE id=? LIMIT 1", [$id]);
    return ($notes ? end($notes) : $notes);
}