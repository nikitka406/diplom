import factory
from function import *
import random


# Создание последовательности для каждого решения
def CreateSequence(X):
    # Создаем спсиок, в которой будем хранить последовательности для каждогоо решения
    sequenceX1 = [0 for n in range(factory.param_population)]
    sequenceX2 = [0 for n in range(factory.param_population)]

    for m in range(factory.param_population):
        # Интерпритируем матрицу Х на двумерный массив
        sequenceX2[m] = GettingTheSequence(X[m])
        sequenceX1[m] = TransferX2toX1(sequenceX2[m], X[m])
        # print(sequenceX1[m], "\n")
    print("Матрица Х из популяция решений преобразованна в последовательность посещений для каждого решения")
    return sequenceX1


# преобразование матрицы Х в последовательность посещения городов,
# bul - порядок посещения
# i-откуда мы сейчас будем уезжать
# k-номер машины
def XDisplayInTheSequenceX2(x, bufer, i, k, bul):
    for j in range(factory.N):
        if x[i][j][k] == 1:
            bul += 1
            bufer[k][bul] = j
            if j != 0:
                XDisplayInTheSequenceX2(x, bufer, j, k, bul)


# Подсчитывает число используемых машин в последовательности
def CountUsedMachines(sequence):
    return sequence.count([0, 0]) - 1


# Выставляем сколько работает каждая машина на локации after
def WorkTimeCounting(sequence, y, s, after):
    local_count = sum(y[after])
    print("На локации ", after, " работает ", local_count, " машин")

    # Считаем сколько хватит каждому скважин
    div = factory.wells[after] // local_count
    if div > 0:
        print("Присваиваем каждой машине, которая работает на локации ", after, " ", div, "кол-во скважин")
        for k in range(len(s[0])):
            if y[after][k] == 1:
                s[after][k] = div * (factory.S[after] / factory.wells[after])

        div = factory.wells[after] % local_count
        if div == 0:
            print("Свободных скважин не осталось, мы все распределили")

        else:
            print("Но у нас еще осталось ", div, " свободных скважин")
            print("Создадим массив, в котором будут номера машин которые обслуживают этот город. Он равен ")

            k = 0
            car_for_after = []
            for i in range(1, len(sequence)):
                if sequence[i][0] == 0 and sequence[i][0] == sequence[-1][0]:
                    k += 1
                elif sequence[i][0] != 0 and sequence[i][0] == after:
                    car_for_after.append(k)

            print(car_for_after)

            print("Распределяем рандомным клиентам оставшиеся скважины")
            while div > 0:
                car = random.choice(car_for_after)
                print("Назначаем машине с номером ", car, " еще одну скважину")
                s[after][car] += factory.S[after] / factory.wells[after]
                car_for_after.remove(car)
                print("Осталось распределить ", div, " скважин по ")
                print(car_for_after, " клиентам")
                div -= 1

    else:
        print("ERROR from WorkTimeCounting: Почему-то оказалось скважин меньше чем приехавших машин")


# Находим время прибытия к after
def ArrivalTime(a, s, before, after, k):
    print("Считаем время прибытия на локацию")
    time = a[before][k] + s[before][k] + factory.t[before][after]

    print("Дерективный срок = ", factory.e[after])
    print("Фактическое время прибытия = ", time)
    if factory.e[after] >= time:
        print("Приехали слишком рано ждем начало временного окна")
        return factory.e[after]

    elif factory.e[after] < time:
        print("Опоздали на начало работ")
        return time


