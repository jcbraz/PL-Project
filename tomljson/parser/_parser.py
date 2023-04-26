import sys
sys.path.append('..')
import ply.yacc as yacc
import json

from lexer._lexer import tokens

def p_document(p):
    '''document : toml
                | toml document'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_toml(p):
    '''toml : content
            | array
            | table
            | inline_table
            | array_tables'''
    p[0] = p[1]


def p_array_tables(p):
    '''array_tables : ARRAY_TABLES_HEADER content
                    | ARRAY_TABLES_HEADER array_tables'''
    p[0] = p[1] + p[2]


def p_child(p):
    '''child : CHILD_HEADER content
             | CHILD_HEADER child'''
    p[0] = p[1] + p[2]


def p_inline_table(p):
    '''inline_table : LCURLY content RCURLY
                    | LCURLY RCURLY'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []


def p_table(p):
    '''table : TABLE_HEADER content
             | TABLE_HEADER child'''
    p[0] = p[1] + p[2]


def p_content(p):
    '''content : assignment
               | content assignment'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]


def p_assignment(p):
    '''assignment : VARIABLE EQUAL value'''
    p[0] = p[3]


def p_array(p):
    '''array : LBRACKET values RBRACKET
             | LBRACKET array RBRACKET
             | LBRACKET RBRACKET'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[2]


def p_values(p):
    '''values : value COMMA values
              | value'''
    if len(p) == 1:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + [p[3]]


def p_value(p):
    '''value : STRING
             | INTEGER
             | FLOAT
             | BOOLEAN
             | DATE'''
    p[0] = p[1]


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

data = """
# This is a TOML document. Boom.
title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], [3.14] ]
temp_targets = { cpu = 79.5, case = 72.0 }

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"
"""


result = parser.parse(data)
print(parser.parse(data))
