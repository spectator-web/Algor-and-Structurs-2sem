import unittest
import tracemalloc
import time
import tempfile
import os
import sys
import random
import math

sys.path.append(os.path.dirname(__file__))
from maim import solve, file_open  # Импортируем solve и file_open


def is_valid_solution(a, result):
    """
    Проверяет корректность решения для задачи о разбиении.
    result может быть -1 (невозможно) или кортежем (k, indices).
    Для успешного решения проверяет:
    - сумма выбранных элементов равна половине общей суммы,
    - все индексы в пределах [1, n],
    - количество элементов совпадает с k.
    """
    if result == -1:
        return True  # -1 всегда допустимый ответ
    if not isinstance(result, tuple) or len(result) != 2:
        return False
    k, indices = result
    if k != len(indices):
        return False
    if not all(1 <= idx <= len(a) for idx in indices):
        return False
    total_sum = sum(a)
    if total_sum % 2 != 0:
        return False  # сумма нечётная – ответ должен быть -1
    half = total_sum // 2
    selected_sum = sum(a[idx - 1] for idx in indices)
    return selected_sum == half


class TestEqualPartition(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        tracemalloc.clear_traces()

    def measure_performance(self, func, *args):
        """Измерение времени и памяти для функции"""
        # Измерение времени
        start_time = time.perf_counter()
        result = func(*args)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # Измерение памяти
        tracemalloc.start()
        _ = func(*args)  # Вызываем функцию еще раз для измерения памяти
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return result, execution_time, peak

    def test_basic_cases(self):
        """Тестирование базовых случаев"""
        print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            {
                "name": "Один элемент (невозможно)",
                "data": [1],
                "expected": -1
            },
            {
                "name": "Два элемента, равных 1 (возможно)",
                "data": [1, 1],
                "expected_any": True
            },
            {
                "name": "Два элемента, сумма нечётная",
                "data": [1, 2],
                "expected": -1
            },
            {
                "name": "Три элемента: 1,2,3 (возможно)",
                "data": [1, 2, 3],
                "expected_any": True
            },
            {
                "name": "Три элемента: 1,1,2 (возможно)",
                "data": [1, 1, 2],
                "expected_any": True
            },
            {
                "name": "Четыре единицы (возможно)",
                "data": [1, 1, 1, 1],
                "expected_any": True
            },
            {
                "name": "1,2,3,4 (сумма 10 – возможно)",
                "data": [1, 2, 3, 4],
                "expected_any": True
            },
            {
                "name": "1,2,3,4,5 (сумма 15 – невозможно)",
                "data": [1, 2, 3, 4, 5],
                "expected": -1
            },
        ]

        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"data={test['data']}")

                n = len(test['data'])
                result, exec_time, mem_peak = self.measure_performance(solve, test['data'], n)

                print(f"Ожидаемый результат: {test.get('expected', 'любое корректное решение')}")
                print(f"Полученный результат: {result}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")

                if 'expected' in test:
                    self.assertEqual(result, test['expected'])
                else:
                    self.assertTrue(is_valid_solution(test['data'], result),
                                    f"Решение {result} некорректно для данных {test['data']}")

    def test_edge_cases(self):
        """Тестирование граничных случаев"""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            {
                "name": "Минимальная длина n=1 (всегда невозможно)",
                "data": [1],
                "expected": -1
            },
            {
                "name": "Максимальные значения при малом n",
                "data": [1, 2, 3, 4, 5, 6, 7],  # сумма 28, половина 14 – возможно
                "expected_any": True
            },
            {
                "name": "Все единицы, чётное количество (возможно)",
                "data": [1] * 10,
                "expected_any": True
            },
            {
                "name": "Все единицы, нечётное количество (невозможно)",
                "data": [1] * 9,
                "expected": -1
            },
            {
                "name": "ai = i, n=3 (возможно)",
                "data": [1, 2, 3],
                "expected_any": True
            },
            {
                "name": "ai = i, n=4 (возможно)",
                "data": [1, 2, 3, 4],
                "expected_any": True
            },
            {
                "name": "ai = i, n=5 (невозможно)",
                "data": [1, 2, 3, 4, 5],
                "expected": -1
            },
            {
                "name": "ai = i, n=7 (возможно)",
                "data": [1, 2, 3, 4, 5, 6, 7],
                "expected_any": True
            },
            {
                "name": "Случай, когда половина суммы достигается единственным способом",
                "data": [1, 1, 2],  # половина = 2, только {2} или {1,1}
                "expected_any": True
            },
        ]

        for i, test in enumerate(test_cases, 1):
            if "data" not in test:
                continue
            # Пропускаем тесты, не удовлетворяющие условию ai ≤ i
            if any(test["data"][j] > j + 1 for j in range(len(test["data"]))):
                print(f"\nТест {i}: {test['name']} — пропущен (не выполнено ai ≤ i)")
                continue

            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"data={test['data']}")

                n = len(test['data'])
                result, exec_time, mem_peak = self.measure_performance(solve, test['data'], n)

                print(f"Ожидаемый результат: {test.get('expected', 'любое корректное решение')}")
                print(f"Полученный результат: {result}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")

                if 'expected' in test:
                    self.assertEqual(result, test['expected'])
                else:
                    self.assertTrue(is_valid_solution(test['data'], result),
                                    f"Решение {result} некорректно для данных {test['data']}")

    # ========== НОВЫЕ ТЕСТЫ ==========

    def test_large_n_all_ones(self):
        """Производительность при n=10000, все единицы (чётное n)"""
        n = 10000
        # Генерируем данные, удовлетворяющие условию ai ≤ i
        data = [1] * n  # сумма n, чётная если n чётное
        # Убедимся, что n чётное
        if n % 2 != 0:
            n -= 1
            data = [1] * n
        print(f"\nТест с {n} единицами")
        result, exec_time, mem_peak = self.measure_performance(solve, data, n)
        print(f"Время выполнения: {exec_time:.6f} сек")
        print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")
        self.assertLess(exec_time, 2.0, f"Время выполнения {exec_time:.2f} сек превышает 2 секунды")
        self.assertTrue(is_valid_solution(data, result), "Решение некорректно")
        # Дополнительно проверим, что количество выбранных элементов равно n//2
        if result != -1:
            k, idxs = result
            self.assertEqual(k, n // 2)

    def test_large_n_ai_equal_i(self):
        """Производительность при n=10000, ai = i (сумма чётная)"""
        n = 10000
        data = [i for i in range(1, n + 1)]
        total = sum(data)
        if total % 2 != 0:
            # Если сумма нечётная, уменьшим n на 1 (чтобы было чётное)
            n -= 1
            data = [i for i in range(1, n + 1)]
        print(f"\nТест с {n} элементами (ai = i)")
        result, exec_time, mem_peak = self.measure_performance(solve, data, n)
        print(f"Время выполнения: {exec_time:.6f} сек")
        print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")
        self.assertLess(exec_time, 2.0, f"Время выполнения {exec_time:.2f} сек превышает 2 секунды")
        self.assertTrue(is_valid_solution(data, result), "Решение некорректно")

    def test_impossible_large_odd_sum(self):
        """Невозможный случай с большой нечётной суммой (n=39999 единиц)"""
        n = 39999
        data = [1] * n
        print(f"\nТест с {n} единицами (нечётная сумма)")
        result, exec_time, mem_peak = self.measure_performance(solve, data, n)
        print(f"Время выполнения: {exec_time:.6f} сек")
        print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")
        self.assertEqual(result, -1, "Должно быть -1 при нечётной сумме")

    def test_early_exit_recovery(self):
        """Проверка восстановления после раннего достижения half"""
        # Случай, где half достигается на первом же элементе (после сортировки по убыванию)
        data = [50, 10, 20, 20]  # сумма=100, half=50
        print(f"\nТест раннего выхода: data={data}")
        result, exec_time, mem_peak = self.measure_performance(solve, data, len(data))
        print(f"Результат: {result}")
        self.assertTrue(is_valid_solution(data, result), "Решение некорректно")
        # Проверим, что выбран именно элемент с индексом 50 (индекс 1 в 1-индексации)
        if result != -1:
            k, idxs = result
            self.assertIn(1, idxs)  # индекс первого элемента (50)
            self.assertEqual(sum(data[i-1] for i in idxs), 50)

    def test_recovery_ambiguity(self):
        """Проверка, что при нескольких возможных решениях алгоритм выдаёт корректное"""
        data = [2, 2, 2, 2]  # half=4, возможны {2,2} (любые два)
        print(f"\nТест с неоднозначным решением: data={data}")
        result, exec_time, mem_peak = self.measure_performance(solve, data, len(data))
        print(f"Результат: {result}")
        self.assertTrue(is_valid_solution(data, result), "Решение некорректно")
        if result != -1:
            k, idxs = result
            self.assertEqual(k, 2)
            self.assertEqual(len(idxs), 2)

    def test_single_element_half(self):
        """Если есть элемент, равный half, ответ должен содержать только его"""
        data = [5, 3, 2]  # half=5
        print(f"\nТест с элементом равным half: data={data}")
        result, exec_time, mem_peak = self.measure_performance(solve, data, len(data))
        print(f"Результат: {result}")
        self.assertTrue(is_valid_solution(data, result), "Решение некорректно")
        if result != -1:
            k, idxs = result
            self.assertEqual(k, 1)
            self.assertEqual(idxs[0], 1)  # индекс первого элемента (5)

    def test_zero_half(self):
        """Случай half = 0 (все элементы нулевые, но по условию ai ≥ 1 – формально недопустимо)"""
        data = [0] * 5
        print(f"\nТест с half=0: data={data}")
        result, exec_time, mem_peak = self.measure_performance(solve, data, len(data))
        print(f"Результат: {result}")
        # Ожидаем 0, [] (пустое множество)
        self.assertEqual(result, (0, []))

    def test_file_operations(self):
        """Тестирование работы с файлами через file_open"""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            {
                "name": "Пример 1 (возможно)",
                "input_data": "3\n1 2 3\n",
                "expected": (1, [3])  # или (2, [1,2]) – допустим любой
            },
            {
                "name": "Пример 2 (невозможно)",
                "input_data": "2\n1 2\n",
                "expected": -1
            },
            {
                "name": "Четыре единицы",
                "input_data": "4\n1 1 1 1\n",
                "expected_any": True
            },
            {
                "name": "ai = i, n=4 (возможно)",
                "input_data": "4\n1 2 3 4\n",
                "expected_any": True
            },
            {
                "name": "ai = i, n=5 (невозможно)",
                "input_data": "5\n1 2 3 4 5\n",
                "expected": -1
            },
        ]

        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")

                # Создаём временные файлы
                input_fd, input_path = tempfile.mkstemp(suffix='.txt', text=True)
                output_fd, output_path = tempfile.mkstemp(suffix='.txt', text=True)

                try:
                    # Записываем входные данные
                    with os.fdopen(input_fd, 'w') as in_file:
                        in_file.write(test['input_data'])
                    os.close(output_fd)

                    # Измеряем время выполнения file_open
                    start_time = time.perf_counter()
                    result = file_open(input_path, output_path)
                    end_time = time.perf_counter()
                    exec_time = end_time - start_time

                    # Читаем результат из выходного файла
                    with open(output_path, 'r') as out_file:
                        lines = out_file.read().strip().split('\n')
                        if lines[0] == '-1':
                            file_result = -1
                        else:
                            count = int(lines[0])
                            indices = list(map(int, lines[1].split())) if len(lines) > 1 else []
                            file_result = (count, indices)

                    print(f"Ожидаемый результат: {test.get('expected', 'любое корректное решение')}")
                    print(f"Результат из файла: {file_result}")
                    print(f"Возвращённое значение file_open: {result}")
                    print(f"Время выполнения: {exec_time:.6f} сек")

                    # Проверяем, что file_open вернул то же, что записано в файл
                    self.assertEqual(result, file_result,
                                     "file_open вернул не то же самое, что записано в файл")

                    # Проверяем корректность решения
                    lines_in = test['input_data'].strip().split('\n')
                    n = int(lines_in[0])
                    a = list(map(int, lines_in[1].split()))
                    if 'expected' in test:
                        if test['expected'] == -1:
                            self.assertEqual(file_result, -1)
                        else:
                            self.assertEqual(file_result, test['expected'])
                    else:
                        self.assertTrue(is_valid_solution(a, file_result),
                                        f"Решение {file_result} некорректно для данных {a}")
                finally:
                    os.unlink(input_path)
                    os.unlink(output_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)