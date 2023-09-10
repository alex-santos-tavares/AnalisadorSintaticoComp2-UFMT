#############################################################################
# Alunos:                                                                   #
# ALEX SANTOS TAVARES                                                       #
# PEDRO LUIZ QUANZ DE SANT'ANA BARROS                                       #
# VICTOR HUGO DUARTE DA SILVA                                                #
# FELIPE CECCONELLO FONTANA                                                 #
#############################################################################

import subprocess
subprocess.run(["a.exe"])

tokens = list()
cont = 1
# Ler os tokens referentes a gramatica do arquivo de saida do lex (saida.txt)
try:
    with open('saida.txt') as f:
        for line in f:
            # print(line)

            if("'ERRO LEXICO'" in line):
                print('Erro léxico encontrado')
                exit()  
            #valores
            elif('Identificador' in line):
                tokens.append('id')
            elif("'numeral'" in line):
                tokens.append('numInt')
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
            elif('System.out.println' in line):
                tokens.append('System.out.println')
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
print('Lista de tokens -------------------------------------------------------------------------------------\n', tokens, '\n------------------------------------------------------------------------------------------------------')

def match(expected_token: str, mandatory:bool = True ) -> None:
    """
        Função para dar match no token, filtra alguns casos de erros.

        Parametros:
            expected_token: String com o token a ser analisado

            mandatory: Booleano que verifica se o token é o obrigatório, por padrão sim. Caso não seja, sua ausência não resultará em erro.

    """
    global tokens
    global cont
    if len(tokens) > 0:
        if tokens and tokens[0] == expected_token:
            cont = cont + 1 
            tokens = tokens[1:]
        else:
            if(mandatory):
                print(f"Erro de sintaxe! esperava '{expected_token }' posicao: {cont} e teve {lookahead()}")
                print(tokens)
                exit()
    elif len(tokens) == 0:
        print('Todos tokens analisados!\nSem erros encontrados')
        exit()

# pega o token atual da analise sem consumilo
def lookahead():
    if tokens:
        return tokens[0]
    else:
        return None
    

# EXPS -> EXP { , EXP }
def exps():
    exp()
    while lookahead() == ',':
        match(',')
        exp()

# isInstanciaDeClasse -> id
#                    | this
#                    | new id '(' ')'
#                    | '(' EXP ')'
#                    | isInstanciaDeClasse '.' id
#                    | isInstanciaDeClasse '.' id '(' [ EXPS ']')
def is_instancia_de_classe():
    if lookahead() == 'new':
        match('new')
        if lookahead() == 'int':
            is_atribuicao()
        else:
            match('id')
            match('(')
            match(')')
    elif lookahead() == 'id':
        match('id')
        if lookahead() == '(':
            is_instancia_de_classe()
    elif lookahead() == 'this':
        match('this')
    elif lookahead() == '(':
        match('(')
        exp()
        match(')')
    if lookahead() == '.':
        match('.')
        if lookahead() == 'id':
            match('id')
            is_instancia_de_classe()

            
# isAtribuicao -> ! isAtribuicao
#             | - isAtribuicao
#             | true
#             | false
#             | num
#             | null
#             | new int '[' EXP ']'
#             | isInstanciaDeClasse . length
#             | isInstanciaDeClasse '[' EXP ']'
#             | isInstanciaDeClasse
def is_atribuicao():
    if lookahead() == 'new':
        match('new')
        if lookahead() == 'int':
            match('int')
            match('[')
            exp()
            match(']')
        elif lookahead() == 'id':
            is_instancia_de_classe()
    elif lookahead() == '!':
        match('!')
        is_atribuicao()
    elif lookahead() == '-':
        match('-')
        is_atribuicao()
    elif lookahead() in ['true', 'false', 'numInt', 'null']:
        match(lookahead())
    else:
        is_instancia_de_classe()
        if lookahead() == 'length':
            match('length')
        elif lookahead() == '[':
                match('[')
                exp()
                match(']')


# isMultiplicacao -> isMultiplicacao * isAtribuicao
#                | isAtribuicao
def is_multiplicacao():
    is_atribuicao()
    while lookahead() in ['*']:
        match('*')
        is_atribuicao()

# isAdicao -> isAdicao + isMultiplicacao
#         | isAdicao - isMultiplicacao
#         | isMultiplicacao
def is_adicao():
    is_multiplicacao()
    while lookahead() in ['+', '-']:
        match(lookahead())
        is_multiplicacao()

