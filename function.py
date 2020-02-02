import random
import factory

#Считаем кол-во используемых ТС
def AmountCarUsed(y):
    summa = 0                   #счетчик
    amount =0                   #число машин
    for k in range(factory.KA):
        for j in range(factory.N):
            summa += y[j][k]    #смотрим посещает ли К-ая машина хотя бы один город
        if summa != 0:          # если не 0 значит  посетила
            amount += 1         # прибавляем еденичку
        summa = 0               #Обнуляем счетчик
    return amount

# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, y, target_function = 0):
    for k in range(factory.KA):
        for i in range(factory.N):
            for j in range(factory.N):
                target_function += factory.d[i][j]*x[i][j][k]
    if AmountCarUsed(y) > factory.K: #если кол-во используемых ТС пока еще боьше чем число допустимых, тогда штрафуем
        target_function += (AmountCarUsed(y) - factory.K) * factory.car_cost
    return target_function

# Распределяем на каждую локацию по машине
def OneCarOneLocation():
    # копия переменной задачи Х, только кол-вo машин = число локаций
    x = [[[0 for k in range(factory.KA)] for j in range(factory.N)] for i in range(factory.N)] # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(factory.KA):
        y[0][k] = 1
    s = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i


    #поочереди отправляем ТС на локации, по одному на скважину
    k = 0
    for j in range(1, factory.N):
        if factory.wells[j] >= 1:
            for i in range(factory.wells[j]):
                x[0][j][k] = 1 # туда
                x[j][0][k] = 1 # обратно
                y[j][k] = 1
                if factory.wells[j] > 1:
                    s[j][k] = factory.S[j] / factory.wells[j]
                else:
                    s[j][k] = factory.S[j]
                if factory.e[j] > factory.t[0][j] / 24:
                    a[j][k] = factory.e[j]
                else:
                    a[j][k] = factory.t[0][j] / 24
                # print(a[j][k], end=' ')
                k += 1
            # print("\n")
    return x, y, s, a

#удаляем машину с локации если позволяют огр
def DeleteCarNonNarushOgr(x, y, s, a):
    #Убираем одну машину
    for i in range(1, factory.N):
        # копии чтобы не испортить исходное решение
        X = x
        Y = y
        Sresh = s
        A = a
        if factory.wells[i] > 1:                              #Выбираем только те локации у которых больше одной скважины
            for k in range(factory.KA-1):
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

#перезапись одного маршрута на другой
def Rewriting(Y, k, m, flag):
    if flag == "1":
        for j in range(factory.N):
            Y[j][k] = Y[j][m]
            Y[j][m] = 0
    if flag == "2":
        for i in range(factory.N):
            for j in range(factory.N):
                Y[i][j][k] = Y[i][j][m]
                Y[i][j][m] = 0

#удаляем/уменьшаем размерность с помощью не используемых машин
def DeleteNotUsedCar(x, y, s, a):
    summa1 = 0
    summa2 = 0
    for k in range(factory.KA):
        summa1 = 0  # Обнуляем счетчик
        for j in range(factory.N):
            summa1 += y[j][k]    #смотрим посещает ли К-ая машина хотя бы один город
        if summa1 == 0:          # если 0 значит не посещает
            for m in range(k+1, factory.KA): # ищем ближайшую рабочую машину
                summa2 = 0
                for i in range(factory.N):
                    summa2 += y[i][m]
                if summa2 != 0: #сохзанем ее в первый пустой маршрут
                    Rewriting(y, k, m, "1")
                    Rewriting(s, k, m, "1")
                    Rewriting(a, k, m, "1")
                    Rewriting(x, k, m, "2")
                    break
    factory.KA = AmountCarUsed(y)
    X = [[[0 for k in range(factory.KA)] for j in range(factory.N)] for i in range(factory.N)]  # едет или нет ТС с номером К из города I в J
    Y = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    Sresh = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    A = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i
    for k in range(factory.KA):
        for i in range(factory.N):
            for j in range(factory.N):
                X[i][j][k] = x[i][j][k]
            Y[i][k] = y[i][k]
            Sresh[i][k] = s[i][k]
            A[i][k] = a[i][k]
    return X, Y, Sresh, A

#ищем минимальный путь по которому можно попасть в client
def SearchTheBestSoseda(client):
    neighbor = 0                                                #старый сосед
    bufer = factory.d[0][client]                                #расстояние от старого сосед адо клиента
    for i in range(factory.N):
        if bufer >= factory.d[i][client] and i != client:       #ищим мин расстояние до клиента с учетом что новый сосед не клиент
            bufer = factory.d[i][client]
            neighbor = i
    return neighbor

