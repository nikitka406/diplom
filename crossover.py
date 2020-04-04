import factory
from function import *
import random


# Создание последовательности для каждого решения
def CreateSequence(X):
    # Создаем спсиок, в которой будем хранить последовательности для каждогоо решения
    sequenceX1 = [0 for n in range(factory.population)]
    sequenceX2 = [0 for n in range(factory.population)]

    for m in range(factory.population):
        # Интерпритируем матрицу Х на двумерный массив
        sequenceX2[m] = GettingTheSequence(X[m])
        # print("Номер решения", m)
        # for k in range(factory.KA):
        #     for i in range(factory.N + 1):
        #         print(sequenceX2[m][k][i], end=" ")
        #     print("\n")
        sequenceX1[m] = TransferX2toX1(sequenceX2[m], X[m])
        # print(sequenceX1[m], "\n")

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
    sequenceX2 = [[0 for i in range(factory.N + 1)] for j in range(factory.KA)]
    for k in range(factory.KA):
        XDisplayInTheSequenceX2(X, sequenceX2, 0, k, 0)
    return sequenceX2


# количество посещений в последовательности (не нулевых элементов)
# Заебись, работает!!!
def CountVisitInSequence(sequenceX1):
    for i in range(1, (factory.N + 1) * factory.KA - 1):
        # если дошли до нулевого, но предэдущий не нулевой
        # а следующий нулевой или мы сейчас на предпоследнем
        if sequenceX1[i - 1] != 0 and sequenceX1[i] == 0 and (
                sequenceX1[i + 1] == 0 or i == ((factory.N + 1) * factory.KA - 1)):
            return i + 1


# уменьшить размерность последовательности
# Заебись, работает!!!
def LowerTheDimensionOfTheSequence(sequenceX1):
    size = CountVisitInSequence(sequenceX1)

    bufer = [0 for i in range(size)]

    for i in range(size):
        bufer[i] = sequenceX1[i]
    return bufer


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


# номер машины которая обслуживает клиента
def NumberCarClientaInSequence(bufer, client):
    for k in range(factory.KA):
        for i in range(factory.N + 1):
            if bufer[k][i] == client:
                return k
    return -1


# номер посещения клиента
def NumberClientaInSequence(bufer, client):
    for i in range(len(bufer)):
        if bufer[i][0] == client:
            return i
    print("ERROR for NumberClientaInSequence: Не нашел номер посещения клиента в последовательности")


# Возвращает матрицу, где индекс это номер клиента а содержимое, это сколько раз его можно посетить
def CountOfVisitsPribityClient(bufer):
    # TODO надо что-то сделать с депо, его можно сколько угодно посещать
    contVisit = [0 for j in range(factory.N)]
    for client in range(factory.N):
        for k in range(factory.KA):
            for i in range(factory.N + 1):
                if bufer[k][i] == client:
                    contVisit[client] += 1
    return contVisit


# выбираю другое ребро но из начала c таким же номером
# вроде тоже все заебись!!!!
def AnotherEdgeWithTheSameBeginning(bufer_in, new_start, flag, countOfRaces):
    for i in range(len(bufer_in)):
        # bufer_in[i][0] == new_start нашли кокой-то выезд из такого же города
        # bufer_in[i][1] == 0 мы из него еще не выезжали
        # flag[ bufer_in[i][0] ] == 0 в этом маршруте еще не посещали
        # countOfRaces[bufer_in[i][0]] > 0 есть свободные скважины
        if bufer_in[i][0] == new_start and bufer_in[i][1] == 0 and flag[
            bufer_in[i + 1][0]] == 0 and countOfRaces[bufer_in[i + 1][0]] > 0:
            return i
    return -1


# Создаем массив у каких локаций остались свободные скважины
def RandNotVisitClient(countOfRaces):
    # считаем сколько свободных скважин осталось
    size = sum(countOfRaces)
    # массив для не посещенных городов
    count_not_visit = [0 for i in range(size)]

    j = 0
    for i in range(size):
        # если у кого-то клиента есть свободные скважины,
        if countOfRaces[i] != 0:
            # то сохраняем номер этого клиента
            count_not_visit[j] = i
            j += 1

    print("Of RandNotVisitClient: создали массив, у каких клиентов остались свободные скважины")
    print(count_not_visit)

    # берем рандомного из списка не посещенных
    i = random.randint(0, size - 1)
    # и возвращаем его
    return count_not_visit[i]


