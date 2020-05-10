from operators import *


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


# Добавляем клиента в последовательность, со всеми флагами
# ЗАебись!!!
def AddClientaInSequence(children, bufer, flag, flagAll, countOfRaces, i_in, file):
    file.write("AddClientaInSequence start: ->\n")
    file.write("    Добавляем " + str(bufer[i_in][0]) + "в ребенка с помощью функции AddClientaInSequence" + '\n')
    children.append([bufer[i_in][0], 0])

    # из первого нуля больше никуда не едем
    bufer[i_in][1] = 1

    # Расставляем флажки локально для первой машины и для общего решения
    flag[0] += 1
    flag[bufer[i_in][0]] = 1
    flagAll[bufer[i_in][0]] = 1
    # на одну мащину к нему (bufer1[1.txt]) теперь может приехать меньше
    countOfRaces[bufer[i_in][0]] -= 1

    file.write("    Ребенок выглядит пока вот так " + '\n')
    file.write("    " + str(children) + '\n')
    file.write("    AddClientaInSequence stop: <-\n")
    file.write("______________________________" + '\n')


# Выбор рандомного города из тех у который остались свободные скважины
def RandomClientWithWells(countOfRaces):
    # список в котором будут хранится клиенты в которорых остались скважины
    ostatok = []
    for i in factory.N:
        if countOfRaces[i] > 0:
            ostatok.append(i)
    return random.choise(ostatok)


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


# Выбор первого клиента с минимальным временем начала
def SelectFirstObj(flagAll):
    # Копируем время начала
    E = factory.e.copy()
    E[0] = 99999999

    minimum = min(E)
    print(" Минимальное время начала = ", minimum)

    count_min = E.count(minimum)
    print("Всего ", count_min, " объектов начинают свою работу в это время")

    arrE = []
    print("Создаем массив для объектов с одинаковым временем начала")

    index = 0
    for i in range(count_min):
        index = E.index(minimum, index + 1)
        if flagAll[index] == 0:
            arrE.append(index)
            print("Cейчас массив выглядит следующим образом ", arrE)

    arrL = []
    print("Создаем массив в котором время окончания всех этих объектов")

    for i in range(len(arrE)):
        arrL.append(factory.l[arrE[i]])
        print("Cейчас массив выглядит следующим образом ", arrL)

    minimum = min(arrL)
    count_min = arrL.count(minimum)
    print("Минимальное время окончания из всех этих объектов = ", minimum, " их число = ", count_min)

    result = []
    print("Создаем массив для выбора случайного клиента из тех кто с одинаковым временем окончания")

    index = -1
    for i in range(count_min):
        index = arrL.index(minimum, index + 1)
        result.append(arrE[index])
        print("Cейчас массив выглядит следующим образом ", result)

    E[0] = 0
    return random.choice(result)


