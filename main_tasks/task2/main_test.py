import unittest
import time
import random
import tempfile
import os
import tracemalloc

# Импортируем solve и file_open
from main_tasks.task2.maim import solve, file_open  # Импортируем solve и file_open

class TestTravel(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        tracemalloc.clear_traces()  # Очищаем информацию о памяти перед каждым тестом

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
                "d": 950,
                "m": 400,
                "n": 4,
                "stops": [200, 375, 550, 750],
                "expected": 2
            },
            {
                "name": "Пример 2",
                "d": 10,
                "m": -1,
                "n": 3,
                "stops": [4, 1, 2, 5, 9],
                "expected": -1
            },
            {
                "name": "Пример 3",
                "d": 200,
                "m": 250,
                "n": 2,
                "stops": [100, 150],
                "expected": 0
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"d={test['d']}, m={test['m']}, stops={test['stops'][:3]}...")
                
                # Измеряем время и память
                result, exec_time, mem_peak = self.measure_performance(
                    solve, test['d'], test['m'], test['n'], test['stops']
                )
                
                print(f"Ожидаемый результат: {test['expected']}")
                print(f"Полученный результат: {result}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
                
                # Проверка с учетом погрешности
                self.assertEqual(result, test['expected'])

    def test_edge_cases(self):
        """Тестирование граничных случаев"""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Максимальные значения (d=10^5)",
                "d": 10**5,
                "m": 400,
                "n": 300,
                "stops": [i * 400 for i in range(1, 301)],
                "expected": 249
            },
            {
                "name": "Минимальные значения",
                "d": 1,
                "m": 1,
                "n": 0,
                "stops": [],
                "expected": 0
            },
            {
                "name": "Невозможный путь, слишком большие расстояния",
                "d": 10**5,
                "m": 100,
                "n": 300,
                "stops": [i * 500 for i in range(1, 301)],
                "expected": -1
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"d={test['d']}, m={test['m']}, stops={test['stops'][:3]}...")
                
                # Измеряем время и память
                result, exec_time, mem_peak = self.measure_performance(
                    solve, test['d'], test['m'], test['n'], test['stops']
                )
                
                print(f"Ожидаемый результат: {test['expected']}")
                print(f"Полученный результат: {result}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
                
                # Проверка с учетом погрешности
                self.assertEqual(result, test['expected'])

    def test_random_cases(self):
        """Тестирование на случайных данных"""
        print(f"\n{'ТЕСТИРОВАНИЕ НА СЛУЧАЙНЫХ ДАННЫХ':^60}")
        print(f"{'=' * 60}")
        
        sizes = [10, 100, 500, 1000]  # До максимального n по условию
        
        for size in sizes:
            print(f"\nТест с размером n={size}")
            
            stops = sorted(random.sample(range(1, 10**5), size))
            d = random.randint(max(stops) + 100, 10**5) if max(stops) + 100 <= 10**5 else 10**5
            m = random.randint(1, 400)
            
            # Измеряем время и память
            result, exec_time, mem_peak = self.measure_performance(
                solve, d, m, size, stops
            )
            
            print(f"Результат: {result}")
            print(f"Время выполнения: {exec_time:.6f} сек")
            print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")

            # Проверяем временные ограничения (2 секунды)
            self.assertLess(exec_time, 2.0, f"Время выполнения {exec_time:.2f} сек превышает 2 секунды")


    def test_file_operations(self):
        """Тестирование работы с файлами"""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Пример из условия 1",
                "data": "950\n400\n4\n200 375 550 750\n",
                "expected": 2
            },
            {
                "name": "Пример из условия 2",
                "data": "10\n-1\n3\n4 1 2 5 9\n",
                "expected": -1
            },
            {
                "name": "Пример 3",
                "data": "200\n250\n2\n100 150\n",
                "expected": 0
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nТест {i}: {test['name']}")
            
            input_fd, input_path = tempfile.mkstemp(suffix='.txt', text=True)
            output_fd, output_path = tempfile.mkstemp(suffix='.txt', text=True)
            
            try:
                with os.fdopen(input_fd, 'w') as in_file:
                    in_file.write(test['data'])
                os.close(output_fd)
                
                start_time = time.perf_counter()
                result = file_open(input_path, output_path)
                end_time = time.perf_counter()
                exec_time = end_time - start_time
                
                with open(output_path, 'r') as out_file:
                    file_result = int(out_file.read().strip())
                
                print(f"Входные данные: {test['data'][:50]}..." if len(test['data']) > 50 else f"Входные данные: {test['data']}")
                print(f"Ожидаемый результат: {test['expected']}")
                print(f"Результат из файла: {file_result}")
                print(f"Возвращенное значение: {result}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                # Memory measurement removed – not critical for this functional test
                
                self.assertEqual(result, test['expected'])
                self.assertEqual(file_result, test['expected'])
                
            finally:
                os.unlink(input_path)
                os.unlink(output_path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
