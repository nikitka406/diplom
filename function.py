from functionFromCross import *
from forFile import *
from math import *


# красивая печать
def BeautifulPrint(X, Y, Sresh, A):
    for k in range(len(X[0][0])):
        print('Номер машины ', k)
        for i in range(factory.N):
            for j in range(factory.N):
                print(X[i][j][k], end=' ')
            print("\n")

        print("e = ", end=' ')
        for i in range(factory.N):
            print(factory.e[i], end=' ')
        print("\n")

        print("l = ", end=' ')
        for i in range(factory.N):
            print(factory.l[i], end=' ')
        print("\n")

        print("y = ", end=' ')
        for i in range(factory.N):
            print(Y[i][k], end=' ')
        print("\n")

        print("a = ", end=' ')
        for i in range(factory.N):
            print(A[i][k], end=' ')
        print("\n")

        print("s = ", end=' ')
        for i in range(factory.N):
            print(Sresh[i][k], end=' ')
        print("\n")
    #
    # for i in range(factory.N):
    #     for k in range (factory.N):
    #        print(factory.t[i][k], end=' ')
    #     print('\n')

    # for i in range(factory.N):
    #     #     for k in range (factory.N):
    #     #         print(factory.d[i][k], end=' ')
    #     #     print('\n')


# красивая печать в файл
def BeautifulPrintInFile(lokal_X, lokal_Y, lokal_Sresh, lokal_A, target_function, number_solution):
    file = open('output/Population.txt', 'a')
    file.write('Номер решения ' + str(number_solution))
    file.write("\n")
    for k in range(len(lokal_X[0][0])):
        file.write('Номер машины ' + str(k))
        file.write("\n")
        for i in range(factory.N):
            for j in range(factory.N):
                file.write(str(lokal_X[i][j][k]) + ' ')
            file.write("\n")
        file.write("\n")

        file.write("e = ")
        for i in range(factory.N):
            file.write(str(factory.e[i]) + ' ')
        file.write("\n")

        file.write("l = ")
        for i in range(factory.N):
            file.write(str(factory.l[i]) + ' ')
        file.write("\n")

        file.write("y = ")
        for i in range(factory.N):
            file.write(str(lokal_Y[i][k]) + ' ')
        file.write("\n")

        file.write("a = ")
        for i in range(factory.N):
            file.write(str(lokal_A[i][k]) + ' ')
            # for k in range(factory.KA):
            #     print(A[i][k], end=' ')
            # print("\n")
        file.write("\n")

        file.write("s = ")
        for i in range(factory.N):
            file.write(str(lokal_Sresh[i][k]) + ' ')
            # for k in range(factory.KA):
            #     print(Sresh[i][k], end=' ')
            # print("\n")
        file.write("\n")
    file.write(str(target_function))
    file.write("\n")
    file.write("\n")
    # for i in range(factory.N):
    #     for k in range (factory.N):
    #        file.write(factory.t[i][k]+' ')
    #     file.write('\n')

    # for i in range(factory.N):
    #     #     for k in range (factory.N):
    #     #         print(factory.d[i][k], end=' ')
    #     #     print('\n')
    file.close()


# печать конкретного маршрута и время работы
def PrintForCar(lokal_X, lokal_Sresh, car1, file, car2):
    sequenceX2 = GettingTheSequence(lokal_X)
    file.write("car1 = " + str(sequenceX2[car1]) + '\n')
    for i in range(factory.N):
        file.write(str(lokal_Sresh[i][car1]) + ' ')
    file.write("\n")

    file.write("car2 = " + str(sequenceX2[car2]) + '\n')
    for i in range(factory.N):
        file.write(str(lokal_Sresh[i][car2]) + ' ')
    file.write("\n")
    # if car2 != 'def':
    #     file.write("car2 = " + str(sequenceX2[car2]) + '\n')
    #     for i in range(factory.N):
    #         file.write(str(lokal_Sresh[i][car2]) + '\n')


