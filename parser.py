from lexer import tokens
import ply.yacc as yacc
import sys
import os
import argparse
import io
from enum import Enum


class Tipo(Enum):
    AUTO = -1
    INT = 1
    REAL = 2
    CARS = 3


class TipoAST():

    def __init__(self, tipo, *dimensoes):
        self.tipo = tipo
        self.dimensoes = list(dimensoes) if dimensoes else [1]

    def real(self):
        return self.tipo == Tipo.REAL

    def int(self):
        return self.tipo == Tipo.INT

    def numerico(self):
        return self.tipo in [Tipo.INT, Tipo.REAL]

    def cars(self):
        return self.tipo == Tipo.CARS

    def singular(self):
        return len(self.dimensoes) == 1 and self.dimensoes[0] == 1

    def tamanho(self):
        n = 1
        for num in self.dimensoes:
            n *= num
        return n

    def subarray(self, n):
        if self.dimensoes[0] == 1:
            self.dimensoes = self.dimensoes[1:]
        self.dimensoes.insert(0, n)
        return self

    def array(self, n):
        if self.dimensoes[-1] == 1:
            self.dimensoes = self.dimensoes[:-1]
        self.dimensoes.append(n)
        return self

    def __eq__(self, dir):
        return dir and self.tipo == dir.tipo and self.dimensoes == dir.dimensoes

    def __str__(self):
        str = f"{self.tipo.name}"
        for num in self.dimensoes:
            str += f"[{num}]"

        return str


def compativel(esq, dir):
    if not esq or not dir:
        return None
    elif esq == dir:
        return esq
    elif esq.dimensoes == dir.dimensoes:
        if esq.int() and dir.int():
            return TipoAST(Tipo.INT, *esq.dimensoes)
        elif esq.numerico() and dir.numerico():
            return TipoAST(Tipo.REAL, *esq.dimensoes)
        elif esq.cars() and dir.cars():
            return TipoAST(Tipo.CARS, *esq.dimensoes)

    print_err(f'Tipos incompatíveis "{esq}" e "{dir}"!')
    return None


