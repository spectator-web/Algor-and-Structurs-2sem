# import unittest
# import tracemalloc
# import time
# import tempfile
# import os
# import sys
# import random

# sys.path.append(os.path.dirname(__file__))
# from maim import solve, file_open


# class TestThreePartition(unittest.TestCase):

#     def setUp(self):
#         tracemalloc.clear_traces()

#     def measure_performance(self, func, *args):
#         """Измерение времени и памяти для функции"""
#         start_time = time.perf_counter()
#         result = func(*args)
#         end_time = time.perf_counter()
#         exec_time = end_time - start_time

#         tracemalloc.start()
#         _ = func(*args)
#         current, peak = tracemalloc.get_traced_memory()
#         tracemalloc.stop()

#         return result, exec_time, peak

#     def test_basic_cases(self):
#         """Базовые случаи разбиения на три равные части"""
#         print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("Один элемент", [1], False),
#             ("Два элемента (сумма не кратна 3)", [1, 1], False),
#             ("Три единицы (возможно)", [1, 1, 1], True),
#             ("1,2,3 (невозможно)", [1, 2, 3], False),
#             ("3,3,3 (возможно)", [3, 3, 3], True),
#             ("Шесть двоек (возможно)", [2, 2, 2, 2, 2, 2], True),
#             ("1,2,3,4,5,6 (возможно)", [1, 2, 3, 4, 5, 6], True),
#             ("1,2,3,4,5,7 (сумма не кратна 3)", [1, 2, 3, 4, 5, 7], False),
#             ("Шесть единиц (возможно)", [1, 1, 1, 1, 1, 1], True),
#             ("Четыре четвёрки (невозможно, сумма 16 не кратна 3)", [4, 4, 4, 4], False),
#         ]

#         for name, data, expected in test_cases:
#             with self.subTest(name=name):
#                 print(f"\n{name}: data={data}, ожидаем {expected}")
#                 n = len(data)
#                 result, exec_time, mem_peak = self.measure_performance(solve, data, n)
#                 print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
#                 self.assertEqual(result, expected)

#     def test_edge_cases(self):
#         """Граничные случаи"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("n=1 минимум", [1], False),
#             ("n=20",[30]*20,False),
#             ("n=10",[1]*10+[2]*10,False),
#             ("Все единицы, n=9 (сумма 9, target=3)", [1] * 9, True),
#             ("Все единицы, n=10 (сумма 10 не кратна 3)", [1] * 10, False),
#             ("Возрастающая 1..7 (сумма 28 не кратна 3)", [1, 2, 3, 4, 5, 6, 7], False),
#             ("1..9 (сумма 45, target=15) – возможно", [1, 2, 3, 4, 5, 6, 7, 8, 9], True),
#             ("Максимальные значения при n=3", [30, 30, 30], True),  # 30+30+30=90, target=30
#             ("Очень большое число, остальные маленькие", [30, 1, 1, 1, 1, 1], False),  # сумма 35, не кратна 3
#         ]

#         for name, data, expected in test_cases:
#             with self.subTest(name=name):
#                 print(f"\n{name}: data={data}, ожидаем {expected}")
#                 n = len(data)
#                 result, exec_time, mem_peak = self.measure_performance(solve, data, n)
#                 print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
#                 self.assertEqual(result, expected)

#     def test_performance_max_n(self):
#         """Производительность при максимальном n=20"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ (n=20)':^60}")
#         print(f"{'=' * 60}")

#         n = 20

#         # 1) все единицы – сумма не кратна 3
#         data1 = [1] * n
#         res1, t1, mem1 = self.measure_performance(solve, data1, n)
#         print(f"\nВсе единицы: результат {res1}, время {t1:.6f} сек, память {mem1/1024:.2f} КБ")
#         self.assertFalse(res1)
#         self.assertLess(t1, 2.0)

