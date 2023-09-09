#############################################################################
# Alunos:                                                                   #
# ALEX SANTOS TAVARES                                                       #
# PEDRO LUIZ QUANZ DE SANT'ANA BARROS                                       #
# VITOR HUGO DUARTE DA SILVA                                                #
#############################################################################

tokens = list()
cont = 1
# Ler os tokens referentes a gramatica do arquivo de saida do lex (saida.txt)
try:
    with open('saida.txt') as f:
        for line in f:
            #print(line)

            #valores
            if('Identificador' in line):
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
print(tokens)



# dá o match no token, filtra alguns casos de erros
def match(expected_token):
    global tokens
    global cont
    if tokens and tokens[0] == expected_token:
        cont = cont + 1 
        tokens = tokens[1:]
    else:
        print(f"Erro de sintaxe! esperava '{expected_token }' posicao: {cont} e teve {lookahead()}")
        print(tokens)
        exit()

# Especificador de Tipo
def type_specifier():
    if lookahead() in ['int', 'boolean']:
        match(lookahead())
    else:
        print(f"Erro de sintaxe: esperava 'int' ou 'boolean', encontrou '{lookahead()}'")
        exit()


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

            
# EXPS -> EXP { , EXP }
def exps():
    exp()
    if lookahead(','):
        while lookahead() == ',':
            match(',')
            exp()
    

def is_multiplicacao():
    is_atribuicao()
    while lookahead() in ['*']:
        match('*')
        is_atribuicao()

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
    elif lookahead() in ['true', 'false', 'num', 'null']:
        match(lookahead())
    else:
        is_instancia_de_classe()
        if lookahead() == 'length':
            match('length')
        elif lookahead() == '[':
                match('[')
                exp()
                match(']')

# EXP -> EXP && isSubtracao
#     | isSubtracao
def exp():
    is_subtracao()
    if lookahead() == '&&':
        match('&&')
        exp()

# isSubtracao -> isSubtracao < isAdicao
#            | isSubtracao == isAdicao
#            | isSubtracao != isAdicao
#            | isAdicao
def is_subtracao():
    is_adicao()
    while lookahead() in ['<', '==', '!=']:
        match(lookahead())
        is_adicao()

# isAdicao -> isAdicao + isMultiplicacao
#         | isAdicao - isMultiplicacao
#         | isMultiplicacao
def is_adicao():
    is_multiplicacao()
    while lookahead() in ['+', '-']:
        match(lookahead())
        is_multiplicacao()

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
            match(';')
        elif lookahead() == '[':
            match('[')
            exp()
            match(']')
            match('=')
            exp()
            match(';')
    else:
        print(f"Erro de sintaxe: comando inválido: '{lookahead()}' + {cont}")
        exit()

# VAR -> TIPO id ;
def var():
    tipo()
    match('id')
    match(';')

# isDeclaracaoMetodo -> public TIPO id '(' [ isParametro ] ')' '{' { VAR } { CMD } return EXP ';' '}'
def is_declaracao_metodo():
    match('public')
    tipo()
    match('id')
    match('(')
    match('[')
    is_parametro()
    match(']')
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

# isParametro -> TIPO id { , TIPO id }
def is_parametro():
    tipo()
    match('id')
    while lookahead() == ',':
        match(',')
        tipo()
        match('id')

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
    else:
        print(f"Erro de sintaxe: esperava 'int' ou 'boolean' ou 'id', encontrou '{lookahead()}'")
        exit()

# PROG -> isMainDeClasse { isClasse }
def prog():
    is_main_de_classe()
    match('{')
    is_classe()
    match('}')

# isMainDeClasse -> class id '{' public static void main ( String [ ] id ) '{' CMD '}' '}'
def is_main_de_classe():
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

# isClasse -> class id [ extends id ] '{' { VAR } { isDeclaracaoMetodo } '}'
def is_classe():
    if lookahead() == 'id':
        match('id')
        if lookahead() == 'extends':
            match('extends')
            match('id')
        else:
            match('{')
    while lookahead() in ['id']:
        var()
    while lookahead() in ['public']:
        is_declaracao_metodo()
    match('}')
    match('}')

# pega o token atual da analise sem consumilo
def lookahead():
    if tokens:
        return tokens[0]
    else:
        return None


prog()
# Caso o gramatica esteja correta é printado a confirmação, se não o codigo é interrompido antes
print('Tudo Certo!')