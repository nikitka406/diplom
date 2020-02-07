import random
import factory
#красивая печать
def BeautifulPrint(X, Y, Sresh, A):
    for k in range(factory.KA):
        print('Номер машины ', k)
        for i in range(factory.N):
            for j in range(factory.N):
                print(X[i][j][k], end = ' ')
            print("\n")

        print("e = ", end=' ')
        for i in range(factory.N):
            print(factory.e[i], end=' ')
        print("\n")

        print("y = ", end=' ')
        for  i in range(factory.N):
            print(Y[i][k], end=' ')
        print("\n")

        print("a = ", end=' ')
        for  i in range(factory.N):
            print(A[i][k], end=' ')
        print("\n")

        print("s = ", end=' ')
        for  i in range(factory.N):
            print(Sresh[i][k], end=' ')
        print("\n")
    for i in range(factory.N):
        for k in range (factory.N):
           print(factory.t[i][k], end=' ')
        print('\n')

    # for i in range(factory.N):
    #     #     for k in range (factory.N):
    #     #         print(factory.d[i][k], end=' ')
    #     #     print('\n')

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
                if factory.e[j] > factory.t[0][j]:
                    a[j][k] = factory.e[j]
                else:
                    a[j][k] = factory.t[0][j]
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

#ищем соседа слева либо справа
def SearchSosedLeftOrRight(x, y, client, leftOrRight):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    if leftOrRight == "left":
        for i in range(client):#ищем по столбцу
            if x[i][client][k] == 1:
                return i
        return -1
    if leftOrRight == "right":
        for i in range(client, factory.N):#ищем по строке
            if x[client][i][k] == 1:
                return i
        return -1

# определяем время приезда на конкретную локацию
def TimeOfArrival(a, s, client, sosed, sosedK):
    # если время прибытия меньше начала работ, то ждем
    if factory.e[client] > a[sosed][sosedK] + s[sosed][sosedK] + factory.t[sosed][client]:
        a[client][sosedK] = factory.e[client]
    # иначе ставим время прибытия
    else:
        a[client][sosedK] = a[sosed][sosedK] + s[sosed][sosedK] + factory.t[sosed][client]

#удаляем клиента из выбранного  маршрут
def DeleteClientaFromPath(x, y, s, a, client):
    k = NumberCarClienta(y, client)                              # номер машины которая обслуживает клиента
    clientLeft = SearchSosedLeftOrRight(x, y, client, "left")    #ищем город перед клиентом
    clientRight = SearchSosedLeftOrRight(x, y, client, "right")  #ищем город после клиента
    #если у клиента есть сосед справо и слево
    if clientLeft != -1 and clientRight != -1:
        x[clientLeft][clientRight][k] = 1                         #соединяем левого и правого соседа
        x[client][clientRight][k] = 0                            #удаляем ребро клиента с правым соседом
        x[clientLeft][client][k] = 0                             #удаляем ребро клиента с левым соседом

        # У и S для левого и правого не меняются, но время прибытия меняется
        y[client][k] = 0                                        #машина К больше не обслуживает клиента
        s[client][k] = 0                                        #время работы машины К у клиента = 0
        a[client][k] = 0                                        #машина не прибывает к клиенту

        TimeOfArrival(a, s, clientRight, clientLeft, k)
    # если клиент лист
    if clientLeft != -1 and clientRight == -1:
        x[clientLeft][client][k] = 0                            #теперь после левого соседа машина К никуда не едет кроме депо
        if clientLeft != 0:
            x[clientLeft][0][k] = 1                             #значит левый сосед становится листом и должен вернуться в депо
        x[client][0][k] = 0                                     #а клиент не возвращается в депо
        y[client][k] = 0                                        #клиент больше не обслуживается машиной К
        s[client][k] = 0                                        #машиной К больше не тратит время у клиента
        a[client][k] = 0                                        #и не приезжает
    if clientLeft == -1:                                         #logir
        print("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")

#присоеденям к листу
def JoinClientaList(x, y, s, a, client, sosed):
    clientK = NumberCarClienta(y, client)                   #ищем номер машины клиента
    sosedK = NumberCarClienta(y, sosed)                     #ищем номер машины соседа
    x[sosed][0][sosedK] = 0                                 #теперь сосед не лист, значит из него не едет в депо
    x[sosed][client][sosedK] = 1                            #вставляем клиента после соседа
    x[client][0][sosedK] = 1                                #теперь клиент литс, значит он возвращается в депо
    y[client][sosedK] = 1                                   #тепреь машина соседа обслуживает клиента
    s[client][sosedK] = s[client][clientK]                  #машина соседа будет работать у клиента столько же

    TimeOfArrival(a, s, client, sosed, sosedK)
    DeleteClientaFromPath(x, y, s, a, client)

