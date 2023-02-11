<?php

include_once "vars.php";

// pravidla jazyka IPP2023
// první položka pole obsahuje všechny instrukce, které sdílí stejný typ a počet operandů
$RULE_SET = array(
    array( "MOVE", // instrukce
        array(Types::Var), // první operand musí být typu <var>
        array(Types::Var, Types::Nil, Types::Int, Types::String, Types::Bool) ),
    array( "CREATEFRAME__PUSHFRAME__POPFRAME__RETURN__BREAK" ),
    array( "DEFVAR__POPS", 
        array(Types::Var) ),
    array( "CALL__LABEL__JUMP", 
        array(Types::Label) ),
    array( "PUSHS__WRITE__DPRINT", 
        array(Types::Var, Types::Int, Types::Bool, Types::String, Types::Nil) ),
    array( "ADD__SUB__MUL__IDIV", 
        array(Types::Var), 
        array(Types::Var, Types::Int), 
        array(Types::Var, Types::Int) ),
    array( "LT__GT__EQ", 
        array(Types::Var), 
        array(Types::Var,Types::Int), 
        array(Types::Var, Types::Int) ),
    array( "LT__GT__EQ", 
        array(Types::Var), 
        array(Types::Var, Types::Bool), 
        array(Types::Var, Types::Bool) ),
    array( "LT__GT__EQ", 
        array(Types::Var), 
        array(Types::Var, Types::String), 
        array(Types::Var, Types::String) ),
    array( "LT__GT__EQ", 
        array(Types::Var), 
        array(Types::Var, Types::Nil), 
        array(Types::Var, Types::Nil) ),
    array( "AND_OR", 
        array(Types::Var), 
        array(Types::Var, Types::Bool), 
        array(Types::Var, Types::Bool) ),
    array( "NOT", 
        array(Types::Var), 
        array(Types::Var, Types::Bool) ),
    array( "INT2CHAR", 
        array(Types::Var), 
        array(Types::Var, Types::Int)),
    array( "STRI2INT__GETCHAR", 
        array(Types::Var), 
        array(Types::Var, Types::String), 
        array(Types::Var, Types::Int) ),
    array( "READ",  
        array(Types::Var), 
        array(Types::Type)),
    array( "CONCAT", 
        array(Types::Var), 
        array(Types::Var, Types::String), 
        array(Types::Var, Types::String) ),
    array( "STRLEN", 
        array(Types::Var), 
        array(Types::Var, Types::String) ),
    array( "SETCHAR", 
        array(Types::Var), 
        array(Types::Var), 
        array(Types::Var, Types::Int)  ),
    array( "TYPE", 
        array(Types::Var), 
        array(Types::Var, Types::String, Types::Bool, Types::Int, Types::Nil) ),
    array("JUMPIFEQ__JUMPIFNEQ", 
        array(Types::Label), 
        array(Types::Var, Types::Nil, Types::Int), 
        array(Types::Var, Types::Nil, Types::Int)),
    array("JUMPIFEQ__JUMPIFNEQ", 
        array(Types::Label), 
        array(Types::Var, Types::Nil, Types::Bool), 
        array(Types::Var, Types::Nil, Types::Bool)),
    array("JUMPIFEQ__JUMPIFNEQ", 
        array(Types::Label), 
        array(Types::Var, Types::Nil, Types::String), 
        array(Types::Var, Types::Nil, Types::String)),
    array( "EXIT", 
        array(Types::Var, Types::Int) )

);

/*

$GROUP_A = "CREATEFRAME__PUSHFRAME__POPFRAME__RETURN__BREAK"; // bez operandu
$GROUP_B = "DEFVAR__POPS"; // operand ve tvaru ⟨var⟩
$GROUP_C = "CALL__LABEL__JUMP"; //operand ve tvaru ⟨label⟩
$GROUP_D = "PUSHS__WRITE__DPRINT"; //operand ve tvaru <symb>
$GROUP_E = "ADD__SUB__MUL__IDIV"; // operandy ve tvaru ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩, kde ⟨symb1⟩ a ⟨symb2⟩ jsou typu int/var
$GROUP_F = "LT__GT__EQ"; // operandy ve tvaru ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩, kde ⟨symb1⟩ a ⟨symb2⟩ jsou stejneho typu
$GROUP_G = "AND_OR"; // operandy ve tvaru ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩, kde ⟨symb1⟩ a ⟨symb2⟩ jsou typu bool/var
$GROUP_H = "NOT"; // operandy ve tvaru ⟨var⟩ ⟨symb⟩, kde <symb> je typu bool/var
$GROUP_I = "INT2CHAR";
$GROUP_J = "STRI2INT__GETCHAR";
$GROUP_K = "READ";
$GROUP_L = "CONCAT";
$GROUP_M = "STRLEN";
$GROUP_N = "MOVE";
$GROUP_O = "SETCHAR";
$GROUP_P = "TYPE";
$GROUP_Q = "JUMPIFEQ__JUMPIFNEQ";
$GROUP_R = "EXIT";
*/



function check_line($line){
    global $RULE_SET;
    global $stderr;
    if(count($line) == 0)
        return;

    $instruction = $line[0]->identif;

    if($line[0]->type == Types::Header){
        fprintf($stderr, "ERROR:: Prebyvajici hlavicka!\n");
            exit(UnknownCode_Error);
    }

    $found = false;
    foreach($RULE_SET as $rule){
        if(str_contains($rule[0], strtoupper($instruction)) && (count($rule) == count($line))){
            if(count($rule) == 1)
                $found = true;
            for($i = 1; $i < count($rule); $i++){
                if(!in_array($line[$i]->type, $rule[$i], true)){
                    $found = false;
                    break;
                }
                else
                    $found = true;
            }
        }
    }
    if(!$found){
        fprintf($stderr, "ERROR:: rule for <%s> with operands:", $instruction);
        for($i = 1; $i < count($line); $i++){
            fprintf($stderr, " <%s>", $line[$i]->identif);
        }
        fprintf($stderr, " not found!\n");
        print_r($line);
        exit(LexSyn_Error);
    }
}

function syntax_check($code_lines){
    global $stderr;

    if(empty($code_lines))
        return;

    if($code_lines[0][0]->type != Types::Header){
        fprintf($stderr, "ERROR:: Chybejici nebo chybna hlavicka souboru!\n");
            exit(Header_Error);
    }
    for($i = 1; $i < count($code_lines); $i++){
        check_line($code_lines[$i]);
    }
}



?>