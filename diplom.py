from function import *
import factory
from crossover import *
from operators import *
import time

start = time.time()

ClearAllFile()
iteration = 1

# заполняем стартовое решение, одна машина на одну локацию
x, y, s, a = OneCarOneLocation()
start_target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))

print("Целевая функция при стартовом решении ", start_target_function)
SaveDateResult("Целевая функция при стартовом решении " + str(start_target_function))
SaveDateResult("Число используемых машин = " + str(AmountCarUsed(y)))

assert VerificationOfBoundaryConditions(x, y, s, a) == 1
print("Проверка стартового решения пройдена")
SaveDateResult("Проверка стартового решения пройдена\n")

# Сохраняем стартовое решение в файл
SaveStartSolution(x, y, s, a)

# Освобождаем машины если позволяют гран усл
DeleteCarNonNarushOgr(len(y[0]))
x, y, s, a = ReadStartSolutionOfFile(len(y[0]))

# Проверяем что ничего не сломалось
target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, iteration))
assert VerificationOfBoundaryConditions(x, y, s, a) == 1

print("Целевая функция при стартовом решении, но меньшем числе машин ", target_function)
SaveDateResult("Целевая функция при стартовом решении, но меньшем числе машин " + str(target_function))
SaveDateResult("Число используемых машин = " + str(AmountCarUsed(y)))

# Сохраняем стартовое решение в файл
SaveStartSolution(x, y, s, a)

# Создаем хранилище решений, для популяции решений
X, Y, Sresh, A, Target_Function, Size_Solution = SolutionStore(target_function, len(y[0]))

# Cоздаем популяцию решений
PopulationOfSolutions(Target_Function, Size_Solution, iteration)

# Считываем популяцию из файла
ReadSolutionPopulationOnFile(X, Y, Sresh, A)

print("Минимальная целевая функция в популяции = ", min(Target_Function))
print("Максимальная целевая функция в популяции = ", max(Target_Function))
SaveDateResult("Минимальная целевая функция в популяции = " + str(min(Target_Function)))
SaveDateResult("Максимальная целевая функция в популяции = " + str(max(Target_Function)))

# Создаем последовательность решения
Sequence = CreateSequence(X)

file = open('output/population.txt', 'w')
for i in  range(factory.param_population):
    file.write(str(Sequence[i]) + '\n')
    file.write("____________________\n")
file.close()

# Создаем новые решения
GetNewSolution(Sequence, X, Y, Sresh, A, Target_Function, Size_Solution, iteration)

Time = time.time() - start
print(Time, "seconds")
SaveDateResult("Время работы программы = " + str(Time) + 'seconds')
SaveDateResult("______________________________________________________________________________________________________")
