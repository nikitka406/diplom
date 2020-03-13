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

#Удаляем не используемые ТС
x, y, s, a = DeleteNotUsedCar(x, y, s, a)

# BeautifulPrint(x, y, s, a)
#Проверяем что ничего не сломалось
target_function = CalculationOfObjectiveFunction(x, y)
assert VerificationOfBoundaryConditions(x, y, s, a) == 1
print(target_function)

#Создаем хранилище решений, для популяции решений
X, Y, Sresh, A, Target_Function, bufer = SolutionStore()

#Cоздаем популяцию решений
#TODO сохранять кол-во машин для каждого решения
PopulationOfSolutions(X, Y, Sresh, A, Target_Function, x, y, s, a)

#Интерпритируем матрицу Х на двумерный массив
sequenceX2 = GettingTheSequence(X[4])
sequenceX1 = TransferX2toX1(sequenceX2)

for k in range(factory.KA):
    for i in range(factory.N):
        print(sequenceX2[k][i], end=' ')
    print("\n")
print("\n")
print(sequenceX1)
