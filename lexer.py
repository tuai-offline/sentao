import ply.lex as lex
import sys

literals = '{}[]()=,'

reserved = {
    'ate': '_ATE',
    'auto': '_AUTO',
    'bool': '_BOOL',
    'dynamic': '_DYNAMIC',
    'car': '_CAR',
    'cars': '_CARS',
    'enquanto': '_ENQUANTO',
    'entao': '_ENTAO',
    'faca': '_FACA',
    'int': '_INT',
    'intervalo': '_INTERVALO',
    'no': '_NO',
    'para': '_PARA',
    'que': '_QUE',
    'real': '_REAL',
    'repita': '_REPITA',
    'retorna': '_RETORNA',
    'se': '_SE',
    'senao': '_SENAO',
    'escreve' : '_ESCREVE',
    'escrevei': '_ESCREVEI',
    'escrever': '_ESCREVER',
    'ler': '_LER',
    'leri': '_LERI',
    'lerr': '_LERR',
    'inicio': '_INICIO',
    'def' : '_DEF',

}

tokens = [
    'ID',
    'INT',
    'CAR',
    'CARS',
    'REAL',
    'SOMA',
    'SUBT',
    'MULT',
    'DIV',
    'MOD',
    'MAIORIG',
    'MENORIG',
    'MAIORQ',
    'MENORQ',
    'IG',
    'NEG',
    'DIF',
    'OU',
    'E',
] + list(reserved.values())


def t_CARS(t):
    r'\"[^\"]*\"'
    return t


def t_ID(t):
    r'[a-zA-Z]\w{0,19}'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_REAL(t):
    r'\d+\.\d+'
    return t


def t_INT(t):
    r'\d+'
    return t


def t_CAR(t):
    r"\'[^\']\'"
    return t


def t_SOMA(t):
    r'\+'
    return t


def t_SUBT(t):
    r'-'
    return t


def t_MULT(t):
    r'\*'
    return t


def t_DIV(t):
    r'/'
    return t


def t_MOD(t):
    r'%'
    return t


def t_MAIORIG(t):
    r'>='
    return t


def t_MENORIG(t):
    r'<='
    return t


def t_MAIORQ(t):
    r'>'
    return t


def t_MENORQ(t):
    r'<'
    return t


def t_IG(t):
    r'=='
    return t


def t_NEG(t):
    r'!'
    return t


def t_DIF(t):
    r'!='
    return t


def t_OU(t):
    r'\|\|'
    return t


def t_E(t):
    r'&&'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print(f'Carácter inválido: {t.value[0]}, na linha {t.lexer.lineno}')
    t.lexer.skip(1)


lexer = lex.lex()
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        f = open(sys.argv[1])
        lexer.input(f.read())
        f.close()
        while tok := lexer.token():
            print(tok.type, end=" ")
        print()
        exit()

    while True:
        lines = []
        print("Digite linhas de texto (pressione Ctrl+D para finalizar):")

        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        if not lines:
            break

        source = '\n'.join(lines)
        lexer.input(source)
        while tok := lexer.token():
            print(tok.type, end=" ")
        print()