# кроссовер AEX
def AEX(sequence1, sequence2, timeCros):
    file = open("log/aexlog.txt", 'a')

    start = time.time()
    timeCros[1] += 1

    file.write("AEX start: ->" + '\n')
    print("Скрещивание решений усуществляется с помощью оператора АЕХ" + '\n')
    # первый индекс это номер машины, второй это последовательность
    # Здесь все заебись!!!!!!!!!!

    # результат скрещивания (РЕБЕНОК)
    children = []

    # число клиентов в текущей машине
    numberInCar = 0

    # сохроняем последовательности чтобы не испортить
    # bufer1 = sequence1
    # bufer2 = sequence2

    # кол-во используемых машин в каждом решение
    size1 = len(sequence1)
    file.write("size1 = " + str(size1) + '\n')
    size2 = len(sequence2)
    file.write("size2 = " + str(size2) + '\n')

    # флаг, для посещенных городов в заключительном решении
    flagAll = [0 for j in range(factory.N)]

    # сколько раз можно заехать к каждому
    countOfRaces = factory.wells.copy()

    file.write("Сколько раз к каждому клиенту можно приехать до оператора AEX " + str(countOfRaces) + '\n')

    # определяем по кому будем делать цикл
    if size1 >= size2:
        file.write("Первая последовательность больше" + '\n')

        # флаг, для посещенных городов в одном маршруте(одной машиной)
        flag = [0 for j in range(factory.N)]
        flag[0] = -2

        # Добавляем первые два города в ребенка
        children.append([sequence1[0][0], 0])
        children.append([sequence1[1][0], 0])
        # children[0][0] = sequence1[0][0]
        # children[1.txt][0] = sequence1[1.txt][0]

        # из первого нуля больше никуда не едем
        sequence1[0][1] = 1

        # Расставляем флажки локально для первой машины и для общего решения
        flag[sequence1[0][0]] += 1
        flag[sequence1[1][0]] = 1
        flagAll[sequence1[0][0]] = 1
        flagAll[sequence1[1][0]] = 1
        # на одну мащину к нему (bufer1[1.txt]) теперь может приехать меньше
        countOfRaces[sequence1[1][0]] -= 1

        # Число задействованных машин в ребенке
        k = 0

        # один клиент в машине
        numberInCar += 1

        file.write("Ребенок выглядит пока вот так " + '\n')
        file.write(str(children) + '\n')
        file.write("______________________________" + '\n')

        # Для первого добавления запустим без цикла
        RecursiveSearchSosedFromAex(children, sequence2, sequence1, 1, flag, flagAll, countOfRaces, numberInCar, file)

        # Обнуляем флаг для следующей машины
        for i in range(factory.N):
            flag[i] = 0
        flag[0] = -2

        # Добавляем еще одну машину + сдвигаем индекс последовательности
        k += 1

        file.write("Построили для первой машины" + '\n')
        file.write(
            "_______________________________________________________________________________________________________" + '\n')
        # Пока кол-во используемых машин не привысило доступного числа  k <= factory.K
        # или остались не посещенные города sum(flagAll) <= factory.N
        counter = 0
        while sum(flagAll) < factory.N and counter <= factory.N * 2:
            file.write("Продолжаем построение с помощью функции SearchForAnUnvisitedZero" + '\n')
            file.write("Хотим найти 0 в каком-нибудь решении из которого еще не выезжали или "
                       "клиента которого еще не посетили в этом решении" + '\n')

            # Поиск номер в последовательности не посещенного нуля
            # или просто не посещенного
            # и его добавление в ребенка с расставлением всех флагов
            # и запуском рекурсии
            SearchForAnUnvisitedZero(sequence1, size1, sequence2, size2, flagAll, countOfRaces, children, flag,
                                     numberInCar, file)

            file.write("Построили для следующей машины" + '\n')
            file.write(
                "_____________________________________"
                "__________________________________________________________________" + '\n')

            # Обнуляем флаг для следующей машины
            for i in range(factory.N):
                flag[i] = 0
            flag[0] = -2

            # Добавляем еще одну машину + сдвигаем индекс последовательности
            k += 1
            counter += 1

    elif size1 < size2:
        file.write("Вторая последовательность больше" + '\n')

        # флаг, для посещенных городов в одном маршруте(одной машиной)
        flag = [0 for j in range(factory.N)]
        flag[0] = -2

        # Добавляем первые два города в ребенка
        children.append([sequence2[0][0], 0])
        children.append([sequence2[1][0], 0])

        # children[0][0] = sequence2[0][0]
        # children[1.txt][0] = sequence2[1.txt][0]

        # из первого нуля больше никуда не едем
        sequence2[0][1] = 1

        # Расставляем флажки локально для первой машины и для общего решения
        flag[sequence2[0][0]] += 1
        flag[sequence2[1][0]] = 1
        flagAll[sequence2[0][0]] = 1
        flagAll[sequence2[1][0]] = 1
        # на одну мащину к нему (bufer1[1.txt]) теперь может приехать меньше
        countOfRaces[sequence2[1][0]] -= 1

        # Число задействованных машин в ребенке
        k = 0

        # один клиент в машине
        numberInCar += 1

        file.write("Ребенок выглядит пока вот так " + '\n')
        file.write(str(children) + '\n')
        file.write("______________________________" + '\n')

        # Для первого добавления запустим без цикла
        RecursiveSearchSosedFromAex(children, sequence1, sequence2, 1, flag, flagAll, countOfRaces, numberInCar, file)

        # Обнуляем флаг для следующей машины
        for i in range(factory.N):
            flag[i] = 0
        flag[0] = -2

        # Добавляем еще одну машину + сдвигаем индекс последовательности
        k += 1

        file.write("Построили для первой машины" + '\n')
        file.write(
            "_______________________________________________________________________________________________________" + '\n')

        # Пока кол-во используемых машин не привысило доступного числа  k <= factory.K
        # или остались не посещенные города sum(flagAll) <= factory.N
        counter = 0
        while sum(flagAll) < factory.N and counter <= factory.N * 2:
            file.write("Продолжаем построение с помощью функции SearchForAnUnvisitedZero" + '\n')
            file.write("Хотим найти 0 в каком-нибудь решении из которого еще не выезжали или "
                       "клиента которого еще не посетили в этом решении" + '\n')
            # Поиск номер в последовательности не посещенного нуля
            # или просто не посещенного
            # и его добавление в ребенка с расставлением всех флагов
            # и запуском рекурсии

            SearchForAnUnvisitedZero(sequence2, size2, sequence1, size1, flagAll, countOfRaces, children, flag,
                                     numberInCar, file)

            file.write("Построили для следующей машиины машины" + '\n')
            file.write(
                "___________________________________________________"
                "____________________________________________________" + '\n')

            # Обнуляем флаг для следующей машины
            for i in range(factory.N):
                flag[i] = 0
            flag[0] = -2

            # Добавляем еще одну машину + сдвигаем индекс последовательности
            k += 1
            counter += 1

    else:
        file.write("ERROR from AEX: исключение, произошло невозможное!!!!" + '\n')

    for i in range(len(children)):
        children[i][1] = 0
    for i in range(len(sequence1)):
        sequence1[i][1] = 0
    for i in range(len(sequence2)):
        sequence2[i][1] = 0

    file.write("Оператор AEX закончил своб работу с решениями" + '\n')
    file.write("sequence1 = " + str(sequence1) + '\n')
    file.write("sequence2 = " + str(sequence2) + '\n')
    file.write("И получился ребенок " + '\n')
    file.write("children = " + str(children) + '\n')
    file.write(
        "______________________________________________________________________________________________________" + '\n')
    print("Оператор AEX закончил своб работу с решениями" + '\n')
    print("sequence1 = " + str(sequence1) + '\n')
    print("sequence2 = " + str(sequence2) + '\n')
    print("И получился ребенок " + '\n')
    print("children = " + str(children) + '\n')
    print(
        "______________________________________________________________________________________________________" + '\n')

    Time = time.time() - start
    timeCros[0] += Time
    file.write("Время работы AEX = " + str(Time) + 'seconds\n')

    file.write("<-AEX stop" + '\n')
    file.close()

    file.close()
    return children, timeCros


