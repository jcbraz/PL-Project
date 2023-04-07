import ply.lex as lex

states = (
    ('default', 'exclusive'),
    ('section', 'exclusive'),
    ('array', 'exclusive'),
)

tokens = (
    'TITLE',
    'NEWLINE',
    'QUOTE',
    'LBRACKET',
    'RBRACKET',
    'TAGINSIDEBRACKETS',
    'COMMENT'
)

t_TITLE = r'title'
t_NEWLINE = r'\n'
t_QUOTE = r'[\"\']'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMENT = r'\#.*'


def t_TITLE(t):
    r'title\s*=\s*"([a-zA-Z0-9_]*)'
    t.value = t.group(1)
    return t


def t_SECTION(t):
    r'\[[a-zA-Z0-9_]+\]\n'
    t.value = t.group(1)
    return t

def t_SECTION_BEGIN(t):
    r'\['
    t.lexer.push_state('section')

def t_SECTION_END(t):
    r'([a-zA-Z0-9_]+)\]'
    t.value = t.group(1)
    t.lexer.pop_state()
    return t

def t_ARRAY_BEGIN(t):
    r'([a-zA-Z0-9_]+)\s*=\s*\['
    t.value = t.group(1)
    t.lexer.push_state('array')
    return t

def t_ARRAY_CONTENT(t):
    r'([[a-zA-Z0-9_]|,|"]+)'
    t.value = t.group(1)
    return t

def t_ARRAY_END(t):
    r'\]'
    t.lexer.pop_state()

# def t_SECTION_BEGIN(t):
#     r'\[[a-zA-Z0-9_]+\]'
#     t.lexer.push_state('section')


# def t_SECTION_END(t):
#     r'\n'
#     if t.lexer.statestack:
#         t.lexer.pop_state()


def t_array_BEGIN(t):
    r'=\s*\['
    t.lexer.push_state('array')


def t_array_END(t):
    r'\]'
    if t.lexer.statestack:
        t.lexer.pop_state()


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data = '''
title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
date = 2010-04-23
time = 21:30:00

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]
[servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"
[servers.beta]
  ip = "10.0.0.2"
  dc = "eqdc10"

# Line breaks are OK when inside arrays
hosts = [
    "alpha",
    "omega" 
    ]
'''

lexer.input(data)
while tok := lexer.token():
    print(tok)