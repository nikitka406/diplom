import factory
from function import *
import random

#преобразование матрицы Х в последовательность посещения городов,
#bul - порядок посещения
#i-откуда мы сейчас будем уезжать
#k-номер машины
def XDisplayInTheSequenceX2(x, bufer, i, k, bul):
    for j in range(factory.N):
        if x[i][j][k] == 1:
            bul += 1
            bufer[k][bul] = j
            if j != 0:
                XDisplayInTheSequenceX2(x, bufer, j, k, bul)

#Получаем двумерную последовательность
def GettingTheSequence(X):
    #factory.N+1 потому что последовательность может посещать все города и при этом возвращается в 0
    sequenceX2 = [[0 for i in range(factory.N+1)] for j in range(factory.KA)]
    for k in range(factory.KA):
        XDisplayInTheSequenceX2(X, sequenceX2, 0, k, 0)
    return sequenceX2

#количество посещений в последовательности
def CountVisitInSequence(sequenceX1):
    for i in range(1, (factory.N+1) * factory.KA):
        if sequenceX1[i - 1] != 0 and sequenceX1[i] == 0 and (sequenceX1[i + 1] == 0 or i == ((factory.N+1) * factory.KA - 1)):
            return i + 1

#уменьшить размерность последовательности
def LowerTheDimensionOfTheSequence(sequenceX1):
    size = CountVisitInSequence(sequenceX1)

    bufer = [0 for i in range(size)]

    for i in range(size):
        bufer[i] = sequenceX1[i]
    return bufer

#Переделываем двумерную в одномерную, вида 014856047852098704850
def TransferX2toX1(sequenceX2):
    sequenceX1 = [0 for i in range((factory.N+1) * factory.KA)]
    j = 1
    for k in range(factory.KA):
        for i in range(1, factory.N-1):
            print(i)
            #случай когда находишься на цифре и следующая цифра
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] != 0:
                sequenceX1[j] = sequenceX2[k][i]
                j += 1
            # случай когда находишься на цифре и следующий ноль
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] == 0:
                sequenceX1[j] = sequenceX2[k][i]
                j += 1
            # случай когда находишься на нуле и предыдущая цифра
            if sequenceX2[k][i - 1] != 0 and sequenceX2[k][i] == 0:
                sequenceX1[j] = sequenceX2[k][i]
                j += 1
    sequenceX1 = LowerTheDimensionOfTheSequence(sequenceX1)
    return sequenceX1

#номер машины которая обслуживает клиента
def NumberCarClientaInSequence(bufer, client):
    for k in range(factory.KA):
        for i in range(factory.N + 1):
            if bufer[k][i] == client:
                return k
    return -1

#номер посещения клиента
def NumberClientaInSequence(bufer, client):
    for i in range(factory.N + 1):
        if bufer[i] == client:
            return i
        else
            print("ERROR for NumberClientaInSequence: Не нашел номер посещения клиента в последовательности")
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
#bufer_in- где ищем(Куда едем), bufer_out- откуда ищем
#bufer_out[i_out] - последний добавленный клиент в новый маршрут
#i_out - номер последнего добавленног клиента
#i - номер куда будем добавлять в ребенке

