# import unittest
# import tracemalloc
# import time
# import tempfile
# import os
# import sys

# sys.path.append(os.path.dirname(__file__))
# from maim import solve, file_open


# class TestDurak(unittest.TestCase):
#     """Тесты для задачи «Дурак» (покрытие карт)"""

#     def setUp(self):
#         tracemalloc.clear_traces()

#     def measure_performance(self, func, *args):
#         """Измерение времени и памяти для функции solve (N, M, trump, hand, attack)"""
#         start_time = time.perf_counter()
#         result = func(*args)
#         end_time = time.perf_counter()
#         exec_time = end_time - start_time

#         tracemalloc.start()
#         _ = func(*args)
#         current, peak = tracemalloc.get_traced_memory()
#         tracemalloc.stop()

#         return result, exec_time, peak

#     # ---------- Базовые тесты ----------
#     def test_basic_cases(self):
#         """Простые ситуации с известным ответом"""
#         print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             # (N, M, trump, hand, attack, expected)
#             ("Одна карта бьётся старшей", 1, 1, 'S', ['7S'], ['6S'], True),
#             ("Одна карта не бьётся (младшая)", 1, 1, 'S', ['6S'], ['7S'], False),
#             ("Козырь бьёт некозыря", 1, 1, 'H', ['6H'], ['7S'], True),
#             ("Козырь не бьёт старшего козыря", 1, 1, 'H', ['7H'], ['AH'], False),
#             ("Две карты, обе бьются", 2, 2, 'D', ['7D', '8D'], ['6D', '7D'], True),
#             ("Две карты, одна не бьётся", 2, 2, 'D', ['7D', '8D'], ['6D', '9D'], False),
#             ("Ход козырями, есть только один старший", 2, 2, 'S', ['AS', 'KS'], ['QS', 'JS'], True),
#             ("Нет хода (M=0)", 5, 0, 'C', ['6C', '7C'], [], True),
#         ]

#         for desc, N, M, trump, hand, attack, expected in test_cases:
#             with self.subTest(desc=desc):
#                 print(f"\n{desc}: N={N}, M={M}, козырь={trump}")
#                 print(f"  рука: {hand}")
#                 print(f"  ход:  {attack}")
#                 result, exec_time, mem_peak = self.measure_performance(solve, N, M, trump, hand, attack)
#                 print(f"Получено: {result}, ожидаем {expected}")
#                 print(f"Время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
#                 self.assertEqual(result, expected)

#     # ---------- Граничные случаи ----------
#     def test_edge_cases(self):
#         """Сложные ситуации с козырями и несколькими вариантами"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("Минимальные N=M=1, YES", 1, 1, 'S', ['7S'], ['6S'], True),
#             ("Минимальные N=M=1, NO", 1, 1, 'S', ['6S'], ['7S'], False),
#             ("Козырь не бьёт своего старшего", 2, 1, 'H', ['7H', '8H'], ['AH'], False),
#             ("Есть козырь, но нужен старше", 3, 2, 'C', ['6C', '7C', '8C'], ['9C', 'TC'], False),
#             ("Перебор вариантов: несколько подходящих", 3, 2, 'D',
#              ['6D', '7D', '8D'], ['5D', '6D'], True),  # 6D бьёт 5D, 7D или 8D бьют 6D
#             ("Все карты – козыри, порядок важен", 4, 3, 'H',
#              ['6H', '7H', '8H', '9H'], ['5H', '6H', '7H'], True),  # 6->5, 7->6, 8->7 (или 9)
#             ("Не хватает старших козырей", 3, 3, 'S',
#              ['6S', '7S', '8S'], ['5S', '6S', '9S'], False),
#             ("Максимальное M=4, всё бьётся", 5, 4, 'C',
#              ['6C', '7C', '8C', '9C', 'TC'], ['5C', '6C', '7C', '8C'], True),
#         ]

