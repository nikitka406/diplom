from functionFromCross import *


# рекурсивный поиск для скрещивания
# bufer_in- где ищем(Куда едем), bufer_out- откуда идем
# bufer_out[i_out] - последний добавленный клиент в новый маршрут
# i_out - номер последнего добавленног клиента
# i - номер куда будем добавлять в ребенке
# flag флаг для машины
# flagAll флаг для всего решения
# countOfRaces - сколько машин мжно отправить на локацию
def RecursiveSearchSosedFromAex(children, bufer_in, bufer_out, i_out, flag, flagAll, countOfRaces, numberInCar, file):
    file.write("RecursiveSearchSosedFromAex start: ->\n")
    # номер позиции клиента bufer_out[i_out][0] в bufer_in
    i_in = NumberClientaInSequence(bufer_in, bufer_out[i_out][0])

    file.write("Ищем " + str(bufer_out[i_out][0]) + '\n')
    file.write("Из" + str(bufer_out) + '\n')
    file.write("В" + str(bufer_in) + '\n')
    file.write("Нашли на индексе " + str(i_in) + '\n')
    file.write("Флаг машины " + str(flag) + '\n')
    file.write("Флаг решения " + str(flagAll) + '\n')
    file.write("Сколько раз к каждому клиенту можно приехать " + str(countOfRaces) + '\n')
    file.write("Число клиентов на одной машине (между нулями) " + str(numberInCar) + '\n')

    # смотрим что этот город еще можно вставлять, в этот маршрут
    # и что у него есть свободные скважины
    # и что конкретно это ребро мы еще не использовали
    # bufer_in[i_in + 1.txt] - новый, которого хотим добавить
    # Здесь все заебись, проверено программой!!!!!!!!!!
    if flag[bufer_in[i_in + 1][0]] == 0 and countOfRaces[bufer_in[i_in + 1][0]] \
            > 0 and bufer_in[i_in][1] == 0:

        file.write("Вставляем в ребенка город " + str(bufer_in[i_in + 1][0]) +
                   ", у которого есть свободные скважины, через ребро которое из решения " + '\n')
        file.write(str(bufer_in) + '\n')
        file.write(" еще не использовали и которого на этой машине еще не посещали" + '\n')

        # добавляем в ребенка bufer_in[i_in + 1.txt]
        children.append([bufer_in[i_in + 1][0], 0])

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # ставим флажки
        flag[bufer_in[i_in + 1][0]] += 1
        flagAll[bufer_in[i_in + 1][0]] = 1

        # Уменьшаем кол-во машин которые к этому клиенту могут приехать
        countOfRaces[bufer_in[i_in + 1][0]] -= 1

        # плюс один клиент в машине
        numberInCar += 1

        file.write("Ребенок выглядит пока вот так " + '\n')
        file.write(str(children) + '\n')
        file.write("______________________________" + '\n')

        RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in + 1, flag, flagAll, countOfRaces, numberInCar,
                                    file)

    # если конкретно это ребро уже использовали, то
    elif bufer_in[i_in][1] != 0:

        file.write("Конкрентно это ребро уже использовали" + '\n')

        file.write("Выбираю другое ребро но из такого же начала" +
                   str(bufer_in[i_in][
                           0]) + ", но которое не посещали в этом маршруте, у которого еще есть свободные скважины" + '\n')

        i_in_buf = AnotherEdgeWithTheSameBeginning(bufer_in, bufer_in[i_in][0], flag, countOfRaces)
        # Если нашли такой индекс
        if i_in_buf != -1:
            file.write(
                "Нашли такое же начало" + str(bufer_in[i_in_buf][0]) + ", его индекс в последовательности " + '\n')
            file.write(str(bufer_in) + '\n')
            file.write(" равен" + str(i_in_buf) + '\n')

            # добавляем в ребенка bufer_in[i_in + 1.txt]
            children.append([bufer_in[i_in_buf + 1][0], 0])

            # Ставим флаг в последовательности в которой искали ребро в доп ячееки
            bufer_in[i_in_buf][1] = 1

            # ставим флажки
            flag[bufer_in[i_in_buf + 1][0]] += 1
            flagAll[bufer_in[i_in_buf + 1][0]] = 1

            # Уменьшаем кол-во машин которые к этому клиенту могут приехать
            countOfRaces[bufer_in[i_in_buf + 1][0]] -= 1

            # плюс один клиент в машине
            numberInCar += 1

            file.write("Ребенок выглядит пока вот так " + '\n')
            file.write(str(children) + '\n')
            file.write("______________________________" + '\n')

            RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in_buf + 1, flag, flagAll, countOfRaces,
                                        numberInCar, file)

        # если не нашли такой индекс
        else:
            file.write("Не нашли такое же начало" + str(bufer_in[i_in][0]) +
                       " . Поэтому ищем такое же начало в другом решении в ")
            file.write(str(bufer_out) + '\n')
            # выбираю другое ребро но из такого же начала в другом решении,
            # но которое не посещали в этом маршруте,
            # у которого еще есть свободные скважины
            i_in_buf = AnotherEdgeWithTheSameBeginning(bufer_out, bufer_in[i_in][0], flag, countOfRaces)
            # Если нашли такой индекс
            if i_in_buf != -1:
                file.write("Нашли такое же начало" + str(bufer_out[i_in_buf][0]) + ", его индекс в последовательности ")
                file.write(str(bufer_out))
                file.write(" равен" + str(i_in_buf) + '\n')

                # добавляем в ребенка bufer_in[i_in + 1.txt]
                children.append([bufer_out[i_in_buf + 1][0], 0])
                # children[i][0] = bufer_out[i_in_buf + 1.txt][0]

                # Ставим флаг в последовательности в которой искали ребро в доп ячееки
                bufer_out[i_in_buf][1] = 1

                # ставим флажки
                flag[bufer_out[i_in_buf + 1][0]] += 1
                flagAll[bufer_out[i_in_buf + 1][0]] = 1

                # Уменьшаем кол-во машин которые к этому клиенту могут приехать
                countOfRaces[bufer_out[i_in_buf + 1][0]] -= 1

                # плюс один клиент в машине
                numberInCar += 1

                file.write("Ребенок выглядит пока вот так " + '\n')
                file.write(str(children) + '\n')
                file.write("______________________________" + '\n')

                RecursiveSearchSosedFromAex(children, bufer_in, bufer_out, i_in_buf + 1, flag, flagAll, countOfRaces,
                                            numberInCar, file)

            else:
                file.write("Не нашли такое же начало ни в одном из решений. Поэтому берем рандомного" + '\n')
                if numberInCar >= factory.param_min_num_cl_in_car:

                    next_client = random.randint(0, factory.N - 1)
                    # номер позиции клиента bufer_out[i_out] в bufer_in
                    i_in = NumberClientaInSequence(bufer_in, next_client)

                elif numberInCar < factory.param_min_num_cl_in_car:

                    next_client = random.randint(1, factory.N - 1)
                    # номер позиции клиента bufer_out[i_out] в bufer_in
                    i_in = NumberClientaInSequence(bufer_in, next_client)

                else:
                    file.write("ERROR from in random client: Кол-во клиентов в маршруте сломалось" + '\n')

                file.write("Берем рандомного клиента " + str(next_client) + '\n')

                file.write("Номер позиции рандомного клиента в " + '\n')
                file.write(str(bufer_in) + '\n')
                file.write("равен " + str(i_in) + '\n')

                # ищем нового клиента, пока не найдем не посещенного (flag[next_client] == 0) и у которого
                # остались свободные скважины (countOfRaces[next_client] > 0)
                # Здесь все заебись, проверенно программой!!!!!!!!!!
                count = 0
                while ((flag[next_client] == 1 and countOfRaces[next_client]
                        <= 0) or (flag[next_client] == 0 and countOfRaces[next_client]
                                  <= 0) or (flag[next_client] == 1 and countOfRaces[next_client]
                                            > 0)) and count <= factory.N:
                    file.write("Рандомный" + str(next_client) + "не подошел, так как мы его либо посещали на "
                                                                "этой машине либо нет свободных скважин" + '\n')

                    # счетчик, чтобы вайл не был бесконечным
                    count += 1

                    if numberInCar >= factory.param_min_num_cl_in_car:

                        next_client = random.randint(0, factory.N - 1)
                        # номер позиции клиента bufer_out[i_out] в bufer_in
                        i_in = NumberClientaInSequence(bufer_in, next_client)

                    elif numberInCar < factory.param_min_num_cl_in_car:

                        next_client = random.randint(1, factory.N - 1)
                        # номер позиции клиента bufer_out[i_out] в bufer_in
                        i_in = NumberClientaInSequence(bufer_in, next_client)

                    else:
                        file.write("ERROR from in random client: Кол-во клиентов в маршруте сломалось" + '\n')

                # Означает что нашли рандомного
                if count <= factory.N:
                    file.write("Итоговый рандомный клиент " + str(next_client) + '\n')
                    file.write("И его позиция в " + '\n')
                    file.write(str(bufer_in) + '\n')
                    file.write("равна" + str(i_in) + '\n')

                    # это значит что встретили ноль, цикл должен завершится
                    if flag[next_client] == -1 and numberInCar >= factory.param_min_num_cl_in_car:
                        file.write("Рандомный оказался 0, поэтому цикл должен завершится" + '\n')

                        # добавляем в ребенка bufer_in[i_in + 1.txt]
                        children.append([next_client, 0])
                        # children[i][0] = next_client

                        # ставим влаг
                        flag[next_client] += 1
                        flagAll[next_client] = 1

                        # зануляем сяетчик, так как следом будет уже другая машина
                        numberInCar = 0

                        file.write("Ребенок выглядит пока вот так " + '\n')
                        file.write(str(children) + '\n')
                        file.write("Переходим к следующей машине" + '\n')
                        file.write("_______________________________________"
                                   "________________________________________________________" + '\n')

                        return True

                    # смотрим что этот город еще можно вставлять
                    # Здесь все заебись, проверенно программой!!!!!!!!!!
                    elif flag[next_client] == 0:
                        file.write("Вставляем " + str(next_client) + "в ребенка" + '\n')

                        # добавляем в ребенка bufer_in[i_in + 1.txt]
                        children.append([next_client, 0])

                        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
                        # bufer_in[i_in][1.txt] = 1.txt

                        # ставим флажки
                        flag[next_client] += 1
                        flagAll[next_client] = 1

                        # Уменьшаем кол-во машин которые к этому клиенту могут приехать
                        countOfRaces[next_client] -= 1

                        # плюс один клиент в машине
                        numberInCar += 1

                        file.write("Ребенок выглядит пока вот так " + '\n')
                        file.write(str(children) + '\n')
                        file.write("______________________________" + '\n')

                        RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces,
                                                    numberInCar, file)

                    else:
                        file.write(
                            "ERROR from RecursiveSearchSosedFromAex inside: ошибка в поске рандомного нового клиента" + '\n')

                # Означает что вывалились из вайла,
                # потому что долго ждали, поэтому возвращаем машину в депо
                else:
                    file.write(
                        "Слишком долго искали рандомного, while закончился по времени. Поэтому возвращаемся в депо." + '\n')
                    # добавляем в ребенка bufer_in[i_in + 1.txt]
                    children.append([0, 0])
                    # children[i][0] = 0

                    # # Ставим флаг в последовательности в которой искали ребро в доп ячееки
                    # bufer_in[i_in][1.txt] = 1.txt

                    # ставим влаг
                    flag[0] += 1
                    flagAll[0] = 1

                    # зануляем сяетчик, так как следом будет уже другая машина
                    numberInCar = 0

                    file.write("Ребенок выглядит пока вот так " + '\n')
                    file.write(str(children) + '\n')
                    file.write("Переходим к следующей машине" + '\n')
                    file.write(
                        "_______________________________________________________________________________________________" + '\n')

                    return True

    # Если мы его на этом ТС уже посещали, то нужно взять рандомного
    # или у него больше не хватает скважин но по этому ребру еще не ехали
    # и главное чтобы он не был нулем
    elif (flag[bufer_in[i_in + 1][0]] == 1 or countOfRaces[bufer_in[i_in + 1][0]] <= 0) and bufer_in[i_in + 1][0] != 0:
        file.write(
            "Клиента " + str(bufer_in[i_in + 1][0]) + "на этом ТС уже посещали или у него нет свободных скважин" + '\n')

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        if numberInCar >= factory.param_min_num_cl_in_car:

            next_client = random.randint(0, factory.N - 1)
            # номер позиции клиента bufer_out[i_out] в bufer_in
            i_in = NumberClientaInSequence(bufer_in, next_client)

        elif numberInCar < factory.param_min_num_cl_in_car:

            next_client = random.randint(1, factory.N - 1)
            # номер позиции клиента bufer_out[i_out] в bufer_in
            i_in = NumberClientaInSequence(bufer_in, next_client)

        else:
            file.write("ERROR from in random client: Кол-во клиентов в маршруте сломалось" + '\n')

        file.write("Берем рандомного клиента " + str(next_client) + '\n')

        file.write("Номер позиции рандомного клиента в " + '\n')
        file.write(str(bufer_in) + '\n')
        file.write("равен " + str(i_in) + '\n')

        # ищем нового клиента, пока не найдем не посещенного и у которого
        # остались свободные скважины
        # Здесь все заебись!!!!!!!!!!
        count = 0
        while ((flag[next_client] == 1 and countOfRaces[next_client]
                <= 0) or (flag[next_client] == 0 and countOfRaces[next_client]
                          <= 0) or (flag[next_client] == 1 and countOfRaces[next_client]
                                    > 0)) and count <= factory.N:
            file.write("Рандомный" + str(next_client) + "не подошел, так как мы его либо посещали на "
                                                        "этой машине либо нет свободных скважин" + '\n')

            # счетчик, чтобы вайл не был бесконечным
            count += 1

            if numberInCar >= factory.param_min_num_cl_in_car:

                next_client = random.randint(0, factory.N - 1)
                # номер позиции клиента bufer_out[i_out] в bufer_in
                i_in = NumberClientaInSequence(bufer_in, next_client)

            elif numberInCar < factory.param_min_num_cl_in_car:

                next_client = random.randint(1, factory.N - 1)
                # номер позиции клиента bufer_out[i_out] в bufer_in
                i_in = NumberClientaInSequence(bufer_in, next_client)

            else:
                file.write("ERROR from in random client: Кол-во клиентов в маршруте сломалось" + '\n')

        # Означает что нашли рандомного
        if count <= factory.N:
            file.write("Итоговый рандомный клиент " + str(next_client) + '\n')
            file.write("И его позиция в " + '\n')
            file.write(str(bufer_in) + '\n')
            file.write("равна" + str(i_in) + '\n')

            # это значит что встретили ноль, цикл должен завершится
            if flag[next_client] == -1 and numberInCar >= factory.param_min_num_cl_in_car:
                file.write("Рандомный оказался 0, поэтому цикл должен завершится" + '\n')

                # добавляем в ребенка bufer_in[i_in + 1.txt]
                children.append([next_client, 0])
                # children[i][0] = next_client

                # ставим влаг
                flag[next_client] += 1
                flagAll[next_client] = 1

                # зануляем сяетчик, так как следом будет уже другая машина
                numberInCar = 0

                file.write("Ребенок выглядит пока вот так " + '\n')
                file.write(str(children) + '\n')
                file.write("Переходим к следующей машине" + '\n')
                file.write(
                    "_______________________________________________________________________________________________" + '\n')

                return True

            # смотрим что этот город еще можно вставлять
            # Здесь все заебись, проверенно программой!!!!!!!!!!
            elif flag[next_client] == 0:
                file.write("Вставляем " + str(next_client) + "в ребенка" + '\n')

                # добавляем в ребенка bufer_in[i_in + 1.txt]
                children.append([next_client, 0])

                # Ставим флаг в последовательности в которой искали ребро в доп ячееки
                # bufer_in[i_in][1.txt] = 1.txt

                # ставим флажки
                flag[next_client] += 1
                flagAll[next_client] = 1

                # Уменьшаем кол-во машин которые к этому клиенту могут приехать
                countOfRaces[next_client] -= 1

                # плюс один клиент в машине
                numberInCar += 1

                file.write("Ребенок выглядит пока вот так " + '\n')
                file.write(str(children) + '\n')
                file.write("______________________________" + '\n')

                RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces,
                                            numberInCar, file)

            else:
                file.write(
                    "ERROR from RecursiveSearchSosedFromAex inside: ошибка в поске рандомного нового клиента" + '\n')

        # Означает что вывалились из вайла,
        # потому что долго ждали, поэтому возвращаем машину в депо
        else:
            file.write(
                "Слишком долго искали рандомного, while закончился по времени. Поэтому возвращаемся в депо." + '\n')
            # добавляем в ребенка bufer_in[i_in + 1.txt]
            children.append([0, 0])
            # children[i][0] = 0

            # # Ставим флаг в последовательности в которой искали ребро в доп ячееки
            # bufer_in[i_in][1.txt] = 1.txt

            # ставим влаг
            flag[0] += 1
            flagAll[0] = 1

            # зануляем сяетчик, так как следом будет уже другая машина
            numberInCar = 0

            file.write("Ребенок выглядит пока вот так " + '\n')
            file.write(str(children) + '\n')
            file.write("Переходим к следующей машине" + '\n')
            file.write(
                "_______________________________________________________________________________________________" + '\n')

            return True

    # Если уже встретили ноль, но в последовательности слишком мало клиентов
    elif flag[bufer_in[i_in + 1][0]] == -1 and numberInCar < factory.param_min_num_cl_in_car:
        file.write("Слишком рано встретили ноль, в последовательности только" + str(numberInCar) + " клиент" + '\n')

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # берем рандомного клиента у кторого есть не посещенные скважины
        file.write(
            "Берем рандомного клиента у кторого есть не посещенные скважины с помощью функции RandNotVisitClient" + '\n')
        rand_client = RandNotVisitClient(countOfRaces, flag, file)

        # Нашли рандомного клиента
        if rand_client != -1:
            # номер позиции клиента bufer_out[i_out][0] в bufer_in
            i_in = NumberClientaInSequence(bufer_in, rand_client)
            file.write("Новый рандомный клиент " + str(rand_client) + "находится под номером " + str(
                i_in) + "в последовательности " + '\n')
            file.write(str(bufer_in) + '\n')

            # добавляем в ребенка bufer_in[i_in + 1]
            children.append([rand_client, 0])

            # ставим флажки
            flag[bufer_in[i_in][0]] = 1
            flagAll[bufer_in[i_in][0]] = 1

            # Уменьшаем кол-во машин которые к этому клиенту могут приехать
            countOfRaces[bufer_in[i_in][0]] -= 1

            # плюс один клиент в машине
            numberInCar += 1

            file.write("Ребенок выглядит пока вот так " + '\n')
            file.write(str(children) + '\n')
            file.write("______________________________" + '\n')

            RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces, numberInCar,
                                        file)

        elif rand_client == -1:
            file.write("Возвращаемся в депо" + '\n')
            # добавляем в ребенка bufer_in[k_in][i_in + 1.txt]
            children.append([0, 0])

            # Ставим флаг в последовательности в которой искали ребро в доп ячееки
            bufer_in[i_in][1] = 1

            # ставим влаг
            flag[0] = 1
            flagAll[0] = 1

            # зануляем сяетчик, так как следом будет уже другая машина
            numberInCar = 0

            file.write("Ребенок выглядит пока вот так " + '\n')
            file.write(str(children) + '\n')
            file.write("Переходим к следующей машине" + '\n')
            file.write(
                "_______________________________________________________________________________________________________" + '\n')
            return True

    # это значит что встретили ноль, цикл должен завершится
    # Здесь все заебись, проверенно программой!!!!!!!!!!
    elif flag[bufer_in[i_in + 1][0]] == -1 and numberInCar >= factory.param_min_num_cl_in_car:
        file.write("Встретили 0 пора возвращаться в депо" + '\n')
        # добавляем в ребенка bufer_in[k_in][i_in + 1.txt]
        children.append([bufer_in[i_in + 1][0], 0])

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # ставим влаг
        flag[bufer_in[i_in + 1][0]] = 1
        flagAll[bufer_in[i_in + 1][0]] = 1

        # зануляем сяетчик, так как следом будет уже другая машина
        numberInCar = 0

        file.write("Ребенок выглядит пока вот так " + '\n')
        file.write(str(children) + '\n')
        file.write("Переходим к следующей машине" + '\n')
        file.write(
            "_______________________________________________________________________________________________________" + '\n')
        return True

    else:
        file.write(
            "ERROR from RecursiveSearchSosedFromAex outside: проблема с флагами, не нашли не ноль, не еще не посещенный" + '\n')


