
...

<?php
    if (isset($_GET['id'])) {
        $id = $_GET['id'];

        $sql_bad_words = ["UNION", "SELECT", "FROM", "WHERE", "union", "select", "from", "where", "flag"];
        foreach ($sql_bad_words as $bad_word) {
            if (strpos($id, $bad_word) !== false){
                $id = '1';
            }
        }
        $result = $db->query("SELECT id, name, image FROM psyducks WHERE id = " . $id);
        $data = $result->fetchArray();
    }
?>

...