precedence = (
    ('left', 'OU'),  # Operadores lógicos
    ('left', 'E'),  # Operadores lógicos
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
    parser.exito = False


def p_estrutura_vazia(p):
    '''Estrutura : '''


def p_estrutura(p):
    '''Estrutura : Global'''


def p_estrutura_inicio(p):
    '''Estrutura : Global preludio DeclFuncoes'''


def p_Preludio(p):
    '''preludio : '''

    writevm("start")
    writevm("pusha inicio")
    writevm("call")
    writevm("stri")
    writevm('pushs "Programa terminou com resultado: "')
    writevm("concat")
    writevm('writes')
    writevm("stop")
    parser.global_flag = 0


def p_estrutural_sem_global(p):
    '''Estrutura : preludio DeclFuncoes'''


def p_global(p):
    '''Global : Programa'''


def p_declFuncoes_unica(p):
    '''DeclFuncoes : DeclInicio'''


def p_declFuncoes(p):
    '''DeclFuncoes : DeclFuncao DeclFuncoes'''


def p_inicio(p):
    '''DeclInicio : AssinaturaFuncaoInicio CorpoFuncao'''


def p_programa_acao(p):
    '''Programa : Acao'''


def p_programa_acao_programa(p):
    '''Programa : Acao Programa'''
    p[0] = p[1]


def p_acao_funcao(p):
    '''Acao : ChamarFuncao'''
    p[0] = p[1]


def p_acao_DeclVariavel(p):
    '''Acao : DeclVariavel'''
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


def p_escopo(p):
    '''Escopo : "{" inicio_escopo Programa fim_escopo "}"'''
    p[0] = p[2]


def inicio_escopo():
    parser.decls.append({})
    parser.escopo_stack.append(
        parser.sp_global if parser.global_flag else parser.sp)


def fim_escopo():
    parser.decls.pop()
    last_sp = parser.escopo_stack.pop()

    sp = parser.sp_global if parser.global_flag else parser.sp
    if sp - last_sp > 0:
        writevm(f'pop {sp - last_sp}')

    if parser.global_flag:
        parser.sp_global = last_sp
    else:
        parser.sp = last_sp


def p_inicio_escopo(p):
    '''inicio_escopo :'''
    inicio_escopo()


def p_fim_escopo(p):
    '''fim_escopo :'''
    fim_escopo()


def inicializacao0(var):
    if var.tipo == Tipo.AUTO:
        print_err(f'Impossível inferir tipo de variável "{nome}"!')
    elif var.int():
        writevm("pushi 0")
    elif var.real():
        writevm("pushf 0")
    elif var.cars():
        writevm('pushs ""')
    else:
        assert False, "Inalcancavel!"


def p_decl_variavel(p):
    '''DeclVariavel : Tipo LDeclVariaveis'''
    esq = p[1]
    for nome, dir in sorted(p[2], key=lambda x: (x[1] is None, x)):
        if dir:
            if esq.tipo == Tipo.AUTO:
                esq = dir
            elif compativel(esq, dir) and compativel(esq, dir) != esq:
                print_err(f'Tipos incompatíveis "{esq}" e "{dir}"!')
        else:
            inicializacao0(esq)

        escopo_alloc(nome, esq)


def p_tipo_INT(p):
    '''Tipo : _INT'''
    p[0] = TipoAST(Tipo.INT)


def p_tipo__REAL(p):
    '''Tipo : _REAL'''
    p[0] = TipoAST(Tipo.REAL)


def p_tipo_AUTO(p):
    '''Tipo : _AUTO'''
    p[0] = TipoAST(Tipo.AUTO)


def p_tipo__CAR(p):
    '''Tipo : _CAR'''
    p[0] = TipoAST(Tipo.INT)


def p_tipo__CARS(p):
    '''Tipo : _CARS'''
    p[0] = TipoAST(Tipo.CARS)


def p_tipo_BOOL(p):
    '''Tipo : _BOOL'''
    p[0] = TipoAST(Tipo.INT)


def p_tipo_array(p):
    '''Tipo : Tipo "[" INT "]"'''
    p[0] = p[1].array(int(p[3]))


def p_l_variaveis(p):
    '''LDeclVariaveis : DeclAtriVariavel'''
    p[0] = [p[1]]


def p_l_variaveis_lista(p):
    '''LDeclVariaveis : DeclAtriVariavel "," LDeclVariaveis'''
    p[0] = [p[1]] + p[3]


def p_atribuicao(p):
    '''Atribuicao : ID "=" Expressao'''
    p[0] = (p[1], p[3])

    if compativel(p[1], p[3]) and compativel(p[1], p[3]) != p[3]:
        print_err(f'Tipos incompatíveis "{esq}" e "{dir}"!')
        return

    for escopo in reversed(parser.decls):
        if p[1] in escopo:
            if p[1] in parser.decls_global:
                writevm(f"storeg {escopo[p[1]][0]}")
            else:
                writevm(f"storel {escopo[p[1]][0]}")
            return

    print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")
    return


def p_atribuicao_array(p):
    '''Atribuicao : IndexacaoEscrita "=" Expressao'''

    if compativel(p[1], p[3]) and compativel(p[1], p[3]) != p[3]:
        print_err(f'Tipos incompatíveis "{esq}" e "{dir}"!')
        return

    writevm("storen")


def escopo_alloc(nome, tipo):
    assert nome not in parser.decls[-1], "Variável com ID já existente!"
    if parser.global_flag:
        parser.decls[-1][nome] = (parser.sp_global, tipo)
        ret = parser.sp_global
        parser.sp_global += tipo.tamanho()
    else:
        parser.decls[-1][nome] = (parser.sp, tipo)
        ret = parser.sp
        parser.sp += tipo.tamanho()
    writevm(f"// ^ variável {nome}")
    return ret


def escopo_dealloc(nome):
    assert nome in parser.decls[-1], "Variável com ID não existente!"
    (_, tipo) = parser.decls[-1].pop(nome)
    if parser.global_flag:
        parser.sp_global -= tipo.tamanho()
    else:
        parser.sp -= tipo.tamanho()


def p_decl_atri_variavel_id(p):
    '''DeclAtriVariavel : ID'''

    for escopo in reversed(parser.decls):
        if p[1] in escopo:
            print_err(f"Variavel '{p[1]}' já declarada!")
            return

    p[0] = (p[1], None)


def p_decl_atri_variavel(p):
    '''DeclAtriVariavel : ID "=" Expressao'''

    p[0] = (p[1], p[3])
    for escopo in reversed(parser.decls):
        if p[1] in escopo:
            print_err(f"Variavel '{p[1]}' já declarada!")
            return


def p_funcao(p):
    '''ChamarFuncao : ID "(" ")"'''
    writevm(f'pusha {p[1]}')
    writevm('call')

    if p[1] not in parser.fun_decls:
        print_err(f"Função '{p[1]}' não declarada!")
        p[0] = None
        return

    p[0] = parser.fun_decls[p[1]]


def p_indexacao_escrita_unidimensional(p):
    '''IndexacaoEscrita : IdIndexacao "[" Expressao "]"'''

    if p[1] == None:
        return

    if p[3].tipo != Tipo.INT:
        print_err("Indexação com expressão inválida!")
        return

    writevm("add")
    p[0] = TipoAST(p[1].tipo)


def p_indexacao_leitura_unidimensional(p):
    '''IndexacaoLeitura : IdIndexacao "[" Expressao "]"'''

    if p[1] == None:
        return

    if p[3].tipo != Tipo.INT:
        print_err("Indexação com expressão inválida!")
        return

    writevm("add")
    writevm("loadn")
    p[0] = TipoAST(p[1].tipo)


def p_indexacao_unidimensional_id(p):
    '''IdIndexacao : ID'''

    for escopo in reversed(parser.decls):
        if p[1] in escopo:
            ptr, tipo = escopo[p[1]]
            if len(tipo.dimensoes) == 1 and not tipo.singular():
                if p[1] in parser.decls_global:
                    writevm("pushgp")
                else:
                    writevm("pushfp")
                writevm(f"pushi {ptr}")
                p[0] = tipo
            else:
                print_err("Indexação em tipo inválido!")
            break
    else:
        print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")


# def p_indexacao_multidimensional(p):
#     '''Indexacao : ID Indices'''

#     indices = p[2]
#     for escopo in reversed(parser.decls):
#         if p[1] in escopo:
#             dimensoes = escopo[p[1]][1].dimensoes

#             if len(dimensoes) != len(indices):
#                 print_err(f"Acesso em array '{p[1]}' inválido!")
#                 break

#             indice_linear = 0
#             multiplicador = 1
#             for indice, dimensao in zip(reversed(indices),
#                                         reversed(dimensoes)):
#                 if indice < -dimensao or indice >= dimensao:
#                     print_err(f"Acesso em array '{p[1]}' fora dos limites!")
#                     break

#                 if indice < 0: indice = indice + dimensao

#                 indice_linear += indice * multiplicador
#                 multiplicador *= dimensao

#             ptr = escopo[p[1]][0] + indice_linear
#             if p[1] in parser.decls_global:
#                 writevm(f"pushg {ptr}")
#             else:
#                 writevm(f"pushl {ptr}")
#             writevm(f"// ^ {p[1]}")

#             p[0] = TipoAST(escopo[p[1]][1].tipo)
#             return
#     else:
#         print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")

#     return


def p_indices(p):
    '''Indices : "[" INT "]"'''
    p[0] = [int(p[2])]


def p_indices_rec(p):
    '''Indices : Indices "[" INT "]"'''
    p[0] = p[1] + [int(p[3])]


def p_funcao_escreve(p):
    '''ChamarFuncao : _ESCREVE "(" Expressao ")"'''
    writevm("writes")
    writevm("writeln")


def p_funcao_escrevei(p):
    '''ChamarFuncao : _ESCREVEI "(" Expressao ")"'''
    writevm("writei")
    writevm("writeln")


def p_funcao_escrever(p):
    '''ChamarFuncao : _ESCREVER "(" Expressao ")"'''
    writevm("writer")
    writevm("writeln")


def p_funcao_ler(p):
    '''ChamarFuncao : _LER "(" ")"'''
    writevm("read")
    p[0] = TipoAST(Tipo.CARS)


def p_funcao_leri(p):
    '''ChamarFuncao : _LERI "(" ")"'''
    writevm('read')
    writevm('atoi')
    p[0] = TipoAST(Tipo.INT)


def p_funcao_lerr(p):
    '''ChamarFuncao : _LERR  "(" ")"'''
    writevm('read')
    writevm('ator')
    p[0] = TipoAST(Tipo.REAL)


def p_funcao_len(p):
    '''ChamarFuncao : _LEN "(" ID ")"'''

    for escopo in reversed(parser.decls):
        if p[3] in escopo:
            ptr, tipo = escopo[p[3]]
            writevm(f"pushi {tipo.dimensoes[-1]}")
            break
    else:
        print_err(f"Variável '{p[3]}' não declarada em nenhum escopo!")

    p[0] = TipoAST(Tipo.INT)


def p_expressao_id(p):
    '''Expressao : ID'''

    for escopo in reversed(parser.decls):
        if p[1] in escopo:
            ptr, p[0] = escopo[p[1]]

            if p[1] in parser.decls_global:
                writevm(f"pushg {ptr}")
            else:
                writevm(f"pushl {ptr}")
            writevm(f"// ^ {p[1]}")

            return

    print_err(f"Variável '{p[1]}' não declarada em nenhum escopo!")
    return


def p_expressao_const(p):
    '''Expressao : TipoConstante'''
    p[0] = p[1]


def p_expressao_funcao(p):
    '''Expressao : ChamarFuncao'''
    p[0] = p[1]


def p_expressao_indexacao(p):
    '''Expressao : IndexacaoLeitura'''
    p[0] = p[1]


def op_binaria_num(p, op):
    tipo = compativel(p[1], p[3])
    if tipo:
        if tipo.int() and tipo.singular():
            writevm(op)
        elif tipo.real() and tipo.singular():
            writevm(f'f{op}')
        else:
            print_err(f'Operação "{p[2]}" não é possível para "{tipo}"')
    return tipo


def p_expressao_bin_soma(p):
    '''Expressao : Expressao SOMA Expressao'''
    tipo = compativel(p[1], p[3])
    if tipo:
        if tipo.int() and tipo.singular():
            writevm('add')
        elif tipo.real() and tipo.singular():
            writevm('fadd')
        elif tipo.cars() and tipo.singular():
            writevm('concat')
        else:
            print_err(f'Operação "{p[2]}" não é possível para "{tipo}"')
    p[0] = tipo


def p_expressao_bin_subt(p):
    '''Expressao : Expressao SUBT Expressao'''
    p[0] = op_binaria_num(p, 'sub')


def p_expressao_bin_mult(p):
    '''Expressao : Expressao MULT Expressao'''
    p[0] = op_binaria_num(p, 'mul')


def p_expressao_bin_div(p):
    '''Expressao : Expressao DIV Expressao'''
    p[0] = op_binaria_num(p, 'div')


def p_expressao_bin_mod(p):
    '''Expressao : Expressao MOD Expressao'''
    tipo = compativel(p[1], p[3])
    if tipo:
        if tipo.int() and tipo.singular():
            writevm('mod')
        else:
            print_err(f'Operação "{p[2]}" não é possível para "{tipo}"')
    p[0] = tipo


def p_expressao_bin_menorq(p):
    '''Expressao : Expressao MENORQ Expressao'''
    p[0] = op_binaria_num(p, 'inf')


def p_expressao_bin_maiorq(p):
    '''Expressao : Expressao MAIORQ Expressao'''
    p[0] = op_binaria_num(p, 'sup')


def p_expressao_bin_menorig(p):
    '''Expressao : Expressao MENORIG Expressao'''
    p[0] = op_binaria_num(p, 'infeq')


def p_expressao_bin_maiorig(p):
    '''Expressao : Expressao MAIORIG Expressao'''
    p[0] = op_binaria_num(p, 'supeq')


def p_expressao_bin_ig(p):
    '''Expressao : Expressao IG Expressao'''
    tipo = compativel(p[1], p[3])
    if tipo:
        if tipo.singular():
            writevm('equal')
        else:
            print_err(f'Operação "{p[2]}" não é possível para "{tipo}"')
    p[0] = tipo


def p_expressao_bin_dif(p):
    '''Expressao : Expressao DIF Expressao'''
    tipo = compativel(p[1], p[3])
    if tipo:
        if tipo.singular():
            writevm('equal')
            writevm('not')
        else:
            print_err(f'Operação "{p[2]}" não é possível para "{tipo}"')
    p[0] = tipo


def p_expressao_bin_e(p):
    '''Expressao : Expressao E Expressao'''
    tipo = compativel(p[1], p[3])
    if tipo:
        if tipo.numerico() and tipo.singular():
            writevm('and')
        else:
            print_err(f'Operação "{p[2]}" não é possível para "{tipo}"')
    p[0] = tipo


def p_expressao_bin_ou(p):
    '''Expressao : Expressao OU Expressao'''
    tipo = compativel(p[1], p[3])
    if tipo:
        if tipo.numerico() and tipo[1].singular():
            writevm('or')
        else:
            print_err(f'Operação "{p[2]}" não é possível para "{tipo}"')
    p[0] = tipo


def p_expressao_un_subt(p):
    '''Expressao : SUBT Expressao %prec SUBTU'''
    tipo = p[2]
    if tipo.int() and tipo.singular():
        writevm('pushi -1')
        writevm('mul')
    elif tipo.real() and tipo.singular:
        writevm('pushf -1')
        writevm('fmul')
    else:
        print_err(f'Operação "{p[1]}" não é possível para "{tipo}"')

    p[0] = tipo


def p_expressao_un_neg(p):
    '''Expressao : NEG Expressao %prec NEG'''
    tipo = p[2]
    if tipo:
        if tipo.numerico() and tipo.singular():
            writevm('not')
        else:
            print_err(f'Operação "{p[1]}" não é possível para "{tipo}"')
    p[0] = tipo


def p_expressao_grupo(p):
    '''Expressao : "(" Expressao ")"'''
    p[0] = [2]


def p_tipo_constante_INT(p):
    '''TipoConstante : INT'''
    p[0] = TipoAST(Tipo.INT)
    writevm(f"pushi {p[1]}")


def p_tipo_REAL(p):
    '''TipoConstante : REAL'''
    p[0] = TipoAST(Tipo.REAL)
    writevm(f"pushf {p[1]}")


def p_tipo_CAR(p):
    '''TipoConstante : CAR'''
    p[0] = TipoAST(Tipo.INT)
    writevm(f"pushi {ord(p[1])}")


def p_tipo_CARS(p):
    '''TipoConstante : CARS'''
    p[0] = TipoAST(Tipo.CARS)
    writevm(f"pushs {p[1]}")


def p_tipo_constante_array(p):
    '''TipoConstante : "[" LTipoConstante "]"'''
    for i in range(len(p[2]) - 1):
        if p[2][i] != p[2][i + 1]:
            print_err(
                f'Elementos do array não são todos iguais: "{p[2][i]}" e "{p[2][i+1]}"'
            )
            return

    p[0] = p[2][0].subarray(len(p[2]))


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
    '''Ciclo : _PARA Intervalo Escopo'''
    ptr, flag = p[2]

    if flag:
        writevm(f'pushg {ptr}')
    else:
        writevm(f'pushl {ptr}')
    writevm('pushi 1')
    writevm('add')
    if flag:
        writevm(f'storeg {ptr}')
    else:
        writevm(f'storel {ptr}')

    labelf = parser.label_stack.pop()
    labeli = parser.label_stack.pop()
    writevm(f'jump {labeli}')
    writevm(f'{labelf}:')

    escopo_dealloc('0inicio')
    escopo_dealloc('0fim')
    writevm(f'pop 2')


def p_intervalo(p):
    '''Intervalo : IdPara _NO _INTERVALO "(" Expressao "," Expressao ")"'''
    inicio, fim = p[5], p[7]
    if not inicio.int() or not fim.int():
        print_err("Argumentos de intervalo devem ser do tipo 'INT'!")
        return

    ptr_inicio = escopo_alloc('0inicio', TipoAST(Tipo.INT))
    ptr_fim = escopo_alloc('0fim', TipoAST(Tipo.INT))
    ptr_i, ptr_i_global = p[1]

    writevm(f'pushl {ptr_inicio}')
    writevm(f"// ^ 0inicio")
    if ptr_i_global:
        writevm(f'storeg {ptr_i}')
    else:
        writevm(f'storel {ptr_i}')

    writevm(f'{parser.label}:')
    parser.label_stack.append(parser.label)
    parser.label += 1
    if ptr_i_global:
        writevm(f'pushg {ptr_i}')
    else:
        writevm(f'pushl {ptr_i}')
    writevm(f"// ^ i")
    writevm(f'pushl {ptr_fim}')
    writevm(f"// ^ 0fim")
    writevm(f'inf')
    writevm(f'jz {parser.label}')
    parser.label_stack.append(parser.label)
    parser.label += 1

    p[0] = (ptr_i, ptr_i_global)


def p_id_para(p):
    '''IdPara : ID'''
    for escopo in reversed(parser.decls):
        if p[1] in escopo:
            if not escopo[p[1]][1].int():
                print_err(
                    f"Variável {p[1]} já declarada com tipo diferente de 'INT'!"
                )
            ptr_i = escopo[p[1]][0]
            break
    else:
        tipo = TipoAST(Tipo.INT)
        inicializacao0(tipo)
        ptr_i = escopo_alloc(p[1], tipo)

    flag = p[1] in parser.decls_global
    p[0] = (ptr_i, flag)


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
    '''DeclFuncao : AssinaturaFuncao CorpoFuncao'''
    nome, esq = p[1]
    dir = p[2]
    if esq.tipo == Tipo.AUTO:
        esq = dir
    elif compativel(esq, dir) and compativel(esq, dir) != esq:
        print_err(f'Tipos incompatíveis "{esq}" e "{dir}"!')

    if not esq.singular():
        assert False, "Não implementado!"

    p[0] = esq
    if nome in parser.fun_decls:
        print_err(f"Função '{nome}' já declarada!")
        return

    parser.fun_decls[nome] = esq


def p_decl_corpo_funcao_simples(p):
    '''CorpoFuncao : "{" Retorno "}"'''
    p[0] = p[2]
    writevm('return')


def p_decl_corpo_funcao(p):
    '''CorpoFuncao : "{" inicio_escopo Programa Retorno fim_escopo "}"'''
    p[0] = p[4]
    writevm('return')


def p_assinatura_funcao(p):
    '''AssinaturaFuncao : _DEF Tipo ID "(" ")"'''
    writevm(f'{p[3]}:')
    inicializacao0(p[2])
    writevm(f'start')
    p[0] = (p[3], p[2])


def p_assinatura_funcao_inicio(p):
    '''AssinaturaFuncaoInicio : _DEF _INT _INICIO "(" ")"'''
    writevm(f'{p[3]}:')
    inicializacao0(TipoAST(Tipo.INT))
    writevm(f'start')
    p[0] = (p[3], p[2])


def p_decl_retorna(p):
    '''Retorno : _RETORNA Expressao'''
    writevm(f"storel -1")
    p[0] = p[2]


def find_column(token):
    # Calculate the column position of the token in the line
    last_newline = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
    if last_newline < 0:
        last_newline = -1
    return token.lexpos - last_newline


def p_error(p):
    if not p:
        print("\033[91mErro de sintaxe: Fim inesperado da entrada\033[0m")
        return

    esperado = []
    if hasattr(parser, 'state'):
        estado = parser.state
        if estado < len(parser.action):
            for token, acao in parser.action[estado].items():
                if token != '$end':
                    esperado.append(token)

    msg_esperado = f"Será que quis escrever: {', '.join(repr(t) for t in esperado)}" if esperado else "Token inesperado"

    linha = p.lineno
    coluna = find_column(p)
    print(f"\033[91mErro de sintaxe na linha {linha}, coluna {coluna}:\033[0m")

    linha = p.lexer.lexdata.splitlines()[linha - 1]
    print(linha)

    sublinhado = " " * (coluna - 1) + "\033[91m^\033[0m"
    print(sublinhado)

    print(msg_esperado)
    parser.exito = False


def init_parser():
    parser.exito = True
    parser.decls = [{}]
    parser.decls_global = parser.decls[0]
    parser.fun_decls = {}
    parser.sp = 0
    parser.sp_global = 0
    parser.global_flag = 1
    parser.escopo_stack = []
    parser.label = 0
    parser.label_stack = []


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
            parser.parse(f.read(), tracking=True)
            if not parser.exito: exit(1)
            print("\033[92mAnálise sintática concluída com sucesso!\033[0m")

            if os.path.exists(args.output):
                print(
                    f"Ficheiro '{args.output}' já existente. Sobrescrevendo!")

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
        parser.parse(source, tracking=True)
        if not parser.exito: exit(1)
        print("\033[92mAnálise sintática concluída com sucesso!\033[0m")
        print("Declarações Variáveis:")
        print(parser.decls)
        print("Declarações Funções:")
        print(parser.fun_decls)
