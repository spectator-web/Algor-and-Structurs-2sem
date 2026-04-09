

def solve(n, matrices):
    # Крайний случай: одна матрица
    if n == 1:
        return "A"

    # Массив размеров p[0..n], где p[i] и p[i+1] — размеры i-й матрицы
    p = [0] * (n + 1)
    p[0] = matrices[0][0]
    for i in range(n):
        p[i + 1] = matrices[i][1]

    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    # Длина 2: произведение двух матриц
    for i in range(n - 1):
        j = i + 1
        dp[i][j] = p[i] * p[i + 1] * p[j + 1]
        split[i][j] = i

    # Длина от 3 до n с оптимизацией Кнута (монотонность точки разбиения)
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = 10 ** 30
            pi = p[i]
            pj = p[j + 1]
            left = split[i][j - 1]
            right = split[i + 1][j]
            for k in range(left, right + 1):
                cost = dp[i][k] + dp[k + 1][j] + pi * p[k + 1] * pj
                if cost < best:
                    best = cost
                    split[i][j] = k
            dp[i][j] = best

    # Рекурсивное построение скобочной формы
    def build(i, j):
        if i == j:
            return "A"
        k = split[i][j]
        return "(" + build(i, k) + build(k + 1, j) + ")"

    return build(0, n - 1)

def file_open(input_file='bonus/task19/input.txt', output_file='bonus/task19/output.txt'):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    matrices = []
    for i in range(1, n + 1):
        a, b = map(int, lines[i].split())
        matrices.append((a, b))
    result = solve(n, matrices)
    with open(output_file, 'w') as f:
        f.write(result + '\n')
    return result


print(file_open())