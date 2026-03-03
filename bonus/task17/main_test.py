import unittest
import tracemalloc
import time
import tempfile
import os
import sys

sys.path.append(os.path.dirname(__file__))
from maim import solve, file_open


class TestKnightNumbers(unittest.TestCase):

    def setUp(self):
        tracemalloc.clear_traces()

    def measure_performance(self, func, arg):
        """Измерение времени и памяти для функции, принимающей число N."""
        start_time = time.perf_counter()
        result = func(arg)
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        tracemalloc.start()
        _ = func(arg)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return result, exec_time, peak

    def test_basic_cases(self):
        """Проверка для малых значений N (известные результаты)."""
        print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            (1, 8),
            (2, 16),
            (3, 36),
        ]

        for N, expected in test_cases:
            with self.subTest(N=N):
                print(f"\nN = {N}, ожидаем {expected}")
                result, exec_time, mem_peak = self.measure_performance(solve, N)
                print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Проверка граничных значений N и работы модуля."""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        # N = 1 уже проверен, проверим N = 999 и N = 1000 (максимум)
        for N in (999, 1000):
            with self.subTest(N=N):
                print(f"\nN = {N}")
                result, exec_time, mem_peak = self.measure_performance(solve, N)
                print(f"Результат (mod 10^9): {result}")
                print(f"Время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertLess(exec_time, 1.0, f"Время {exec_time:.2f} сек превышает 1 с")
                self.assertGreaterEqual(result, 0)
                self.assertLess(result, 10**9)

    def test_file_operations(self):
        """Проверка чтения из файла и записи результата."""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("N=1", "1\n", 8),
            ("N=2", "2\n", 16),
            ("N=3", "3\n", 36),
            ("N=1000", "1000\n", None),  # не знаем точное значение, проверим только соответствие
        ]

        for name, input_data, expected in test_cases:
            with self.subTest(name=name):
                print(f"\n{name}: входные данные: {input_data.strip()}")
                fd_in, path_in = tempfile.mkstemp(suffix='.txt', text=True)
                fd_out, path_out = tempfile.mkstemp(suffix='.txt', text=True)
                try:
                    with os.fdopen(fd_in, 'w') as f:
                        f.write(input_data)
                    os.close(fd_out)

                    # Измерять file_open не обязательно, но можно
                    start_time = time.perf_counter()
                    result = file_open(path_in, path_out)
                    end_time = time.perf_counter()
                    exec_time = end_time - start_time

                    with open(path_out, 'r') as f:
                        content = f.read().strip()

                    print(f"Возврат file_open: {result}")
                    print(f"Содержимое выходного файла: '{content}'")
                    print(f"Время выполнения: {exec_time:.6f} сек")

                    if expected is not None:
                        self.assertEqual(result, expected)
                        self.assertEqual(content, str(expected))
                    else:
                        # Для N=1000 просто проверим, что результат целый и в пределах модуля
                        self.assertIsInstance(result, int)
                        self.assertGreaterEqual(result, 0)
                        self.assertLess(result, 10**9)
                        self.assertEqual(content, str(result))

                finally:
                    os.unlink(path_in)
                    os.unlink(path_out)


if __name__ == '__main__':
    unittest.main(verbosity=2)