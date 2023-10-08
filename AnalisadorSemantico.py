
import ast
from time import sleep

dict_prioridade = {
    '*' : 10,
    '+' : 9,
    '-' : 9,
    '<' : 8,
    '==': 7,
    '!=': 7,
    '&&': 7,
    '!': 7,
    '=': 5
}


def resolver_operacao(operador,valor_e,valor_d):
    match operador:
        case '*':
            if(valor_e=='int' and valor_d =='int'):
                return 'int'
            else:
                raise Exception(f"Operador {operador} esperava int * int e recebeu {valor_e} * {valor_d}")
        case '+':
            if(valor_e=='int' and valor_d =='int'):
                return 'int'
            else:
                raise Exception(f"Operador {operador} esperava int + int e recebeu {valor_e} * {valor_d}")
        case '-':
            if(valor_e=='int' and valor_d =='int'):
                return 'int'
            else:
                raise Exception(f"Operador {operador} esperava int - int e recebeu {valor_e} * {valor_d}")
        case '<':
            if(valor_e=='int' and valor_d =='int'):
                return 'Boolean'
            else:
                raise Exception(f"Operador {operador} esperava int < int e recebeu {valor_e} * {valor_d}")
        case '==':
            if(valor_e=='Boolean' and valor_d =='Boolean'):
                return 'Boolean'
            else:
                raise Exception(f"Operador {operador} esperava Boolean == Boolean e recebeu {valor_e} * {valor_d}")
        case '!=':
            if(valor_e=='Boolean' and valor_d =='Boolean'):
                return 'Boolean'
            else:
                raise Exception(f"Operador {operador} esperava Boolean != Boolean e recebeu {valor_e} * {valor_d}")
        case '&&':
            if(valor_e=='Boolean' and valor_d =='Boolean'):
                return 'Boolean'
            else:
                raise Exception(f"Operador {operador} esperava Boolean && Boolean e recebeu {valor_e} * {valor_d}")
        case '!':
            if(valor_d =='Boolean'):
                return 'Boolean'
            else:
                raise Exception(f"Operador {operador} esperava Boolean  e recebeu {valor_d}")
        case '=':  
            if(valor_d == valor_e):
                return None
            else:
                raise Exception(f"Operador {operador} esperava {valor_e} = {valor_e} e recebeu {valor_e} = {valor_d}")
    
        

def get_operador_mais_importante(list_operadores:list[list]):
    index = 0
    valor_prioridade_geral = dict_prioridade[list_operadores[0][2]]
    for i in range(len(list_operadores)):
        operador = list_operadores[i]
        valor_prioridade = dict_prioridade[operador[2]]
        if(valor_prioridade>valor_prioridade_geral):
            valor_prioridade_geral = valor_prioridade
            index = i
    return index

def converte_valor(operador:list):
    operacao = operador[0] 
    if(operacao == 'Identificador'):
        var_type = list_de_var[operador[1]]
        return var_type
    if(operacao == 'numeral'):
        return 'int'
    if(operacao == 'Boolean'):
       return 'Boolean'
    return None

def desconverte_valor(valor):
    if(valor == 'int'):
        return ['numeral','0']
    if(valor == 'Boolean'):
        return ['Boolean','true']
    return None

def gera_lista_operadores(expressoes: list[list]):
    print('expressoes',expressoes)
    list_operadores = []
    for i in range(len(expressoes)):
        sintaxe = expressoes[i]
        if(sintaxe[0]=='Operador'):
            list_operadores.append([i,sintaxe[0],sintaxe[1]])
    return list_operadores

        


