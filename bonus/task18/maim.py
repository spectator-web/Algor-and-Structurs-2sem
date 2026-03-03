def solve(prices):
    n = len(prices)
    INF = 10 ** 12

    dp = [[INF] * (n + 2) for _ in range(n + 1)]
    prev_c = [[-1] * (n + 2) for _ in range(n + 1)]
    used = [[False] * (n + 2) for _ in range(n + 1)]

    dp[0][0] = 0

    for i in range(1, n + 1):
        s = prices[i - 1]
        for c_prev in range(n + 1):
            if dp[i - 1][c_prev] == INF:
                continue

            # 1) Платим за обед
            new_c = c_prev + (1 if s > 100 else 0)
            cost = dp[i - 1][c_prev] + s
            if cost < dp[i][new_c]:
                dp[i][new_c] = cost
                prev_c[i][new_c] = c_prev
                used[i][new_c] = False

            # 2) Используем купон (если есть) – теперь без ограничения по цене!
            if c_prev > 0:
                new_c2 = c_prev - 1
                cost2 = dp[i - 1][c_prev]
                if cost2 < dp[i][new_c2]:
                    dp[i][new_c2] = cost2
                    prev_c[i][new_c2] = c_prev
                    used[i][new_c2] = True

    # Выбираем минимальную стоимость
    min_cost = INF
    best_c = -1
    for c in range(n + 1):
        if dp[n][c] < min_cost:
            min_cost = dp[n][c]
            best_c = c
        elif dp[n][c] == min_cost and c > best_c:
            best_c = c

    # Восстановление ответа
    days_used = []
    c = best_c
    for i in range(n, 0, -1):
        if used[i][c]:
            days_used.append(i)
        c = prev_c[i][c]

    days_used.reverse()
    k2 = len(days_used)
    k1 = best_c

    return min_cost, k1, k2, days_used

def file_open(input_file='bonus/task18/input.txt', output_file='bonus/task18/output.txt'):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split()
        if not lines:
            prices = []
        else:
            n = int(lines[0])
            prices = list(map(int, lines[1:1 + n]))

    min_cost, k1, k2, used_days = solve(prices)

    with open(output_file, 'w') as f:
        f.write(str(min_cost) + '\n')
        f.write(f"{k1} {k2}\n")
        for day in used_days:
            f.write(str(day) + '\n')

    return min_cost, k1, k2, used_days

print(file_open())