#         # 2) чередующиеся 1 и 2 – сумма 30, кратна 3, заведомо возможное разбиение
#         data2 = [1, 2] * 10  # 20 элементов
#         res2, t2, mem2 = self.measure_performance(solve, data2, n)
#         print(f"\nЧередование 1 и 2: результат {res2}, время {t2:.6f} сек, память {mem2/1024:.2f} КБ")
#         self.assertTrue(res2)
#         self.assertLess(t2, 2.0)

#         # 3) случайные числа от 1 до 30
#         random.seed(42)
#         data3 = [random.randint(1, 30) for _ in range(n)]
#         res3, t3, mem3 = self.measure_performance(solve, data3, n)
#         print(f"\nСлучайные числа: результат {res3}, время {t3:.6f} сек, память {mem3/1024:.2f} КБ")
#         self.assertLess(t3, 2.0)

#     def test_file_operations(self):
#         """Тестирование файлового ввода-вывода через file_open"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("Успех (три единицы)", "3\n1 1 1\n", True),
#             ("Неудача (сумма не кратна 3)", "2\n1 2\n", False),
#             ("Успех 1..6", "6\n1 2 3 4 5 6\n", True),
#             ("Успех 1..5 (сумма 15, target=5)", "5\n1 2 3 4 5\n", True),
#             ("Неудача 1..4 (сумма 10 не кратна 3)", "4\n1 2 3 4\n", False),
#         ]

#         for name, input_data, expected in test_cases:
#             with self.subTest(name=name):
#                 print(f"\n{name}: входные данные:\n{input_data.strip()}")
#                 fd_in, path_in = tempfile.mkstemp(suffix='.txt', text=True)
#                 fd_out, path_out = tempfile.mkstemp(suffix='.txt', text=True)
#                 try:
#                     with os.fdopen(fd_in, 'w') as f:
#                         f.write(input_data)
#                     os.close(fd_out)

#                     result = file_open(path_in, path_out)
#                     print(f"Возврат file_open: {result}, ожидаем {expected}")
#                     self.assertEqual(result, expected)

#                     with open(path_out, 'r') as f:
#                         content = f.read().strip()
#                     expected_content = '1' if expected else '0'
#                     print(f"Содержимое выходного файла: '{content}', ожидаем '{expected_content}'")
#                     self.assertEqual(content, expected_content)
#                 finally:
#                     os.unlink(path_in)
#                     os.unlink(path_out)


# if __name__ == '__main__':
#     unittest.main(verbosity=2)

import unittest
import tracemalloc
import time
import tempfile
import os
import sys
import random

sys.path.append(os.path.dirname(__file__))
from maim import solve, file_open


