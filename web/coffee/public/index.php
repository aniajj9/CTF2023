<?php

include '/var/www/shared/generic.php';

$usr = getenv('DB_USER');
$pwd = getenv('DB_PASSWORD');

?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Secure Coffee</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Oxygen:400,300,700" rel="stylesheet" type="text/css"/>
    <link href="https://code.ionicframework.com/ionicons/1.4.1/css/ionicons.min.css" rel="stylesheet" type="text/css"/>
    <link rel="stylesheet" type="text/css" media="screen" href="/css/style.css" />
    <link rel="stylesheet" type="text/css" media="screen" href="/css/ribbon.css" />

    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
</head>
<body>
    
<div id="app">
  <div class="signin cf">
    <div class="avatar"></div>
    <?php
    $errors = NULL;
    $completed = false;

    if(isset($_POST['pass'],$_POST['name'])){
      ob_start();

      if(!($db = connect($usr, $pwd, "database"))){
        error("Could not connect to database");
        $errors = ob_get_clean();
      } else {
        $sql = "SELECT COUNT(*) FROM users WHERE username='" . $_POST['name'] . "' AND password='" . $_POST['pass'] . "'";
        $res = SQLResult::parse(sql($db, $sql, $silent = false));
        
        $errors = ob_get_clean();

        if($res)
        {
          if($res->numRows() == 0 OR $res->fetchField() == 0)
            msg( "No such user!", 'err');
          else 
            $completed = true;
        }
      }
    }
    
    if(!$completed){
    ?>
    <form method="post" autocomplete="off"> 
      <div class="inputrow">
        <input type="text" id="name" placeholder="Username" autocomplete="off" v-model="username" name="name" />
        <label class="ion-person" for="name"></label>
      </div>
      <div class="inputrow">
        <input type="password" id="pass" placeholder="Password" autocomplete="off" v-model="password" name="pass" />
        <label class="ion-locked" for="pass"></label>
      </div>
      <input type="checkbox" name="remember" id="remember"/>
      <label class="radio" for="remember">Stay Logged In</label>
      <input type="submit" value="Login" />
    </form>
    <?php 
      echo $errors; 
    } else {
      echo "<h2>Welcome!</h2>";
      echo "<p>Your secret flag is: <code class='flag'>" . getenv("FLAG") . "</code></p>";
    }
    
    ?>
  </div>


  <div id="debug" class="signin">
    <div class="ribbon ribbon-top-right"><span>Debug</span></div>
    <p id="sql" class="syntax" v-html="syntaxHighlightedQuery"></p>
  </div>
</div>

