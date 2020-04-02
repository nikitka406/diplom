from function import *
import factory
from crossover import *
target_function = 0 # значение целевой функции
#TODO надо разобраться почему время в А выставляется не правильно

# заполняем стартовое решение, одна машина на одну локацию
x, y, s, a = OneCarOneLocation()
target_function = CalculationOfObjectiveFunction(x, y)
print(target_function)
assert VerificationOfBoundaryConditions(x, y, s, a) == 1

#Убераем маршруты если позволяют гран усл
DeleteCarNonNarushOgr(x, y, s, a)
#TODO делит почему портит стартовое решение
BeautifulPrintInFile(x, y, s, a, 1, 2)
X, Y, Sreh, A = CopyingSolution(x, y, s, a)
#Удаляем не используемые ТС
x, y, s, a = DeleteNotUsedCar(x, y, s, a)
BeautifulPrintInFile(x, y, s, a, 1, 2)
BeautifulPrintInFile(X, Y, Sreh, A, 1, 2)


# # BeautifulPrint(x, y, s, a)
# #Проверяем что ничего не сломалось
# target_function = CalculationOfObjectiveFunction(x, y)
# assert VerificationOfBoundaryConditions(x, y, s, a) == 1
# print(target_function)
#
# #Создаем хранилище решений, для популяции решений
# X, Y, Sresh, A, Target_Function = SolutionStore()
#
# #Cоздаем популяцию решений
# #TODO сохранять кол-во машин для каждого решения
# PopulationOfSolutions(X, Y, Sresh, A, Target_Function, x, y, s, a)




# for n in range(factory.population):
#     BeautifulPrint(X[n], Y[n], Sresh[n], A[n])
# #
# Sequence = CreateSequence(X)
# for k in range(factory.KA):
#     for i in range(factory.N):
#         print(Sequence[0][k][i], end=' ')
#     print("\n")
# print("\n")