# кроссовер HGreX
def HGreX(sequence1, sequence2, aex=0, countOper=0):
    children = [[0, 0]]
    numberInCar = 0
    flag = [0 for i in range(factory.N)]
    flag[0] = -1
    flagAll = [0 for i in range(factory.N)]
    flagAll[0] = 1

    first = SelectFirstObj(flag)
    print("Выбираем случайную вершину = ", first)

    print("Расставляем флаги")
    flagAll[first] += 1
    flag[first] = 1
    print("flag = ", flag)
    print("flagAll = ", flagAll)

    print("Добавили первое ребро в ребенка, ")
    children.append([first, 0])
    numberInCar += 1
    print(children)

    number = random.randint(1, 2)
    if number == 1:
        sequence1[first][1] = 1
    elif number == 2:
        sequence2[first][1] = 1

    index = sequence1.index([first, 0])
    jndex = sequence2.index([first, 0])
    i = sequence1[index + 1][0]
    j = sequence2[jndex + 1][0]

    if factory.t[first][i] < factory.t[first][j] and i != 0:
        print("Если i < j и i не ноль")
        RecursiveSearchSosedFromHGreX(children, i, sequence1, sequence2, flagAll, flag, numberInCar)

    elif factory.t[first][i] < factory.t[first][j] and j != 0:
        print("Если i < j и j не ноль")
        RecursiveSearchSosedFromHGreX(children, j, sequence2, sequence1, flagAll, flag, numberInCar)

    elif factory.t[first][i] >= factory.t[first][j] and j != 0:
        print("Если j < i и j не ноль")
        RecursiveSearchSosedFromHGreX(children, j, sequence2, sequence1, flagAll, flag, numberInCar)

    elif factory.t[first][i] >= factory.t[first][j] and i != 0:
        print("Если j < i и j не ноль")
        RecursiveSearchSosedFromHGreX(children, i, sequence1, sequence2, flagAll, flag, numberInCar)

    else:
        print("Не получилось вставить самое короткое выходящие ребро, попробуем просто самое короткое")
        ti = factory.t[first].copy()
        print("Кондидаты на выбор самого короткого ", ti)

        minimum = min(ti)
        index = ti.index(minimum)
        print("Самое короткое ребро = ", index)
        ti[index] = 999999
        print("Теперь кондидаты выглядят так")

        while index == first or index == 0:
            print("Предыдущие короткое ребро не подошло ищем новое")
            minimum = min(ti)
            index = ti.index(minimum)
            print("Самое короткое ребро = ", index)
            ti[index] = 999999
            print("Теперь кондидаты выглядят так")

        print("Итоговое короткое ребро = ", index)
        print("Добавим его через рекурсию")

        if number == 1:
            RecursiveSearchSosedFromHGreX(children, index, sequence1, sequence2, flagAll, flag, numberInCar)
        elif number == 2:
            RecursiveSearchSosedFromHGreX(children, index, sequence2, sequence1, flagAll, flag, numberInCar)

    return children


