import factory

#преобразование матрицы Х в последовательность посещения городов
def XDisplayInTheSequence(x, bufer, i, k, bul):
    for j in range(factory.N):
        if x[i][j][k] == 1:
            bul += 1
            bufer[k][bul] = j
            if j != 0:
                XDisplayInTheSequence(x, bufer, j, k, bul)

