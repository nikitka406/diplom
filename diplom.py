from function import *
import factory
from crossover import *
import time
start = time.time()


ClearAllFile()
target_function = 0  # значение целевой функции
# TODO надо разобраться почему время в А выставляется не правильно

# заполняем стартовое решение, одна машина на одну локацию
x, y, s, a = OneCarOneLocation()
target_function = CalculationOfObjectiveFunction(x, y)
print(target_function)
assert VerificationOfBoundaryConditions(x, y, s, a) == 1

# Освобождаем машины если позволяют гран усл
DeleteCarNonNarushOgr(x, y, s, a)

# Удаляем не используемые ТС
# x, y, s, a = DeleteNotUsedCar(x, y, s, a)

# Проверяем что ничего не сломалось
target_function = CalculationOfObjectiveFunction(x, y)
assert VerificationOfBoundaryConditions(x, y, s, a) == 1
print(target_function)

# Сохраняем стартовое решение в файл
SaveStartSolution(x, y, s, a)

# Создаем хранилище решений, для популяции решений
X, Y, Sresh, A, Target_Function = SolutionStore()

# Cоздаем популяцию решений
PopulationOfSolutions(Target_Function, x, y, s, a)

# Считываем популяцию из файла
ReadSolutionPopulationOnFile(X, Y, Sresh, A)

# Создаем последовательность решения
Sequence = CreateSequence(X)

# Создаем новые решения
GetNewSolution(Sequence, X, Y, Sresh, A, Target_Function)

print("Минимальная целевая функция ", min(Target_Function), " номер решения ", Target_Function.count(min(Target_Function)))
print(time.time() - start, "seconds")


#
# for i in  range(factory.param_population):
#     result = CheckSequence(Sequence[i])
#     if result != 1:
#         print("Последовательность строится не верно")
#         print(Sequence[i])
# AEX(Sequence[0], Sequence[1])