# Оператор HRndX
def HRndX(sequence1, sequence2, aex=0, countOper=0):
    return


# Оператор HProX
def HProX(sequence1, sequence2, aex=0, countOper=0):
    return


# Функция вызывает выбранный оператор
def UsedCrossovers(sequence1, sequence2, operator, timeCros):
    print("Запускаем оператор ", operator)
    if operator == 'AEX':
        children, timeCros[0] = AEX(sequence1, sequence2, timeCros[0])
        return children, timeCros

    elif operator == 'HGreX':
        return HGreX(sequence1, sequence2, timeCros[1])

    elif operator == 'HRndX':
        return HRndX(sequence1, sequence2, timeCros[2])

    elif operator == 'HProX':
        return HProX(sequence1, sequence2, timeCros[3])

    else:
        print("ERROR from UsedCrossovers: название такого оператора нет")


# Локальный поиск (локально меняем решение)
def LocalSearch(x, y, s, a, target_function, sizeK, iteration, timeLocal):
    print("Применяем локальный поиск (локально меняем решение)")

    # TODO выбираем оператор локального поиска
    local_search_oper = ['relocate', '2Opt', 'Exchange']
    oper = random.choice(local_search_oper)
    oper = 'Exchange'

    print("Используем оператор ", oper)
    if oper == 'relocate':
        x, y, s, a, target_function, sizeK, timeLocal[0] = Relocate(x, y, s, a, target_function, sizeK, iteration,
                                                                    timeLocal[0])
        # iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal

    elif oper == '2Opt':
        x, y, s, a, target_function, sizeK, timeLocal[1] = Two_Opt(x, y, s, a, target_function, sizeK, iteration,
                                                                   timeLocal[1])
        # iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal

    elif oper == 'Exchange':
        x, y, s, a, target_function, sizeK, timeLocal[3] = Exchange(x, y, s, a, target_function, sizeK, iteration,
                                                                    timeLocal[3])
        # iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal


# Мутация
def Mutation(sequence, file):
    # TODO пересмотеть реализацию
    if ResultCoins(factory.coinsMut):
        file.write(
            "____________________________________________________________________________________________________\n")
        file.write("Начилась мутация\n")
        count_car = CountUsedMachines(sequence)
        file.write("Число используемых машин = " + str(count_car) + "\n")

        buf_random = []
        k = 0
        # print("Последовательность до мутации ")
        # print(sequence)
        for i in range(1, len(sequence)):
            if sequence[i][0] != 0:
                buf_random.append(sequence[i][0])
            elif sequence[i][0] == 0 and len(buf_random) > 1:

                # print("Полученный массив ", buf_random)
                obj1 = int(random.choice(buf_random))
                # print("Берем рандомного клиента ", obj1)
                buf_random.remove(obj1)
                obj2 = int(random.choice(buf_random))
                # print("Берем рандомного клиента ", obj2)
                buf_random.remove(obj2)

                index1 = sequence.index([obj1, 0], k)
                # print("Их места в последовательности ", index1)
                index2 = sequence.index([obj2, 0], k)
                # print("Их места в последовательности ", index2)

                sequence[index1][0] = obj2
                sequence[index2][0] = obj1
                # print("Получившаяся последовательность")
                # print(sequence)

                buf_random = []
                k = i

            elif sequence[i][0] == 0 and len(buf_random) == 1:
                # print("Машина обслуживает только одного клиента, никого никуда не переставляем")
                buf_random = []
                k = i

        file.write("Итоговая, измененая последовательность = \n")
        file.write(str(sequence) + '\n')
        return sequence
    else:
        return sequence


