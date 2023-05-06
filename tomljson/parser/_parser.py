import os
import ply.yacc as yacc
from tomljson.lexer._lexer import tokens
from tomljson.utils._readfile import handlePath, readFile
from tomljson.utils._format_toml import handleTableArrayFormat


def _parser(toml_path: str):
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
        """child : CHILD_HEADER content
        | CHILD_HEADER child
        | CHILD_HEADER"""
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = p[1]

    def p_inline_table(p):
        """inline_table : LCURLY inline_contents RCURLY
        | LCURLY RCURLY"""
        if len(p) == 4:
            p[0] = [p[1]] + p[2] + [p[3]]
        else:
            p[0] = []

    def p_table(p):
        """table : TABLE_HEADER content
        | child
        | TABLE_HEADER"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = [p[1]] + p[2]

    def p_inline_content(p):
        """inline_contents : inline_contents COMMA content
        | content"""
        if len(p) == 4:
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1]

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
        """values : values COMMA value
        | value"""
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

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
    
    filepath = abs_path.split('/')
    filepath = filepath[:-2]
    filepath = '/'.join(filepath) + '/' + toml_path

    data = handleTableArrayFormat(readFile(filepath))

    return parser.parse(data)
