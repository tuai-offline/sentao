#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: [ ps.ply ])"
from lexer import tokens
import ply.yacc as yacc
import sys


def p_programa_acao(p):
    '''Programa : Acao'''
    pass


def p_programa_acao_programa(p):
    '''Programa : Acao Programa'''
    pass


def p_acao(p):
    '''Acao : DeclVariavel
            | DeclFuncao
            | Atribuicao 
            | Condicao
            | Ciclo'''
    pass


def p_decl_variavel(p):
    '''DeclVariavel : Tipo LVariaveis'''
    pass


def p_tipo(p):
    '''Tipo : _INT
            | _REAL
            | _AUTO
            | _DYNAMIC
            | _CAR
            | _CARS
            | _BOOL'''
    pass


def p_tipo_array(p):
    '''Tipo : Tipo "[" INT "]"'''
    pass


def p_l_variaveis(p):
    '''LVariaveis : Variavel'''
    pass


def p_l_variaveis_lista(p):
    '''LVariaveis : Variavel "," LVariaveis'''
    pass


def p_variavel_id(p):
    '''Variavel : ID'''
    pass


def p_variavel_atrib(p):
    '''Variavel : Atribuicao'''
    pass


def p_atribuicao(p):
    '''Atribuicao : ID "=" Expressao'''
    parser.decls[p[1]] = p[3]


def p_funcao(p):
    '''Funcao : ID "(" ")"'''
    pass


def p_expressao_id(p):
    '''Expressao : ID'''
    if p[1] not in parser.decls:
        print(f"Variável {p[1]} não declarada!")
        parser.exito = False
        return

    p[0] = ('id', p[1])


def p_expressao_const(p):
    '''Expressao : TipoConstante'''

    p[0] = ('const', p[1])


def p_expressao_funcao(p):
    '''Expressao : Funcao'''

    p[0] = ('fun', p[1])


def p_expressao_bin(p):
    '''Expressao : Expressao OpBinario Expressao'''

    p[0] = (p[2], p[1], p[3])
    pass


def p_expressao_un(p):
    '''Expressao : OpUnario Expressao'''
    pass


def p_expressao_grupo(p):
    '''Expressao : "(" Expressao ")"'''
    pass


def p_op_binario(p):
    '''OpBinario : SOMA
                 | SUBT
                 | MULT
                 | DIV
                 | MENORQ
                 | MAIORQ
                 | MENORIG
                 | MAIORIG
                 | IG
                 | DIF
                 | E
                 | OU'''
    p[0] = p[1]


def p_op_unario(p):
    '''OpUnario : NEG
                | SUBT'''
    pass


def p_tipo_constante(p):
    '''TipoConstante : INT
                     | REAL
                     | CAR
                     | CARS'''

    p[0] = p[1]


def p_tipo_constante_array(p):
    '''TipoConstante : "[" LTipoConstante "]"'''
    pass


def p_l_tipo_constante(p):
    '''LTipoConstante : TipoConstante'''
    pass


def p_l_tipo_constante_lista(p):
    '''LTipoConstante : TipoConstante "," LTipoConstante'''
    pass


def p_condicao_se(p):
    '''Condicao : _SE "(" Expressao ")" _ENTAO "{" Programa "}"'''
    pass


def p_condicao_se_senao(p):
    '''Condicao : _SE "(" Expressao ")" _ENTAO "{" Programa "}" _SENAO "{" Programa "}"'''
    pass


def p_condicao_se_senao_se(p):
    '''Condicao : _SE "(" Expressao ")" _ENTAO "{" Programa "}" _SENAO Condicao'''
    pass


def p_ciclo_para(p):
    '''Ciclo : _PARA ID _NO _INTERVALO "(" INT "," INT ")" "{" Programa "}"'''
    pass


def p_ciclo_enquanto(p):
    '''Ciclo : _ENQUANTO "(" Expressao ")" _FACA "{" Programa "}"'''
    pass


def p_ciclo_repita(p):
    '''Ciclo : _REPITA "{" Programa "}" _ATE _QUE "(" Expressao ")"'''
    pass


def p_decl_funcao(p):
    '''DeclFuncao : Tipo ID "(" ")" "{" Programa _RETORNA Expressao "}"'''
    pass


def p_decl_funcao_simples(p):
    '''DeclFuncao : Tipo ID "(" ")" "{" _RETORNA Expressao "}"'''
    pass


def p_error(p):
    return p


if __name__ == '__main__':
    parser = yacc.yacc()
    parser.exito = True
    parser.decls = {}

    if (len(sys.argv) > 1):
        f = open(sys.argv[1])
        parser.parse(f.read(), tracking=True)
        f.close()
        if parser.exito:
            print("\033[92mAnálise sintática concluída com sucesso!\033[0m")
        exit()

    while True:
        parser.exito = True

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
        parser.parse(source, tracking=True)
        if parser.exito:
            print("\033[92mAnálise sintática concluída com sucesso!\033[0m")
            print("Declarações:")
            print(parser.decls)
