#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: [ ps.ply ])"
from lexer import tokens
import ply.yacc as yacc
import sys


def p_programa_acao(p):
    '''Programa : Acao'''
    p[0] = p[1]


def p_programa_acao_programa(p):
    '''Programa : Acao Programa'''
    p[0] = p[1]


def p_acao_DeclVariavel(p):
    '''Acao : DeclVariavel'''
    p[0] = p[1]


def p_acao_DeclFuncao(p):
    '''Acao :  DeclFuncao'''
    p[0] = p[1]


def p_acao_Atribuicao(p):
    '''Acao : Atribuicao'''
    p[0] = p[1]


def p_acao_Condicao(p):
    '''Acao : Condicao'''
    p[0] = p[1]


def p_acao_Ciclo(p):
    '''Acao : Ciclo'''
    p[0] = p[1]


def p_decl_variavel(p):
    '''DeclVariavel : Tipo LDeclVariaveis'''
    p[0] = p[1]


def p_tipo_INT(p):
    '''Tipo : _INT'''
    p[0] = p[1]


def p_tipo__REAL(p):
    '''Tipo : _REAL'''
    p[0] = p[1]


def p_tipo_AUTO(p):
    '''Tipo : _AUTO'''
    p[0] = p[1]


def p_tipo_DYNAMIC(p):
    '''Tipo : _DYNAMIC'''
    p[0] = p[1]


def p_tipo__CAR(p):
    '''Tipo : _CAR'''
    p[0] = p[1]


def p_tipo__CARS(p):
    '''Tipo : _CARS'''
    p[0] = p[1]


def p_tipo_BOOL(p):
    '''Tipo : _BOOL'''
    p[0] = p[1]


def p_tipo_array(p):
    '''Tipo : Tipo "[" INT "]"'''
    pass


def p_l_variaveis(p):
    '''LDeclVariaveis : DeclAtriVariavel'''
    p[0] = [p[1]]


def p_l_variaveis_lista(p):
    '''LDeclVariaveis : DeclAtriVariavel "," LDeclVariaveis'''
    p[0] = [p[1]] + p[3]


def p_atribuicao(p):
    '''Atribuicao : ID "=" Expressao'''
    p[0] = (p[1], p[3])
    if p[1] not in parser.decls:
        print("Variavel não declarada!")
        parser.exito = False
        return

    print(f"storeg {parser.decls[p[1]]}")


def p_decl_atri_variavel_id(p):
    '''DeclAtriVariavel : ID'''
    p[0] = ('var', p[1], ('const', 0))
    if p[1] in parser.decls:
        print("Variavel já declarada!")
        parser.exito = False
        return
    print("pushi 0")
    parser.decls[p[1]] = parser.sp
    parser.sp += 1


def p_decl_atri_variavel(p):
    '''DeclAtriVariavel : ID "=" Expressao'''
    p[0] = ('var', p[1], p[3])
    if p[1] in parser.decls:
        print("Variavel já declarada!")
        parser.exito = False
        return
    parser.decls[p[1]] = parser.sp
    parser.sp += 1


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
    print(f"pushg {parser.decls[p[1]]}")


def p_expressao_const(p):
    '''Expressao : TipoConstante'''

    p[0] = ('const', *p[1])
    print(f"pushi {p[1][1]}")


def p_expressao_funcao(p):
    '''Expressao : Funcao'''

    p[0] = ('fun', p[1])


def p_expressao_bin(p):
    '''Expressao : Expressao OpBinario Expressao'''

    p[0] = (p[2], p[1], p[3])
    print(p[2])
    pass


def p_expressao_un(p):
    '''Expressao : OpUnario Expressao'''
    pass


def p_expressao_grupo(p):
    '''Expressao : "(" Expressao ")"'''
    pass


def p_op_binario_SOMA(p):
    '''OpBinario : SOMA '''
    p[0] = 'add'


def p_op_binario_SUBT(p):
    '''OpBinario : SUBT'''
    p[0] = 'sub'


def p_op_binario_MULT(p):
    '''OpBinario : MULT'''
    p[0] = 'mul'


def p_op_binario_DIV(p):
    '''OpBinario : DIV'''
    p[0] = 'div'


def p_op_binario_MOD(p):
    '''OpBinario : MOD'''
    p[0] = 'mod'


def p_op_binario_MENORQ(p):
    '''OpBinario : MENORQ'''
    p[0] = 'inf' 


def p_op_binario_MAIORQ(p):
    '''OpBinario : MAIORQ'''
    p[0] = 'sup'


def p_op_binario_MENORIG(p):
    '''OpBinario : MENORIG'''
    p[0] = 'infq'


def p_op_binario_MAIORIG(p):
    '''OpBinario : MAIORIG'''
    p[0] = 'supq'


def p_op_binario_IG(p):
    '''OpBinario : IG'''
    p[0] = 'equal'


def p_op_binario_DIF(p):
    '''OpBinario : DIF'''
    p[0] = p[1]


def p_op_binario_E(p):
    '''OpBinario : E'''
    p[0] = p[1]


def p_op_binario_OU(p):
    '''OpBinario : OU'''
    p[0] = p[1]


def p_op_unario_NEG(p):
    '''OpUnario : NEG'''
    p[0] = 'neg'


def p_op_unario_SUBT(p):
    '''OpUnario : SUBT'''
    p[0] = p[1]


def p_tipo_constante_INT(p):
    '''TipoConstante : INT'''
    p[0] = ('INT', p[1])


def p_tipo_REAL(p):
    '''TipoConstante : REAL'''
    p[0] = ('REAL', p[1])


def p_tipo_CAR(p):
    '''TipoConstante : CAR'''
    p[0] = ('CAR', p[1])


def p_tipo_CARS(p):
    '''TipoConstante : CARS'''
    p[0] = ('CARS', p[1])


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
    '''Condicao : Se "(" Expressao ")" Entao "{" Programa "}"'''
    print(f"{parser.label}:")
    parser.label += 1


def p_se(p):
    '''Se : _SE'''
    parser.label_stack.append(parser.label)


def p_entao(p):
    '''Entao : _ENTAO'''
    print(f"jz {parser.label_stack.pop()}")


def p_condicao_se_senao(p):
    '''Condicao : Se "(" Expressao ")" Entao "{" Programa "}" _SENAO "{" Programa "}"'''
    pass


def p_condicao_se_senao_se(p):
    '''Condicao : Se "(" Expressao ")" Entao "{" Programa "}" _SENAO Condicao'''
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


def init_parser(p):
    parser.exito = True
    parser.decls = {}
    parser.sp = 0
    parser.label = 0
    parser.label_stack = []


if __name__ == '__main__':
    parser = yacc.yacc()
    init_parser()

    if (len(sys.argv) > 1):
        f = open(sys.argv[1])
        parser.parse(f.read(), tracking=True)
        f.close()
        if parser.exito:
            print("\033[92mAnálise sintática concluída com sucesso!\033[0m")
        exit()

    while True:
        init_parser()
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