# Преобразуем последовательность в матрицы решений
def SequenceDisplayInTheXYSA(sequence):
    print("Переделываем последовательность в матрицы решений")

    count_car = CountUsedMachines(sequence)
    print("Количество машин используемых ребенком = ", count_car)

    x = [[[0 for k in range(count_car)] for j in range(factory.N)] for i in
         range(factory.N)]  # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(count_car)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(count_car):
        y[0][k] = 1
    s = [[0 for k in range(count_car)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(count_car)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    k = 0
    print("Теперь перейдем к заполнению матрицы Х У")
    for i in range(1, len(sequence)):
        before = sequence[i - 1][0]
        after = sequence[i][0]
        print("Предыдущий посещенный ", before)
        print("Которого вставляем ", after)

        if sequence[i][0] == 0:
            x[before][after][k] = 1
            y[after][k] = 1

            k += 1
            print("Увидели 0, значит переходим к следующей машине с номером ", k)
            if k == count_car:
                print("Кол-во используемых авто ", count_car)
                break
        else:
            x[before][after][k] = 1
            y[after][k] = 1

    k = 0
    print("Теперь заполним А и S")
    for i in range(1, len(sequence)):
        before = sequence[i - 1][0]
        after = sequence[i][0]
        print("Предыдущий посещенный ", before)
        print("Которого вставляем ", after)

        if after == 0:
            a[after][k] = a[before][k] + factory.t[before][after]
            k += 1
            print("Увидели 0, значит переходим к следующей машине с номером ", k)
            if k == count_car:
                print("Кол-во используемых авто ", count_car)
                break

        if after != 0:
            try:
                if sequence.index([after, 0], 0, i) > 0:
                    print("Уже считали для этого ", after, " города")

            except ValueError:
                print("До этого еще не встречали город ", after)
                WorkTimeCounting(sequence, y, s, after)

            a[after][k] = ArrivalTime(a, s, before, after, k)

    return x, y, s, a, count_car


# Получаем двумерную последовательность вида
# 0 3 0 0 0 0 0 0 0 0
#
# 0 5 0 0 0 0 0 0 0 0
#
# 0 7 1 0 0 0 0 0 0 0
#
# 0 2 6 4 8 0 0 0 0 0
#
# 0 9 0 0 0 0 0 0 0 0
# Заебись, работает!!!
def GettingTheSequence(X):
    # factory.N+1 потому что последовательность может посещать все города и при этом возвращается в 0
    sequenceX2 = [[0 for i in range(factory.N + 1)] for j in range(len(X[0][0]))]
    for k in range(len(X[0][0])):
        XDisplayInTheSequenceX2(X, sequenceX2, 0, k, 0)
    return sequenceX2


# Добавление еще одной ячейки к последовательности
# Заебись, работает!!!
def AddOneCell(sequenceX1):
    bufer = [[0 for j in range(2)] for i in range(len(sequenceX1))]
    # ячейка означает, что из этого конкретного города на этой машине нельзя ехать в следующий
    for i in range(len(sequenceX1)):
        bufer[i][0] = sequenceX1[i]
    return bufer


# Переделываем двумерную в одномерную, вида 014856047852098704850
# Заебись, работает!!!
def TransferX2toX1(sequenceX2, X):
    sequenceX1 = [0]
    for k in range(len(X[0][0])):
        for i in range(1, factory.N - 1):
            # случай когда находишься на цифре и следующая цифра
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] != 0:
                sequenceX1.append(sequenceX2[k][i])
            # случай когда находишься на цифре и следующий ноль
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] == 0:
                sequenceX1.append(sequenceX2[k][i])
            # случай когда находишься на нуле и предыдущая цифра
            if sequenceX2[k][i - 1] != 0 and sequenceX2[k][i] == 0:
                sequenceX1.append(sequenceX2[k][i])
    # ДОбавляем еще одну ячейку к каждому элементу последовательности
    sequenceX1 = AddOneCell(sequenceX1)
    return sequenceX1


# номер посещения клиента
def NumberClientaInSequence(bufer, client):
    for i in range(len(bufer)):
        if bufer[i][0] == client:
            return i
    print("ERROR for NumberClientaInSequence: Не нашел номер посещения клиента в последовательности")


# выбираю другое ребро но из начала c таким же номером
# вроде тоже все заебись!!!!
def AnotherEdgeWithTheSameBeginning(bufer_in, new_start, flag, countOfRaces):
    for i in range(len(bufer_in)):
        # bufer_in[i][0] == new_start нашли кокой-то выезд из такого же города
        # bufer_in[i][1.txt] == 0 мы из него еще не выезжали
        # flag[ bufer_in[i][0] ] == 0 в этом маршруте еще не посещали
        # countOfRaces[bufer_in[i][0]] > 0 есть свободные скважины
        if bufer_in[i][0] == new_start and bufer_in[i][1] == 0 and flag[
            bufer_in[i + 1][0]] == 0 and countOfRaces[bufer_in[i + 1][0]] > 0:
            return i
    return -1


# Создаем массив у каких локаций остались свободные скважины
def RandNotVisitClient(countOfRaces, flag):
    # массив для не посещенных городов
    count_not_visit = []

    for i in range(len(countOfRaces)):
        # если у кого-то клиента есть свободные скважины,
        if countOfRaces[i] != 0 and flag[i] == 0:
            # то сохраняем номер этого клиента
            count_not_visit.append(i)

    print("Of RandNotVisitClient: создали массив, у каких клиентов остались свободные скважины")
    print(count_not_visit)

    try:
        # берем рандомного из списка не посещенных
        i = random.choice(count_not_visit)
        print("Взяли рандомного из этого списка равного ", i)
        return i

    except IndexError:
        print("Больше нет клиентов с свободными скважинами")
        return -1