def RecursiveSearchSosed(children, i, bufer_in, bufer_out, i_out, flag, flagAll, countOfRaces):

    # #номер машины в bufer_in, которая обслуживает последнего добавленного клиента в ребенка из bufer_out
    # k_in = NumberCarClientaInSequence(bufer_in, bufer_out[i_out])
    #номер позиции клиента bufer_out[i_out] в bufer_in
    i_in = NumberClientaInSequence(bufer_in, bufer_out[i_out])

    # # Убираем последний добавленный чтобы больше на него не попадаться
    # bufer_out[i_out] = 0
    # bufer_in[i_in] = 0

    #смотрим что этот город еще можно вставлять, в этот маршрут
    # bufer_in[i_in + 1] - новый, которого хотим добавить
    if flag[ bufer_in[i_in + 1] ] == 0 and countOfRaces[bufer_in[i_in + 1]] > 0:
        # ставим флаг
        flag [bufer_in[i_in + 1] ] += 1
        flagAll[bufer_in[i_in + 1]] = 1
        #добавляем в ребенка bufer_in[i_in + 1]
        children[i] = bufer_in[i_in + 1]
        #ищем дальше
        RecursiveSearchSosed(children, i+1, bufer_out, bufer_in, i_in+1, flag, flagAll)

    #это значит что встретили ноль, цикл должен завершится
    elif flag[ bufer_in[i_in + 1] ] == -1:
        # ставим влаг
        flag[bufer_in[i_in + 1]] += 1
        flagAll[bufer_in[i_in + 1]] = 1
        # добавляем в ребенка bufer_in[k_in][i_in + 1]
        children[i] = bufer_in[i_in + 1]

    #Если мы его на этом ТС уже посещали, то нужно взять рандомного
    #или у него больше не хватает скважин
    elif flag[bufer_in[i_in + 1]] == 1 or countOfRaces[bufer_in[i_in + 1]] <= 0:
        #Берем рандомного клиента
        next_client = random.randint(0, factory.N-1)
        # номер позиции клиента bufer_out[i_out] в bufer_in
        i_in = NumberClientaInSequence(bufer_in, next_client)

        # ищем нового клиента, пока не найдем не посещенного и у которого остались свободные скважины
        while flag[next_client] == 1 or countOfRaces[bufer_in[i_in + 1]] <= 0:
            next_client = random.randint(0, factory.N - 1)
            # номер позиции клиента bufer_out[i_out] в bufer_in
            i_in = NumberClientaInSequence(bufer_in, next_client)

        # это значит что встретили ноль, цикл должен завершится
        if flag[next_client] == -1:
            #ставим влаг
            flag[next_client] += 1
            flagAll[bufer_in[i_in + 1]] = 1
            # добавляем в ребенка bufer_in[i_in + 1]
            children[i] = next_client

        # смотрим что этот город еще можно вставлять
        elif flag[next_client] == 0:
            # ставим влаг
            flag[next_client] += 1
            flagAll[bufer_in[i_in + 1]] = 1
            # добавляем в ребенка bufer_in[i_in + 1]
            children[i] = next_client
            # ищем дальше
            RecursiveSearchSosed(children, i + 1, bufer_out, bufer_in, i_in, flag, flagAll)
        else:
            print("ERROR from RecursiveSearchSosed inside: ошибка в поске рандомного нового клиента")
    else:
        print("ERROR from RecursiveSearchSosed outside: проблема с флагами, не нашли не ноль, не еще не посещенный")

#кроссовер AEX
def AEX(sequence1, sequence2, X1, Y1, S1, A1, X2, Y2, S2, A2):
    # первый индекс это номер машины, второй это последовательность
    children = [0 for i in range((factory.N+1) * factory.KA)]  # результат скрещивания (РЕБЕНОК)

    #сохроняем последовательности чтобы не испортить
    bufer1 = sequence1
    bufer2 = sequence2

    #кол-во используемых машин в каждом решение
    size1 = CountVisitInSequence(sequence1)
    size2 = CountVisitInSequence(sequence2)

    # флаг, для посещенных городов в заключительном решении
    flagAll = [0 for j in range(factory.N)]
    #сколько раз можно заехать к каждому
    countOfRaces = factory.wells

    #определяем по кому будем делать цикл
    if size1 >= size2:
        # флаг, для посещенных городов в одном маршруте(одной машиной)
        flag = [0 for j in range(factory.N)]
        flag[0] = -2

        #Добавляем первые два города в ребенка
        children[0] = bufer1[0]
        children[1] = bufer1[1]

        #Расставляем флажки локально для первой машины и для общего решения
        flag[bufer1[0]] += 1
        flag[bufer1[1]] += 1
        flagAll[bufer1[0]] = 1
        flagAll[bufer1[1]] = 1
        #на одну мащину к нему теперь может приехать меньше
        countOfRaces[bufer1[1]] -= 1

        #Число задействованных машин в ребенке
        k = 0
        #Индекс который идет по ребенку
        j = 2

        #Для первого добавления запустим без цикла
        RecursiveSearchSosed(children, j, bufer2, bufer1, 1, flag, flagAll)
        #Обнуляем флаг для следующей машины
        for i in range(factory.N):
            flag[i] = 0
        flag[0] = -2

        #Добавляем еще одну машину + сдвигаем индекс последовательности
        k += 1
        j += 1

        #Пока есть свободные не арендованные машины или остались не посещенные города
        while k <= factory.K or sum(flagAll) <= factory.N:

            RecursiveSearchSosed(children, 2, bufer2, bufer1, 1, flag, flagAll)

            for i in range(factory.N):
                flag[i] = 0
            flag[0] = -2
            k += 1
            j += 1


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
    # TODO нужно описать ситуацию, когда цикл закончился, а посетили еще не все
    else:
        print("ERROR from AEX: исключение, произошло не возможное!!!!")
