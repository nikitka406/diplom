########################### Входные значения
N = 10  # число объектов
K = 5  # набор всех ТС
car_cost = 1000 # цена за арнеду машины


# подсчет значения целевой функции
def CalculationOfObjectiveFunction(d, x, KA, target_function = 0):
    for k in range(KA):
        for i in range(N):
            for j in range(N):
                target_function += d[i][j]*x[i][j][k]
    target_function += (KA-K) * car_cost
    return target_function

# Распределяем на каждую локацию по машине
def OneCarOneLocation(KA, S, t, wells, e):
    # копия переменной задачи Х, только кол-вo машин = число локаций
    x = [[[0 for k in range(KA)] for j in range(N)] for i in range(N)] # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(KA)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(KA):
        y[0][k] = 1
    s = [[0 for k in range(KA)] for i in range(N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(KA)] for i in range(N)]  # время прибытия ТС с номером К на объект i


    #поочереди отправляем ТС на локации, по одному на скважину
    k = 0
    for j in range(1, N):
        if wells[j] >= 1:
            for i in range(wells[j]):
                x[0][j][k] = 1 # туда
                x[j][0][k] = 1 # обратно
                y[j][k] = 1
                if wells[j] > 1:
                    s[j][k] = S[j] / wells[j]
                else:
                    s[j][k] = S[j]
                if e[j] > t[0][j] / 24:
                    a[j][k] = e[j]
                else:
                    a[j][k] = t[0][j] / 24
                print(a[j][k], end=' ')
                k += 1
            print("\n")
    return x, y, s, a

# def RouteReduction():


# for k in range(KA):
#     print(k)
#     for i in range(N):
#         for j in range(N):
#             print(x[i][j][k], end = ' ')
#         print("\n")
# for i  in range(N):
#     for k in range (KA):
#         print(a[i][k], end=' ')
#     print('\n')
#
# for i  in range(N):
#     print(t[0][i], end=' ')
# print('\n')


# Граничные условия
def X_join_Y(x, y, KA):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(KA):
        for j in range(N):
            for i in range(N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                print("1")
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s, S, KA):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, N):
        if i != 0:
            for k in range(KA):
                bufer1 += s[i][k]
            if bufer1 != S[i]:
                print("2")
                return 0
            bufer1 = 0
    return 1


def TC_equal_KA(ka, y, KA):
    bufer1 =0
    # Add constraint: sum (y[i][k])<=ka[i]
    for i in range(1, N):
        if i != 0:
            for k in range(KA):
                bufer1 += y[i][k]
            if bufer1 > ka[i]:
                print("3")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, S, y, KA):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, N):
        for k in range(KA):
            if s[i][k] > S[i] * y[i][k]:
                print("4")
                return 0
    return 1


def window_time_down(a, e, KA):
    # Add constraint: e[i]<=a[i][k]
    for i in range(N):
        for k in range(KA):
            if e[i] > a[i][k]:
                print("5")
                return 0
    return 1


def window_time_up(a, s, l, KA):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, N):
        for k in range(KA):
            if a[i][k] + s[i][k] > l[i]:
                print("6")
                return 0
    return 1


def ban_cycle(a, x, t, s, l, KA):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, N):
        for j in range(1, N):
            for k in range(KA):
                if a[i][k] - a[j][k] + x[i][j][k] * t[i][j] + s[i][k] > l[i] * (1 - x[i][j][k]):
                    print("7")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s, KA):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(N):
        for j in range(N):
            for k in range(KA):
                if s[i][k] < 0 or a[i][k] < 0:
                    print("8")
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    return 0
    return 1

# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a, wells, S, e, l, t, KA):
    result = X_join_Y(x, y, KA) * V_jobs(s, S, KA) * TC_equal_KA(wells, y, KA) * ban_driling(s, S, y, KA) * window_time_down(a, e, KA) * \
             window_time_up(a, s, l, KA) * ban_cycle(a, x, t, s, l, KA) * positive_a_and_s(x, y, a, s, KA)
    if result == 1:
        return 1
    else:
        return 0
