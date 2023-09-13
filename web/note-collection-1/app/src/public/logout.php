<?php

include '../init.php';

unset($_SESSION['userid']);
session_destroy();

redirect("/login.php");