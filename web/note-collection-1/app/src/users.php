<?php

function create_user(string $username, string $password)
{
    if($username === $password){    
        store_message(true, "Username and password cannot be identical!");
        return false;
    }

    if(strlen($password) < 8){  
        store_message(true, "Password should be at least 8 characters long!");
        return false;
    }

    try
    {
        $db = getDB();
        $stmt = $db->prepare("INSERT INTO users (name, password) VALUES (?, ?)");
        $success = $stmt->execute([
            $username,
            password_hash($password, PASSWORD_DEFAULT)
        ]);
        
        return $success ? $db->lastInsertId() : false;
    } catch(PDOException $exception){
        if($exception->errorInfo[1] === 1062){
            store_message(true, "Username is already taken!");
            return false;
        }
        throw $exception;
    }
}

function login($username, $password)
{
    $standardError = 'Incorrect username or password!';

    if(!$username || !is_string($username) || !$password || !is_string($password)){
        return $standardError;
    }

    $users = query("SELECT id, name, password FROM users WHERE name=?", [$username]);

    if(!$users || count($users) != 1){
        return $standardError;
    }

    $targetUser = end($users);
    if(!password_verify($password, $targetUser['password'])){
        return $standardError;
    }

    $_SESSION['userid'] = (string)$targetUser['id'];
    return true;
}

function get_user_id() : ?string
{
    return $_SESSION['userid'] ?? NULL;
}

function is_logged_in() : bool
{
    return !empty(get_user_id());
}

function require_authentication()
{
    if(is_logged_in())
        return true;
    
    redirect("/login.php");
}

function require_no_authentication()
{
    if(!is_logged_in())
        return true;
    
    store_message(true, "Action failed");
    redirect('/');
}

function redirect($url)
{
    header("Location: " . $url);
    exit();
}