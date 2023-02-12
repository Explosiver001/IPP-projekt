<?php

ini_set('display_errors', 'stderr');

include 'parse_libs/scanner.php';
include 'parse_libs/parser.php';
include 'parse_libs/generator.php';

// zpracování argumentů programu
$short_options = "hd";
$long_options = array("help", "debug", "stats:", "loc", "comments", "labels", "jumps", "fwjumps", "backjumps", "badjumps", "frequent", "print:", "eol");
$options = getopt($short_options, $long_options);

$DEBUG_PARAM = false;
$STATS = array();

if(array_key_exists("h", $options) || array_key_exists("help", $options)){
    echo "help\n";
    return;
}
// argument pro DEBUG funkci
if(array_key_exists("d", $options) || array_key_exists("debug", $options)){
    $DEBUG_PARAM = true;
    echo "--- Debug mode ACTIVE ---\n";
}

print_r($argv);

// lexikální analýza a uložení tokenů
$code_lines = scanner($input_file);

// syntaktická a základní sémantická analýza
syntax_check($code_lines);

// generace výstupního XML formátu
generate_xml($code_lines);

exit(0);

?>