# рекурсивный поиск для скрещивания
# bufer_in- где ищем(Куда едем), bufer_out- откуда идем
# bufer_out[i_out] - последний добавленный клиент в новый маршрут
# i_out - номер последнего добавленног клиента
# i - номер куда будем добавлять в ребенке
# flag флаг для машины
# flagAll флаг для всего решения
# countOfRaces - сколько машин мжно отправить на локацию
def RecursiveSearchSosed(children, bufer_in, bufer_out, i_out, flag, flagAll, countOfRaces, numberInCar):
    # номер позиции клиента bufer_out[i_out][0] в bufer_in
    # TODO i_in = bufer_in.__index__(bufer_out[i_out][0])
    i_in = NumberClientaInSequence(bufer_in, bufer_out[i_out][0])

    print("Ищем ", bufer_out[i_out][0])
    print("Из", bufer_out)
    print("В", bufer_in)
    print("Нашли на индексе ", i_in)

    # смотрим что этот город еще можно вставлять, в этот маршрут
    # и что у него есть свободные скважины
    # и что конкретно это ребро мы еще не использовали
    # bufer_in[i_in + 1] - новый, которого хотим добавить
    # Здесь все заебись!!!!!!!!!!
    if flag[bufer_in[i_in + 1][0]] == 0 and countOfRaces[bufer_in[i_in + 1][0]] \
            > 0 and bufer_in[i_in][1] == 0:

        print("Вставляем в ребенка город ", bufer_in[i_in + 1][0],
              ", у которого есть свободные скважины, через ребро которое из решения")
        print(bufer_in)
        print("еще не использовали и которого на этой машине еще не посещали")

        # добавляем в ребенка bufer_in[i_in + 1]
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

        RecursiveSearchSosed(children, bufer_out, bufer_in, i_in + 1, flag, flagAll, countOfRaces, numberInCar)

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

            # добавляем в ребенка bufer_in[i_in + 1]
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

            RecursiveSearchSosed(children, bufer_out, bufer_in, i_in_buf + 1, flag, flagAll, countOfRaces, numberInCar)

        # если не нашли такой индекс
        else:
            print("Не нашли такое же начало", bufer_in[i_in][0],
                  " . Поэтому ищем такое же начало в другом решении ")
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

                # добавляем в ребенка bufer_in[i_in + 1]
                children.append([bufer_out[i_in_buf + 1][0], 0])
                # children[i][0] = bufer_out[i_in_buf + 1][0]

                # Ставим флаг в последовательности в которой искали ребро в доп ячееки
                bufer_out[i_in_buf][1] = 1

                # ставим флажки
                flag[bufer_out[i_in_buf + 1][0]] += 1
                flagAll[bufer_out[i_in_buf + 1][0]] = 1

                # Уменьшаем кол-во машин которые к этому клиенту могут приехать
                countOfRaces[bufer_out[i_in_buf + 1][0]] -= 1

                # плюс один клиент в машине
                numberInCar += 1

                RecursiveSearchSosed(children, bufer_in, bufer_out, i_in_buf + 1, flag, flagAll, countOfRaces,
                                     numberInCar)

    # Если мы его на этом ТС уже посещали, то нужно взять рандомного
    # или у него больше не хватает скважин но по этому ребру еще не ехали
    elif flag[bufer_in[i_in + 1][0]] == 1 or countOfRaces[bufer_in[i_in + 1][0]] <= 0:
        print("Клиента ", bufer_in[i_in + 1][0], "на этом ТС уже посещали или у него нет свободных скважин")

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # Берем рандомного клиента
        next_client = random.randint(0, factory.N - 1)
        print("Берем рандомного клиента ", next_client)

        # номер позиции клиента next_client в bufer_in
        i_in = NumberClientaInSequence(bufer_in, next_client)
        print("Номер позиции рандомного клиента в ")
        print(bufer_in)
        print("равен ", i_in)

        # ищем нового клиента, пока не найдем не посещенного и у которого
        # остались свободные скважины
        # Здесь все заебись!!!!!!!!!!
        count = 0
        while (flag[next_client] == 1 or countOfRaces[next_client]
               <= 0) and count <= factory.N:
            print("Тот рандомный", next_client, "не подошел, так как мы его либо посещали на "
                                                "этой машине либо нет свободных скважин")

            # счетчик, чтобы вайл не был бесконечным
            count += 1
            next_client = random.randint(0, factory.N - 1)
            # номер позиции клиента bufer_out[i_out] в bufer_in
            i_in = NumberClientaInSequence(bufer_in, next_client)

        # Означает что нашли рандомного
        if count <= factory.N:
            print("Итоговый рандомный клиент ", next_client)
            print("И его позиция в ")
            print(bufer_in)
            print("равен", i_in)

            # это значит что встретили ноль, цикл должен завершится
            if flag[next_client] == -1 and numberInCar >= factory.min_num_cl_in_car:
                print("Рандомный оказался 0, поэтому цикл должен завершится")

                # добавляем в ребенка bufer_in[i_in + 1]
                children.append([next_client, 0])
                # children[i][0] = next_client

                # ставим влаг
                flag[next_client] += 1
                flagAll[next_client] = 1

                # зануляем сяетчик, так как следом будет уже другая машина
                numberInCar = 0

            # смотрим что этот город еще можно вставлять
            # Здесь все заебись!!!!!!!!!!
            elif flag[next_client] == 0:
                print("Вставляем ", next_client, "в ребенка")

                # добавляем в ребенка bufer_in[i_in + 1]
                children.append([next_client, 0])

                # Ставим флаг в последовательности в которой искали ребро в доп ячееки
                # bufer_in[i_in][1] = 1

                # ставим флажки
                flag[next_client] += 1
                flagAll[next_client] = 1

                # Уменьшаем кол-во машин которые к этому клиенту могут приехать
                countOfRaces[next_client] -= 1

                # плюс один клиент в машине
                numberInCar += 1

                RecursiveSearchSosed(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces, numberInCar)

            else:
                print("ERROR from RecursiveSearchSosed inside: ошибка в поске рандомного нового клиента")

        # Означает что вывалились из вайла,
        # потому что долго ждали, поэтому возвращаем машину в депо
        else:
            print("Слишком долго искали рандомного, while закончился по времени. Поэтому возвращаемся в депо.")
            # добавляем в ребенка bufer_in[i_in + 1]
            children.append([0, 0])
            # children[i][0] = 0

            # # Ставим флаг в последовательности в которой искали ребро в доп ячееки
            # bufer_in[i_in][1] = 1

            # ставим влаг
            flag[0] += 1
            flagAll[0] = 1

            # зануляем сяетчик, так как следом будет уже другая машина
            numberInCar = 0
            return

    # Если уже встретили ноль, но в последовательности слишком мало клиентов
    elif flag[bufer_in[i_in + 1][0]] == -1 and numberInCar < factory.min_num_cl_in_car:
        print("Слишком рано встретили ноль, в последовательности только", numberInCar, " клиентов")

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # берем рандомного клиента у кторого есть не посещенные скважины
        print("Берем рандомного клиента у кторого есть не посещенные скважины с помощью функции RandNotVisitClient")
        rand_client = RandNotVisitClient(countOfRaces)

        # номер позиции клиента bufer_out[i_out][0] в bufer_in
        i_in = NumberClientaInSequence(bufer_in, rand_client)
        print("Новый рандомный клиент ", rand_client, "находится под номером ", i_in, "в последовательности ")
        print(bufer_in)

        # добавляем в ребенка bufer_in[i_in + 1]
        children.append([rand_client, 0])
        # children[i][0] = rand_client

        # ставим флажки
        flag[bufer_in[i_in][0]] += 1
        flagAll[bufer_in[i_in][0]] = 1

        # Уменьшаем кол-во машин которые к этому клиенту могут приехать
        countOfRaces[bufer_in[i_in][0]] -= 1

        # плюс один клиент в машине
        numberInCar += 1

        RecursiveSearchSosed(children, bufer_out, bufer_in, i_in, flag, flagAll, countOfRaces, numberInCar)

    # это значит что встретили ноль, цикл должен завершится
    # Здесь все заебись!!!!!!!!!!
    elif flag[bufer_in[i_in + 1][0]] == -1 and numberInCar >= factory.min_num_cl_in_car:
        print("Встретили 0 пора возвращаться в депо")
        # добавляем в ребенка bufer_in[k_in][i_in + 1]
        children.append([bufer_in[i_in + 1][0], 0])
        # children[i][0] = bufer_in[i_in + 1][0]

        # Ставим флаг в последовательности в которой искали ребро в доп ячееки
        bufer_in[i_in][1] = 1

        # ставим влаг
        flag[bufer_in[i_in + 1][0]] += 1
        flagAll[bufer_in[i_in + 1][0]] = 1

        # зануляем сяетчик, так как следом будет уже другая машина
        numberInCar = 0
    else:
        print("ERROR from RecursiveSearchSosed outside: проблема с флагами, не нашли не ноль, не еще не посещенный")


