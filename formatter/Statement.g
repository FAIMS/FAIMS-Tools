grammar Statement;

options {
  language  = Ruby;
  output    = AST;
}

@token::members {
    def value
        return nil if text == 'null'
        return text.to_f unless text =~ /^(\'|\")/
        text[1..-2]
    end
}

program returns [value]
    : s=statement { $value = $s.value }
    ;

statement returns [value]
    : 'if' e=multi_expression 'then' v=literal s=next_statement? 
        { 
            if $e.value 
                $value = $v.value
            else
                $value = $s.value
            end
        }
    ;

next_statement returns [value]
    : 'elsif' e=multi_expression 'then' v=literal s=next_statement?
        { 
            if $e.value 
                $value = $v.value
            else
                $value = $s.value
            end
        }
    | 'else' v=literal
        { 
            $value = $v.value
        }
    ;

multi_expression returns [value]
    : 'and(' l=single_expression ',' r=multi_expression ')' { $value = $l.value && $r.value }
    | 'or(' l=single_expression ',' r=multi_expression ')' { $value = $l.value || $r.value }
    | e=single_expression { $value = $e.value }
    ;

single_expression returns [value]
    : 'equal(' l=literal ',' r=literal ')' { $value = $l.value == $r.value }
    | 'greaterThan(' l=literal ',' r=literal ')' { $value = $l.value.nil? == false && $r.value.nil? == false && $l.value.to_f > $r.value.to_f }
    | 'greaterThanEqual('l=literal ',' r=literal ')' { $value = $l.value.nil? == false && $r.value.nil? == false && $l.value.to_f >= $r.value.to_f }
    | 'lessThan(' l=literal ',' r=literal ')' { $value = $l.value.nil? == false && $r.value.nil? == false && $l.value.to_f < $r.value.to_f }
    | 'lessThanEqual(' l=literal ',' r=literal ')' { $value = $l.value.nil? == false && $r.value.nil? == false && $l.value.to_f <= $r.value.to_f }
    | 'between(' l=literal ',' min=literal ',' max=literal ')' { $value = $l.value.nil? == false && $min.value.nil? == false && $max.value.nil? == false && $l.value.to_f >= $min.value.to_f && $l.value.to_f <= $max.value.to_f }
    | 'not(' e=single_expression ')' 
        { 
            if $e.value
                $value = false
            else
                $value = true
            end  
        }
    | 'in(' v=literal ',' l=list ')' 
        {
            $value = $l.value.include?($v.value)
        } 
    | e=literal { $value = $e.value }
    ;

list returns [value]
    : '[' l=literals']' { $value = $l.value }
    ;

literals returns [value]
    : l=literal ',' rest=literals { $value = $rest.value.push($l.value) }
    | l=literal { $value = [$l.value] }
    ;

literal returns [value]
    : s=STRING { $value = $s.value }
    | v=VARIABLE { $value = \$argument_mapper.get_value($v.text) }
    | n=NUMBER { $value = $n.value }
    | i=INT { $value = $i.value }
    ;

NEWLINE     : '\n' { $channel = HIDDEN } ;
SPACE       : ' '+ { $channel = HIDDEN } ;
STRING      : '\'' ~('\'')* '\''
            | '\"' ~('\"')* '\"'
            ;
NUMBER      : '-'? DIGIT+ '.' DIGIT+ ;
INT         : '-'? DIGIT+ ;
VARIABLE    : '$' DIGIT+ ;

fragment DIGIT : ('0' .. '9') ;