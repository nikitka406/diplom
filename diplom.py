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
Target_Function = [0 for n in
                   range(factory.param_population)]  # здесь сохраняем результат целевой функции для каждого решения
# X, Y, Sresh, A, Target_Function = SolutionStore()

# Cоздаем популяцию решений
PopulationOfSolutions(Target_Function, x, y, s, a)

# Создаем последовательность решения
# Sequence = CreateSequence(y)

# Создаем новые решения
GetNewSolution(Target_Function)

min_result = min(Target_Function)
number_solution = Target_Function.count(min(Target_Function))
print("Минимальная целевая функция ", min_result, " номер решения ", number_solution)
Time = time.time() - start
print(Time, "seconds")

# X1, Y1, Sresh1, A1 = SolutionStore()
# ReadSolutionPopulationOnFile(X1, Y1, Sresh1, A1, number_solution)
# Sequence1 = CreateSequence(X1)

SaveDateResult(min_result, Time)

