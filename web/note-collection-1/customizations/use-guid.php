<?php

function create_note(string $title, string $content, bool $public)
{
    if(is_current_user_protected()){
        return false;
    }

    $noteId = create_uuid4();
    $db = getDB();
    $stmt = $db->prepare("INSERT INTO notes (id, title, is_public, content, `owner`) VALUES (?, ?, ?, ?, ?)");
    $success = $stmt->execute([
        $noteId,
        $title,
        $public ? 1 : 0,
        $content,
        get_user_id()
    ]);
    
    
    return $success ? $noteId : false;
}

function create_uuid4()
{
    $data = openssl_random_pseudo_bytes(16);
    $data[6] = chr(ord($data[6]) & 0x0f | 0x40);    // set version to 0100
    $data[8] = chr(ord($data[8]) & 0x3f | 0x80);    // set bits 6-7 to 10
    return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}