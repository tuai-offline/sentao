from lexer import tokens
import ply.yacc as yacc
import sys
import os
import argparse
import io

precedence = (
    ('left', 'E', 'OU'),  # Operadores lógicos
    ('left', 'IG', 'DIF'),  # Comparadores
    ('left', 'MENORQ', 'MAIORQ', 'MENORIG', 'MAIORIG'),
    ('left', 'SOMA', 'SUBT'),  # Soma e subtração
    ('left', 'MULT', 'DIV', 'MOD'),  # Multiplicação, divisão e módulo
    ('right', 'SUBTU', 'NEG'),  # Operadores unários (negativo)
)


def writevm(instruction):
    output_file.write(f"{instruction}\n")


def print_err(s):
    print(f"\033[91m{s}\033[0m")


def p_programa_acao(p):
    '''Programa :'''


def p_programa_acao_programa(p):
    '''Programa : Acao Programa'''
    p[0] = p[1]


def p_acao_funcao(p):
    '''Acao : Funcao'''


def p_acao_DeclVariavel(p):
    '''Acao : DeclVariavel'''
    p[0] = p[1]


def p_acao_DeclFuncao(p):
    '''Acao : DeclFuncao'''
    p[0] = p[1]
    writevm('return')


def p_acao_Atribuicao(p):
    '''Acao : Atribuicao'''
    p[0] = p[1]


def p_acao_Condicao(p):
    '''Acao : Condicao'''
    p[0] = p[1]


def p_acao_Ciclo(p):
    '''Acao : Ciclo'''
    p[0] = p[1]


def p_escopo(p):
    '''Escopo : "{" inicio_escopo Programa fim_escopo "}"'''
    p[0] = p[2]


def p_inicio_escopo(p):
    '''inicio_escopo :'''
    parser.decls.append({})
    parser.scope_stack.append(parser.sp)


def p_fim_escopo(p):
    '''fim_escopo :'''
    removed_scope = parser.decls.pop()
    last_sp = parser.scope_stack.pop()
    writevm(f'pop {parser.sp - last_sp}')
    parser.sp = last_sp


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

    for scope in reversed(parser.decls):
        if p[1] in scope:
            writevm(f"storeg {scope[p[1]][0]}")
            return

    print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")
    parser.exito = False
    return


def p_decl_atri_variavel_id(p):
    '''DeclAtriVariavel : ID'''

    p[0] = ('var', p[1], ('const', 0))

    for scope in reversed(parser.decls):
        if p[1] in scope:
            print_err(f"Variavel '{p[1]}' já declarada!")
            parser.exito = False
            return

    writevm("pushi 0")
    parser.decls[-1][p[1]] = parser.sp
    parser.sp += 1


def p_decl_atri_variavel(p):
    '''DeclAtriVariavel : ID "=" Expressao'''

    for scope in reversed(parser.decls):
        if p[1] in parser.decls:
            print_err(f"Variavel '{p[1]}' já declarada!")
            parser.exito = False
            return

    parser.decls[-1][p[1]] = (parser.sp, p[3][1])
    parser.sp += p[3][1]
    p[0] = p[3]


def p_funcao(p):
    '''Funcao : ID "(" ")"'''
    writevm(f'pusha {p[1]}')
    writevm('call')


def p_indexacao(p):
    '''Indexacao : ID "[" INT "]"'''

    for scope in reversed(parser.decls):
        if p[1] in scope:
            p[0] = ('INT', 1)
            if int(p[3]) < -scope[p[1]][1] or int(p[3]) >= scope[p[1]][1]:
                print_err(f"Acesso em array '{p[1]}' fora dos limites!")
                break
            if (int(p[3]) >= 0):
                idx = scope[p[1]][0] + int(p[3])
            else:
                idx = scope[p[1]][0] + scope[p[1]][1] + int(p[3])
            writevm(f"pushg {idx}")
            return
    else:
        print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")

    parser.exito = False
    return


def p_funcao_escreve(p):
    '''Funcao : _ESCREVE "(" ARG ")"'''
    writevm("writes")


def p_funcao_escrevei(p):
    '''Funcao : _ESCREVEI "(" ARG ")"'''
    writevm("writei")


def p_funcao_escrever(p):
    '''Funcao : _ESCREVER "(" ARG ")"'''
    writevm("writer")


