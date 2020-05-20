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
    file = 0
    if cros == 'HGreX':
        if os.path.getsize("log/hgrexlog.txt") <= 700 * 1000000:
            file = open("log/hgrexlog.txt", 'a')
        else:
            if os.path.getsize("log/hgrexlog1.txt") <= 700 * 1000000:
                file = open("log/hgrexlog1.txt", 'a')
            else:
                file = open("log/hgrexlog2.txt", 'a')

    elif cros == 'HRndX':
        if os.path.getsize("log/hrndxlog.txt") <= 700 * 1000000:
            file = open("log/hrndxlog.txt", 'a')
        else:
            if os.path.getsize("log/hrndxlog1.txt") <= 700 * 1000000:
                file = open("log/hrndxlog1.txt", 'a')
            else:
                file = open("log/hrndxlog2.txt", 'a')

    elif cros == 'HProX':
        if os.path.getsize("log/hproxlog.txt") <= 700 * 1000000:
            file = open("log/hproxlog.txt", 'a')
        else:
            if os.path.getsize("log/hproxlog1.txt") <= 700 * 1000000:
                file = open("log/hproxlog1.txt", 'a')
            else:
                file = open("log/hproxlog2.txt", 'a')

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
            file.write("Вернулись в ноль, нужно перейти на новую машину или завершить скрещивание\n")
            car += 1
            numberInCar = 0
            for i in range(factory.N):
                flag[i] = 0

            if car < factory.K or sum(flagAll) < factory.N:
                first = SelectFirstObj(sequence1, sequence2, flagAll, countOfRaces, file)
                if first:
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
                else:
                    break

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
