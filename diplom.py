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

#Создаем хранилище решений, для большего числа рещений
X, Y, Sresh, A, Target_Function, bufer = SolutionStore()

#Cоздаем популяцию решений
PopulationOfSolutions(X, Y, Sresh, A, Target_Function, x, y, s, a)