def p_funcao_ler(p):
    '''Funcao : _LER "(" ")"'''
    writevm("read")


def p_funcao_leri(p):
    '''Funcao : _LERI "(" ")"'''
    writevm('read')
    writevm('atoi')


def p_funcao_lerr(p):
    '''Funcao : _LERR  "(" ")"'''
    writevm('read')
    writevm('ator')


def p_funcao_ARG(p):
    '''ARG : ID'''
    for scope in reversed(parser.decls):
        if p[1] in scope:
            writevm(f"pushg {scope[p[1]][0]}")
            return

    print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")
    parser.exito = False
    return


def p_funcao_ARG_INT(p):
    '''ARG : INT'''
    writevm("pushi", p[1])


def p_funcao_ARG_REAL(p):
    '''ARG : REAL'''
    writevm("pushf", p[1])


def p_funcao_ARG_CARS(p):
    '''ARG : CARS'''
    writevm("pushs", p[1])


def p_expressao_id(p):
    '''Expressao : ID'''

    for scope in reversed(parser.decls):
        if p[1] in scope:
            p[0] = ('id', p[1])
            writevm(f"pushg {scope[p[1]][0]}")
            return

    print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")
    parser.exito = False
    return


def p_expressao_const(p):
    '''Expressao : TipoConstante'''
    p[0] = p[1]


def p_expressao_funcao(p):
    '''Expressao : Funcao'''
    p[0] = ('INT', 1)


def p_expressao_indexacao(p):
    '''Expressao : Indexacao'''
    p[0] = p[1]


def p_expressao_bin_soma(p):
    '''Expressao : Expressao SOMA Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('add')
    pass


def p_expressao_bin_subt(p):
    '''Expressao : Expressao SUBT Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('sub')
    pass


def p_expressao_bin_mult(p):
    '''Expressao : Expressao MULT Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('mul')
    pass


def p_expressao_bin_div(p):
    '''Expressao : Expressao DIV Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('div')
    pass


def p_expressao_bin_mod(p):
    '''Expressao : Expressao MOD Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('mod')
    pass


def p_expressao_bin_menorq(p):
    '''Expressao : Expressao MENORQ Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('inf')
    pass


def p_expressao_bin_maiorq(p):
    '''Expressao : Expressao MAIORQ Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('sup')
    pass


def p_expressao_bin_menorig(p):
    '''Expressao : Expressao MENORIG Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('infeq')
    pass


def p_expressao_bin_maiorig(p):
    '''Expressao : Expressao MAIORIG Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('supeq')
    pass


def p_expressao_bin_ig(p):
    '''Expressao : Expressao IG Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('equal')
    pass


def p_expressao_bin_dif(p):
    '''Expressao : Expressao DIF Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('dif')
    pass


def p_expressao_bin_e(p):
    '''Expressao : Expressao E Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('and')
    pass


def p_expressao_bin_ou(p):
    '''Expressao : Expressao OU Expressao'''

    p[0] = (p[2], p[1], p[3])
    writevm('or')
    pass


def p_expressao_un_subt(p):
    '''Expressao : SUBT Expressao %prec SUBTU'''
    p[0] = ('neg', p[2])
    writevm('pushi -1')
    writevm('mul')


def p_expressao_un_neg(p):
    '''Expressao : NEG Expressao %prec NEG'''
    pass


def p_expressao_grupo(p):
    '''Expressao : "(" Expressao ")"'''
    p[0] = [2]


def p_tipo_constante_INT(p):
    '''TipoConstante : INT'''
    p[0] = ('INT', 1)
    writevm(f"pushi {p[1]}")


def p_tipo_REAL(p):
    '''TipoConstante : REAL'''
    p[0] = ('REAL', 1)
    writevm(f"pushf {p[1]}")


def p_tipo_CAR(p):
    '''TipoConstante : CAR'''
    p[0] = ('CAR', 1)


def p_tipo_CARS(p):
    '''TipoConstante : CARS'''
    p[0] = ('CARS', 1)


def p_tipo_constante_array(p):
    '''TipoConstante : "[" LTipoConstante "]"'''
    p[0] = (p[2][0], len(p[2]))


def p_l_tipo_constante(p):
    '''LTipoConstante : TipoConstante'''
    p[0] = [p[1]]


