import factory
import random

""" Функции для кроссоверов"""


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
    count = 0
    for i in range(1, len(sequence)):
        if sequence[i] == [0, 0]:
            count += 1
    return count


# Выставляем сколько работает каждая машина на локации after
def WorkTimeCounting(sequence, y, s, after):
    local_count = sum(y[after])
    # print("На локации ", after, " работает ", local_count, " машин")

    # Считаем сколько хватит каждому скважин
    div = factory.wells[after] // local_count
    if div > 0:
        # print("Присваиваем каждой машине, которая работает на локации ", after, " ", div, "кол-во скважин")
        for k in range(len(s[0])):
            if y[after][k] == 1:
                s[after][k] = div * (factory.S[after] / factory.wells[after])

        div = factory.wells[after] % local_count
        if div == 0:
            print("Свободных скважин не осталось, мы все распределили")

        else:
            # print("Но у нас еще осталось ", div, " свободных скважин")
            # print("Создадим массив, в котором будут номера машин которые обслуживают этот город. Он равен ")

            k = 0
            car_for_after = []
            for i in range(1, len(sequence)):
                if sequence[i][0] == 0 and sequence[i][0] == sequence[-1][0]:
                    k += 1
                elif sequence[i][0] != 0 and sequence[i][0] == after:
                    car_for_after.append(k)

            # print(car_for_after)

            # print("Распределяем рандомным клиентам оставшиеся скважины")
            while div > 0:
                car = random.choice(car_for_after)
                # print("Назначаем машине с номером ", car, " еще одну скважину")
                s[after][car] += factory.S[after] / factory.wells[after]
                car_for_after.remove(car)
                # print("Осталось распределить ", div, " скважин по ")
                # print(car_for_after, " клиентам")
                div -= 1

    else:
        print("ERROR from WorkTimeCounting: Почему-то оказалось скважин меньше чем приехавших машин")


# Находим время прибытия к after
def ArrivalTime(a, s, before, after, k):
    # print("Считаем время прибытия на локацию")
    time = a[before][k] + s[before][k] + factory.t[before][after]

    # print("Дерективный срок = ", factory.e[after])
    # print("Фактическое время прибытия = ", time)
    if factory.e[after] >= time:
        # print("Приехали слишком рано ждем начало временного окна")
        return factory.e[after]

    elif factory.e[after] < time:
        # print("Опоздали на начало работ")
        return time


