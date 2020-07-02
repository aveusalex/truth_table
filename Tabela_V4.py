from prettytable import PrettyTable  # importar o módulo Pretty Table
from time import sleep


operadores_de_cada_sentenca = {}  # Definir variável global para ser retomado pela tabela
compostas_parciais = {}


def caca_sentencas(proposicao_bruta):
    snt = []
    for elemento in proposicao_bruta:
        if elemento not in ['^', 'v', '->', '<->', '~', 'xv', '(', ')', '[', ']', '{', '}']:
            if elemento not in snt:
                snt.append(elemento)

    return snt


def calculo_frequencia_op_log(quantidade_sentencas, coluna):
    '''
    Calcula quantas vezes o 1 e 0 se repetirão para cada sentença. Exemplo: para 8 linhas, o 'p'
    assumirá 4 vezes '1' e 4 vezes '0'.
    '''

    coluna = coluna + 1
    frequencia = 2 ** (quantidade_sentencas - coluna)
    return frequencia


def operadores_da_sentenca(coluna, quantidade_de_linhas, frequencia):
    '''
    Definirá os bools para a sentença específica. (ex: p receberá 1 1 0 0 ...)

    '''

    aux = 0
    operadores = []
    lista_operadores_da_sentenca = []
    while aux < 2 ** coluna:
        for i in range(frequencia):
            operadores.append(1)
        for i in range(frequencia):
            operadores.append(0)
        aux += 1

    return operadores


def definir_operadores_logicos(sentencas):
    '''
     Definirá os valores bools (0, 1) que cada sentença (p, q, r...) irá assumir para cada linha.
     Monta os resultados obtidos da função anterior em um dicionário e o retorna.

    '''

    global operadores_de_cada_sentenca
    operadores_de_cada_sentenca = {}
    quantidade_sentecas = len(sentencas)
    quantidade_de_linhas = 2 ** (quantidade_sentecas)
    coluna = 0
    for sentenca in sentencas:  # (p, q, r ...)
        frequencia_da_sentenca = calculo_frequencia_op_log(quantidade_sentecas, coluna)  # A sequencia de 1 ou 0 dependendo da sentenca
        operadores_de_cada_sentenca[sentenca] = operadores_da_sentenca(coluna, quantidade_de_linhas, frequencia_da_sentenca)
        coluna += 1

    return operadores_de_cada_sentenca


def montador_de_expressao(sentencas, numero_da_linha, proposicao_bruta):
    '''
    Substitui os símbolos (^, ~, ->, v...) pelos nomes das operações e as sentenças (p, q, r...) por 0 ou 1.
    Itera pela lista proposicao_bruta e procura pelos elementos da lista sentencas. A medida que os acha, substitui-os
    pelos valores bool.

    '''
    proposicao_reformada = proposicao_bruta[:]
    dicionario_bools = definir_operadores_logicos(sentencas)
    for sentenca in dicionario_bools:
        index_sentenca = []
        valor_em_bool = dicionario_bools[sentenca][numero_da_linha]
        index_auxiliar = 0
        for element in proposicao_bruta:
            if element == sentenca:
                index_sentenca.append(index_auxiliar)
            index_auxiliar += 1
        for i in index_sentenca:
            proposicao_reformada.remove(sentenca)
            proposicao_reformada.insert(i, valor_em_bool)

    for carac in proposicao_reformada:
        if carac == '^':
            index_carac = proposicao_reformada.index(carac)
            proposicao_reformada.remove(carac)
            proposicao_reformada.insert(index_carac, 'and')

        elif carac == 'v':
            index_carac = proposicao_reformada.index(carac)
            proposicao_reformada.remove(carac)
            proposicao_reformada.insert(index_carac, 'or')

        elif carac == '~':
            index_carac = proposicao_reformada.index(carac)
            proposicao_reformada.remove(carac)
            proposicao_reformada.insert(index_carac, 'not')

    return proposicao_reformada


def prioridade(expressao):
    '''
    Determina o index das operações com prioridade, acha a expressão que será realizada e retorna o index por meio de uma
    lista binária.

    '''
    lista_prioridade = []
    aux = 0
    for elemento in expressao:
        if elemento == '(':
            first_index = aux
        elif elemento == ')':
            second_index = aux
            lista_prioridade.append([first_index, second_index])
            return lista_prioridade
            break
        elif elemento == '[':
            third_index = aux
        elif elemento == ']':
            fourth_index = aux
            lista_prioridade.append([third_index, fourth_index])
            return lista_prioridade
            break
        elif elemento == '{':
            fifth_index = aux
        elif elemento == '}':
            sixth_index = aux
            lista_prioridade.append([fifth_index, sixth_index])
            return lista_prioridade
            break
        aux += 1

    return lista_prioridade


def resolve_expressao_aux(expre):
    '''
    Função auxiliar para a resolução das expressões. Ela que realiza as operações lógicas e retorna o valor final da
    expressão.

    '''
    end = False
    while not end:
        if not 'not' in expre and len(expre) != 1:
            for elemento in expre:
                if elemento == 'and':
                    index = expre.index('and')
                    op1 = index - 1
                    op2 = index + 1
                    end = True
                    return expre[op1] and expre[op2]
                elif elemento == 'or':
                    index = expre.index('or')
                    op1 = index - 1
                    op2 = index + 1
                    end = True
                    return expre[op1] or expre[op2]
                elif elemento == '->':
                    index = expre.index('->')
                    op1 = expre[index - 1]
                    op2 = expre[index + 1]
                    end = True
                    if op1 and op2:
                        return True
                    elif op1 and not op2:
                        return False
                    elif not op1 and op2:
                        return True
                    elif not op1 and not op2:
                        return True
                elif elemento == '<->':
                    index = expre.index('<->')
                    op1 = expre[index - 1]
                    op2 = expre[index + 1]
                    end = True
                    if op1 and op2:
                        return 1
                    elif op1 and not op2:
                        return 0
                    elif not op1 and op2:
                        return 0
                    elif not op1 and not op2:
                        return 1
                elif elemento == 'xv':
                    index = expre.index('xv')
                    op1 = expre[index - 1]
                    op2 = expre[index + 1]
                    end = True
                    if op1 and op2:
                        return 0
                    elif op1 and not op2:
                        return 1
                    elif not op1 and op2:
                        return 1
                    elif not op1 and not op2:
                        return 0
        else:
            aux = 0  # index auxiliar, pois não conflitará caso exista dois objetos iguais na lista.
            for elemento in expre:
                if elemento == 'not':
                    index = aux  # Armazena o valor do ultimo 'not' a aparecer na lista, caso hajam dois 'not' seguidos, assim pode fazê-los sem problemas
                aux += 1
            if len(expre) == 1:
                return expre[0]
            elif expre[index + 1] in [0, 1]:
                contrario = not expre[index + 1]  # Define o bool contrário
                expre.pop(index + 1)  # Remove o bool antigo
                expre.insert(index + 1, contrario)  # Insere o bool contrário
                expre.pop(index)  # Remove o 'not' operado


def resolve_expressao(sentencas, proposicao_bruta):
    '''
    Função que resolve as operações lógicas por meio de organizar as expressões com prioridade, pois, a partir dos index
    já determinados anteriormente (expressões com prioridade), a função faz um recorte a cada duas sentenças e as envia
    para a função anterior resolvê-la. Recebe o valor da operação feita, substitui o valor no lugar da expressão já re-
    solvida.

    '''
    resultado_de_cada_linha = {}
    expressoes = []  # O numero da linha corresponde ao index de cada elemento dessa lista, iniciando por 0.
    for i in range(2**len(sentencas)):
        expressoes.append(montador_de_expressao(sentencas, i, proposicao_bruta))

    aux = 0
    for expressao in expressoes:
        prop_bruta_aux = proposicao_bruta[:]
        passo_a_passo = []
        end = False
        while not end:
            lista_prio = prioridade(expressao)
            if len(lista_prio) != 0:
                while len(lista_prio) != 0:  # prio é uma lista com dois números referentes à prioridade (index).
                    prio = lista_prio[0]
                    inicio = prio[0]
                    fim = prio [1] + 1
                    expressao_prioritária = expressao[inicio:fim]
                    expressao_prioritaria_bruta = prop_bruta_aux[inicio:fim]  # Identifica o resultado das compostas parciais.
                    resultado = resolve_expressao_aux(expressao_prioritária)    
                    for i in range(inicio, fim):
                        expressao.pop(inicio)  # Remove a expressao já resolvida
                        prop_bruta_aux.pop(inicio)
                    expressao.insert(inicio, resultado)
                    lista_prio.remove(lista_prio[0])
                    expressao_prioritaria_bruta = lista_to_string(expressao_prioritaria_bruta)
                    global compostas_parciais
                    try:
                        compostas_parciais[expressao_prioritaria_bruta].append(resultado)
                    except:
                        compostas_parciais[expressao_prioritaria_bruta] = []

            else:
                resultado = resolve_expressao_aux(expressao)
                end = True
                resultado_de_cada_linha[aux] = resultado
        aux += 1

    return resultado_de_cada_linha


# Agora é montar a tabela
pt = PrettyTable()


def lista_to_string(lista):  # Transforma uma lista em string para ser escrita na tabela.
    string = ''
    for elemento in lista:
        string += str(elemento)

    return string


def montador_de_tabela(sentencas, proposicao_bruta, resultados):
    '''
    Monta a tabela associando os resultados finais das expressões com sua respectiva linha da tabela. Substitui os 0 e 1
    recebidos por True e False.

    '''
    sentencas1 = sentencas[:]
    global compostas_parciais
    for elemento in compostas_parciais:
        sentencas.append(elemento)
    sentencas.append(lista_to_string(proposicao_bruta))
    colunas = sentencas
    pt.field_names = colunas
    qtd_de_linhas = len(operadores_de_cada_sentenca['p'])
    for linha in range(qtd_de_linhas):
        line = []
        result = resultados[linha]
        for sentenca in sentencas1:
            line.append(operadores_de_cada_sentenca[sentenca][linha])
        for i in compostas_parciais:
            line.append(compostas_parciais[i][linha])
        if result == 0:
            result = 'False'
        elif result == 1:
            result = 'True'
        line.append(result)
        pt.add_row(line)
    print(pt)


def main():  # Chamada principal
    print("Tabela Verdade!")
    print("Por Alex Victor Silva")
    print()
    sleep(2)
    print('Use os seguintes sinais para cada operador: E = ^ , OU = v , NOT = ~ , CONDICIONAL = -> , BICONDICIONAL = <-> , OU EXCLUSIVO = xv .')
    sleep(2)
    proposicao_bruta = input('Digite a proposição lógica, com cada caracter separado por espaço. (Exemplo: ( p ^ q ) -> ~ r ): ').split()  # Faz a expressão ser uma lista
    sentencas = caca_sentencas(proposicao_bruta)
    resultados = resolve_expressao(sentencas, proposicao_bruta)  # Chama as funções secundárias
    montador_de_tabela(sentencas, proposicao_bruta, resultados)


if __name__ == '__main__':
    main()

