#import "@preview/tgm-hit-protocol:0.1.0": *

#set text(lang: "pt")
#show: template(
  title: [Trabalho Prático nº2\ (Gramáticas, Compiladores)],
  course: [Ciências da Computação 2024/25],
  subtitle: [Sentão Linguagem de Programação],
  subject: [Processamento de Linguagens e Compiladores],
  author: "Davide Santos | A102938\nEdgar Araújo | A102946\nGabriel Paiva | A102507",
  teacher: [Michael Borko],
  version: [1.0],
  begin: parse-date("2024-10-07"),
  finish: parse-date("2025-01-04"),
  date: parse-date("2025-01-05"),
  bibliography: bibliography("bibliography.bib"),
)

#import "assets/mod.typ" as assets
#include "glossaries.typ"

= Introdução
== Objetivos do Projeto
Este trabalho prático tem como principais objetivos:
- Aumentar a experiência em engenharia de linguagens e programação generativa
- Desenvolver processadores de linguagens usando tradução dirigida pela sintaxe
- Implementar um compilador gerando código para uma máquina virtual de stack
- Utilizar geradores de compiladores baseados em gramáticas (PLY/Python)
- Aprimorar a capacidade de escrever gramáticas independentes de contexto
- Desenvolver documentação técnica adequada

== Descrição da Linguagem Ent
A linguagem Ent é uma linguagem de programação imperativa desenvolvida para fins educacionais, com foco em simplicidade e clareza. Suas principais características incluem:

- Tipagem estática com tipos básicos (int, real, char, string)
- Tipos especiais auto e dynamic para flexibilidade
- Suporte a arrays unidimensionais
- Estruturas de controle de fluxo convencionais
- Funções com retorno de valor (sem parâmetros)
- Sintaxe em português para maior acessibilidade

== Ferramentas Utilizadas
- Python como linguagem base
- PLY (Python Lex-Yacc) para análise léxica e sintática
- Máquina virtual de stack para execução do código gerado

= Análise Léxica
== Tokens da Linguagem
O analisador léxico foi implementado usando PLY e reconhece os seguintes tipos de tokens:

#figure(
  ```python
  tokens = [
    'ID',        # Identificadores
    'INT',       # Números inteiros
    'CAR',       # Caracteres
    'CARS',      # Strings
    'REAL',      # Números reais
    'SOMA',      # +
    'SUBT',      # -
    'MULT',      # *
    'DIV',       # /
    'MOD',       # %
    'MAIORIG',   # >=
    'MENORIG',   # <=
    'MAIORQ',    # >
    'MENORQ',    # <
    'IG',        # ==
    'NEG',       # !
    'DIF',       # !=
    'OU',        # ||
    'E',         # &&
  ]
  ```,
  caption: "Definição dos Tokens Principais"
)

== Expressões Regulares
As expressões regulares definem os padrões para reconhecimento dos tokens. Alguns exemplos importantes:

#figure(
  ```python
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
  ```,
  caption: "Principais Expressões Regulares"
)

== Palavras Reservadas
A linguagem inclui palavras reservadas em português para maior clareza:

#figure(
  ```python
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
  }
  ```,
  caption: "Palavras Reservadas da Linguagem"
)

= Análise Sintática
== Gramática da Linguagem
A gramática da linguagem foi projetada para ser clara e expressiva. Algumas das principais produções incluem:

#figure(
  ```
  Programa      : Acao
                | Acao Programa

  Acao          : DeclVariavel
                | DeclFuncao
                | Atribuicao
                | Condicao
                | Ciclo
  ```,
  caption: "Estrutura Básica do Programa"
)

== Tratamento de Precedências
A linguagem implementa precedência de operadores através da seguinte hierarquia:

#figure(
  ```python
  precedence = (
      ('left', 'E', 'OU'),         # Operadores lógicos
      ('left', 'IG', 'DIF'),       # Comparadores
      ('left', 'MENORQ', 'MAIORQ', 'MENORIG', 'MAIORIG'),
      ('left', 'SOMA', 'SUBT'),    # Soma e subtração
      ('left', 'MULT', 'DIV', 'MOD'), # Multiplicação, divisão e módulo
      ('right', 'SUBTU', 'NEG'),   # Operadores unários
  )
  ```,
  caption: "Definição de Precedências"
)

== Estruturas de Controle
A linguagem suporta várias estruturas de controle de fluxo:

=== Condicionais
#figure(
  ```
  // Estrutura if-then-else
  se (condicao) entao {
    // código
  } senao {
    // código alternativo
  }

  // Estrutura if-then
  se (condicao) entao {
    // código
  }
  ```,
  caption: "Estruturas Condicionais"
)