def pega_expressao_e_resolve (list_list: list[list], index_inicial,index_final):
    expressoes = list_list[index_inicial:index_final]
    print(expressoes)
    list_operadores = []
    list_valores = []
    for i in range(len(expressoes)):
        sintaxe = expressoes[i]
        if(sintaxe[0]=='Operador'):
            list_operadores.append([i,sintaxe[0],sintaxe[1]])
        else:
            list_valores.append([i,sintaxe[0],sintaxe[1]])
    while len(list_operadores)  > 0 :
        # print('lista expressoes',expressoes)
        # print('lista operadores',list_operadores)
        index_operador_mais_importante = get_operador_mais_importante(list_operadores)
        # print('list_operadores',list_operadores)
        # print('index_operador_mais_importante',index_operador_mais_importante)

        index_lista_de_expressao = int(list_operadores[index_operador_mais_importante][0])

        expressao_antes = expressoes[index_lista_de_expressao-1]
        expressao_depois = expressoes[index_lista_de_expressao+1]
        valor_antes = converte_valor(expressao_antes)
        valor_depois = converte_valor(expressao_depois)


        print('\n\n\n=========================')
        print(f"Operador -> {list_operadores[index_operador_mais_importante][2]}")
        print(f"expressao antes = {expressao_antes}")
        print(f"valor antes = {valor_antes}")
        print(f"expressao depois = {valor_antes}")
        print(f"valor depois = {valor_depois}")
        valor_final = resolver_operacao(list_operadores[index_operador_mais_importante][2],valor_antes,valor_depois)
        print(f"valor de retorno = {valor_final}")
        print('=========================')
        
        print(expressoes)

        del expressoes[index_lista_de_expressao+1]
        del expressoes[index_lista_de_expressao]
        if(valor_final):
            expressoes[index_lista_de_expressao-1] = desconverte_valor(valor_final)
        else:
            del expressoes[index_lista_de_expressao-1]

        list_operadores = gera_lista_operadores(expressoes)
        print(expressoes)
        print('=========================')
        # sleep(1)
    return expressoes

        
    # exit()

def resolve_operacao(limite_inferior,limite_superior):
    print(limite_inferior,limite_superior)

def carrega_sintaxe():
    f = open('saida.txt','r')

    list_sintaxe = []

    for element in f.readlines():
        list_sintaxe.append(ast.literal_eval(element.replace("\n","")))
    return list_sintaxe

def recorta_expressao (full_list:list[list],index):
    # print(full_list[index])
    atual = full_list[index]
    antes = index
    depois = index
    while (atual[0] == 'Operador' or atual[0] == 'Pontuacao' or atual[0] == 'Identificador' or atual[0] == 'numeral' or (atual[0] == 'Palavra reservada' and (atual[1] == 'this' or atual[1] == 'true' or atual[1] == 'false'))):
        if(antes == 0 ):
            break
        antes -= 1
        atual = full_list[antes]
        # print(full_list[antes])
    #     sleep(0.5)
    # print('antes foi ==========')
    atual = full_list[index]
    while (atual[0] == 'Operador' or atual[0] == 'Pontuacao' or atual[0] == 'Identificador' or atual[0] == 'numeral' or (atual[0] == 'Palavra reservada' and (atual[1] == 'this' or atual[1] == 'true' or atual[1] == 'false'))):
        depois += 1
        atual = full_list[depois]
    #     print(full_list[depois])
    #     sleep(0.5)
    # print('depois foi ==========')
    return [antes+1,depois-1]
    


def find_operacoes(full_list:list[list]):
    list_intervalos = []
    i = 0
    while i < (len(full_list)):
        sintaxe = full_list[i]
        if(sintaxe[0]=='Operador'):
            [index_antes, index_depois] = recorta_expressao(full_list,i)
            i = index_depois + 1
            list_intervalos.append([index_antes,index_depois])
        i+=1
    return list_intervalos



def carrega_dict_variaveis(full_list:list[list]):
    dict_var = {}
    for i in range(len(full_list)):
        semi_list = full_list[i]
        if(semi_list[0]=='Identificador'):
            # print('identificador',semi_list[1])
            if( full_list[i-2] and  full_list[i-2][1] == 'public'):
                dict_var[semi_list[1]] = 'func'
            else:
                palavra_reservada = full_list[i-1][1]
                if ('Palavra reservada' == full_list[i-1][0] and (palavra_reservada=='String' or palavra_reservada=='int' or palavra_reservada=='Boolean')):
                    dict_var[semi_list[1]] = full_list[i-1][1]
    return dict_var

list_de_sitaxes = carrega_sintaxe()
global list_de_var
list_de_var = carrega_dict_variaveis(list_de_sitaxes)
# print(list_de_var)
# exit()
list_operacoes = find_operacoes(list_de_sitaxes)
for list_index in list_operacoes:
    pega_expressao_e_resolve(list_de_sitaxes,list_index[0],list_index[1])
    print("Operação está correta")
    print("\n\n\n\n\n\n")