# Считаем кол-во используемых ТС
def AmountCarUsed(lokal_y):
    summa = 0  # счетчик
    amount = 0  # число машин
    for k in range(len(lokal_y[0])):
        for j in range(1, factory.N):
            summa += lokal_y[j][k]  # смотрим посещает ли К-ая машина хотя бы один город
        if summa != 0:  # если не 0 значит  посетила
            amount += 1  # прибавляем еденичку
        summa = 0  # Обнуляем счетчик
    return amount


# копирование решения
def CopyingSolution(local_x, local_y, local_s, local_a):
    local_X = local_x.copy()
    # local_X = [[[0 for k in range(len(local_x[0][0]))] for j in range(factory.N)] for i in
    #      range(factory.N)]  # едет или нет ТС с номером К из города I в J
    # # for k in range(factory.KA):
    # for i in range(factory.N):
    #     local_X[i] = list(local_x[i])
    #     for j in range(factory.N):
    #             local_X[i][j][k] = local_x[i][j][k]
    local_Y = local_y.copy()
    local_S = local_s.copy()
    local_A = local_a.copy()
    return local_X, local_Y, local_S, local_A


# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, pinalty_function=0):
    target_function = 0
    for k in range(len(x[0][0])):
        for i in range(factory.N):
            for j in range(factory.N):
                target_function += factory.d[i][j] * x[i][j][k]

    # target_function = target_function/5
    target_function += pinalty_function
    return target_function


# Распределяем на каждую локацию по машине
def OneCarOneLocation():
    # копия переменной задачи Х, только кол-вo машин = число локаций
    x = [[[0 for k in range(factory.KA)] for j in range(factory.N)] for i in
         range(factory.N)]  # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(factory.KA):
        y[0][k] = 1
    s = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(factory.KA)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    # поочереди отправляем ТС на локации, по одному на скважину
    k = 0
    for j in range(1, factory.N):
        if factory.wells[j] >= 1:
            for i in range(factory.wells[j]):
                x[0][j][k] = 1  # туда
                x[j][0][k] = 1  # обратно
                y[j][k] = 1
                if factory.wells[j] > 1:
                    s[j][k] = factory.S[j] / factory.wells[j]
                else:
                    s[j][k] = factory.S[j]

                if factory.e[j] > factory.t[0][j]:
                    a[j][k] = factory.e[j]
                    a[0][k] = a[j][k] + s[j][k] + factory.t[j][0]
                else:
                    a[j][k] = factory.t[0][j]
                    a[0][k] = a[j][k] + s[j][k] + factory.t[j][0]
                # print(a[j][k], end=' ')
                k += 1
            # print("\n")
    return x, y, s, a


# удаляем машину с локации если позволяют огр
def DeleteCarNonNarushOgr(sizeK):
    # Убираем одну машину
    for i in range(1, factory.N):
        # копии чтобы не испортить исходное решение
        lokal_X, lokal_Y, lokal_Sresh, lokal_A = ReadStartSolutionOfFile(sizeK)

        if factory.wells[i] > 1:  # Выбираем только те локации у которых больше одной скважины
            for k in range(sizeK - 1):
                if lokal_Y[i][k] == 1 and lokal_Y[i][k + 1] == 1:  # -//- ту машину за которой едет еще одна
                    lokal_Y[i][k] = 0
                    lokal_Y[0][k] = 0
                    lokal_Sresh[i][k + 1] += lokal_Sresh[i][k]
                    lokal_Sresh[i][k] = 0
                    lokal_A[i][k] = 0
                    lokal_X[0][i][k] = 0
                    lokal_X[i][0][k] = 0
                    # target_function -= car_cost
                    if VerificationOfBoundaryConditions(lokal_X, lokal_Y, lokal_Sresh, lokal_A) == 1:
                        # BeautifulPrint(lokal_X, lokal_Y, lokal_Sresh, lokal_A)
                        SaveStartSolution(lokal_X, lokal_Y, lokal_Sresh, lokal_A)
                        # Если ограничения не сломались то сохраняем эти изменения
                    else:
                        lokal_X, lokal_Y, lokal_Sresh, lokal_A = ReadStartSolutionOfFile(sizeK)


