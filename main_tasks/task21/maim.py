def can_cover(att, hand, trump, rank_val):
    """
    Определяет, может ли карта hand покрыть карту att.
    rank_val: словарь соответствия ранга и его порядка.
    """
    rank_att, suit_att = att[0], att[1]
    rank_hand, suit_hand = hand[0], hand[1]

    if suit_att != trump:
        # некозырная атакующая карта
        # можно покрыть либо старшей картой той же масти, либо любым козырем
        if suit_hand == suit_att and rank_val[rank_hand] > rank_val[rank_att]:
            return True
        if suit_hand == trump:
            return True
        return False
    else:
        # козырная атакующая карта
        # можно покрыть только старшим козырем
        if suit_hand == trump and rank_val[rank_hand] > rank_val[rank_att]:
            return True
        return False


def solve(N, M, trump, hand, attack):
    """Возвращает True, если можно отбить все карты."""
    if M == 0:
        return True

    # числовые значения рангов для сравнения
    rank_order = ['6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    rank_val = {r: i for i, r in enumerate(rank_order)}

    # рекурсивный перебор с использованием битовой маски использованных карт
    def dfs(idx, used):
        if idx == M:
            return True
        for i in range(N):
            if not (used >> i) & 1:
                if can_cover(attack[idx], hand[i], trump, rank_val):
                    if dfs(idx + 1, used | (1 << i)):
                        return True
        return False

    return dfs(0, 0)


def file_open(input_file='main_tasks/task21/input.txt', output_file='main_tasks/task21/output.txt'):
    """Чтение входных данных, вызов solve и запись результата."""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # первая строка: N M R
    first = lines[0].strip().split()
    N = int(first[0])
    M = int(first[1])
    trump = first[2]

    # вторая строка: карты на руках
    hand = lines[1].strip().split()
    # третья строка: карты хода
    attack = lines[2].strip().split()

    result = solve(N, M, trump, hand, attack)

    with open(output_file, 'w') as f:
        f.write("YES\n" if result else "NO\n")
    return result


print(file_open())