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
        SR[client][sosedK] += SR[client][clientK]

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
        Sl[client][sosedK] += Sl[client][clientK]

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

    elif minimum == targetR and minimum != -1 and targetR != targetL:
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
    file.write("Help start: ->" + '\n')

    SaveStartSolution(X, Y, Sresh, A)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    iteration = 1
    file.write("Число используемых машин на начальном этапе " + str(AmountCarUsed(Y)) + '\n')
    while target_function_start != buf_targ:
        file.write("Начался while\n")

        buf_targ = target_function_start
        iteration += 1

        for car in range(sizeK_start):
            if CountObjInCar(Y, car) == 1:
                X, Y, Sresh, A = ReadStartSolutionOfFile(SizeK)
                TargetFunction = target_function_start
                SizeK = sizeK_start

                for sosed in range(sizeK_start):

                    if car != sosed:
                        file.write("Беру номер машины равный " + str(car) + '\n')
                        file.write("И переставляю его к машине " + str(sosed) + '\n')

                        x, y, s, a, target_function, sizeK = OperatorJoinFromHelp(X, Y, Sresh, A, SizeK, car,
                                                                                  sosed, target_function_start, file)
                        file.write("Число используемых машин теперь " + str(AmountCarUsed(y)) + '\n')

                        file.write("Выбираем минимальное решение из стартового и измененного" + '\n')
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
                        file.write('\n')

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