# перезапись одного маршрута на другой
def Rewriting(lokal, k, m, flag):
    if flag == "1":
        for j in range(factory.N):
            lokal[j][k] = lokal[j][m]
            lokal[j][m] = 0
    if flag == "2":
        for i in range(factory.N):
            for j in range(factory.N):
                lokal[i][j][k] = lokal[i][j][m]
                lokal[i][j][m] = 0


# TODO делит почему портит стартовое решение
# TODO надо полностью переписать делит с помощью флага и последующео удаления через remove
# удаляем/уменьшаем размерность с помощью не используемых машин
def DeleteNotUsedCar(lokal_x, lokal_y, lokal_s, lokal_a):
    # todo сейчас удаляются машину пока получается, надо чтобы оставались те которые наши(не арендованные) под
    #  вопросом?????
    for k in range(len(lokal_x[0][0])):
        summa1 = 0  # Обнуляем счетчик
        for j in range(1, factory.N):
            # смотрим посещает ли К-ая машина хотя бы один город
            summa1 += lokal_y[j][k]
        if summa1 == 0:  # если 0 значит не посещает
            if k != len(lokal_x[0][0]) - 1:  # если пустой машиной оказалась не последняя в списке, то
                for m in range(k + 1, len(lokal_x[0][0])):  # ищем ближайшую рабочую машину
                    summa2 = 0
                    for i in range(factory.N):
                        summa2 += lokal_y[i][m]
                    if summa2 != 0:  # сохранем ее в первый пустой маршрут
                        Rewriting(lokal_y, k, m, "1.txt")
                        Rewriting(lokal_s, k, m, "1.txt")
                        Rewriting(lokal_a, k, m, "1.txt")
                        Rewriting(lokal_x, k, m, "2")
                        break

            factory.KA = AmountCarUsed(lokal_y)
            if factory.KA > factory.K - 1:
                # создаем новые переменные так как они должны быть меньше по размерности относительно старых,
                # нельзя просто прировнять
                lokal_X = [[[0 for k in range(factory.KA)] for j in range(factory.N)] for i in
                           range(factory.N)]  # едет или нет ТС с номером К из города I в J
                lokal_Y = [[0 for k in range(factory.KA)] for i in
                           range(factory.N)]  # посещает или нет ТС с номером К объект i
                lokal_Sresh = [[0 for k in range(factory.KA)] for i in
                               range(factory.N)]  # время работы ТС c номером К на объекте i
                lokal_A = [[0 for k in range(factory.KA)] for i in
                           range(factory.N)]  # время прибытия ТС с номером К на объект i
                for k in range(factory.KA):
                    for i in range(factory.N):
                        for j in range(factory.N):
                            lokal_X[i][j][k] = lokal_x[i][j][k]
                        lokal_Y[i][k] = lokal_y[i][k]
                        lokal_Sresh[i][k] = lokal_s[i][k]
                        lokal_A[i][k] = lokal_a[i][k]
                return lokal_X, lokal_Y, lokal_Sresh, lokal_A
            else:
                print("NOTIFICATION from DeleteNotUsedCar: Уже удалены все арендованные машины")
                return lokal_x, lokal_y, lokal_s, lokal_a


# ищем минимальный путь по которому можно попасть в client
def SearchTheBestSoseda(client):
    neighbor = 0  # старый сосед
    bufer = factory.d[0][client]  # расстояние от старого сосед адо клиента
    for i in range(factory.N):
        if bufer >= factory.d[i][client] and i != client:
            # ищим мин расстояние до клиента с учетом что новый сосед не клиент
            bufer = factory.d[i][client]
            neighbor = i
    return neighbor


# Возвращает рандомного клиента и машину
def ChooseRandomObjAndCar(y, sizeK):
    # Выбираем рандомную машину
    if sizeK > 1:
        car = random.randint(0, (sizeK-1))
        while not CarIsWork(y, car):
            car = random.randint(0, (sizeK-1))
    else:
        car = 0

    # ЗАпоминаем всех кого она обслуживает
    buf = []
    for i in range(1, factory.N):
        if y[i][car] == 1:
            buf.append(i)
    # Выбираем случайного среди них
    client = random.choice(buf)
    return client, car


