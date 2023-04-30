import os
import ply.yacc as yacc
from tomljson.lexer._lexer import tokens
from tomljson.utils._readfile import handlePath, readFile
from tomljson.utils._format_toml import handleTableArrayFormat


def p_document(p):
    """document : toml
    | toml document"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_toml(p):
    """toml : content
    | array
    | table
    | inline_table
    | array_tables"""
    p[0] = p[1]


def p_array_tables(p):
    """array_tables : ARRAY_TABLES_HEADER content
    | ARRAY_TABLES_HEADER array_tables"""
    p[0] = [p[1]] + p[2]


def p_child(p):
    """child : CHILD_HEADER content"""
    p[0] = [p[1]] + p[2]


def p_inline_table(p):
    """inline_table : LCURLY inline_contents RCURLY
    | LCURLY RCURLY"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []


def p_table(p):
    """table : TABLE_HEADER content
    | TABLE_HEADER child
    | table child"""
    p[0] = [p[1]] + p[2]


def p_inline_content(p):
    """inline_contents : inline_contents COMMA content
    | content"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[3]]


def p_content(p):
    """content : assignment
    | content assignment"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_assignment(p):
    """assignment : VARIABLE value
    | VARIABLE array
    | VARIABLE inline_table"""
    p[0] = [p[1]] + [p[2]]


def p_array(p):
    """array : DOT LBRACKET array RBRACKET
    | DOT LBRACKET values RBRACKET
    | DOT LBRACKET RBRACKET"""
    if len(p) == 4:
        p[0] = []
    else:
        p[0] = p[3]


def p_values(p):
    """values : value COMMA values
    | value"""
    if len(p) == 1:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = [p[1]] + [p[3]]


def p_value(p):
    """value : STRING
    | NUMBER
    | BOOLEAN
    | DATE"""
    p[0] = p[1]


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


dirname = os.path.dirname(__file__)
abs_path = os.path.abspath(dirname)

handledPath = handlePath("../../model.toml")

filepath = os.path.join(abs_path, handledPath[0])

for i in range(1, len(handledPath)):
    filepath = os.path.join(filepath, handledPath[i])

data = handleTableArrayFormat(readFile(filepath))

result = parser.parse(data, debug=True)

# with open("result.json", "w") as file:
#     file.write(str(result))
