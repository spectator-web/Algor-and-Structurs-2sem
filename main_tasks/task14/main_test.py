# import unittest
# import tracemalloc
# import time
# import tempfile
# import os
# import sys
# import random

# sys.path.append(os.path.dirname(__file__))
# from maim import solve, file_open


# class TestArithmeticExpression(unittest.TestCase):

#     def setUp(self):
#         tracemalloc.clear_traces()

#     def measure_performance(self, func, arg):
#         """Измерение времени и памяти для функции, принимающей строку"""
#         # Измерение времени
#         start_time = time.perf_counter()
#         result = func(arg)
#         end_time = time.perf_counter()
#         exec_time = end_time - start_time

#         # Измерение памяти
#         tracemalloc.start()
#         _ = func(arg)
#         current, peak = tracemalloc.get_traced_memory()
#         tracemalloc.stop()

#         return result, exec_time, peak

#     def test_basic_cases(self):
#         """Простые выражения с известным максимумом"""
#         print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("Одна цифра", "5", 5),
#             ("Сложение двух чисел", "1+2", 3),
#             ("Вычитание двух чисел", "1-2", -1),
#             ("Умножение двух чисел", "2*3", 6),
#             ("Три сложения", "1+2+3", 6),
#             ("Три вычитания (максимум со скобками)", "1-2-3", 2),
#             ("Умножение и сложение", "2*3+4", 14),
#             ("Пример из условия", "5-8+7*4-8+9", 200),
#         ]

#         for description, expr, expected in test_cases:
#             with self.subTest(description=description):
#                 print(f"\n{description}: {expr} -> ожидаем {expected}")
#                 result, exec_time, mem_peak = self.measure_performance(solve, expr)
#                 print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
#                 self.assertEqual(result, expected)

#     def test_edge_cases(self):
#         """Граничные случаи и выражения с нулём, максимумом"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("Нули", "0+0", 0),
#             ("Все девятки через умножение", "9*9*9", 729),
#             ("Вычитание с получением большего", "9-9-9", 9),
#             ("Умножение и вычитание", "1-2*3", -3),   # максимум: (1-2)*3 = -3
#             ("Сложение и умножение", "1+2*3", 9),    # максимум: (1+2)*3 = 9
#             ("Длинное выражение с нулём в конце", "1*2*3*4*5*6*7*8*9*0", 0),
#             ("Отрицательный максимум", "0-1-2-3-4-5", 13),  # расстановка: 0-(1-2-3-4-5) = 0-(-13) = 13? Проверим: надо вычислить правильно. Для 0-1-2-3-4-5 без скобок = -15. Максимум: 0-(1-2-3-4-5) = 0-( -13) = 13. Или (0-1)-2-3-4-5 = -15. Лучше 13. Но можно и 0-1-2-3-(4-5)=0-1-2-3-(-1)= -5. Найдём максимум: (0-1-2-3-4)-5 = -15, (0-1-2-3)-(4-5)= -6-(-1)= -5, (0-1-2)-(3-4-5)= -3-( -6)=3, (0-1)-(2-3-4-5)= -1-( -10)=9, 0-(1-2-3-4-5)=13. Действительно 13. Проверим, что алгоритм найдёт 13.
#             # Но для проверки проще взять "0-1-2-3-4-5", ожидаем 13.
#         ]
#         # Добавим последний случай отдельно, чтобы не запутаться
#         test_cases.append(("Максимум при вычитаниях", "0-1-2-3-4-5", 13))

#         for description, expr, expected in test_cases:
#             with self.subTest(description=description):
#                 print(f"\n{description}: {expr} -> ожидаем {expected}")
#                 result, exec_time, mem_peak = self.measure_performance(solve, expr)
#                 print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
#                 self.assertEqual(result, expected)

#     def test_performance_max_n(self):
#         """Производительность при максимальной длине (15 чисел, 14 операций)"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ (макс. длина)':^60}")
#         print(f"{'=' * 60}")

#         n_numbers = 15
#         digits = [str(random.randint(0, 9)) for _ in range(n_numbers)]
#         ops = [random.choice(['+', '-', '*']) for _ in range(n_numbers - 1)]

#         # Построим строку: цифра операция цифра операция ...
#         expr = digits[0]
#         for d, op in zip(digits[1:], ops):
#             expr += op + d