=== Ciclos
A linguagem oferece três tipos diferentes de estruturas de repetição:

#figure(
  ```
  // Ciclo while
  enquanto (condicao) faca {
    // código
  }

  // Ciclo repeat-until
  repita {
    // código
  } ate que (condicao)

  // Ciclo for com intervalo
  para i no intervalo(1, 10) {
    // código
  }
  ```,
  caption: "Estruturas de Repetição"
)

== Gestão de Escopos
O compilador implementa um sistema de escopos aninhados que permite o controle de visibilidade de variáveis. Cada escopo é representado por um dicionário que mapeia identificadores para posições de memória.

=== Implementação dos Escopos
#figure(
  ```python
  def p_escopo(p):
      '''Escopo : "{" entrar Programa "}"'''
      removed_scope = parser.decls.pop()
      parser.sp -= len(removed_scope)
      print(f'pop {len(removed_scope)}')
      p[0] = p[2]

  def p_entrar(p):
      '''entrar :'''
      parser.decls.append({})
  ```,
  caption: "Implementação Base dos Escopos"
)

=== Verificação de Variáveis
O compilador verifica a existência e validade das variáveis em todos os escopos acessíveis:

#figure(
  ```python
  def p_atribuicao(p):
      '''Atribuicao : ID "=" Expressao'''
      p[0] = (p[1], p[3])

      for scope in reversed(parser.decls):
          if p[1] in scope:
              print(f"storeg {scope[p[1]]}")
              return

      print(f"Variável {p[1]} não declarada em nenhum escopo!")
      parser.exito = False
      return
  ```,
  caption: "Verificação de Variáveis nos Escopos"
)

=== Declaração de Variáveis
O sistema previne redeclarações de variáveis no mesmo escopo:

#figure(
  ```python
  def p_decl_atri_variavel_id(p):
      '''DeclAtriVariavel : ID'''
      p[0] = ('var', p[1], ('const', 0))

      for scope in reversed(parser.decls):
          if p[1] in scope:
              print("Variavel já declarada!")
              parser.exito = False
              return

      print("pushi 0")
      parser.decls[-1][p[1]] = parser.sp
      parser.sp += 1
  ```,
  caption: "Controle de Declarações de Variáveis"
)

=== Estrutura de Dados
O compilador mantém uma pilha de escopos (`parser.decls`) e um contador de posições de memória (`parser.sp`):
- A pilha de escopos permite aninhar blocos de código
- O contador de posições garante alocação única de memória
- A busca de variáveis é feita do escopo mais interno para o mais externo

= Exemplos de Programas
== Exemplo de Ciclo While
#figure(
  ```
  // Contagem regressiva
  int x;
  x = 10;
  enquanto (x > 0) faca {
    x = x - 1;
  }
  ```,
  caption: "Exemplo de Ciclo While"
)

== Exemplo de Funções
#figure(
  ```
  int dobro() {
    int x;
    x = 5;
    retorna x * 2;
  }
  ```,
  caption: "Exemplo de Função"
)

== Exemplo de Operações Lógicas
#figure(
  ```
  int a, b;
  a = 5;
  b = 10;
  
  se ((a < b) && (b > 0)) entao {
    // código
  }
  ```,
  caption: "Exemplo de Operações Lógicas"
)

= Geração de Código
== Instruções da Máquina Virtual
O compilador gera código para uma máquina virtual baseada em stack. As principais instruções incluem:

#figure(
  ```
  // Instruções geradas para atribuição
  pushi 0    // Empilha valor inicial
  storeg N   // Armazena na posição N

  // Instruções para operações
  pushg N    // Carrega variável da posição N
  add        // Soma dois valores do topo
  mul        // Multiplica dois valores do topo
  div        // Divide dois valores do topo
  mod        // Resto da divisão
  ```,
  caption: "Exemplos de Instruções da VM"
)

== Gestão de Memória
O compilador mantém controle das variáveis através de um contador de posições de memória:

#figure(
  ```python
  parser.decls[-1][p[1]] = parser.sp  # Associa variável à posição
  parser.sp += 1                      # Incrementa contador
  ```,
  caption: "Gestão de Posições de Memória"
)

= Testes e Validação
== Casos de Teste
O compilador foi testado com diversos programas de exemplo que cobrem todas as funcionalidades implementadas. Os testes foram organizados em diferentes categorias:

=== Testes de Estruturas Básicas
- Declaração e atribuição de variáveis
- Operações aritméticas e lógicas
- Entrada e saída básica