# Поиск депо из которого не выезжали
# jndex - индекс у ребенка
# ЗАебись!!!
def SearchForAnUnvisitedZero(bufer1, size1, bufer2, size2, flagAll, countOfRaces, children, flag, numberInCar, file):
    file.write("SearchForAnUnvisitedZero start: ->\n")
    # TODO надо просмотреть
    # #Сначала проверим есть ли те которых мне не посетили ни разу
    # if sum(flagAll) <= factory.N:
    #

    # ищем в первом, в большем решении
    for i in range(size1 - 1):
        # bufer1[i][0] == 0 ищем ноль,
        # bufer1[i][1.txt] == 0 из которого еще не выезжали
        # bufer1[i+1.txt][0] > 0 у которого еще есть свободные скважины
        if bufer1[i] == [0, 0] and countOfRaces[bufer1[i + 1][0]] > 0:
            file.write("Нашли 0 в решении" + '\n')
            file.write("    " + str(bufer1) + '\n')
            file.write("из которого еще не выезжали и первый после него со скважинами " + str(bufer1[i + 1][0]) + '\n')

            bufer1[i][1] = 1
            AddClientaInSequence(children, bufer1, flag, flagAll, countOfRaces, i + 1, file)
            RecursiveSearchSosedFromAex(children, bufer2, bufer1, i + 1, flag, flagAll, countOfRaces, numberInCar, file)
            return
            # return i+1.txt

    # если не нашли в большем, ищем в меньшем
    for i in range(size2 - 1):
        # bufer2[i][0] == 0 ищем ноль,
        # bufer2[i][1.txt] == 0 из которого еще не выезжали
        # countOfRaces[bufer2[i + 1.txt][0]] > 0 у которого еще есть свободные скважины
        if bufer2[i] == [0, 0] and countOfRaces[bufer2[i + 1][0]] > 0:
            file.write("Не нашли 0 в решении" + '\n')
            file.write("    " + str(bufer1) + '\n')
            file.write("но, нашли 0 в решении" + '\n')
            file.write("    " + str(bufer2) + '\n')
            file.write("из которого еще не выезжали и первый после него со скважинами " + str(bufer2[i + 1][0]) + '\n')

            bufer2[i][1] = 1
            AddClientaInSequence(children, bufer2, flag, flagAll, countOfRaces, i + 1, file)
            RecursiveSearchSosedFromAex(children, bufer1, bufer2, i + 1, flag, flagAll, countOfRaces, numberInCar, file)
            return
            # return i+1.txt

    # если не нашли ноль, то ищем просто не посещенного
    for i in range(factory.N):
        # Если в первом и вотором не нашли то ищем просто не посещенный
        # впринципе и у которого есть свободные скважины!!
        if flagAll[i] == 0 and countOfRaces[i] > 0:
            file.write("Не нашли 0 из которого еще не выезжали ни в одном из решений" + '\n')
            file.write("Значит ищем у кого вообще остались скважины" + '\n')
            file.write(
                "Нашли " + str(i) + " город у которого еще есть скважины и в этом решении его не посещали" + '\n')

            # Если нашли такого, то ищем этот город в большем решении
            # и из него мы еще не выезжали
            for j in range(size1 - 1):
                # bufer1[i][0] == 0 ищем этот итый город,
                # bufer1[i][1.txt] == 0 из которого еще не выезжали
                if bufer1[j][0] == i and bufer1[j][1] == 0:
                    file.write("Нашли этот город в решении" + '\n')
                    file.write("    " + str(bufer1) + '\n')
                    AddClientaInSequence(children, bufer1, flag, flagAll, countOfRaces, j, file)
                    RecursiveSearchSosedFromAex(children, bufer2, bufer1, j, flag, flagAll, countOfRaces, numberInCar,
                                                file)
                    return
                    # return j
            # если не нашли в большем, ищем в меньшем
            for j in range(size2 - 1):
                # bufer2[i][0] == 0 ищем ноль,
                # bufer2[i][1.txt] == 0 из которого еще не выезжали
                if bufer2[j][0] == 0 and bufer2[j][1] == 0:
                    file.write("Нашли этот город в решении" + '\n')
                    file.write("    " + str(bufer1) + '\n')
                    AddClientaInSequence(children, bufer2, flag, flagAll, countOfRaces, j, file)
                    RecursiveSearchSosedFromAex(children, bufer1, bufer2, j, flag, flagAll, countOfRaces, numberInCar,
                                                file)
                    return
                    # return j

    file.write("Notification from SearchForAnUnvisitedZero: не нашли куда ехать" + '\n')
    file.write("SearchForAnUnvisitedZero stop: <-\n")


