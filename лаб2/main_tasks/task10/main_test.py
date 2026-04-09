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

class TestSignatureCollection(unittest.TestCase):

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
                "data": [(1, 3), (2, 5), (3, 6)],
                "expected": (1, [3])
            },
            {
                "name": "Пример 2",
                "data": [(4, 7), (1, 3), (2, 5), (5, 6)],
                "expected": (2, [3, 6])
            },
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"data={test['data']}")
                
                # Измеряем производительность
                result, exec_time, mem_peak = self.measure_performance(solve, test['data'], len(test['data']))
                
                print(f"Ожидаемый результат: {test['expected']}")
                print(f"Полученный результат: {result}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
                
                # Проверка с учетом погрешности
                self.assertEqual(result, test['expected'], msg=f"Ожидалось {test['expected']}, получено {result}")

    def test_edge_cases(self):
        """Тестирование граничных случаев"""
        print(f"\n{'ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Минимальное количество отрезков (n=1)",
                "data": [(1, 3)],
                "expected": (1, [3])
            },
            {
                "name": "Максимальные значения (проверка работы с большими числами)",
                "data": [(0, 10**9), (5*10**8, 10**9), (10**8, 10**9)],
                "expected": (1, [1000000000])  # Все отрезки покрываются точкой 10^9
            },
            {
                "name": "Пересекающиеся отрезки с одной точкой",
                "data": [(1, 5), (2, 6), (3, 7)],
                "expected": (1, [5])  # Все отрезки можно покрыть точкой 5
            },
            # Добавляем тест для худшего случая с 100 отрезками
            {
                "name": "Худший случай с 100 отрезками (отсутствие пересечений)",
                "data": [(i * 10_000_000, i * 10_000_000 + 9_999_999) for i in range(100)],
                "expected": (100, [i * 10_000_000 + 9_999_999 for i in range(100)])  # 100 точек для покрытия 100 отрезков
            },
            # Добавляем тест для среднего случая
            {
                "name": "Средний случай (пересекающиеся отрезки)",
                "data": [(1, 5), (4, 8), (6, 9)],
                "expected": (2, [5, 9])  # Точки, покрывающие пересекающиеся отрезки
            },
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                print(f"data={test['data']}")
                
                # Измеряем производительность
                result, exec_time, mem_peak = self.measure_performance(solve, test['data'], len(test['data']))
                
                print(f"Ожидаемый результат: {test['expected']}")
                print(f"Полученный результат: {result}")
                print(f"Время выполнения: {exec_time:.6f} сек")
                print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
                
                # Проверка с учетом погрешности
                self.assertEqual(result, test['expected'], msg=f"Ожидалось {test['expected']}, получено {result}")

    def test_performance(self):
        """Тестирование производительности для больших данных"""
        print(f"\n{'ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ':^60}")
        print(f"{'=' * 60}")
        
        n = 1000  # Максимальное количество отрезков для теста
        
        # Генерация случайных отрезков
        data = [(random.randint(0, 10**9 - 1), random.randint(0, 10**9)) for _ in range(n)]
        
        print(f"\nТест с {n} отрезками")
        
        # Измеряем производительность
        result, exec_time, mem_peak = self.measure_performance(solve, data, n)
        
        print(f"Время выполнения: {exec_time:.6f} сек")
        print(f"Пиковое использование памяти: {mem_peak/1024:.2f} КБ")
        
        # Проверка временных ограничений (2 сек)
        self.assertLess(exec_time, 2.0, f"Время выполнения {exec_time:.2f} сек превышает 2 секунды")

    def test_file_operations(self):
        """Тестирование работы с файлами"""
        print(f"\n{'ТЕСТИРОВАНИЕ ФАЙЛОВЫХ ОПЕРАЦИЙ':^60}")
        print(f"{'=' * 60}")
        
        test_cases = [
            {
                "name": "Пример 1",
                "data": "4\n4 7\n1 3\n2 5\n5 6\n",  # Исправленный формат
                "expected": (2, [3, 6])
            },
            {
                "name": "Пример 2",
                "data": "4\n1 3\n2 5\n5 6\n7 8\n",  # Формат исправлен
                "expected": (3, [3, 6, 8])
            },
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']}")
                
                # Создаем временные файлы
                input_fd, input_path = tempfile.mkstemp(suffix='.txt', text=True)
                output_fd, output_path = tempfile.mkstemp(suffix='.txt', text=True)
                
                try:
                    # Записываем входные данные
                    with os.fdopen(input_fd, 'w') as in_file:
                        in_file.write(test['data'])
                    os.close(output_fd)
                    
                    # Измеряем время выполнения file_open
                    start_time = time.perf_counter()
                    result = file_open(input_path, output_path)
                    end_time = time.perf_counter()
                    exec_time = end_time - start_time
                    
                    # Проверяем запись в выходной файл
                    with open(output_path, 'r') as out_file:
                        file_result = out_file.read().strip().split('\n')
                        file_result = (int(file_result[0]), list(map(int, file_result[1].split())))
                    
                    print(f"Входные данные: {test['data']}")
                    print(f"Ожидаемый результат: {test['expected']}")
                    print(f"Результат из файла: {file_result}")
                    print(f"Время выполнения: {exec_time:.6f} сек")
                    
                    # Проверяем корректность
                    self.assertEqual(result, test['expected'], msg=f"Ожидалось {test['expected']}, получено {result}")
                    self.assertEqual(file_result, test['expected'], msg=f"Ожидалось {test['expected']}, получено {file_result}")
                finally:
                    # Удаляем временные файлы
                    os.unlink(input_path)
                    os.unlink(output_path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
