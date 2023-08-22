#############################################################################
# Alunos:                                                                   #
# ALEX SANTOS TAVARES                                                       #
# PEDRO LUIZ QUANZ DE SANT'ANA BARROS                                       #
# VITOR HUGO DUARTE DA SILVA                                                #
#############################################################################

tokens = list()
# Ler os tokens referentes a gramatica do arquivo de saida do lex (saida.txt)
try:
    with open('saida.txt') as f:
        for line in f:
            #print(line)

            #valores
            if('Identificador' in line):
                tokens.append('id')
            elif('numeral' in line):
                tokens.append('num')
            #operadores    
            elif('+' in line):
                tokens.append('+')
            elif('-' in line):
                tokens.append('-')
            elif('*' in line):
                tokens.append('*')
            elif('=' in line):
                tokens.append('=')
            elif('<' in line):
                tokens.append('<')
            elif('==' in line):
                tokens.append('==')
            elif('!=' in line):
                tokens.append('!=')
            elif('&&' in line):
                tokens.append('&&')
            elif('!' in line):
                tokens.append('!')
            #pontuacao
            elif('(' in line):
                tokens.append('(')
            elif(')' in line):
                tokens.append(')')
            elif("'['" in line):
                tokens.append('[')
            elif("']'" in line):
                tokens.append(']')
            elif('{' in line):
                tokens.append('{')
            elif('}' in line):
                tokens.append('}')
            elif(';' in line):
                tokens.append(';')
            elif('.' in line):
                tokens.append('.')
            elif("','" in line):
                tokens.append(',')
            #reservadas
            elif('boolean' in line):
                tokens.append('boolean')
            elif('class' in line):
                tokens.append('class')
            elif('extends' in line):
                tokens.append('extends')
            elif('public' in line):
                tokens.append('public')
            elif('static' in line):
                tokens.append('static')
            elif('void' in line):
                tokens.append('void')
            elif('main' in line):
                tokens.append('main')
            elif('String' in line):
                tokens.append('String')
            elif('return' in line):
                tokens.append('return')
            elif('int' in line):
                tokens.append('int')
            elif('if' in line):
                tokens.append('if')
            elif('else' in line):
                tokens.append('else')
            elif('while' in line):
                tokens.append('while')
            elif('System.out.println' in line):
                tokens.append('System.out.println')
            elif('length' in line):
                tokens.append('length')
            elif('true' in line):
                tokens.append('true')
            elif('false' in line):
                tokens.append('false')
            elif('this' in line):
                tokens.append('this')
            elif('new' in line):
                tokens.append('new')
            elif('null' in line):
                tokens.append('null')
except:
    print('Erro ao abrir o arquivo de tokens')
    exit()

# imprime os tokens em ordem
print(tokens)


# # dá o match no token, filtra alguns casos de erros
# def match(expected_token):
#     global tokens
#     if tokens and tokens[0] == expected_token:
#         tokens = tokens[1:]
#     else:
#         if expected_token == ')':
#             print("Erro de sintaxe: Abertura de parenteses indevida")
#             exit()
#         if expected_token == '(':
#             print("Erro de sintaxe: Abertura de parenteses indevida")
#             exit()
#         elif tokens[0] == 'num' or tokens[0] == 'id':
#             print(f"Erro de sintaxe: esperava '+'|'-'|'*'|'/', encontrou '{tokens[0]}'")
#             exit()
#         elif tokens[0] in ['*', '/', '+', '-']:
#             print(f"Erro de sintaxe: esperava 'id'|'num', encontrou '{tokens[0]}'")
#             exit()
#         else:
#             print("Erro inesperado")
#             exit()

# # caso um token errado seja encontrado apos todos os anteriores serem aprovados ele informa que existem tokens a mais
# def goal():
#     expr()
#     if tokens:
#         print("Erro de sintaxe: fechamento indevido de parenteses e(ou) tokens adicionais após a análise sintática")
#         exit()

# # expressão
# def expr():
#     term()
#     expr_prime()


# # adicao | subtracao
# def expr_prime():
#     if lookahead() in ['+', '-']:
#         parse_op()
#         term()
#         expr_prime()
    
# # termo
# def term():
#     factor()
#     term_prime()

# # mult | div
# def term_prime():
#     if lookahead() in ['*', '/']:
#         parse_op()
#         factor()
#         term_prime()

# # contem parenteses, numero e identificador. Já filtra caso exista um fechamento de parentes indevido ou a falta de um fator
# def factor():
#     if lookahead() == ')':
#         print("Erro de sintaxe: fechamente de parenteses indevido")
#         exit()
#     if lookahead() == '(':
#         match('(')
#         expr()
#         match(')')
#     elif lookahead() == 'num':
#         match('num')
#     elif lookahead() == 'id':
#         match('id')
#     else:
#         print("Erro de sintaxe: esperava um fator")
#         exit()

# # similar a anterior só que com os operadores aditivos e multiplicativos/divisivos. Caso não exista ele retorna que era esperado um operador
# def parse_op():
#     if lookahead() == '+':
#         match('+')
#     elif lookahead() == '-':
#         match('-')
#     elif lookahead() == '*':
#         match('*')
#     elif lookahead() == '/':
#         match('/')
#     else:
#         print("Erro de sintaxe: esperava um operador")
#         exit()

# # pega o token atual da analise sem consumilo
# def lookahead():
#     if tokens:
#         return tokens[0]
#     else:
#         return None

# goal()
# # Caso o gramatica esteja correta é printado a confirmação, se não o codigo é interrompido antes
# print('Tudo Certo!')