<?php

function postback(string $key)
{
    return htmlentities($_POST[$key] ?? '', ENT_QUOTES);
}