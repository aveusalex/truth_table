# Primeiro passo é reconhecer a proposição lógica


def coloca_parenteses(proposicao):
    for i in ['[', ']', '{', '}']:
        if i in ['[', '{']:
            proposicao = proposicao.replace(i, "(")
        elif i in [']', '}']:
            proposicao = proposicao.replace(i, ')')
    return proposicao


def operadores(prop):
    dicionario_operadores = {'^':" and ", "~":"not ", "v":" or "}
    for operador in ['^', '~', 'v']:
        for letra in prop:
            if letra == operador:
                prop = prop.replace(letra, dicionario_operadores[operador])
    return prop


def valores_bool(letras):
    bools = {}
    tamanho_letras = len(letras)

    for ind in range(tamanho_letras):
        i = ind+1
        k = 2**(tamanho_letras-i)
        bools[letras[ind]] = k

    for letra in letras:
        aux = 0
        frequencia = bools[letra]
        lista_bools = []
        while aux < 2**(letras.index(letra)):
            for valor_bool in range(frequencia):
                lista_bools.append('1')
            for valor_bool in range(frequencia):
                lista_bools.append('0')
            aux += 1
        bools[letra] = lista_bools

    return bools


def aplicador_logico(prop, lista_bools, letras, linha):
    dicionario_bools = lista_bools

    for letra in letras:
        bool_respectivo_letra = dicionario_bools[letra]  # Assume a lista de bools respectiva à letra no dicionário.
        bool_respectivo_letra = bool_respectivo_letra[linha]
        prop = prop.replace(letra, bool_respectivo_letra)  # Troca a letra correspondente à proposição por um operador lógico 0 ou 1
        expressao_logica = prop

    return expressao_logica


def inverse(value):
    if value == 0:
        return 1
    else:
        return 0


def expressao_to_bool(expressao):
    bools = []

    if 'and' in expressao:
        for i in expressao:
            if i == '0':
                bools.append(0)
            elif i == '1':
                bools.append(1)
        try:
            expressao = expressao.split()
            contar = expressao.count('not')
            if contar < 2:
                indice_not = expressao.index('not')
                indice_and = expressao.index('and')
                if indice_and > indice_not:
                    bools[0] = inverse(bools[0])
                else:
                    bools[1] = inverse(bools[1])
            else:
                bools[0], bools[1] = inverse(bools[0]), inverse(bools[1])
        except:
            pass

        logicas = bools[0] and bools[1]

    elif 'or' in expressao:
        for i in expressao:
            if i == '0':
                bools.append(0)
            elif i == '1':
                bools.append(1)
        try:
            expressao = expressao.split()
            contar = expressao.count('not')
            if contar < 2:
                indice_not = expressao.index('not')
                indice_or = expressao.index('or')
                if indice_or > indice_not:
                    bools[0] = inverse(bools[0])
                else:
                    bools[1] = inverse(bools[1])
            else:
                bools[0], bools[1] = inverse(bools[0]), inverse(bools[1])
        except:
            pass

        logicas = bools[0] or bools[1]

    return logicas


# Montagem da tabela


def numero_de_linhas(letras):
    linhas = 2**(len(letras))
    return linhas


def montagem(letras, ):
    lista_letras = letras



def le_proposicao():
    letras = input('Digite as letras correspondentes às proposições, separadas por espaço (NÃO USE V): ').split()
    prop = input("Digite uma proposição qualquer, respeitando os símbolos"
                 " ( E:^ , OU:v , NÃO:~ , CONDICIONAL:-> , BICONDICIONAL:<-> ): ")
    print()

    qtd_de_linhas = numero_de_linhas(letras)
    prop = coloca_parenteses(prop)

    for linha in range(qtd_de_linhas):
        proposicao = aplicador_logico(prop, valores_bool(letras), letras, linha)
        proposicao_formatada = operadores(proposicao)
        print(proposicao_formatada)
        operacao = expressao_to_bool(proposicao_formatada)
        print(operacao)
        print()



le_proposicao()
