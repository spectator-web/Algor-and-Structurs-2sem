def solve(N):
    """
    Возвращает количество телефонных номеров длины N,
    набираемых ходом коня, по модулю 10^9.
    """
    MOD = 10**9

    # переходы для каждой цифры (куда можно попасть ходом коня)
    moves = [
        [4, 6],       # 0
        [6, 8],       # 1
        [7, 9],       # 2
        [4, 8],       # 3
        [0, 3, 9],    # 4
        [],           # 5 (нет ходов)
        [0, 1, 7],    # 6
        [2, 6],       # 7
        [1, 3],       # 8
        [2, 4]        # 9 (исправлено: только 2 и 4)
    ]

    # dp[digit] – количество номеров текущей длины, оканчивающихся на digit
    dp = [0] * 10
    # длина 1: первая цифра не может быть 0 или 8
    for d in range(10):
        if d != 0 and d != 8:
            dp[d] = 1
        else:
            dp[d] = 0

    # если N == 1, сразу возвращаем сумму
    if N == 1:
        return sum(dp) % MOD

    # для длин от 2 до N
    for _ in range(2, N + 1):
        new_dp = [0] * 10
        for prev in range(10):
            if dp[prev] == 0:
                continue
            for nxt in moves[prev]:
                new_dp[nxt] = (new_dp[nxt] + dp[prev]) % MOD
        dp = new_dp

    # суммируем все возможные окончания
    return sum(dp) % MOD


def file_open(input_file='bonus/task17/input.txt', output_file='bonus/task17/output.txt'):
    """Чтение N из файла, запись результата."""
    with open(input_file, 'r') as f:
        N = int(f.readline().strip())
    result = solve(N)
    with open(output_file, 'w') as f:
        f.write(str(result) + '\n')
    return result


print(file_open())