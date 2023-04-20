import ply.lex as lex
import datetime


class TableControl:
    def __init__(self):
        self.indentifier_control = 0

    def increment(self):
        self.indentifier_control += 1

    def decrement(self):
        self.indentifier_control -= 1

    def getIdentifierControl(self):
        return self.indentifier_control
    
    def setter(self, value):
        self.indentifier_control = value

    def get_table_title(t):
        title = t.split('.')
        return title


table_control = TableControl()


states = (
    ("default", "inclusive"),
    ("array", "inclusive"),
    ("table", "inclusive"),
    ("table_child", "inclusive"),

)

tokens = (
    'COMMENT',
    'DATE',
    'DATE_TIME',
    'ISO8601_DATE',
    'RFC3339_DATE',
    'LOCALDATE_TIME_MILLISECONDS',
    'LOCALTIME',
    'FLOAT',
    'INTEGER',
    'BOOLEAN',
    'STRING',
    'TABLE_START',
    'TABLE_START_INLINE',
    'TABLE_END',
    'TABLE_END_INLINE',
    'ARRAY_START',
    'ARRAY_END', 
    'IDENTIFIER',
    'LINE'
)

t_ignore = ' \t'



def t_ANY_COMMENT(t):
    r'\#.*'
    pass

def t_ANY_IDENTIFIER (t):
    r"\[([\w\.-]+)\]"
    t.value = t.value[1:-1]
    return t

def t_ANY_LINE (t):
    r'[a-zA-Z0-9]*\s?=\s?([\'"])?.*[\'"]?\n'
    t.value= t.value[1:-1]
    return t


def t_ANY_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    t.value = datetime.datetime.strptime(t.value, '%Y-%m-%d').date()
    return t

def t_ANY_LOCALTIME(t):
    r'\d{2}:\d{2}:\d{2}'
    t.value = datetime.datetime.strptime(t.value, '%H:%M:%S').time()
    return t

def t_ANY_LOCALTIME_MILISECONDS(t):
    r'\d{2}:\d{2}:\d{2}\.\d+'
    t.value = datetime.datetime.strptime(
        t.value.group(0), '%H:%M:%S.%f').time()
    return t


def t_ANY_DATE_TIME(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    t.value = datetime.datetime.strptime(t.value.group(0), '%Y-%m-%dT%H:%M:%S')
    return t


def t_ANY_ISO8601_DATE(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'
    t.value = datetime.datetime.strptime(
        t.value.group(0), '%Y-%m-%dT%H:%M:%SZ')
    return t


def t_ANY_RFC3339_DATE(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z'
    t.value = datetime.datetime.strptime(t.value.group(0), '%Y-%m-%dT%H:%M:%S')
    return t


def t_ANY_LOCALDATE_TIME_MILLISECONDS(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+'
    t.value = datetime.datetime.strptime(
        t.value.group(0), '%Y-%m-%dT%H:%M:%S.%f')
    return t


def t_ANY_FLOAT(t):
    r"\d*\.\d+([eE][-+]?\d+)?"
    t.value = float(t.value)
    return t


def t_ANY_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ANY_BOOLEAN(t):
    r"true|false"
    t.value = bool(t.value)
    return t


def t_ANY_STRING(t):
    r'"(?:[^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_default_TABLE_START(t):
    r"\[([\w\.-]+)\]"
    t.value = t.value[1:-1]
    table_control.setter(1)
    t.lexer.begin('table')
    return t


def t_table_TABLE_START(t):
    r"\[([\w\.-]+)\]"
    title = table_control.get_table_title(t.value[1:-1])
    t.value = title
    if (len(title) > 1):
        table_control.setter(len(title))
        t.lexer.begin('table_child')
    return t

def t_table_child_TABLE_START(t):
    r"\[([\w\.-]+)\]"
    table_title = table_control.get_table_title(t.value[1:-1])
    t.value = table_title
    if (len(table_title) > 1):
        table_control.setter(len(table_title))
    else:
        table_control.setter(1)
        t.lexer.begin('table')
    return t

def t_TABLE_START_INLINE(t):
    r'\{([\w\.-]+)\}'
    t.value = t.value[1:-1]
    t.lexer.push_state('table')
    return t


def t_array_ARRAY_START(t):
    r'\=\s?\['
    t.lexer.push_state('array')
    return t


def t_array_ARRAY_END(t):
    r'\]'
    t.lexer.pop_state()
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

data = """
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

lexer.input(data)

while tok := lexer.token():
    print(tok)

# print(parser.parse(texto_input, debug=True)) => debug no yacc