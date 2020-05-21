from crossover import *


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
        scenario_cross = ['randomAndRandom', 'BestAndRand']
        scenario = random.choice(scenario_cross)
        scenario = 'BestAndRand'
        file.write("Выбрали сценарий по выбору родителей " + str(scenario) + '\n')

        # Выбираю как буду сохранять полученное решение
        scenario_add_new_solution = ['deleteTheBad', 'deleteTheBadParents']
        scenario_add = random.choice(scenario_add_new_solution)
        # scenario_add = 'deleteTheBad'
        file.write("Выбрали сценарий по сохранению нового решения " + str(scenario_add) + '\n')

        # TODO Задаю список с названиями операторов
        name_crossover = ['AEX', 'HGreX', 'HRndX', 'HProX']
        crossover = random.choice(name_crossover)
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

        elif scenario == 'BestAndRand':
            file.write("Пошли по сценарию, один рандомный второй самый лучший" + '\n')
            # Индекс первого родителя
            index = random.randint(0, factory.param_population - 1)
            file.write("Номер первого решения " + str(index) + '\n')

            # Ищем самое маленькое решение по целевой функции
            minimum = min(Target_Function)
            # Оно будет вторым родителем
            jndex = Target_Function.index(minimum)
            file.write("Номер второго решения " + str(jndex) + '\n')

            file.write(str(Sequence) + '\n')
            file.write("Первое рандомное решение" + '\n')
            file.write(str(Sequence[index]) + '\n')
            file.write("Второе решение, лучшие из всех" + '\n')
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
    if timeCros[0][1] != 0:
        SaveDateResult("Среднее время работы AEX = " + str(timeCros[0][0] / timeCros[0][1]))
    if timeCros[1][1] != 0:
        SaveDateResult("Среднее время работы HGreX = " + str(timeCros[1][0]/timeCros[1][1]))
    if timeCros[2][1] != 0:
        SaveDateResult("Среднее время работы HRndX = " + str(timeCros[2][0]/timeCros[2][1]))
    if timeCros[3][1] != 0:
        SaveDateResult("Среднее время работы HProX = " + str(timeCros[3][0]/timeCros[3][1]))
    if timeLocal[0][1] != 0:
        SaveDateResult("Среднее время работы Relocate в эволюции = " + str(timeLocal[0][0] / timeLocal[0][1]))
    if timeLocal[1][1] != 0:
        SaveDateResult("Среднее время работы 2-opt в эволюции = " + str(timeLocal[1][0] / timeLocal[1][1]))
    if timeLocal[2][1] != 0:
        SaveDateResult("Среднее время работы Help в эволюции = " + str(timeLocal[2][0] / timeLocal[2][1]))
    if timeLocal[3][1] != 0:
        SaveDateResult("Среднее время работы Exchange в эволюции = " + str(timeLocal[3][0] / timeLocal[3][1]))

    min_result = min(Target_Function)
    number_solution = Target_Function.index(min_result)
    file.write("Минимальная целевая функция " + str(min_result) + " номер решения " + str(number_solution) + '\n')
    print("Минимальная целевая функция " + str(min_result) + " номер решения " + str(number_solution) + '\n')

    SaveDateResult("Итоговая минимальная целевая функция без штрафом = " + str(CalculationOfObjectiveFunction(X[number_solution], 0)))
    SaveDateResult("Итоговая минимальная целевая функция со штрафом = " + str(min_result))
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