def p_l_tipo_constante_lista(p):
    '''LTipoConstante : TipoConstante "," LTipoConstante'''
    p[0] = [p[1]] + p[3]


def p_condicao_se(p):
    '''Condicao : Se "(" Expressao ")" Entao Escopo'''
    writevm(f"{parser.label_stack.pop()}:")


def p_condicao_se_senao(p):
    '''Condicao : Se "(" Expressao ")" Entao Escopo Senao Escopo'''
    writevm(f"{parser.label_stack.pop()}:")


def p_condicao_se_senao_se(p):
    '''Condicao : Se "(" Expressao ")" Entao Escopo Senao Condicao'''
    writevm(f"{parser.label_stack.pop()}:")


def p_se(p):
    '''Se : _SE'''
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_entao(p):
    '''Entao : _ENTAO'''
    writevm(f"jz {parser.label_stack[-1]}")


def p_senao(p):
    '''Senao : _SENAO'''
    a = parser.label_stack.pop()
    writevm(f"jump {parser.label}")
    parser.label_stack.append(parser.label)
    parser.label += 1
    writevm(f"{a}:")


def p_ciclo_para(p):
    '''Ciclo : _PARA ID _NO _INTERVALO "(" INT "," INT ")" Escopo'''
    pass


def p_ciclo_enquanto(p):
    '''Ciclo : Enquanto "(" Expressao ")" Faca Escopo'''
    a = parser.label_stack.pop()
    b = parser.label_stack.pop()
    writevm(f'jump {b}')
    writevm(f'{a}:')


def p_ciclo_enquantoTransicao(p):
    '''Enquanto : _ENQUANTO'''
    writevm(f"{parser.label}:")
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_ciclo_enquanto_faca(p):
    '''Faca : _FACA'''
    writevm(f'jz {parser.label}')
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_ciclo_repita(p):
    '''Ciclo : Repita Escopo _ATE _QUE "(" Expressao ")"'''
    writevm(f"jz {parser.label_stack.pop()}")


def p_ciclo_repitaTRANS(p):
    '''Repita : _REPITA'''
    writevm(f"{parser.label}:")
    parser.label_stack.append(parser.label)
    parser.label += 1


def p_decl_funcao(p):
    '''DeclFuncao : Tipo IdFuncao "(" ")" "{" inicio_escopo Programa _RETORNA Expressao fim_escopo "}"'''
    pass


def p_decl_id_funcao(p):
    '''IdFuncao : ID'''
    parser.fun_decls.append(p[1])
    writevm(f'{p[1]}:')
    writevm(f'start')


def p_error(p):
    return p


def init_parser():
    parser.exito = True
    parser.decls = [{}]
    parser.fun_decls = []
    parser.sp = 0
    parser.scope_stack = []
    parser.label = 0
    parser.label_stack = []


def preludio():
    writevm("jump inicio")


def epilogo():
    if 'inicio' not in parser.fun_decls:
        print_err("Função 'inicio' não declarada!")


if __name__ == '__main__':
    parser = yacc.yacc(debug=True, write_tables=True)
    init_parser()

    parser_args = argparse.ArgumentParser()
    parser_args.add_argument('input_file',
                             nargs='?',
                             help='input file to parse',
                             default=None)
    parser_args.add_argument('-o',
                             '--output',
                             help='output file name',
                             default='output.ewvm')
    args = parser_args.parse_args()

    if args.input_file:
        output_file = io.StringIO()
        with open(args.input_file, 'r') as f:
            preludio()
            parser.parse(f.read(), tracking=True)
            epilogo()
            if parser.exito:
                print(
                    "\033[92mAnálise sintática concluída com sucesso!\033[0m")

                if os.path.exists(args.output):
                    print(
                        f"Ficheiro '{args.output}' já existente. Sobrescrevendo!"
                    )

                with open(args.output, 'w') as out:
                    out.write(output_file.getvalue())
        exit()

    while True:
        output_file = sys.stdout
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
        print("==== Instruções EWVM ====")
        preludio()
        parser.parse(source, tracking=True)
        epilogo()
        if parser.exito:
            print("\033[92mAnálise sintática concluída com sucesso!\033[0m")
            print("Declarações:")
            print(parser.decls)
