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
                buf = 0
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
                buf = 0
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


def OperatorJoinFromTwoOpt(x, y, s, a, sizeK, target_function, client1, client1Car, client2, client2Car, iteration,
                           file):
    file.write("OperatorJoinFromTwoOpt start: ->" + '\n')
    SizeK = sizeK
    X, Y, Sresh, A = ReadStartLocalSearchOfFile(SizeK)

    if client1Car != client2Car:

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

    elif client1Car == client2Car:

        tail1 = SearchTail(X, client1, client1Car, file)
        time1 = SaveTime(Sresh, tail1, client1Car, file)

        tail2 = SearchTail(X, client2, client2Car, file)
        time2 = SaveTime(Sresh, tail2, client2Car, file)

        sosed1 = SearchSosedLeftOrRight(X, Y, client1, "left", client1Car)
        sosed2 = SearchSosedLeftOrRight(X, Y, client2, "left", client2Car)
        file.write("    Сосед слева для хвоста один = " + str(sosed1) + '\n')
        file.write("    Сосед слева для хвоста два = " + str(sosed2) + '\n')

        if len(tail1) > len(tail2):

            for i in range(len(tail2)):
                tail1.remove(tail2[i])
                time1.remove(time2[i])

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

            A = TimeOfArrival(X, Y, Sresh, file)

        elif len(tail1) < len(tail2):

            for i in range(len(tail1)):
                tail2.remove(tail1[i])
                time2.remove(time1[i])

            file.write("    Занулим хвост\n")
            X, Y, Sresh, A = DeleteTail(X, Y, Sresh, A, sosed1, tail2, client1Car, file, tail1[0])

            file.write("    Разворачиваем хвост" + '\n')
            tail2.reverse()
            time2.reverse()
            for i in range(len(tail2)):
                X[sosed2][tail2[i]][client2Car] = 1
                Y[tail2[i]][client2Car] = 1
                Sresh[tail2[i]][client2Car] = time2[i]
                sosed2 = tail2[i]

            A = TimeOfArrival(X, Y, Sresh, file)

        try:
            X, Y, Sresh, A, Target_Function, SizeK = Checker(X, Y, Sresh, A, SizeK, iteration, "Two_Opt", file)
            file.write("OperatorJoinFromTwoOpt stop: <-\n")
            return X, Y, Sresh, A, Target_Function, SizeK
        except TypeError:
            file.write("OperatorJoinFromTwoOpt stop: <-\n")
            return x, y, s, a, target_function, sizeK


def OperatorJoinFromHelp(x, y, s, a, sizeK_start, client, clientCar, sosed, sosedCar, target_function_start, iteration,
                         flag, file):
    file.write("OperatorJoinFromHelp start: ->\n")
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
        if sosedRight != -1:
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
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, sizeK, iteration, "Help", file)
            except TypeError:
                targetR = -1
        else:
            targetR = -1

        if sosedLeft != -1:
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
                Xl, Yl, Sl, Al, targetL, sizeK = Checker(Xl, Yl, Sl, Al, sizeK, iteration, "Help", file)
            except TypeError:
                targetL = -1
        else:
            targetL = -1

        if sosed == 0 and sosedRight == -1:
            try:
                file.write("    Вставляем скважину в новый маршрут" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client][sosedCar] += factory.S[client] / factory.wells[client]

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

            elif minimum == targetR and minimum != -1 and targetR != targetL:
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

