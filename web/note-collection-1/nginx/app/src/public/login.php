<?php 
include '../init.php'; 

if(is_logged_in()){
    redirect("/");
}

if(isset($_POST['username'], $_POST['password'])){
    $result = login($_POST['username'], $_POST['password']);

    if($result === true){
        redirect("/");
    } else {
        store_message(true, $result);
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
                        <?php render_messages(); ?>
                        <div class="body list">
                            <form class="uk-form" action="/login.php" method="post">
                                <div class="uk-form-row uk-text-center">
                                    <h1>Note Collection</h1>
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
                                    <button class="uk-width-1-1 uk-button uk-button-primary uk-button-large" id="btn-login">Login</a>
                                </div>
                                <div class="uk-form-row uk-text-small">
                                    <a class="uk-float-left uk-link uk-link-muted" href="/signup.php">Create Account</a>
                                    <a class="uk-float-right uk-link uk-link-muted" href="#tooBad">Forgot Password?</a>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>