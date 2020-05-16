from forCross import *
from operators import *


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
        # children[1][0] = sequence1[1][0]

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
    return children, timeCros


# кроссовер HGreX
def HGreXOrHRndXOrHProX(sequence1, sequence2, timeCros, cros):
    if cros == 'HGreX':
        file = open("log/hgrexlog.txt", 'a')
    elif cros == 'HRndX':
        file = open("log/hrndxlog.txt", 'a')
    elif cros == 'HProX':
        file = open("log/hproxlog.txt", 'a')

    start = time.time()
    timeCros[1] += 1

    file.write("HGreX start: ->" + '\n')
    print("Скрещивание решений осуществляется с помощью оператора HGreX" + '\n')

    children = [[0, 0]]
    # число клиентов в текущей машине
    numberInCar = 0
    # число используемых машин
    car = 0
    # флаг, для посещенных городов в одном маршруте(одной машиной)
    flag = [0 for i in range(factory.N)]
    flag[0] = -1
    # флаг, для посещенных городов в заключительном решении
    flagAll = [0 for i in range(factory.N)]
    flagAll[0] = 1

    # сколько раз можно заехать к каждому
    countOfRaces = factory.wells.copy()

    first = SelectFirstObj(sequence1, sequence2, flagAll, countOfRaces, file)
    file.write("Выбираем случайную вершину = " + str(first) + '\n')

    file.write("Расставляем флаги" + '\n')
    flagAll[first] = 1
    flag[first] = 1
    countOfRaces[first] -= 1
    file.write("flag = " + str(flag) + '\n')
    file.write("flagAll = " + str(flagAll) + '\n')
    file.write("Число свободных скважин на каждом объекте " + str(countOfRaces) + '\n')

    file.write("Добавили первое ребро в ребенка, " + '\n')
    children.append([first, 0])
    numberInCar += 1
    file.write("Ребенок сейчас выглядит во так " + str(children) + '\n')

    scnd = first
    while car < factory.K or sum(flagAll) < factory.N or children[-1] != [0, 0]:
        file.write("\n")
        if cros == 'HGreX':
            scnd = GetShortArc(sequence1, sequence2, scnd, flag, numberInCar, countOfRaces, file)
        elif cros == 'HRndX':
            scnd = GetArcHRndX(sequence1, sequence2, scnd, flag, numberInCar, countOfRaces, file)
        elif cros == 'HProX':
            scnd = GetArcHProX(sequence1, sequence2, scnd, flag, numberInCar, countOfRaces, file)

        file.write("Добавляем следующие ребро " + str(scnd) + "\n")
        children.append([scnd, 0])
        file.write("Ребенок сейчас выглядит во так " + str(children) + "\n")

        flagAll[scnd] = 1
        file.write("flagAll сейчас выглядит во так " + str(flagAll) + "\n")

        flag[scnd] += 1
        file.write("flag сейчас выглядит во так " + str(flag) + "\n")

        if scnd != 0:
            numberInCar += 1
            file.write("Кол-во объектов в текущей машине " + str(numberInCar) + "\n")

            countOfRaces[scnd] -= 1
            file.write("Число свободных скважин на каждом объекте " + str(countOfRaces) + '\n')

        if scnd == 0:
            file.write("Вернулись в ноль, нужно перейти на новую машину\n")
            car += 1
            numberInCar = 0
            for i in range(factory.N):
                flag[i] = 0

            if car < factory.K or sum(flagAll) < factory.N:
                first = SelectFirstObj(sequence1, sequence2, flagAll, countOfRaces, file)
                file.write("Выбираем случайную вершину = " + str(first) + '\n')

                file.write("Расставляем флаги" + '\n')
                flagAll[first] = 1
                flag[first] += 1
                countOfRaces[first] -= 1
                file.write("flag = " + str(flag) + '\n')
                file.write("flagAll = " + str(flagAll) + '\n')
                file.write("Число свободных скважин на каждом объекте " + str(countOfRaces) + '\n')

                file.write("Добавили первое ребро в ребенка, " + '\n')
                children.append([first, 0])
                numberInCar += 1
                file.write("Ребенок сейчас выглядит во так " + str(children) + '\n')
                scnd = first

    Time = time.time() - start
    timeCros[0] += Time
    file.write("Время работы HGreX = " + str(Time) + 'seconds\n')

    file.write("<-HGreX stop" + '\n')
    file.close()

    return children, timeCros


