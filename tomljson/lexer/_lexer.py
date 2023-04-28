import ply.lex as lex

states = (
    ("array", "inclusive"),
    ("table", "inclusive"),
    ("child", "inclusive"),
)

tokens = (
    "EQUAL",
    "VARIABLE",
    "STRING",
    "INTEGER",
    "FLOAT",
    "BOOLEAN",
    "DATE",
    "LBRACKET",
    "RBRACKET",
    "LCURLY",
    "RCURLY",
    "COMMA",
    "DOT",
    "SPACE",
    "NEWLINE",
    "COMMENT",
    "TABLE_HEADER",
    "CHILD_HEADER",
    "ARRAY_TABLES_HEADER",
)

# table_control = TableControl()

t_EQUAL = r"="
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LCURLY = r"\{"
t_RCURLY = r"\}"
t_COMMA = r","
t_DOT = r"\."
t_SPACE = r"\s+"
t_ignore = " \t"


# Add support for comments
# initialize default state
def t_ANY_COMMENT(t):
    r"\#.*"
    pass


# Add support for dates
def t_ANY_DATE(t):
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2})?"
    return t


def t_ANY_VARIABLE(t):
    r"\w+\s?="
    if t.value[-2] == " ":
        t.value = t.value[:-2]
    else:
        t.value = t.value[:-1]
    return t


# def t_ANY_STRING(t):
#     r'"([^"\\]|\\.)*"'
#     return t
def t_ANY_STRING(t):
    r"[\"'](?:\s?\w+)+[\"']"
    return t

def t_ANY_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ANY_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_ANY_BOOLEAN(t):
    r"(true|false)"
    t.value = True if t.value == "true" else False
    return t


def t_ANY_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    pass


def t_TABLE_HEADER(t):
    r"\[\w*\]\n*?"
    t.lexer.begin("table")
    return t


def t_ARRAY_TABLES_HEADER(t):
    r"\[\[[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]*)*\]\]"
    t.lexer.begin("array")
    return t


def t_table_TABLE_HEADER(t):
    r"\[\w*\]\n*?"
    return t


def t_table_CHILD_HEADER(t):
    r"\[[a-zA-Z]+\.(?:[a-zA-Z]*\.)*[a-zA-Z]*\]"
    t.lexer.begin("child")
    return t


def t_child_TABLE_HEADER(t):
    r"\[\w*\]\n*?"
    t.lexer.begin("table")
    return t


def t_child_CHILD_HEADER(t):
    r"\[[a-zA-Z]+\.(?:[a-zA-Z]*\.)*[a-zA-Z]*\]"
    return t


def t_ANY_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()
