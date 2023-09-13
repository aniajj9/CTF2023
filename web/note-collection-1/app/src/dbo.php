<?php

function getDB(){
    try 
    {
        $host = env('DB_HOST');
        $user = env('DB_USER');
        $pass = env('DB_PASSWORD');
        $name = env('DB_NAME');

        return new PDO("mysql:host=$host;dbname=$name", $user, $pass);
    } catch (Exception $ex) {
        throw new Exception("Failed to connect to database!");
    }
}

function query(string $sql, array $params = [])
{
    $stmt = getDB()->prepare($sql);
    if(!$stmt->execute($params)){
        throw new Exception("Failed to query database! Sql was '$sql'");
    }

    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}