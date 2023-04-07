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
)

t_TITLE = r'title'
t_NEWLINE = r'\n'
t_QUOTE = r'[\"\']'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_TAGINSIDEBRACKETS = r'[a-zA-Z0-9_]+'

def t_section_begin(t):
    r'\[[a-zA-Z0-9_]+\]\n'
    t.lexer.push_state('section')

def t_section_end(t):
    r'\n'
    if t.lexer.statestack:
        t.lexer.pop_state()

def t_array_begin(t):
    r'=\s*\['
    t.lexer.push_state('array')

def t_array_end(t):
    r'\]'
    if t.lexer.statestack:
        t.lexer.pop_state()

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

