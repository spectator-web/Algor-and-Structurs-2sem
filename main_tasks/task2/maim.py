def solve(d, m, n, stops):
    stops = [0] + stops + [d]
    current_pos = 0
    num_refills = 0
    i = 0

    while current_pos < d:
        last_pos = current_pos

        while i < len(stops) and stops[i] <= current_pos + m:
            last_pos = stops[i]
            i += 1

        if last_pos == current_pos:
            return -1

        current_pos = last_pos

        if current_pos < d:
            num_refills += 1

    return num_refills


# def file_open(input_file='main_tasks/task2/input.txt',
#               output_file='main_tasks/task2/output.txt'):
#     with open(input_file, 'r') as f:
#         lines = f.read().strip().split('\n')
#         d = int(lines[0])
#         m = int(lines[1])
#         n = int(lines[2])
#         stops = list(map(int, lines[3].split()))

#     result = solve(d, m, n, stops)

#     with open(output_file, 'w') as f:
#         f.write(str(result))

#     return result

def file_open(input_file='main_tasks/task2/input.txt', output_file='main_tasks/task2/output.txt'):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')
        
        # Считываем данные из файла
        d = int(lines[0])  # Первая строка - это d
        m = int(lines[1])  # Вторая строка - это m
        n = int(lines[2])  # Третья строка - это n
        stops = list(map(int, lines[3].split()))  # Четвертая строка - это список заправок
        
    # Вызываем функцию решения задачи
    result = solve(d, m, n, stops)

    # Записываем результат в выходной файл
    with open(output_file, 'w') as f:
        f.write(str(result))

    return result


print(file_open())









