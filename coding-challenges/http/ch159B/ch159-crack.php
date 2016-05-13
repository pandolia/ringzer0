<?php
    # usage: http://.../ch159-crack.php?sha1=xxxxxxxxs

    $crackst_dir = "/home/????/crackstation-hashdb";
    require_once($crackst_dir . "/LookupTable.php");

    $idxfile = $crackst_dir . "/data/ch159-dict-sha1.idx";
    $dictfile = $crackst_dir . "/data/ch159-dict.txt";
    $algo = "sha1";

    $lookup = new LookupTable($idxfile, $dictfile, $algo);

    $to_crack = $_GET["sha1"];
    $result = $lookup->crack($to_crack);
    if ($result !== FALSE) {
        echo $result[0];
    }
?>