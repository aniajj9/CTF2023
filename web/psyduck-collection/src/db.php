
<?php
    class psyduckDB extends SQLite3 {
        function __construct() {
            $this->open('/var/www/data/psyduck.db');
        }
    }
    $db = new psyduckDB();
    if(!$db) {
        echo $db->lastErrorMsg();
    } else {
        # psyducks
        $db->exec('CREATE TABLE IF NOT EXISTS "psyducks" ( "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" INTEGER, "image" VARCHAR)');

        $db->exec('BEGIN');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Infinte Psyduck", "psy_4ever.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Dancing Psyduck", "psy_dance.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Moving Psyduck", "psy_move.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Rainbow Psyduck", "psy_rainbow.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Xmas Psyduck", "psy_xmas.png")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Just Psyduck", "psy1.png")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Celebrating Psyduck", "psy_celebrate.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Strong Psyduck", "psy_strong.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Poolday Psyduck", "psy_poolday.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Drowning Psyduck 😭", "psy_drown.gif")');
        $db->query('INSERT INTO "psyducks" ("name", "image")
            VALUES ("Hacker Psyduck", "psy_hacks.gif")');
        $db->exec('COMMIT');

        # flag
        $db->exec('CREATE TABLE IF NOT EXISTS "secret_table" ( "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "flag" VARCHAR)');

        $db->exec('BEGIN');
        $db->query('INSERT INTO "secret_table" ("flag")
            VALUES ("' . $_ENV["flag"] . '")');
        $db->exec('COMMIT');
    }
?>
