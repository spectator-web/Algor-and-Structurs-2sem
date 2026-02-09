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

def solve(n, W, items):
    for i in items :
        
    



def file_open(input_file='bonus/task1/input.txt',
              output_file='bonus/task1/output.txt'):
    with open(input_file, 'r') as f:
        with open(input_file, 'r') as f:
        arr = f.read().strip().split('\n')
        n, W = map(int, lines[0].split())
        for i in range(1, n + 1):
        value, weight = map(int, lines[i].split())
        items.append((value, weight))
        result = solve(n, W, items)


    # result = tree_height(n, arr)

    with open(output_file, 'w') as f:
        f.write(str(result))

    return result


print(file_open())
