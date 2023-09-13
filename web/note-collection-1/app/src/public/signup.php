<?php

include '../init.php';
require_no_authentication();

if(isset($_POST['username'])){
    if(!isset($_POST['username'],$_POST['password'],$_POST['password2']) ||
        !is_string($_POST['username']) || !is_string($_POST['password']) || !is_string($_POST['password2'])){
        store_message(true, "Please fill out all fields!");
    } else if($_POST['password'] !== $_POST['password2']) {
        store_message(true, "The provided passwords are not identical!");
    } else if(create_user($_POST['username'], $_POST['password']) !== false) {
        store_message(false, "User created!");
        redirect("/login.php");
    }
}
?><!DOCTYPE html>
<html>
    <head>
        <?php
        include '../template/meta.php';
        ?>
    </head>
    <body class="page-login">
        <div class="wrapper">
            <div id="content-area">
                <div id="content-wrapper">
                    <div class="content-box">
                        <?= render_messages(); ?>
                        <div class="body list">
                            <form class="uk-form" action="/signup.php" method="post">
                                <div class="uk-form-row uk-text-center">
                                    <h1>Register User</h1>
                                </div>
                                <div class="uk-form-row">
                                    <div class="uk-form-icon uk-width-1-1 ">
                                        <i class="uk-icon-user"></i>
                                        <input class="uk-width-1-1 uk-form-large" type="text" name="username" placeholder="Username" value="<?= postback('username'); ?>">
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <div class="uk-form-icon uk-width-1-1 ">
                                        <i class="uk-icon-lock"></i>
                                        <input class="uk-width-1-1 uk-form-large" type="password" name="password" placeholder="Password" value="<?= postback('password'); ?>">
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <div class="uk-form-icon uk-width-1-1 ">
                                        <i class="uk-icon-lock"></i>
                                        <input class="uk-width-1-1 uk-form-large" type="password" name="password2" placeholder="Repeat Password" value="<?= postback('password2'); ?>">
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <div class="uk-grid uk-grid-small uk-grid-width-1-2">
                                        <div>
                                            <button class="uk-width-1-1 uk-button uk-button-primary uk-button-large">Register</a>
                                        </div>
                                        <div>
                                            <a class="uk-width-1-1 uk-button uk-button-large" href="/login.php">Back</a>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>