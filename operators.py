from function import *


# вклиниваем между
def OperatorJoinFromReloc(x, y, s, a, sizeK, client, sosed, iteration):
    Xl, Yl, Sl, Al = ReadRelocateOfFile(sizeK)
    XR, YR, SR, AR = ReadRelocateOfFile(sizeK)

    sosedK = NumberCarClienta(Yl, sosed)
    clientK = NumberCarClienta(Yl, client)

    sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left")  # левый сосед соседа
    sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right")  # правый сосед соседа

    print("sosed_left = ", sosedLeft)
    print("sosed_right = ", sosedRight)

    print("Время окончание client = ", factory.l[client])
    print("Время окончание sosed = ", factory.l[sosed])
    print("Время окончание sosedLeft = ", factory.l[sosedLeft])
    print("Время окончание sosedRight = ", factory.l[sosedRight])

    # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
    # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
    try:
        print("Вставляем клиента к соседу справа")
        # машина соседа будет работать у клиента столько же
        SR[client][sosedK] = SR[client][clientK]

        # Чтобы все корректно работало, сначала надо написать
        # новое время приезда и новое время работы, потом
        # удалить старое решение, и только потом заполнять Х и У
        XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client)
        XR[sosed][sosedRight][sosedK] = 0
        XR[sosed][client][sosedK] = 1
        XR[client][sosedRight][sosedK] = 1
        YR[client][sosedK] = 1  # тепреь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        AR = TimeOfArrival(XR, YR, SR)

    except IOError:
        print("Объект не удален")
        XR[sosed][sosedRight][sosedK] = 1
        XR[sosed][client][sosedK] = 0
        XR[client][sosedRight][sosedK] = 0
        YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        AR = TimeOfArrival(XR, YR, SR)

    try:
        print("Вставляем клиента к соседу слева")
        # машина соседа будет работать у клиента столько же
        Sl[client][sosedK] = Sl[client][clientK]

        # Чтобы все корректно работало, сначала надонаписать
        # новое время приезда и новое время работы, потом
        # удалить старое решение, и только потом заполнять Х и У
        Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client)
        Xl[sosedLeft][sosed][sosedK] = 0
        Xl[sosedLeft][client][sosedK] = 1
        Xl[client][sosed][sosedK] = 1
        Yl[client][sosedK] = 1  # теперь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        Al = TimeOfArrival(Xl, Yl, Sl)

    except IOError:
        print("Объект не удален")
        Xl[sosedLeft][sosed][sosedK] = 1
        Xl[sosedLeft][client][sosedK] = 0
        Xl[client][sosed][sosedK] = 0
        Yl[client][sosedK] = 0  # теперь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        Al = TimeOfArrival(Xl, Yl, Sl)

    print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого")
    if window_time_up(Al, Sl, Yl) == 0:
        if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true") == 1:
            print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
            targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
            print("Подсчет целевой функции для левого вставления ", targetL)
        else:
            targetL = -1
            print(
                "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
    elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al) == 1:
        print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
        targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
        print("Подсчет целевой функции для левого вставления ", targetL)
    else:
        targetL = -1
        print("ERROR from Relocate: не получилось переставить, что-то пошло нет")

    print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого")
    if window_time_up(AR, SR, YR) == 0:
        if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true") == 1:
            print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
            targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
            print("Подсчет целевой функции для правого вставления ", targetR)
        else:
            targetR = -1
            print(
                "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
    elif VerificationOfBoundaryConditions(XR, YR, SR, AR) == 1:
        print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
        targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
        print("Подсчет целевой функции для правого вставления ", targetR)
    else:
        targetR = -1
        print("ERROR from Relocate: не получилось переставить, что-то пошло нет")

    print("Теперь ищем минимум из двух целевых")
    minimum = min(targetL, targetR)
    if minimum == targetL and minimum != -1:
        print("Выбрали левого у него целевая меньше")
        # for k in range(len(Xl[0][0])):
        #     print('Номер машины ', k)
        #     for i in range(factory.N):
        #         for j in range(factory.N):
        #             print(Xl[i][j][k], end=' ')
        #         print("\n")
        return Xl, Yl, Sl, Al, targetL, sizeK, iteration

    elif minimum == targetR and minimum != -1:
        print("Выбрали правого у него целевая меньше")
        # for k in range(len(XR[0][0])):
        #     print('Номер машины ', k)
        #     for i in range(factory.N):
        #         for j in range(factory.N):
        #             print(XR[i][j][k], end=' ')
        #         print("\n")
        return XR, YR, SR, AR, targetR, sizeK, iteration

    else:
        print("Все пошло по пизде ничего не сохранили")
        return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK, iteration


# переставляем клиента к новому соседу, локальный поиск
def Relocate(X, Y, Sresh, A, target_function_start, sizeK_start, iteration):
    file = open("log/relog.txt", 'w')
    file.write("->Relocate start" + '\n')

    SaveRelocate(X, Y, Sresh, A, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    while TargetFunction != buf_targ:
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadRelocateOfFile(SizeK)

        # Bыбираем клиента
        client = random.randint(1, (
                factory.N - 1))  # Берем рандомного клиента -1 потому что иногда может появится 10, а это выход за граници

        file.write("Переставляем клиентa " + str(client) + '\n')
        file.write("С машины" + str(NumberCarClienta(Y, client)) + '\n')

        for sosed in range(1, factory.N):

            if client != sosed:
                sosedK = NumberCarClienta(Y, sosed)

                file.write("К соседу " + str(sosed) + '\n')
                file.write("На машине " + str(sosedK) + '\n')

                x, y, s, a, target_function, sizeK, iteration = OperatorJoinFromReloc(X, Y, Sresh, A, SizeK, client,
                                                                                      sosed, iteration)
                file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                file.write("Выбираем минимальное решение" + '\n')
                minimum = min(TargetFunction, target_function)
                if minimum == target_function:
                    file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                    file.write("Новая целевая функция равна " + str(target_function) + '\n')

                    SaveRelocate(x, y, s, a, sizeK)
                    TargetFunction = target_function
                    SizeK = sizeK
                else:
                    file.write("Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                    file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')

    file.write("Локальный оптимум найден сохраняем в популяцию решение" + '\n')
    for k in range(sizeK):
        for i in range(factory.N):
            for j in range(factory.N):
                file.write(str(X[i][j][k]) + ' ')
            file.write("\n")
        file.write("\n")

    X, Y, Sresh, A = ReadRelocateOfFile(SizeK)

    file.write("<-Relocate stop" + '\n')
    file.close()

    return X, Y, Sresh, A, TargetFunction, SizeK, iteration


# Подсчет сколько объектов обслуживает машина
def CountObjInCar(y, car):
    count = 0
    for i in range(1, factory.N):
        if y[i][car] == 1:
            count += 1
    return count


# def OperatorJoinFromTwoOpt(X, Y, Sresh, A, SizeK, client1, client2, sosed1, sosed2, iteration):
#     Xl, Yl, Sl, Al = ReadRelocateOfFile(sizeK)
#     XR, YR, SR, AR = ReadRelocateOfFile(sizeK)
#
#     sosedK = NumberCarClienta(Yl, sosed)
#     clientK = NumberCarClienta(Yl, client)
#
#     sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left")  # левый сосед соседа
#     sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right")  # правый сосед соседа
#
#     print("sosed_left = ", sosedLeft)
#     print("sosed_right = ", sosedRight)
#
#     print("Время окончание client = ", factory.l[client])
#     print("Время окончание sosed = ", factory.l[sosed])
#     print("Время окончание sosedLeft = ", factory.l[sosedLeft])
#     print("Время окончание sosedRight = ", factory.l[sosedRight])
#
#     # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
#     # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
#     try:
#         print("Вставляем клиента к соседу справа")
#         # машина соседа будет работать у клиента столько же
#         SR[client][sosedK] = SR[client][clientK]
#
#         # Чтобы все корректно работало, сначала надо написать
#         # новое время приезда и новое время работы, потом
#         # удалить старое решение, и только потом заполнять Х и У
#         XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client)
#         XR[sosed][sosedRight][sosedK] = 0
#         XR[sosed][client][sosedK] = 1
#         XR[client][sosedRight][sosedK] = 1
#         YR[client][sosedK] = 1  # тепреь машина соседа обслуживает клиента
#
#         # Подсчет времени приезда к клиенту от соседа
#         AR = TimeOfArrival(XR, YR, SR)
#
#     except IOError:
#         print("Объект не удален")
#         XR[sosed][sosedRight][sosedK] = 1
#         XR[sosed][client][sosedK] = 0
#         XR[client][sosedRight][sosedK] = 0
#         YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента
#
#         # Подсчет времени приезда к клиенту от соседа
#         AR = TimeOfArrival(XR, YR, SR)
#
#     try:
#         print("Вставляем клиента к соседу слева")
#         # машина соседа будет работать у клиента столько же
#         Sl[client][sosedK] = Sl[client][clientK]
#
#         # Чтобы все корректно работало, сначала надонаписать
#         # новое время приезда и новое время работы, потом
#         # удалить старое решение, и только потом заполнять Х и У
#         Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client)
#         Xl[sosedLeft][sosed][sosedK] = 0
#         Xl[sosedLeft][client][sosedK] = 1
#         Xl[client][sosed][sosedK] = 1
#         Yl[client][sosedK] = 1  # теперь машина соседа обслуживает клиента
#
#         # Подсчет времени приезда к клиенту от соседа
#         Al = TimeOfArrival(Xl, Yl, Sl)
#
#     except IOError:
#         print("Объект не удален")
#         Xl[sosedLeft][sosed][sosedK] = 1
#         Xl[sosedLeft][client][sosedK] = 0
#         Xl[client][sosed][sosedK] = 0
#         Yl[client][sosedK] = 0  # теперь машина соседа обслуживает клиента
#
#         # Подсчет времени приезда к клиенту от соседа
#         Al = TimeOfArrival(Xl, Yl, Sl)
#
#     print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого")
#     if window_time_up(Al, Sl, Yl) == 0:
#         if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true") == 1:
#             print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
#             targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
#             print("Подсчет целевой функции для левого вставления ", targetL)
#         else:
#             targetL = -1
#             print(
#                 "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
#     elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al) == 1:
#         print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
#         targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
#         print("Подсчет целевой функции для левого вставления ", targetL)
#     else:
#         targetL = -1
#         print("ERROR from Relocate: не получилось переставить, что-то пошло нет")
#
#     print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого")
#     if window_time_up(AR, SR, YR) == 0:
#         if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true") == 1:
#             print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
#             targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
#             print("Подсчет целевой функции для правого вставления ", targetR)
#         else:
#             targetR = -1
#             print(
#                 "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
#     elif VerificationOfBoundaryConditions(XR, YR, SR, AR) == 1:
#         print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
#         targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
#         print("Подсчет целевой функции для правого вставления ", targetR)
#     else:
#         targetR = -1
#         print("ERROR from Relocate: не получилось переставить, что-то пошло нет")
#
#     print("Теперь ищем минимум из двух целевых")
#     minimum = min(targetL, targetR)
#     if minimum == targetL and minimum != -1:
#         print("Выбрали левого у него целевая меньше")
#         iteration += 2
#         return Xl, Yl, Sl, Al, targetL, sizeK, iteration
#
#     elif minimum == targetR and minimum != -1:
#         print("Выбрали правого у него целевая меньше")
#         iteration += 2
#         return XR, YR, SR, AR, targetR, sizeK, iteration
#
#     else:
#         print("Все пошло по пизде ничего не сохранили")
#         return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK, iteration
#
#
# def Two_Opt(X, Y, Sresh, A, target_function_start, sizeK_start, iteration):
#     file = open("log/twooptlog.txt", 'a')
#     file.write("->Two_Opt start" + '\n')
#
#     SaveRelocate(X, Y, Sresh, A, sizeK_start)
#     TargetFunction = target_function_start
#     SizeK = sizeK_start
#     buf_targ = 0
#
#     while TargetFunction != buf_targ:
#         buf_targ = TargetFunction
#         X, Y, Sresh, A = ReadRelocateOfFile(SizeK)
#
#         # Bыбираем клиента
#         client1 = random.randint(1, (
#                 factory.N - 1))  # Берем рандомного клиента -1 потому что иногда может появится 10, а это выход за граници
#         sosed1 = SearchSosedLeftOrRight(X, Y, client1, "right")  # правый сосед клиента
#
#         file.write("Меняем продолжение клиентa " + str(client1) + '\n')
#         file.write("на машине " + str(NumberCarClienta(Y, client1)) + '\n')
#
#         for client2 in range(1, factory.N):
#             if client1 != client2:
#                 sosed2 = SearchSosedLeftOrRight(X, Y, client2, "right")  # правый сосед клиента
#                 sosedK = NumberCarClienta(Y, client2)
#
#                 file.write("На продолжение соседа два " + str(sosed2) + '\n')
#                 file.write("А клиенту два" + str(client2) + " продолжение сосед один " + str(sosed1) + '\n')
#                 file.write("На машине " + str(sosedK) + '\n')
#
#                 x, y, s, a, target_function, sizeK, iteration = OperatorJoinFromTwoOpt(X, Y, Sresh, A, SizeK, client1,
#                                                                                        client2,
#                                                                                        sosed1, sosed2, iteration)
#                 file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')
#
#                 file.write("Выбираем минимальное решение" + '\n')
#                 minimum = min(TargetFunction, target_function)
#                 if minimum == target_function:
#                     file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
#                     file.write("Новая целевая функция равна " + str(target_function) + '\n')
#                     SaveRelocate(x, y, s, a, sizeK)
#                     TargetFunction = target_function
#                     SizeK = sizeK
#                 elif minimum == TargetFunction:
#                     file.write("Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
#                     file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')
#
#     file.write("Локальный оптимум найден сохраняем в популяцию решение")
#     for i in range(factory.N):
#         for j in range(factory.N):
#             for k in range(sizeK):
#                 file.write(str(X[i][j][k]) + ' ')
#             file.write("\n")
#
#     X, Y, Sresh, A = ReadRelocateOfFile(SizeK)
#
#     file.write("<->Two_Opt stop" + '\n')
#     file.close()
#
#     return X, Y, Sresh, A, TargetFunction, SizeK, iteration


# Возможность приезжать нескольким машинам на одну локацию
def Help(X, Y, Sresh, A, target_function_start, sizeK_start):
    file = open("log/helog.txt", 'w')
    file.write("->Help start" + '\n')

    SaveStartSolution(X, Y, Sresh, A)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    iteration = 1
    file.write("Число используемых машин на начальном этапе " + str(AmountCarUsed(Y)) + '\n')
    while target_function_start != buf_targ:
        buf_targ = target_function_start
        iteration += 1

        for car in range(sizeK_start):
            if CountObjInCar(Y, car) == 1:
                X, Y, Sresh, A = ReadStartSolutionOfFile(SizeK)
                TargetFunction = target_function_start
                SizeK = sizeK_start

                file.write("Беру номер машины равный " + str(car) + '\n')

                for sosed in range(sizeK_start):

                    if car != sosed:
                        file.write("И переставляю его к машине " + str(sosed) + '\n')

                        x, y, s, a, target_function, sizeK = OperatorJoinFromHelp(X, Y, Sresh, A, SizeK, car,
                                                                                  sosed)
                        file.write("Число используемых машин теперь " + str(AmountCarUsed(y)) + '\n')

                        file.write("Выбираем минимальное решение" + '\n')
                        minimum1 = min(TargetFunction, target_function)
                        if minimum1 == target_function:
                            file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                            file.write("Новая целевая функция равна " + str(target_function) + '\n')

                            SaveHelp(x, y, s, a, sizeK)
                            TargetFunction = target_function
                            SizeK = sizeK
                        else:
                            file.write("Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                            file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')

        file.write("Итоговый выбор минимального. " + str(iteration) + "-ый раз переставили" + '\n')

        X, Y, Sresh, A = ReadStartSolutionOfFile(sizeK_start)
        target_function_start = CalculationOfObjectiveFunction(X, PenaltyFunction(Y, Sresh, A, 1))
        file.write("Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

        x, y, s, a = ReadHelpOfFile(SizeK)
        target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1))
        file.write("Целевая функция последнего минимального переставления = " + str(target_function) + '\n')

        minimum2 = min(target_function_start, target_function)
        if minimum2 == target_function:
            file.write("Новое перемещение, лучше чем стартовое, сохраняем это решение" + '\n')
            file.write("Новая целевая функция равна " + str(target_function) + '\n')

            SaveStartSolution(x, y, s, a)
            target_function_start = target_function
            sizeK_start = SizeK
        else:
            file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
            file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')

    file.write("Локальный оптимум найден сохраняем в популяцию решение" + '\n')
    for k in range(sizeK_start):
        for i in range(factory.N):
            for j in range(factory.N):
                file.write(str(X[i][j][k]) + ' ')
            file.write("\n")
        file.write("\n")

    file.write("<-Help stop" + '\n')
    file.close()

    return X, Y, Sresh, A, target_function_start, sizeK_start


# Проверка на содержание скважин тех же объектов car у soseda
def IsContainWells(y, car, sosed):
    for i in range(factory.N):
        for j in range(factory.N):
            if y[i][car] == y[j][sosed] == 1:
                return True
    return False


# Возвращает номер объекта который обслуживает конкретная машина
def GetObjForCar(y, car):
    for i in range(1, factory.N):
        if y[i][car] == 1:
            return i


def OperatorJoinFromHelp(x, y, s, a, sizeK, car, sosedCar):
    print("Узнаем сколько скважин обслуживает машина ", sosedCar)
    if CountObjInCar(y, sosedCar) == 1:
        print("Соседская машина обслуживает один объект")

        client = GetObjForCar(y, car)
        print("Машина ", car, " обслуживает объект ", client)
        sosed = GetObjForCar(y, sosedCar)
        print("Машина ", sosedCar, " обслуживает объект ", sosed)

        Xl, Yl, Sl, Al = ReadStartSolutionOfFile(sizeK)
        XR, YR, SR, AR = ReadStartSolutionOfFile(sizeK)

        sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left")  # левый сосед соседа
        sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right")  # правый сосед соседа

        print("sosed_left = ", sosedLeft)
        print("sosed_right = ", sosedRight)

        print("Время окончание client = ", factory.l[client])
        print("Время окончание sosed = ", factory.l[sosed])
        print("Время окончание sosedLeft = ", factory.l[sosedLeft])
        print("Время окончание sosedRight = ", factory.l[sosedRight])

        # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
        # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
        try:
            print("Вставляем клиента к соседу справа")
            # машина соседа будет работать у клиента столько же
            SR[client][sosedCar] = SR[client][car]

            # Чтобы все корректно работало, сначала надо написать
            # новое время приезда и новое время работы, потом
            # удалить старое решение, и только потом заполнять Х и У
            XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client)
            XR[sosed][sosedRight][sosedCar] = 0
            XR[sosed][client][sosedCar] = 1
            XR[client][sosedRight][sosedCar] = 1
            YR[client][sosedCar] = 1  # тепреь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            AR = TimeOfArrival(XR, YR, SR)

        except IOError:
            print("Объект не удален")
            XR[sosed][sosedRight][sosedCar] = 1
            XR[sosed][client][sosedCar] = 0
            XR[client][sosedRight][sosedCar] = 0
            YR[client][sosedCar] = 0  # тепреь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            AR = TimeOfArrival(XR, YR, SR)

        try:
            print("Вставляем клиента к соседу слева")
            # машина соседа будет работать у клиента столько же
            Sl[client][sosedCar] = Sl[client][car]

            # Чтобы все корректно работало, сначала надонаписать
            # новое время приезда и новое время работы, потом
            # удалить старое решение, и только потом заполнять Х и У
            Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client)
            Xl[sosedLeft][sosed][sosedCar] = 0
            Xl[sosedLeft][client][sosedCar] = 1
            Xl[client][sosed][sosedCar] = 1
            Yl[client][sosedCar] = 1  # теперь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            Al = TimeOfArrival(Xl, Yl, Sl)

        except IOError:
            print("Объект не удален")
            Xl[sosedLeft][sosed][sosedCar] = 1
            Xl[sosedLeft][client][sosedCar] = 0
            Xl[client][sosed][sosedCar] = 0
            Yl[client][sosedCar] = 0  # теперь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            Al = TimeOfArrival(Xl, Yl, Sl)

        print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого")
        if window_time_up(Al, Sl, Yl) == 0:
            if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true") == 1:
                print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
                targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, 1))
                print("Подсчет целевой функции для левого вставления ", targetL)
            else:
                targetL = -1
                print(
                    "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
        elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al) == 1:
            print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
            targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, 1))
            print("Подсчет целевой функции для левого вставления ", targetL)
        else:
            targetL = -1
            print("ERROR from Relocate: не получилось переставить, что-то пошло нет")

        print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого")
        if window_time_up(AR, SR, YR) == 0:
            if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true") == 1:
                print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
                targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, 1))
                print("Подсчет целевой функции для правого вставления ", targetR)
            else:
                targetR = -1
                print(
                    "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
        elif VerificationOfBoundaryConditions(XR, YR, SR, AR) == 1:
            print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
            targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, 1))
            print("Подсчет целевой функции для правого вставления ", targetR)
        else:
            targetR = -1
            print("ERROR from Relocate: не получилось переставить, что-то пошло нет")

        print("Теперь ищем минимум из двух целевых")
        minimum = min(targetL, targetR)
        if minimum == targetL and minimum != -1:
            print("Выбрали левого у него целевая меньше")
            return Xl, Yl, Sl, Al, targetL, sizeK

        elif minimum == targetR and minimum != -1:
            print("Выбрали правого у него целевая меньше")
            return XR, YR, SR, AR, targetR, sizeK

        else:
            print("Все пошло по пизде ничего не сохранили")
            return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1)), sizeK

    elif CountObjInCar(y, sosedCar) > 1:
        print("Соседская машина обслуживает несколько объектов")
        if IsContainWells(y, car, sosedCar):
            for i in range(1, factory.N):
                # Ищем какую скважину обслуживает машина car
                if y[i][car] == 1 and y[i][sosedCar] == 1:
                    s[i][sosedCar] += s[i][car]
                    flag = RecursiaForTime(x, s, a, 0, sosedCar, 0)
                    if not flag:
                        print("ERROR from OperatorJoinFromHelp: Рекурсия по подсчету времени прибытия превысила счетчик")
                    DeleteClientaFromPath(x, y, s, a, i, car)
                    return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1)), sizeK

        elif not IsContainWells(y, car, sosedCar):
            # TODO Надо разсмотреть случай когда нет такого объекта у соседа, и у соседа больше одной скважины



# Cоздаем популяцию решений
def PopulationOfSolutions(Target_Function, SizeSolution, iteration):
    for n in range(factory.param_population):  # создаем популяцию решений в кол-ве param_population
        # Берем стартовое решение из файла, потому что какой-то пиздюк его испортил

        # TODO раскоментить
        name_oper = ['reloc', '2-Opt']
        oper = random.choice(name_oper)
        oper = 'reloc'
        X, Y, Sresh, A = ReadStartSolutionOfFile(SizeSolution[n])

        if oper == 'reloc':
            x, y, s, a, Target_Function[n], SizeSolution[n], iteration = Relocate(X, Y, Sresh, A, Target_Function[n],
                                                                                  SizeSolution[n],
                                                                                  iteration)
        # elif oper == '2-Opt':
        #     x, y, s, a, Target_Function[n], SizeSolution[n], iteration = Two_Opt(X, Y, Sresh, A, Target_Function[n],
        #                                                                          SizeSolution[n],
        #                                                                          iteration)

        print("\nРешение номер", n, "построено")
        print("_____________________________")

        SavePopulation(x, y, s, a)
    # iteration += 1
    print("Популяция создана и сохранена в файл!!")
    print("___________________________________________________________________________________________________________")