# Функция вызывает выбранный оператор
def UsedCrossovers(sequence1, sequence2, operator, timeCros):
    print("Запускаем оператор ", operator)
    if operator == 'AEX':
        children, timeCros[0] = AEX(sequence1, sequence2, timeCros[0])
        return children, timeCros

    elif operator == 'HGreX':
        children, timeCros[1] = HGreXOrHRndXOrHProX(sequence1, sequence2, timeCros[1], operator)
        return children, timeCros

    elif operator == 'HRndX':
        children, timeCros[2] = HGreXOrHRndXOrHProX(sequence1, sequence2, timeCros[2], operator)
        return children, timeCros

    elif operator == 'HProX':
        children, timeCros[2] = HGreXOrHRndXOrHProX(sequence1, sequence2, timeCros[3], operator)
        return children, timeCros

    else:
        print("ERROR from UsedCrossovers: название такого оператора нет")


# Локальный поиск (локально меняем решение)
def LocalSearch(x, y, s, a, target_function, sizeK, iteration, timeLocal):
    print("Применяем локальный поиск (локально меняем решение)")

    # TODO выбираем оператор локального поиска
    local_search_oper = ['relocate', 'Exchange', '2Opt']
    oper = random.choice(local_search_oper)
    # oper = 'Exchange'

    print("Используем оператор ", oper)
    if oper == 'relocate':
        x, y, s, a, target_function, sizeK, timeLocal[0] = Relocate(x, y, s, a, target_function, sizeK, iteration,
                                                                    timeLocal[0], factory.param_local_search/2)
        SaveDateFromGraph(target_function, "Reloc")
        iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal

    elif oper == '2Opt':
        x, y, s, a, target_function, sizeK, timeLocal[1] = Two_Opt(x, y, s, a, target_function, sizeK, iteration,
                                                                   timeLocal[1])
        SaveDateFromGraph(target_function, "2Opt")
        iteration += 1
        return x, y, s, a, target_function, sizeK, iteration, timeLocal

    elif oper == 'Exchange':
        x, y, s, a, target_function, sizeK, timeLocal[3] = Exchange(x, y, s, a, target_function, sizeK, iteration,
                                                                    timeLocal[3], factory.param_local_search/2)
        SaveDateFromGraph(target_function, "Exchange")
        iteration += 1
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
        name_crossover = ['AEX', 'HGreX', 'HRndX']#, 'HProX']
        crossover = random.choice(name_crossover)
        crossover = 'HProX'
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
        SaveDateFromGraph(target_function, "Crossover")

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

        file.write("Help start" + '\n')
        x, y, s, a, target_function, sizek, timeLocal[2] = Help(x, y, s, a, target_function, sizek, iteration - 1,
                                                                timeLocal[2])
        file.write("Целевая функция нового решения после оператора хелп " + str(target_function) + '\n')
        minimumHelp = min(minimumHelp, target_function)
        maximumHelp = max(maximumHelp, target_function)

        # Проверяем что новое решение не хуже самого плохого
        # Ищем самое большое решение по целевой функции
        maximum = max(Target_Function)
        i_max = Target_Function.index(maximum)
        file.write("Самое плохое решение в популяции " + str(maximum) + '\n')

        # Удаляем какое-нибудь решение
        if maximum >= target_function:
            SaveDateFromGraph(target_function, "AfterCrosSearsh")
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
    SaveDateResult("Минимальное значение целевой в поппуляции после локального поиска= " + str(minimumLocal))
    SaveDateResult("Максимальное значение целевой в поппуляции после локального поиска = " + str(maximumLocal))
    SaveDateResult("Минимальное значение целевой в поппуляции после оператора хелп = " + str(minimumHelp))
    SaveDateResult("Максимальное значение целевой в поппуляции после оператора хелп = " + str(maximumHelp))
    SaveDateResult("Число итераций = " + str(iteration))
    # SaveDateResult("Среднее время работы AEX = " + str(timeCros[0][0] / timeCros[0][1]))
    # SaveDateResult("Среднее время работы HGreX = " + str(timeCros[1][0]/timeCros[1][1]))
    # SaveDateResult("Среднее время работы HRndX = " + str(timeCros[2][0]/timeCros[2][1]))
    # SaveDateResult("Среднее время работы HProX = " + str(timeCros[3][0]/timeCros[3][1]))
    # SaveDateResult("Среднее время работы Relocate в эволюции = " + str(timeLocal[0][0] / timeLocal[0][1]))
    # SaveDateResult("Среднее время работы 2-opt в эволюции = " + str(timeLocal[1][0] / timeLocal[1][1]))
    # SaveDateResult("Среднее время работы Help в эволюции = " + str(timeLocal[2][0] / timeLocal[2][1]))
    # SaveDateResult("Среднее время работы Exchange в эволюции = " + str(timeLocal[3][0] / timeLocal[3][1]))

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
