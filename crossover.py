import factory

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

#номер посещения клиента
def NumberClientaInSequence(bufer, client, k):
    for i in range(factory.N + 1):
        if bufer[k][i] == client:
            return i

#Возвращает матрицу, где индекс это номер клиента а содержимое, это сколько раз его можно посетить
def CountOfVisitsPribityClient(bufer):
    contVisit = [0 for j in range(factory.N)]
    for client in range(factory.N):
        for k in range(factory.KA):
            for i in range(factory.N + 1):
                if bufer[k][i] == client:
                    contVisit[client] += 1
    return contVisit
#
# #кроссовер AEX
# def AEX(bufer1, bufer2, X1, Y1, S1, A1, X2, Y2, S2, A2):
#     # первы индекс это номер машины, второй это последовательность
#     children = [[0 for j in range(factory.N + 1)] for i in range(factory.KA)] #результат скрещивания (РЕБЕНОК)
#     contVisit1 = CountOfVisitsPribityClient(bufer1)
#     contVisit2 = CountOfVisitsPribityClient(bufer2)
#     for k in range(factory.KA):
#         if contVisit1[bufer1[k][0]] >= 0 and contVisit1[bufer1[k][1]] >= 0 or contVisit2[bufer1[k][0]] >= 0 and contVisit2[bufer1[k][1]] >= 0:
#             children[k][0] = bufer1[k][0]
#             children[k][1] = bufer1[k][1]
#             for i in range(2, factory.N+1):
