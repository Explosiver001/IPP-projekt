<?php

ini_set('display_errors', 'stderr');

include 'parse_libs/scanner.php';
include 'parse_libs/parser.php';
include 'parse_libs/generator.php';

// zpracování argumentů programu
$short_options = "h";
$long_options = array("help");
$options = getopt($short_options, $long_options);

if(array_key_exists("h", $options) || array_key_exists("help", $options)){
    echo "help\n";
    return;
}

// lexikální analýza a uložení tokenů
$code_lines = scanner($input_file);

// syntaktická a základní sémantická analýza
syntax_check($code_lines);

// generace výstupního XML formátu
generate_xml($code_lines);

exit(0);

?>