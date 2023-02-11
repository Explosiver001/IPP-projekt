<?php

include_once "vars.php";

// pravidla jazyka IPP2023
// první položka pole obsahuje všechny instrukce, které sdílí stejný typ a počet operandů
$RULE_SET_EXTENDED = array(
    array( "_MOVE_", // instrukce
        array(Types::Var), // první operand musí být typu <var>
        array(Types::Var, Types::Nil, Types::Int, Types::String, Types::Bool) ),
    array( "_CREATEFRAME__PUSHFRAME__POPFRAME__RETURN__BREAK_" ),
    array( "_DEFVAR__POPS_", 
        array(Types::Var) ),
    array( "_CALL__LABEL__JUMP_", 
        array(Types::Label) ),
    array( "_PUSHS__WRITE__DPRINT_", 
        array(Types::Var, Types::Int, Types::Bool, Types::String, Types::Nil) ),
    array( "_ADD__SUB__MUL__IDIV_", 
        array(Types::Var), 
        array(Types::Var, Types::Int), 
        array(Types::Var, Types::Int) ),
    array( "_LT__GT__EQ_", 
        array(Types::Var), 
        array(Types::Var,Types::Int), 
        array(Types::Var, Types::Int) ),
    array( "_LT__GT__EQ_", 
        array(Types::Var), 
        array(Types::Var, Types::Bool), 
        array(Types::Var, Types::Bool) ),
    array( "_LT__GT__EQ_", 
        array(Types::Var), 
        array(Types::Var, Types::String), 
        array(Types::Var, Types::String) ),
    array( "_LT__GT__EQ_", 
        array(Types::Var), 
        array(Types::Var, Types::Nil), 
        array(Types::Var, Types::Nil) ),
    array( "_AND_OR_", 
        array(Types::Var), 
        array(Types::Var, Types::Bool), 
        array(Types::Var, Types::Bool) ),
    array( "_NOT_", 
        array(Types::Var), 
        array(Types::Var, Types::Bool) ),
    array( "_INT2CHAR_", 
        array(Types::Var), 
        array(Types::Var, Types::Int)),
    array( "_STRI2INT__GETCHAR_", 
        array(Types::Var), 
        array(Types::Var, Types::String), 
        array(Types::Var, Types::Int) ),
    array( "_READ_",  
        array(Types::Var), 
        array(Types::Type)),
    array( "_CONCAT_", 
        array(Types::Var), 
        array(Types::Var, Types::String), 
        array(Types::Var, Types::String) ),
    array( "_STRLEN_", 
        array(Types::Var), 
        array(Types::Var, Types::String) ),
    array( "_SETCHAR_", 
        array(Types::Var), 
        array(Types::Var), 
        array(Types::Var, Types::Int)  ),
    array( "_TYPE_", 
        array(Types::Var), 
        array(Types::Var, Types::String, Types::Bool, Types::Int, Types::Nil) ),
    array("_JUMPIFEQ__JUMPIFNEQ_", 
        array(Types::Label), 
        array(Types::Var, Types::Nil, Types::Int), 
        array(Types::Var, Types::Nil, Types::Int)),
    array("_JUMPIFEQ__JUMPIFNEQ_", 
        array(Types::Label), 
        array(Types::Var, Types::Nil, Types::Bool), 
        array(Types::Var, Types::Nil, Types::Bool)),
    array("_JUMPIFEQ__JUMPIFNEQ_", 
        array(Types::Label), 
        array(Types::Var, Types::Nil, Types::String), 
        array(Types::Var, Types::Nil, Types::String)),
    array( "_EXIT_", 
        array(Types::Var, Types::Int) )

);


// zjednodušená pravidla neuvažující ani základní kontrolu sémantiky operandu
$RULE_SET = array(
    array( "_MOVE__NOT__INT2CHAR__STRLEN__TYPE_", // instrukce
        array(Types::Var), // arg1
        array(Types::AnyDataType) ), //arg2 
    array( "_CREATEFRAME__PUSHFRAME__POPFRAME__RETURN__BREAK_" ),
    array( "_DEFVAR__POPS_", 
        array(Types::Var) ),
    array( "_CALL__LABEL__JUMP_", 
        array(Types::Label) ),
    array( "_PUSHS__WRITE__DPRINT_", 
        array(Types::AnyDataType) ),
    array( "_ADD__SUB__MUL__IDIV__LT__GT__EQ__AND_OR__STRI2INT__GETCHAR__CONCAT_", 
        array(Types::Var), 
        array(Types::AnyDataType), 
        array(Types::AnyDataType) ),
    array( "_READ_",  
        array(Types::Var), 
        array(Types::Type)),
    array( "_SETCHAR_", 
        array(Types::Var), 
        array(Types::AnyDataType), 
        array(Types::AnyDataType) ),
    array("_JUMPIFEQ__JUMPIFNEQ_", 
        array(Types::Label), 
        array(Types::AnyDataType), 
        array(Types::AnyDataType) ),
    array( "_EXIT_", 
        array(Types::AnyDataType) )

);

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
        if(str_contains($rule[0], strtoupper("_".$instruction."_")) && (count($rule) == count($line))){
            if(count($rule) == 1)
                $found = true;
            for($i = 1; $i < count($rule); $i++){
                if(($line[$i]->type == Types::Var || $line[$i]->type == Types::Bool 
                || $line[$i]->type == Types::Int || $line[$i]->type == Types::String || $line[$i]->type == Types::Nil) 
                && (in_array(Types::AnyDataType, $rule[$i]))){
                    $found = true;
                }
                elseif(!in_array($line[$i]->type, $rule[$i], true)){
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