# ищем соседа слева либо справа
def SearchSosedLeftOrRight(x, y, client, leftOrRight, k=-1):
    if leftOrRight == "left":
        for i in range(factory.N):  # ищем по строке
            if x[i][client][k] == 1:
                return i
        return -1
    if leftOrRight == "right":
        for i in range(factory.N):  # ищем по столбцу
            if x[client][i][k] == 1:
                return i
        return -1
    if leftOrRight != "left" and leftOrRight != "right":
        print("ERROR from SearchSosedLeftOrRight: неверное значение переменной leftOrRight")


# Работает ли машина
def CarIsWork(y, k):
    suma = 0
    for i in range(1, factory.N):
        if y[i][k] == 1:
            suma += 1

    if suma != 0:
        return True
    else:
        return False


# Рекурсия чтобы заполнить время прибытия
def RecursiaForTime(x, s, a, i, k, recurs):
    for j in range(factory.N):
        if x[i][j][k] == 1 and j != 0 and recurs < factory.N:
            # print("Нашли соседа для ", i, " справа ", j)
            # print("Время перемещения из ", i, " в ", j, " = ", factory.t[i][j])
            # print("Время начало работ на объкекте " + str(j) + " = " + str(factory.e[j]))
            # если время прибытия меньше начала работ, то ждем
            if factory.e[j] > a[i][k] + s[i][k] + factory.t[i][j]:
                # print("Приехали слишком рано ждем")
                a[j][k] = factory.e[j]
                # print("a[j][k] = ", a[j][k], '\n')
            # иначе ставим время прибытия
            else:
                # print("Опоздали")
                a[j][k] = a[i][k] + s[i][k] + factory.t[i][j]
                # print("a[j][k] = ", a[j][k], '\n')

            recurs += 1
            RecursiaForTime(x, s, a, j, k, recurs)

        elif x[i][j][k] == 1 and j == 0 and recurs < factory.N:
            # print("Встретили ноль, пора заканчивать рекурсию")
            # print("Время прибытия в ", i, " = ", a[i][k])
            # print("Время работы в ", i, " = ", s[i][k])
            # print("Время переиещения из ", i, " в ", j, " = ", factory.t[i][j])

            a[j][k] = a[i][k] + s[i][k] + factory.t[i][j]

            # print("Время прибытия в депо = ", a[j][k], '\n')
            return True

        elif recurs > factory.N:
            return False


# определяем время приезда для всех локаций
# определяем время приезда для всех локаций
def TimeOfArrival(x, y, s, file):
    file.write("    Начнем заполнять время прибытия\n")
    a = [[0 for k in range(len(s[0]))] for i in range(factory.N)]
    for k in range(len(s[0])):
        if CarIsWork(y, k):
            # print("ЗАходим в рекурсию")
            RecursiaForTime(x, s, a, 0, k, 0)
    if not a:
        return -1
    return a


# удаляем клиента из выбранного  маршрут
def DeleteClientaFromPath(x, y, s, a, client, k):
    clientLeft = SearchSosedLeftOrRight(x, y, client, "left", k)  # ищем город перед клиентом
    clientRight = SearchSosedLeftOrRight(x, y, client, "right", k)  # ищем город после клиента
    # если у клиента есть сосед справо и слево
    if clientLeft != -1 and clientRight != -1:
        if clientLeft != clientRight:
            x[clientLeft][clientRight][k] = 1  # соединяем левого и правого соседа
        else:
            x[clientLeft][clientRight][k] = 0

        x[client][clientRight][k] = 0  # удаляем ребро клиента с правым соседом
        x[clientLeft][client][k] = 0  # удаляем ребро клиента с левым соседом

        # У и S для левого и правого не меняются, но время прибытия меняется
        y[client][k] = 0  # машина К больше не обслуживает клиента
        s[client][k] = 0  # время работы машины К у клиента = 0
        a[client][k] = 0  # машина не прибывает к клиенту
        a[0][k] = 0
        # a = TimeOfArrival(x, y, s, file)
        # если удаляем клиента и остается только депо, ставим там 0
        summa = 0
        for i in range(1, factory.N):
            summa += y[i][k]
        if summa == 0 and y[0][k] == 1:
            y[0][k] = 0

    elif clientLeft == -1 or clientRight == -1:
        print("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")  # log
        raise IOError("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")

    return x, y, s, a


