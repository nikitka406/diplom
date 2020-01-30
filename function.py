import random
from factory import *
########################### Входные значения
#Считаем кол-во используемых ТС
def AmountCarUsed(y):
    summa = 0                   #счетчик
    amount =0                   #число машин
    for k in range(KA):
        for j in range(N):
            summa += y[j][k]    #смотрим посещает ли К-ая машина хотя бы один город
        if summa != 0:          # если не 0 значит  посетила
            amount += 1         # прибавляем еденичку
        summa = 0               #Обнуляем счетчик
    return amount

# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, y, target_function = 0):
    for k in range(KA):
        for i in range(N):
            for j in range(N):
                target_function += d[i][j]*x[i][j][k]
    if AmountCarUsed(y) > K: #если кол-во используемых ТС пока еще боьше чем число допустимых, тогда штрафуем
        target_function += (AmountCarUsed(y) - K) * car_cost
    return target_function

# Распределяем на каждую локацию по машине
def OneCarOneLocation():
    # копия переменной задачи Х, только кол-вo машин = число локаций
    x = [[[0 for k in range(KA)] for j in range(N)] for i in range(N)] # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(KA)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(KA):
        y[0][k] = 1
    s = [[0 for k in range(KA)] for i in range(N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(KA)] for i in range(N)]  # время прибытия ТС с номером К на объект i


    #поочереди отправляем ТС на локации, по одному на скважину
    k = 0
    for j in range(1, N):
        if wells[j] >= 1:
            for i in range(wells[j]):
                x[0][j][k] = 1 # туда
                x[j][0][k] = 1 # обратно
                y[j][k] = 1
                if wells[j] > 1:
                    s[j][k] = S[j] / wells[j]
                else:
                    s[j][k] = S[j]
                if e[j] > t[0][j] / 24:
                    a[j][k] = e[j]
                else:
                    a[j][k] = t[0][j] / 24
                # print(a[j][k], end=' ')
                k += 1
            # print("\n")
    return x, y, s, a

#ищем минимальный путь по которому можно попасть в client
def SearchTheBestSoseda(d, client):
    neighbor = 0
    bufer = d[0][client]
    for i in range(N):
        if bufer <= d[i][client] and i != client:
            bufer = d[i][client]
            neighbor = i
    return neighbor

#номер машины которая обслуживает клиента
def NumberCarClienta(y, client, KA):
    for k in range(KA):
        if y[client][k] == 1:
            return k

#удаляем машину с локации если позволяют огр
def DeleteCarNonNarushOgr(x, y, s, a):
    #Убираем одну машину
    for i in range(1, N):
        # копии чтобы не испортить исходное решение
        X = x
        Y = y
        Sresh = s
        A = a
        if wells[i] > 1:                              #Выбираем только те локации у которых больше одной скважины
            for k in range(KA-1):
                if Y[i][k] == 1 and Y[i][k+1] == 1:   #-//- ту машину за которой едет еще одна
                    Y[i][k] = 0
                    Y[0][k] = 0
                    Sresh[i][k+1] += Sresh[i][k]
                    Sresh[i][k] = 0
                    A[i][k] = 0
                    X[0][i][k] = 0
                    X[i][0][k] = 0
                    # target_function -= car_cost
                    if VerificationOfBoundaryConditions(X, Y, Sresh, A) == 1:
                        x = X
                        y = Y
                        s = Sresh
                        a = A                       #Если ограничения не сломались то сохраняем эти изменения
    # return x, y, s, a#, target_function

#удаляем маршрут для выбранного клиента
def DeletePathClienta(x, y, s, a, client, KA):
    k = NumberCarClienta(y, client, KA)  # номер машины которая обслуживает клиента
    for i in range(N):
        if x[i][client][k] == 1 and y[i][k] == 1:
            x[client][i][k] = 0
            x[i][client][k] = 0
            y[i][k] = 0
            s[i][k] = 0
            a[i][k] = 0

# def MaxTimeEndJob():

