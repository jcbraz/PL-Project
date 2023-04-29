import ply.yacc as yacc

from tabela_lex import tokens

def p_tabela(p):
    'tabela : cabecalho linha_lixo conteudo'
    p[0] = p[1] + '\n' + p[3]

def p_cabecalho(p):
    'cabecalho : BARRA valores_cab BARRA'
    p[0] = ','.join(p[2])

def p_valores_cab(p):
    '''valores_cab : valores_cab BARRA valor_cab
                   | valor_cab'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [ p[3] ]

def p_valor_cab(p):
    'valor_cab : TEXTO'
    p[0] = p[1]

def p_linha_lixo(p):
    'linha_lixo : BARRA vals_lixo BARRA'
    pass

def p_vals_lixo(p):
    '''vals_lixo : vals_lixo BARRA TRACOS
                 | TRACOS'''
    pass

def p_conteudo(p):
    '''conteudo : linha
                | conteudo linha'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '\n' + p[2]

def p_linha(p):
    'linha : BARRA valores BARRA'
    p[0] = ','.join(p[2])

def p_valores(p):
    '''valores : valores BARRA valor
               | valor'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [ p[3] ]

def p_valor(p):
    '''valor : TEXTO
             | INT
             | FLOAT'''
    p[0] = str(p[1])

def p_error(p):
    print("Erro sintático!")

parser = yacc.yacc()

texto_input = """
| Nome        | Idade | Género      | Altura | Ocupação         |
|-------------|-------|-------------|--------|------------------|
| Alex        | 32    | Não-binário | 1.72   | Desenvolvimento  |
| Avery       | 29    | Feminino    | 1.85   | Marketing        |
| Casey       | 27    | Masculino   | 1.80   | Apoio ao cliente |
| David       | 40    | Masculino   | 1.76   | Gerente          |
| Emily       | 31    | Feminino    | 1.62   | Designer         |
| Frank       | 25    | Masculino   | 1.81   | Apoio ao cliente |
| Grace       | 38    | Feminino    | 1.68   | Vendas           |
| Harper      | 33    | Não-binário | 1.70   | Desenvolvimento  |
| Ivan        | 30    | Masculino   | 1.77   | Apoio ao cliente |
| Jane        | 29    | Feminino    | 1.74   | Designer         |
| Kim         | 35    | Feminino    | 1.79   | Gerente          |
| Liam        | 28    | Masculino   | 1.83   | Marketing        |
| Morgan      | 26    | Não-binário | 1.67   | Desenvolvimento  |
| Nathan      | 34    | Masculino   | 1.76   | Apoio ao cliente |
| Olivia      | 36    | Feminino    | 1.75   | Gerente          |
| Pat         | 37    | Não-binário | 1.78   | Designer         |
| Quinn       | 27    | Não-binário | 1.68   | Marketing        |
| Rachel      | 39    | Feminino    | 1.69   | Desenvolvimento  |
| Sam         | 23    | Não-binário | 1.70   | Apoio ao cliente |
| Taylor      | 31    | Não-binário | 1.81   | Vendas           |
"""

csv = parser.parse(texto_input)

with open("tabela.csv", "w") as f:
    f.write(csv)