def solve(nums, n):
    total = sum(nums)
    if total % 3 != 0:
        return False
    target = total // 3

    # префиксные суммы для быстрого вычисления суммы уже распределённых предметов
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    # dp[idx][s1][s2] : 0 – не посещено, 1 – можно, 2 – нельзя
    dp = [[[0] * (target + 1) for _ in range(target + 1)] for _ in range(n + 1)]

    def dfs(idx, s1, s2):
        # idx – количество обработанных элементов, s1, s2 – суммы у первого и второго друзей
        if s1 > target or s2 > target:
            return False
        if idx == n:
            return s1 == target and s2 == target

        if dp[idx][s1][s2] != 0:
            return dp[idx][s1][s2] == 1

        # 1) отдаём предмет первому другу
        if s1 + nums[idx] <= target:
            if dfs(idx + 1, s1 + nums[idx], s2):
                dp[idx][s1][s2] = 1
                return True

        # 2) отдаём второму другу
        if s2 + nums[idx] <= target:
            if dfs(idx + 1, s1, s2 + nums[idx]):
                dp[idx][s1][s2] = 1
                return True

        # 3) отдаём третьему другу (его текущая сумма = prefix[idx] - s1 - s2)
        s3 = prefix[idx] - s1 - s2
        if s3 + nums[idx] <= target:
            if dfs(idx + 1, s1, s2):
                dp[idx][s1][s2] = 1
                return True

        dp[idx][s1][s2] = 2
        return False

    return dfs(0, 0, 0)


def file_open(input_file='bonus/task13/input.txt', output_file='bonus/task13/output.txt'):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')
        n = int(lines[0])
        data = list(map(int, lines[1].split()))
    result = solve(data, n)
    with open(output_file, 'w') as f:
        f.write('1\n' if result else '0\n')
    return result


if __name__ == '__main__':
    file_open()