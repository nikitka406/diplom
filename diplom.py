from function import *
import factory
from crossover import *
import time

start = time.time()

ClearAllFile()
target_function = 0  # значение целевой функции
iterations = 0

# заполняем стартовое решение, одна машина на одну локацию
x, y, s, a = OneCarOneLocation()
start_target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(s, a))
print(target_function)
assert VerificationOfBoundaryConditions(x, y, s, a) == 1
print("Проверка стартового решения пройдена")

# Освобождаем машины если позволяют гран усл
# TODO проверить делит
DeleteCarNonNarushOgr(x, y, s, a)

# Удаляем не используемые ТС
# x, y, s, a = DeleteNotUsedCar(x, y, s, a)

# Проверяем что ничего не сломалось
target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(s, a))
assert VerificationOfBoundaryConditions(x, y, s, a) == 1
print(target_function)

# Сохраняем стартовое решение в файл
SaveStartSolution(x, y, s, a)

# Создаем хранилище решений, для популяции решений
X, Y, Sresh, A, Target_Function, Size_Solution = SolutionStore(target_function, len(y[0]))

# Cоздаем популяцию решений
PopulationOfSolutions(Target_Function, Size_Solution)

# Считываем популяцию из файла
ReadSolutionPopulationOnFile(X, Y, Sresh, A)

# Создаем последовательность решения
Sequence = CreateSequence(X)

# Создаем новые решения
GetNewSolution(Sequence, X, Y, Sresh, A, Target_Function, Size_Solution)

min_result = min(Target_Function)
number_solution = Target_Function.count(min(Target_Function))
print("Минимальная целевая функция ", min_result, " номер решения ", number_solution)
Time = time.time() - start
print(Time, "seconds")

SaveDateResult(start_target_function, min_result, Time, Sequence[number_solution])

