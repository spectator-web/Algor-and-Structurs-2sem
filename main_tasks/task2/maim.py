# def tree_height(n, parents):
#     heights = [0] * n

#     for i in range(n):
#         if heights[i] != 0:
#             continue

#         height = 0
#         current = i
#         path = []

#         while current != -1:
#             # 🛡 Защита от неверного индекса
#             if current < 0 or current >= n:
#                 break

#             path.append(current)

#             if heights[current] != 0:
#                 height = heights[current]
#                 break

#             current = parents[current]

#         if height == 0:
#             height = 1

#         for j in range(len(path)-1, -1, -1):
#             node = path[j]
#             if node < 0 or node >= n:
#                 continue
#             if j == len(path)-1:
#                 heights[node] = height
#             else:
#                 heights[node] = heights[path[j+1]] + 1

#     return max(heights)
# здесь мы считаем коэфиценты (цена(1 ст)/вес(2 ст) ) и берм наиб коэфицент





def file_open(input_file='lab5/main_task/task2/input.txt',
              output_file='lab5/main_task/task2/output.txt'):
    with open(input_file, 'r') as f:
        n = int(f.readline().strip())
        arr = list(map(int, f.readline().split()))

    result = tree_height(n, arr)

    with open(output_file, 'w') as f:
        f.write(str(result))

    return result


print(file_open())