#         for desc, N, M, trump, hand, attack, expected in test_cases:
#             with self.subTest(desc=desc):
#                 print(f"\n{desc}")
#                 result, exec_time, mem_peak = self.measure_performance(solve, N, M, trump, hand, attack)
#                 print(f"Получено: {result}, ожидаем {expected}")
#                 print(f"Время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
#                 self.assertEqual(result, expected)

#     # ---------- Производительность ----------
#     def test_performance_max(self):
#         """Тест производительности при максимальных N=35, M=4"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ (N=35, M=4)':^60}")
#         print(f"{'=' * 60}")

#         # Генерируем максимально возможные данные (но так, чтобы ответ был предсказуем)
#         # Возьмём все карты одной масти и козырь тоже эта масть – тогда всё бьётся, если ход младшими
#         trump = 'S'
#         hand = [f"{rank}{trump}" for rank in ['6','7','8','9','T','J','Q','K','A']] * 3 + ['6S','7S']  # 9*3+2=29 <35, добавим ещё
#         # Добираем до 35
#         while len(hand) < 35:
#             hand.append('6S')  # можно повторять, но тогда не хватит старшинства
#         # Но лучше сделать разумный набор, чтобы ответ был True
#         # Для простоты: все карты от 6 до A одной масти, козырь та же – всегда можно отбить любые 4 младшие
#         hand = ['6S','7S','8S','9S','TS','JS','QS','KS','AS'] * 3 + ['6S','7S','8S','9S','TS','JS','QS','KS','AS'][:35-27]
#         # Ход: 4 младшие карты
#         attack = ['6S','7S','8S','9S']

#         N, M = len(hand), len(attack)
#         print(f"N = {N}, M = {M}, козырь S")
#         result, exec_time, mem_peak = self.measure_performance(solve, N, M, trump, hand, attack)
#         print(f"Результат: {result} (ожидается True)")
#         print(f"Время выполнения: {exec_time:.6f} сек")
#         print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")
#         self.assertTrue(result)
#         self.assertLess(exec_time, 1.0, f"Время {exec_time:.2f} сек превышает 1 секунду")

#         # Проверим заведомо ложный случай (не хватает старших)
#         hand2 = ['6S','7S','8S','9S'] * 8 + ['6S','7S','8S']  # 32+3=35, но старших мало
#         attack2 = ['AS','KS','QS','JS']  # все старшие – нечем бить
#         result2, exec_time2, mem_peak2 = self.measure_performance(solve, N, M, trump, hand2, attack2)
#         print(f"\nЛожный случай: результат {result2} (ожидается False)")
#         print(f"Время: {exec_time2:.6f} сек, память: {mem_peak2/1024:.2f} КБ")
#         self.assertFalse(result2)
#         self.assertLess(exec_time2, 1.0)

#     # ---------- Файловые операции ----------
#     def test_file_operations(self):
#         """Проверка чтения из файла и записи результата"""
#         print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
#         print(f"{'=' * 60}")

#         test_cases = [
#             ("YES: одна карта бьётся", "1 1 S\n7S\n6S\n", True),
#             ("NO: одна карта не бьётся", "1 1 S\n6S\n7S\n", False),
#             ("YES: две карты, обе бьются", "2 2 D\n7D 8D\n6D 7D\n", True),
#             ("NO: не хватает козыря", "2 2 H\n6H 7H\n8H 9H\n", False),
#             ("M=0", "3 0 C\n6C 7C 8C\n\n", True),  # пустая строка для хода
#         ]

#         for name, input_data, expected in test_cases:
#             with self.subTest(name=name):
#                 print(f"\n{name}")
#                 fd_in, path_in = tempfile.mkstemp(suffix='.txt', text=True)
#                 fd_out, path_out = tempfile.mkstemp(suffix='.txt', text=True)
#                 try:
#                     with os.fdopen(fd_in, 'w') as f:
#                         f.write(input_data)
#                     os.close(fd_out)

#                     result = file_open(path_in, path_out)
#                     with open(path_out, 'r') as f:
#                         content = f.read().strip()

