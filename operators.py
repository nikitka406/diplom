from forOper import *
import time


# переставляем клиента к новому соседу, локальный поиск
def Relocate(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration, timeLocal):
    file = open("log/relog.txt", 'a')

    start = time.time()
    timeLocal[1] += 1

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
    x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile(sizeK_start)

    Time = time.time() - start
    timeLocal[0] += Time
    file.write("Время работы Relocate = " + str(Time) + 'seconds\n')

    file.write("<-Relocate stop" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sizeK_start, timeLocal


def Two_Opt(x_start, y_start, s_start, a_start, target_function_start, sizeK_start, iteration, timeLocal):
    file = open("log/twooptlog.txt", 'a')

    start = time.time()
    timeLocal[1] += 1

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
                if Y[client1][client1Car] == 1:
                    file.write("Переставляем от клиентa " + str(client1) + '\n')
                    file.write("С машины " + str(client1Car) + '\n')

                    tail1, sequenceX2 = SearchTail(X, client1, client1Car, file)

                    for client2Car in range(SizeK):
                        for client2 in range(1, factory.N):
                            if Y[client2][client2Car] == 1:
                                tail2, sequenceX2 = SearchTail(X, client2, client2Car, file)

                                if not IsContainTailInStart(sequenceX2[client1Car], tail2, client1) and not \
                                        IsContainTailInStart(sequenceX2[client2Car], tail1, client2):

                                    coins = ResultCoins()
                                    file.write(
                                        "Монетка сказала что рассматриваем эту окрестность coins = " + str(
                                            coins) + '\n')
                                    if coins == 1:
                                        file.write(
                                            "У маршрутов " + str(client1Car) + " " + str(
                                                client2Car) + " меняем хвосты\nНачиная с "
                                                              "объектов " + str(
                                                client1) + " и " + str(client2) + " соответствено\n")

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
                                else:
                                    file.write("Это решение мусор, такое не смотрим\n")

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
    x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile(sizeK_start)

    Time = time.time() - start
    timeLocal[0] += Time
    file.write("Время работы Two_Opt = " + str(Time) + 'seconds\n')

    file.write("Two_Opt stop: <-" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sizeK_start, timeLocal


# Возможность приезжать нескольким машинам на одну локацию
def Help(Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start, iteration, timeLocal):
    file = open("log/helog.txt", 'a')

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
                                    for sosed in range(factory.N):
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
                                            file.write("Последняя целевая функция = " + str(TargetFunction) + '\n')
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

    Time = time.time() - start
    timeLocal[0] += Time
    file.write("Время работы Help = " + str(Time) + 'seconds\n')

    file.write("<-Help stop" + '\n')
    file.close()

    return Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start, timeLocal


# def Swap(Xstart, Ystart, Sstart, Astart, target_function_start, sizeK_start, iteration):

# Cоздаем популяцию решений
def PopulationOfSolutions(Target_Function, SizeSolution, iteration, timeLocal):
    for n in range(factory.param_population):  # создаем популяцию решений в кол-ве param_population
        # Берем стартовое решение из файла, потому что какой-то пиздюк его испортил

        # TODO раскоментить
        name_oper = ['reloc', '2-Opt']
        oper = random.choice(name_oper)
        oper = 'reloc'
        X, Y, Sresh, A = ReadStartSolutionOfFile(SizeSolution[n])

        if oper == 'reloc':
            x, y, s, a, Target_Function[n], SizeSolution[n], timeLocal[0] = Relocate(X, Y, Sresh, A, Target_Function[n],
                                                                                     SizeSolution[n], iteration,
                                                                                     timeLocal[0])
            # x, y, s, a, Target_Function[n], SizeSolution[n], timeLocal[2] = Help(x, y, s, a, Target_Function[n], SizeSolution[n], iteration,
            #                                                         timeLocal[2])

        elif oper == '2-Opt':
            x, y, s, a, Target_Function[n], SizeSolution[n], timeLocal[1] = Two_Opt(X, Y, Sresh, A, Target_Function[n],
                                                                                    SizeSolution[n], iteration,
                                                                                    timeLocal[1])

        print("\nРешение номер", n, "построено")
        print("_____________________________")

        SavePopulation(x, y, s, a)
    # iteration += 1
    print("Популяция создана и сохранена в файл!!")
    print("___________________________________________________________________________________________________________")
    return timeLocal
