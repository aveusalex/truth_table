from prettytable import PrettyTable  # importar o módulo Pretty Table
from time import sleep

operadores_de_cada_sentenca = {}  # Definir variável global para ser retomado pela tabela


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
        valor_em_bool = dicionario_bools[sentenca][numero_da_linha]
        index_sentenca = proposicao_bruta.index(sentenca)
        proposicao_reformada.remove(sentenca)
        proposicao_reformada.insert(index_sentenca, valor_em_bool)

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


def prioridade(expressoes):
    '''
    Determina o index das operações com prioridade (parenteses, colchetes, chaves). Assim que os determina, retorna-os
    por uma lista. Além de contar quantos abre parênteses possui a expressão, pois eles podem dar problema na contagem
    se não forem considerados. Exemplo: [(pvq) v (rvs)] ^ t, se não considerarmos que após resolver o primeiro parêntese
    os indices dos outros dois parenteses mudam, daria problema na hora da resolução.

    '''
    expressao = expressoes[0]
    lista_prioridade = []
    aux = 0
    rep = expressao.count('(')
    for elemento in expressao:
        if elemento == '(':
            first_index = aux
        elif elemento == ')':
            second_index = aux
            lista_prioridade.append([first_index, second_index])
        elif elemento == '[':
            third_index = aux
        elif elemento == ']':
            fourth_index = aux
            lista_prioridade.append([third_index, fourth_index])
        elif elemento == '{':
            fifth_index = aux
        elif elemento == '}':
            sixth_index = aux
            lista_prioridade.append([fifth_index, sixth_index])
        aux += 1
    if rep > 1:
        valor_a_ser_subtraido = lista_prioridade[0][1] - lista_prioridade[0][0]
        for i in range(1, rep):
            lista_prioridade[i][0] -= valor_a_ser_subtraido
            lista_prioridade[i][1] -= valor_a_ser_subtraido

    return lista_prioridade, rep


def resolve_expressao_aux(expre):
    '''
    Função auxiliar para a resolução das expressões. Ela que realiza as operações lógicas e retorna o valor final da
    expressão.

    '''
    end = False
    while not end:
        if not 'not' in expre:
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

        else:
            aux = 0  # index auxiliar, pois não conflitará caso exista dois objetos iguais na lista.
            for elemento in expre:
                if elemento == 'not':
                    index = aux  # Armazena o valor do ultimo 'not' a aparecer na lista, caso hajam dois 'not' seguidos, assim pode fazê-los sem problemas
                aux += 1
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

    resultado_func_prioridade = prioridade(expressoes)  # lista_prio é uma lista com várias sub-lista binárias, com os index das prioridades.
    lista_prio1 = resultado_func_prioridade[0]
    rep = resultado_func_prioridade[1] - 1
    if len(lista_prio1) > 1 and rep == 0:
        aux = [lista_prio1[0]]
        for i in range(len(lista_prio1) - 1):  # Quantidade de operações a serem feitas
            valor_a_ser_subtraido = lista_prio1[0][1] - lista_prio1[0][0]
            for n in range(1, len(lista_prio1)):  # Operações de troca do valor prioridade
                lista_prio1[n][1] = lista_prio1[n][1] - valor_a_ser_subtraido
            aux.append(lista_prio1[1])
            lista_prio1.pop(0)

        lista_prio1 = aux[:]
    elif len(lista_prio1) > 1 and rep != 0:
        aux = []
        aux.append(lista_prio1[0])
        for i in range(len(lista_prio1) - 1):  # Quantidade de operações a serem feitas
            valor_a_ser_subtraido = lista_prio1[0][1] - lista_prio1[0][0]
            for n in range(1, len(lista_prio1) - rep):  # Operações de troca do valor prioridade
                lista_prio1[n+rep][1] = lista_prio1[n+rep][1] - valor_a_ser_subtraido
            aux.append(lista_prio1[1])
            lista_prio1.pop(0)
            if rep > 0:
                rep -= 1

        lista_prio1 = aux[:]

    aux = 0
    for expressao in expressoes:
        passo_a_passo = []
        lista_prio = lista_prio1[:]
        end = False
        while not end:
            if len(lista_prio) != 0:
                while len(lista_prio) != 0:  # prio é uma lista com dois números referentes à prioridade (index).
                    prio = lista_prio[0]
                    inicio = prio[0]
                    fim = prio [1] + 1
                    expressao_prioritária = expressao[inicio:fim]
                    resultado = resolve_expressao_aux(expressao_prioritária)
                    for i in range(inicio, fim):
                        expressao.pop(inicio)  # Remove a expressao já resolvida
                    expressao.insert(inicio, resultado)
                    lista_prio.remove(lista_prio[0])

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
    sentencas.append(lista_to_string(proposicao_bruta))
    colunas = sentencas
    pt.field_names = colunas
    qtd_de_linhas = len(operadores_de_cada_sentenca['p'])
    for linha in range(qtd_de_linhas):
        line = []
        result = resultados[linha]
        for sentenca in sentencas1:
            line.append(operadores_de_cada_sentenca[sentenca][linha])
        if result == 0:
            result = 'False'
        elif result == 1:
            result = 'True'
        line.append(result)
        pt.add_row(line)
    print(pt)




def main():  # Chamada principal
    sentencas = input('Digite os símbolos das sentenças, separados por espaço: ').split()  # Faz as sentenças serem listas
    sleep(0.5)
    print('Use os seguintes sinais para cada operador: E = ^ , OU = v , NOT = ~ , CONDICIONAL = -> , BICONDICIONAL = <-> .')
    sleep(2)
    proposicao_bruta = input('Digite a proposição lógica, com cada caracter separado por espaço. Não use V. (Exemplo: ( p ^ q ) -> ~ r ): ').split()  # Faz a expressão ser uma lista
    resultados = resolve_expressao(sentencas, proposicao_bruta)  # Chama as funções secundárias
    montador_de_tabela(sentencas, proposicao_bruta, resultados)

if __name__ == '__main__':
    main()

