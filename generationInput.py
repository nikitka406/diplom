# Входные данные
import random

N = 10  # число объектов
K = 5  # набор всех ТС

X = [random.randint(-50, 50) for i in range(N)]  # координаты по ОХ
Y = [random.randint(-50, 50) for i in range(N)]  # координаты по ОУ
X[0] = 0
Y[0] = 0
S = [random.randint(2, 2) for i in range(N)]  # число рабочих дней для одного ТС для выполнения всех работ на i объекте
S[0] = 0
ka = [random.randint(1, 1) for i in range(N)]  # число скважин на i объекте
ka[0] = 0
e = [random.randint(1, 10) for i in range(N)]  # начало работы на i объекте
e[0] = 0
l = [0 for j in range(N)]  # конец работы на i объекте
for i in range(N):
    l[i] = e[i] + S[i]

coordinate = open('coordinate.txt', 'w')  # записываем координаты в файл
coordinate.write('X ')
for i in range(N):
    coordinate.write(str(X[i]))
    coordinate.write(',')
coordinate.write('\n')
coordinate.write('Y ')
for i in range(N):
    coordinate.write(str(Y[i]))
    coordinate.write(',')
coordinate.write('\n')
coordinate.write('S ')
for i in range(N):
    coordinate.write(str(S[i]))
    coordinate.write(',')
coordinate.write('\n')
coordinate.write('ka ')
for i in range(N):
    coordinate.write(str(ka[i]))
    coordinate.write(',')
coordinate.write('\n')
coordinate.write('e ')
for i in range(N):
    coordinate.write(str(e[i]))
    coordinate.write(',')
coordinate.write('\n')
coordinate.write('l ')
for i in range(N):
    coordinate.write(str(l[i]))
    coordinate.write(',')
coordinate.write('\n')
coordinate.close()