# Рекурсия для HGreX
def RecursiveSearchSosedFromHGreX(children, inserted, sequence1, sequence2, flagAll, flag, numberInCar):
    if inserted == 0:
        return
    # TODO для начала надо разсмотреть ситуацию если ноль
    print("Добавили в ребенка ", inserted)
    children.append([inserted, 0])
    flag[inserted] = 1
    flagAll[inserted] += 1
    numberInCar += 1
    print("Ребенок сейчас выглядит вот так ", children)
    print("flag = ", flag)
    print("flagAll = ", flagAll)

    index = sequence1.index([inserted, 0])
    sequence1[index][1] = 1
    jndex = sequence2.index([inserted, 0])

    i = sequence1[index + 1][0]
    j = sequence2[jndex + 1][0]
    print("Объект из sequence1 = ", i)
    print("Объект из sequence2 = ", j)

    if numberInCar < factory.param_min_num_cl_in_car:
        print("В машине еще не достаточно клиентов чтобы в любой момент вернуться в депо")
        if factory.t[inserted][i] < factory.t[inserted][j] and i != 0 and flag[i] == 0 and \
                sequence1[index + 1][1] == 0 and flagAll[i] <= factory.wells[i]:
            print("Если i < j и i не ноль и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, i, sequence1, sequence2, flagAll, flag, numberInCar)

        elif factory.t[inserted][i] < factory.t[inserted][j] and j != 0 and flag[j] == 0 and \
                sequence2[jndex + 1][1] == 0 and flagAll[j] <= factory.wells[j]:
            print("Если i < j и j не ноль и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, j, sequence2, sequence1, flagAll, flag, numberInCar)

        elif factory.t[inserted][i] >= factory.t[inserted][j] and j != 0 and flag[j] == 0 and \
                sequence2[jndex + 1][1] == 0 and flagAll[j] <= factory.wells[j]:
            print("Если j < i и j не ноль и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, j, sequence2, sequence1, flagAll, flag, numberInCar)

        elif factory.t[inserted][i] >= factory.t[inserted][j] and i != 0 and flag[i] == 0 and \
                sequence1[index + 1][1] == 0 and flagAll[i] <= factory.wells[i]:
            print("Если j < i и j не ноль и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, i, sequence1, sequence2, flagAll, flag, numberInCar)

        else:
            print("Не получилось вставить самое короткое выходящие ребро, попробуем просто самое короткое")
            ti = factory.t[inserted].copy()
            print("Кондидаты на выбор самого короткого ", ti)

            minimum = min(ti)
            index = ti.index(minimum)
            print("Самое короткое ребро = ", index)
            ti[index] = 999999
            print("Теперь кондидаты выглядят так")

            while index == inserted or index == 0:
                print("Предыдущие короткое ребро не подошло ищем новое")
                minimum = min(ti)
                index = ti.index(minimum)
                print("Самое короткое ребро = ", index)
                ti[index] = 999999
                print("Теперь кондидаты выглядят так")

            print("Итоговое короткое ребро = ", index)
            print("Добавим его через рекурсию")
            number = random.randint(1, 2)
            if number == 1:
                RecursiveSearchSosedFromHGreX(children, index, sequence1, sequence2, flagAll, flag, numberInCar)
            elif number == 2:
                RecursiveSearchSosedFromHGreX(children, index, sequence2, sequence1, flagAll, flag, numberInCar)

    elif numberInCar >= factory.param_min_num_cl_in_car:
        print("В машине уже достаточно клиентов чтобы в любой момент вернуться в депо")
        if factory.t[inserted][i] < factory.t[inserted][j] and flag[i] == 0 and \
                sequence1[index + 1][1] == 0 and flagAll[i] <= factory.wells[i]:
            print("Если i < j и i и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, i, sequence1, sequence2, flagAll, flag, numberInCar)

        elif factory.t[inserted][i] < factory.t[inserted][j] and flag[j] == 0 and \
                sequence2[jndex + 1][1] == 0 and flagAll[j] <= factory.wells[j]:
            print("Если i < j и j и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, j, sequence2, sequence1, flagAll, flag, numberInCar)

        elif factory.t[inserted][i] >= factory.t[inserted][j] and flag[j] == 0 and \
                sequence2[jndex + 1][1] == 0 and flagAll[j] <= factory.wells[j]:
            print("Если j < i и j и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, j, sequence2, sequence1, flagAll, flag, numberInCar)

        elif factory.t[inserted][i] >= factory.t[inserted][j] and flag[i] == 0 and \
                sequence1[index + 1][1] == 0 and flagAll[i] <= factory.wells[i]:
            print("Если j < i и j и в этой машине не посещали и конкретно "
                  "это ребро не брали и есть свободные скважины")
            RecursiveSearchSosedFromHGreX(children, i, sequence1, sequence2, flagAll, flag, numberInCar)

        else:
            print("Не получилось вставить самое короткое выходящие ребро, попробуем просто самое короткое")
            ti = factory.t[inserted].copy()
            print("Кондидаты на выбор самого короткого ", ti)

            minimum = min(ti)
            index = ti.index(minimum)
            print("Самое короткое ребро = ", index)
            ti[index] = 999999
            print("Теперь кондидаты выглядят так")

            while index == inserted or index == 0:
                print("Предыдущие короткое ребро не подошло ищем новое")
                minimum = min(ti)
                index = ti.index(minimum)
                print("Самое короткое ребро = ", index)
                ti[index] = 999999
                print("Теперь кондидаты выглядят так")

            print("Итоговое короткое ребро = ", index)
            print("Добавим его через рекурсию")
            number = random.randint(1, 2)
            if number == 1:
                RecursiveSearchSosedFromHGreX(children, index, sequence1, sequence2, flagAll, flag, numberInCar)
            elif number == 2:
                RecursiveSearchSosedFromHGreX(children, index, sequence2, sequence1, flagAll, flag, numberInCar)