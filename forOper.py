from function import *


# вклиниваем между
def OperatorJoinFromReloc(x, y, s, a, sizeK, client, clientK, sosed, sosedK, sosedLeft, sosedRight, iteration, file):
    file.write("    OperatorJoinFromReloc start: ->\n")
    if client != sosed:
        Xl, Yl, Sl, Al = ReadStartLocalSearchOfFile(sizeK)
        XR, YR, SR, AR = ReadStartLocalSearchOfFile(sizeK)

        file.write("sosed_left = " + str(sosedLeft) + '\n')
        file.write("sosed_right = " + str(sosedRight) + '\n')

        file.write("Время окончание client = " + str(factory.l[client]) + '\n')
        file.write("Время окончание sosed = " + str(factory.l[sosed]) + '\n')
        file.write("Время окончание sosedLeft = " + str(factory.l[sosedLeft]) + '\n')
        file.write("Время окончание sosedRight = " + str(factory.l[sosedRight]) + '\n')

        # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
        # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
        if sosedRight != -1 and sosed != 0:
            try:
                file.write("Вставляем клиента к соседу справа" + '\n')
                # машина соседа будет работать у клиента столько же
                buf = 0
                if sosedK != clientK:
                    SR[client][sosedK] += SR[client][clientK]
                elif sosedK == clientK:
                    buf = SR[client][clientK]

                # Чтобы все корректно работало, сначала надо написать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientK)
                if sosedK == clientK:
                    SR[client][sosedK] += buf
                if sosedRight != client:
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
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, sizeK, iteration, "Relocate", file)
            except TypeError:
                targetR = -1
        else:
            targetR = -1

        if sosedLeft != -1 and sosed != 0:  # and factory.t[client][sosed] < factory.l[sosed]:
            try:
                file.write("Вставляем клиента к соседу слева" + '\n')
                # машина соседа будет работать у клиента столько же
                buf = 0
                if sosedK != clientK:
                    Sl[client][sosedK] += Sl[client][clientK]
                elif sosedK == clientK:
                    buf = Sl[client][clientK]

                # Чтобы все корректно работало, сначала надонаписать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client, clientK)
                if sosedK == clientK:
                    Sl[client][sosedK] += buf
                if sosedLeft != client:
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

            try:
                Xl, Yl, Sl, Al, targetL, sizeK = Checker(Xl, Yl, Sl, Al, sizeK, iteration, "Relocate", file)
            except TypeError:
                targetL = -1
        else:
            targetL = -1

        if sosed == 0 and not CarIsWork(YR, sosedK):
            try:
                file.write("    Вставляем скважину в новый маршрут" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client][sosedK] += SR[client][clientK]

                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientK)

                XR[sosed][client][sosedK] = 1
                XR[client][sosed][sosedK] = 1
                YR[sosed][sosedK] = 1
                YR[client][sosedK] = 1  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

            except IOError:
                file.write("    Объект не удален" + '\n')

                XR[sosed][sosedRight][sosedK] = 1
                XR[sosed][client][sosedK] = 0
                XR[client][sosedRight][sosedK] = 0
                YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

            try:
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, sizeK, iteration, "Reloc", file)
                file.write("OperatorJoinFromReloc stop: <-\n")
                return XR, YR, SR, AR, targetR, sizeK
            except TypeError:
                file.write("OperatorJoinFromReloc stop: <-\n")
                return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK

        file.write("Теперь ищем минимум из двух целевых" + '\n')
        if (targetL < targetR and targetL != -1) or (targetR == -1 and targetL != -1):
            file.write("Выбрали левого у него целевая меньше" + '\n')
            file.write("    OperatorJoinFromReloc stop: <-\n")
            return Xl, Yl, Sl, Al, targetL, sizeK

        elif (targetR < targetL and targetR != -1) or (targetL == -1 and targetR != -1):
            file.write("Выбрали правого у него целевая меньше" + '\n')
            file.write("    OperatorJoinFromReloc stop: <-\n")
            return XR, YR, SR, AR, targetR, sizeK

        else:
            file.write("Все пошло по пизде ничего не сохранили" + '\n')
            file.write("    OperatorJoinFromReloc stop: <-\n")
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
            X, Y, Sresh, A, target, SizeK = Checker(X, Y, Sresh, A, sizeK, iteration, "Relocate", file)
            file.write("OperatorJoinFromReloc stop: <-\n")
            return X, Y, Sresh, A, target, SizeK
        except TypeError:
            file.write("OperatorJoinFromReloc stop: <-\n")
            return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK

    file.write("Переставляем одного и тоже к тому же на той же машине" + '\n')
    file.write("OperatorJoinFromReloc stop: <-\n")
    return x, y, s, a, CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration)), sizeK


