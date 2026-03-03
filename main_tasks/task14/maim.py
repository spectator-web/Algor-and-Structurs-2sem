def solve(expression):
    """
    Возвращает максимальное значение арифметического выражения,
    полученного расстановкой скобок.
    """
    # Разделяем строку на числа и операции
    numbers = []
    ops = []
    for i, ch in enumerate(expression):
        if i % 2 == 0:
            numbers.append(int(ch))
        else:
            ops.append(ch)

    n = len(numbers)
    # Таблицы минимальных и максимальных значений для подотрезков
    min_val = [[0] * n for _ in range(n)]
    max_val = [[0] * n for _ in range(n)]

    # Инициализация диагонали (одно число)
    for i in range(n):
        min_val[i][i] = max_val[i][i] = numbers[i]

    # Перебор длины подотрезка
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Начальные значения для текущего отрезка
            min_val[i][j] = float('inf')
            max_val[i][j] = -float('inf')

            # Перебор места последней операции
            for k in range(i, j):
                op = ops[k]
                # Возможные значения левой и правой частей
                left_min = min_val[i][k]
                left_max = max_val[i][k]
                right_min = min_val[k + 1][j]
                right_max = max_val[k + 1][j]

                # Вычисляем все комбинации в зависимости от операции
                if op == '+':
                    candidates = (
                        left_min + right_min,
                        left_min + right_max,
                        left_max + right_min,
                        left_max + right_max
                    )
                elif op == '-':
                    candidates = (
                        left_min - right_min,
                        left_min - right_max,
                        left_max - right_min,
                        left_max - right_max
                    )
                else:  # op == '*'
                    candidates = (
                        left_min * right_min,
                        left_min * right_max,
                        left_max * right_min,
                        left_max * right_max
                    )

                # Обновляем минимум и максимум для отрезка [i, j]
                min_val[i][j] = min(min_val[i][j], min(candidates))
                max_val[i][j] = max(max_val[i][j], max(candidates))

    # Результат для всего выражения
    return max_val[0][n - 1]


def file_open(input_file='main_tasks/task14/input.txt', output_file='main_tasks/task14/output.txt'):
    """Чтение из файла, вычисление и запись результата."""
    with open(input_file, 'r') as f:
        s = f.readline().strip()
    result = solve(s)
    with open(output_file, 'w') as f:
        f.write(str(result) + '\n')
    return result


print(file_open())