# штрафнвя функция
def PenaltyFunction(y, s, a):
    penalty_sum = 0
    day = [0 for i in range(factory.N)]
    for k in range(len(y[0])):
        for i in range(factory.N):
            day[i] += max(0, ((a[i][k] + s[i][k]) - factory.l[i]))

    for i in range(factory.N):
        penalty_sum += day[i]*factory.fineCof[i]

    # если кол-во используемых ТС пока еще боьше чем число допустимых, тогда штрафуем
    fine = 0
    if AmountCarUsed(y) > factory.K:
        fine = max(0, (AmountCarUsed(y) - factory.K) * factory.car_cost)

    return penalty_sum + fine


# Создаем хранилище решений, для большего числа рещений
def SolutionStore(target_start, sizeK):
    # Хранилище решений, первый индекс это номер решения, со второго начинается само решение
    X = [0 for n in range(factory.param_population)]  # едет или нет ТС с номером К из города I в J
    for n in range(factory.param_population):
        X[n] = [[[0 for k in range(sizeK)] for j in range(factory.N)] for i in range(factory.N)]

    Y = [0 for n in range(factory.param_population)]  # посещает или нет ТС с номером К объект i
    for n in range(factory.param_population):
        Y[n] = [[0 for k in range(sizeK)] for i in range(factory.N)]

    Sresh = [0 for n in range(factory.param_population)]  # время работы ТС c номером К на объекте i
    for n in range(factory.param_population):
        Sresh[n] = [[0 for k in range(sizeK)] for i in range(factory.N)]

    A = [0 for n in range(factory.param_population)]  # время прибытия ТС с номером К на объект i
    for n in range(factory.param_population):
        A[n] = [[0 for k in range(sizeK)] for i in range(factory.N)]

    Target_Function = [target_start for n in
                       range(factory.param_population)]  # здесь сохраняем результат целевой функции для каждого решения

    SizeSolution = [sizeK for n in
                    range(factory.param_population)]  # здесь сохраняем размер каждого решения в популяции

    Fine = [0 for n in range(factory.param_population)]  # Здесь число дней которые опоздали для каждого объекта

    return X, Y, Sresh, A, Target_Function, SizeSolution, Fine


# Проверка на содержание хвоста в новом начале
def IsContainTailInStart(sequence, tail, place1, file):
    for i in range(len(tail)):
        if IsContainWells(sequence, tail[i], file, place1, "start"):
            return True
    return False


def IsContainTailInEnd(sequence, tail, place1, file):
    for i in range(len(tail)):
        if IsContainWells(sequence, tail[i], file, place1, "end"):
            return True
    return False


def IsContainTailInTail(tail1, tail2, file):
    for i in range(len(tail2)):
        if IsContainWells(tail1, tail2[i], file):
            return True
    return False


# Проверка на содержание скважин тех же объектов car у soseda
def IsContainWells(sequence, client, file, place='all', flag='start'):
    # file.write("IsContainWells start: ->\n")
    if flag == 'start':
        if place == 'all':
            size = len(sequence)
        else:
            size = sequence.index(place) + 1
        for i in range(size):
            # file.write("    " + str(sequence[i]) + ' == ' + str(client) + '     ')
            if sequence[i] == client and client != 0 and sequence[i] != 0:
                # file.write("\nIsContainWells stop: <-\n")

                return True
        # file.write("\nIsContainWells stop: <-\n")
        return False

    elif flag == 'end':
        start = sequence.index(place)
        for i in range(start, len(sequence)):
            # file.write("    " + str(sequence[i]) + ' == ' + str(client) + '    ')
            if sequence[i] == client:
                # file.write("\nIsContainWells stop: <-\n")
                return True
        # file.write("\nIsContainWells stop: <-\n")
        return False


