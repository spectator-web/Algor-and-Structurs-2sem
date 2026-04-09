



# def insertion_sort(arr, left, right):
#     for i in range(left + 1, right + 1):
#         key = arr[i]
#         j = i - 1
#         while j >= left and arr[j][0] < key[0]:
#             arr[j + 1] = arr[j]
#             j -= 1
#         arr[j + 1] = key
#     return arr

# def merge(arr, left, mid, right):
#     n1 = mid - left + 1
#     n2 = right - mid
#     L = arr[left:mid + 1]
#     R = arr[mid + 1:right + 1]

#     i = j = 0
#     k = left

#     while i < n1 and j < n2:
#         if L[i][0] >= R[j][0]:
#             arr[k] = L[i]
#             i += 1
#         else:
#             arr[k] = R[j]
#             j += 1
#         k += 1

#     while i < n1:
#         arr[k] = L[i]
#         i += 1
#         k += 1
#     while j < n2:
#         arr[k] = R[j]
#         j += 1
#         k += 1

# def timsort(arr):
#     n = len(arr)
#     min_run = 32

#     for start in range(0, n, min_run):
#         end = min(start + min_run - 1, n - 1)
#         insertion_sort(arr, start, end)

#     size = min_run
#     while size < n:
#         for start in range(0, n, 2 * size):
#             mid = min(n - 1, start + size - 1)
#             end = min((start + 2 * size - 1), n - 1)
#             if mid < end:
#                 merge(arr, start, mid, end)
#         size *= 2

#     return arr



def solve(a, n):
    total = sum(a)

    if total % 2 != 0:
        return -1

    half = total // 2

    if half == 0:
        return 0, []

    #  1. Приоритет одиночного элемента = half
    for i in range(n):
        if a[i] == half:
            return 1, [i + 1]

    #  2. Жадный набор с конца
    result = []
    current = 0

    for i in range(n - 1, -1, -1):
        if current + a[i] <= half:
            result.append(i + 1)
            current += a[i]
        if current == half:
            break

    if current != half:
        return -1

    return len(result), result

def file_open(input_file='main_tasks/task12/input.txt', output_file='main_tasks/task12/output.txt'):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')
        n = int(lines[0])
        data = list(map(int, lines[1].split()))
    result = solve(data, n)
    with open(output_file, 'w') as f:
        if result == -1:
            f.write("-1\n")
        else:
            count, indices = result
            f.write(f"{count}\n{' '.join(map(str, indices))}\n")
    return result

print(file_open())