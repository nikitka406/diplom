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
print("Проверка стартового решения пройдена")

# Освобождаем машины если позволяют гран усл
DeleteCarNonNarushOgr(x, y, s, a)

# Удаляем не используемые ТС
# x, y, s, a = DeleteNotUsedCar(x, y, s, a)

# Проверяем что ничего не сломалось
target_function = CalculationOfObjectiveFunction(x, y, PenaltyFunction(s, a))
assert VerificationOfBoundaryConditions(x, y, s, a, "true") == 1
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

min_result = min(Target_Function)
number_solution = Target_Function.count(min(Target_Function))
print("Минимальная целевая функция ", min_result, " номер решения ", number_solution)
Time = time.time() - start
print(Time, "seconds")

SaveDateResult(min_result, Time, Sequence[number_solution])
#
# for i in  range(factory.param_population):
#     result = CheckSequence(Sequence[i])
#     if result != 1:
#         print("Последовательность строится не верно")
#         print(Sequence[i])
# AEX(Sequence[0], Sequence[1])