def OperatorJoinFromTwoOpt(x, y, s, a, sizeK, target_function, client1, client1Car, tail1, client2, client2Car, tail2,
                           iteration, file):
    file.write("OperatorJoinFromTwoOpt start: ->" + '\n')
    SizeK = sizeK
    X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)
    file.write("    tail1 = " + str(tail1) + '\n')
    file.write("    tail2 = " + str(tail2) + '\n')

    if client1Car != client2Car:
        file.write("    Машинки не равны\n")

        time1 = SaveTime(Sresh, tail1, client1Car, file)

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

    elif client1Car == client2Car:
        file.write("    Машинки равны\n")

        time1 = SaveTime(Sresh, tail1, client1Car, file)

        time2 = SaveTime(Sresh, tail2, client2Car, file)

        sosed1 = SearchSosedLeftOrRight(X, Y, client1, "left", client1Car)
        sosed2 = SearchSosedLeftOrRight(X, Y, client2, "left", client2Car)
        file.write("    Сосед слева для хвоста один = " + str(sosed1) + '\n')
        file.write("    Сосед слева для хвоста два = " + str(sosed2) + '\n')

        if len(tail1) - len(tail2) > 1:

            for i in range(len(tail2)):
                tail1.remove(tail2[i])
                time1.pop(len(tail1))

            file.write("    Занулим хвост\n")
            X, Y, Sresh, A = DeleteTail(X, Y, Sresh, A, sosed1, tail1, client1Car, file, tail2[0])

            file.write("    Разворачиваем хвост" + '\n')
            tail1.reverse()
            time1.reverse()
            for i in range(len(tail1)):
                X[sosed1][tail1[i]][client1Car] = 1
                Y[tail1[i]][client1Car] = 1
                Sresh[tail1[i]][client1Car] = time1[i]
                sosed1 = tail1[i]
            X[sosed1][tail2[0]][client1Car] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif len(tail2) - len(tail1) > 1:

            for i in range(len(tail1)):
                tail2.remove(tail1[i])
                time2.pop(len(tail2))

            file.write("    Занулим хвост\n")
            X, Y, Sresh, A = DeleteTail(X, Y, Sresh, A, sosed2, tail2, client2Car, file, tail1[0])

            file.write("    Разворачиваем хвост" + '\n')
            tail2.reverse()
            time2.reverse()
            for i in range(len(tail2)):
                X[sosed2][tail2[i]][client2Car] = 1
                Y[tail2[i]][client2Car] = 1
                Sresh[tail2[i]][client2Car] = time2[i]
                sosed2 = tail2[i]
            X[sosed2][tail1[0]][client2Car] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        else:
            file.write("OperatorJoinFromTwoOpt stop: <-\n")
            return x, y, s, a, target_function, sizeK

        try:
            X, Y, Sresh, A, Target_Function, SizeK = Checker(X, Y, Sresh, A, SizeK, iteration, "Two_Opt", file)
            file.write("OperatorJoinFromTwoOpt stop: <-\n")
            return X, Y, Sresh, A, Target_Function, SizeK
        except TypeError:
            file.write("OperatorJoinFromTwoOpt stop: <-\n")
            return x, y, s, a, target_function, sizeK


