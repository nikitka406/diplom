from diplom import *

# Граничные условия
def X_join_Y(x, y):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(K):
        for j in range(N):
            for i in range(N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s, S):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += s[i][k]
            if bufer1 != S[i]:
                return 0
            bufer1 = 0
    return 1


def TC_equal_KA(ka, y):
    bufer1 =0
    # Add constraint: sum (y[i][k])<=ka[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += y[i][k]
            if bufer1 > ka[i]:
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, S, y):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, N):
        for k in range(K):
            if s[i][k] > S[i] * y[i][k]:
                return 0
    return 1


def window_time_down(a, s, e):
    # Add constraint: e[i]<=a[i][k]
    for i in range(N):
        for k in range(K):
            if e[i] > a[i][k]:
                return 0
    return 1


def window_time_up(a, s, l):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, N):
        for k in range(K):
            if a[i][k] + s[i][k] > l[i]:
                return 0
    return 1


def ban_cycle(a, x, t, s, l):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, N):
        for j in range(1, N):
            for k in range(K):
                if a[i][k] - a[j][k] + x[i][j][k] * t[i][j] + s[i][k] > l[i] * (1 - x[i][j][k]):
                    return 0
    return 1


def positive_a_and_s(a, s):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(N):
        for j in range(N):
            for k in range(K):
                if s[i][k] < 0 or a[i][k] < 0:
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    return 0
    return 1
