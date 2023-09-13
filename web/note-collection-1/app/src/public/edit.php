<?php 
include '../init.php'; 
require_authentication();

// Fetch note
$note_id = $_GET['note'] ?: NULL;
if(!$note_id || !is_string($note_id)){
    store_message(true, "No note provided!");
    redirect("/");
} else {
    $note = get_my_note(get_user_id(), $note_id);

    if(!$note){
        store_message(true, "Note not found!");
        redirect("/");
    }
}

// Update
if(isset($_POST['visibility'])){
    if(!isset($_POST['visibility'], $_POST['title'], $_POST['content']) || empty($_POST['title'])){
        store_message(true, "Please fill out all fields!");
    } elseif(update_note($note_id, $_POST['title'], $_POST['content'], $_POST['visibility'] === 'public')) {
        store_message(false, "Note updated");
    } else {
        store_message(true, "Failed to save note. Please try again");
    }
}


include '../template/head.php';

$is_public = $note['is_public'];

if(isset($_POST['visibility']) && $_POST['visibility'] === 'public')
    $is_public = true;

?>
                        <div class="title">
                            <h1>Edit Note</h1>
                        </div>
                        <div class="body">
                            <form class="uk-form uk-form-horizontal" method="post" action="/edit.php?note=<?= htmlentities($note_id, ENT_QUOTES) ?>">
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="title">Title:</label>
                                    <div class="uk-form-controls">
                                        <input type="text" placeholder="Title of your note goes here" id="title" name="title" class="uk-width-1-1" value="<?= postback('title') ?: htmlentities($note['title'], ENT_QUOTES) ?>">
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="visibility">Visibility:</label>
                                    <div class="uk-form-controls">
                                        <select name="visibility" id="visibility" class="uk-width-1-1">
                                        <option value="private">Private/Hidden</option>
                                            <option value="public" <?= ($is_public ? ' selected' : ''); ?>>Public</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="post-content">Content:</label>
                                    <div class="uk-form-controls">
                                        <textarea placeholder="Offload your head into this section. We will store it securely!" id="post-content" name="content" class="uk-width-1-1" rows="15"><?= postback('content') ?: htmlentities($note['content']) ?></textarea>
                                    </div>
                                </div>
                                <div class="uk-form-row">
                                    <label class="uk-form-label" for="post-content"></label>
                                    <div class="uk-form-controls">
                                        <button class="uk-button uk-button-primary">Save</button>
                                        <a class="uk-button" href="/">Cancel</a>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <?php
                        include '../template/bottom.php';
                        ?>