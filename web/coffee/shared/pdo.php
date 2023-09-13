<?php

function connect($usr, $pwd, $host="localhost"){
    try
    {        
        $db = new PDO("mysql:host=$host;dbname=$usr;charset=utf8mb4", $usr, $pwd, 
        array(
            PDO::ATTR_EMULATE_PREPARES => false, 
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
        ));
        return $db;
    } catch(Exception $e){
        return false;
    }
}

class SQLResult
{
    private $stmt;

    public function __construct($result)
    {
        $this->stmt = $result;
    }

    public static function parse($result)
    {
        if(!$result)
            return false;
        
        return new SQLResult($result);
    }

    public function numRows()
    {
        return $this->stmt->rowCount();
    }

    public function fetchField()
    {
        $row = $this->stmt->fetch(PDO::FETCH_NUM);

        return ($row !== false ? $row[0] : false);
    }

    public function fetchRow()
    {
        return $this->stmt->fetch(PDO::FETCH_BOTH);
    }
}

function prepare($db, $command, $params, $silent = false){
    if(!$db)
        return false;

    try
    {
        $stmt = $db->prepare($command);
        if(!$stmt->execute($params))
            return false;
        return $stmt;
    } catch(PDOException  $e){
        if(!$silent)
            error($e->getMessage());
    } catch(Exception $e){
        
    }
    return false;
}

function sql($db, $command, $silent = false){
    if(!$db)
        return false;
    
    try {
        return @$db->query($command);
    } catch(PDOException  $e){
        if(!$silent)
            error($e->getMessage());
    } catch(Exception $e){
        
    }
    return false;
}