=== Testes de Estruturas de Controle
#figure(
  ```
  // Teste de estruturas condicionais aninhadas
  int x;
  x = 10;
  se (x > 5) entao {
    se (x < 15) entao {
      x = x + 1;
    }
  }

  // Teste de ciclos
  int i;
  i = 0;
  enquanto (i < 5) faca {
    i = i + 1;
  }
  ```,
  caption: "Exemplos de Testes de Estruturas de Controle"
)

=== Testes de Escopos
#figure(
  ```
  int x;
  x = 5;
  {
    int x;  // Variável diferente em novo escopo
    x = 10;
  }
  // x aqui ainda é 5
  ```,
  caption: "Teste de Escopo Aninhado"
)

== Resultados Obtidos
=== Análise de Desempenho
O compilador demonstrou bom desempenho em:
- Detecção de erros de sintaxe
- Gestão de escopos aninhados
- Geração de código para a máquina virtual

=== Pontos de Melhoria Identificados
- Otimização do código gerado
- Melhor tratamento de erros
- Suporte a mais tipos de dados

= Conclusão

O desenvolvimento deste compilador para a linguagem Ent representou um desafio significativo que nos permitiu aplicar e aprofundar conhecimentos em várias áreas da computação, especialmente em processamento de linguagens e compiladores.

== Síntese do Trabalho
O projeto resultou na implementação de um compilador funcional que inclui:
- Um analisador léxico robusto que reconhece todos os tokens da linguagem
- Um analisador sintático capaz de processar a gramática completa da linguagem
- Um sistema de gestão de escopos que permite variáveis locais e globais
- Um gerador de código para uma máquina virtual de stack
- Uma suite de testes abrangente com exemplos práticos

== Aprendizagens
O desenvolvimento deste projeto proporcionou várias aprendizagens importantes:
- Compreensão profunda do processo de compilação e suas fases
- Experiência prática com ferramentas de geração de compiladores (PLY)
- Desenvolvimento de habilidades de debug e teste de compiladores
- Melhor entendimento de gramáticas e análise sintática
- Experiência com geração de código intermediário

== Desafios Superados
Durante o desenvolvimento, enfrentamos e superamos vários desafios:
- Implementação correta da precedência de operadores
- Gestão de escopos aninhados
- Tratamento adequado de erros léxicos e sintáticos
- Geração de código eficiente para a máquina virtual

== Contribuições Individuais
O trabalho foi desenvolvido de forma colaborativa, com cada membro contribuindo em diferentes aspectos:
- Davide Santos: Análise léxica e documentação
- Edgar Araújo: Análise sintática e geração de código
- Gabriel Paiva: Sistema de tipos e testes

== Perspectivas Futuras
Além das melhorias já mencionadas na seção de trabalho futuro, identificamos outras possibilidades interessantes:
- Implementação de um sistema de módulos
- Adição de recursos de programação orientada a objetos
- Desenvolvimento de uma IDE simples para a linguagem
- Criação de uma biblioteca padrão mais abrangente

Esta experiência nos proporcionou uma compreensão mais profunda dos desafios e complexidades envolvidos no desenvolvimento de compiladores, bem como das melhores práticas para superá-los. O projeto não apenas cumpriu seus objetivos educacionais, mas também nos preparou para desafios futuros no campo do desenvolvimento de linguagens de programação.

= Anexos
== Manual da Linguagem
=== Sintaxe Básica
#figure(
  ```
  // Declarações
  int x;
  real y;
  car c;
  cars s;

  // Atribuições
  x = 10;
  y = 3.14;
  c = 'a';
  s = "texto";

  // Estruturas de controle
  se (condição) entao {
    // código
  }

  enquanto (condição) faca {
    // código
  }
  ```,
  caption: "Exemplos de Sintaxe Básica"
)

== Exemplos de Código
=== Exemplo 1: Calculadora Simples
#figure(
  ```
  int a, b, resultado;
  
  // Leitura de valores
  escreve("Digite o primeiro número: ");
  a = leri();
  
  escreve("Digite o segundo número: ");
  b = leri();
  
  // Operações
  resultado = a + b;
  escrevei(resultado);
  ```,
  caption: "Calculadora Simples"
)

=== Exemplo 2: Verificação de Números
#figure(
  ```
  int num;
  
  escreve("Digite um número: ");
  num = leri();
  
  se (num > 0) entao {
    escreve("Positivo");
  } senao {
    se (num < 0) entao {
      escreve("Negativo");
    } senao {
      escreve("Zero");
    }
  }
  ```,
  caption: "Verificação de Números"
)

== Código Fonte do Compilador
O código fonte completo do compilador está disponível e inclui:
- Analisador léxico (lexer.py)
- Analisador sintático (parser.py)
- Exemplos de programas (pasta examples/)
- Documentação técnica

= Bibliografia
#bibliography("bibliography.bib")

