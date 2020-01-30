import factory
from function import *
import factory
target_function = 0 # значение целевой функции

# заполняем стартовое решение, одна машина на одну локацию
x, y, s, a = OneCarOneLocation()
target_function = CalculationOfObjectiveFunction(x, y)
print(target_function)
assert VerificationOfBoundaryConditions(x, y, s, a) == 1

DeleteCarNonNarushOgr(x, y, s, a)
x, y, s, a = DeleteNotUsedCar(x, y, s, a)
target_function = CalculationOfObjectiveFunction(x, y)
assert VerificationOfBoundaryConditions(x, y, s, a) == 1
print(target_function)
# CombiningRoutesLessFine(x, y, s, a, KA)

#
# #Хранилище решений, первый индекс это номер решения, со второго начинается само решение
# X = [[0 for m in range(2)] for n in range(1000)]# едет или нет ТС с номером К из города I в J
# for n in range(1000):
#     X[n][0] = n
#     X[n][1] = [[[0 for k in range(KA)] for j in range(N)] for i in range(N)]
#
# Y = [[0 for m in range(2)] for n in range(1000)]  # посещает или нет ТС с номером К объект i
# for n in range(1000):
#     Y[n][0] = n
#     Y[n][1] = [[0 for k in range(KA)] for i in range(N)]
#
# Sresh = [[0 for m in range(2)] for n in range(1000)] # время работы ТС c номером К на объекте i
# for n in range(1000):
#     Sresh[n][0] = n
#     Sresh[n][1] = [[0 for k in range(KA)] for i in range(N)]
#
# A = [[0 for m in range(2)] for n in range(1000)]# время прибытия ТС с номером К на объект i
# for n in range(1000):
#     A[n][0] = n
#     A[n][1] = [[0 for k in range(KA)] for i in range(N)]