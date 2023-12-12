import numpy as np
import time

matrix1 = [[26, 65, -32, -35, 91, 70, 27, -96, 25],
           [-55, 88, -11, 71, -15, -18, -10, 29, -46],
           [-69, 12, -78, 52, -93, -77, -95, 3, -20],
           [-86, -11, -60, -83, -1, -39, 54, 13, 41],
           [-61, -22, 99, -56, -64, -79, -46, 53, -58],
           [41, -46, -18, 84, 69, 38, -71, -84, -26],
           [87, -14, -60, 40, 12, 13, -58, -18, -50],
           [93, -91, 65, -85, -26, -12, 91, 4, 58],
           [33, -34, -75, -72, -66, 15, 84, 11, -72]]

vector1 = [-69, 1, -45, -79, -97, -72, 87, 44, -15]

matrix2 = [[188, -32, -9, 7, -61, 49, -53, 23, -31, 62],
           [-32, 101, 11, -32, -80, 1, 53, -7, 94, -109],
           [-9, 11, 231, 96, -62, -12, 72, -40, 72, -77],
           [7, -32, 96, 174, -37, -119, 19, 7, -27, 27],
           [-61, -80, -62, -37, 184, -34, -115, 45, -53, 46],
           [49, 1, -12, -119, -34, 182, 80, -56, -4, 18],
           [-53, 53, 72, 19, -115, 80, 231, -101, 70, -50],
           [23, -7, -40, 7, 45, -56, -101, 227, -10, 23],
           [-31, 94, 72, -27, -53, -4, 70, -10, 241, -155],
           [62, -109, -77, 27, 46, 18, -50, 23, -155, 212]]

vector2 = [-44, 74, 87, 247, -39, 168, 192, -199, -194, 243]

matrix3 = [[-8,-9,-8],
           [2,2,2],
           [-9,-9,4],
           ]

vector3 = [1, 2, 10]


def printMatrixAndVector(A, v):
    for i in range(len(A)):
        for j in range(len(A[0])):
            print("%11.6f " % A[i][j], end="")
        print("%11.6f " % v[i], end="")
        print('\n')


def printMatrix(A):
    for i in range(len(A)):
        for j in range(len(A[0])):
            print("%11.6f " % A[i][j], end="")
        print('\n')


def printVector(v):
    for i in range(len(v)):
        print("%11.6f " % v[i], end="")
    print('\n')


def swap(v, a, b):
    x = v[a]
    v[a] = v[b]
    v[b] = x
    return v


def method_1(A, v):
    print("Метод Гаусса: \n")
    printMatrixAndVector(A, v)
    print("1 шаг\n")
    for i in range(len(A)):
        maxi = abs(A[i][i])
        myi = i
        for j in range(i + 1, len(A), 1):
            if abs(A[j][i]) > maxi and i != j:
                maxi = abs(A[j][i])
                myi = j
        swap(A, i, myi)
        swap(v, i, myi)
        printMatrixAndVector(A, v)
        print("")
        a = A[i][i]
        if a != 0:
            for j in range(i, len(A), 1):  # приведение главного ряда
                A[i][j] = A[i][j] / a
            v[i] = v[i] / a
        for k in range(i + 1, len(A), 1):  # следующий ряд для приведения х[i]
            b = A[k][i]
            if b != 0:
                for j in range(i, len(A), 1):
                    A[i][j] = A[i][j] * b
                v[i] = v[i] * b
            flag = 0
            if np.sign(A[i][i]) == np.sign(A[k][i]) and A[k][i] != 0:
                for j in range(i, len(A), 1):
                    A[k][j] = A[i][j] - A[k][j]
                flag = 1
            elif np.sign(A[i][i]) != np.sign(A[k][i]) and A[k][i] != 0:
                for j in range(i, len(A), 1):
                    A[k][j] = A[i][j] + A[k][j]
                flag = 2
            if flag == 1:
                v[k] = v[i] - v[k]
            elif flag == 2:
                v[k] = v[i] + v[k]
            if b != 0:
                for j in range(i, len(A), 1):
                    A[i][j] = A[i][j] / b
                v[i] = v[i] / b
        printMatrixAndVector(A, v)
        print("%d шаг" % (i + 2) + "\n")
    arr = [0] * len(A)
    arr[len(A) - 1] = v[len(A) - 1]
    for i in range(len(A) - 2, -1, -1):
        res = 0
        for j in range(len(A) - 1, i, -1):
            res += A[i][j] * arr[j]
        res = v[i] - res
        if A[i][i] != 0:
            arr[i] = res / A[i][i]
    printVector(arr)


