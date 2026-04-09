import unittest
import tracemalloc
import time
import tempfile
import os
import sys
import random

sys.path.append(os.path.dirname(__file__))
from maim import solve, file_open


def check_parentheses(s, n):
    """Проверяет, что строка s содержит ровно n букв 'A' и правильно расставленные скобки."""
    count_a = 0
    balance = 0
    for ch in s:
        if ch == 'A':
            count_a += 1
        elif ch == '(':
            balance += 1
        elif ch == ')':
            balance -= 1
            if balance < 0:
                return False
    return count_a == n and balance == 0


class TestMatrixParentheses(unittest.TestCase):

    def setUp(self):
        tracemalloc.clear_traces()

    def measure_performance(self, func, *args):
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
        """Простые случаи с известной оптимальной расстановкой."""
        print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        # n=1
        matrices1 = [(5, 5)]
        expected1 = "A"
        result1, t1, mem1 = self.measure_performance(solve, 1, matrices1)
        print(f"\nn=1: ожидаем '{expected1}', получено '{result1}', время {t1:.6f} сек, память {mem1/1024:.2f} КБ")
        self.assertEqual(result1, expected1)
        self.assertTrue(check_parentheses(result1, 1))

        # n=2 – всегда (AA)
        matrices2 = [(2, 3), (3, 4)]
        expected2 = "(AA)"
        result2, t2, mem2 = self.measure_performance(solve, 2, matrices2)
        print(f"n=2: ожидаем '{expected2}', получено '{result2}', время {t2:.6f} сек, память {mem2/1024:.2f} КБ")
        self.assertEqual(result2, expected2)
        self.assertTrue(check_parentheses(result2, 2))

        # n=3 – для размеров 1x2, 2x3, 3x4 оптимально ((AA)A)
        matrices3 = [(1, 2), (2, 3), (3, 4)]
        expected3 = "((AA)A)"  # левоассоциативный порядок
        result3, t3, mem3 = self.measure_performance(solve, 3, matrices3)
        print(f"n=3 (1,2,3,4): ожидаем '{expected3}', получено '{result3}', время {t3:.6f} сек, память {mem3/1024:.2f} КБ")
        self.assertEqual(result3, expected3)
        self.assertTrue(check_parentheses(result3, 3))

        # Другой набор, где оптимально (A(AA))
        matrices3b = [(100, 1), (1, 100), (100, 1)]
        # Для таких размеров левая ассоциация: ((A1A2)A3): cost = 100*1*100 + 100*100*1 = 10000+10000=20000
        # Правая ассоциация: (A1(A2A3)): cost = 1*100*1 + 100*1*1 = 100+100=200 – гораздо меньше.
        expected3b = "(A(AA))"
        result3b, t3b, mem3b = self.measure_performance(solve, 3, matrices3b)
        print(f"n=3 (100,1,100,1): ожидаем '{expected3b}', получено '{result3b}', время {t3b:.6f} сек, память {mem3b/1024:.2f} КБ")
        self.assertEqual(result3b, expected3b)
        self.assertTrue(check_parentheses(result3b, 3))

    def test_edge_cases(self):
        """Граничные случаи: максимальное n=400, случайные размеры."""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        n = 400
        random.seed(123)
        # Генерируем согласованные размеры: a_i, b_i, где b_i = a_{i+1}
        sizes = [random.randint(1, 100) for _ in range(n + 1)]
        matrices = [(sizes[i], sizes[i+1]) for i in range(n)]

        print(f"\nТест с n={n} (случайные размеры)")
        result, exec_time, mem_peak = self.measure_performance(solve, n, matrices)
        print(f"Результат: {result[:50]}... (длина {len(result)})")
        print(f"Время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
        self.assertLess(exec_time, 2.0, f"Время {exec_time:.2f} сек превышает 2 с")
        self.assertTrue(check_parentheses(result, n))

    def test_file_operations(self):
        """Проверка чтения из файла и записи результата."""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("n=1", "1\n5 5\n", "A"),
            ("n=2", "2\n2 3\n3 4\n", "(AA)"),
            ("n=3 (оптимально ((AA)A))", "3\n1 2\n2 3\n3 4\n", "((AA)A)"),
            ("n=3 (оптимально (A(AA)))", "3\n100 1\n1 100\n100 1\n", "(A(AA))"),
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
                    with open(path_out, 'r') as f:
                        content = f.read().strip()

                    print(f"Возврат file_open: '{result}'")
                    print(f"Содержимое выходного файла: '{content}'")
                    self.assertEqual(result, expected)
                    self.assertEqual(content, expected)
                finally:
                    os.unlink(path_in)
                    os.unlink(path_out)


if __name__ == '__main__':
    unittest.main(verbosity=2)