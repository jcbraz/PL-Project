import ply.lex as lex

tokens = (
    'KEY',
    'EQUAL',
    'STRING',
    'INTEGER',
    'FLOAT',
    'BOOLEAN',
    'LBRACKET',
    'RBRACKET',
    'LCURLY',
    'RCURLY',
    'COMMA',
    'DOT',
    'NEWLINE',
    'COMMENT',
    'DATE'
)

t_EQUAL = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r','
t_DOT = r'\.'
t_ignore = ' \t'

# Add support for comments
def t_COMMENT(t):
    r'\#.*'
    pass

# Add support for dates
def t_DATE(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2})?'
    return t

# Update the regular expression for keys
def t_KEY(t):
    r'([a-zA-Z_][a-zA-Z_0-9]*(\.[a-zA-Z_][a-zA-Z_0-9]*)*)|("[^"]+")'
    return t

def t_STRING(t):
    r'"(?:[^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_BOOLEAN(t):
    r'(true|false)'
    t.value = True if t.value == 'true' else False
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# data = """
# # This is a TOML document. Boom.
# title = "TOML Example"

# [owner]
# name = "Tom Preston-Werner"
# dob = 1979-05-27T07:32:00-08:00

# [database]
# enabled = true
# ports = [ 8000, 8001, 8002 ]
# data = [ ["delta", "phi"], [3.14] ]
# temp_targets = { cpu = 79.5, case = 72.0 }

# [servers]

# [servers.alpha]
# ip = "10.0.0.1"
# role = "frontend"

# [servers.beta]
# ip = "10.0.0.2"
# role = "backend"
# """

# lexer.input(data)

# while tok := lexer.token():
#     print(tok)
