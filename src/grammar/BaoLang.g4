grammar BaoLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program: stmt* EOF;

// statements - do not return anything
stmt: letStmt  
    | exprStmt 
    ;
letStmt: LET ID ASSIGN expr SEMI ;
exprStmt: expr SEMI ;

// expressions - return a value
expr:ID                                          # idExpr
    | (INTLIT | FLOATLIT | STRINGLIT | BOOLLIT)   # litExpr

    | expr LPAREN (expr (COMMA expr)*)? RPAREN    # funcCallExpr
    | expr LBRACKET expr RBRACKET                 # listAccessExpr

    | expr (PLUS | MINUS) expr                    # addSubExpr
    | expr (MULTIPLY | DIVIDE | MODULO) expr      # mulDivModExpr
    | expr (EQUAL | NOTEQUAL) expr                # eqExpr
    | expr (LT | GT | LE | GE) expr               # relExpr
    | expr OR expr                                # orExpr
    | expr AND expr                               # andExpr
    | (NOT | MINUS) expr                          # unaryExpr

    | MATCH expr LBRACE matchCase+ RBRACE         # matchExpr
    | LBRACE stmt* expr RBRACE                    # blockExpr
    | LBRACKET (expr (COMMA expr)*)? RBRACKET     # listExpr
    

    | IF expr THEN expr ELSE expr                 # ifExpr1
    | expr IF expr ELSE expr                      # ifExpr2

    | paramList ARROW expr                        # lambdaExpr
    | LPAREN expr RPAREN                          # parenExpr 
    ;

matchCase : (pattern ARROW expr SEMI) ;
pattern : INTLIT
    | FLOATLIT
    | STRINGLIT
    | BOOLLIT
    | ID
    | DEFAULT
    | pattern (COMMA pattern)+
    | LBRACKET (pattern (COMMA pattern)*)? RBRACKET 
    ;

paramList: ID (COMMA ID)* ;

//Comments
COMMENT : '/*' .*? '*/' -> skip ; // skip comments
LINE_COMMENT : '//' ~[\r\n]* -> skip ; // skip line comments

//Keywords
IF : 'if' ;
THEN : 'then' ;
ELSE : 'else' ;
LET : 'let' ;
MATCH : 'match' ;
DEFAULT : 'default' | '_' ;


//Operators
ASSIGN : '=' ;
PLUS : '+' ;
MINUS : '-' ;
MULTIPLY : '*' ;
DIVIDE : '/' ;
MODULO : '%' ;
EQUAL : '==' ;
NOTEQUAL : '!=' ;
LT : '<' ;
GT : '>' ;
LE : '<=' ;
GE : '>=' ;
AND : '&&' ;
OR : '||' ;
NOT : '!' ;
ARROW : '->' ;

//Delimiters
LPAREN : '(' ;
RPAREN : ')' ;
LBRACE : '{' ;
RBRACE : '}' ;
LBRACKET : '[' ;
RBRACKET : ']' ;
COMMA : ',' ;
SEMI : ';' ;
COLON : ':' ;

//Literals
INTLIT : [0-9]+ ;
FLOATLIT : [0-9]+ '.' [0-9]+ ;
fragment ESC_SEQ: '\\' [btnfr"\\];
fragment CHARLIT: ESC_SEQ | ~["\\\r\n\f];
STRINGLIT: '"' CHARLIT* '"' {self.text=self.text[1:-1]};
BOOLLIT : 'true' | 'false' ;
ID : [a-zA-Z_][a-zA-Z0-9_]* ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs 

UNCLOSE_STRING : '"' CHARLIT* {self.text=self.text[1:]} ;
ILLEGAL_ESCAPE : '"' CHARLIT* '\\' ~[btnfr"\\] {self.text=self.text[1:]};
ERROR_CHAR     : . ;