<script>
new Vue({
  el: '#app',
  data() {
    return {
      username: this.decode('<?= escape(post('name')); ?>'),
      password: this.decode('<?= escape(post('pass')); ?>'),
      keywords: {'ACCESSIBLE':'','ADD':'','ALL':'','ALTER':'','ANALYZE':'','AND':'','AS':'','ASC':'','ASENSITIVE':'','BEFORE':'','BETWEEN':'','BIGINT':'','BINARY':'','BLOB':'','BOTH':'','BY':'','CALL':'','CASCADE':'','CASE':'','CHANGE':'','CHAR':'','CHARACTER':'','CHECK':'','COLLATE':'','COLUMN':'','CONDITION':'','CONSTRAINT':'','CONTINUE':'','CONVERT':'','CREATE':'','CROSS':'','CURRENT_DATE':'','CURRENT_TIME':'','CURRENT_TIMESTAMP':'','CURRENT_USER':'','CURSOR':'','DATABASE':'','DATABASES':'','DAY_HOUR':'','DAY_MICROSECOND':'','DAY_MINUTE':'','DAY_SECOND':'','DEC':'','DECIMAL':'','DECLARE':'','DEFAULT':'','DELAYED':'','DELETE':'','DESC':'','DESCRIBE':'','DETERMINISTIC':'','DISTINCT':'','DISTINCTROW':'','DIV':'','DOUBLE':'','DROP':'','DUAL':'','EACH':'','ELSE':'','ELSEIF':'','ENCLOSED':'','ESCAPED':'','EXISTS':'','EXIT':'','EXPLAIN':'','FALSE':'','FETCH':'','FLOAT':'','FLOAT4':'','FLOAT8':'','FOR':'','FORCE':'','FOREIGN':'','FROM':'','FULLTEXT':'','GENERAL':'','GRANT':'','GROUP':'','HAVING':'','HIGH_PRIORITY':'','HOUR_MICROSECOND':'','HOUR_MINUTE':'','HOUR_SECOND':'','IF':'','IGNORE':'','IGNORE_SERVER_IDS':'','IN':'','INDEX':'','INFILE':'','INNER':'','INOUT':'','INSENSITIVE':'','INSERT':'','INT':'','INT1':'','INT2':'','INT3':'','INT4':'','INT8':'','INTEGER':'','INTERVAL':'','INTO':'','IS':'','ITERATE':'','JOIN':'','KEY':'','KEYS':'','KILL':'','LEADING':'','LEAVE':'','LEFT':'','LIKE':'','LIMIT':'','LINEAR':'','LINES':'','LOAD':'','LOCALTIME':'','LOCALTIMESTAMP':'','LOCK':'','LONG':'','LONGBLOB':'','LONGTEXT':'','LOOP':'','LOW_PRIORITY':'','MASTER_HEARTBEAT_PERIOD':'','MASTER_SSL_VERIFY_SERVER_CERT':'','MATCH':'','MAXVALUE':'','MEDIUMBLOB':'','MEDIUMINT':'','MEDIUMTEXT':'','MIDDLEINT':'','MINUTE_MICROSECOND':'','MINUTE_SECOND':'','MOD':'','MODIFIES':'','NATURAL':'','NOT':'','NO_WRITE_TO_BINLOG':'','NULL':'','NUMERIC':'','ON':'','OPTIMIZE':'','OPTION':'','OPTIONALLY':'','OR':'','ORDER':'','OUT':'','OUTER':'','OUTFILE':'','PRECISION':'','PRIMARY':'','PROCEDURE':'','PURGE':'','RANGE':'','READ':'','READS':'','READ_WRITE':'','REAL':'','REFERENCES':'','REGEXP':'','RELEASE':'','RENAME':'','REPEAT':'','REPLACE':'','REQUIRE':'','RESIGNAL':'','RESTRICT':'','RETURN':'','REVOKE':'','RIGHT':'','RLIKE':'','SCHEMA':'','SCHEMAS':'','SECOND_MICROSECOND':'','SELECT':'','SENSITIVE':'','SEPARATOR':'','SET':'','SHOW':'','SIGNAL':'','SLOW':'','SMALLINT':'','SPATIAL':'','SPECIFIC':'','SQL':'','SQLEXCEPTION':'','SQLSTATE':'','SQLWARNING':'','SQL_BIG_RESULT':'','SQL_CALC_FOUND_ROWS':'','SQL_SMALL_RESULT':'','SSL':'','STARTING':'','STRAIGHT_JOIN':'','TABLE':'','TERMINATED':'','THEN':'','TINYBLOB':'','TINYINT':'','TINYTEXT':'','TO':'','TRAILING':'','TRIGGER':'','TRUE':'','UNDO':'','UNION':'','UNIQUE':'','UNLOCK':'','UNSIGNED':'','UPDATE':'','USAGE':'','USE':'','USING':'','UTC_DATE':'','UTC_TIME':'','UTC_TIMESTAMP':'','VALUES':'','VARBINARY':'','VARCHAR':'','VARCHARACTER':'','VARYING':'','WHEN':'','WHERE':'','WHILE':'','WITH':'','WRITE':'','XOR':'','YEAR_MONTH':'','ZEROFILL':''}
    }
  },
  computed: {
    query(){
      return "SELECT COUNT(*) FROM users WHERE username='" + this.username + "' AND password='" + this.password + "'"
    },
    syntaxHighlightedQuery(){
      var sql = this.htmlentities(this.query)

      // Highlight strings
      sql = sql.replace(/(['"])([^\1]*?)(\1|$)/g, "<span class='quote'>$1$2$3</span>") 

      // Highlight keywords
      var words = this.keywords
      sql = sql.replace(/\b([a-zA-Z]{2,}\d?)\b/g, function(a, b){
        if(words[b] === '')
          return "<span class='keyword'>" + b + "</span>"
        return b
      });

      // Highlight comments
      sql = sql.replace(/(\-\- .*?)(\n|$)/g, "<span class='comment'>$1$2</span>") 

      return sql
    }
  },
  methods: {
    htmlentities(value){
      return value.replace(/[\u00A0-\u9999<>\&]/gim, function(i) {
        return '&#'+i.charCodeAt(0)+';';
      });
    },
    decode(str){
    	var textArea = document.createElement('textarea');
      textArea.innerHTML = str;
      return textArea.value;
    }
  }
})
</script>
</body>
</html>
