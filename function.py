#Распределяем на каждую локацию по машине
def OneCarOneLocation(N, S, t):
    # копия переменной задачи Х, только кол-вo машин = число локаций
    x = [[[0 for k in range(N)] for j in range(N)] for i in range(N)]
    y = [[0 for k in range(N)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(N):
        y[0][k] = 1
    s = [[0 for k in range(N)] for i in range(N)]  # время работы ТС номером К на объекте i
    a = [[0 for k in range(N)] for i in range(N)]  # время прибытия ТС с номером К на объект i

    for j in range(1, N):
        x[0][j][j] = 1
        y[j][j] = 1
        s[j][j] = S[j]
        a[j][j] = t[0][j]
    return x, y, s, a

# def RouteReduction():
