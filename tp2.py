#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: [ ps.ply ])"
import ply.lex as lex
import sys

literals = '{}[]()=,'
reserved = {
    'ate': 'ATE',
    'auto': 'AUTO',
    'enquanto': 'ENQUANTO',
    'entao': 'ENTAO',
    'erro': 'ERRO',
    'escreva': 'ESCREVA',
    'faca': 'FACA',
    'intervalo': 'INTERVALO',
    'leia': 'LEIA',
    'no': 'NO',
    'para': 'PARA',
    'que': 'QUE',
    'repita': 'REPITA',
    'retorna': 'RETORNA',
    'se': 'SE',
    'senao': 'SENAO'
}

tokens = [
    'ID', 'STRING', 'INT', 'REAL', 'SOMA', 'SUBT', 'MULT', 'DIV', 'MAIORIG',
    'MENORIG', 'MAIORQ', 'MENORQ', 'IG', 'DIF'
] + list(reserved.values())


def t_STRING(t):
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


def t_DIF(t):
    r'!='
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
