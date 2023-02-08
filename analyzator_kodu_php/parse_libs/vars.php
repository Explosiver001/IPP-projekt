<?php
$stderr = fopen('php://stderr', 'w');
$input_file = fopen('php://stdin', "r");

$instruction_set = array(
    "MOVE",
    "CREATEFRAME",
    "PUSHFRAME",
    "POPFRAME",
    "DEFVAR",
    "CALL",
    "RETURN",
    "PUSHS",
    "POPS",
    "ADD",
    "SUB",
    "MUL",
    "IDIV",
    "LT",
    "GT",
    "EQ",
    "AND",
    "OR",
    "NOT",
    "INT2CHAR",
    "STRI2INT",
    "READ",
    "WRITE",
    "CONCAT",
    "STRLEN",
    "GETCHAR",
    "SETCHAR",
    "TYPE",
    "LABEL",
    "JUMP",
    "JUMPIFEQ",
    "JUMPIFNEQ",
    "EXIT",
    "DPRINT",
    "BREAK"
);
?>