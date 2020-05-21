from forOper import *
import time


# переставляем клиента к новому соседу, локальный поиск
def Relocate(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration, timeLocal, evolution=2,
             cycle=factory.param_local_search):
    if os.path.getsize("log/relog.txt") <= 700 * 1000000:
        file = open("log/relog.txt", 'a')
    else:
        if os.path.getsize("log/relog1.txt") <= 700 * 1000000:
            file = open("log/relog1.txt", 'a')
        else:
            file = open("log/relog2.txt", 'a')

    start = time.time()
    timeLocal[1] += 1

    file.write("->Relocate start" + '\n')
    file.write("Целевая функция до применения Relocate = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    fileflag = 0
    it = 0
    # for it in range(factory.param_local_search):
    while it < cycle:
        it += 1
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)
        sequenceX2 = GettingTheSequence(X)

        # Bыбираем клиента
        # client, clientCar = ChooseRandomObjAndCar(Y, SizeK)
        for clientCar in range(SizeK):
            for client in range(1, factory.N):
                if Y[client][clientCar] == 1:

                    for sosedK in range(SizeK):
                        for sosed in range(factory.N):

                            sosedLeft = SearchSosedLeftOrRight(X, Y, sosed, "left", sosedK)  # левый сосед соседа
                            sosedRight = SearchSosedLeftOrRight(X, Y, sosed, "right", sosedK)  # правый сосед соседа

                            if (client != sosedLeft and client != sosed and client != sosedRight
                                and not IsContainWells(sequenceX2[sosedK], client, file))\
                                or (client == sosedLeft or client == sosed or client == sosedRight)\
                                    or (sosed == 0 and not CarIsWork(Y, sosedK)):

                                file.write("Это не мусорное решение, можно смотреть\n")

                                if (Y[sosed][sosedK] == 1 and sosed != 0) or (sosed == 0 and not CarIsWork(Y, sosedK)
                                                                              and evolution == 2):

                                    if ResultCoins():
                                        file.write(
                                            "Монетка сказала что рассматриваем эту окрестность" + '\n')
                                        file.write("Переставляем клиентa " + str(client) + '\n')
                                        file.write("С машины " + str(clientCar) + '\n')

                                        file.write("К соседу " + str(sosed) + '\n')
                                        file.write("На машине " + str(sosedK) + '\n')

                                        x, y, s, a, target_function, sizeK = OperatorJoinFromReloc(X, Y, Sresh, A,
                                                                                                   SizeK,
                                                                                                   client, clientCar,
                                                                                                   sosed, sosedK,
                                                                                                   sosedLeft, sosedRight,
                                                                                                   iteration,
                                                                                                   file)
                                        file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')
                                        file.write("Стартовая целевая функция " + str(target_function_start) + '\n')
                                        file.write("Целевая функция до релока " + str(TargetFunction) + '\n')
                                        file.write("Целевая функция после релока " + str(target_function) + '\n')

                                        file.write("Выбираем минимальное решение" + '\n')
                                        minimum = min(TargetFunction, target_function)
                                        if minimum == target_function and minimum != TargetFunction:
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
                                    else:
                                        file.write("Монетка сказала не берем\n")
                                else:
                                    file.write("Не прошло условие\n")
                            else:
                                file.write("Отбросили мусорное решение\n")

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

        # if evolution == 1:
        #     SaveStartLocalSearch(x, y, s, a, SizeK)
        #     target_function_start = target_function
        #     TargetFunction = target_function
        #     sizeK_start = SizeK

        minimum2 = min(target_function_start, target_function)
        if (minimum2 == target_function and target_function != -1) or (fileflag == 1 and it == 0):
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
    x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile(sizeK_start)

    Time = time.time() - start
    timeLocal[0] += Time
    file.write("Время работы Relocate = " + str(Time) + 'seconds\n')

    file.write("<-Relocate stop" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sizeK_start, timeLocal


def Two_Opt(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration, timeLocal):
    if os.path.getsize("log/twooptlog.txt") <= 700 * 1000000:
        file = open("log/twooptlog.txt", 'a')
    else:
        if os.path.getsize("log/twooptlog1.txt") <= 700 * 1000000:
            file = open("log/twooptlog1.txt", 'a')
        else:
            file = open("log/twooptlog2.txt", 'a')

    start = time.time()
    timeLocal[1] += 1

    file.write("Two_Opt start: ->" + '\n')
    file.write("Целевая функция до применения Two_Opt = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    fileflag = 0
    it = 0
    # for it in range(factory.param_local_search):
    while it < factory.param_local_search:
        it += 1
        file.write("While start\n")
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)

        # Bыбираем клиента
        # client, clientCar = ChooseRandomObjAndCar(Y, SizeK)
        for client1Car in range(SizeK):
            for client1 in range(1, factory.N):
                if Y[client1][client1Car] == 1:

                    tail1, sequenceX2 = SearchTail(X, client1, client1Car, file)

                    for client2Car in range(SizeK):
                        for client2 in range(factory.N):
                            if (Y[client2][client2Car] == 1 and client2 != 0) or (client2 == 0 and not CarIsWork(Y, client2Car)):
                                file.write("\nsequenceX2[client1Car] = " + str(sequenceX2[client1Car]) + '\n')
                                file.write("Хвост1 = " + str(tail1) + '\n')

                                tail2, sequenceX2 = SearchTail(X, client2, client2Car, file)
                                file.write("\nsequenceX2[client2Car] = " + str(sequenceX2[client2Car]) + '\n')
                                file.write("Хвост2 = " + str(tail2) + '\n')

                                file.write("Меняем от клиентa1 " + str(client1) + '\n')
                                file.write("С машины1 " + str(client1Car) + '\n')

                                file.write("Меняем от клиентa2 " + str(client2) + '\n')
                                file.write("С машины2 " + str(client2Car) + '\n')

                                if (not IsContainTailInStart(sequenceX2[client1Car], tail2, client1, file) and not
                                    IsContainTailInStart(sequenceX2[client2Car], tail1, client2, file)
                                    and client1Car != client2Car) or client1Car == client2Car or client2 == 0:

                                    if ResultCoins():
                                        file.write(
                                            "Монетка сказала что рассматриваем эту окрестность coins = " + '\n')

                                        file.write(
                                            "У маршрутов " + str(client1Car) + " " + str(
                                                client2Car) + " меняем хвосты\nНачиная с "
                                                              "объектов " + str(
                                                client1) + " и " + str(client2) + " соответствено\n")
                                        tail1, sequenceX2 = SearchTail(X, client1, client1Car, file)

                                        x, y, s, a, target_function, sizeK = OperatorJoinFromTwoOpt(X, Y, Sresh, A,
                                                                                                    SizeK,
                                                                                                    TargetFunction,
                                                                                                    client1,
                                                                                                    client1Car, tail1,
                                                                                                    client2, client2Car,
                                                                                                    tail2,
                                                                                                    iteration,
                                                                                                    file)
                                        file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                                        file.write("Выбираем минимальное решение" + '\n')
                                        file.write("Последняя минимальная целевая = " + str(TargetFunction) + '\n')
                                        file.write("Новая целевая = " + str(target_function) + '\n')
                                        minimum = min(TargetFunction, target_function)
                                        if minimum == target_function and minimum != TargetFunction:
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
                                else:
                                    file.write("Это решение мусор, такое не смотрим\n\n")

        file.write(
            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

        if fileflag == 1:
            x, y, s, a = ReadLocalSearchOfFile(SizeK)
            target_function = CalculationOfObjectiveFunction(x, 0)
            file.write(
                "Целевая функция последнего минимального переставления без штрафа= " + str(
                    target_function) + '\n')
            target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
            file.write(
                "Целевая функция последнего минимального переставления со штрафом= " + str(
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
    x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile(sizeK_start)

    Time = time.time() - start
    timeLocal[0] += Time
    file.write("Время работы Two_Opt = " + str(Time) + 'seconds\n')

    file.write("Two_Opt stop: <-" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sizeK_start, timeLocal


# Возможность приезжать нескольким машинам на одну локацию
def Help(Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start, iteration, timeLocal):
    if os.path.getsize("log/helog.txt") <= 700 * 1000000:
        file = open("log/helog.txt", 'a')
    else:
        if os.path.getsize("log/helog1.txt") <= 700 * 1000000:
            file = open("log/helog1.txt", 'a')
        else:
            file = open("log/helog2.txt", 'a')

    start = time.time()
    timeLocal[1] += 1

    file.write("Help start: ->" + '\n')
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

                    file.write("По одной скважине отдаем\n")

                    howMuch = 0
                    for proebSkv in range(1, contWells + 1):
                        X, Y, Sresh, A = ReadStartHelpOfFile(sizeK_start)
                        TargetFunction = target_function_start
                        SizeK = sizeK_start

                        flag = 0
                        if 1 < int(Sresh[client][k] / factory.timeWork):
                            flag = 'not the last'
                        elif 1 == int(Sresh[client][k] / factory.timeWork):
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
                                    for sosed in range(factory.N):
                                        if (Y[sosed][sosedK] == 1 and sosed != 0) or (
                                                sosed == 0 and not CarIsWork(Y, sosedK)):
                                            file.write("Рассматриваемый объект " + str(sosed) + "\n")
                                            file.write(
                                                "Попробую одну скважину с объекта " + str(client) + " и машины " + str(
                                                    k) + "\n")
                                            file.write(" отдать машине " + str(sosedK) + " рядом с объектом " + str(
                                                sosed) + "\n")
# TODO можно ускорить отбросив мусорные решения
                                            x, y, s, a, target_function, sizeK = OperatorJoinFromHelp(X, Y, Sresh, A,
                                                                                                      SizeK,
                                                                                                      client, k, sosed,
                                                                                                      sosedK,
                                                                                                      factory.timeWork,
                                                                                                      TargetFunction,
                                                                                                      iteration, flag,
                                                                                                      file)
                                            file.write(
                                                "Число используемых машин теперь " + str(AmountCarUsed(y)) + '\n')

                                            file.write(
                                                "Выбираем минимальное решение из стартового и измененного" + '\n')
                                            file.write("Последняя целевая функция = " + str(TargetFunction) + '\n')
                                            minimum1 = min(TargetFunction, target_function)
                                            if minimum1 == target_function and minimum1 != TargetFunction:
                                                file.write(
                                                    "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                file.write("Новая целевая функция равна " + str(target_function) + '\n')

                                                SaveHelp(x, y, s, a, sizeK)
                                                TargetFunction = target_function
                                                SizeK = sizeK
                                                fileflag = 1
                                                sequence2 = GettingTheSequence(x)
                                                sequence1 = TransferX2toX1(sequence2, x)
                                                file.write("Новое решение " + str(sequence1) + '\n')
                                            else:
                                                file.write("Новое перемещение, хуже чем то что было, возвращаем наше "
                                                           "старое решение" + '\n')
                                                file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')
                                            file.write('\n')

                            file.write(
                                "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

                            if fileflag == 1:
                                x, y, s, a = ReadHelpOfFile(SizeK)
                                target_function = CalculationOfObjectiveFunction(x, 0)
                                file.write(
                                    "Целевая функция последнего минимального переставления без штрафа= " + str(
                                        target_function) + '\n')
                                target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
                                file.write(
                                    "Целевая функция последнего минимального переставления со штрафом= " + str(
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
                                howMuch = 'all'
                                break

                    if howMuch == 'all':
                        file.write("\nПопробуем отдать несколько скважин\n")

                        file.write("Пересчитываем проебанные скважины\n")
                        contWells = CountWellsWithFane(Sstart, Astart, client, k)
                        file.write("Всего не укладывается " + str(contWells) + " скважин\n")

                        for proebSkv in range(2, contWells + 1):
                            file.write("Отдаем " + str(proebSkv) + " скважин\n")
                            X, Y, Sresh, A = ReadStartHelpOfFile(sizeK_start)
                            TargetFunction = target_function_start
                            SizeK = sizeK_start

                            flag = 0
                            if proebSkv < int(Sresh[client][k] / factory.timeWork):
                                flag = 'not the last'
                            elif proebSkv == int(Sresh[client][k] / factory.timeWork):
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
                                            if (Y[sosed][sosedK] == 1 and sosed != 0) or (
                                                    sosed == 0 and not CarIsWork(Y, sosedK)):
                                                file.write("Рассматриваемый объект " + str(sosed) + "\n")
                                                file.write(
                                                    "Попробую одну скважину с объекта " + str(
                                                        client) + " и машины " + str(
                                                        k) + "\n")
                                                file.write(" отдать машине " + str(sosedK) + " рядом с объектом " + str(
                                                    sosed) + "\n")

                                                x, y, s, a, target_function, sizeK = OperatorJoinFromHelp(X, Y, Sresh,
                                                                                                          A,
                                                                                                          SizeK,
                                                                                                          client, k,
                                                                                                          sosed,
                                                                                                          sosedK,
                                                                                                          proebSkv * factory.timeWork,
                                                                                                          TargetFunction,
                                                                                                          iteration,
                                                                                                          flag,
                                                                                                          file)
                                                file.write(
                                                    "Число используемых машин теперь " + str(AmountCarUsed(y)) + '\n')

                                                file.write(
                                                    "Выбираем минимальное решение из стартового и измененного" + '\n')
                                                file.write("Последняя целевая функция = " + str(TargetFunction) + '\n')
                                                minimum1 = min(TargetFunction, target_function)
                                                if minimum1 == target_function and minimum1 != TargetFunction:
                                                    file.write(
                                                        "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                    file.write(
                                                        "Новая целевая функция равна " + str(target_function) + '\n')

                                                    SaveHelp(x, y, s, a, sizeK)
                                                    TargetFunction = target_function
                                                    SizeK = sizeK
                                                    fileflag = 1
                                                    sequence2 = GettingTheSequence(x)
                                                    sequence1 = TransferX2toX1(sequence2, x)
                                                    file.write("Новое решение " + str(sequence1) + '\n')
                                                else:
                                                    file.write(
                                                        "Новое перемещение, хуже чем то что было, возвращаем наше "
                                                        "старое решение" + '\n')
                                                    file.write(
                                                        "Старая целевая функция равна " + str(TargetFunction) + '\n')
                                                file.write('\n')

                        file.write(
                            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

                        if fileflag == 1:
                            x, y, s, a = ReadHelpOfFile(SizeK)
                            target_function = CalculationOfObjectiveFunction(x, 0)
                            file.write(
                                "Целевая функция последнего минимального переставления без штрафа = " + str(
                                    target_function) + '\n')
                            target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
                            file.write(
                                "Целевая функция последнего минимального переставления со штрафом = " + str(
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

    Time = time.time() - start
    timeLocal[0] += Time
    file.write("Время работы Help = " + str(Time) + 'seconds\n')

    file.write("<-Help stop" + '\n')
    file.close()

    return Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start, timeLocal


def Exchange(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration, timeLocal,
             cycle=factory.param_local_search):
    if os.path.getsize("log/exchlog.txt") <= 700 * 1000000:
        file = open("log/exchlog.txt", 'a')
    else:
        if os.path.getsize("log/exchlog1.txt") <= 700 * 1000000:
            file = open("log/exchlog1.txt", 'a')
        else:
            file = open("log/exchlog2.txt", 'a')

    start = time.time()
    timeLocal[1] += 1

    file.write("->Exchange start" + '\n')
    file.write("Целевая функция до применения Exchange = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start, sizeK_start)
    TargetFunction = target_function_start
    SizeK = sizeK_start
    buf_targ = 0

    fileflag = 0
    it = 0
    # for it in range(factory.param_local_search):
    while it < cycle:
        it += 1
        buf_targ = TargetFunction
        X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)
        sequenceX2 = GettingTheSequence(X)

        # Bыбираем клиента
        for clientCar in range(SizeK):
            for client in range(1, factory.N):
                if Y[client][clientCar] == 1:
                    for sosedCar in range(SizeK):
                        for sosed in range(1, factory.N):
                            if Y[sosed][sosedCar] == 1:

                                subseq1 = []
                                subseq2 = []

                                indexCl = sequenceX2[clientCar].index(client)
                                indexSos = sequenceX2[sosedCar].index(sosed)

                                for i in range(indexCl, len(sequenceX2[clientCar])):
                                    if i <= indexCl + factory.param_len_subseq and sequenceX2[clientCar][i] != 0:
                                        subseq1.append(sequenceX2[clientCar][i])
                                    else:
                                        break
                                for i in range(indexSos, len(sequenceX2[sosedCar])):
                                    if i <= indexSos + factory.param_len_subseq and sequenceX2[sosedCar][i] != 0:
                                        subseq2.append(sequenceX2[sosedCar][i])
                                    else:
                                        break

                                if subseq1 != [] and subseq2 != []:
                                    file.write("Переставляем клиентa " + str(client) + '\n')
                                    file.write("С машины " + str(clientCar) + '\n')

                                    file.write("К соседу " + str(sosed) + '\n')
                                    file.write("На машине " + str(sosedCar) + '\n')

                                    file.write("Собираем подпоследовательности\n")
                                    file.write("path1 = " + str(sequenceX2[clientCar]) + '\n')
                                    file.write("path2 = " + str(sequenceX2[sosedCar]) + '\n')

                                    file.write("subseq1 = " + str(subseq1) + '\n')
                                    file.write("subseq2 = " + str(subseq2) + '\n')

                                    buf1 = []
                                    for i in range(len(subseq1)):
                                        if subseq1[-1] != 0:
                                            buf1.append(subseq1[i])
                                            buf2 = []
                                            for j in range(len(subseq2)):
                                                if subseq2[-1] != 0:
                                                    buf2.append(subseq2[j])

                                                seq1Start = sequenceX2[clientCar].index(buf1[0])
                                                seq1End = sequenceX2[clientCar].index(buf1[-1])
                                                seq2Start = sequenceX2[sosedCar].index(buf2[0])
                                                seq2End = sequenceX2[sosedCar].index(buf2[-1])

                                                if seq1Start == 1 or sequenceX2[clientCar][seq1End] == 0:
                                                    sequence1Left = 0
                                                else:
                                                    sequence1Left = sequenceX2[clientCar][seq1Start-2]

                                                if sequenceX2[clientCar][seq1End+1] == 0 or sequenceX2[clientCar][seq1End] == 0:
                                                    sequence1Right = 0
                                                else:
                                                    sequence1Right = sequenceX2[clientCar][seq1End+2]

                                                if seq2Start == 1 or sequenceX2[sosedCar][seq2End] == 0:
                                                    sequence2Left = 0
                                                else:
                                                    sequence2Left = sequenceX2[sosedCar][seq2Start-2]

                                                if sequenceX2[sosedCar][seq2End+1] == 0 or sequenceX2[sosedCar][seq2End] == 0:
                                                    sequence2Right = 0
                                                else:
                                                    sequence2Right = sequenceX2[sosedCar][seq2End+2]

                                                file.write("buf1 = " + str(buf1) + '\n')
                                                file.write("buf2 = " + str(buf2) + '\n')

                                                # TODO не отбрасываюся решения в которых левые и правые соседи равны элементам другой последовательности кроме первого и последнего
                                                if (not IsContainTailInStart(sequenceX2[sosedCar], buf1, sequence2Left,
                                                                             file)
                                                    and not IsContainTailInEnd(sequenceX2[sosedCar], buf1,
                                                                               sequence2Right, file)
                                                    and not IsContainTailInStart(sequenceX2[clientCar], buf2,
                                                                                 sequence1Left, file)
                                                    and not IsContainTailInEnd(sequenceX2[clientCar], buf2,
                                                                               sequence1Right,
                                                                               file) and clientCar != sosedCar) \
                                                        or (
                                                        clientCar == sosedCar and not IsContainTailInTail(buf1, buf2,
                                                                                                          file)):
                                                    file.write("Пред Слева от последовательности клиента " + str(
                                                        sequence1Left) + "\n")
                                                    file.write(
                                                        "После Справа от последовательности клиента " + str(
                                                            sequence1Right) + "\n")
                                                    file.write("Перд Слева от последовательности соседа " + str(
                                                        sequence2Left) + "\n")
                                                    file.write(
                                                        "После Справа от последовательности соседа " + str(
                                                            sequence2Right) + "\n")
                                                    file.write("Элементы подпоследовательностей "
                                                               "не содержатся в другом маршруте\n")

                                                    if ResultCoins():
                                                        file.write("Монетка сказала, берем\n")
                                                        file.write("buf1 = " + str(buf1) + '\n')
                                                        for p in range(len(buf1)):
                                                            file.write(str(Sresh[buf1[p]][clientCar]) + ' ')
                                                        file.write('\n')

                                                        file.write("buf2 = " + str(buf2) + '\n')
                                                        for p in range(len(buf2)):
                                                            file.write(str(Sresh[buf2[p]][sosedCar]) + ' ')
                                                        file.write('\n')

                                                        x, y, s, a, target_function, sizeK = OperatorJoinFromExchange(
                                                            X, Y, Sresh, A, SizeK, TargetFunction, sequenceX2, client,
                                                            clientCar, buf1, sosed, sosedCar, buf2, iteration, file)
                                                        file.write(
                                                            "Число используемых машин " + str(
                                                                AmountCarUsed(y)) + '\n')

                                                        file.write("Выбираем минимальное решение" + '\n')
                                                        minimum = min(TargetFunction, target_function)
                                                        if minimum == target_function and minimum != TargetFunction:
                                                            file.write(
                                                                "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                            file.write(
                                                                "Новая целевая функция равна " + str(
                                                                    target_function) + '\n')

                                                            SaveLocalSearch(x, y, s, a, sizeK)
                                                            TargetFunction = target_function
                                                            SizeK = sizeK
                                                            fileflag = 1
                                                        else:
                                                            file.write(
                                                                "Новое перемещение, хуже чем то что было, "
                                                                "возвращаем наше старое решение" + '\n')
                                                            file.write(
                                                                "Старая целевая функция равна " + str(
                                                                    TargetFunction) + '\n')
                                                    else:
                                                        file.write("Монетка сказала, не берем\n")
                                                        file.write("buf1 = " + str(buf1) + '\n')
                                                        file.write("buf2 = " + str(buf2) + '\n\n')

                                                else:
                                                    file.write("Отбросили мусорные решения\n")
        file.write(
            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

        if fileflag == 1:
            x, y, s, a = ReadLocalSearchOfFile(SizeK)
            target_function = CalculationOfObjectiveFunction(x, 0)
            file.write(
                "Целевая функция последнего минимального переставления без штрафа= " + str(
                    target_function) + '\n')
            target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
            file.write(
                "Целевая функция последнего минимального переставления со штрафом= " + str(
                    target_function) + '\n')
            fileflag = 0
        else:
            target_function = -1
        # TODO сравнивать по вероятностb
        minimum2 = min(target_function_start, target_function)
        if (minimum2 == target_function and target_function != -1) or (fileflag == 1 and it == 0):
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
    x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile(sizeK_start)

    Time = time.time() - start
    timeLocal[0] += Time
    file.write("Время работы Exchange = " + str(Time) + 'seconds\n')

    file.write("<-Exchange stop" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sizeK_start, timeLocal


# Cоздаем популяцию решений
def PopulationOfSolutions(Target_Function, SizeSolution, iteration, timeLocal):
    for n in range(factory.param_population):  # создаем популяцию решений в кол-ве param_population
        # Берем стартовое решение из файла, потому что какой-то пиздюк его испортил

        X, Y, Sresh, A = ReadStartSolutionOfFile(SizeSolution[n])

        x, y, s, a, Target_Function[n], SizeSolution[n], timeLocal[0] = Relocate(X, Y, Sresh, A, Target_Function[n],
                                                                                     SizeSolution[n], iteration,
                                                                                     timeLocal[0], 1)

        SaveDateFromGraph(Target_Function[n], "StartPopulation")
        print("\nРешение номер", n, "построено")
        print("_____________________________")

        SavePopulation(x, y, s, a)
    print("Популяция создана и сохранена в файл!!")
    print("___________________________________________________________________________________________________________")
    return timeLocal


# Локальный поиск (локально меняем решение)
def LocalSearch(x, y, s, a, target_function, sizeK, iteration, timeLocal):
    print("Применяем локальный поиск (локально меняем решение)")

    # TODO выбираем оператор локального поиска
    local_search_oper = ['relocate', 'Exchange', '2Opt']
    oper = random.choice(local_search_oper)
    # oper = '2Opt'

    print("Используем оператор ", oper)
    if oper == 'relocate':
        x, y, s, a, target_function, sizeK, timeLocal[0] = Relocate(x, y, s, a, target_function, sizeK, iteration,
                                                                    timeLocal[0])
        SaveDateFromGraph(target_function, "Reloc")
        # iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal

    elif oper == '2Opt':
        x, y, s, a, target_function, sizeK, timeLocal[1] = Two_Opt(x, y, s, a, target_function, sizeK, iteration,
                                                                   timeLocal[1])
        SaveDateFromGraph(target_function, "2Opt")
        # iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal

    elif oper == 'Exchange':
        x, y, s, a, target_function, sizeK, timeLocal[3] = Exchange(x, y, s, a, target_function, sizeK, iteration,
                                                                    timeLocal[3], factory.param_local_search/2)
        SaveDateFromGraph(target_function, "Exchange")
        # iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal
