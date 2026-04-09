import sys

def solve(n, keys, left, right):
    """
    Выполняет три обхода дерева.
    Возвращает строки для in-order, pre-order, post-order.
    """
    # In-order (центрированный) – итеративный со стеком
    inorder = []
    stack = []
    node = 0
    while stack or node != -1:
        while node != -1:
            stack.append(node)
            node = left[node]
        node = stack.pop()
        inorder.append(str(keys[node]))
        node = right[node]
    
    # Pre-order (прямой) – итеративный со стеком
    preorder = []
    stack = [0]
    while stack:
        node = stack.pop()
        if node == -1:
            continue
        preorder.append(str(keys[node]))
        # Правый потомок кладём первым, чтобы левый обработался следующим
        stack.append(right[node])
        stack.append(left[node])
    
    # Post-order (обратный) – итеративный с флагом посещения
    postorder = []
    stack = [(0, False)]  # (node, children_visited)
    while stack:
        node, visited = stack.pop()
        if node == -1:
            continue
        if visited:
            postorder.append(str(keys[node]))
        else:
            stack.append((node, True))
            stack.append((right[node], False))
            stack.append((left[node], False))
    
    return ' '.join(inorder), ' '.join(preorder), ' '.join(postorder)


def file_open(input_file='input.txt', output_file='output.txt'):
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
        if not data:
            return
        it = iter(data)
        n = int(next(it))
        keys = [0] * n
        left = [-1] * n
        right = [-1] * n
        for i in range(n):
            k = int(next(it))
            l = int(next(it))
            r = int(next(it))
            keys[i] = k
            left[i] = l
            right[i] = r
    
    inorder_str, preorder_str, postorder_str = solve(n, keys, left, right)
    
    with open(output_file, 'w') as f:
        f.write(inorder_str + '\n')
        f.write(preorder_str + '\n')
        f.write(postorder_str + '\n')
    
    return inorder_str, preorder_str, postorder_str


if __name__ == "__main__":
    file_open()