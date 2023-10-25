<?php 
include '../init.php'; 

$note_id = $_GET['note'] ?: NULL;
$note = NULL;

$is_admin = is_current_user_protected();

if(!$note_id || !is_string($note_id)){
    store_message(true, "No note provided!");
    redirect("/");
} else {
    $note = ($is_admin
                ? get_note_for_admin($note_id) 
                : get_note(get_user_id(), $note_id));

    if(!$note){
        store_message(true, "Note not found!");
        redirect("/");
    } else if($note['is_blocked'] && !$is_admin) {
        store_message(true, "Message has been blocked by administrator!");
    } else if($note['is_reported']) {
        store_info_message("Be aware: Note is pending review from administrators due to abuse complains");
    }
}

include '../template/head.php';
?>
                        <div class="title">
                            <?php
                            echo '<h1>' . htmlentities($note['title']) . '</h1>';

                            if($note['is_public']){
                                echo '<span class="uk-badge">Public</span>';
                            }
                            
                            $encodedNodeId = htmlentities($note['id'], ENT_QUOTES);
                            echo '<div class="actions">';

                            if($note['is_public'])
                                echo '<a class="uk-button uk-button-primary" href="/view.php?note=' . $encodedNodeId . '" target="_blank"><i class="uk-icon-share-alt"></i> Share Link</a>';
                            
                            if($note['owner'] == get_user_id()){
                                echo '<a class="uk-button" href="/edit.php?note=' . $encodedNodeId . '"><i class="uk-icon-pencil"></i> Edit</a>';
                                echo '<a class="uk-button" href="/delete.php?note=' . $encodedNodeId . '"><i class="uk-icon-remove"></i> Delete</a>';
                            }

                            echo '<a class="uk-button" href="/report.php?note=' . $encodedNodeId . '" title="Report abuse to admin"><i class="uk-icon-bug"></i> Report</a>';
                            echo '</div>';
                            ?>
                        </div>
                        <div class="body">
                            <?= $note['is_blocked'] && !$is_admin ? '' : $note['content']; ?>
                        </div>
                    <?php
                    include '../template/bottom.php';
                    ?>