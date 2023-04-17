import ply.lex as lex
import datetime


class StackControl:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1

    def decrement(self):
        self.counter -= 1

    def get(self):
        return self.counter

    def get_table_title(t):
        title = t.split('.')
        return title


stack_control = StackControl()

states = (
    ("default", "exclusive"),
    ("array", "exclusive"),
    ("table", "inclusive"),
    ("table_child", "inclusive"),
)

tokens = (
    'COMMENT',
    'DATE',
    'TIME',
    'FLOAT',
    'INTEGER',
    'BOOLEAN',
    'STRING',
    'TABLE_START',
    'TABLE_START_INLINE'
    'TABLE_END',
    'TABLE_END_INLINE',
    'ARRAY_START',
    'ARRAY_END'
)

t_ignore = ' \t'


def t_COMMENT(t):
    r'\#.*'
    pass


def t_DATE(t):
    r'\d{4}-\d{2}-\d{2}'
    t.value = datetime.datetime.strptime(t.value, '%Y-%m-%d').date()
    return t


def t_LOCALDATE(t):
    r'\d{4}-\d{2}-\d{2}'
    t.value = datetime.datetime.strptime(t.value.group(0), '%Y-%m-%d').date()
    return t


def t_LOCALTIME(t):
    r'\d{2}:\d{2}:\d{2}'
    t.value = datetime.datetime.strptime(t.value.group(0), '%H:%M:%S').time()
    return t


def t_LOCALTIME_MILISECONDS(t):
    r'\d{2}:\d{2}:\d{2}\.\d+'
    t.value = datetime.datetime.strptime(
        t.value.group(0), '%H:%M:%S.%f').time()
    return t


def t_LOCALDATE_TIME(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    t.value = datetime.datetime.strptime(t.value.group(0), '%Y-%m-%dT%H:%M:%S')
    return t


def t_ISO8601_DATE(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'
    t.value = datetime.datetime.strptime(
        t.value.group(0), '%Y-%m-%dT%H:%M:%SZ')
    return t


def t_RFC3339_DATE(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z'
    t.value = datetime.datetime.strptime(t.value.group(0), '%Y-%m-%dT%H:%M:%S')
    return t


def t_LOCALDATE_TIME_MILLISECONDS(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+'
    t.value = datetime.datetime.strptime(
        t.value.group(0), '%Y-%m-%dT%H:%M:%S.%f')
    return t


def t_FLOAT(t):
    r"\d*\.\d+([eE][-+]?\d+)?"
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r"true|false"
    t.value = bool(t.value)
    return t


def t_STRING(t):
    r'"([^"\n]*)"?'
    t.value = t.value[1:-1]
    return t


def t_TABLE_START(t):
    r"\[([\w\.-]+)\]"
    t.value = t.value[1:-1]
    if t.lexer.current_state():
        stack_control.increment()
        t.lexer.push_state('table_child')
    else:
        stack_control.increment()
        t.lexer.push_state('table')
    return t


def t_TABLE_START_INLINE(t):
    r'\{'
    stack_control.increment()
    t.lexer.push_state('table')
    return t


def t_TABLE_END(t):
    r"\[([\w\.-]+)\]"
    table_title = stack_control.get_table_title(t.value[1:-1])
    if len(table_title) == 1 and t.lexer.current_state() == 'table_child':
        stack_control.decrement()
        stack_control.decrement()
        t.lexer.pop_state()
        t.lexer.pop_state()
    elif len(table_title) == 1 and t.lexer.current_state() == 'table':
        stack_control.decrement()
        t.lexer.pop_state()
    else:
        for _ in range(stack_control.get()):
            stack_control.decrement()
            t.lexer.pop_state()


def t_TABLE_END_INLINE(t):
    r'\}'
    t.lexer.pop_state()
    return t


def t_ARRAY_START(t):
    r'\=\s?\['
    t.lexer.push_state('array')
    return t


def t_ARRAY_END(t):
    r'\]'
    t.lexer.pop_state()
    return t


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
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