# рекурсивный поиск для скрещивания
# bufer_in- где ищем(Куда едем), bufer_out- откуда идем
# bufer_out[i_out] - последний добавленный клиент в новый маршрут
# i_out - номер последнего добавленног клиента
# i - номер куда будем добавлять в ребенке
# flag флаг для машины
# flagAll флаг для всего решения
# countOfRaces - сколько машин мжно отправить на локацию
def RecursiveSearchSosedFromAex(children, bufer_in, bufer_out, i_out, flag, flagAll, countOfRaces, numberInCar):
    # номер позиции клиента bufer_out[i_out][0] в bufer_in
    i_in = NumberClientaInSequence(bufer_in, bufer_out[i_out][0])

    print("Ищем ", bufer_out[i_out][0])
    print("Из", bufer_out)
    print("В", bufer_in)
    print("Нашли на индексе ", i_in)
    print("Флаг машины ", flag)
    print("Флаг решения ", flagAll)
    print("Сколько раз к каждому клиенту можно приехать", countOfRaces)
    print("Число клиентов на одной машине (между нулями)", numberInCar)

    # смотрим что этот город еще можно вставлять, в этот маршрут
    # и что у него есть свободные скважины
    # и что конкретно это ребро мы еще не использовали
    # bufer_in[i_in + 1.txt] - новый, которого хотим добавить
    # Здесь все заебись, проверено программой!!!!!!!!!!
    if flag[bufer_in[i_in + 1][0]] == 0 and countOfRaces[bufer_in[i_in + 1][0]] \
            > 0 and bufer_in[i_in][1] == 0:

        print("-------------------Этот блок проверен программой!!-------------------")
        print("Вставляем в ребенка город ", bufer_in[i_in + 1][0],
              ", у которого есть свободные скважины, через ребро которое из решения")
        print(bufer_in)
        print("еще не использовали и которого на этой машине еще не посещали")

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

        print("Ребенок выглядит пока вот так ")
        print(children)
        print("______________________________")

        RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in + 1, flag, flagAll, countOfRaces, numberInCar)

    # если конкретно это ребро уже использовали, то
    elif bufer_in[i_in][1] != 0:

        print("Конкрентно это ребро уже использовали")

        print("Выбираю другое ребро но из такого же начала",
              bufer_in[i_in][0], ", но которое не посещали в этом маршруте, у которого еще есть свободные скважины")

        i_in_buf = AnotherEdgeWithTheSameBeginning(bufer_in, bufer_in[i_in][0], flag, countOfRaces)
        # Если нашли такой индекс
        if i_in_buf != -1:
            print("Нашли такое же начало", bufer_in[i_in_buf][0], ", его индекс в последовательности ")
            print(bufer_in)
            print("равен", i_in_buf)

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

            print("Ребенок выглядит пока вот так ")
            print(children)
            print("______________________________")

            RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in_buf + 1, flag, flagAll, countOfRaces, numberInCar)

        # если не нашли такой индекс
        else:
            print("-------------------Этот блок проверен программой!!-------------------")
            print("Не нашли такое же начало", bufer_in[i_in][0],
                  " . Поэтому ищем такое же начало в другом решении в ")
            print(bufer_out)
            # выбираю другое ребро но из такого же начала в другом решении,
            # но которое не посещали в этом маршруте,
            # у которого еще есть свободные скважины
            i_in_buf = AnotherEdgeWithTheSameBeginning(bufer_out, bufer_in[i_in][0], flag, countOfRaces)
            # Если нашли такой индекс
            if i_in_buf != -1:
                print("Нашли такое же начало", bufer_out[i_in_buf][0], ", его индекс в последовательности ")
                print(bufer_out)
                print("равен", i_in_buf)

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

                print("Ребенок выглядит пока вот так ")
                print(children)
                print("______________________________")

                RecursiveSearchSosedFromAex(children, bufer_in, bufer_out, i_in_buf + 1, flag, flagAll, countOfRaces,
                                     numberInCar)

            else:
                print("-------------------Этот блок проверен программой!!-------------------")
                print("Не нашли такое же начало ни в одном из решений. Поэтому берем рандомного")
                if numberInCar >= factory.param_min_num_cl_in_car:

                    next_client = random.randint(0, factory.N - 1)
                    # номер позиции клиента bufer_out[i_out] в bufer_in
                    i_in = NumberClientaInSequence(bufer_in, next_client)

                elif numberInCar < factory.param_min_num_cl_in_car:

                    next_client = random.randint(1, factory.N - 1)
                    # номер позиции клиента bufer_out[i_out] в bufer_in
                    i_in = NumberClientaInSequence(bufer_in, next_client)

                else:
                    print("ERROR from in random client: Кол-во клиентов в маршруте сломалось")

                print("Берем рандомного клиента ", next_client)

                print("Номер позиции рандомного клиента в ")
                print(bufer_in)
                print("равен ", i_in)

                # ищем нового клиента, пока не найдем не посещенного (flag[next_client] == 0) и у которого
                # остались свободные скважины (countOfRaces[next_client] > 0)
                # Здесь все заебись, проверенно программой!!!!!!!!!!
                count = 0
                while ((flag[next_client] == 1 and countOfRaces[next_client]
                        <= 0) or (flag[next_client] == 0 and countOfRaces[next_client]
                                  <= 0) or (flag[next_client] == 1 and countOfRaces[next_client]
                                            > 0)) and count <= factory.N:
                    print("Рандомный", next_client, "не подошел, так как мы его либо посещали на "
                                                    "этой машине либо нет свободных скважин")

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
                        print("ERROR from in random client: Кол-во клиентов в маршруте сломалось")

                # Означает что нашли рандомного
                if count <= factory.N:
                    print("Итоговый рандомный клиент ", next_client)
                    print("И его позиция в ")
                    print(bufer_in)
                    print("равна", i_in)

                    # это значит что встретили ноль, цикл должен завершится
                    if flag[next_client] == -1 and numberInCar >= factory.param_min_num_cl_in_car:
                        print("Рандомный оказался 0, поэтому цикл должен завершится")

                        # добавляем в ребенка bufer_in[i_in + 1.txt]
                        children.append([next_client, 0])
                        # children[i][0] = next_client

                        # ставим влаг
                        flag[next_client] += 1
                        flagAll[next_client] = 1

                        # зануляем сяетчик, так как следом будет уже другая машина
                        numberInCar = 0

                        print("Ребенок выглядит пока вот так ")
                        print(children)
                        print("Переходим к следующей машине")
                        print("_______________________________________"
                              "________________________________________________________")

                        return True

                    # смотрим что этот город еще можно вставлять
                    # Здесь все заебись, проверенно программой!!!!!!!!!!
                    elif flag[next_client] == 0:
                        print("-------------------Этот блок проверен программой!!-------------------")
                        print("Вставляем ", next_client, "в ребенка")

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

                        print("Ребенок выглядит пока вот так ")
                        print(children)
                        print("______________________________")

                        RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces,
                                             numberInCar)

                    else:
                        print("ERROR from RecursiveSearchSosedFromAex inside: ошибка в поске рандомного нового клиента")

                # Означает что вывалились из вайла,
                # потому что долго ждали, поэтому возвращаем машину в депо
                else:
                    print("-------------------Этот блок проверен программой!!-------------------")
                    print("Слишком долго искали рандомного, while закончился по времени. Поэтому возвращаемся в депо.")
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

                    print("Ребенок выглядит пока вот так ")
                    print(children)
                    print("Переходим к следующей машине")
                    print(
                        "_______________________________________________________________________________________________")

                    return True

    # Если мы его на этом ТС уже посещали, то нужно взять рандомного
    # или у него больше не хватает скважин но по этому ребру еще не ехали
    # и главное чтобы он не был нулем
    elif (flag[bufer_in[i_in + 1][0]] == 1 or countOfRaces[bufer_in[i_in + 1][0]] <= 0) and bufer_in[i_in + 1][0] != 0:
        print("-------------------Этот блок проверен программой!!-------------------")
        print("Клиента ", bufer_in[i_in + 1][0], "на этом ТС уже посещали или у него нет свободных скважин")

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
            print("ERROR from in random client: Кол-во клиентов в маршруте сломалось")

        print("Берем рандомного клиента ", next_client)

        print("Номер позиции рандомного клиента в ")
        print(bufer_in)
        print("равен ", i_in)

        # ищем нового клиента, пока не найдем не посещенного и у которого
        # остались свободные скважины
        # Здесь все заебись!!!!!!!!!!
        count = 0
        while ((flag[next_client] == 1 and countOfRaces[next_client]
                <= 0) or (flag[next_client] == 0 and countOfRaces[next_client]
                          <= 0) or (flag[next_client] == 1 and countOfRaces[next_client]
                                    > 0)) and count <= factory.N:
            print("Рандомный", next_client, "не подошел, так как мы его либо посещали на "
                                            "этой машине либо нет свободных скважин")

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
                print("ERROR from in random client: Кол-во клиентов в маршруте сломалось")

        # Означает что нашли рандомного
        if count <= factory.N:
            print("Итоговый рандомный клиент ", next_client)
            print("И его позиция в ")
            print(bufer_in)
            print("равна", i_in)

            # это значит что встретили ноль, цикл должен завершится
            if flag[next_client] == -1 and numberInCar >= factory.param_min_num_cl_in_car:
                print("Рандомный оказался 0, поэтому цикл должен завершится")

                # добавляем в ребенка bufer_in[i_in + 1.txt]
                children.append([next_client, 0])
                # children[i][0] = next_client

                # ставим влаг
                flag[next_client] += 1
                flagAll[next_client] = 1

                # зануляем сяетчик, так как следом будет уже другая машина
                numberInCar = 0

                print("Ребенок выглядит пока вот так ")
                print(children)
                print("Переходим к следующей машине")
                print("_______________________________________________________________________________________________")

                return True

            # смотрим что этот город еще можно вставлять
            # Здесь все заебись, проверенно программой!!!!!!!!!!
            elif flag[next_client] == 0:
                print("Вставляем ", next_client, "в ребенка")

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

                print("Ребенок выглядит пока вот так ")
                print(children)
                print("______________________________")

                RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces, numberInCar)

            else:
                print("ERROR from RecursiveSearchSosedFromAex inside: ошибка в поске рандомного нового клиента")

        # Означает что вывалились из вайла,
        # потому что долго ждали, поэтому возвращаем машину в депо
        else:
            print("-------------------Этот блок проверен программой!!-------------------")
            print("Слишком долго искали рандомного, while закончился по времени. Поэтому возвращаемся в депо.")
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

            print("Ребенок выглядит пока вот так ")
            print(children)
            print("Переходим к следующей машине")
            print("_______________________________________________________________________________________________")

            return True

    # Если уже встретили ноль, но в последовательности слишком мало клиентов
    elif flag[bufer_in[i_in + 1][0]] == -1 and numberInCar < factory.param_min_num_cl_in_car:
        print("-------------------Этот блок проверен программой!!-------------------")
        print("Слишком рано встретили ноль, в последовательности только", numberInCar, " клиент")

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # берем рандомного клиента у кторого есть не посещенные скважины
        print("Берем рандомного клиента у кторого есть не посещенные скважины с помощью функции RandNotVisitClient")
        rand_client = RandNotVisitClient(countOfRaces, flag)

        # Нашли рандомного клиента
        if rand_client != -1:
            # номер позиции клиента bufer_out[i_out][0] в bufer_in
            i_in = NumberClientaInSequence(bufer_in, rand_client)
            print("Новый рандомный клиент ", rand_client, "находится под номером ", i_in, "в последовательности ")
            print(bufer_in)

            # добавляем в ребенка bufer_in[i_in + 1]
            children.append([rand_client, 0])

            # ставим флажки
            flag[bufer_in[i_in][0]] = 1
            flagAll[bufer_in[i_in][0]] = 1

            # Уменьшаем кол-во машин которые к этому клиенту могут приехать
            countOfRaces[bufer_in[i_in][0]] -= 1

            # плюс один клиент в машине
            numberInCar += 1

            print("Ребенок выглядит пока вот так ")
            print(children)
            print("______________________________")

            RecursiveSearchSosedFromAex(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces, numberInCar)

        elif rand_client == -1:
            print("Возвращаемся в депо")
            # добавляем в ребенка bufer_in[k_in][i_in + 1.txt]
            children.append([0, 0])

            # Ставим флаг в последовательности в которой искали ребро в доп ячееки
            bufer_in[i_in][1] = 1

            # ставим влаг
            flag[0] = 1
            flagAll[0] = 1

            # зануляем сяетчик, так как следом будет уже другая машина
            numberInCar = 0

            print("Ребенок выглядит пока вот так ")
            print(children)
            print("Переходим к следующей машине")
            print(
                "_______________________________________________________________________________________________________")
            return True

    # это значит что встретили ноль, цикл должен завершится
    # Здесь все заебись, проверенно программой!!!!!!!!!!
    elif flag[bufer_in[i_in + 1][0]] == -1 and numberInCar >= factory.param_min_num_cl_in_car:
        print("-------------------Этот блок проверен программой!!-------------------")
        print("Встретили 0 пора возвращаться в депо")
        # добавляем в ребенка bufer_in[k_in][i_in + 1.txt]
        children.append([bufer_in[i_in + 1][0], 0])

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # ставим влаг
        flag[bufer_in[i_in + 1][0]] = 1
        flagAll[bufer_in[i_in + 1][0]] = 1

        # зануляем сяетчик, так как следом будет уже другая машина
        numberInCar = 0

        print("Ребенок выглядит пока вот так ")
        print(children)
        print("Переходим к следующей машине")
        print("_______________________________________________________________________________________________________")
        return True

    else:
        print("ERROR from RecursiveSearchSosedFromAex outside: проблема с флагами, не нашли не ноль, не еще не посещенный")