class TestThreePartition(unittest.TestCase):

    def setUp(self):
        tracemalloc.clear_traces()

    def measure_performance(self, func, *args):
        """Измерение времени и памяти для функции"""
        start_time = time.perf_counter()
        result = func(*args)
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        tracemalloc.start()
        _ = func(*args)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return result, exec_time, peak

    def test_basic_cases(self):
        """Базовые случаи разбиения на три равные части"""
        print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("Один элемент", [1], False),
            ("Два элемента (сумма не кратна 3)", [1, 1], False),
            ("Три единицы (возможно)", [1, 1, 1], True),
            ("1,2,3 (невозможно, target=2, но нельзя собрать)", [1, 2, 3], False),
            ("3,3,3 (возможно)", [3, 3, 3], True),
            ("Шесть двоек (возможно)", [2, 2, 2, 2, 2, 2], True),
            ("1,2,3,4,5,6 (возможно)", [1, 2, 3, 4, 5, 6], True),
            ("1,2,3,4,5,7 (сумма не кратна 3)", [1, 2, 3, 4, 5, 7], False),
            ("Шесть единиц (возможно)", [1, 1, 1, 1, 1, 1], True),
            ("Четыре четвёрки (невозможно, сумма 16 не кратна 3)", [4, 4, 4, 4], False),
        ]

        for name, data, expected in test_cases:
            with self.subTest(name=name):
                print(f"\n{name}: data={data}, ожидаем {expected}")
                n = len(data)
                result, exec_time, mem_peak = self.measure_performance(solve, data, n)
                print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Граничные случаи"""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("n=1 минимум", [1], False),
            ("20 чисел по 30 (сумма 600, target=200, но 200 не кратно 30)", [30] * 20, False),
            ("10 единиц + 10 двоек (сумма 30, target=10) – возможно", [1] * 10 + [2] * 10, True),
            ("Все единицы, n=9 (сумма 9, target=3)", [1] * 9, True),
            ("Все единицы, n=10 (сумма 10 не кратна 3)", [1] * 10, False),
            ("Возрастающая 1..7 (сумма 28 не кратна 3)", [1, 2, 3, 4, 5, 6, 7], False),
            ("1..9 (сумма 45, target=15) – возможно", [1, 2, 3, 4, 5, 6, 7, 8, 9], True),
            ("Максимальные значения при n=3", [30, 30, 30], True),
            ("Очень большое число, остальные маленькие", [30, 1, 1, 1, 1, 1], False),
        ]

        for name, data, expected in test_cases:
            with self.subTest(name=name):
                print(f"\n{name}: data={data}, ожидаем {expected}")
                n = len(data)
                result, exec_time, mem_peak = self.measure_performance(solve, data, n)
                print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertEqual(result, expected)

    def test_performance_max_n(self):
        """Производительность при максимальном n=20"""
        print(f"\n{'ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ (n=20)':^60}")
        print(f"{'=' * 60}")

        n = 20

        # 1) все единицы – сумма не кратна 3
        data1 = [1] * n
        res1, t1, mem1 = self.measure_performance(solve, data1, n)
        print(f"\nВсе единицы: результат {res1}, время {t1:.6f} сек, память {mem1/1024:.2f} КБ")
        self.assertFalse(res1)
        self.assertLess(t1, 2.0)

        # 2) чередующиеся 1 и 2 – сумма 30, кратна 3, заведомо возможное разбиение
        data2 = [1, 2] * 10  # 20 элементов
        res2, t2, mem2 = self.measure_performance(solve, data2, n)
        print(f"\nЧередование 1 и 2: результат {res2}, время {t2:.6f} сек, память {mem2/1024:.2f} КБ")
        self.assertTrue(res2)
        self.assertLess(t2, 2.0)

        # 3) случайные числа от 1 до 30
        random.seed(42)
        data3 = [random.randint(1, 30) for _ in range(n)]
        res3, t3, mem3 = self.measure_performance(solve, data3, n)
        print(f"\nСлучайные числа: результат {res3}, время {t3:.6f} сек, память {mem3/1024:.2f} КБ")
        self.assertLess(t3, 2.0)

    def test_file_operations(self):
        """Тестирование файлового ввода-вывода через file_open"""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("Успех (три единицы)", "3\n1 1 1\n", True),
            ("Неудача (сумма не кратна 3)", "2\n1 2\n", False),
            ("Успех 1..6", "6\n1 2 3 4 5 6\n", True),
            ("Успех 1..5 (сумма 15, target=5)", "5\n1 2 3 4 5\n", True),
            ("Неудача 1..4 (сумма 10 не кратна 3)", "4\n1 2 3 4\n", False),
        ]

        for name, input_data, expected in test_cases:
            with self.subTest(name=name):
                print(f"\n{name}: входные данные:\n{input_data.strip()}")
                fd_in, path_in = tempfile.mkstemp(suffix='.txt', text=True)
                fd_out, path_out = tempfile.mkstemp(suffix='.txt', text=True)
                try:
                    with os.fdopen(fd_in, 'w') as f:
                        f.write(input_data)
                    os.close(fd_out)

                    result = file_open(path_in, path_out)
                    print(f"Возврат file_open: {result}, ожидаем {expected}")
                    self.assertEqual(result, expected)

                    with open(path_out, 'r') as f:
                        content = f.read().strip()
                    expected_content = '1' if expected else '0'
                    print(f"Содержимое выходного файла: '{content}', ожидаем '{expected_content}'")
                    self.assertEqual(content, expected_content)
                finally:
                    os.unlink(path_in)
                    os.unlink(path_out)


if __name__ == '__main__':
    unittest.main(verbosity=2)