def OperatorJoinFromHelp(x, y, s, a, sizeK_start, car, sosedCar, target_function_start, file):
    file.write("OperatorJoinFromHelp start: ->\n")
    target_function = target_function_start
    sizeK = sizeK_start

    file.write("    Узнаем сколько скважин обслуживает машина " + str(sosedCar) + '\n')
    if CountObjInCar(y, sosedCar) == 1:
        file.write("    Соседская машина обслуживает один объект" + '\n')
        file.write("    Проверяем на совпадение объектов" + '\n')

        if not IsContainWells(y, car, sosedCar):
            file.write("Объекты не совпали" + '\n')

            client = GetObjForCar(y, car)
            file.write("Машина " + str(car) + " обслуживает объект " + str(client[0]) + '\n')
            sosed = GetObjForCar(y, sosedCar)
            file.write("Машина " + str(sosedCar) + " обслуживает объект " + str(sosed[0]) + '\n')

            Xl, Yl, Sl, Al = ReadStartSolutionOfFile(sizeK)
            XR, YR, SR, AR = ReadStartSolutionOfFile(sizeK)

            sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed[0], "left")  # левый сосед соседа
            sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed[0], "right")  # правый сосед соседа

            file.write("sosed_left = " + str(sosedLeft) + '\n')
            file.write("sosed_right = " + str(sosedRight) + '\n')

            file.write("Время окончание client = " + str(factory.l[client[0]]) + '\n')
            file.write("Время окончание sosed = " + str(factory.l[sosed[0]]) + '\n')
            file.write("Время окончание sosedLeft = " + str(factory.l[sosedLeft]) + '\n')
            file.write("Время окончание sosedRight = " + str(factory.l[sosedRight]) + '\n')

            # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
            # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
            try:
                file.write("Вставляем клиента к соседу справа" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client[0]][sosedCar] += SR[client[0]][car]

                # Чтобы все корректно работало, сначала надо написать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client[0])

                XR[sosed[0]][sosedRight][sosedCar] = 0
                XR[sosed[0]][client[0]][sosedCar] = 1
                XR[client[0]][sosedRight][sosedCar] = 1
                YR[client[0]][sosedCar] = 1  # тепреь машина соседа обслуживает клиента
                BeautifulPrint(XR, YR, SR, AR)

                # Подсчет времени приезда к клиенту от соседа
                # AR = TimeOfArrival(XR, YR, SR)
                flag = RecursiaForTime(XR, SR, AR, 0, sosedCar, 0)
                if not flag:
                    file.write(
                        "ERROR from OperatorJoinFromHelp: Рекурсия по подсчету времени прибытия превысила счетчик" + '\n')
                    file.write("OperatorJoinFromHelp stop: <-\n")
                    return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1)), sizeK

            except IOError:
                file.write("Объект не удален" + '\n')
                XR[sosed[0]][sosedRight][sosedCar] = 1
                XR[sosed[0]][client[0]][sosedCar] = 0
                XR[client[0]][sosedRight][sosedCar] = 0
                YR[client[0]][sosedCar] = 0  # тепреь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR)

            try:
                file.write("Вставляем клиента к соседу слева" + '\n')
                # машина соседа будет работать у клиента столько же
                Sl[client[0]][sosedCar] += Sl[client[0]][car]

                # Чтобы все корректно работало, сначала надонаписать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client[0])
                Xl[sosedLeft][sosed[0]][sosedCar] = 0
                Xl[sosedLeft][client[0]][sosedCar] = 1
                Xl[client[0]][sosed[0]][sosedCar] = 1
                Yl[client[0]][sosedCar] = 1  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                # Al = TimeOfArrival(Xl, Yl, Sl)
                flag = RecursiaForTime(Xl, Sl, Al, 0, sosedCar, 0)
                if not flag:
                    file.write(
                        "ERROR from OperatorJoinFromHelp: Рекурсия по подсчету времени прибытия превысила счетчик" + '\n')
                    file.write("OperatorJoinFromHelp stop: <-\n")
                    return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1)), sizeK

            except IOError:
                file.write("Объект не удален" + '\n')
                Xl[sosedLeft][sosed[0]][sosedCar] = 1
                Xl[sosedLeft][client[0]][sosedCar] = 0
                Xl[client[0]][sosed[0]][sosedCar] = 0
                Yl[client[0]][sosedCar] = 0  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                Al = TimeOfArrival(Xl, Yl, Sl)

            for k in range(sizeK):
                for i in range(factory.N):
                    print(Al[i][k], end=' ')
                print("\n")
            file.write("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого" + '\n')
            if window_time_up(Al, Sl, Yl) == 0:
                if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true") == 1:
                    file.write("NOTIFICATION from Relocate: вставили с нарушением временного окна" + '\n')
                    targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, 1))
                    file.write("Подсчет целевой функции для левого вставления " + str(targetL) + '\n')
                else:
                    targetL = -1
                    file.write(
                        "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
            elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al) == 1:
                file.write("NOTIFICATION from Relocate: вставили без нарушений ограничений" + '\n')
                targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, 1))
                file.write("Подсчет целевой функции для левого вставления " + str(targetL) + '\n')
            else:
                targetL = -1
                file.write("ERROR from Relocate: не получилось переставить, что-то пошло нет" + '\n')

            file.write("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого" + '\n')
            if window_time_up(AR, SR, YR) == 0:
                if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true") == 1:
                    file.write("NOTIFICATION from Relocate: вставили с нарушением временного окна" + '\n')
                    targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, 1))
                    file.write("Подсчет целевой функции для правого вставления " + str(targetR) + '\n')
                else:
                    targetR = -1
                    file.write(
                        "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
            elif VerificationOfBoundaryConditions(XR, YR, SR, AR) == 1:
                file.write("NOTIFICATION from Relocate: вставили без нарушений ограничений" + '\n')
                targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, 1))
                file.write("Подсчет целевой функции для правого вставления " + str(targetR) + '\n')
            else:
                targetR = -1
                file.write("ERROR from Relocate: не получилось переставить, что-то пошло нет" + '\n')

            file.write("Теперь ищем минимум из двух целевых" + '\n')
            minimum = min(targetL, targetR)
            if minimum == targetL and minimum != -1:
                file.write("Выбрали левого у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return Xl, Yl, Sl, Al, targetL, sizeK

            elif minimum == targetR and minimum != -1:
                file.write("Выбрали правого у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return XR, YR, SR, AR, targetR, sizeK

            else:
                file.write("Все пошло по пизде ничего не сохранили" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1)), sizeK

        elif IsContainWells(y, car, sosedCar):
            file.write("    Объекты совпали" + '\n')

            client = GetObjForCar(y, car)
            file.write("    Машина " + str(car) + " обслуживает объект " + str(client[0]) + '\n')
            sosed = GetObjForCar(y, sosedCar)
            file.write("    Машина " + str(sosedCar) + " обслуживает объект " + str(sosed[0]) + '\n')

            X, Y, S, A = ReadStartSolutionOfFile(sizeK)

            # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
            # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
            try:
                file.write("    Передаем скважину машине, которая обслуживает этот же объект " + '\n')
                # машина соседа будет работать у клиента столько же
                S[sosed[0]][sosedCar] += S[client[0]][car]

                # Чтобы все корректно работало, сначала надо написать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                X, Y, S, A = DeleteClientaFromPath(X, Y, S, A, client[0])

                # Подсчет времени приезда к клиенту от соседа
                A[0][sosedCar] = A[sosed[0]][sosedCar] + S[sosed[0]][sosedCar] + factory.t[sosed[0]][0]

            except IOError:
                file.write("    Объект не удален" + '\n')
                S[client[0]][sosedCar] -= 2
                S[client[0]][car] += 2

                X[0][client[0]][car] = 1
                X[client[0]][0][car] = 0
                Y[client[0]][car] = 0  # тепреь машина соседа обслуживает клиента
                A[client[0]][car] = 0 + S[client[0]][car] + factory.t[0][client[0]]
                A[0][car] = A[client[0]][car] + S[client[0]][car] + factory.t[client[0]][0]

            file.write("    СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ" + '\n')
            if window_time_up(A, S, Y) == 0:
                if VerificationOfBoundaryConditions(X, Y, S, A, "true") == 1:
                    file.write("    NOTIFICATION from Help: вставили с нарушением временного окна" + '\n')
                    target = CalculationOfObjectiveFunction(X, PenaltyFunction(Y, S, A, 1))
                    file.write("    Подсчет измененной целевой функции  " + str(target) + '\n')
                else:
                    target = -1
                    file.write(
                        "   ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
            elif VerificationOfBoundaryConditions(X, Y, S, A) == 1:
                file.write("    NOTIFICATION from Help: вставили без нарушений ограничений" + '\n')
                target = CalculationOfObjectiveFunction(X, PenaltyFunction(Y, S, A, 1))
                file.write("    Подсчет измененной целевой функции " + str(target) + '\n')
            else:
                target = -1
                file.write("    ERROR from Relocate: не получилось переставить, что-то пошло нет" + '\n')

            file.write("    А стартовая целевая функция = " + str(target_function_start) + '\n')
            file.write("    Теперь ищем минимум из двух целевых" + '\n')
            minimum = min(target_function, target)
            if minimum == target_function:
                file.write("    Выбрали стартовое решение у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, target_function_start, sizeK_start

            elif minimum == target and minimum != -1:
                file.write("    Выбрали измененное у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return X, Y, S, A, target, sizeK

            else:
                file.write("    Все пошло по пизде ничего не сохранили" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1)), sizeK

    elif CountObjInCar(y, sosedCar) > 1:
        X, Y, Sresh, A = ReadStartSolutionOfFile(sizeK)

        file.write("    Соседская машина обслуживает несколько объектов" + '\n')
        if IsContainWells(Y, car, sosedCar):
            file.write("    У машины " + str(car) + " есть такой же объект как у машины " + str(sosedCar) + '\n')
            for i in range(1, factory.N):
                # Ищем какую скважину обслуживает машина car
                if Y[i][car] == 1 and Y[i][sosedCar] == 1:
                    Sresh[i][sosedCar] += Sresh[i][car]
                    flag = RecursiaForTime(X, Sresh, A, 0, sosedCar, 0)
                    if not flag:
                        file.write(
                            "   ERROR from OperatorJoinFromHelp: Рекурсия по подсчету времени прибытия превысила "
                            "счетчик" + '\n')
                        file.write("OperatorJoinFromHelp stop: <-\n")
                        return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1)), sizeK

                    DeleteClientaFromPath(X, Y, Sresh, A, i, car)
                    file.write("OperatorJoinFromHelp stop: <-\n")
                    return X, Y, Sresh, A, CalculationOfObjectiveFunction(X, PenaltyFunction(Y, Sresh, A, 1)), sizeK

        elif not IsContainWells(Y, car, sosedCar):
            flag = 0
            file.write("    У машины " + str(car), " нет такого же объекта как у машины " + str(sosedCar) + '\n')

            client = GetObjForCar(Y, car)
            sosed = GetObjForCar(Y, sosedCar)
            file.write("    Машина " + str(car) + " обслуживает объект " + str(client[0]))
            file.write("    Машина " + str(sosedCar) + " обслуживает объекты " + str(sosed))

            for i in range(len(sosed)):
                file.write("    Переставляем скважину с объекта " + str(client[0]) + " на машине " + str(car) + '\n')
                file.write("    К объекту " + str(sosed[i]) + '\n')
                file.write("    На машине " + str(sosedCar) + '\n')

                X, Y, Sresh, A, TargetFunction, SizeK, iteration = OperatorJoinFromReloc(x, y, s, a, sizeK, client[0],
                                                                                         sosed[i], 1)
                file.write("    Число используемых машин " + str(SizeK) + '\n')

                file.write("    Выбираем минимальное решение" + '\n')
                minimum = min(TargetFunction, target_function)
                if minimum == TargetFunction:
                    file.write("    Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                    file.write("    Новая целевая функция равна " + str(target_function) + '\n')

                    SaveRelocate(X, Y, Sresh, A, SizeK)
                    target_function = TargetFunction
                    sizeK = SizeK
                    flag = 1
                else:
                    file.write("    Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                    file.write("    Старая целевая функция равна " + str(target_function) + '\n')

            if flag == 1:
                file.write("    Локальный оптимум найден сохраняем в популяцию решение" + '\n')
                X, Y, Sresh, A = ReadRelocateOfFile(sizeK)
                for k in range(sizeK):
                    for i in range(factory.N):
                        for j in range(factory.N):
                            file.write(str(X[i][j][k]) + ' ')
                        file.write("\n")
                    file.write("\n")

                file.write("OperatorJoinFromHelp stop: <-\n")
                return X, Y, Sresh, A, target_function, sizeK
            else:
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, target_function_start, sizeK_start


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