# Добавляем клиента в последовательность, со всеми флагами
# ЗАебись!!!
def AddClientaInSequence(children, bufer, flag, flagAll, countOfRaces, i_in):
    print("Добавляем ", bufer[i_in][0], "в ребенка с помощью функции AddClientaInSequence")
    children.append([bufer[i_in][0], 0])

    # из первого нуля больше никуда не едем
    bufer[i_in][1] = 1

    # Расставляем флажки локально для первой машины и для общего решения
    flag[0] += 1
    flag[bufer[i_in][0]] = 1
    flagAll[bufer[i_in][0]] = 1
    # на одну мащину к нему (bufer1[1.txt]) теперь может приехать меньше
    countOfRaces[bufer[i_in][0]] -= 1

    print("Ребенок выглядит пока вот так ")
    print(children)
    print("______________________________")


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
def SearchForAnUnvisitedZero(bufer1, size1, bufer2, size2, flagAll, countOfRaces, children, flag, numberInCar):
    # #Сначала проверим есть ли те которых мне не посетили ни разу
    # if sum(flagAll) <= factory.N:
    #

    # ищем в первом, в большем решении
    for i in range(size1 - 1):
        # bufer1[i][0] == 0 ищем ноль,
        # bufer1[i][1.txt] == 0 из которого еще не выезжали
        # bufer1[i+1.txt][0] > 0 у которого еще есть свободные скважины
        if bufer1[i] == [0, 0] and countOfRaces[bufer1[i + 1][0]] > 0:
            print("Нашли 0 в решении")
            print(bufer1)
            print("из которого еще не выезжали и первый после него со скважинами ", bufer1[i + 1][0])

            bufer1[i][1] = 1
            AddClientaInSequence(children, bufer1, flag, flagAll, countOfRaces, i + 1)
            RecursiveSearchSosedFromAex(children, bufer2, bufer1, i + 1, flag, flagAll, countOfRaces, numberInCar)
            return
            # return i+1.txt

    # если не нашли в большем, ищем в меньшем
    for i in range(size2 - 1):
        # bufer2[i][0] == 0 ищем ноль,
        # bufer2[i][1.txt] == 0 из которого еще не выезжали
        # countOfRaces[bufer2[i + 1.txt][0]] > 0 у которого еще есть свободные скважины
        if bufer2[i] == [0, 0] and countOfRaces[bufer2[i + 1][0]] > 0:
            print("Не нашли 0 в решении")
            print(bufer1)
            print("но, нашли 0 в решении")
            print(bufer2)
            print("из которого еще не выезжали и первый после него со скважинами ", bufer2[i + 1][0])

            bufer2[i][1] = 1
            AddClientaInSequence(children, bufer2, flag, flagAll, countOfRaces, i + 1)
            RecursiveSearchSosedFromAex(children, bufer1, bufer2, i + 1, flag, flagAll, countOfRaces, numberInCar)
            return
            # return i+1.txt

    # если не нашли ноль, то ищем просто не посещенного
    for i in range(factory.N):
        # Если в первом и вотором не нашли то ищем просто не посещенный
        # впринципе и у которого есть свободные скважины!!
        if flagAll[i] == 0 and countOfRaces[i] > 0:
            print("Не нашли 0 из которого еще не выезжали ни в одном из решений")
            print("Значит ищем у кого вообще остались скважины")
            print("Нашли ", i, " город у которого еще есть скважины и в этом решении его не посещали")

            # Если нашли такого, то ищем этот город в большем решении
            # и из него мы еще не выезжали
            for j in range(size1 - 1):
                # bufer1[i][0] == 0 ищем этот итый город,
                # bufer1[i][1.txt] == 0 из которого еще не выезжали
                if bufer1[j][0] == i and bufer1[j][1] == 0:
                    print("Нашли этот город в решении")
                    print(bufer1)
                    AddClientaInSequence(children, bufer1, flag, flagAll, countOfRaces, j)
                    RecursiveSearchSosedFromAex(children, bufer2, bufer1, j, flag, flagAll, countOfRaces, numberInCar)
                    return
                    # return j
            # если не нашли в большем, ищем в меньшем
            for j in range(size2 - 1):
                # bufer2[i][0] == 0 ищем ноль,
                # bufer2[i][1.txt] == 0 из которого еще не выезжали
                if bufer2[j][0] == 0 and bufer2[j][1] == 0:
                    print("Нашли этот город в решении")
                    print(bufer1)
                    AddClientaInSequence(children, bufer2, flag, flagAll, countOfRaces, j)
                    RecursiveSearchSosedFromAex(children, bufer1, bufer2, j, flag, flagAll, countOfRaces, numberInCar)
                    return
                    # return j

    print("Notification from SearchForAnUnvisitedZero: не нашли куда ехать")


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
def AEX(sequence1, sequence2):
    print("Скрещивание решений усуществляется с помощью оператора АЕХ")
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
    print("size1 = ", size1)
    size2 = len(sequence2)
    print("size2 = ", size2)

    # флаг, для посещенных городов в заключительном решении
    flagAll = [0 for j in range(factory.N)]

    # сколько раз можно заехать к каждому
    countOfRaces = factory.wells.copy()

    print("Сколько раз к каждому клиенту можно приехать до оператора AEX ", countOfRaces)

    # определяем по кому будем делать цикл
    if size1 >= size2:
        print("Первая последовательность больше")

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

        print("Ребенок выглядит пока вот так ")
        print(children)
        print("______________________________")

        # Для первого добавления запустим без цикла
        RecursiveSearchSosedFromAex(children, sequence2, sequence1, 1, flag, flagAll, countOfRaces, numberInCar)

        # Обнуляем флаг для следующей машины
        for i in range(factory.N):
            flag[i] = 0
        flag[0] = -2

        # Добавляем еще одну машину + сдвигаем индекс последовательности
        k += 1

        print("Построили для первой машины")
        print("_______________________________________________________________________________________________________")
        # Пока кол-во используемых машин не привысило доступного числа  k <= factory.K
        # или остались не посещенные города sum(flagAll) <= factory.N
        counter = 0
        while sum(flagAll) <= factory.N and counter <= factory.N * 2:
            print("Продолжаем построение с помощью функции SearchForAnUnvisitedZero")
            print("Хотим найти 0 в каком-нибудь решении из которого еще не выезжали или "
                  "клиента которого еще не посетили в этом решении")

            # Поиск номер в последовательности не посещенного нуля
            # или просто не посещенного
            # и его добавление в ребенка с расставлением всех флагов
            # и запуском рекурсии
            SearchForAnUnvisitedZero(sequence1, size1, sequence2, size2, flagAll, countOfRaces, children, flag,
                                     numberInCar)

            print("Построили для следующей машины")
            print(
                "_____________________________________"
                "__________________________________________________________________")

            # Обнуляем флаг для следующей машины
            for i in range(factory.N):
                flag[i] = 0
            flag[0] = -2

            # Добавляем еще одну машину + сдвигаем индекс последовательности
            k += 1
            counter += 1

    elif size1 < size2:
        print("Вторая последовательность больше")

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

        print("Ребенок выглядит пока вот так ")
        print(children)
        print("______________________________")

        # Для первого добавления запустим без цикла
        RecursiveSearchSosedFromAex(children, sequence1, sequence2, 1, flag, flagAll, countOfRaces, numberInCar)

        # Обнуляем флаг для следующей машины
        for i in range(factory.N):
            flag[i] = 0
        flag[0] = -2

        # Добавляем еще одну машину + сдвигаем индекс последовательности
        k += 1

        print("Построили для первой машины")
        print("_______________________________________________________________________________________________________")

        # Пока кол-во используемых машин не привысило доступного числа  k <= factory.K
        # или остались не посещенные города sum(flagAll) <= factory.N
        counter = 0
        # TODO разобраться, когда всех посетили, но на одной машине
        while sum(flagAll) <= factory.N and counter <= factory.N * 2:
            print("Продолжаем построение с помощью функции SearchForAnUnvisitedZero")
            print("Хотим найти 0 в каком-нибудь решении из которого еще не выезжали или "
                  "клиента которого еще не посетили в этом решении")
            # Поиск номер в последовательности не посещенного нуля
            # или просто не посещенного
            # и его добавление в ребенка с расставлением всех флагов
            # и запуском рекурсии

            SearchForAnUnvisitedZero(sequence2, size2, sequence1, size1, flagAll, countOfRaces, children, flag,
                                     numberInCar)

            print("Построили для следующей машиины машины")
            print(
                "___________________________________________________"
                "____________________________________________________")

            # Обнуляем флаг для следующей машины
            for i in range(factory.N):
                flag[i] = 0
            flag[0] = -2

            # Добавляем еще одну машину + сдвигаем индекс последовательности
            k += 1
            counter += 1

    else:
        print("ERROR from AEX: исключение, произошло невозможное!!!!")

    for i in range(len(children)):
        children[i][1] = 0
    for i in range(len(sequence1)):
        sequence1[i][1] = 0
    for i in range(len(sequence2)):
        sequence2[i][1] = 0
    print("Оператор AEX закончил своб работу с решениями")
    print("sequence1 = ", sequence1)
    print("sequence2 = ", sequence2)
    print("И получился ребенок ")
    print("children = ", children)
    print("__________________________________________________________________________________________________________")
    return children


