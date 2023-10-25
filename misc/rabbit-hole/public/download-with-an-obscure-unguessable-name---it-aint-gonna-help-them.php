<?php

include '/srv/private/passwords.php';

function redirect($counter){
    global $passwords;
    $url = "/downloads/flags/$counter/" . $passwords[$counter];
    die("<a href='" . $url . "'><img src='/we-need-to-go-deeper.jpg'></a>");
}

$counter  = (int)$_GET['counter'] ?? NULL;
$password = $_GET['password'] ?? NULL;
$referrer = $_SERVER['HTTP_REFERER'] ?? NULL;

// Validate referrer
if(!$referrer){
    header("Content-Type: image/jpg");
    @readfile("no-just-no.jpg");
    exit;
}

$parsed = parse_url($referrer);

if($parsed['host'] !== $_SERVER['HTTP_HOST']){
    header("Content-Type: image/jpg");
    @readfile("no-just-no.jpg");
    exit;
}

// Init
if($counter === 10000){
    redirect($counter - 1);
}

// Validate counter
if(!array_key_exists($counter, $passwords)){
    header("Content-Type: image/jpg");
    @readfile("are-you-kidding.jpg");
    exit;
}

if($passwords[$counter] !== $password){
    header("Content-Type: image/jpg");
    @readfile("are-you-kidding.jpg");
    exit;
}

// Goal
if($counter === 1){
    die("<a href='/'><img src='/fuck-we-went-too-far.jpg'></a>");
}

if($counter === 17){
    @readfile("/srv/private/flag.txt");
}

redirect($counter - 1);