# Возвращает номер объекта который обслуживает конкретная машина
def GetObjForCar(y, car):
    result = []
    for i in range(1, factory.N):
        if y[i][car] == 1:
            result.append(i)
    return result


# Возвращает число скважин которые не уложились во временное окно
def CountWellsWithFane(s, a, i, k):
    # Если приехали во временное окно
    if factory.e[i] <= a[i][k] <= factory.l[i]:
        # мах на случай если уложились
        return max(0, ceil((a[i][k] + s[i][k] - factory.l[i]) / (factory.S[i] / factory.wells[i])))
    # Если приехали позже окончания работ
    else:
        # Возвращаем число скважин конкретно на этом объекте этой машиной
        return int(s[i][k] / (factory.S[i] / factory.wells[i]))


# Подсчет сколько объектов обслуживает машина
def CountObjInCar(y, car):
    count = 0
    for i in range(1, factory.N):
        if y[i][car] == 1:
            count += 1
    return count


# Поиск хвоста
def SearchTail(x, client, clientCar, file):
    # TODO Можно сюда передавать последовательность, но если нет то искать
    file.write("SearchTail start: ->\n")
    sequence = GettingTheSequence(x)
    file.write("    Ищем хвост для маршрута\n")
    file.write("    " + str(sequence[clientCar]) + "\n      начиная с объекта " + str(client) + '\n')
    tail = []
    start = sequence[clientCar].index(client)
    for i in range(start, len(sequence[clientCar])):
        if sequence[clientCar][i] != 0:
            tail.append(sequence[clientCar][i])
        else:
            break
    tail.append(0)
    file.write("    Хвост = " + str(tail) + '\n')
    file.write("SearchTail stop: <-\n")
    return tail, sequence


# Сохраняем время работы
def SaveTime(s, tail, car, file):
    file.write("    SaveTime start: ->" + '\n')
    time = []
    for i in range(len(tail)):
        index = tail[i]
        time.append(s[index][car])
    file.write("        Время работы на каждом объекте хвоста = \n")
    file.write("        " + str(time) + '\n')
    file.write("    SaveTime stop: <-\n")
    return time


# Удаление хвоста
def DeleteTail(x, y, s, a, sosed, tail, car,  file, tail0="def"):
    file.write("    DeleteTail start: ->\n")
    sos = sosed
    for i in range(len(tail)):
        x[sos][tail[i]][car] = 0
        sos = tail[i]
        y[tail[i]][car] = 0
        s[tail[i]][car] = 0
        a[tail[i]][car] = 0

    if tail0 != 'def':
        x[tail[-1]][tail0][car] = 0

    file.write("    DeleteTail stop: <-\n")
    return x, y, s, a


# Подбрасываем монетку, берем эту окрестность или нет
def ResultCoins(monetochka=factory.coinsLS):
    coins = random.choice(monetochka)
    if coins == 1:
        return True
    else:
        return False


# Проверка ограничений и подсчет целевой
def Checker(X, Y, Sresh, A, SizeK, iteration, name, file):
    file.write("    СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ" + '\n')
    if window_time_up(A, Sresh, Y, file) == 0:
        if VerificationOfBoundaryConditions(X, Y, Sresh, A, "true", file) == 1:
            file.write("    NOTIFICATION from " + name + ": вставили с нарушением временного окна" + '\n')
            Target_Function = CalculationOfObjectiveFunction(X, PenaltyFunction(Y, Sresh, A))
            file.write("    Подсчет целевой функции после вставления " + str(Target_Function) + '\n')
            return X, Y, Sresh, A, Target_Function, SizeK
        else:
            file.write(
                "   ERROR from " + name + ": не получилось переставить, потому что сломались ограничения, возвращаем "
                "стартовое" + '\n')
            return -1

    elif VerificationOfBoundaryConditions(X, Y, Sresh, A, "false", file) == 1:
        file.write("    NOTIFICATION from " + name + ": вставили без нарушений ограничений" + '\n')
        Target_Function = CalculationOfObjectiveFunction(X, PenaltyFunction(Y, Sresh, A))
        file.write("    Подсчет целевой функции после вставления " + str(Target_Function) + '\n')
        return X, Y, Sresh, A, Target_Function, SizeK
    else:
        file.write("ERROR from " + name + ": не получилось переставить, потому что сломались ограничения, возвращаем "
                   "стартовое" + '\n')
        return -1


