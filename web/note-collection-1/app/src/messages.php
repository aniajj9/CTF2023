<?php

function store_message(bool $error, string $message)
{
    if(!array_key_exists('messages', $_SESSION))
        $_SESSION['messages'] = [];
    
    $_SESSION['messages'][] = ['type' => ($error ? 'danger' : 'success'), 'message' => $message];
}

function store_info_message(string $message)
{
    if(!array_key_exists('messages', $_SESSION))
        $_SESSION['messages'] = [];
    
    $_SESSION['messages'][] = ['type' => 'info', 'message' => $message];
}

function get_messages()
{
    
    if(!array_key_exists('messages', $_SESSION))
        return [];
    
    $messages = $_SESSION['messages'];
    unset($_SESSION['messages']);
    return $messages;
}

function render_messages()
{
    $messages = get_messages();

    if(!$messages){
        return "";
    }

    echo "<div class='messages'>";
    foreach($messages as $alert)
    {
        if(in_array($alert['type'], ['danger','success','info'])){
            $class = $alert['type'] != 'info' ? 'uk-alert-' . $alert['type'] : '';
            echo "<div class=\"uk-alert {$class}\">" . htmlentities($alert['message']) . "</div>";
        }
    }
    echo "</div>";
}