#         print(f"\nВыражение длины {len(expr)}: {expr[:50]}...")

#         result, exec_time, mem_peak = self.measure_performance(solve, expr)
#         print(f"Результат: {result}")
#         print(f"Время выполнения: {exec_time:.6f} сек")
#         print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")

#         self.assertLess(exec_time, 5.0, f"Время выполнения {exec_time:.2f} сек превышает 5 секунд")

#     def test_file_operations(self):
#         """Тестирование файлового ввода-вывода через file_open"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("Простое сложение", "1+2+3\n", 6),
#             ("Пример из условия", "5-8+7*4-8+9\n", 200),
#             ("Одна цифра", "7\n", 7),
#             ("Выражение с нулём", "0*9+8-7\n", 8),  # (0*9)+(8-7)=1? Но можно 0*(9+8-7)=0, максимум 1? Проверим: 0*9+8-7 без скобок = 1, со скобками: 0*(9+8-7)=0, (0*9+8)-7=1, 0*(9+8)-7=-7, 0*9+(8-7)=1. Максимум 1. Ожидаем 1.
#         ]
#         # Исправим последнее, чтобы было однозначно: "0*9+8-7" максимум 1.
#         # Но для надёжности возьмём что-то проще.
#         test_cases = [
#             ("Простое сложение", "1+2+3\n", 6),
#             ("Пример из условия", "5-8+7*4-8+9\n", 200),
#             ("Одна цифра", "7\n", 7),
#             ("Умножение и сложение", "2*3+4\n", 14),
#         ]

#         for name, input_data, expected in test_cases:
#             with self.subTest(name=name):
#                 print(f"\n{name}: входные данные: {input_data.strip()}")
#                 fd_in, path_in = tempfile.mkstemp(suffix='.txt', text=True)
#                 fd_out, path_out = tempfile.mkstemp(suffix='.txt', text=True)
#                 try:
#                     with os.fdopen(fd_in, 'w') as f:
#                         f.write(input_data)
#                     os.close(fd_out)

#                     # Измерять file_open по желанию, можно просто вызвать
#                     result = file_open(path_in, path_out)
#                     print(f"Возврат file_open: {result}, ожидаем {expected}")
#                     self.assertEqual(result, expected)

#                     with open(path_out, 'r') as f:
#                         content = f.read().strip()
#                     print(f"Содержимое выходного файла: '{content}'")
#                     self.assertEqual(content, str(expected))
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


