import factory


# Сохраняем решение в файл
def SaveDateResult(date1):
    file = open('log/Result.txt', 'a')
    file.write(date1 + '\n')
    file.close()


# Сохраняем стартовое решение в файл
# Заебись работает!!!
def SaveStartSolution(local_x, local_y, local_s, local_a):
    file = open('output/StartSolution.txt', 'w')

    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(len(local_y[0])):
                file.write(str(local_x[i][j][k]) + ' ')
            file.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(factory.N):
        for k in range(len(local_y[0])):
            file.write(str(local_y[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл S
    for i in range(factory.N):
        for k in range(len(local_y[0])):
            file.write(str(local_s[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл A
    for i in range(factory.N):
        for k in range(len(local_y[0])):
            file.write(str(local_a[i][k]) + ' ')
        file.write("\n")

    file.close()


# Cчитываем стартовое решение в файл
# Заебись работает!!!
def ReadStartSolutionOfFile(sizeK):
    local_x = [[[0 for k in range(sizeK)] for j in range(factory.N)] for i in
               range(factory.N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(sizeK)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(factory.KA):
        local_y[0][k] = 1
    local_s = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    file = open('output/StartSolution.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            # for k in range(factory.KA):
            local_x[i][j] = line[index].split()
            for k in range(len(local_x[i][j])):
                local_x[i][j][k] = int(local_x[i][j][k])
            index += 1

    # Печатаем в файл Y
    for i in range(factory.N):
        local_y[i] = line[index].split()
        for k in range(len(local_y[i])):
            local_y[i][k] = int(local_y[i][k])
        index += 1
    # Печатаем в файл S
    for i in range(factory.N):
        local_s[i] = line[index].split()
        for k in range(len(local_s[i])):
            local_s[i][k] = float(local_s[i][k])
        index += 1
    # Печатаем в файл A
    for i in range(factory.N):
        local_a[i] = line[index].split()
        for k in range(len(local_a[i])):
            local_a[i][k] = float(local_a[i][k])
        index += 1
    file.close()
    return local_x, local_y, local_s, local_a


# Cохраняем промежуточное решение в релоке
def SaveStartLocalSearch(local_x, local_y, local_s, local_a, sizeK):
    file = open('output/StartLocalSearch.txt', 'w')

    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(sizeK):
                file.write(str(local_x[i][j][k]) + ' ')
            file.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(factory.N):
        for k in range(sizeK):
            file.write(str(local_y[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл S
    for i in range(factory.N):
        for k in range(sizeK):
            file.write(str(local_s[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл A
    for i in range(factory.N):
        for k in range(sizeK):
            file.write(str(local_a[i][k]) + ' ')
        file.write("\n")

    file.close()


def ReadStartLocalSearchOfFile(sizeK):
    local_x = [[[0 for k in range(sizeK)] for j in range(factory.N)] for i in
               range(factory.N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(sizeK)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(sizeK):
        local_y[0][k] = 1
    local_s = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    file = open('output/StartLocalSearch.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            # for k in range(factory.KA):
            local_x[i][j] = line[index].split()
            for k in range(len(local_x[i][j])):
                local_x[i][j][k] = int(local_x[i][j][k])
            index += 1

    # Печатаем в файл Y
    for i in range(factory.N):
        local_y[i] = line[index].split()
        for k in range(len(local_y[i])):
            local_y[i][k] = int(local_y[i][k])
        index += 1
    # Печатаем в файл S
    for i in range(factory.N):
        local_s[i] = line[index].split()
        for k in range(len(local_s[i])):
            local_s[i][k] = float(local_s[i][k])
        index += 1
    # Печатаем в файл A
    for i in range(factory.N):
        local_a[i] = line[index].split()
        for k in range(len(local_a[i])):
            local_a[i][k] = float(local_a[i][k])
        index += 1
    file.close()
    return local_x, local_y, local_s, local_a


# Cохраняем промежуточное решение в релоке
def SaveLocalSearch(local_x, local_y, local_s, local_a, sizeK):
    file = open('output/LocalSearch.txt', 'w')

    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(sizeK):
                file.write(str(local_x[i][j][k]) + ' ')
            file.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(factory.N):
        for k in range(sizeK):
            file.write(str(local_y[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл S
    for i in range(factory.N):
        for k in range(sizeK):
            file.write(str(local_s[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл A
    for i in range(factory.N):
        for k in range(sizeK):
            file.write(str(local_a[i][k]) + ' ')
        file.write("\n")

    file.close()


def ReadLocalSearchOfFile(sizeK):
    local_x = [[[0 for k in range(sizeK)] for j in range(factory.N)] for i in
               range(factory.N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(sizeK)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(sizeK):
        local_y[0][k] = 1
    local_s = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    file = open('output/LocalSearch.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            # for k in range(factory.KA):
            local_x[i][j] = line[index].split()
            for k in range(len(local_x[i][j])):
                local_x[i][j][k] = int(local_x[i][j][k])
            index += 1

    # Печатаем в файл Y
    for i in range(factory.N):
        local_y[i] = line[index].split()
        for k in range(len(local_y[i])):
            local_y[i][k] = int(local_y[i][k])
        index += 1
    # Печатаем в файл S
    for i in range(factory.N):
        local_s[i] = line[index].split()
        for k in range(len(local_s[i])):
            local_s[i][k] = float(local_s[i][k])
        index += 1
    # Печатаем в файл A
    for i in range(factory.N):
        local_a[i] = line[index].split()
        for k in range(len(local_a[i])):
            local_a[i][k] = float(local_a[i][k])
        index += 1
    file.close()
    return local_x, local_y, local_s, local_a


# Cохраняем промежуточное решение в хелпе
def SaveHelp(local_x, local_y, local_s, local_a, sizeK):
    file1 = open('output/Help.txt', 'w')

    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(sizeK):
                file1.write(str(local_x[i][j][k]) + ' ')
            file1.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(factory.N):
        for k in range(sizeK):
            file1.write(str(local_y[i][k]) + ' ')
        file1.write("\n")
    # Печатаем в файл S
    for i in range(factory.N):
        for k in range(sizeK):
            file1.write(str(local_s[i][k]) + ' ')
        file1.write("\n")
    # Печатаем в файл A
    for i in range(factory.N):
        for k in range(sizeK):
            file1.write(str(local_a[i][k]) + ' ')
        file1.write("\n")

    file1.close()


def ReadHelpOfFile(sizeK):
    local_x = [[[0 for k in range(sizeK)] for j in range(factory.N)] for i in
               range(factory.N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(sizeK)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(sizeK):
        local_y[0][k] = 1
    local_s = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    file = open('output/Help.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()
    # print(line)

    index = 0
    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            # for k in range(factory.KA):
            local_x[i][j] = line[index].split()
            for k in range(sizeK):
                local_x[i][j][k] = int(local_x[i][j][k])
            index += 1
            # print(index)

    # Печатаем в файл Y
    for i in range(factory.N):
        local_y[i] = line[index].split()
        for k in range(sizeK):
            local_y[i][k] = int(local_y[i][k])
        index += 1
    # Печатаем в файл S
    for i in range(factory.N):
        local_s[i] = line[index].split()
        for k in range(sizeK):
            local_s[i][k] = float(local_s[i][k])
        index += 1
    # Печатаем в файл A
    for i in range(factory.N):
        local_a[i] = line[index].split()
        for k in range(sizeK):
            local_a[i][k] = float(local_a[i][k])
        index += 1
    file.close()
    return local_x, local_y, local_s, local_a


# Cохраняем стартовое решение в хелпе
def SaveStartHelp(local_x, local_y, local_s, local_a, sizeK):
    file = open('output/StartHelp.txt', 'w')

    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(len(local_y[0])):
                file.write(str(local_x[i][j][k]) + ' ')
            file.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(factory.N):
        for k in range(len(local_y[0])):
            file.write(str(local_y[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл S
    for i in range(factory.N):
        for k in range(len(local_y[0])):
            file.write(str(local_s[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл A
    for i in range(factory.N):
        for k in range(len(local_y[0])):
            file.write(str(local_a[i][k]) + ' ')
        file.write("\n")

    file.close()


def ReadStartHelpOfFile(sizeK):
    local_x = [[[0 for k in range(sizeK)] for j in range(factory.N)] for i in
               range(factory.N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(sizeK)] for i in range(factory.N)]  # посещает или нет ТС с номером К объект i
    for k in range(sizeK):
        local_y[0][k] = 1
    local_s = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(sizeK)] for i in range(factory.N)]  # время прибытия ТС с номером К на объект i

    file = open('output/StartHelp.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            # for k in range(factory.KA):
            local_x[i][j] = line[index].split()
            for k in range(len(local_x[i][j])):
                local_x[i][j][k] = int(local_x[i][j][k])
            index += 1

    # Печатаем в файл Y
    for i in range(factory.N):
        local_y[i] = line[index].split()
        for k in range(len(local_y[i])):
            local_y[i][k] = int(local_y[i][k])
        index += 1
    # Печатаем в файл S
    for i in range(factory.N):
        local_s[i] = line[index].split()
        for k in range(len(local_s[i])):
            local_s[i][k] = float(local_s[i][k])
        index += 1
    # Печатаем в файл A
    for i in range(factory.N):
        local_a[i] = line[index].split()
        for k in range(len(local_a[i])):
            local_a[i][k] = float(local_a[i][k])
        index += 1
    file.close()
    return local_x, local_y, local_s, local_a


# Сохраняем популяцию, добавляя новое решение в конец
def SavePopulation(lokal_X, lokal_Y, lokal_Sresh, lokal_A):
    file = open('output/SolutionPopulation.txt', 'a')

    # Печатаем в файл Х
    for i in range(factory.N):
        for j in range(factory.N):
            for k in range(len(lokal_Y[0])):
                file.write(str(lokal_X[i][j][k]) + ' ')
            file.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(factory.N):
        for k in range(len(lokal_Y[0])):
            file.write(str(lokal_Y[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл S
    for i in range(factory.N):
        for k in range(len(lokal_Y[0])):
            file.write(str(lokal_Sresh[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл A
    for i in range(factory.N):
        for k in range(len(lokal_Y[0])):
            file.write(str(lokal_A[i][k]) + ' ')
        file.write("\n")

    file.close()


# Считываем популяцию
def ReadSolutionPopulationOnFile(local_x, local_y, local_s, local_a):
    file = open('output/SolutionPopulation.txt', 'r')
    print("Считываем популяцию из файла output/SolutionPopulation.txt")
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    for n in range(factory.param_population):
        # Печатаем в файл Х
        for i in range(factory.N):
            for j in range(factory.N):
                # for k in range(factory.KA):
                local_x[n][i][j] = line[index].split()
                for k in range(len(local_x[n][i][j])):
                    local_x[n][i][j][k] = int(local_x[n][i][j][k])
                index += 1

        # Печатаем в файл Y
        for i in range(factory.N):
            local_y[n][i] = line[index].split()
            for k in range(len(local_y[n][i])):
                local_y[n][i][k] = int(local_y[n][i][k])
            index += 1

        # Печатаем в файл S
        for i in range(factory.N):
            local_s[n][i] = line[index].split()
            for k in range(len(local_s[n][i])):
                local_s[n][i][k] = float(local_s[n][i][k])
            index += 1
        # Печатаем в файл A
        for i in range(factory.N):
            local_a[n][i] = line[index].split()
            for k in range(len(local_a[n][i])):
                local_a[n][i][k] = float(local_a[n][i][k])
            index += 1
    file.close()


# Отчищаем файл
def ClearAllFile():
    file = open('log/aexlog.txt', 'w')
    file.close()
    file = open('log/exchlog.txt', 'w')
    file.close()
    file = open("log/genalog.txt", 'w')
    file.close()
    file = open('log/helog.txt', 'w')
    file.close()
    file = open('log/relog.txt', 'w')
    file.close()
    file = open('log/Two_Opt.txt', 'w')
    file.close()
    file = open('log/twooptlog.txt', 'w')
    file.close()
    file = open('output/Help.txt', 'w')
    file.close()
    file = open('output/LocalSearch.txt', 'w')
    file.close()
    file = open('output/population.txt', 'w')
    file.close()
    file = open('output/Relocate.txt', 'w')
    file.close()
    file = open('output/SolutionPopulation.txt', 'w')
    file.close()
    file = open('output/StartHelp.txt', 'w')
    file.close()
    file = open('output/StartLocalSearch.txt', 'w')
    file.close()
    file = open('output/StartSolution.txt', 'w')
    file.close()
