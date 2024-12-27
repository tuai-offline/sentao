import ply.lex as lex
import ply.yacc as yacc


literals = ['{', '}', '[', ']', '(', ')']
reserved = {
    'se' : 'SE',
    'entao' : 'ENTAO',
    'senao' : 'SENAO',
    'para' : 'PARA',
    'faca' : 'FACA',
    'enquanto' : 'ENQUANTO',
    'retorna' : 'RETORNA',
    'leia' : 'LEIA',
    'escreva' : 'ESCREVA', # imprime?
    'erro' : 'ERRO',
    'intervalo' : 'INTERVALO',
    'repita' : 'REPITA',
    'ate' : 'ATE',
    'que' : 'QUE',
    'ig' : 'IG'

    }
tokens =  ['ID', 'STRING', 'INT', 'REAL', 'MAIS', 'MENOS', 'MULT', 'DIV'] + list(reserved.values())

def t_STRING(t):
  r'\"[^\"]*\"'
  return t

def t_ID(t):
  r'[a-zA-Z]\w{0,19}'
  t.type = reserved.get(t.value,'ID')  
  return t

def t_REAL(t):
  r'\d+\.\d+'
  return t

def t_INT(t):
  r'\d+'
  return t

def t_MAIS(t):
  r'\+'
  return t

def t_MENOS(t):
  r'-'
  return t

def t_MULT(t):
  r'\*'
  return t

def t_DIV(t):
  r'/'
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
  print(f'Carácter inválido: {t.value[0]}, na linha {t.lexer.lineno}')


  t.lexer.skip(1)

lexer = lex.lex()

data = '''se (10 * 3 ig 30) entao { 
escreva (10)}'''

lexer.input(data)

for tok in lexer:
  print(tok)

