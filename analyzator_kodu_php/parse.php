<?php

include 'parse_libs/scanner.php';
include 'parse_libs/parser.php';
include 'parse_libs/generator.php';

$short_options = "hd";
$long_options = array("help", "debug");

$options = getopt($short_options, $long_options);

$DEBUG_PARAM = false;

if(array_key_exists("h", $options) || array_key_exists("help", $options)){
    echo "help\n";
    return;
}
if(array_key_exists("d", $options) || array_key_exists("debug", $options)){
    $DEBUG_PARAM = true;
    echo "--- Debug mode ACTIVE ---\n";
}

$code_lines = read_lines($input_file);

syntax_check($code_lines);
generate_xml($code_lines);


?>