# start_time = time.time()
# method_1(matrix1, vector1)
# print("--- %s seconds ---" % (time.time() - start_time))

def create_ed_matrix(A):
    res = np.zeros((len(A), len(A)))
    for i in range(len(A)):
        res[i][i] = 1
    return res


def transpose(array):
    for i in range(len(array)):
        for j in range(i, len(array), 1):
            b = array[i][j]
            array[i][j] = array[j][i]
            array[j][i] = b
    return array


def expose(A, B):  # умножение столбца на вектор
    # A - столбец
    # B - ряд
    resarr = np.zeros((len(B), len(B)))
    for i in range(len(B)):
        for j in range(len(B)):
            resarr[i][j] = 2 * A[i] * B[j]
    # printMatrix(resarr)
    return resarr


def gleb(w):
    od_matrix = create_ed_matrix(w)
    resw = expose(w, w)
    H = np.zeros((len(w), len(w)))
    for k in range(len(w)):
        for j in range(len(w)):
            H[k][j] = od_matrix[k][j] - resw[k][j]
    return H


def expose_matrix(A, B):  # умножение матрицы на матрицу
    resarr = np.zeros((len(B), len(B)))
    for i in range(len(B)):
        for j in range(len(B)):
            suma = 0
            for k in range(len(B)):
                suma += A[i][k] * B[k][j]
            resarr[i][j] = suma
    return resarr


def expose_matrix_to_column(A, B):  # умножение матрицы на столбец
    resarr = [0] * len(B)
    for i in range(len(B)):
        suma = 0
        for j in range(len(B)):
            suma += A[i][j] * B[j]
        resarr[i] = suma
    return resarr


w = [0.766183, -0.4544, 0.4544]
m1 = [[2, -8, 8], [10, -8, 10], [5, -5, -8]]
f = expose(w, w)
printMatrix(f)
print("*********************")
s = gleb(w)
printMatrix(s)
print("*********************")
t = expose_matrix(m1, s)
printMatrix(t)


def method_4(A, v):
    print("Метод QR: \n")
    printMatrixAndVector(A, v)
    b = [0] * len(A)
    m = [0] * len(A)
    H = np.zeros((len(A), len(A)))
    w = np.zeros((len(A), len(A)))
    resw = np.zeros((len(A), len(A)))
    R = np.zeros((len(A), len(A)))
    Q = np.zeros((len(A), len(A)))
    od_matrix = create_ed_matrix(A)
    for i in range(len(A)):
        sum = 0
        for k in range(i, len(A), 1):
            sum += A[k][i] * A[k][i]
        b[i] = np.sign((-1) * A[i][i]) * np.sqrt(sum)
        print("вектор бета")
        printVector(b)
        m[i] = 1.0 / (np.sqrt(2 * b[i] * b[i] - 2 * b[i] * A[i][i]))
        print("вектор мю")
        printVector(m)
        for j in range(i, len(A), 1):
            if (j == i):
                w[i][j] = m[i] * (A[i][i] - b[i])
            else:
                w[i][j] = m[i] * A[j][i]
        print("матрица дубль вэ")
        printMatrix(w)
        resw = expose(w[i], w[i])
        for k in range(len(A)):
            for j in range(len(A)):
                H[k][j] = od_matrix[k][j] - resw[k][j]
        print("матрица Н")
        printMatrix(H)
        if i == 0:
            for j in range(len(A)):
                for k in range(len(A)):
                    Q[j][k] = H[j][k]
        else:
            Q = expose_matrix(Q, H)
        R = expose_matrix(H, A)
        for j in range(len(R)):
            for k in range(j):
                if abs(R[j][k]) < 0.000001:
                    R[j][k] = 0
        for j in range(len(A)):
            for k in range(len(A)):
                A[j][k] = R[j][k]
        print("матрица R\n")
        printMatrix(R)
        print("матрица Q\n")
        printMatrix(Q)
    print("результат\n")
    # start_time = time.time()
    for i in range(len(A)):
        for j in range(i, len(A), 1):
            transpose(Q)
    y = expose_matrix_to_column(Q, v)
    printMatrixAndVector(R, y)
    print("ответ\n")
    result = [0] * len(A)
    result[len(A) - 1] = y[len(A) - 1] / R[len(A) - 1][len(A) - 1]
    for i in range(len(A) - 2, -1, -1):
        res = 0
        for j in range(len(A) - 1, i, -1):
            res += R[i][j] * result[j]
        res = y[i] - res
        result[i] = res / R[i][i]
    # print("--- %s seconds ---" % (time.time() - start_time))
    printVector(result)