#номер машины которая обслуживает клиента
def NumberCarClienta(y, client):
    for k in range(factory.KA):
        if y[client][k] == 1:
            return k

#удаляем маршрут для выбранного клиента
def DeletePathClienta(x, y, s, a, client):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    for i in range(factory.N):
        if x[i][client][k] == 1 and y[i][k] == 1:
            x[client][i][k] = 0
            x[i][client][k] = 0
            y[i][k] = 0
            s[i][k] = 0
            a[i][k] = 0

# def MaxTimeEndJob():
#
# #присоеденям к листу
# def JoinClientaList(x, y, s, a, client, sosed, k):
#     x[client][sosed][k] = 1
#     x[sosed][client][k] = 1
#     y[client][k] = 1
#     s
#     a[client][k] = a[sosed][k] + t[sosed][client]# здесь надо узнать мах время окончания работ у соседа
#
# вклиниваем между
# def JoinClientaNonList():


def CombiningRoutesLessFine(x, y, s, a):
####### Bыбираем коиента листа#############
    flag = 1
    while flag != 0: # Будем искать такого рандомного клиента который лист
        client = random.randint(1, (factory.N - 1)) #Берем рандомного клиента/ -1 потому что иногда может появится 10, а это выход за граници
        k = NumberCarClienta(y, client) # получаем номер машины, которая обслуживает этого клиента
        for i in range(1, factory.N):
            if a[client][k] < a[i][k]:
                flag = 1
            else:
                flag = 0

    # for i  in range(factory.N):
    #     for k in range (factory.KA):
    #         print(y[i][k], end=' ')
    #     print('\n')
    #
    #
    # print('\n')
    # for i  in range(factory.N):
    #     for k in range (factory.KA):
    #         print(a[i][k], end=' ')
    #     print('\n')

###########################################

    sosed = SearchTheBestSoseda(client) #выбираем нового соседа

    # X = x
    # Y = y
    # Sresh = s
    # A = a
    #
    # k = NumberCarClienta(y, sosed, KA) # узнаем машину которая обслуживает нового соседа
    # summa = 0 #узнаем про нового соседа, лист он или нет
    # for i in range(1, sosed):
    #     summa += x[sosed][i][k]
    # for i in range(sosed+1, N):
    #     summa += x[sosed][i][k]
    # if summa == 0 and wells:  #если лист
    #     JoinClientaList()
    # else:
    #     JoinClientaNonList()
    #


# for k in range(factory.KA):
#     print('Номер машины ', k)
#     for i in range(factory.N):
#         for j in range(factory.N):
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
def X_join_Y(x, y):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(factory.KA):
        for j in range(factory.N):
            for i in range(factory.N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                print("1")
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, factory.N):
        if i != 0:
            for k in range(factory.KA):
                bufer1 += s[i][k]
            if bufer1 != factory.S[i]:
                print("2")
                return 0
            bufer1 = 0
    return 1


def TC_equal_KA(y):
    bufer1 =0
    # Add constraint: sum (y[i][k])<=ka[i]
    for i in range(1, factory.N):
        if i != 0:
            for k in range(factory.KA):
                bufer1 += y[i][k]
            if bufer1 > factory.wells[i]:
                print("3")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, factory.N):
        for k in range(factory.KA):
            if s[i][k] > factory.S[i] * y[i][k]:
                print("4")
                return 0
    return 1


def window_time_down(a, y):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, factory.N):
        for k in range(factory.KA):
            if factory.e[i] > a[i][k] and y[i][k] == 1:
                print("5")#не работает ээто ограничение
                return 0
    return 1


def window_time_up(a, s, y):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, factory.N):
        for k in range(factory.KA):
            if a[i][k] + s[i][k] > factory.l[i] and y[i][k] == 1:
                print("6")
                return 0
    return 1


def ban_cycle(a, x, s, y):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, factory.N):
        for j in range(1, factory.N):
            for k in range(factory.KA):
                if a[i][k] - a[j][k] + x[i][j][k] * factory.t[i][j] + s[i][k] > factory.l[i] * (1 - x[i][j][k]) and y[i][k] == 1:
                    print("7")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(factory.KA):
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
    result = X_join_Y(x, y) * V_jobs(s) * TC_equal_KA(y) * ban_driling(s, y) * window_time_down(a, y) * window_time_up(a, s, y) * ban_cycle(a, x, s, y) * positive_a_and_s(x, y, a, s)
    if result == 1:
        return 1 # good
    else:
        return 0
