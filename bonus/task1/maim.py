def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        # Изменено условие для сортировки по убыванию коэффициента
        while j >= left and arr[j][0] < key[0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < n1 and j < n2:
        # Изменено условие для сортировки по убыванию коэффициента
        if L[i][0] >= R[j][0]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def timsort(arr):
    n = len(arr)
    min_run = 32
    
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)
    
    size = min_run
    while size < n:
        for start in range(0, n, 2 * size):
            mid = min(n - 1, start + size - 1)
            end = min((start + 2 * size - 1), n - 1)
            if mid < end:
                merge(arr, start, mid, end)
        size *= 2
    
    return arr

def solve(n, W, items):
    # Создаем список кортежей (коэффициент, стоимость, вес)
    items = [(p / w, p, w) for p, w in items]
    
    # Сортируем по убыванию коэффициента с использованием timsort
    timsort(items)  # Теперь сортирует по убыванию коэффициента
    
    total_value = 0.0
    for ratio, p, w in items:
        if W == 0:
            break
        take = min(w, W)
        total_value += (p / w) * take  # Используем исходный коэффициент
        W -= take
    
    return total_value

def file_open(input_file='bonus/task1/input.txt', output_file='bonus/task1/output.txt'):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')
        n, W = map(int, lines[0].split())
        items = [tuple(map(int, line.split())) for line in lines[1:n+1]]

    result = solve(n, W, items)

    with open(output_file, 'w') as f:
        f.write(f"{result:.4f}")

    return result

print(file_open())