#присоеденям к листу
def JoinClientaList(x, y, s, a, client, sosed, k):
    x[client][sosed][k] = 1
    x[sosed][client][k] = 1
    y[client][k] = 1
    s
    a[client][k] = a[sosed][k] + t[sosed][client]# здесь надо узнать мах время окончания работ у соседа

#вклиниваем между
# def JoinClientaNonList():

#
# def CombiningRoutesLessFine(x, y, s, a, KA, d):
# ####### Bыбираем коиента листа#############
#     summa = 1
#     client = 0
#     while summa != 0: # Будем искать такого рандомного клиента который лист
#         client = random.randint(1, N) #Берем рандомного клиента
#         k = NumberCarClienta(y, client, KA) # получаем номер машины, которая обслуживает этого клиента
#         for i in range(1, N):
#             if a[client][k] < a[i][k]:
#                 summa = 0
# ###########################################
#     X = x
#     Y = y
#     Sresh = s
#     A = a
#
#     sosed = SearchTheBestSoseda(d, client) #выбираем нового соседа
#
#     k = NumberCarClienta(y, sosed, KA) # узнаем машину которая обслуживает нового соседа
#     summa = 0 #узнаем про нового соседа, лист он или нет
#     for i in range(1, sosed):
#         summa += x[sosed][i][k]
#     for i in range(sosed+1, N):
#         summa += x[sosed][i][k]
#     if summa == 0 and wells:  #если лист
#         JoinClientaList()
#     # else:
#         # JoinClientaNonList()

# for k in range(KA):
#     print(k)
#     for i in range(N):
#         for j in range(N):
#             print(x[i][j][k], end = ' ')
#         print("\n")
# for i  in range(N):
#     for k in range (KA):
#         print(a[i][k], end=' ')
#     print('\n')
#
# for i  in range(N):
#     print(t[0][i], end=' ')
# print('\n')

# for n in range(10):
#     for k in range(KA):
#         print(X[n][0])
#         print(k)
#         for i in range(N):
#             for j in range(N):
#                 print(X[n][1][i][j][k], end = ' ')
#             print("\n")


# Граничные условия
def X_join_Y(x, y, KA):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(KA):
        for j in range(N):
            for i in range(N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                print("1")
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s, KA):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, N):
        if i != 0:
            for k in range(KA):
                bufer1 += s[i][k]
            if bufer1 != S[i]:
                print("2")
                return 0
            bufer1 = 0
    return 1


def TC_equal_KA(ka, y, KA):
    bufer1 =0
    # Add constraint: sum (y[i][k])<=ka[i]
    for i in range(1, N):
        if i != 0:
            for k in range(KA):
                bufer1 += y[i][k]
            if bufer1 > ka[i]:
                print("3")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y, KA):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, N):
        for k in range(KA):
            if s[i][k] > S[i] * y[i][k]:
                print("4")
                return 0
    return 1


def window_time_down(a, y, KA):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, N):
        for k in range(KA):
            if e[i] > a[i][k] and y[i][k] == 1:
                print("5")#не работает ээто ограничение
                return 0
    return 1


def window_time_up(a, s, y, KA):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, N):
        for k in range(KA):
            if a[i][k] + s[i][k] > l[i] and y[i][k] == 1:
                print("6")
                return 0
    return 1


def ban_cycle(a, x, s, y, KA):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, N):
        for j in range(1, N):
            for k in range(KA):
                if a[i][k] - a[j][k] + x[i][j][k] * t[i][j] + s[i][k] > l[i] * (1 - x[i][j][k]) and y[i][k] == 1:
                    print("7")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s, KA):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(N):
        for j in range(N):
            for k in range(KA):
                if s[i][k] < 0 or a[i][k] < 0:
                    print("8")
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    return 0
    return 1

# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a):
    result = X_join_Y(x, y, KA) * V_jobs(s, KA) * TC_equal_KA(wells, y, KA) * ban_driling(s, y, KA) * window_time_down(a, y, KA) * window_time_up(a, s, y, KA) * ban_cycle(a, x, s, y, KA) * positive_a_and_s(x, y, a, s, KA)
    if result == 1:
        return 1 # good
    else:
        return 0