class TestArithmeticExpression(unittest.TestCase):

    def setUp(self):
        tracemalloc.clear_traces()

    def measure_performance(self, func, arg):
        """Измерение времени и памяти для функции, принимающей строку"""
        # Измерение времени
        start_time = time.perf_counter()
        result = func(arg)
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        # Измерение памяти
        tracemalloc.start()
        _ = func(arg)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return result, exec_time, peak

    def test_basic_cases(self):
        """Простые выражения с известным максимумом"""
        print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("Одна цифра", "5", 5),
            ("Сложение двух чисел", "1+2", 3),
            ("Вычитание двух чисел", "1-2", -1),
            ("Умножение двух чисел", "2*3", 6),
            ("Три сложения", "1+2+3", 6),
            ("Три вычитания (максимум со скобками)", "1-2-3", 2),
            ("15 чисел, все умножения (без нуля)", "1*2*3*4*5*6*7*8*9*1*2*3*4*5", 43545600),
            ("15 чисел, максимум при вычитаниях", "0-1-2-3-4-5-6-7-8-9-0-1-2-3-4", 53),
            ("Умножение и сложение", "2*3+4", 14),
            ("Пример из условия", "5-8+7*4-8+9", 200),
        ]

        for description, expr, expected in test_cases:
            with self.subTest(description=description):
                print(f"\n{description}: {expr} -> ожидаем {expected}")
                result, exec_time, mem_peak = self.measure_performance(solve, expr)
                print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Граничные случаи и выражения с нулём, максимумом"""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("Нули", "0+0", 0),
            ("Все девятки через умножение", "9*9*9", 729),
            ("Вычитание с получением большего", "9-9-9", 9),
            ("Умножение и вычитание", "1-2*3", -3),   # максимум: (1-2)*3 = -3
            ("Сложение и умножение", "1+2*3", 9),    # максимум: (1+2)*3 = 9
            ("Длинное выражение с нулём в конце", "1*2*3*4*5*6*7*8*9*0", 0),
            ("Отрицательный максимум", "0-1-2-3-4-5", 13),  # расстановка: 0-(1-2-3-4-5) = 0-(-13) = 13? Проверим: надо вычислить правильно. Для 0-1-2-3-4-5 без скобок = -15. Максимум: 0-(1-2-3-4-5) = 0-( -13) = 13. Или (0-1)-2-3-4-5 = -15. Лучше 13. Но можно и 0-1-2-3-(4-5)=0-1-2-3-(-1)= -5. Найдём максимум: (0-1-2-3-4)-5 = -15, (0-1-2-3)-(4-5)= -6-(-1)= -5, (0-1-2)-(3-4-5)= -3-( -6)=3, (0-1)-(2-3-4-5)= -1-( -10)=9, 0-(1-2-3-4-5)=13. Действительно 13. Проверим, что алгоритм найдёт 13.
            # Но для проверки проще взять "0-1-2-3-4-5", ожидаем 13.
        ]
        # Добавим последний случай отдельно, чтобы не запутаться
        test_cases.append(("Максимум при вычитаниях", "0-1-2-3-4-5", 13))

        for description, expr, expected in test_cases:
            with self.subTest(description=description):
                print(f"\n{description}: {expr} -> ожидаем {expected}")
                result, exec_time, mem_peak = self.measure_performance(solve, expr)
                print(f"Получено: {result}, время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertEqual(result, expected)

    def test_performance_max_n(self):
        """Производительность при максимальной длине (15 чисел, 14 операций)"""
        print(f"\n{'ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ (макс. длина)':^60}")
        print(f"{'=' * 60}")

        n_numbers = 15
        digits = [str(random.randint(0, 9)) for _ in range(n_numbers)]
        ops = [random.choice(['+', '-', '*']) for _ in range(n_numbers - 1)]

        # Построим строку: цифра операция цифра операция ...
        expr = digits[0]
        for d, op in zip(digits[1:], ops):
            expr += op + d

        print(f"\nВыражение длины {len(expr)}: {expr[:50]}...")

        result, exec_time, mem_peak = self.measure_performance(solve, expr)
        print(f"Результат: {result}")
        print(f"Время выполнения: {exec_time:.6f} сек")
        print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")

        self.assertLess(exec_time, 5.0, f"Время выполнения {exec_time:.2f} сек превышает 5 секунд")

    def test_file_operations(self):
        """Тестирование файлового ввода-вывода через file_open"""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("Простое сложение", "1+2+3\n", 6),
            ("Пример из условия", "5-8+7*4-8+9\n", 200),
            ("Одна цифра", "7\n", 7),
            ("Выражение с нулём", "0*9+8-7\n", 8),  # (0*9)+(8-7)=1? Но можно 0*(9+8-7)=0, максимум 1? Проверим: 0*9+8-7 без скобок = 1, со скобками: 0*(9+8-7)=0, (0*9+8)-7=1, 0*(9+8)-7=-7, 0*9+(8-7)=1. Максимум 1. Ожидаем 1.
        ]
        # Исправим последнее, чтобы было однозначно: "0*9+8-7" максимум 1.
        # Но для надёжности возьмём что-то проще.
        test_cases = [
            ("Простое сложение", "1+2+3\n", 6),
            ("Пример из условия", "5-8+7*4-8+9\n", 200),
            ("Одна цифра", "7\n", 7),
            ("Умножение и сложение", "2*3+4\n", 14),
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

                    # Измерять file_open по желанию, можно просто вызвать
                    result = file_open(path_in, path_out)
                    print(f"Возврат file_open: {result}, ожидаем {expected}")
                    self.assertEqual(result, expected)

                    with open(path_out, 'r') as f:
                        content = f.read().strip()
                    print(f"Содержимое выходного файла: '{content}'")
                    self.assertEqual(content, str(expected))
                finally:
                    os.unlink(path_in)
                    os.unlink(path_out)


if __name__ == '__main__':
    unittest.main(verbosity=2)