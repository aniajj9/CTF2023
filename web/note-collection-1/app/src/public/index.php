<?php 
include '../init.php'; 
require_authentication();
include '../template/head.php';

?>
                        <div class="title">
                            <h1>Note Collection</h1>
                        </div>
                        <div class="body no-padding list">
                        <?php
                        $notes = get_notes(get_user_id());

                        if(!$notes){
                            echo '<p class="list-empty">You have no saved notes.</p>';
                        } else {
                            echo '<ul>';
                            foreach($notes as $note)
                            {
                                $badge = $note['is_public'] ? ' <span class="uk-badge">Public</span>' : '';
                                echo sprintf('<li><i class="uk-icon-caret-right"></i> <a href="/view.php?note=%s">%s</a>%s</li>',
                                        $note['id'],
                                        htmlentities($note['title']),
                                        $badge
                                    );
                            }
                            echo '</ul>';
                        }
                        ?>
                        </div>
                    <?php 
                    include '../template/bottom.php';
                    ?>