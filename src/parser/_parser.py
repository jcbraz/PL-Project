import sys
import os
from pathlib import Path
import ply.yacc as yacc
import json

# Add the lexer directory to the search path
lexer_dir = Path(__file__).parent / "../lexer"
sys.path.append(str(lexer_dir.resolve()))

# Import the tokens list from _new_lexer.py
from _new_lexer import tokens

def p_document(p):
    '''
    document : items
    '''
    p[0] = p[1]

def p_items(p):
    '''
    items : item items
          | item
    '''
    if len(p) == 3:
        p[0] = {**p[1], **p[2]}
    else:
        p[0] = p[1]

def p_item(p):
    '''
    item : KEY EQUAL value NEWLINE
         | KEY EQUAL value
         | KEY LBRACKET RBRACKET NEWLINE
         | KEY LBRACKET RBRACKET
         | NEWLINE
    '''
    if len(p) == 5 or (len(p) == 4 and p[2] == '='):
        p[0] = {p[1]: p[3]}
    elif len(p) == 4 or len(p) == 3:
        p[0] = {p[1]: {}}
    else:
        p[0] = {}

def p_value(p):
    '''
    value : STRING
          | INTEGER
          | FLOAT
          | BOOLEAN
          | DATE
          | array
          | inline_table
    '''
    p[0] = p[1]

def p_array(p):
    '''
    array : LBRACKET values RBRACKET
    '''
    p[0] = p[2]

def p_values(p):
    '''
    values : value COMMA values
           | value
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_inline_table(p):
    '''
    inline_table : LCURLY pairs RCURLY
    '''
    p[0] = p[2]

def p_pairs(p):
    '''
    pairs : KEY EQUAL value COMMA pairs
          | KEY EQUAL value
    '''
    if len(p) == 6:
        p[0] = {p[1]: p[3], **p[5]}
    else:
        p[0] = {p[1]: p[3]}

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
print(json.dumps(result, indent=2))
