from function import *


# вклиниваем между
def OperatorJoinFromReloc(x, y, s, a, sizeK, client, sosed, iteration, file):
    Xl, Yl, Sl, Al = ReadLocalSearchOfFile(sizeK)
    XR, YR, SR, AR = ReadLocalSearchOfFile(sizeK)

    sosedK = NumberCarClienta(Yl, sosed)
    clientK = NumberCarClienta(Yl, client)

    sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left")  # левый сосед соседа
    sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right")  # правый сосед соседа

    file.write("sosed_left = " + str(sosedLeft) + '\n')
    file.write("sosed_right = " + str(sosedRight) + '\n')

    file.write("Время окончание client = " + str(factory.l[client]) + '\n')
    file.write("Время окончание sosed = " + str(factory.l[sosed]) + '\n')
    file.write("Время окончание sosedLeft = " + str(factory.l[sosedLeft]) + '\n')
    file.write("Время окончание sosedRight = " + str(factory.l[sosedRight]) + '\n')

    # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
    # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
    try:
        file.write("Вставляем клиента к соседу справа" + '\n')
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
        AR = TimeOfArrival(XR, YR, SR, file)

    except IOError:
        file.write("Объект не удален" + '\n')
        XR[sosed][sosedRight][sosedK] = 1
        XR[sosed][client][sosedK] = 0
        XR[client][sosedRight][sosedK] = 0
        YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        AR = TimeOfArrival(XR, YR, SR, file)

    try:
        file.write("Вставляем клиента к соседу слева" + '\n')
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
        Al = TimeOfArrival(Xl, Yl, Sl, file)

    except IOError:
        file.write("Объект не удален" + '\n')
        Xl[sosedLeft][sosed][sosedK] = 1
        Xl[sosedLeft][client][sosedK] = 0
        Xl[client][sosed][sosedK] = 0
        Yl[client][sosedK] = 0  # теперь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        Al = TimeOfArrival(Xl, Yl, Sl, file)

    file.write("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого" + '\n')
    if window_time_up(Al, Sl, Yl, file) == 0:
        if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true", file) == 1:
            file.write("NOTIFICATION from Relocate: вставили с нарушением временного окна" + '\n')
            targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
            file.write("Подсчет целевой функции для левого вставления " + str(targetL) + '\n')
        else:
            targetL = -1
            file.write(
                "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
    elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "false", file) == 1:
        file.write("NOTIFICATION from Relocate: вставили без нарушений ограничений" + '\n')
        targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
        file.write("Подсчет целевой функции для левого вставления " + str(targetL) + '\n')
    else:
        targetL = -1
        file.write("ERROR from Relocate: не получилось переставить, что-то пошло нет" + '\n')

    file.write("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого" + '\n')
    if window_time_up(AR, SR, YR, file) == 0:
        if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true", file) == 1:
            file.write("NOTIFICATION from Relocate: вставили с нарушением временного окна" + '\n')
            targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
            file.write("Подсчет целевой функции для правого вставления " + str(targetR) + '\n')
        else:
            targetR = -1
            file.write(
                "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
    elif VerificationOfBoundaryConditions(XR, YR, SR, AR, "false", file) == 1:
        file.write("NOTIFICATION from Relocate: вставили без нарушений ограничений" + '\n')
        targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
        file.write("Подсчет целевой функции для правого вставления " + str(targetR) + '\n')
    else:
        targetR = -1
        file.write("ERROR from Relocate: не получилось переставить, что-то пошло нет" + '\n')

    file.write("Теперь ищем минимум из двух целевых" + '\n')
    minimum = min(targetL, targetR)
    if minimum == targetL and minimum != -1:
        file.write("Выбрали левого у него целевая меньше" + '\n')
        return Xl, Yl, Sl, Al, targetL, sizeK, iteration

    elif minimum == targetR and minimum != -1 and targetR != targetL:
        file.write("Выбрали правого у него целевая меньше" + '\n')
        return XR, YR, SR, AR, targetR, sizeK, iteration

    else:
        file.write("Все пошло по пизде ничего не сохранили" + '\n')
        return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK, iteration


# переставляем клиента к новому соседу, локальный поиск
def Relocate(X, Y, Sresh, A, target_function_start, sizeK_start, iteration):
    file = open("log/relog.txt", 'w')
    file.write("->Relocate start" + '\n')

    SaveLocalSearch(X, Y, Sresh, A, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    while TargetFunction != buf_targ:
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadLocalSearchOfFile(SizeK)

        # Bыбираем клиента
        client = random.randint(1, (
                factory.N - 1))  # Берем рандомного клиента -1 потому что иногда может появится 10, а это выход за граници
        # TODO надо поменять поиск машины
        file.write("Переставляем клиентa " + str(client) + '\n')
        file.write("С машины" + str(NumberCarClienta(Y, client)) + '\n')

        for sosed in range(1, factory.N):

            if client != sosed:
                sosedK = NumberCarClienta(Y, sosed)

                file.write("К соседу " + str(sosed) + '\n')
                file.write("На машине " + str(sosedK) + '\n')

                x, y, s, a, target_function, sizeK, iteration = OperatorJoinFromReloc(X, Y, Sresh, A, SizeK, client,
                                                                                      sosed, iteration, file)
                file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                file.write("Выбираем минимальное решение" + '\n')
                minimum = min(TargetFunction, target_function)
                if minimum == target_function:
                    file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                    file.write("Новая целевая функция равна " + str(target_function) + '\n')

                    SaveLocalSearch(x, y, s, a, sizeK)
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

    X, Y, Sresh, A = ReadLocalSearchOfFile(SizeK)

    file.write("<-Relocate stop" + '\n')
    file.close()

    return X, Y, Sresh, A, TargetFunction, SizeK, iteration


def OperatorJoinFromTwoOpt(X, Y, Sresh, A, SizeK, client1, client1Car, client2, client2Car, iteration):
    Xl, Yl, Sl, Al = ReadLocalSearchOfFile(sizeK)
    XR, YR, SR, AR = ReadLocalSearchOfFile(sizeK)

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
        AR = TimeOfArrival(XR, YR, SR, file)

    except IOError:
        print("Объект не удален")
        XR[sosed][sosedRight][sosedK] = 1
        XR[sosed][client][sosedK] = 0
        XR[client][sosedRight][sosedK] = 0
        YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        AR = TimeOfArrival(XR, YR, SR, file)

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
        Al = TimeOfArrival(Xl, Yl, Sl, file)

    except IOError:
        print("Объект не удален")
        Xl[sosedLeft][sosed][sosedK] = 1
        Xl[sosedLeft][client][sosedK] = 0
        Xl[client][sosed][sosedK] = 0
        Yl[client][sosedK] = 0  # теперь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        Al = TimeOfArrival(Xl, Yl, Sl, file)

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
        iteration += 2
        return Xl, Yl, Sl, Al, targetL, sizeK, iteration

    elif minimum == targetR and minimum != -1:
        print("Выбрали правого у него целевая меньше")
        iteration += 2
        return XR, YR, SR, AR, targetR, sizeK, iteration

    else:
        print("Все пошло по пизде ничего не сохранили")
        return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK, iteration


def Two_Opt(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration):
    file = open("log/twooptlog.txt", 'a')
    file.write("Two_Opt start: ->" + '\n')

    SaveLocalSearch(x_start, y_start, s_start, a_start, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    while TargetFunction != buf_targ:
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadLocalSearchOfFile(SizeK)

        # Bыбираем клиента
        client1, client1Car = ChooseRandomObjAndCar(Y, SizeK)

        file.write("Меняем продолжение клиентa " + str(client1) + '\n')
        file.write("на машине " + str(client1Car) + '\n')

        for client2Car in range(SizeK):
            if client2Car != client1Car:
                for client2 in range(1, factory.N):
                    file.write("У маршрутов " + str(client1Car) + str(client2Car) + " меняем хвосты\n Начиная с "
                                "объектов " + str(client1) + " и " + str(client2) + " соответствено\n")

                    x, y, s, a, target_function, sizeK, iteration = OperatorJoinFromTwoOpt(X, Y, Sresh, A, SizeK,
                                                                                           client1, client1Car,
                                                                                           client2, client2Car,
                                                                                           iteration)
                    file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                    file.write("Выбираем минимальное решение" + '\n')
                    minimum = min(TargetFunction, target_function)
                    if minimum == target_function:
                        file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                        file.write("Новая целевая функция равна " + str(target_function) + '\n')
                        SaveLocalSearch(x, y, s, a, sizeK)
                        TargetFunction = target_function
                        SizeK = sizeK
                    else:
                        file.write("Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                        file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')

    X, Y, Sresh, A = ReadLocalSearchOfFile(SizeK)

    file.write("Локальный оптимум найден сохраняем в популяцию решение\n")
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(SizeK):
                file.write(str(X[i][j][k]) + ' ')
            file.write("\n")

    file.write("Two_Opt stop: <-" + '\n')
    file.close()

    return X, Y, Sresh, A, TargetFunction, SizeK, iteration


# Возможность приезжать нескольким машинам на одну локацию
def Help(Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start, iteration):
    file = open("log/helog.txt", 'w')
    file.write("Help start: ->" + '\n')

    SaveStartHelp(Xstart, Ystart, Sstart, Astart, sizeK_start)

    file.write("Начинаем поиск объектов, которые в маршруте не успевают закончить работу\n")
    fileflag = 0
    for k in range(sizeK_start):
        for client in range(1, factory.N):
            if Ystart[client][k] == 1:
                if Astart[client][k] + Sstart[client][k] > factory.l[client]:
                    file.write("Нашли объект который опаздывает " + str(client) + " который обслуживает машина " + str(
                        k) + '\n')
                    contWells = CountWellsWithFane(Sstart, Astart, client, k)
                    file.write("Всего не укладывается " + str(contWells) + " скважин\n")

                    for proebSkv in range(contWells):
                        X, Y, Sresh, A = ReadStartHelpOfFile(sizeK_start)
                        TargetFunction = target_function_start
                        SizeK = sizeK_start

                        flag = 0
                        if factory.S[client] / factory.wells[client] > 0:
                            flag = 'not the last'
                        elif factory.S[client] / factory.wells[client] == 0:
                            flag = 'last'
                        else:
                            flag = 'end'

                        if flag != 'end':
                            file.write("Сейчас " + flag + " скважина\n")
                            file.write("Начинаем цикл по присовыванию везде (по машинам)\n")
                            for sosedK in range(sizeK_start):
                                if sosedK != k:
                                    file.write("Сейчас рассматриваем " + str(sosedK) + " машину\n")
                                    file.write("Она не похожа на ту из которой взяли скважину\n")

                                    file.write("Начинаем цикл по объектам в этой машине\n")
                                    for sosed in range(1, factory.N):
                                        if Y[sosed][sosedK] == 1:
                                            file.write("Рассматриваемый объект " + str(sosed) + "\n")
                                            file.write(
                                                "Попробую одну скважину с объекта " + str(client) + " и машины " + str(
                                                    k) + "\n")
                                            file.write(" отдать машине " + str(sosedK) + " рядом с объектом " + str(
                                                sosed) + "\n")

                                            x, y, s, a, target_function, sizeK = OperatorJoinFromHelp(X, Y, Sresh, A,
                                                                                                      SizeK,
                                                                                                      client, k, sosed,
                                                                                                      sosedK,
                                                                                                      TargetFunction,
                                                                                                      iteration, flag,
                                                                                                      file)
                                            file.write(
                                                "Число используемых машин теперь " + str(AmountCarUsed(y)) + '\n')

                                            file.write(
                                                "Выбираем минимальное решение из стартового и измененного" + '\n')
                                            minimum1 = min(TargetFunction, target_function)
                                            if minimum1 == target_function:
                                                file.write(
                                                    "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                file.write("Новая целевая функция равна " + str(target_function) + '\n')

                                                SaveHelp(x, y, s, a, sizeK)
                                                TargetFunction = target_function
                                                SizeK = sizeK
                                                fileflag = 1
                                            else:
                                                file.write("Новое перемещение, хуже чем то что было, возвращаем наше "
                                                           "старое решение" + '\n')
                                                file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')
                                            file.write('\n')

                        Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile(sizeK_start)
                        target_function_start = CalculationOfObjectiveFunction(Xstart, PenaltyFunction(Ystart, Sstart,
                                                                                                       Astart, 1))
                        file.write(
                            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

                        if fileflag == 1:
                            x, y, s, a = ReadHelpOfFile(SizeK)
                            target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1))
                            file.write(
                                "Целевая функция последнего минимального переставления = " + str(
                                    target_function) + '\n')
                            fileflag = 0
                        else:
                            target_function = -1

                        minimum2 = min(target_function_start, target_function)
                        if minimum2 == target_function and target_function != -1:
                            file.write("Новое перемещение, лучше чем стартовое, сохраняем это решение" + '\n')
                            file.write("Новая целевая функция равна " + str(target_function) + '\n')

                            SaveStartHelp(x, y, s, a, SizeK)
                            target_function_start = target_function
                            sizeK_start = SizeK
                        else:
                            file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
                            file.write("Старая целевая функция равна " + str(target_function_start) + '\n')
                            return Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start

    file.write("По максимуму постарались поделиться скважинами" + '\n')
    Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile(sizeK_start)
    for k in range(sizeK_start):
        for i in range(factory.N):
            for j in range(factory.N):
                file.write(str(Xstart[i][j][k]) + ' ')
            file.write("\n")
        file.write("\n")

    file.write("<-Help stop" + '\n')
    file.close()

    return Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start


def OperatorJoinFromHelp(x, y, s, a, sizeK_start, client, clientCar, sosed, sosedCar, target_function_start, iteration,
                         flag, file):
    file.write("OperatorJoinFromHelp start: ->\n")
    target_function = target_function_start
    sizeK = sizeK_start

    file.write("    Проверяем на равенство клиента и соседа\n")
    if client == sosed:
        file.write("    Равны\n")
        X, Y, Sresh, A = ReadStartHelpOfFile(sizeK)

        file.write("    Время работы до забирания скважины " + str(Sresh[client][clientCar]) + "\n")
        Sresh[client][clientCar] -= factory.S[client] / factory.wells[client]
        file.write("    Время работы после забирания скважины " + str(Sresh[client][clientCar]) + "\n")

        Sresh[sosed][sosedCar] += factory.S[client] / factory.wells[client]
        if flag == 'last':
            file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                       "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
            X, Y, Sresh, A = DeleteClientaFromPath(X, Y, Sresh, A, client)

        A = TimeOfArrival(X, Y, Sresh, file)

        file.write("    СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ" + '\n')
        if window_time_up(A, Sresh, Y, file) == 0:
            if VerificationOfBoundaryConditions(X, Y, Sresh, A, "true", file) == 1:
                file.write("    NOTIFICATION from Help: вставили с нарушением временного окна" + '\n')
                target_function = CalculationOfObjectiveFunction(X, PenaltyFunction(Y, Sresh, A, iteration))
                file.write("    Подсчет целевой функции после вставления " + str(target_function) + '\n')
                file.write("    OperatorJoinFromHelp stop: <-\n")
                return X, Y, Sresh, A, target_function, sizeK
            else:
                file.write(
                    "   ERROR from Help: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
                file.write("    OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, target_function_start, sizeK_start

        elif VerificationOfBoundaryConditions(X, Y, Sresh, A, "false", file) == 1:
            file.write("    NOTIFICATION from Help: вставили без нарушений ограничений" + '\n')
            target_function = CalculationOfObjectiveFunction(X, PenaltyFunction(Y, Sresh, A, iteration))
            file.write("    Подсчет целевой функции после вставления " + str(target_function) + '\n')
            file.write("    OperatorJoinFromHelp stop: <-\n")
            return X, Y, Sresh, A, target_function, sizeK
        else:
            file.write("    ERROR from Help: не получилось переставить, что-то пошло нет" + '\n')
            file.write("    OperatorJoinFromHelp stop: <-\n")
            return x, y, s, a, target_function_start, sizeK_start

    if not IsContainWells(y, client, sosedCar):
        file.write("    Не равны\n")
        Xl, Yl, Sl, Al = ReadStartHelpOfFile(sizeK)
        XR, YR, SR, AR = ReadStartHelpOfFile(sizeK)

        file.write("    Время работы до забирания скважины " + str(Sl[client][clientCar]) + "\n")
        file.write("    Забираем проебанную скважину\n")
        Sl[client][clientCar] -= factory.S[client] / factory.wells[client]
        SR[client][clientCar] -= factory.S[client] / factory.wells[client]
        file.write("    Время работы после забирания скважины " + str(Sl[client][clientCar]) + "\n")

        sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left", sosedCar)  # левый сосед соседа
        sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right", sosedCar)  # правый сосед соседа

        file.write("    sosed_left = " + str(sosedLeft) + '\n')
        file.write("    sosed_right = " + str(sosedRight) + '\n')

        file.write("    Время окончание client = " + str(factory.l[client]) + '\n')
        file.write("    Время окончание sosed = " + str(factory.l[sosed]) + '\n')
        file.write("    Время окончание sosedLeft = " + str(factory.l[sosedLeft]) + '\n')
        file.write("    Время окончание sosedRight = " + str(factory.l[sosedRight]) + '\n')

        # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
        # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
        try:
            file.write("    Вставляем скважину к соседу справа" + '\n')
            # машина соседа будет работать у клиента столько же
            SR[client][sosedCar] += factory.S[client] / factory.wells[client]

            # на случай если мы в итоге все скважины забрали, и эта была последняя
            if flag == 'last':
                file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                           "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client)

            XR[sosed][client][sosedCar] = 1
            if client != sosedRight:
                file.write("    Сосед справа не равен клиенту\n")
                XR[client][sosedRight][sosedCar] = 1
            YR[client][sosedCar] = 1  # тепреь машина соседа обслуживает клиента
            XR[sosed][sosedRight][sosedCar] = 0

            # Подсчет времени приезда к клиенту от соседа
            AR = TimeOfArrival(XR, YR, SR, file)

        except IOError:
            file.write("    Объект не удален" + '\n')
            XR[sosed][sosedRight][sosedCar] = 1
            XR[sosed][client][sosedCar] = 0
            XR[client][sosedRight][sosedCar] = 0
            YR[client][sosedCar] = 0  # тепреь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            AR = TimeOfArrival(XR, YR, SR, file)

        try:
            file.write("    Вставляем клиента к соседу слева" + '\n')
            # машина соседа будет работать у клиента столько же
            Sl[client][sosedCar] += factory.S[client] / factory.wells[client]

            # на случай если мы в итоге все скважины забрали, и эта была последняя
            if flag == 'last':
                file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                           "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client)

            Xl[sosedLeft][sosed][sosedCar] = 0
            if sosedLeft != client:
                Xl[sosedLeft][client][sosedCar] = 1
            Xl[client][sosed][sosedCar] = 1
            Yl[client][sosedCar] = 1  # теперь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            Al = TimeOfArrival(Xl, Yl, Sl, file)

        except IOError:
            file.write("    Объект не удален")
            Xl[sosedLeft][sosed][sosedCar] = 1
            Xl[sosedLeft][client][sosedCar] = 0
            Xl[client][sosed][sosedCar] = 0
            Yl[client][sosedCar] = 0  # теперь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            Al = TimeOfArrival(Xl, Yl, Sl, file)

        file.write("    СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого" + '\n')
        if window_time_up(Al, Sl, Yl, file) == 0:
            if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true", file) == 1:
                file.write("    NOTIFICATION from Help: вставили с нарушением временного окна" + '\n')
                targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
                file.write("    Подсчет целевой функции для левого вставления " + str(targetL) + '\n')
            else:
                targetL = -1
                file.write(
                    "   ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
        elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "false", file) == 1:
            file.write("    NOTIFICATION from Help: вставили без нарушений ограничений" + '\n')
            targetL = CalculationOfObjectiveFunction(Xl, PenaltyFunction(Yl, Sl, Al, iteration))
            file.write("    Подсчет целевой функции для левого вставления " + str(targetL) + '\n')
        else:
            targetL = -1
            file.write("    ERROR from Help: не получилось переставить, что-то пошло нет" + '\n')

        file.write("    СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого" + '\n')
        if window_time_up(AR, SR, YR, file) == 0:
            if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true", file) == 1:
                file.write("    NOTIFICATION from Help: вставили с нарушением временного окна" + '\n')
                targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
                file.write("    Подсчет целевой функции для правого вставления " + str(targetR) + '\n')
            else:
                targetR = -1
                file.write(
                    "   ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено" + '\n')
        elif VerificationOfBoundaryConditions(XR, YR, SR, AR, "false", file) == 1:
            file.write("    NOTIFICATION from Help: вставили без нарушений ограничений" + '\n')
            targetR = CalculationOfObjectiveFunction(XR, PenaltyFunction(YR, SR, AR, iteration))
            file.write("    Подсчет целевой функции для правого вставления " + str(targetR) + '\n')
        else:
            targetR = -1
            file.write("    ERROR from Help: не получилось переставить, что-то пошло нет" + '\n')

        file.write("    Теперь ищем минимум из двух целевых" + '\n')
        minimum = min(targetL, targetR)
        if minimum == targetL and minimum != -1:
            file.write("    Выбрали левого у него целевая меньше" + '\n')
            file.write("OperatorJoinFromHelp stop: <-\n")
            return Xl, Yl, Sl, Al, targetL, sizeK

        elif minimum == targetR and minimum != -1 and targetR != targetL:
            file.write("    Выбрали правого у него целевая меньше" + '\n')
            file.write("OperatorJoinFromHelp stop: <-\n")
            return XR, YR, SR, AR, targetR, sizeK

        else:
            file.write("    Все пошло по пизде ничего не сохранили" + '\n')
            file.write("OperatorJoinFromHelp stop: <-\n")
            return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK

    file.write("    В этом маршруте есть такой объек, вернемся к нему позже\n")
    file.write("OperatorJoinFromHelp stop: <-\n")
    return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK


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