# Добавляем клиента в последовательность, со всеми флагами
# ЗАебись!!!
def AddClientaInSequence(children, bufer, flag, flagAll, countOfRaces, i_in):
    # # Добавляем первые два города в ребенка
    # children[j][0] = bufer1[i_in][0]
    # j += 1
    # TODO children.append([bufer[i_in][0], 0])
    children.append([bufer[i_in][0], 0])

    # из первого нуля больше никуда не едем
    bufer[i_in][1] = 1

    # Расставляем флажки локально для первой машины и для общего решения
    flag[0] += 1
    flag[bufer[i_in][0]] = 1
    flagAll[bufer[i_in][0]] = 1
    # на одну мащину к нему (bufer1[1]) теперь может приехать меньше
    countOfRaces[bufer[i_in][0]] -= 1


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
        # bufer1[i][1] == 0 из которого еще не выезжали
        # bufer1[i+1][0] > 0 у которого еще есть свободные скважины
        if bufer1[i][0] == 0 and bufer1[i][1] == 0 and countOfRaces[bufer1[i + 1][0]] > 0:
            AddClientaInSequence(children, bufer1, flag, flagAll, countOfRaces, i + 1)
            RecursiveSearchSosed(children, bufer2, bufer1, i + 1, flag, flagAll, countOfRaces, numberInCar)
            return
            # return i+1

    # если не нашли в большем, ищем в меньшем
    for i in range(size2 - 1):
        # bufer2[i][0] == 0 ищем ноль,
        # bufer2[i][1] == 0 из которого еще не выезжали
        # countOfRaces[bufer2[i + 1][0]] > 0 у которого еще есть свободные скважины
        if bufer2[i][0] == 0 and bufer2[i][1] == 0 and countOfRaces[bufer2[i + 1][0]] > 0:
            AddClientaInSequence(children, bufer2, flag, flagAll, countOfRaces, i + 1)
            RecursiveSearchSosed(children, bufer1, bufer2, i + 1, flag, flagAll, countOfRaces, numberInCar)
            return
            # return i+1

    # если не нашли ноль, то ищем просто не посещенного
    for i in range(factory.N):
        # Если в первом и вотором не нашли то ищем просто не посещенный
        # впринципе и у которого есть свободные скважины!!
        if flagAll[i] == 0 and countOfRaces[i] > 0:
            # TODO здесь можно искать с минимальным расстоянием от нуля
            # Если нашли такого, то ищем этот город в большем решении
            # и из него мы еще не выезжали
            for j in range(size1 - 1):
                # bufer1[i][0] == 0 ищем этот итый город,
                # bufer1[i][1] == 0 из которого еще не выезжали
                if bufer1[j][0] == i and bufer1[j][1] == 0:
                    AddClientaInSequence(children, bufer1, flag, flagAll, countOfRaces, j)
                    RecursiveSearchSosed(children, bufer2, bufer1, j, flag, flagAll, countOfRaces)
                    return
                    # return j
            # если не нашли в большем, ищем в меньшем
            for j in range(size2 - 1):
                # bufer2[i][0] == 0 ищем ноль,
                # bufer2[i][1] == 0 из которого еще не выезжали
                if bufer2[j][0] == 0 and bufer2[j][1] == 0:
                    AddClientaInSequence(children, bufer2, flag, flagAll, countOfRaces, j)
                    RecursiveSearchSosed(children, bufer1, bufer2, j, flag, flagAll, countOfRaces)
                    return
                    # return j
        else:
            print("ERROR from SearchForAnUnvisitedZero: нарушенно заполнение флага")

    # TODO надо ли рассматривать клиентов у которых остались скважины
    # Если не нашли ни в большем ни в меньшем, и уже всех посетили хотя бы по разу
    # else:
    #     #рандомный клиент у которого есть свободные скважины
    #     new_client = RandomClientWithWells(countOfRaces)
    #     AddClientaInSequence(children, bufer1, flag, flagAll, countOfRaces, i + 1, jndex)
    #     RecursiveSearchSosed(children, jndex, bufer2, bufer1, i + 1, flag, flagAll, countOfRaces)
    #     return

    print("ERROR from SearchForAnUnvisitedZero: не нашли куда ехать, проблема с флагами")


