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


class TestKnapsack(unittest.TestCase):

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
        """Тестирование базовых случаев из условия"""
        print(f"\n{'ТЕСТИРОВАНИЕ БАЗОВЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Пример 1",
                "n": 3,
                "W": 50,
                "items": [(60, 20), (100, 50), (120, 30)],
                "expected": 180.0,
                "tolerance": 0.0001
            },
            {
                "name": "Пример 2",
                "n": 1,
                "W": 10,
                "items": [(500, 30)],
                "expected": 500/30*10,
                "tolerance": 0.0001
            },
            {
                "name": "Пустой рюкзак",
                "n": 3,
                "W": 0,
                "items": [(60, 20), (100, 50), (120, 30)],
                "expected": 0.0,
                "tolerance": 0.0001
            },
            {
                "name": "Все помещается",
                "n": 3,
                "W": 100,
                "items": [(60, 20), (100, 50), (120, 30)],
                "expected": 280.0,
                "tolerance": 0.0001
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"n={test['n']}, W={test['W']}, items={test['items'][:3]}...")
                
                # Измеряем производительность
                result, exec_time, mem_peak = self.measure_performance(
                    solve, test['n'], test['W'], test['items']
                )
                
                print(f"Ожидаемый результат: {test['expected']:.4f}")
                print(f"Полученный результат: {result:.4f}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
                
                # Проверка с учетом погрешности
                self.assertAlmostEqual(result, test['expected'], 
                                     delta=test['tolerance'],
                                     msg=f"Ожидалось {test['expected']}, получено {result}")

    def test_edge_cases_large_numbers(self):
        """Тестирование граничных случаев с большими числами"""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Максимальные значения (n=1)",
                "n": 1,
                "W": 2 * 10**6,
                "items": [(2 * 10**6, 2 * 10**6)],
                "expected": 2 * 10**6,
                "tolerance": 0.001
            },
            {
                "name": "Большой W, маленькие предметы",
                "n": 100,
                "W": 2 * 10**6,
                "items": [(1, 1) for _ in range(100)],
                "expected": 100.0,
                "tolerance": 0.001
            },
            {
                "name": "Маленький W, большие предметы",
                "n": 100,
                "W": 1,
                "items": [(10**6, 10**6) for _ in range(100)],
                "expected": 1.0,
                "tolerance": 0.001
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"n={test['n']}, W={test['W']}")
                
                result, exec_time, mem_peak = self.measure_performance(
                    solve, test['n'], test['W'], test['items']
                )
                
                print(f"Ожидаемый результат: {test['expected']:.2f}")
                print(f"Полученный результат: {result:.2f}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
                
                self.assertAlmostEqual(result, test['expected'], 
                                     delta=test['tolerance'])

    def test_random_cases(self):
        """Тестирование на случайных данных"""
        print(f"\n{'ТЕСТИРОВАНИЕ НА СЛУЧАЙНЫХ ДАННЫХ':^60}")
        print(f"{'=' * 60}")
        
        sizes = [10, 100, 500, 1000]  # До максимального n по условию
        
        for size in sizes:
            for case_type in ["random", "worst_case"]:
                if case_type == "random":
                    # Случайные предметы (избегаем нулевого веса)
                    items = [(random.randint(1, 2000000), 
                             random.randint(1, 2000000)) 
                            for _ in range(size)]
                    W = random.randint(1, 2000000)
                    name = f"Случайные данные (n={size})"
                else:
                    # "Худший" случай: все предметы одинакового качества
                    items = [(1000000, 1000000) for _ in range(size)]
                    W = 500000
                    name = f"Одинаковые предметы (n={size})"
                
                print(f"\n{name}")
                print(f"n={size}, W={W}")
                
                # Вычисляем эталонный результат жадным алгоритмом
                items_with_ratio = [(p/w if w > 0 else float('inf'), p, w) for p, w in items]
                items_with_ratio.sort(reverse=True, key=lambda x: x[0])
                
                expected = 0.0
                remaining = W
                for ratio, p, w in items_with_ratio:
                    if remaining == 0:
                        break
                    take = min(w, remaining)
                    expected += (p/w) * take if w > 0 else p
                    remaining -= take
                
                # Измеряем производительность solve
                result, exec_time, mem_peak = self.measure_performance(
                    solve, size, W, items
                )
                
                print(f"Ожидаемый результат: {expected:.2f}")
                print(f"Полученный результат: {result:.2f}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
                
                # Проверяем, что разница менее 0.001
                diff = abs(result - expected)
                self.assertLess(diff, 0.001, 
                              f"Разница {diff} больше допустимой 0.001")
                
                # Проверяем временные ограничения (2 секунды)
                self.assertLess(exec_time, 2.0, 
                              f"Время выполнения {exec_time:.2f} сек превышает 2 секунды")

    def test_file_operations(self):
        """Тестирование работы с файлами"""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Пример из условия 1",
                "data": "3 50\n60 20\n100 50\n120 30\n",
                "expected": 180.0
            },
            {
                "name": "Пример из условия 2",
                "data": "1 10\n500 30\n",
                "expected": 500/30*10
            },
            {
                "name": "Пустой рюкзак",
                "data": "3 0\n60 20\n100 50\n120 30\n",
                "expected": 0.0
            },
            {
                "name": "Большие данные",
                "data": "100 500000\n" + 
                       "\n".join(f"{random.randint(1, 10000)} {random.randint(1, 1000)}" 
                                for _ in range(100)),
                "expected": None  # Будет вычислено программно
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nТест {i}: {test['name']}")
            
            # Создаем временные файлы
            input_fd, input_path = tempfile.mkstemp(suffix='.txt', text=True)
            output_fd, output_path = tempfile.mkstemp(suffix='.txt', text=True)
            
            try:
                # Записываем входные данные
                with os.fdopen(input_fd, 'w') as in_file:
                    in_file.write(test['data'])
                os.close(output_fd)
                
                # Вычисляем ожидаемый результат, если он не задан
                if test['expected'] is None:
                    lines = test['data'].strip().split('\n')
                    n, W = map(int, lines[0].split())
                    items = [tuple(map(int, line.split())) for line in lines[1:]]
                    test['expected'] = solve(n, W, items)
                
                # Измеряем время выполнения file_open
                start_time = time.perf_counter()
                result = file_open(input_path, output_path)
                end_time = time.perf_counter()
                exec_time = end_time - start_time
                
                # Проверяем запись в выходной файл
                with open(output_path, 'r') as out_file:
                    file_result = float(out_file.read().strip())
                
                print(f"Входные данные: {test['data'][:50]}..." if len(test['data']) > 50 else f"Входные данные: {test['data']}")
                print(f"Ожидаемый результат: {test['expected']:.4f}")
                print(f"Результат из файла: {file_result:.4f}")
                print(f"Возвращенное значение: {result:.4f}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                
                # Проверяем корректность
                self.assertAlmostEqual(result, test['expected'], places=4)
                self.assertAlmostEqual(file_result, test['expected'], places=4)
                
            finally:
                # Удаляем временные файлы
                os.unlink(input_path)
                os.unlink(output_path)

    def test_memory_efficiency(self):
        """Тестирование эффективности использования памяти"""
        print(f"\n{'ТЕСТИРОВАНИЕ ЭФФЕКТИВНОСТИ ПАМЯТИ':^60}")
        print(f"{'=' * 60}")
        
        # Тест с максимальным n по условию
        n = 1000
        W = 1000000
        
        # Генерируем предметы (избегаем нулевого веса)
        items = [(random.randint(1, 2000000), 
                 random.randint(1, 2000000)) 
                for _ in range(n)]
        
        print(f"\nТест с максимальным n={n}")
        
        # Измеряем память для solve
        result, exec_time, mem_peak = self.measure_performance(
            solve, n, W, items
        )
        
        print(f"Время выполнения: {exec_time:.6f} сек")
        print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
        
        # Оцениваем использование памяти
        # Каждый предмет: tuple из 2 int (16 байт) + overhead
        # В timsort используется O(n) дополнительной памяти
        expected_memory_upper_bound = n * 100  # Оценка сверху в байтах
        self.assertLess(mem_peak, expected_memory_upper_bound * 10,  # С запасом
                       f"Использование памяти {mem_peak} байт кажется чрезмерным")

    def test_precision(self):
        """Тестирование точности вычислений"""
        print(f"\n{'ТЕСТИРОВАНИЕ ТОЧНОСТИ ВЫЧИСЛЕНИЙ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Точное деление (исправленный)",
                "n": 4,
                "W": 10,
                "items": [(1, 3), (1, 3), (1, 3), (1, 3)],
                "expected": 10/3
            },
            {
                "name": "Много предметов",
                "n": 100,
                "W": 100,
                "items": [(1, 1) for _ in range(100)],
                "expected": 100.0
            },
            {
                "name": "Дробные значения - исправленный",
                "n": 3,
                "W": 5,
                "items": [(3, 2), (5, 3), (7, 5)],
                "expected": 8.0  # Исправлено с 8.6666666667 на 8.0
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nТест {i}: {test['name']}")
            
            # Для первого теста вычисляем ожидаемый результат
            if test["name"] == "Точное деление (исправленный)":
                # У нас 4 предмета по (1,3), W=10
                # Берем 3 предмета целиком (вес 9, стоимость 3) и 1/3 от четвертого (вес 1, стоимость 1/3)
                test["expected"] = 3 + 1/3
            
            result, exec_time, mem_peak = self.measure_performance(
                solve, test['n'], test['W'], test['items']
            )
            
            print(f"Ожидаемый результат: {test['expected']}")
            print(f"Полученный результат: {result}")
            print(f"Абсолютная погрешность: {abs(result - test['expected']):.10f}")
            print(f"Относительная погрешность: {abs((result - test['expected'])/test['expected'] if test['expected'] != 0 else 0):.10f}")
            print(f"Время выполнения: {exec_time:.6f} сек")
            
            # Проверяем, что погрешность меньше 1e-3
            self.assertLess(abs(result - test['expected']), 0.001,
                          f"Погрешность {abs(result - test['expected'])} больше 0.001")


if __name__ == '__main__':
    unittest.main(verbosity=2)