# isSubtracao -> isSubtracao < isAdicao
#            | isSubtracao == isAdicao
#            | isSubtracao != isAdicao
#            | isAdicao
def is_subtracao():
    is_adicao()
    while lookahead() in ['<', '==', '!=']:
        match(lookahead())
        is_adicao()


# EXP -> EXP && isSubtracao
#     | isSubtracao
def exp():
    is_subtracao()
    if lookahead() == '&&':
        match('&&')
        exp()

# CMD -> '{' { CMD } '}'
#     | if '(' EXP ')' CMD
#     | if '(' EXP ')' CMD else CMD
#     | while '(' EXP ')' CMD
#     | System.out.println '(' EXP ')' ';'
#     | id '=' EXP ';'
#     | id '[' EXP ']' '=' EXP ';'
def cmd():
    if lookahead() == '{':
        match('{')
        while lookahead() not in ['}']:
            cmd()
        match('}')
    elif lookahead() == 'if':
        match('if')
        match('(')
        exp()
        if lookahead() == 'numInt':
            match('numInt')
        if lookahead() == 'id':
            match('id')
        match(')')
        cmd()
        if lookahead() == 'else':
            match('else')
            cmd()
    elif lookahead() == 'while':
        match('while')
        match('(')
        exp()
        match(')')
        cmd()
    elif lookahead() == 'System.out.println':
        match('System.out.println')
        match('(')
        exp()
        match(')')
        match(';')
    elif lookahead() == 'id':
        match('id')
        if lookahead() == '=':
            match('=')
            exp()
            if lookahead() == 'numInt':
                match('numInt')
            match(';')
        elif lookahead() == '[':
            match('[')
            exp()
            match(']')
            match('=')
            exp()
            match(';')
    elif lookahead() in ['int', 'boolean']:
        var()
    else:
        print(f"Erro de sintaxe: comando inválido: '{lookahead()}' + {cont}")
        print(tokens)
        exit()

# VAR -> TIPO id ;
def var():
    tipo()
    match('id')
    match(';')

# TIPO -> int '[' ']' | boolean | int | id
def tipo():
    if lookahead() == 'int':
        match('int')
        if lookahead() == '[':
            match('[')
            match(']')
    elif lookahead() == 'boolean':
        match('boolean')
    elif lookahead() == 'id':
        match('id')

# isParametro -> TIPO id { , TIPO id }
def is_parametro():
    tipo()
    match('id')
    while lookahead() == ',':
        match(',')
        tipo()
        match('id')

# isDeclaracaoMetodo -> public TIPO id '(' [ isParametro ] ')' '{' { VAR } { CMD } return EXP ';' '}'
def is_declaracao_metodo():
    match('public',False)
    tipo()
    match('id')
    match('(')
    while lookahead() in ['int', 'boolean']:
        is_parametro()
    match(')')
    match('{')
    while lookahead() in ['id']:
        var()
    while lookahead() not in ['return']:
        cmd()
    match('return')
    exp()
    match(';')
    match('}')

# isClasse -> class id [ extends id ] '{' { VAR } { isDeclaracaoMetodo } '}'
def is_classe():
    match('public',False)
    if lookahead() == 'id':
        match('id')
        if lookahead() == 'extends':
            match('extends')
            match('id')
        else:
            match('{')
    while lookahead() in ['int', 'boolean']:
        var()
    while lookahead() in ['public']:
        is_declaracao_metodo()
    match('}')
    match('}')

# isMainDeClasse -> class id '{' public static void main ( String [ ] id ) '{' CMD '}' '}'
def is_main_de_classe():
    match('public',False)
    match('class')
    match('id')
    match('{')
    match('public')
    match('static')
    match('void')
    match('main')
    match('(')
    match('String')
    match('[')
    match(']')
    match('id')
    match(')')
    match('{')
    cmd()
    match('}')
    match('}')
    if lookahead() == 'class':
        match('class')
        is_classe()
    else:
        print('tudo certo')
        exit()


# PROG -> isMainDeClasse { isClasse }
def prog():
    is_main_de_classe()
    match('{')
    is_classe()
    match('}')

def teste():
    return 'entrou'

prog()
# Caso o gramatica esteja correta é printado a confirmação, se não o codigo é interrompido antes