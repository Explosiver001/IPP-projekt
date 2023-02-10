<?php

include 'parse_libs/scanner.php';

$short_options = "h";
$long_options = array("help");

$options = getopt($short_options, $long_options);

if(array_key_exists("h", $options)){
    echo "help\n";
    return;
}



read_lines($input_file);



?>