<?php
include_once 'vars.php';

function type_parser($type){
    switch($type){
        case Types::Int:
            return "int";
        case Types::Bool:
            return "bool";
        case Types::String:
            return "string";
        case Types::Nil:
            return "nil";
        case Types::Label:
            return "label";
        case Types::Type:
            return "type";
        case Types::Var:
            return "var";
        default:
            //exit
    }
}

function generate_xml($code){
    $xml = new XMLWriter();
    $xml->openMemory();
    $xml->setIndent(true);
    $xml->setIndentString("\t");
    
    // povinná hlavička
    $xml->startDocument('1.0', 'UTF-8');
    $xml->startElement('program');
    $xml->startAttribute('language');
    $xml->text('IPPcode23');
    
    for($i = 1; $i < count($code); $i++){
        $line = $code[$i];
        $xml->startElement('instruction');

        $xml->startAttribute('order');
        $xml->text($i);
        $xml->endAttribute();

        $xml->startAttribute('opcode');
        $xml->text($line[0]->identif);
        $xml->endAttribute();

        for($j = 1; $j < count($line); $j++){
            $xml->startElement('arg'.$j);

            $xml->startAttribute('type');
            $xml->text(type_parser($line[$j]->type));//todo
            $xml->endAttribute();

            
            $xml->text($line[$j]->identif);
            

            $xml->endElement();
        }
        $xml->endElement();

    }
    
    // ukončení souboru
    $xml->endAttribute();
    $xml->endElement();
    $xml->endDocument();

    file_put_contents("output.xml", $xml->outputMemory());
}


?>