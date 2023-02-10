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

class Token{
    private $identif;
    private $type;
    private $data_type;
    private $data;

    function Init($new_identif, $new_type, $new_data_type){
        
    }
} 

class InstructionData{
    public $operandCount;
    public $operands;
    public $operand_types;
}


?>