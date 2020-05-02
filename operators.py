from function import *


# вклиниваем между
def OperatorJoinFromReloc(x, y, s, a, sizeK, client, clientK, sosed, sosedK, iteration, file):
    if client != sosed:
        Xl, Yl, Sl, Al = ReadStartLocalSearchOfFile(sizeK)
        XR, YR, SR, AR = ReadStartLocalSearchOfFile(sizeK)

        sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left", sosedK)  # левый сосед соседа
        sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right", sosedK)  # правый сосед соседа

        file.write("sosed_left = " + str(sosedLeft) + '\n')
        file.write("sosed_right = " + str(sosedRight) + '\n')

        file.write("Время окончание client = " + str(factory.l[client]) + '\n')
        file.write("Время окончание sosed = " + str(factory.l[sosed]) + '\n')
        file.write("Время окончание sosedLeft = " + str(factory.l[sosedLeft]) + '\n')
        file.write("Время окончание sosedRight = " + str(factory.l[sosedRight]) + '\n')

        # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
        # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
        if sosedRight != -1:
            try:
                file.write("Вставляем клиента к соседу справа" + '\n')
                # машина соседа будет работать у клиента столько же
                if sosedK != clientK:
                    SR[client][sosedK] += SR[client][clientK]
                else:
                    buf = SR[client][clientK]

                # Чтобы все корректно работало, сначала надо написать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientK)
                if sosedK == clientK:
                    SR[client][sosedK] += buf
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
        if sosedLeft != -1:
            try:
                file.write("Вставляем клиента к соседу слева" + '\n')
                # машина соседа будет работать у клиента столько же
                if sosedK != clientK:
                    Sl[client][sosedK] += Sl[client][clientK]
                else:
                    buf = Sl[client][clientK]

                # Чтобы все корректно работало, сначала надонаписать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client, clientK)
                if sosedK == clientK:
                    Sl[client][sosedK] += buf
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

        if sosedLeft != -1 and sosedRight != -1:
            try:
                Xl, Yl, Sl, Al, targetL, sizeK = Checker(Xl, Yl, Sl, Al, sizeK, iteration, "Relocate", file)
            except TypeError:
                targetL = -1

            try:
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, sizeK, iteration, "Relocate", file)
            except TypeError:
                targetR = -1

            file.write("Теперь ищем минимум из двух целевых" + '\n')
            minimum = min(targetL, targetR)
            if minimum == targetL and minimum != -1:
                file.write("Выбрали левого у него целевая меньше" + '\n')
                return Xl, Yl, Sl, Al, targetL, sizeK

            elif minimum == targetR and minimum != -1 and targetR != targetL:
                file.write("Выбрали правого у него целевая меньше" + '\n')
                return XR, YR, SR, AR, targetR, sizeK

            else:
                file.write("Все пошло по пизде ничего не сохранили" + '\n')
                return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK

        file.write("По какой-то причине нет соседей" + '\n')
        return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK

    elif client == sosed and clientK != sosedK:
        X, Y, Sresh, A = ReadStartLocalSearchOfFile(sizeK)
        try:
            file.write("Клиент и сосед равны, добавляем время работы\n")
            Sresh[sosed][sosedK] += Sresh[client][clientK]
            X, Y, Sresh, A = DeleteClientaFromPath(X, Y, Sresh, A, client, clientK)
            A = TimeOfArrival(X, Y, Sresh, file)

        except IOError:
            file.write("Объект не удален" + '\n')
            Sresh[sosed][sosedK] -= factory.S[client] / factory.wells[client]
            Sresh[client][clientK] += factory.S[client] / factory.wells[client]

        try:
            X, Y, Sresh, A, target, SizeK = Checker(X, Y, Sresh, A, sizeK, iteration, "Two_Opt", file)
            file.write("OperatorJoinFromReloc stop: <-\n")
            return X, Y, Sresh, A, target, SizeK
        except TypeError:
            file.write("OperatorJoinFromReloc stop: <-\n")
            return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK

    file.write("Что-то пошло не так" + '\n')
    return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK


# переставляем клиента к новому соседу, локальный поиск
def Relocate(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration):
    file = open("log/relog.txt", 'a')
    file.write("->Relocate start" + '\n')
    file.write("Целевая функция до применения Relocate = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    fileflag = 0
    while TargetFunction != buf_targ:
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)

        # Bыбираем клиента
        # client, clientCar = ChooseRandomObjAndCar(Y, SizeK)
        for clientCar in range(SizeK):
            for client in range(1, factory.N):
                if Y[client][clientCar] == 1:
                    file.write("Переставляем клиентa " + str(client) + '\n')
                    file.write("С машины " + str(clientCar) + '\n')

                    for sosedK in range(SizeK):
                        for sosed in range(1, factory.N):
                            coins = ResultCoins()
                            if Y[sosed][sosedK] == 1 and coins == 1:
                                file.write(
                                    "Монетка сказала что рассматриваем эту окрестность coins = " + str(coins) + '\n')
                                file.write("К соседу " + str(sosed) + '\n')
                                file.write("На машине " + str(sosedK) + '\n')

                                x, y, s, a, target_function, sizeK = OperatorJoinFromReloc(X, Y, Sresh, A, SizeK,
                                                                                           client, clientCar,
                                                                                           sosed, sosedK, iteration,
                                                                                           file)
                                file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                                file.write("Выбираем минимальное решение" + '\n')
                                minimum = min(TargetFunction, target_function)
                                if minimum == target_function:
                                    file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                    file.write("Новая целевая функция равна " + str(target_function) + '\n')

                                    SaveLocalSearch(x, y, s, a, sizeK)
                                    TargetFunction = target_function
                                    SizeK = sizeK
                                    fileflag = 1
                                else:
                                    file.write(
                                        "Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                                    file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')

        x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile(sizeK_start)
        target_function_start = CalculationOfObjectiveFunction(x_start, PenaltyFunction(y_start, s_start,
                                                                                        a_start, iteration))
        file.write(
            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

        if fileflag == 1:
            x, y, s, a = ReadLocalSearchOfFile(SizeK)
            target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
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

            SaveStartLocalSearch(x, y, s, a, SizeK)
            target_function_start = target_function
            TargetFunction = target_function
            sizeK_start = SizeK
        else:
            file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
            file.write("Старая целевая функция равна " + str(target_function_start) + '\n')
    file.write("While stop\n")

    file.write("<-Relocate stop" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sizeK_start


def OperatorJoinFromTwoOpt(x, y, s, a, sizeK, target_function, client1, client1Car, client2, client2Car, iteration,
                           file):
    file.write("OperatorJoinFromTwoOpt start: ->" + '\n')
    SizeK = sizeK
    Target_Function = target_function
    X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)

    tail1 = SearchTail(X, client1, client1Car, file)
    time1 = SaveTime(Sresh, tail1, client1Car, file)

    tail2 = SearchTail(X, client2, client2Car, file)
    time2 = SaveTime(Sresh, tail2, client2Car, file)

    sosed1 = SearchSosedLeftOrRight(X, Y, client1, "left", client1Car)
    sosed2 = SearchSosedLeftOrRight(X, Y, client2, "left", client2Car)
    file.write("    Сосед слева для хвоста один = " + str(sosed1) + '\n')
    file.write("    Сосед слева для хвоста два = " + str(sosed2) + '\n')

    file.write("    Занулим хвосты\n")
    X, Y, Sresh, A = DeleteTail(X, Y, Sresh, A, sosed1, tail1, client1Car, file)
    X, Y, Sresh, A = DeleteTail(X, Y, Sresh, A, sosed2, tail2, client2Car, file)

    if sosed1 == tail2[0] or sosed2 == tail1[0]:
        file.write("    Рассматриваем вариант, что начало хвоста = соседу слева\n")

        if sosed1 == tail2[0] and sosed2 != tail1[0]:
            file.write("    Сосед один = началу хвоста два (" + str(sosed1) + "=" + str(tail2[0]) + ")\n")

            file.write("    Присоединяем второй хвост" + '\n')
            Sresh[sosed1][client1Car] += time2[0]
            for i in range(1, len(tail2)):
                X[sosed1][tail2[i]][client1Car] = 1
                Y[tail2[i]][client1Car] = 1
                Sresh[tail2[i]][client1Car] = time2[i]
                sosed1 = tail2[i]

            file.write("    Присоединяем первый хвост" + '\n')
            for i in range(len(tail1)):
                X[sosed2][tail1[i]][client2Car] = 1
                Y[tail1[i]][client2Car] = 1
                Sresh[tail1[i]][client2Car] = time1[i]
                sosed2 = tail1[i]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif sosed2 == tail1[0] and sosed1 != tail2[0]:
            file.write("    Сосед два = началу хвоста один (" + str(sosed2) + "=" + str(tail1[0]) + ")\n")

            file.write("    Присоединяем первый хвост" + '\n')
            Sresh[sosed2][client2Car] += time1[0]
            for i in range(1, len(tail1)):
                X[sosed2][tail1[i]][client2Car] = 1
                Y[tail1[i]][client2Car] = 1
                Sresh[tail1[i]][client2Car] = time1[i]
                sosed2 = tail1[i]

            file.write("    Присоединяем второй хвост" + '\n')
            for i in range(len(tail2)):
                X[sosed1][tail2[i]][client1Car] = 1
                Y[tail2[i]][client1Car] = 1
                Sresh[tail2[i]][client1Car] = time2[i]
                sosed1 = tail2[i]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif sosed1 == tail2[0] and sosed2 == tail1[0]:
            file.write("    Сосед один = началу хвоста два (" + str(sosed1) + "=" + str(tail2[0]) + ")\n")
            file.write("    Сосед два = началу хвоста один (" + str(sosed2) + "=" + str(tail1[0]) + ")\n")

            file.write("    Присоединяем второй хвост" + '\n')
            Sresh[sosed1][client1Car] += time2[0]
            for i in range(1, len(tail2)):
                X[sosed1][tail2[i]][client1Car] = 1
                Y[tail2[i]][client1Car] = 1
                Sresh[tail2[i]][client1Car] = time2[i]
                sosed1 = tail2[i]

            file.write("    Присоединяем первый хвост" + '\n')
            Sresh[sosed2][client2Car] += time1[0]
            for i in range(1, len(tail1)):
                X[sosed2][tail1[i]][client2Car] = 1
                Y[tail1[i]][client2Car] = 1
                Sresh[tail1[i]][client2Car] = time1[i]
                sosed2 = tail1[i]

            A = TimeOfArrival(X, Y, Sresh, file)

    else:
        file.write("    Начало хвоста не равно соседу слева\n")

        file.write("    Присоединяем первый хвост" + '\n')
        for i in range(len(tail1)):
            X[sosed2][tail1[i]][client2Car] = 1
            Y[tail1[i]][client2Car] = 1
            Sresh[tail1[i]][client2Car] = time1[i]
            sosed2 = tail1[i]

        file.write("    Присоединяем второй хвост" + '\n')
        for i in range(len(tail2)):
            X[sosed1][tail2[i]][client1Car] = 1
            Y[tail2[i]][client1Car] = 1
            Sresh[tail2[i]][client1Car] = time2[i]
            sosed1 = tail2[i]

        A = TimeOfArrival(X, Y, Sresh, file)

    try:
        X, Y, Sresh, A, Target_Function, SizeK = Checker(X, Y, Sresh, A, SizeK, iteration, "Two_Opt", file)
        file.write("OperatorJoinFromTwoOpt stop: <-\n")
        return X, Y, Sresh, A, Target_Function, SizeK
    except TypeError:
        file.write("OperatorJoinFromTwoOpt stop: <-\n")
        return x, y, s, a, target_function, sizeK


def Two_Opt(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration):
    file = open("log/twooptlog.txt", 'a')
    file.write("Two_Opt start: ->" + '\n')
    file.write("Целевая функция до применения Two_Opt = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    fileflag = 0
    while TargetFunction != buf_targ:
        file.write("While start\n")
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)

        # Bыбираем клиента
        # client, clientCar = ChooseRandomObjAndCar(Y, SizeK)
        for client1Car in range(SizeK):
            for client1 in range(1, factory.N):
                coins = ResultCoins()
                if Y[client1][client1Car] == 1 and coins == 1:
                    file.write("Монетка сказала что рассматриваем эту окрестность coins = " + str(coins) + '\n')
                    file.write("Переставляем от клиентa " + str(client1) + '\n')
                    file.write("С машины " + str(client1Car) + '\n')

                    for client2Car in range(SizeK):
                        for client2 in range(1, factory.N):
                            if Y[client2][client2Car] == 1:
                                file.write(
                                    "У маршрутов " + str(client1Car) + " " + str(
                                        client2Car) + " меняем хвосты\nНачиная с "
                                                      "объектов " + str(
                                        client1) + " и " + str(client2) + " соответствено\n")

                                x, y, s, a, target_function, sizeK = OperatorJoinFromTwoOpt(X, Y, Sresh, A, SizeK,
                                                                                            TargetFunction, client1,
                                                                                            client1Car,
                                                                                            client2, client2Car,
                                                                                            iteration,
                                                                                            file)
                                file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                                file.write("Выбираем минимальное решение" + '\n')
                                file.write("Последняя минимальная целевая = " + str(TargetFunction) + '\n')
                                file.write("Новая целевая = " + str(target_function) + '\n')
                                minimum = min(TargetFunction, target_function)
                                if minimum == target_function:
                                    file.write(
                                        "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                    file.write("Новая целевая функция равна " + str(target_function) + '\n')
                                    SaveLocalSearch(x, y, s, a, sizeK)
                                    TargetFunction = target_function
                                    SizeK = sizeK
                                    fileflag = 1
                                else:
                                    file.write(
                                        "Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                                    file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')

        x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile(sizeK_start)
        target_function_start = CalculationOfObjectiveFunction(x_start, PenaltyFunction(y_start, s_start,
                                                                                        a_start, iteration))
        file.write(
            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

        if fileflag == 1:
            x, y, s, a = ReadLocalSearchOfFile(SizeK)
            target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
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

            SaveStartLocalSearch(x, y, s, a, SizeK)
            target_function_start = target_function
            TargetFunction = target_function
            sizeK_start = SizeK
        else:
            file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
            file.write("Старая целевая функция равна " + str(target_function_start) + '\n')
    file.write("While stop\n")

    file.write("Локальный оптимум найден сохраняем в популяцию решение\n")
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(SizeK):
                file.write(str(X[i][j][k]) + ' ')
            file.write("\n")

    file.write("Two_Opt stop: <-" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sizeK_start


# Возможность приезжать нескольким машинам на одну локацию
def Help(Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start, iteration):
    file = open("log/helog.txt", 'a')
    file.write("Help start: ->" + '\n')
#TODO если есть свободная машина, то тдавать ей скважины
    SaveStartHelp(Xstart, Ystart, Sstart, Astart, sizeK_start)
    file.write("Целевая функция до применения оператора хелп = " + str(target_function_start) + "\n")

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
                                            file.write("Последняя целевая функция = " + str(TargetFunction)+ '\n')
                                            minimum1 = min(TargetFunction, target_function)
                                            if minimum1 == target_function:
                                                file.write(
                                                    "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                file.write("Новая целевая функция равна " + str(target_function) + '\n')

                                                SaveHelp(x, y, s, a, sizeK)
                                                TargetFunction = target_function
                                                SizeK = sizeK
                                                fileflag = 1
                                                sequence2 = GettingTheSequence(X)
                                                sequence1 = TransferX2toX1(sequence2, X)
                                                file.write("Новое решение " + str(sequence1) + '\n')
                                            else:
                                                file.write("Новое перемещение, хуже чем то что было, возвращаем наше "
                                                           "старое решение" + '\n')
                                                file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')
                                            file.write('\n')
# TODO надо понять почему если сделал хуже он возвращет
                        Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile(sizeK_start)
                        target_function_start = CalculationOfObjectiveFunction(Xstart, PenaltyFunction(Ystart, Sstart,
                                                                                                       Astart,
                                                                                                       iteration))
                        file.write(
                            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

                        if fileflag == 1:
                            x, y, s, a = ReadHelpOfFile(SizeK)
                            target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
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
            X, Y, Sresh, A = DeleteClientaFromPath(X, Y, Sresh, A, client, clientCar)

        A = TimeOfArrival(X, Y, Sresh, file)

        try:
            X, Y, Sresh, A, target_function, sizeK = Checker(X, Y, Sresh, A, sizeK, iteration, "Help", file)
            file.write("    OperatorJoinFromHelp stop: <-\n")
            return X, Y, Sresh, A, target_function, sizeK
        except TypeError:
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
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientCar)

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
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client, clientCar)

            Xl[sosedLeft][sosed][sosedCar] = 0
            if sosedLeft != client:
                file.write("    Сосед слева не равен клиенту\n")
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

        try:
            Xl, Yl, Sl, Al, targetL, sizeK = Checker(Xl, Yl, Sl, Al, sizeK, iteration, "Relocate", file)
        except TypeError:
            targetL = -1

        try:
            XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, sizeK, iteration, "Relocate", file)
        except TypeError:
            targetR = -1

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
            x, y, s, a, Target_Function[n], SizeSolution[n] = Relocate(X, Y, Sresh, A, Target_Function[n],
                                                                       SizeSolution[n], iteration)
        elif oper == '2-Opt':
            x, y, s, a, Target_Function[n], SizeSolution[n] = Two_Opt(X, Y, Sresh, A, Target_Function[n],
                                                                      SizeSolution[n], iteration)

        print("\nРешение номер", n, "построено")
        print("_____________________________")

        SavePopulation(x, y, s, a)
    # iteration += 1
    print("Популяция создана и сохранена в файл!!")
    print("___________________________________________________________________________________________________________")
