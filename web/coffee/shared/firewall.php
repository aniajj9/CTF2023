<?php

if(preg_match("#sqlmap#i", $_SERVER['HTTP_USER_AGENT'])){
    die("You should really try these exercises by hand. They are indeed doable and that way, you will learn something!");
}