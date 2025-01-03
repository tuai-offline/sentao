from lexer import tokens
import ply.yacc as yacc
import sys

precedence = (
    ('left', 'E', 'OU'),  # Operadores lógicos
    ('left', 'IG', 'DIF'),  # Comparadores
    ('left', 'MENORQ', 'MAIORQ', 'MENORIG', 'MAIORIG'),
    ('left', 'SOMA', 'SUBT'),  # Soma e subtração
    ('left', 'MULT', 'DIV', 'MOD'),  # Multiplicação, divisão e módulo
    ('right', 'SUBTU', 'NEG'),  # Operadores unários (negativo)
)


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


def p_expressao_bin_soma(p):
    '''Expressao : Expressao SOMA Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('add')
    pass


def p_expressao_bin_subt(p):
    '''Expressao : Expressao SUBT Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('sub')
    pass


def p_expressao_bin_mult(p):
    '''Expressao : Expressao MULT Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('mul')
    pass


def p_expressao_bin_div(p):
    '''Expressao : Expressao DIV Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('div')
    pass


def p_expressao_bin_mod(p):
    '''Expressao : Expressao MOD Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('mod')
    pass


def p_expressao_bin_menorq(p):
    '''Expressao : Expressao MENORQ Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('inf')
    pass


def p_expressao_bin_maiorq(p):
    '''Expressao : Expressao MAIORQ Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('sup')
    pass


def p_expressao_bin_menorig(p):
    '''Expressao : Expressao MENORIG Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('infq')
    pass


def p_expressao_bin_maiorig(p):
    '''Expressao : Expressao MAIORIG Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('sup')
    pass


def p_expressao_bin_ig(p):
    '''Expressao : Expressao IG Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('equal')
    pass


def p_expressao_bin_dif(p):
    '''Expressao : Expressao DIF Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('dif')
    pass


def p_expressao_bin_e(p):
    '''Expressao : Expressao E Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('e')
    pass


def p_expressao_bin_ou(p):
    '''Expressao : Expressao OU Expressao'''

    p[0] = (p[2], p[1], p[3])
    print('ou')
    pass


def p_expressao_un_subt(p):
    '''Expressao : SUBT Expressao %prec SUBTU'''
    p[0] = ('neg', p[2])
    print('pushi -1')
    print('mul')


def p_expressao_un_neg(p):
    '''Expressao : NEG Expressao %prec NEG'''
    pass


def p_expressao_grupo(p):
    '''Expressao : "(" Expressao ")"'''
    p[0] = [2]


def p_tipo_constante_INT(p):
    '''TipoConstante : INT'''
    p[0] = ('INT', int(p[1]))


def p_tipo_REAL(p):
    '''TipoConstante : REAL'''
    p[0] = ('REAL', float(p[1]))


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
    print(f"{parser.label_stack.pop()}:")


def p_se(p):
    '''Se : _SE'''
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_entao(p):
    '''Entao : _ENTAO'''
    print(f"jz {parser.label_stack[-1]}")


def p_condicao_se_senao(p):
    '''Condicao : Se "(" Expressao ")" Entao "{" Programa "}" Senao "{" Programa "}"'''
    print(f"{parser.label_stack.pop()}:")


def p_condicao_se_senao_se(p):
    '''Condicao : Se "(" Expressao ")" Entao "{" Programa "}" Senao Condicao'''
    print(f"{parser.label_stack.pop()}:")


def p_senao(p):
    '''Senao : _SENAO'''
    a = parser.label_stack.pop()
    print(f"jump {parser.label}")
    parser.label_stack.append(parser.label)
    parser.label += 1
    print(f"{a}:")


def p_ciclo_para(p):
    '''Ciclo : _PARA ID _NO _INTERVALO "(" INT "," INT ")" "{" Programa "}"'''
    pass


def p_ciclo_enquanto(p):
    '''Ciclo : Enquanto "(" Expressao ")" Faca "{" Programa "}"'''
    a = parser.label_stack.pop()
    b = parser.label_stack.pop()
    print(f'jump {b}')
    print(f'{a}:')


def p_ciclo_enquantoTransicao(p):
    '''Enquanto : _ENQUANTO'''
    print(f"{parser.label}:")
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_ciclo_enquanto_faca(p):
    '''Faca : _FACA'''
    print(f'jz {parser.label}')
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_ciclo_repita(p):
    '''Ciclo : Repita "{" Programa "}" _ATE _QUE "(" Expressao ")"'''

    print(f"jz {parser.label_stack.pop()}")


def p_ciclo_repitaTRANS(p):
    '''Repita : _REPITA'''

    print(f"{parser.label}:")
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_decl_funcao(p):
    '''DeclFuncao : Tipo ID "(" ")" "{" Programa _RETORNA Expressao "}"'''
    pass


def p_decl_funcao_simples(p):
    '''DeclFuncao : Tipo ID "(" ")" "{" _RETORNA Expressao "}"'''
    pass


def p_error(p):
    return p


def init_parser():
    parser.exito = True
    parser.decls = {}
    parser.sp = 0
    parser.label = 0
    parser.label_stack = []


if __name__ == '__main__':
    parser = yacc.yacc(debug=True, write_tables=True)
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