#вклиниваем между
def JoinClientaNonList(x, y, s, a, client, sosed):
    sosedK = NumberCarClienta(y, sosed)
    clientK = NumberCarClienta(y, client)

    sosedLeft = SearchSosedLeftOrRight(x, y, sosed, "left")                                             #левый сосед соседа
    sosedRight = SearchSosedLeftOrRight(x, y, sosed, "right")                                           #правый сосед соседа

    zatratLeft = factory.t[sosedLeft][client] + factory.t[client][sosed] + factory.t[sosed][sosedRight] #затраты присунуть слева
    zatratRight = factory.t[sosedLeft][sosed] + factory.t[sosed][client] + factory.t[client][sosedRight]#затраты присунуть справа

    if zatratLeft >= zatratRight and factory.l[sosed] < factory.l[client] < factory.l[sosedRight]:
        x[sosed][client][sosedK] = 1
        x[client][sosedRight][sosedK] = 1
        y[client][sosedK] = 1                                                                           #тепреь машина соседа обслуживает клиента
        s[client][sosedK] = s[client][clientK]                                                          #машина соседа будет работать у клиента столько же
        TimeOfArrival(a, s, client, sosed, sosedK)
        DeleteClientaFromPath(x, y, s, a, client)
    elif zatratLeft < zatratRight and factory.l[sosedLeft] < factory.l[client] < factory.l[sosed]:
        x[sosedLeft][client][sosedK] = 1
        x[client][sosed][sosedK] = 1
        y[client][sosedK] = 1                                                                          # тепреь машина соседа обслуживает клиента
        s[client][sosedK] = s[client][clientK]                                                         # машина соседа будет работать у клиента столько же
        TimeOfArrival(a, s, client, sosed, sosedK)
        DeleteClientaFromPath(x, y, s, a, client)


def CombiningRoutesLessFine(x, y, s, a):
# копируем чтобы не испортить решение
    X = x
    Y = y
    Sresh = s
    A = a

#скорее всего нужен вайл пока ограничения выполняются
####### Bыбираем коиента листа#############
    flag = 1
    change_cl = [0 for i in range(factory.N)]
    while flag != 0:                                # Будем искать такого рандомного клиента который лист
        client = random.randint(1, (factory.N - 1)) #Берем рандомного клиента/ -1 потому что иногда может появится 10, а это выход за граници
        k = NumberCarClienta(y, client)             # получаем номер машины, которая обслуживает этого клиента
        for i in range(1, factory.N):
            if a[client][k] < a[i][k]:              #Если у машины, котораяя посещает clienta есть город,
                flag = 1                            # который она посещает позже, значит он НЕ ЛЕСИТ
            else:                                   #Он лист
                flag = 0
                change_cl[client] = 1               #флажок что мы этого клиента уже переставляли
###########################################
    print(client)
    sosed = SearchTheBestSoseda(client)             #выбираем нового, лучшего соседа
    print(sosed)
    k = NumberCarClienta(y, sosed)                  # узнаем машину которая обслуживает нового соседа
    print(k)
    #узнаем про нового соседа, лист он или нет
    flag = 0
    for i in range(1, factory.N):
        if a[sosed][k] < a[i][k]:                   #Если у машины, котораяя посещает соседа есть город,
            flag += 1                               # который она посещает позже, значит он НЕ ЛЕСИТ
        else:#Он лист
            flag += 0

    if flag == 0: #лист
        JoinClientaList(X, Y, Sresh, A, client, sosed)
        if VerificationOfBoundaryConditions(X, Y, Sresh, A) != 1:
            print("error")
            # if window_time_up(A, Sresh, Y) != 1:
                # то штраф
    else: #не лист
        JoinClientaNonList(x, y, s, a, client, sosed)
        # проверить временные рамки, если нарушились штрафовать
    BeautifulPrint(X, Y, Sresh, A)
    return X, Y, Sresh, A






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
                print("ERROR from X_join_Y: сломалось первое ограничение, несовместность переменных х, у")
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
                print("ERROR from V_jobs: сломалось второе ограничение, общий объем работ на объекте", i,"не совпадает с регламентом")
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
                print("ERROR from TC_equal_KA: сломалось третье ограничение, кол-во ТС на одном объекте", i,"больше чем число скважин")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, factory.N):
        for k in range(factory.KA):
            if s[i][k] > factory.S[i] * y[i][k]:
                print("ERROR from ban_driling: сломалось четвертое ограничение, ТС не приехало на объект", i,", но начало бурение")
                return 0
    return 1


def window_time_down(a, y):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, factory.N):
        for k in range(factory.KA):
            if factory.e[i] > a[i][k] and y[i][k] == 1:
                print("ERROR from window_time_down: сломалось пятое ограничение, время приезда на объкект", i,"меньше чем начало работ")#не работает ээто ограничение
                return 0
    return 1


def window_time_up(a, s, y):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, factory.N):
        for k in range(factory.KA):
            if a[i][k] + s[i][k] > factory.l[i] and y[i][k] == 1:
                print("ERROR from window_time_up: сломалось шестое ограничение, время окончание работ на объкект", i,"больше чем конец работ")
                return 0
    return 1


def ban_cycle(a, x, s, y):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, factory.N):
        for j in range(1, factory.N):
            for k in range(factory.KA):
                if a[i][k] - a[j][k] + x[i][j][k] * factory.t[i][j] + s[i][k] > factory.l[i] * (1 - x[i][j][k]) and y[i][k] == 1:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, машина", k,"не посещает депо")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(factory.KA):
                if s[i][k] < 0 or a[i][k] < 0:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, неправельные значение переменных a, s")
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, неправельное значение переменной x")
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    print("ERROR from ban_cycle: сломалось седьмое ограничение, неправельное значение переменной y")
                    return 0
    return 1

# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a):
    result = X_join_Y(x, y) * V_jobs(s) * TC_equal_KA(y) * ban_driling(s, y) * window_time_down(a, y) * window_time_up(a, s, y) * ban_cycle(a, x, s, y) * positive_a_and_s(x, y, a, s)
    if result == 1:
        return 1 # good
    else:
        return 0
