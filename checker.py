from function import *
from operators import *
from forFile import *
ClearAllFile()
children = [[0, 0], [5, 0], [13, 0], [14, 0], [8, 0], [4, 0], [9, 0], [6, 0], [12, 0], [15, 0], [7, 0], [11, 0], [1, 0], [2, 0], [3, 0], [10, 0], [0, 0]]
x, y, s, a, sizek = SequenceDisplayInTheXYSA(children)
BeautifulPrint(x, y, s, a)
target_function = CalculationOfObjectiveFunction(x, PenaltyFunction(y, s, a, 1))
timeLocal = [0, 0]
x, y, s, a, target_function, sizeK, timeLocal = Relocate(x, y, s, a, target_function, sizek, 1,
                                                                    timeLocal)
