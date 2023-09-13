<?php 
include '../init.php'; 
require_authentication();

if(isset($_POST['visibility'])){
    if(!isset($_POST['visibility'], $_POST['title'], $_POST['content']) || empty($_POST['title'])){
        store_message(true, "Please fill out all fields!");
    } elseif(create_note($_POST['title'], $_POST['content'], $_POST['visibility'] === 'public')) {
        store_message(false, "Note saved");
        redirect("/");
    } else {
        store_message(true, "Failed to save message. Please try again");
    }
}

include '../template/head.php';
?>
                        <div class="title">
                            <h1>Create Note</h1>
                        </div>
                        <div class="body">
                            <form class="uk-form uk-form-horizontal" method="post" action="/create.php">
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="title">Title:</label>
                                    <div class="uk-form-controls">
                                        <input type="text" placeholder="Title of your note goes here" id="title" name="title" class="uk-width-1-1" value="<?= postback('title') ?>">
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="visibility">Visibility:</label>
                                    <div class="uk-form-controls">
                                        <select name="visibility" id="visibility" class="uk-width-1-1">
                                        <option value="private">Private/Hidden</option>
                                            <option value="public" <?= (($_POST['visibility'] ?? '') === 'public' ? ' selected' : ''); ?>>Public</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="post-content">Content:</label>
                                    <div class="uk-form-controls">
                                        <textarea placeholder="Offload your head into this section. We will store it securely!" id="post-content" name="content" class="uk-width-1-1" rows="15"><?= postback('content') ?></textarea>
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="post-content"></label>
                                    <div class="uk-form-controls">
                                        <button class="uk-button uk-button-primary">Create</button>
                                        <a class="uk-button" href="/">Cancel</a>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <?php
                        include '../template/bottom.php';
                        ?>