# кроссовер AEX
def AEX(sequence1, sequence2):
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
        # children[1][0] = sequence1[1][0]

        # из первого нуля больше никуда не едем
        sequence1[0][1] = 1

        # Расставляем флажки локально для первой машины и для общего решения
        flag[sequence1[0][0]] += 1
        flag[sequence1[1][0]] = 1
        flagAll[sequence1[0][0]] = 1
        flagAll[sequence1[1][0]] = 1
        # на одну мащину к нему (bufer1[1]) теперь может приехать меньше
        countOfRaces[sequence1[1][0]] -= 1

        # Число задействованных машин в ребенке
        k = 0

        # один клиент в машине
        numberInCar += 1

        # Для первого добавления запустим без цикла
        RecursiveSearchSosed(children, sequence2, sequence1, 1, flag, flagAll, countOfRaces, numberInCar)

        # Обнуляем флаг для следующей машины
        for i in range(factory.N):
            flag[i] = 0
        flag[0] = -2

        # Добавляем еще одну машину + сдвигаем индекс последовательности
        k += 1

        counter = 0
        # Пока кол-во используемых машин не привысило доступного числа  k <= factory.K
        # или остались не посещенные города sum(flagAll) <= factory.N
        while sum(flagAll) <= factory.N and counter <= factory.N * 2:
            # Поиск номер в последовательности не посещенного нуля
            # или просто не посещенного
            # и его добавление в ребенка с расставлением всех флагов
            # и запуском рекурсии

            # SearchForAnUnvisitedZero(sequence1, size1, sequence2, size2, flagAll, countOfRaces, children, flag, j, numberInCar)

            #
            # # # Добавляем первые два города в ребенка
            # # children[j][0] = bufer1[i_in][0]
            # # j += 1
            # children[j][0] = bufer1[i_in][0]
            # j += 1
            # # из первого нуля больше никуда не едем
            # bufer1[i_in][1] = 1
            #
            # # Расставляем флажки локально для первой машины и для общего решения
            # flag[0] += 1
            # flag[bufer1[i_in]] = 1
            # flagAll[bufer1[i_in]] = 1
            # # на одну мащину к нему (bufer1[1]) теперь может приехать меньше
            # countOfRaces[bufer1[i_in]] -= 1
            #
            # RecursiveSearchSosed(children, j, bufer2, bufer1, i_in, flag, flagAll, countOfRaces)

            # Обнуляем флаг для следующей машины
            for i in range(factory.N):
                flag[i] = 0
            flag[0] = -2

            # Добавляем еще одну машину + сдвигаем индекс последовательности
            k += 1
            print(counter)
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
        # children[1][0] = sequence2[1][0]

        # из первого нуля больше никуда не едем
        sequence2[0][1] = 1

        # Расставляем флажки локально для первой машины и для общего решения
        flag[sequence2[0][0]] += 1
        flag[sequence2[1][0]] = 1
        flagAll[sequence2[0][0]] = 1
        flagAll[sequence2[1][0]] = 1
        # на одну мащину к нему (bufer1[1]) теперь может приехать меньше
        countOfRaces[sequence2[1][0]] -= 1

        # Число задействованных машин в ребенке
        k = 0

        # один клиент в машине
        numberInCar += 1

        # Для первого добавления запустим без цикла
        RecursiveSearchSosed(children, sequence1, sequence2, 1, flag, flagAll, countOfRaces, numberInCar)

        # Обнуляем флаг для следующей машины
        for i in range(factory.N):
            flag[i] = 0
        flag[0] = -2

        # Добавляем еще одну машину + сдвигаем индекс последовательности
        k += 1

        print("Построили для первой машины")

        # Пока кол-во используемых машин не привысило доступного числа  k <= factory.K
        # или остались не посещенные города sum(flagAll) <= factory.N
        counter = 0
        # TODO разобраться, когда всех посетили, но на одной машине
        while sum(flagAll) <= factory.N and counter <= factory.N * 5:
            # Поиск номер в последовательности не посещенного нуля
            # или просто не посещенного
            # и его добавление в ребенка с расставлением всех флагов
            # и запуском рекурсии

            # SearchForAnUnvisitedZero(sequence2, size2, sequence1, size1, flagAll, countOfRaces, children, flag, j, numberInCar)

            #
            # # # Добавляем первые два города в ребенка
            # # children[j][0] = bufer1[i_in][0]
            # # j += 1
            # children[j][0] = bufer1[i_in][0]
            # j += 1
            # # из первого нуля больше никуда не едем
            # bufer1[i_in][1] = 1
            #
            # # Расставляем флажки локально для первой машины и для общего решения
            # flag[0] += 1
            # flag[bufer1[i_in]] = 1
            # flagAll[bufer1[i_in]] = 1
            # # на одну мащину к нему (bufer1[1]) теперь может приехать меньше
            # countOfRaces[bufer1[i_in]] -= 1
            #
            # RecursiveSearchSosed(children, j, bufer2, bufer1, i_in, flag, flagAll, countOfRaces)

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
    print("children = ", children)
    print("sequence1 = ", sequence1)
    print("sequence2 = ", sequence2)
    print("wells = ", factory.wells)
    print("countOfRaces", countOfRaces)