# method_4(matrix1, vector1)

def hol(A, v):
    f = 0
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] != A[j][i]:
                f = 1
    if f == 0:
        print("Метод Холецкого: \n")
        printMatrixAndVector(A, v)
        Ut = np.zeros((len(A), len(A)))
        U = np.zeros((len(A), len(A)))
        # start_time = time.time()
        for i in range(len(U)):
            sum1 = 0
            for k in range(i):
                sum1 += U[k][i] * U[k][i]
            U[i][i] = np.sqrt(A[i][i] - sum1)
            Ut[i][i] = np.sqrt(A[i][i] - sum1)
            for j in range(i + 1, len(U), 1):
                sum2 = 0
                for k in range(i):
                    sum2 += U[k][i] * U[k][j]
                U[i][j] = (A[i][j] - sum2) / U[i][i];
                Ut[i][j] = (A[i][j] - sum2) / U[i][i];
            print("превращение U\n")
            printMatrix(U)
        print("матрица Ut\n")
        transpose(Ut)
        printMatrix(Ut)
        y = [0] * 10
        x = [0] * 10
        for i in range(len(y)):
            sum = 0
            for k in range(i):
                sum += Ut[i][k] * y[k]
            y[i] = (v[i] - sum) / Ut[i][i]
            print("вектор у\n")
            printVector(y)
        for i in range(len(U) - 1, -1, -1):
            sum = 0
            for k in range(i + 1, len(U), 1):
                sum += U[i][k] * x[k]
            x[i] = (y[i] - sum) / U[i][i];
            print("вектор х\n")
            printVector(x)
        # print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print("Матрица не есть симметричной")


# hol(matrix2, vector2)

# method_4(matrix2, vector2)

def prog(A, v):
    f = 0
    for i in range(len(A) - 2):
        for j in range(i + 2, len(A) - 2, 1):
            if A[i][j] != 0:
                f = 1
    for j in range(len(A) - 2):
        for i in range(j + 2, len(A) - 2, 1):
            if A[i][j] != 0:
                f = 1
                myi = i
                myj = j
    if f == 0:
        print("Метод прогоноки: \n")
        printMatrixAndVector(A, v)
        tau = [0] * len(A)
        tau[0] = A[0][0]
        lam = [0] * len(A)
        lam[0] = v[0] / tau[0]
        delta = [0] * len(A)
        delta[0] = (-1) * A[0][1] / tau[0]
        for i in range(len(A)):
            tau[i] = A[i][i] + A[i][i - 1] * delta[i - 1]
            if (i != len(A) - 1):
                delta[i] = (-1) * A[i][i + 1] / tau[i]
            else:
                delta[i] = 0
            lam[i] = (v[i] - A[i][i - 1] * lam[i - 1]) / tau[i]
            print("вектор tau\n")
            printVector(tau)
            print("вектор lambda\n")
            printVector(lam)
            print("вектор delta\n")
            printVector(delta)
        x = [0] * len(A)
        x[len(A) - 1] = (v[len(A) - 1] - A[len(A) - 1][len(A) - 2] * lam[len(A) - 2]) / tau[len(A) - 1]
        print("вектор х\n")
        printVector(x)
        for i in range(len(A) - 2, -1, -1):
            x[i] = lam[i] + delta[i] * x[i + 1]
            print("вектор х\n")
            printVector(x)
    else:
        print("Метод прогонки не может быть использован для данной матрицы")

# start_time = time.time()
# prog(matrix3, vector3)
# print("--- %s seconds ---" % (time.time() - start_time))

method_4(matrix3, vector3)