# Добавляем подпоследовательности в маршрут в Exchange
def AddSubSeqInPath(X, Y, Sresh, subseq1, subseq2Left, car2, time1, start=0):
    for i in range(start, len(subseq1)):
        X[subseq2Left][subseq1[i]][car2] = 1
        Y[subseq1[i]][car2] = 1
        Sresh[subseq1[i]][car2] += time1[i]
        subseq2Left = subseq1[i]
    return X, Y, Sresh, subseq2Left


# Подсчет числа дней которые не укладываются в временное окно
def FineDay(s, a, sizeK):
    Fine = [0 for i in range(factory.N)]
    for k in range(sizeK):
        for i in range(factory.N):
            Fine[i] += max(0, ((a[i][k] + s[i][k]) - factory.l[i]))
    return Fine


# разворачиваем решение
def RightOrder(x):
    sequenceX2 = GettingTheSequence(x)
    for k in range(len(sequenceX2)):
        buf = [0]
        for j in range(len(sequenceX2[k])):
            minimum = 9999999999
            for i in range(len(sequenceX2[k])):
                if sequenceX2[k][i] != 0 and minimum > sequenceX2[k][i]:
                    minimum = sequenceX2[k][i]

            if minimum != 9999999999:
                buf.append(minimum)
                sequenceX2[k].remove(minimum)
        buf.append(0)
        sequenceX2[k] = buf

    sequenceX1 = [0]
    for k in range(len(x[0][0])):
        for i in range(len(sequenceX2[k])):
            # случай когда находишься на цифре и следующая цифра
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] != 0:
                sequenceX1.append(sequenceX2[k][i])
            # случай когда находишься на цифре и следующий ноль
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] == 0:
                sequenceX1.append(sequenceX2[k][i])
            # случай когда находишься на нуле и предыдущая цифра
            if sequenceX2[k][i - 1] != 0 and sequenceX2[k][i] == 0:
                sequenceX1.append(sequenceX2[k][i])

    sequenceX1 = AddOneCell(sequenceX1)
    return sequenceX1


# Граничные условия
def X_join_Y(x, y, file='def'):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(len(y[0])):
        for j in range(factory.N):
            for i in range(factory.N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                if file != 'def':
                    file.write(
                        "   ERROR from X_join_Y: сломалось первое ограничение, несовместность переменных х, у" + '\n')
                else:
                    print("ERROR from X_join_Y: сломалось первое ограничение, несовместность переменных х, у")
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s, file='def'):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, factory.N):
        if i != 0:
            for k in range(len(s[i])):
                bufer1 += s[i][k]
            if int(bufer1) != factory.S[i]:
                if file != 'def':
                    file.write(
                        "   ERROR from V_jobs: сломалось второе ограничение, общий объем работ на объекте " + str(i) +
                        " не совпадает с регламентом" + '\n')
                else:
                    print("ERROR from V_jobs: сломалось второе ограничение, общий объем работ на объекте" + str(i) +
                          "не совпадает с регламентом")
                return 0
            bufer1 = 0
    return 1


def TC_equal_KA(y, file='def'):
    bufer1 = 0
    # Add constraint: sum (y[i][k])<=ka[i]
    for i in range(1, factory.N):
        if i != 0:
            for k in range(len(y[i])):
                bufer1 += y[i][k]
            if bufer1 > factory.wells[i]:
                if file != 'def':
                    file.write("    ERROR from TC_equal_KA: сломалось третье ограничение, кол-во ТС на одном объекте" +
                               str(i) + "больше чем число скважин" + '\n')
                else:
                    print("ERROR from TC_equal_KA: сломалось третье ограничение, кол-во ТС на одном объекте" + str(i) +
                          "больше чем число скважин")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y, file='def'):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, factory.N):
        for k in range(len(y[i])):
            if s[i][k] > factory.S[i] * y[i][k]:

                if file != 'def':
                    file.write(
                        "   ERROR from ban_driling: сломалось четвертое ограничение, ТС не приехало на объект" + str(i) +
                        ", но начало бурение" + '\n')
                else:
                    print("ERROR from ban_driling: сломалось четвертое ограничение, ТС не приехало на объект" + str(i) +
                          ", но начало бурение")
                return 0
    return 1


