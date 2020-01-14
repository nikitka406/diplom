from function import *
from math import sqrt
target_function = 0 # значение целевой функции

X = [0,-27,21,50,31,-25,31,-43,-35,-14]#координаты по ОХ
Y = [0,-44,38,42,30,39,15,-23,28,20]#координаты по ОУ

d = [[0 for j in range(N)] for i in range(N)]  # расстояния между городами
for i in range(N):
    for j in range(N):
        d[i][j] = sqrt(pow((X[i] - X[j]), 2) + pow((Y[i] - Y[j]), 2))

t = d  # время перемещения между городами
for i in range(N):
    for j in range(N):
        t[i][j] = round(t[i][j])

wells = [0,1,2,1,3,1,1,1,5,1]  # число скважин на i объекте

S = [0 for j in range(N)] # число рабочих дней для одного ТС для выполнения всех работ на i объекте
for i in range(N):
    S[i] = wells[i] * 2

KA = 0 # кол-во ТС = кол-ву скважин
for i in range(N):
    KA += wells[i]

e = [0,7,4,8,9,7,8,3,9,8]  # начало работы на i объекте
l = [0 for j in range(N)]  # конец работы на i объекте
for i in range(N):
    l[i] = e[i] + S[i]

# заполняем стартовое решение, одна машина на одну локацию
x, y, s, a = OneCarOneLocation(KA, S, t, wells, e)
target_function = CalculationOfObjectiveFunction(d, x, KA)
# print(target_function)
# print(VerificationOfBoundaryConditions(x, y, s, a, wells, S, e, l, t, KA))