# кроссовер HGreX
def HGreX(sequence1, sequence2):
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
def HRndX(sequence1, sequence2):
    return


# Оператор HProX
def HProX(sequence1, sequence2):
    return


# Функция вызывает выбранный оператор
def UsedOperators(sequence1, sequence2, operator):
    print("Запускаем оператор ", operator)
    if operator == 'AEX':
        return AEX(sequence1, sequence2)

    elif operator == 'HGreX':
        return HGreX(sequence1, sequence2)

    elif operator == 'HRndX':
        return HRndX(sequence1, sequence2)

    elif operator == 'HProX':
        return HProX(sequence1, sequence2)

    else:
        print("ERROR from UsedOperators: название такого оператора нет")


# Локальный поиск (локально меняем решение)
def LocalSearch(x, y, s, a, target_function, sizeK):
    print("Применяем локальный поиск (локально меняем решение)")

    # TODO выбираем оператор локального поиска
    local_search_oper = ['relocate', '2Opt', 'Exchange']
    oper = random.choice(local_search_oper)
    oper = 'relocate'

    print("Используем оператор ", oper)
    if oper == 'relocate':
        x, y, s, a, target_function,  sizeK = Relocate(x, y, s, a, target_function, sizeK)
        return x, y, s, a, target_function,  sizeK

    elif oper == '2Opt':
        print("")

    elif oper == 'Exchange':
        print("")