#                     print(f"Возврат file_open: {result}, ожидаем {expected}")
#                     print(f"Содержимое выходного файла: '{content}'")
#                     self.assertEqual(result, expected)
#                     self.assertEqual(content, "YES" if expected else "NO")
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

sys.path.append(os.path.dirname(__file__))
from maim import solve, file_open


class TestDurak(unittest.TestCase):
    """Тесты для задачи «Дурак» (покрытие карт)"""

    def setUp(self):
        tracemalloc.clear_traces()

    def measure_performance(self, func, *args):
        """Измерение времени и памяти для функции solve (N, M, trump, hand, attack)"""
        start_time = time.perf_counter()
        result = func(*args)
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        tracemalloc.start()
        _ = func(*args)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return result, exec_time, peak

    # ---------- Базовые тесты ----------
    def test_basic_cases(self):
        """Простые ситуации с известным ответом"""
        print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            # (N, M, trump, hand, attack, expected)
            ("Одна карта бьётся старшей", 1, 1, 'S', ['7S'], ['6S'], True),
            ("Одна карта не бьётся (младшая)", 1, 1, 'S', ['6S'], ['7S'], False),
            ("Козырь бьёт некозыря", 1, 1, 'H', ['6H'], ['7S'], True),
            ("Козырь не бьёт старшего козыря", 1, 1, 'H', ['7H'], ['AH'], False),
            ("Две карты, обе бьются", 2, 2, 'D', ['7D', '8D'], ['6D', '7D'], True),
            ("Две карты, одна не бьётся", 2, 2, 'D', ['7D', '8D'], ['6D', '9D'], False),
            ("Ход козырями, есть только один старший", 2, 2, 'S', ['AS', 'KS'], ['QS', 'JS'], True),
            ("Нет хода (M=0)", 5, 0, 'C', ['6C', '7C'], [], True),
        ]

        for desc, N, M, trump, hand, attack, expected in test_cases:
            with self.subTest(desc=desc):
                print(f"\n{desc}: N={N}, M={M}, козырь={trump}")
                print(f"  рука: {hand}")
                print(f"  ход:  {attack}")
                result, exec_time, mem_peak = self.measure_performance(solve, N, M, trump, hand, attack)
                print(f"Получено: {result}, ожидаем {expected}")
                print(f"Время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertEqual(result, expected)

    # ---------- Граничные случаи ----------
    def test_edge_cases(self):
        """Сложные ситуации с козырями и несколькими вариантами (только допустимые ранги)"""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("Минимальные N=M=1, YES", 1, 1, 'S', ['7S'], ['6S'], True),
            ("Минимальные N=M=1, NO", 1, 1, 'S', ['6S'], ['7S'], False),
            ("Козырь не бьёт своего старшего", 2, 1, 'H', ['7H', '8H'], ['AH'], False),
            ("Есть козырь, но нужен старше", 3, 2, 'C', ['6C', '7C', '8C'], ['9C', 'TC'], False),
            # Перебор вариантов: несколько подходящих (используем ранги 6-9)
            ("Перебор вариантов: несколько подходящих", 3, 2, 'D',
             ['6D', '7D', '8D'], ['6D', '7D'], True),  # 7D бьёт 6D, 8D бьёт 7D
            # Все карты – козыри, порядок важен
            ("Все карты – козыри, порядок важен", 4, 3, 'H',
             ['6H', '7H', '8H', '9H'], ['6H', '7H', '8H'], True),  # 7->6, 8->7, 9->8
            # Не хватает старших козырей
            ("Не хватает старших козырей", 3, 3, 'S',
             ['6S', '7S', '8S'], ['6S', '7S', '9S'], False),  # нет карты для 9S
            # Максимальное M=4, всё бьётся
            ("Максимальное M=4, всё бьётся", 5, 4, 'C',
             ['6C', '7C', '8C', '9C', 'TC'], ['6C', '7C', '8C', '9C'], True),
        ]

        for desc, N, M, trump, hand, attack, expected in test_cases:
            with self.subTest(desc=desc):
                print(f"\n{desc}")
                result, exec_time, mem_peak = self.measure_performance(solve, N, M, trump, hand, attack)
                print(f"Получено: {result}, ожидаем {expected}")
                print(f"Время: {exec_time:.6f} сек, память: {mem_peak/1024:.2f} КБ")
                self.assertEqual(result, expected)

    # ---------- Производительность ----------
    def test_performance_max(self):
        """Тест производительности при максимальных N=35, M=4"""
        print(f"\n{'ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ (N=35, M=4)':^60}")
        print(f"{'=' * 60}")

        # Формируем допустимые наборы карт
        ranks = ['6','7','8','9','T','J','Q','K','A']
        trump = 'S'
        # Рука: все карты одной масти (S) – 9 карт, повторим, чтобы получить 35
        hand = [f"{r}{trump}" for r in ranks] * 3 + [f"{r}{trump}" for r in ranks[:8]]  # 27+8=35
        # Ход: 4 младшие карты той же масти
        attack = [f"{r}{trump}" for r in ranks[:4]]

        N, M = len(hand), len(attack)
        print(f"N = {N}, M = {M}, козырь S")
        result, exec_time, mem_peak = self.measure_performance(solve, N, M, trump, hand, attack)
        print(f"Результат: {result} (ожидается True)")
        print(f"Время выполнения: {exec_time:.6f} сек")
        print(f"Пиковое использование памяти: {mem_peak / 1024:.2f} КБ")
        self.assertTrue(result)
        self.assertLess(exec_time, 1.0, f"Время {exec_time:.2f} сек превышает 1 секунду")

        # Проверим заведомо ложный случай (не хватает старших)
        # Рука: только младшие карты (6-9) – 4 ранга * 9 копий = 36, возьмём 35
        hand2 = [f"{r}{trump}" for r in ranks[:4]] * 8 + [f"{r}{trump}" for r in ranks[:3]]  # 32+3=35
        attack2 = [f"{r}{trump}" for r in ranks[5:9]]  # Q,K,A – старшие, нечем бить
        result2, exec_time2, mem_peak2 = self.measure_performance(solve, N, M, trump, hand2, attack2)
        print(f"\nЛожный случай: результат {result2} (ожидается False)")
        print(f"Время: {exec_time2:.6f} сек, память: {mem_peak2/1024:.2f} КБ")
        self.assertFalse(result2)
        self.assertLess(exec_time2, 1.0)

    # ---------- Файловые операции ----------
    def test_file_operations(self):
        """Проверка чтения из файла и записи результата"""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")

        test_cases = [
            ("YES: одна карта бьётся", "1 1 S\n7S\n6S\n", True),
            ("NO: одна карта не бьётся", "1 1 S\n6S\n7S\n", False),
            ("YES: две карты, обе бьются", "2 2 D\n7D 8D\n6D 7D\n", True),
            ("NO: не хватает козыря", "2 2 H\n6H 7H\n8H 9H\n", False),
            ("M=0", "3 0 C\n6C 7C 8C\n\n", True),  # пустая строка для хода
        ]

        for name, input_data, expected in test_cases:
            with self.subTest(name=name):
                print(f"\n{name}")
                fd_in, path_in = tempfile.mkstemp(suffix='.txt', text=True)
                fd_out, path_out = tempfile.mkstemp(suffix='.txt', text=True)
                try:
                    with os.fdopen(fd_in, 'w') as f:
                        f.write(input_data)
                    os.close(fd_out)

                    result = file_open(path_in, path_out)
                    with open(path_out, 'r') as f:
                        content = f.read().strip()

                    print(f"Возврат file_open: {result}, ожидаем {expected}")
                    print(f"Содержимое выходного файла: '{content}'")
                    self.assertEqual(result, expected)
                    self.assertEqual(content, "YES" if expected else "NO")
                finally:
                    os.unlink(path_in)
                    os.unlink(path_out)


if __name__ == '__main__':
    unittest.main(verbosity=2)