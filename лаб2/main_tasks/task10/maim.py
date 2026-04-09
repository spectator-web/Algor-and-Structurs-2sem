def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        # Изменено условие для сортировки по убыванию коэффициента
        while j >= left and arr[j][1] > key[1]: #здесь можно менять порядок сортировки (повозр-ю/убыванию),а ткже элемент по которому сортируем
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
        if L[i][1] <= R[j][1]: #здесь можно менять порядок сортировки (повозр-ю/убыванию),а ткже элемент по которому сортируем
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


def solve(data, n):
    # Сортируем отрезки по правому концу
    data = timsort(data)
    
    points = []  # Множество точек, которые мы будем выбирать
    current_point = -1  # Текущая точка, которая будет покрывать отрезки
    
    for segment in data:
        # Если текущий отрезок не покрыт текущей точкой
        if current_point < segment[0]:
            # Выбираем новую точку, которая будет покрывать этот отрезок
            current_point = segment[1]
            points.append(current_point)
    
    # Возвращаем минимальное количество точек и сами точки
    return len(points), points
    

def file_open(input_file='main_tasks/task4/input.txt', output_file='main_tasks/task4/output.txt'):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')
        
        # Считываем данные из файла
        n = int(lines[0])  # Первая строка - это количество отрезков

        data = [list(map(int, line.split())) for line in lines[1:]]  # Считываем отрезки
        
    # Вызываем функцию решения задачи
    count, result = solve(data, n)

    # Записываем результат в выходной файл
    with open(output_file, 'w') as f:
        f.write(str(count) + '\n')  # Количество точек
        f.write(' '.join(map(str, result)) + '\n')  # Сами точки, разделенные пробелами

    return count, result


# Выводим результат выполнения программы
print(file_open())