def window_time_down(a, y, file='def'):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, factory.N):
        for k in range(len(y[i])):
            if factory.e[i] > a[i][k] and y[i][k] == 1:
                if file != 'def':
                    file.write("    ERROR from window_time_down: сломалось пятое ограничение, время приезда на объкект" +
                               str(i) + "меньше чем начало работ" + '\n')
                else:
                    print("ERROR from window_time_down: сломалось пятое ограничение, время приезда на объкект", i,
                          "меньше чем начало работ")
                return 0
    return 1


def window_time_up(a, s, y, file='def'):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, factory.N):
        for k in range(len(y[i])):
            if a[i][k] + s[i][k] > factory.l[i] and y[i][k] == 1:
                if file != 'def':
                    file.write("    ERROR from window_time_up: сломалось шестое ограничение, "
                               "время окончание работ на объкект" + str(i) + "больше чем конец работ" + '\n')
                else:
                    print(" ERROR from window_time_up: сломалось шестое ограничение, время окончание работ на объкект",
                          i,
                          "больше чем конец работ")
                return 0
    return 1


def ban_cycle(a, x, s, y, file='def'):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1.txt-x[i][j][k])
    for i in range(1, factory.N):
        for j in range(1, factory.N):
            for k in range(len(a[0])):
                if a[i][k] - a[j][k] + x[i][j][k] * factory.t[i][j] + s[i][k] > factory.l[i] * (1 - x[i][j][k]) and \
                        y[i][k] == 1:
                    if file != 'def':
                        file.write("    ERROR from ban_cycle: сломалось седьмое ограничение, машина" + str(k) +
                                   "не посещает депо согласно временным рамкам" + '\n')
                    else:
                        print("ERROR from ban_cycle: сломалось седьмое ограничение, машина", k,
                              "не посещает депо согласно временным рамкам")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s, file='def'):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(len(y[i])):
                if s[i][k] < 0 or a[i][k] < 0:
                    if file != 'def':
                        file.write("    ERROR from positive_a_and_s: сломалось седьмое ограничение, "
                                   "неправельные значение переменных a, s" + '\n')
                    else:
                        print(
                            "ERROR from positive_a_and_s: сломалось седьмое ограничение, "
                            "неправельные значение переменных a, s")
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    print("ERROR from positive_a_and_s: сломалось седьмое ограничение, "
                          "неправельное значение переменной x")
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    print("ERROR from positive_a_and_s: сломалось седьмое ограничение, "
                          "неправельное значение переменной y")
                    return 0
    return 1


# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a, pinalty="false", file='def'):
    # по дефолту смотрим все огр, но если тру то не рассматриваем огр на своевременный конец работ
    if pinalty == "false":
        result = X_join_Y(x, y, file) * V_jobs(s, file) * TC_equal_KA(y, file) * ban_driling(s, y, file) * \
                 window_time_down(a, y, file) * window_time_up(a, s, y, file) * \
                 ban_cycle(a, x, s, y, file) * positive_a_and_s(x, y, a, s, file)
    elif pinalty == "true":
        result = X_join_Y(x, y, file) * V_jobs(s, file) * TC_equal_KA(y, file) * ban_driling(s, y, file) * \
                 window_time_down(a, y, file) * \
                 positive_a_and_s(x, y, a, s, file)
    else:
        print("ERROR from VerificationOfBoundaryConditions: неверное значение, переменной pinalty")
        return -1
    if result == 1:
        return 1  # good
    else:
        return 0
