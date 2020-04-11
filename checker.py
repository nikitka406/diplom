from crossover import *
from function import *

x, y, s, a = OneCarOneLocation()
target_function = CalculationOfObjectiveFunction(x, y, PenaltyFunction(s, a))
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
print("Число используемых машин ", AmountCarUsed(y))

# Сохраняем стартовое решение в файл
SaveStartSolution(x, y, s, a)

target_function, x, y, s, a = Relocate(target_function, len(y[0]))
BeautifulPrint(x, y, s, a)
print("target_function = ", target_function)