# Преобразуем последовательность в матрицы решений
def SequenceDisplayInTheXYSA(sequence):
    # print("Переделываем последовательность в матрицы решений")

    count_car = CountUsedMachines(sequence)
    print("Количество машин используемых ребенком = ", count_car)
    count_carBig = count_car
    if count_car < factory.K:
        count_carBig = factory.K

    x = [[[0 for k in range(count_carBig)] for j in range(factory.N)] for i in
         range(factory.N)]  # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(count_carBig)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(count_car):
        y[0][k] = 1
    s = [[0 for k in range(count_carBig)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(count_carBig)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    k = 0
    # print("Теперь перейдем к заполнению матрицы Х У")
    for i in range(1, len(sequence)):
        before = sequence[i - 1][0]
        after = sequence[i][0]
        # print("Предыдущий посещенный ", before)
        # print("Которого вставляем ", after)

        if sequence[i][0] == 0:
            x[before][after][k] = 1
            y[after][k] = 1

            k += 1
            # print("Увидели 0, значит переходим к следующей машине с номером ", k)
            if k == count_car:
                # print("Кол-во используемых авто ", count_car)
                break
        else:
            x[before][after][k] = 1
            y[after][k] = 1

    k = 0
    # print("Теперь заполним А и S")
    for i in range(1, len(sequence)):
        before = sequence[i - 1][0]
        after = sequence[i][0]
        # print("Предыдущий посещенный ", before)
        # print("Которого вставляем ", after)

        if after == 0:
            a[after][k] = a[before][k] + factory.t[before][after]
            k += 1
            # print("Увидели 0, значит переходим к следующей машине с номером ", k)
            if k == count_car:
                # print("Кол-во используемых авто ", count_car)
                break

        if after != 0:
            try:
                if sequence.index([after, 0], 0, i) > 0:
                    print("Уже считали для этого ", after, " города")

            except ValueError:
                # print("До этого еще не встречали город ", after)
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
def RandNotVisitClient(countOfRaces, flag, file):
    file.write("RandNotVisitClient start: ->\n")
    # массив для не посещенных городов
    count_not_visit = []

    for i in range(len(countOfRaces)):
        # если у кого-то клиента есть свободные скважины,
        if countOfRaces[i] != 0 and flag[i] == 0:
            # то сохраняем номер этого клиента
            count_not_visit.append(i)

    file.write("    Of RandNotVisitClient: создали массив, у каких клиентов остались свободные скважины" + '\n')
    file.write("    " + str(count_not_visit) + '\n')

    try:
        # берем рандомного из списка не посещенных
        i = random.choice(count_not_visit)
        file.write("    Взяли рандомного из этого списка равного " + str(i) + '\n')
        file.write("RandNotVisitClient stop: <-\n")
        return i

    except IndexError:
        file.write("    Больше нет клиентов с свободными скважинами" + '\n')
        file.write("RandNotVisitClient stop: <-\n")
        return -1


# Добавляем клиента в последовательность, со всеми флагами
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


# Выбор случайного первого клиента
def SelectFirstObj(sequence1, sequence2, flagAll, file):
    buf = []
    file.write("SelectFirstObj start: ->\n")

    file.write("    Ищем первые объекты в маршрутах из решения\n    " + str(sequence1) + "\n")
    for i in range(1, len(sequence1)):
        if i == 1 and flagAll[i] == 0:
            buf.append(i)
        elif i != len(sequence1) - 1 and sequence1[i - 1] != [0, 0] and sequence1[i] == [0, 0] and sequence1[i + 1] != [
            0, 0] \
                and flagAll[sequence1[i + 1][0]] == 0:
            buf.append(sequence1[i + 1][0])

    file.write("    Ищем первые объекты в маршрутах из решения\n    " + str(sequence2) + "\n")
    for i in range(1, len(sequence2)):
        if i == 1 and flagAll[i] == 0:
            buf.append(i)
        elif i != len(sequence2) - 1 and sequence2[i - 1] != [0, 0] and sequence2[i] == [0, 0] and sequence2[i + 1] != [
            0, 0] \
                and flagAll[sequence2[i + 1][0]] == 0:
            buf.append(sequence2[i + 1][0])

    if buf:
        file.write("buf = " + str(buf) + '\n')
        file.write("SelectFirstObj stop: <-\n")
        return random.choice(buf)
    else:
        file.write("    Не нашли ни одного не посещенного первого, берем любого\n")

        file.write("    Ищем первые объекты в маршрутах из решения\n    " + str(sequence1) + "\n")
        for i in range(1, len(sequence1)):
            if i == 1 and flagAll[i] == 0:
                buf.append(i)
            elif i != len(sequence1) - 1 and sequence1[i - 1] != [0, 0] and sequence1[i] == [0, 0] and sequence1[
                i + 1] != [0, 0]:
                buf.append(sequence1[i + 1][0])

        file.write("    Ищем первые объекты в маршрутах из решения\n    " + str(sequence2) + "\n")
        for i in range(1, len(sequence2)):
            if i == 1 and flagAll[i] == 0:
                buf.append(i)
            elif i != len(sequence2) - 1 and sequence2[i - 1] != [0, 0] and sequence2[i] == [0, 0] and sequence2[
                i + 1] != [0, 0]:
                buf.append(sequence2[i + 1][0])

        file.write("    buf = " + str(buf) + '\n')
        file.write("SelectFirstObj stop: <-\n")
        return random.choice(buf)


# функция возвращает ребро в случаи неопределенности
def Uncertainty(start, flag, file):
    file.write("    Uncertainty start:->\n")
    buf = []
    file.write("        Задаем заданное число случайных ребер c началом " + str(start) + "\n")
    for i in range(factory.param_hgrex_uncertainty):
        buf.append(random.randint(1, factory.N - 1))
    file.write("        buf = " + str(buf) + "\n")

    file.write("        Считаем минимальное ребро\n")
    minimum = factory.d[start][buf[0]]
    j = 0
    flagok = 0
    for i in range(len(buf)):
        if minimum >= factory.d[start][buf[i]] and buf[i] != start and flag[buf[i]] != 1:
            flagok = 1
            minimum = factory.d[start][buf[i]]
            j = i
            file.write("        minimum = " + str(minimum) + '\n')
            file.write("        j = " + str(j) + '\n')

    if flagok == 1:
        file.write("    Uncertainty stop:<-\n")
        file.write("GetShortArc stop: <-\n")
        return buf[j]
    else:
        file.write("    Uncertainty stop:<-\n")
        file.write("   С первого раза не получилось разрешить неопределенность попробуем еще раз")
        return Uncertainty(start, flag, file)


# Возвращаем самое короткое ребро из двух родителей
def GetShortArc(sequence1, sequence2, start, flag, numberInCar, file):
    file.write("GetShortArc start: ->\n")

    file.write("    Ищем индексы всех таких объектов" + '\n')
    buf1 = []
    buf2 = []
    for i in range(len(sequence1)):
        if sequence1[i][0] == start and flag[sequence1[i + 1][0]] <= 0 and sequence1[i + 1][1] == 0:
            buf1.append(i)
    file.write("    В первом решении объект " + str(start) + " имеет индексы " + str(buf1) + '\n')

    for i in range(len(sequence2)):
        if sequence2[i][0] == start and flag[sequence2[i + 1][0]] <= 0 and sequence2[i + 1][1] == 0:
            buf2.append(i)
    file.write("    Во втором решении объект " + str(start) + " имеет индексы " + str(buf2) + '\n')

    if buf1 == [] and buf2 == []:
        file.write("    Не нашли ни одноготакого ребра, ослабим условия\n")
        for i in range(len(sequence1)):
            if sequence1[i][0] == start and flag[sequence1[i + 1][0]] <= 0:
                buf1.append(i)
        file.write("    В первом решении объект " + str(start) + " имеет индексы " + str(buf1) + '\n')

        for i in range(len(sequence2)):
            if sequence2[i][0] == start and flag[sequence2[i + 1][0]] <= 0:
                buf2.append(i)
        file.write("    Во втором решении объект " + str(start) + " имеет индексы " + str(buf2) + '\n')

    file.write("    Составляем массив расстояний" + '\n')
    distance1 = []
    distance2 = []
    for i in range(len(buf1)):
        index = sequence1[buf1[i]][0]
        jndex = sequence1[buf1[i] + 1][0]
        distance1.append(factory.d[index][jndex])
    file.write("    distance1 = " + str(distance1) + '\n')

    for i in range(len(buf2)):
        index = sequence2[buf2[i]][0]
        jndex = sequence2[buf2[i] + 1][0]
        distance2.append(factory.d[index][jndex])
    file.write("    distance2 = " + str(distance2) + '\n')

    try:
        min1 = min(distance1)
        file.write("    min1 = " + str(min1) + '\n')
    except ValueError:
        try:
            min2 = min(distance2)
            file.write("    min2 = " + str(min2) + '\n')
        except ValueError:
            return Uncertainty(start, flag, file)

    try:
        min2 = min(distance2)
        file.write("    min2 = " + str(min2) + '\n')
    except ValueError:
        index = distance1.index(min1)
        if buf1[index] != 0 and numberInCar >= factory.param_min_num_cl_in_car:
            file.write("GetShortArc stop: <-\n")
            return buf1[index]
        elif buf2[index] == 0 and numberInCar < factory.param_min_num_cl_in_car:
            file.write("    Неопределенность, вернулись в ноль когда слишком мало клиентов в машине\n")
            return Uncertainty(start, flag, file)

    if min1 >= min2:
        file.write("   min1 >= min2\n")
        index = distance2.index(min2)
        if numberInCar >= factory.param_min_num_cl_in_car:
            file.write("GetShortArc stop: <-\n")
            return sequence2[buf2[index] + 1][0]

        elif numberInCar < factory.param_min_num_cl_in_car:

            if sequence2[buf2[index] + 1][0] == 0:
                file.write("    Неопределенность, вернулись в ноль когда слишком мало клиентов в машине\n")

                return Uncertainty(start, flag, file)

            else:
                file.write("GetShortArc stop: <-\n")
                return sequence2[buf2[index] + 1][0]

    elif min2 > min1:
        file.write("   min2 > min1\n")
        index = distance1.index(min1)
        if numberInCar >= factory.param_min_num_cl_in_car:
            file.write("GetShortArc stop: <-\n")
            return sequence1[buf1[index] + 1][0]

        elif numberInCar < factory.param_min_num_cl_in_car:

            if sequence1[buf1[index] + 1][0] == 0:
                file.write("    Неопределенность, вернулись в ноль когда слишком мало клиентов в машине\n")

                return Uncertainty(start, flag, file)

            else:
                file.write("GetShortArc stop: <-\n")
                return sequence1[buf1[index] + 1][0]