# Мутация
def Mutation(sequence):
    print("___________________________________________________________________________________________________________")
    print("Начилась мутация")
    count_car = CountUsedMachines(sequence)
    print("Число используемых машин = ", count_car)

    buf_random = []
    k = 0
    print("Последовательность до мутации ")
    print(sequence)
    for i in  range(1, len(sequence)):
        if sequence[i][0] != 0:
            print("Составляем массив какие клиенты обслуживаются этим маршрутом, сейчас добавляем ", sequence[i][0])
            buf_random.append(sequence[i][0])
        elif sequence[i][0] == 0 and len(buf_random) > 1:

            print("Полученный массив ", buf_random)
            obj1 = int(random.choice(buf_random))
            print("Берем рандомного клиента ", obj1)
            buf_random.remove(obj1)
            obj2 = int(random.choice(buf_random))
            print("Берем рандомного клиента ", obj2)

            index1 = sequence.index([obj1, 0], k)
            print("Их места в последовательности ", index1)
            index2 = sequence.index([obj2, 0], k)
            print("Их места в последовательности ", index2)

            sequence[index1][0] = obj2
            sequence[index2][0] = obj1
            print("Получившаяся последовательность")
            print(sequence)

            buf_random = []
            k = i

        elif sequence[i][0] == 0 and len(buf_random) == 1:
            print("Машина обслуживает только одного клиента, никого никуда не переставляем")
            buf_random = []
            k = i

    print("Итоговая, измененая последовательность = ")
    print(sequence)


