<?php 
if (isset($_GET["id"])) {
   if (explode(" ", $_GET["id"])[0] < 1) {
        header("Location: /?id=11"); 
        exit();
    }
    if (explode(" ", $_GET["id"])[0] >= 12) {
        header("Location: /?id=1"); 
        exit();
    }
} else {
    header("Location: /?id=1"); 
    exit();
}
include 'db.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/assets/style.css" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <title>psyduck selection</title>
</head>
<body>
    <div class="main">
        <!-- I fixed Bob's stupid Union selection typo -->
        <h1>Welcome to the Psyduck collection</h1>
        <h4>We have the most beautiful psyducks and all you need to do is go through the selection and choose your favorite one</h4>
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
        <div class="psyduck_img_container">
            <img class="psyduck_img" src="/assets/images/<?php echo $data["image"] ?>" />
        </div>
        <!-- Credit https://codepen.io/slimsmearlapp/pen/HJgFG-->
        <div class="button-container">
            <button class="third" onclick="window.location.href = '/?id=<?php echo ($_GET['id'] - 1); ?>'" value="Redirect">Back</button>
            <h3><?php echo $data["name"] ?></h3>
            <button class="third" onclick="window.location.href = '/?id=<?php echo ($_GET['id'] + 1); ?>'" value="Redirect">Next</button>
        </div>
    </div>
    <!-- <a href="https://www.flaticon.com/free-icons/ui" title="ui icons">Ui icons created by judanna - Flaticon</a> -->
    <!-- <a id="pause" href="https://www.flaticon.com/free-icons/stop" title="stop icons"></a> -->
    <img id="play" class="br" src="assets/images/play.png" />
    <img id="pause" class="br" src="assets/images/pause.png" />
    <script src="https://code.jquery.com/jquery-3.6.4.min.js" integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>
    <script>

        var audio = new Audio('assets/audio/hag.wav');

        $("document").ready(() => {
            $("#pause").hide();
        });
        $("#play").click(function() {
            audio.play();
            $("#play").hide();
            $("#pause").show();
        });
        $("#pause").click(function() {
            audio.pause();
            $("#pause").hide();
            $("#play").show();
        });
    </script>
</body>
</html>