# Функция которая позволяет родить ребенка (скрестить два решения)
# и отдать его в хорошую школу (оператор локального перемещения)
# и дальнейшее его помещение в популяцию решений, если он не хуже всех
# и все это сделает factory.param_crossing раз
def GeneticAlgorithm(Sequence, X, Y, Sresh, A, Target_Function, SizeK, iteration):
    file = open("log/genalog.txt", 'a')
    file.write("GeneticAlgorithm start: ->\n")
    file.write("Начинаем процесс порождения нового решения" + '\n')
    minimumCros = Target_Function[0]
    maximumCros = Target_Function[0]
    minimumLocal = Target_Function[0]
    maximumLocal = Target_Function[0]
    minimumHelp = Target_Function[0]
    maximumHelp = Target_Function[0]
    timeCros = [[0, 0], [0, 0], [0, 0], [0, 0]]  # 0- AEX; 1- HGreX; 2- HRndX; 3- HProX
    timeLocal = [[0, 0], [0, 0], [0, 0], [0, 0]]  # 0- Relocate; 1- TwoOpt; 2- Help 3- Exchange;

    for crossing in range(factory.param_crossing):
        file.write("Запускаем " + str(crossing) + "-ый раз" + '\n')

        # Выбираем по каком сценарию будем брать родителей
        scenario_cross = ['randomAndRandom', 'randomAndBad', 'BestAndRand', 'BestAndBad']
        scenario = random.choice(scenario_cross)
        scenario = 'randomAndRandom'
        file.write("Выбрали сценарий по выбору родителей " + str(scenario) + '\n')

        # Выбираю как буду сохранять полученное решение
        scenario_add_new_solution = ['deleteTheBad', 'deleteTheBadParents']
        scenario_add = random.choice(scenario_add_new_solution)
        # scenario_add = 'deleteTheBad'
        file.write("Выбрали сценарий по сохранению нового решения " + str(scenario_add) + '\n')

        # TODO Задаю список с названиями операторов
        name_crossover = ['AEX', 'HGreX', 'HRndX', 'HProX']
        crossover = random.choice(name_crossover)
        crossover = 'AEX'
        file.write("Выбрали кроссовер для скрещивания" + str(crossover) + '\n')

        # Идем по одному сценарию
        if scenario == 'randomAndRandom':
            file.write("Пошли по сценарию, два рандомных решения" + '\n')
            # Индекс первого родителя
            index = int(random.randint(0, factory.param_population - 1))
            file.write("Номер первого решения " + str(index) + '\n')

            # Индекс второго родителя
            jndex = int(random.randint(0, factory.param_population - 1))
            file.write("Номер второго решения " + str(jndex) + '\n')

            # Если вдруг индекс второго родителя равен первому
            while jndex == index:
                jndex = random.randint(0, factory.param_population - 1)

            file.write(str(Sequence) + '\n')
            file.write("Первое рандомное решение" + '\n')
            file.write(str(Sequence[index]) + '\n')
            file.write("Второе рандомное решение" + '\n')
            file.write(str(Sequence[jndex]) + '\n')

            children, timeCros = UsedCrossovers(Sequence[index], Sequence[jndex], crossover, timeCros)

        elif scenario == 'randomAndBad':
            file.write("Пошли по сценарию, один рандомный второй самый худший" + '\n')
            # Индекс первого родителя
            index = random.randint(0, factory.param_population - 1)
            file.write("Номер первого решения " + str(index) + '\n')

            # Ищем самое большое решение по целевой функции
            maximum = max(Target_Function)
            # Оно будет вторым родителем
            jndex = Target_Function.count(maximum)
            file.write("Номер второго решения " + str(jndex) + '\n')

            file.write(str(Sequence) + '\n')
            file.write("Первое рандомное решение" + '\n')
            file.write(str(Sequence[index]) + '\n')
            file.write("Второе решение, худшие из всех" + '\n')
            file.write(str(Sequence[jndex]) + '\n')

            children, timeCros = UsedCrossovers(Sequence[index], Sequence[jndex], crossover, timeCros)

        elif scenario == 'BestAndRand':
            file.write("Пошли по сценарию, один рандомный второй самый лучший" + '\n')
            # Индекс первого родителя
            index = random.randint(0, factory.param_population - 1)
            file.write("Номер первого решения " + str(index) + '\n')

            # Ищем самое маленькое решение по целевой функции
            minimum = min(Target_Function)
            # Оно будет вторым родителем
            jndex = Target_Function.count(minimum)
            file.write("Номер второго решения " + str(jndex) + '\n')

            file.write(str(Sequence) + '\n')
            file.write("Первое рандомное решение" + '\n')
            file.write(str(Sequence[index]) + '\n')
            file.write("Второе решение, лучшие из всех" + '\n')
            file.write(str(Sequence[jndex]) + '\n')

            children, timeCros = UsedCrossovers(Sequence[index], Sequence[jndex], crossover, timeCros)

        elif scenario == 'BestAndBad':
            file.write("Пошли по сценарию, один самый лудший второй самый худший" + '\n')
            # Ищем самое маленькое решение по целевой функции
            minimum = min(Target_Function)
            # Оно будет первым родителем
            index = Target_Function.count(minimum)
            file.write("Номер первого решения " + str(index) + '\n')

            # Ищем самое большое решение по целевой функции
            maximum = max(Target_Function)
            # Оно будет вторым родителем
            jndex = Target_Function.count(maximum)
            file.write("Номер второго решения " + str(jndex) + '\n')

            file.write(str(Sequence) + '\n')
            file.write("Первое решение, лудшие из всех" + '\n')
            file.write(str(Sequence[index]) + '\n')
            file.write("Второе решение, худшие из всех" + '\n')
            file.write(str(Sequence[jndex]) + '\n')

            children, timeCros = UsedCrossovers(Sequence[index], Sequence[jndex], crossover, timeCros)

        # У ребенка в конце может не быть нуля
        if children[-1] != [0, 0]:
            children.append([0, 0])
        file.write("children = " + str(children) + '\n')
        # Применяем мутацию
        children = Mutation(children, file)

        # Переводим последовательность в матрицы решений
        x, y, s, a, sizek = SequenceDisplayInTheXYSA(children)

        assert VerificationOfBoundaryConditions(x, y, s, a, 'true') == 1
        # Считаем целевую функцию
        target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
        file.write(
            "Целевая функция нового решения после оператора скрещивания и мутации равна " + str(target_function) + '\n')
        minimumCros = min(minimumCros, target_function)
        maximumCros = max(maximumCros, target_function)

        # file.write("Help start" + '\n')
        # x, y, s, a, target_function, sizek, timeLocal[2] = Help(x, y, s, a, target_function, sizek, iteration, timeLocal[2])
        # file.write("Целевая функция нового решения после оператора хелп " + str(target_function) + '\n')
        # minimumHelp = min(minimumHelp, target_function)
        # maximumHelp = max(maximumHelp, target_function)

        # Применяем локальный поиск
        file.write("LocalSearch start\n")
        x, y, s, a, target_function, sizek, iteration, timeLocal = LocalSearch(x, y, s, a, target_function, sizek,
                                                                               iteration, timeLocal)
        file.write("Целевая функция нового решения после локального поиска равна " + str(target_function) + '\n')
        minimumLocal = min(minimumLocal, target_function)
        maximumLocal = max(maximumLocal, target_function)

        # file.write("Help start" + '\n')
        # x, y, s, a, target_function, sizek, timeLocal[2] = Help(x, y, s, a, target_function, sizek, iteration - 1,
        #                                                         timeLocal[2])
        # file.write("Целевая функция нового решения после оператора хелп " + str(target_function) + '\n')
        # minimumHelp = min(minimumHelp, target_function)
        # maximumHelp = max(maximumHelp, target_function)

        # Проверяем что новое решение не хуже самого плохого
        # Ищем самое большое решение по целевой функции
        maximum = max(Target_Function)
        i_max = Target_Function.index(maximum)
        file.write("Самое плохое решение в популяции " + str(maximum) + '\n')

        # Удаляем какое-нибудь решение
        if maximum >= target_function:
            if scenario_add == 'deleteTheBad':
                file.write("Удаляем самое плохое решение в популяции" + '\n')
                X.pop(i_max)
                Y.pop(i_max)
                Sresh.pop(i_max)
                A.pop(i_max)
                Target_Function.pop(i_max)
                Sequence.pop(i_max)
                SizeK.pop(i_max)

            elif scenario_add == 'deleteTheBadParents':
                file.write("Удаляем самого плохого родителя" + '\n')

                if Target_Function[index] <= Target_Function[jndex]:
                    file.write("с целевой функцией " + str(Target_Function[jndex]) + '\n')
                    X.pop(jndex)
                    Y.pop(jndex)
                    Sresh.pop(jndex)
                    A.pop(jndex)
                    Target_Function.pop(jndex)
                    Sequence.pop(jndex)
                    SizeK.pop(jndex)

                elif Target_Function[index] > Target_Function[jndex]:
                    file.write("с целевой функцией " + str(Target_Function[index]) + '\n')
                    X.pop(index)
                    Y.pop(index)
                    Sresh.pop(index)
                    A.pop(index)
                    Target_Function.pop(index)
                    Sequence.pop(index)
                    SizeK.pop(index)

            file.write("Добавляем новое решение в конец" + '\n')
            X.append(x)
            Y.append(y)
            Sresh.append(s)
            A.append(a)
            Target_Function.append(target_function)
            Sequence.append(children)
            SizeK.append(sizek)

        file.write("Число итераций = " + str(iteration) + '\n')
    SaveDateResult("Минимальное значение целевой в поппуляции после кроссовера = " + str(minimumCros))
    SaveDateResult("Максимальное значение целевой в поппуляции после кроссовера = " + str(maximumCros))
    # SaveDateResult("Минимальное значение целевой в поппуляции после оператора хелп = " + str(minimumHelp))
    # SaveDateResult("Максимальное значение целевой в поппуляции после оператора хелп = " + str(maximumHelp))
    SaveDateResult("Минимальное значение целевой в поппуляции после локального поиска= " + str(minimumLocal))
    SaveDateResult("Максимальное значение целевой в поппуляции после локального поиска = " + str(maximumLocal))
    SaveDateResult("Число итераций = " + str(iteration))
    SaveDateResult("Среднее время работы AEX = " + str(timeCros[0][0] / timeCros[0][1]))
    # SaveDateResult("Среднее время работы HGreX = " + str(timeCros[1][0]/timeCros[1][1]))
    # SaveDateResult("Среднее время работы HRndX = " + str(timeCros[2][0]/timeCros[2][1]))
    # SaveDateResult("Среднее время работы HProX = " + str(timeCros[3][0]/timeCros[3][1]))
    # SaveDateResult("Среднее время работы Relocate в эволюции = " + str(timeLocal[0][0] / timeLocal[0][1]))
    # SaveDateResult("Среднее время работы 2-opt в эволюции = " + str(timeLocal[1][0] / timeLocal[1][1]))
    # SaveDateResult("Среднее время работы Help в эволюции = " + str(timeLocal[2][0] / timeLocal[2][1]))
    SaveDateResult("Среднее время работы Exchange в эволюции = " + str(timeLocal[3][0] / timeLocal[3][1]))

    min_result = min(Target_Function)
    number_solution = Target_Function.count(min(Target_Function))
    file.write("Минимальная целевая функция " + str(min_result) + " номер решения " + str(number_solution) + '\n')
    print("Минимальная целевая функция " + str(min_result) + " номер решения " + str(number_solution) + '\n')

    SaveDateResult("Итоговая минимальная целевая функция = " + str(min_result))
    SaveDateResult("Число используемых машин = " + str(AmountCarUsed(Y[number_solution])))
    SaveDateResult("Решение " + str(Sequence[number_solution]))

    for n in range(factory.param_population):
        file.write(str(Sequence[n]) + '\n')

    file.close()


def CheckSequence(Sequence):
    if Sequence.count([0, 0]) != 0 and Sequence.count([1, 0]) != 0 and Sequence.count([2, 0]) != 0 and Sequence.count(
            [3, 0]) != 0 and Sequence.count([4, 0]) != 0 and Sequence.count([5, 0]) != 0 and Sequence.count(
        [6, 0]) != 0 and Sequence.count([7, 0]) != 0 and Sequence.count([8, 0]) != 0 and Sequence.count(
        [9, 0]) != 0:
        return 1
    else:
        return 0