def OperatorJoinFromHelp(x, y, s, a, sizeK_start, client, clientCar, sosed, sosedCar, timeWork, target_function_start,
                         iteration, flag, file):
    file.write("OperatorJoinFromHelp start: ->\n")
    sizeK = sizeK_start

    sequenceX2 = GettingTheSequence(x)
    file.write("    Переставляем скважину " + str(client) + " с маршрута " + str(sequenceX2[clientCar]) + '\n')
    file.write("    К объекту " + str(sosed) + " в маршрута " + str(sequenceX2[sosedCar]) + '\n')
    file.write("    Регламент работ " + str(factory.S) + '\n')
    file.write("    Фактическое время работ\n")
    for k in range(len(s[0])):
        for i in range(factory.N):
            file.write(str(s[i][k]) + ' ')
        file.write('\n')
    file.write('\n')

    file.write("    Проверяем на равенство клиента и соседа\n")
    if client == sosed:
        file.write("    Равны\n")
        X, Y, Sresh, A = ReadStartHelpOfFile(sizeK)

        file.write("    Время работы до забирания скважины " + str(Sresh[client][clientCar]) + "\n")
        Sresh[client][clientCar] -= timeWork
        file.write("    Время работы после забирания скважины " + str(Sresh[client][clientCar]) + "\n")

        Sresh[sosed][sosedCar] += timeWork
        if flag == 'last':
            file.write("    Забрали с объекта все скважины, и эта оказаласть последняя,\n"
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

    elif not IsContainWells(sequenceX2[sosedCar], client, file):
        file.write("    Не равны\n")
        Xl, Yl, Sl, Al = ReadStartHelpOfFile(sizeK)
        XR, YR, SR, AR = ReadStartHelpOfFile(sizeK)

        file.write("    Время работы до забирания скважины " + str(Sl[client][clientCar]) + "\n")
        file.write("    Забираем проебанную скважину\n")
        Sl[client][clientCar] -= timeWork
        SR[client][clientCar] -= timeWork
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
        if sosedRight != -1 and sosed != 0:
            try:
                file.write("    Вставляем скважину к соседу справа" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client][sosedCar] += timeWork

                # на случай если мы в итоге все скважины забрали, и эта была последняя
                if flag == 'last':
                    file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                               "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                    XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientCar)

                XR[sosed][sosedRight][sosedCar] = 0
                XR[sosed][client][sosedCar] = 1
                if client != sosedRight:
                    file.write("    Сосед справа не равен клиенту\n")
                    XR[client][sosedRight][sosedCar] = 1
                YR[client][sosedCar] = 1  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

            except IOError:
                file.write("    Объект не удален" + '\n')
                XR[sosed][sosedRight][sosedCar] = 1
                XR[sosed][client][sosedCar] = 0
                XR[client][sosedRight][sosedCar] = 0
                YR[client][sosedCar] = 0  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

            try:
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, sizeK, iteration, "Help", file)
            except TypeError:
                targetR = -1
        else:
            targetR = -1

        if sosedLeft != -1 and sosed != 0:
            try:
                file.write("    Вставляем клиента к соседу слева" + '\n')
                # машина соседа будет работать у клиента столько же
                Sl[client][sosedCar] += timeWork

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
                Xl, Yl, Sl, Al, targetL, sizeK = Checker(Xl, Yl, Sl, Al, sizeK, iteration, "Help", file)
            except TypeError:
                targetL = -1
        else:
            targetL = -1

        if sosed == 0 and not CarIsWork(YR, sosedCar):
            try:
                file.write("    Вставляем скважину в новый маршрут" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client][sosedCar] += timeWork

                # на случай если мы в итоге все скважины забрали, и эта была последняя
                if flag == 'last':
                    file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                               "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                    XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientCar)

                XR[sosed][client][sosedCar] = 1
                XR[client][sosed][sosedCar] = 1
                YR[sosed][sosedCar] = 1
                YR[client][sosedCar] = 1  # теперь машина соседа обслуживает клиента

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
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, sizeK, iteration, "Help", file)
                file.write("OperatorJoinFromHelp stop: <-\n")
                return XR, YR, SR, AR, targetR, sizeK
            except TypeError:
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, target_function_start, sizeK_start

        # Выбор минимума
        if sosedLeft != -1 or sosedRight != -1:
            file.write("    Теперь ищем минимум из двух целевых" + '\n')
            minimum = min(targetL, targetR)
            if minimum == targetL and minimum != -1:
                file.write("    Выбрали левого у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return Xl, Yl, Sl, Al, targetL, sizeK

            elif minimum == targetR and minimum != -1:
                file.write("    Выбрали правого у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return XR, YR, SR, AR, targetR, sizeK

            else:
                file.write("    Все пошло по пизде ничего не сохранили" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, target_function_start, sizeK_start

    file.write("    В этом маршруте есть такой объек, вернемся к нему позже\n")
    file.write("OperatorJoinFromHelp stop: <-\n")
    return x, y, s, a, target_function_start, sizeK_start


def OperatorJoinFromExchange(x, y, s, a, sizeK, target_function, sequenceX2, client, clientCar, subseq1,
                             sosed, sosedCar, subseq2, iteration, file):
    file.write("->OperatorJoinFromExchange start" + '\n')

    SizeK = sizeK
    TargetFunction = target_function
    X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)

    subseq1Left = SearchSosedLeftOrRight(X, Y, subseq1[0], "left", clientCar)  # левый сосед клиента
    subseq1Right = SearchSosedLeftOrRight(X, Y, subseq1[-1], "right", clientCar)  # левый сосед клиента
    subseq2Left = SearchSosedLeftOrRight(X, Y, subseq2[0], "left", sosedCar)  # правый сосед соседа
    subseq2Right = SearchSosedLeftOrRight(X, Y, subseq2[-1], "right", sosedCar)  # правый сосед соседа

    file.write("    Слева от последовательности клиента " + str(subseq1Left) + " Время работы = " + str(
        Sresh[subseq1Left][clientCar]) + "\n")
    file.write("    Справа от последовательности клиента " + str(subseq1Right) + " Время работы = " + str(
        Sresh[subseq1Right][clientCar]) + "\n")
    file.write("    Слева от последовательности соседа " + str(subseq2Left) + " Время работы = " + str(
        Sresh[subseq2Left][sosedCar]) + "\n")
    file.write("    Справа от последовательности соседа " + str(subseq2Right) + " Время работы = " + str(
        Sresh[subseq2Right][sosedCar]) + "\n")

    time1 = SaveTime(Sresh, subseq1, clientCar, file)
    time2 = SaveTime(Sresh, subseq2, sosedCar, file)

    X, Y, Sresh, A = DeleteTail(X, Y, Sresh, A, subseq1Left, subseq1, clientCar, file, subseq1Right)
    X, Y, Sresh, A = DeleteTail(X, Y, Sresh, A, subseq2Left, subseq2, sosedCar, file, subseq2Right)

    # Сценарий когда какие-нибудь края равны соседям другой последовательности
    if (subseq1[0] == subseq2Left or subseq1[-1] == subseq2Right or
        subseq2[0] == subseq1Left or subseq2[-1] == subseq1Right) and clientCar != sosedCar:
        file.write("    Сценарий когда какие-нибудь края равны соседям другой последовательности\n")

        if subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[0] == subseq2Left остальные не равны\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 0)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[-1] == subseq2Right остальные не равны\n")

            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 0)
            # Sresh[subseq2Right][sosedCar] += time1[-1]

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 0)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right остальные не равны\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            # Sresh[subseq1[-1]][sosedCar] += time1[-1]

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 0)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только эти не равен subseq1[-1] != subseq2Right\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только эти не равен subseq1[0] != subseq2Left\n")

            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 0)
            # Sresh[subseq1[-1]][sosedCar] += time1[-1]

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Все равны\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            # Sresh[subseq1[-1]][sosedCar] += time1[-1]

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    subseq1[0] == subseq2Left and subseq2[-1] == subseq1Right остальные не равны\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 0)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    subseq1[-1] == subseq2Right and subseq2[-1] == subseq1Right остальные не равны\n")

            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 0)
            # Sresh[subseq1[-1]][sosedCar] += time1[-1]

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 0)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только эти не равны subseq2[0] != subseq1Left\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            # Sresh[subseq1[-1]][sosedCar] += time1[-1]

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 0)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[0] == subseq2Left and subseq2[0] == subseq1Left остальные не равны\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq2[0] == subseq1Left and subseq1[-1] == subseq2Right остальные не равны\n")

            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 0)
            # Sresh[subseq1[-1]][sosedCar] += time1[-1]

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    Только этот не равен subseq2[-1] != subseq1Right\n")

            Sresh[subseq1[0]][sosedCar] += time1[0]
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 1)
            # Sresh[subseq1[-1]][sosedCar] += time1[-1]

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right\n")

            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 0)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    Только это равно subseq2[0] == subseq1Left\n")

            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 0)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Sresh[subseq2[0]][clientCar] += time2[0]
            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только этот равен subseq2[-1] == subseq1Right\n")

            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1, 0)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2, 0)
            # Sresh[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Sresh, file)

        try:
            X, Y, Sresh, A, Target_Function, SizeK = Checker(X, Y, Sresh, A, SizeK, iteration, "Exchange", file)
            PrintForCar(X, Sresh, clientCar, file, sosedCar)
            file.write("OperatorJoinFromExchange stop: <-\n")
            return X, Y, Sresh, A, Target_Function, SizeK
        except TypeError:
            # for i in range(factory.N):
            #     file.write("Scl = " + str(Sresh[i][clientCar]) + ' ')
            # file.write('\n')
            #
            # for i in range(factory.N):
            #     file.write("Ssos = " + str(Sresh[i][sosedCar]) + ' ')
            # file.write('\n')

            file.write("OperatorJoinFromExchange stop: <-\n")
            return x, y, s, a, target_function, sizeK

    else:
        if clientCar == sosedCar:
            file.write("    Сценарий когда меняем местами в одной машине\n")
        else:
            file.write("    Сценарий когда никакие края не равны с соседями из другой последовательности\n")

        if clientCar == sosedCar \
                and (sequenceX2[clientCar].index(subseq1[-1]) + 1 == sequenceX2[clientCar].index(subseq2[0])
                     or sequenceX2[clientCar].index(subseq2[-1]) + 1 == sequenceX2[clientCar].index(subseq1[0])):
            file.write("    Сценарий, когда последовательности идут друг за другом\n")
            if sequenceX2[clientCar].index(subseq1[-1]) + 1 == sequenceX2[clientCar].index(subseq2[0]):
                X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2)
                X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, clientCar, time1)
                X[subseq1Left][subseq2Right][clientCar] = 1

                A = TimeOfArrival(X, Y, Sresh, file)

            elif sequenceX2[clientCar].index(subseq2[-1]) + 1 == sequenceX2[clientCar].index(subseq1[0]):
                X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, clientCar, time1)
                X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2)
                X[subseq2Left][subseq1Right][clientCar] = 1

                A = TimeOfArrival(X, Y, Sresh, file)

        else:
            X, Y, Sresh, subseq2Left = AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, sosedCar, time1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            X, Y, Sresh, subseq1Left = AddSubSeqInPath(X, Y, Sresh, subseq2, subseq1Left, clientCar, time2)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Sresh, file)

        try:
            X, Y, Sresh, A, Target_Function, SizeK = Checker(X, Y, Sresh, A, SizeK, iteration, "Exchange", file)
            PrintForCar(X, Sresh, clientCar, file, sosedCar)
            file.write("OperatorJoinFromExchange stop: <-\n")
            return X, Y, Sresh, A, Target_Function, SizeK
        except TypeError:
            file.write("OperatorJoinFromExchange stop: <-\n")
            return x, y, s, a, target_function, sizeK
