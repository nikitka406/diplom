import factory
from function import *
import random

#преобразование матрицы Х в последовательность посещения городов
#bul - порядок посещения
#i-откуда мы сейчас будем уезжать
#k-номер машины
def XDisplayInTheSequence(x, bufer, i, k, bul):
    for j in range(factory.N):
        if x[i][j][k] == 1:
            bul += 1
            bufer[k][bul] = j
            if j != 0:
                XDisplayInTheSequence(x, bufer, j, k, bul)

#номер машины которая обслуживает клиента
def NumberCarClientaInSequence(bufer, client):
    for k in range(factory.KA):
        for i in range(factory.N + 1):
            if bufer[k][i] == client:
                return k
    return -1

#номер посещения клиента
def NumberClientaInSequence(bufer, client, k):
    for i in range(factory.N + 1):
        if bufer[k][i] == client:
            return i
    return -1

#Возвращает матрицу, где индекс это номер клиента а содержимое, это сколько раз его можно посетить
def CountOfVisitsPribityClient(bufer):
    #TODO надо что-то сделать с депо, его можно сколько угодно посещать
    contVisit = [0 for j in range(factory.N)]
    for client in range(factory.N):
        for k in range(factory.KA):
            for i in range(factory.N + 1):
                if bufer[k][i] == client:
                    contVisit[client] += 1
    return contVisit

#рекурсивный поиск для скрещивания
#bufer_in- где ищем, bufer_out- откуда ищем
#bufer_out[k_out][i_out] - последний добавленный клиент в новый маршрут
def RecursiveSearchSosed(children, k, i, bufer_in, bufer_out, k_out, i_out, flag):
    #номер машины в bufer_in, которая обслуживает последнего добавленного клиента в ребенка из bufer_out
    k_in = NumberCarClientaInSequence(bufer_in, bufer_out[k_out][i_out])
    #номер позиции клиента в bufer_in из bufer_out
    i_in = NumberClientaInSequence(bufer_in, bufer_out[k_out][i_out], k_in)

    # Убираем последний добавленный чтобы больше на него не попадаться
    bufer_out[k_out][i_out] = 0

    #смотрим что этот город еще можно вставлять
    # bufer_in[k_in][i_in + 1] - новый, которого хотим добавить
    if flag[ bufer_in[k_in][i_in + 1] ] == 0:
        # добавляем в ребенка bufer_in[k_in][i_in + 1], ставим влаг
        flag [bufer_in[k_in][i_in + 1] ] += 1
        #добавляем в ребенка bufer_in[k_in][i_in + 1]
        children[k][i] = bufer_in[k_in][i_in + 1]
        #ищем дальше
        RecursiveSearchSosed(children, k, i+1, bufer_out, bufer_in, k_in, i_in, flag)

    #это значит что встретили ноль, цикл должен завершится
    elif flag[ bufer_in[k_in][i_in + 1] ] == -1:
        # добавляем в ребенка bufer_in[k_in][i_in + 1], ставим влаг
        flag[bufer_in[k_in][i_in + 1]] += 1
        # добавляем в ребенка bufer_in[k_in][i_in + 1]
        children[k][i] = bufer_in[k_in][i_in + 1]

    #Если мы его в на этом ТС уже посещали, то нужно взять рандомного
    #или его уже посетили в каком-то другом
    elif flag[bufer_in[k_in][i_in + 1]] == 1 or k_in == -1 and i_in == -1:
        #ищем нового клиента, пока не найдем не посещенного
        next_client = random.randint(0, factory.N-1)
        while flag[next_client] == 1:
            next_client = random.randint(0, factory.N - 1)
        # номер машины в bufer_in, которая обслуживает последнего добавленного клиента в ребенка из bufer_out
        k_in = NumberCarClientaInSequence(bufer_in, next_client)
        # номер позиции клиента в bufer_in из bufer_out
        i_in = NumberClientaInSequence(bufer_in, next_client, k_in)

        if k_in != -1 and i_in != -1:
            # это значит что встретили ноль, цикл должен завершится
            if flag[next_client] == -1:
                # добавляем в ребенка bufer_in[k_in][i_in + 1], ставим влаг
                flag[next_client] += 1
                # добавляем в ребенка bufer_in[k_in][i_in + 1]
                children[k][i] = next_client

            # смотрим что этот город еще можно вставлять
            elif flag[next_client] == 0:
                # добавляем в ребенка bufer_in[k_in][i_in + 1], ставим влаг
                flag[next_client] += 1
                # добавляем в ребенка bufer_in[k_in][i_in + 1]
                children[k][i] = next_client
                # ищем дальше
                RecursiveSearchSosed(children, k, i + 1, bufer_out, bufer_in, k_in, i_in, flag)
            else:
                print("ERROR from RecursiveSearchSosed inside: ошибка в поске рандомного нового клиента")
            #TODO нужно описать ситуацию, когда цикл закончился, а посетили еще не все
    else:
        print("ERROR from RecursiveSearchSosed outside: проблема с флагами, не нашли не ноль, не еще не посещенный")



#кроссовер AEX
def AEX(sequence1, sequence2, X1, Y1, S1, A1, X2, Y2, S2, A2):
    #сохроняем последовательности чтобы не испортить
    bufer1 = sequence1
    bufer2 = sequence2

    #кол-во используемых машин в каждом решение
    size1 = AmountCarUsed(Y1)
    size2 = AmountCarUsed(Y2)
    # первы индекс это номер машины, второй это последовательность
    children = [[0 for j in range(factory.N + 1)] for i in range(factory.KA)]  # результат скрещивания (РЕБЕНОК)

    #определяем по кому будем делать цикл
    if size1 >= size2:
        for k in range(size1):
            #флаг, для посещенных городов в одном маршруте(одной машиной)
            flag = [0 for j in range(factory.N)]
            flag[0] = -2

            children[k][0] = bufer1[k][0]
            children[k][1] = bufer1[k][1]

            flag[bufer1[k][0]] += 1
            flag[bufer1[k][1]] += 1

            RecursiveSearchSosed(children, k, 2, bufer2, bufer1, k, 1, flag)
    elif size2 < size1:
        for k in range(size2):
            # флаг, для посещенных городов в одном маршруте(одной машиной)
            flag = [0 for j in range(factory.N)]
            flag[0] = -2

            children[k][0] = bufer2[k][0]
            children[k][1] = bufer2[k][1]

            flag[bufer2[k][0]] += 1
            flag[bufer2[k][1]] += 1

            RecursiveSearchSosed(children, k, 2, bufer1, bufer2, k, 1, flag)

    else:
        print("ERROR from AEX: исключение, произошло не возможное!!!!")
