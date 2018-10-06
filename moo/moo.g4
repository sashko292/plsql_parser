/*
BSD License

Copyright (c) 2018, Tom Everett
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of Tom Everett nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
/*
* http://www2.iath.virginia.edu/courses/moo/ProgrammersManual.texinfo_4.html
*/
/*
* https://www.hayseed.net/MOO/manuals/ProgrammersManual.html
*/

grammar moo;

prog
   : declaration + '.'
   ;

declaration
   : programdecl
   | verbdecl
   ;

programdecl
   : '@program' name ':' name statement +
   ;

verbdecl
   : '@verb' name ':' name +
   ;

statement
   : ifblock
   | whileblock
   | doblock
   | forblock
   | assignblock
   | tryblock
   | command SEMICOLON
   ;

ifblock
   : 'if' condition statement + ('else' statement +)? 'endif' ';'?
   ;

whileblock
   : 'while' condition statement +
   ;

doblock
   : 'do' statement + 'while' condition
   ;

forblock
   : 'for' name 'in' expression statement + 'endfor'
   ;

tryblock
   : 'try' statement + 'except' property statement + 'endtry'
   ;

assignblock
   : property ASSIGN expression SEMICOLON
   ;

condition
   : LPAREN expression (relop expression)* RPAREN
   ;

relop
   : EQ
   | NEQ
   | GT
   | GTE
   | LT
   | LTE
   | AND
   | OR
   ;

expressionlist
   : expression (COMMA expression)*
   ;

expression
   : term ((PLUS | MINUS) term)*
   ;

term
   : factor ((TIMES | DIV | MOD) factor)*
   ;

factor
   : signedAtom (POW signedAtom)*
   ;

signedAtom
   : PLUS signedAtom
   | MINUS signedAtom
   | atom
   ;

atom
   : stringliteral
   | functioninvocation
   | verbinvocation
   | property
   | integer
   | real
   | list
   | '(' expression ')'
   ;

functioninvocation
   : name '(' expressionlist ')'
   ;

command
   : verbinvocation
   | returncommand
   ;

returncommand
   : 'return' expression
   ;

verbinvocation
   : property ':' verb
   ;

verb
   : name ('(' expressionlist? ')')?
   ;

property
   : name (('.' name) | '[' expression ']')*
   ;

list
   : '{' expressionlist? '}'
   ;

stringliteral
   : STRINGLITERAL
   ;

integer
   : INTEGER
   ;

real
   : REAL
   ;

name
   : username
   | sysname
   ;

sysname
   : DOLLAR STRING?
   ;

username
   : STRING
   ;


LPAREN
   : '('
   ;


RPAREN
   : ')'
   ;


PLUS
   : '+'
   ;


MINUS
   : '-'
   ;


TIMES
   : '*'
   ;


MOD
   : '%'
   ;


DIV
   : '/'
   ;


GT
   : '>'
   ;


LT
   : '<'
   ;


GTE
   : '>='
   ;


LTE
   : '<='
   ;


EQ
   : '=='
   ;


AND
   : '&&'
   ;


OR
   : '||'
   ;


NEQ
   : '!='
   ;


POW
   : '^'
   ;


COMMA
   : ','
   ;


ASSIGN
   : '='
   ;


SEMICOLON
   : ';'
   ;


DOLLAR
   : '$'
   ;


STRING
   : [a-zA-Z] [a-zA-Z0-9!_] +
   ;


STRINGLITERAL
   : '"' ~ ["\r\n]* '"'
   ;


INTEGER
   : [0-9] +
   ;


REAL
   : [0-9] + '.' [0-9] +
   ;


COMMENT
   : ';' ~ [\r\n]* -> skip
   ;


WS
   : [ \r\n\t] -> skip
   ;