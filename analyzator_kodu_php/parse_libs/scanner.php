<?php
include_once 'vars.php';



function is_instruction($token){
    global $instruction_set;
    foreach($instruction_set as $instruction){
        if (!strcmp(strtolower($instruction), strtolower($token)))
            return true;
    }
    return false;
}

function find_type($token){
    $variable_pattern = "/^((LF)|(TF)|(GF))@([-]|[a-z]|[A-Z]|[0-9]|[_$&%*!?])+$/";
    //$string_pattern = "/^string@([!\"]|[%-[]|]|\^|[_-~]|([\\\\][0-9][0-9][0-9]))*$/"; //! stara verze, jen ascii 0-127
    $string_pattern = "/^string@(([^\#\\\\\001-\032])|([\\\\][0-9][0-9][0-9]))*$/";
    $int_pattern = "/^(int@[+-]\d+)|(int@\d+)$/";
    $bool_pattern = "/^(bool@true)|(bool@false)$/";
    $nil_pattern = "/^nil@nil$/";
    $type_pattern = "/^(int)|(string)|(bool)$/";
    $label_pattern = "/^([-]|[a-z]|[A-Z]|[0-9]|[_$&%*!?])+$/";
    $comment_pattern = "/^#/";
    $header_pattern = "/^.IPPcode23$/";

    
    if(is_instruction($token))
        return Types::Instruction;
    if(preg_match($header_pattern, $token))
        return Types::Header;
    if(preg_match($comment_pattern, $token))
        return Types::Comment;
    if(preg_match($variable_pattern, $token))
        return Types::Var;
    if(preg_match($int_pattern, $token))
        return Types::Int;
    if(preg_match($bool_pattern, $token))
        return Types::Bool;
    if(preg_match($string_pattern, $token))
        return Types::String;
    if(preg_match($nil_pattern, $token))
        return Types::Nil;
    if(preg_match($type_pattern, $token))
        return Types::Type;
    if(preg_match($label_pattern, $token))
        return Types::Label;

    return Types::Error;
    
    /*
    if (preg_match($variable_pattern, $token) || preg_match($string_pattern, $token) || preg_match($int_pattern, $token) 
        || preg_match($bool_pattern, $token) || preg_match($nil_pattern, $token))
        return true;
    return false;
    */
}


function read_lines($input_file): array{
    global $stderr;
    global $DEBUG_PARAM;

    $code_array = array();
    //for($line_num = 1; )
    while(!feof($input_file)){
        $line = fgets($input_file);
        while(str_contains($line, "\t") || str_contains($line, "  ")){
            $to_replace = array("  ", "\t");
            $line = str_replace($to_replace, " ", $line);
        }
        $line = trim($line);

        if(!strcmp($line, "")){
            continue;
        }
        
        $split_line = explode(' ', $line);


        $operation = array();

        for ($i = 0; $i < count($split_line); $i++) {

            $ret_type = find_type($split_line[$i]);
            if($ret_type == Types::Comment)
                break;
            elseif($i == 0 && $ret_type != Types::Instruction && $ret_type != Types::Header){
                fprintf($stderr, "ERROR:: %s\n", $split_line[$i]);
                exit(UnknownCode_Error);
            }
            elseif($ret_type == Types::Error){
                fprintf($stderr, "ERROR:: %s\n", $split_line[$i]);
                exit(LexSyn_Error);
            }
            else{
                $token = new Token($split_line[$i], $ret_type);
                array_push($operation, $token);
            }



            /*if (!$in_comment) {
                
                if (!strcmp($split_line[$i], "#")) { // komnetáře
                    $in_comment = true;
                }
                elseif (!(is_operand($split_line[$i]) || is_instruction($split_line[$i]))){ // token není instrukce ani operand
                    fprintf($stderr, "<< %s >> neni validni token!\n\n", $split_line[$i]);
                }
                else{
                    fprintf($stderr, "(( %s )) je validni token!\n\n", $split_line[$i]);
                }
                    
            }*/
        }
        array_push($code_array, $operation);

    }
    if($DEBUG_PARAM)
        print_r($code_array);
    
    return $code_array;
}

?>