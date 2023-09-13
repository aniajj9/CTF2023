<!DOCTYPE html>
<html>
    <head>
        <?php include 'meta.php'; ?>
    </head>
    <body>
        <div class="wrapper">
            <div id="content-area">
                <div id="content-wrapper">
                    <div class="arrow-start">
                        <?php
                        if(stripos($_SERVER['SCRIPT_NAME'],'index.php') !== false){
                            echo '<a href="/create.php"><i class="uk-icon-plus-circle"></i></a>';
                        } else {
                            echo '<a href="/index.php"><i class="uk-icon-caret-left"></i></a>';
                        }
                        ?>
                    </div>
                    <div class="content-box">
                        <?php render_messages(); ?>