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
def OneCarOneLocation(KA, S, t, wells, d):
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
                x[0][j][k] = 1
                y[j][k] = 1
                if wells[j] > 1:
                    s[j][k] = S[j] / wells[j]
                else:
                    s[j][k] = S[j]
                a[j][k] = t[0][j]
                k += 1
    return x, y, s, a, CalculationOfObjectiveFunction(d, x, KA)

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