# Функция которая позволяет родить ребенка (скрестить два решения)
# и отдать его в хорошую школу (оператор локального перемещения)
# и дальнейшее его помещение в популяцию решений, если он не хуже всех
# и все это сделает factory.param_crossing раз
def GetNewSolution(Sequence, X, Y, Sresh, A, Target_Function, SizeK):
    print("Начинаем процесс порождения нового решения")

    for crossing in range(factory.param_crossing):
        print("Запускаем ", crossing, "-ый раз")

        # Выбираем по каком сценарию будем брать родителей
        scenario_cross = ['randomAndRandom', 'randomAndBad', 'BestAndRand', 'BestAndBad']
        scenario = random.choice(scenario_cross)
        print("Выбрали сценарий по выбору родителей", scenario)

        # Выбираю как буду сохранять полученное решение
        scenario_add_new_solution = ['deleteTheBad', 'deleteTheBadParents']
        scenario_add = random.choice(scenario_add_new_solution)
        print("Выбрали сценарий по сохранению нового решения", scenario_add)

        # TODO Задаю список с названиями операторов
        name_crossover = ['AEX', 'HGreX', 'HRndX', 'HProX']
        crossover = random.choice(name_crossover)
        crossover = 'AEX'
        print("Выбрали кроссовер для скрещивания", crossover)

        # Идем по одному сценарию
        if scenario == 'randomAndRandom':
            print("Пошли по сценарию, два рандомных решения")
            # Индекс первого родителя
            index = int(random.randint(0, factory.param_population - 1))
            print("Номер первого решения ", index)

            # Индекс второго родителя
            jndex = int(random.randint(0, factory.param_population - 1))
            print("Номер второго решения ", jndex)

            # Если вдруг индекс второго родителя равен первому
            while jndex == index:
                jndex = random.randint(0, factory.param_population - 1)

            print(Sequence)
            print("Первое рандомное решение")
            print(Sequence[index])
            print("Второе рандомное решение")
            print(Sequence[jndex])

            children = UsedOperators(Sequence[index], Sequence[jndex], crossover)

        elif scenario == 'randomAndBad':
            print("Пошли по сценарию, один рандомный второй самый худший")
            # Индекс первого родителя
            index = random.randint(0, factory.param_population - 1)
            print("Номер первого решения ", index)

            # Ищем самое большое решение по целевой функции
            maximum = max(Target_Function)
            # Оно будет вторым родителем
            jndex = Target_Function.count(maximum)
            print("Номер второго решения ", jndex)

            print(Sequence)
            print("Первое рандомное решение")
            print(Sequence[index])
            print("Второе решение, худшие из всех")
            print(Sequence[jndex])

            children = UsedOperators(Sequence[index], Sequence[jndex], crossover)

        elif scenario == 'BestAndRand':
            print("Пошли по сценарию, один рандомный второй самый лудший")
            # Индекс первого родителя
            index = random.randint(0, factory.param_population - 1)
            print("Номер первого решения ", index)

            # Ищем самое маленькое решение по целевой функции
            minimum = min(Target_Function)
            # Оно будет вторым родителем
            jndex = Target_Function.count(minimum)
            print("Номер второго решения ", jndex)

            print(Sequence)
            print("Первое рандомное решение")
            print(Sequence[index])
            print("Второе решение, лудшие из всех")
            print(Sequence[jndex])

            children = UsedOperators(Sequence[index], Sequence[jndex], crossover)

        elif scenario == 'BestAndBad':
            print("Пошли по сценарию, один самый лудший второй самый худший")
            # Ищем самое маленькое решение по целевой функции
            minimum = min(Target_Function)
            # Оно будет первым родителем
            index = Target_Function.count(minimum)
            print("Номер первого решения ", index)

            # Ищем самое большое решение по целевой функции
            maximum = max(Target_Function)
            # Оно будет вторым родителем
            jndex = Target_Function.count(maximum)
            print("Номер второго решения ", jndex)

            print(Sequence)
            print("Первое решение, лудшие из всех")
            print(Sequence[index])
            print("Второе решение, худшие из всех")
            print(Sequence[jndex])

            children = UsedOperators(Sequence[index], Sequence[jndex], crossover)

        # У ребенка в конце может не быть нуля
        if children[-1] != [0, 0]:
            children.append([0, 0])

        # Применяем мутацию
        Mutation(children)

        # Переводим последовательность в матрицы решений
        x, y, s, a, sizek = SequenceDisplayInTheXYSA(children)

        assert VerificationOfBoundaryConditions(x, y, s, a, 'true') == 1
        # Считаем целевую функцию
        target_function = CalculationOfObjectiveFunction(x, y, PenaltyFunction(s, a))
        print("Целевая функция нового решения после оператора скрещивания равна ", target_function)

        # Применяем локальный поиск
        x, y, s, a, target_function, sizek = LocalSearch(x, y, s, a, target_function, sizek)

        # Считаем целевую функцию
        target_function = CalculationOfObjectiveFunction(x, y, PenaltyFunction(s, a))
        print("Целевая функция нового решения после локального поиска равна ", target_function)

        # Проверяем что новое решение не хуже самого плохого
        # Ищем самое большое решение по целевой функции
        maximum = max(Target_Function)
        i_max = Target_Function.index(maximum)
        print("Самое плохое решение в популяции ", maximum)

        # Удаляем какое-нибудь решение
        if maximum >= target_function:
            if scenario_add == 'deleteTheBad':
                print("Удаляем самое плохое решение в популяции")
                X.pop(i_max)
                Y.pop(i_max)
                Sresh.pop(i_max)
                A.pop(i_max)
                Target_Function.pop(i_max)
                Sequence.pop(i_max)
                SizeK.pop(i_max)

            elif scenario_add == 'deleteTheBadParents':
                print("Удаляем самого плохого родителя")

                if Target_Function[index] <= Target_Function[jndex]:
                    print("с целевой функцией ", Target_Function[jndex])
                    X.pop(jndex)
                    Y.pop(jndex)
                    Sresh.pop(jndex)
                    A.pop(jndex)
                    Target_Function.pop(jndex)
                    Sequence.pop(jndex)
                    SizeK.pop(jndex)

                elif Target_Function[index] > Target_Function[jndex]:
                    print("с целевой функцией ", Target_Function[index])
                    X.pop(index)
                    Y.pop(index)
                    Sresh.pop(index)
                    A.pop(index)
                    Target_Function.pop(index)
                    Sequence.pop(index)
                    SizeK.pop(index)

            print("Добавляем новое решение в конец")
            X.append(x)
            Y.append(y)
            Sresh.append(s)
            A.append(a)
            Target_Function.append(target_function)
            Sequence.append(children)
            SizeK.append(sizek)


def CheckSequence(Sequence):
    if Sequence.count([0, 0]) != 0 and Sequence.count([1, 0]) != 0 and Sequence.count([2, 0]) != 0 and Sequence.count(
            [3, 0]) != 0 and Sequence.count([4, 0]) != 0 and Sequence.count([5, 0]) != 0 and Sequence.count(
            [6, 0]) != 0 and Sequence.count([7, 0]) != 0 and Sequence.count([8, 0]) != 0 and Sequence.count(
            [9, 0]) != 0:
        return 1
    else:
        return 0
