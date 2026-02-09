import unittest
import tracemalloc
import time
import tempfile
import os
import sys
import random

sys.path.append(os.path.dirname(__file__))
from maim import file_open  # Импортируем только то, что нужно для файловых операций


def insertion_sort_numbers(arr, left, right):
    """Insertion sort для чисел (по возрастанию)"""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_numbers(arr, left, mid, right):
    """Merge для чисел (по возрастанию)"""
    n1 = mid - left + 1
    n2 = right - mid
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def timsort_numbers(arr):
    """Timsort для чисел (по возрастанию)"""
    n = len(arr)
    min_run = 32
    
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort_numbers(arr, start, end)
    
    size = min_run
    while size < n:
        for start in range(0, n, 2 * size):
            mid = min(n - 1, start + size - 1)
            end = min((start + 2 * size - 1), n - 1)
            if mid < end:
                merge_numbers(arr, start, mid, end)
        size *= 2
    
    return arr


class TestSorts(unittest.TestCase):

    def setUp(self):
        random.seed(42)
    
    def measure_performance(self, sort_func, arr, *args):
        """Измерение времени и памяти для функции сортировки"""
        arr_copy = arr.copy()
        start_time = time.perf_counter()
        result = sort_func(arr_copy, *args)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        arr_copy2 = arr.copy()
        tracemalloc.start()
        sort_func(arr_copy2, *args)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return result, execution_time, peak
    
    def generate_small_medium_tests(self):
        """Генерация тестов для небольших и средних массивов (до 1000 элементов)"""
        test_cases = []
        
        # Базовые тесты
        base_tests = [
            {"name": "Empty array", "input": [], "expected": []},
            {"name": "Single element", "input": [42], "expected": [42]},
            {"name": "Two elements", "input": [2, 1], "expected": [1, 2]},
            {"name": "Small array", "input": [31, 41, 59, 26, 41, 58], 
             "expected": [26, 31, 41, 41, 58, 59]}
        ]
        
        # Средние тесты (до 1000 элементов)
        sizes = [100, 500, 1000]
        
        for size in sizes:
            # Наихудший случай
            worst_case = list(range(size, 0, -1))
            test_cases.append({
                "name": f"Reversed {size}",
                "input": worst_case,
                "expected": sorted(worst_case)
            })
            
            # Случайный массив
            random_case = [random.randint(-1000, 1000) for _ in range(size)]
            test_cases.append({
                "name": f"Random {size}",
                "input": random_case,
                "expected": sorted(random_case)
            })
        
        return base_tests + test_cases
    
    def generate_large_tests(self):
        """Генерация тестов для больших массивов"""
        test_cases = []
        sizes = [5000, 10000, 50000, 100000]
        
        for size in sizes:
            # Наихудший случай
            worst_case = list(range(size, 0, -1))
            test_cases.append({
                "name": f"Reversed {size}",
                "input": worst_case,
                "expected": sorted(worst_case)
            })
            
            # Случайный массив
            random_case = [random.randint(-10000, 10000) for _ in range(size)]
            test_cases.append({
                "name": f"Random {size}",
                "input": random_case,
                "expected": sorted(random_case)
            })
        
        # Добавлен специальный тест для больших чисел
        large_numbers = [random.randint(10**7, 10**9) for _ in range(100000)]
        test_cases.append({
            "name": "Large numbers 10^5",
            "input": large_numbers,
            "expected": sorted(large_numbers)
        })
        
        return test_cases
    
    def test_small_medium_comparison(self):
        """Сравнение Insertion Sort и Merge Sort на малых и средних данных"""
        test_cases = self.generate_small_medium_tests()
        
        print(f"\n{'СРАВНЕНИЕ INSERTION SORT И MERGE SORT':^60}")
        print(f"{'=' * 60}")
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']} (размер: {len(test['input'])})")
                
                input_preview = str(test['input'][:5]) + "..." if len(test['input']) > 5 else str(test['input'])
                
                # Insertion Sort
                if test['input']:  # Не тестируем пустой массив для insertion_sort с индексами
                    result_ins, time_ins, mem_ins = self.measure_performance(
                        insertion_sort_numbers, test['input'], 0, len(test['input']) - 1
                    )
                    output_preview_ins = str(result_ins[:5]) + "..." if len(result_ins) > 5 else str(result_ins)
                    print(f"Insertion Sort - Выход: {output_preview_ins}, Время: {time_ins:.6f} сек, Память: {mem_ins/1024:.2f} КБ")
                else:
                    result_ins = []
                    print(f"Insertion Sort - Выход: [], Время: 0 сек, Память: 0 КБ")
                
                # Merge Sort
                result_merge, time_merge, mem_merge = self.measure_performance(
                    timsort_numbers, test['input']
                )
                output_preview_merge = str(result_merge[:5]) + "..." if len(result_merge) > 5 else str(result_merge)
                print(f"Merge Sort - Выход: {output_preview_merge}, Время: {time_merge:.6f} сек, Память: {mem_merge/1024:.2f} КБ")
                
                print(f"Вход: {input_preview}")
                
                # Проверка корректности
                self.assertEqual(result_ins, test['expected'], "Insertion Sort: неверный результат")
                self.assertEqual(result_merge, test['expected'], "Merge Sort: неверный результат")
    
    def test_large_merge_sort(self):
        """Тестирование Merge Sort на больших данных"""
        test_cases = self.generate_large_tests()
        
        print(f"\n{'ТЕСТИРОВАНИЕ MERGE SORT НА БОЛЬШИХ ДАННЫХ':^60}")
        print(f"{'=' * 60}")
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test=test["name"]):
                print(f"\nТест {i}: {test['name']} (размер: {len(test['input'])})")
                
                input_preview = str(test['input'][:5]) + "..." if len(test['input']) > 5 else str(test['input'])
                
                # Merge Sort
                result_merge, time_merge, mem_merge = self.measure_performance(
                    timsort_numbers, test['input']
                )
                output_preview_merge = str(result_merge[:5]) + "..." if len(result_merge) > 5 else str(result_merge)
                
                # Упрощенный вывод
                print(f"Вход: {input_preview}")
                print(f"Выход: {output_preview_merge}")
                print(f"Время: {time_merge:.6f} сек")
                print(f"Память: {mem_merge/1024:.2f} КБ")
                
                # Проверка корректности
                self.assertEqual(result_merge, test['expected'], "Merge Sort: неверный результат")
    
    def test_edge_cases(self):
    """Тестирование граничных случаев для задачи о грабителе."""
    
    # Тест с минимальным значением для n
    test_case_min_n = {
        "name": "Minimum n",
        "data": "1 10\n500 30\n",  # Один предмет
        "expected": 166.6667
    }

    # Тест с максимальным значением для n
    max_n = 1000  # Максимум по условию
    test_case_max_n = {
        "name": "Maximum n",
        "data": f"{max_n} {2 * 10**6}\n" + "\n".join(f"{random.randint(0, 2 * 10**6)} {random.randint(0, 2 * 10**6)}" for _ in range(max_n)),
        "expected": "Проверить вручную или с помощью заранее известного значения"
    }

    # Тест с максимальной вместимостью рюкзака W
    test_case_max_W = {
        "name": "Maximum W",
        "data": "3 2000000\n60 20\n100 50\n120 30\n",  # Тест с очень большим W
        "expected": 180.0
    }

    # Тест с максимальной стоимостью и весом предметов
    test_case_max_p_w = {
        "name": "Maximum p and w",
        "data": "2 1000000\n2000000 1000000\n2000000 1000000\n",  # Два предмета с максимальными p и w
        "expected": 2000000.0
    }

    # Добавляем в список
    edge_cases = [
        test_case_min_n,
        test_case_max_n,
        test_case_max_W,
        test_case_max_p_w
    ]
    
    # Запуск тестов
    for test in edge_cases:
        print(f"\n{test['name']}")
        
        # Создаем временные файлы для входных и выходных данных
        input_fd, input_path = tempfile.mkstemp(suffix='.txt', text=True)
        output_fd, output_path = tempfile.mkstemp(suffix='.txt', text=True)
        
        try:
            with os.fdopen(input_fd, 'w') as in_file:
                in_file.write(test['data'])
            os.close(output_fd)
            
            start_time = time.perf_counter()
            result_file = file_open(input_path, output_path)
            end_time = time.perf_counter()
            time_file = end_time - start_time
            
            print(f"Входные данные: {test['data'].strip()}")
            print(f"Результат: {result_file}")
            print(f"Время: {time_file:.6f} сек")
            
            # Проверка с учетом погрешности для float
            self.assertAlmostEqual(result_file, test['expected'], places=4, 
                                  msg=f"Ожидалось {test['expected']}, получено {result_file}")
        
        finally:
            os.unlink(input_path)
            os.unlink(output_path)
    
    
    
    def test_file_operations(self):
        """Тестирование работы с файлами (задача о грабителе)"""
        print(f"\n{'ТЕСТИРОВАНИЕ РАБОТЫ С ФАЙЛАМИ':^60}")
        print(f"{'=' * 60}")
        
        # Создаем тестовые данные для задачи о рюкзаке
        test_cases = [
            {
                "name": "Small knapsack",
                "data": "3 50\n60 20\n100 50\n120 30\n",
                "expected": 180.0
            },
            {
                "name": "Medium knapsack", 
                "data": "1 10\n500 30\n",
                "expected": 166.6667  # Примерное значение
            }
        ]
        
        for test in test_cases:
            print(f"\n{test['name']}")
            
            input_fd, input_path = tempfile.mkstemp(suffix='.txt', text=True)
            output_fd, output_path = tempfile.mkstemp(suffix='.txt', text=True)
            
            try:
                with os.fdopen(input_fd, 'w') as in_file:
                    in_file.write(test['data'])
                os.close(output_fd)
                
                start_time = time.perf_counter()
                result_file = file_open(input_path, output_path)
                end_time = time.perf_counter()
                time_file = end_time - start_time
                
                print(f"Входные данные: {test['data'].strip()}")
                print(f"Результат: {result_file}")
                print(f"Время: {time_file:.6f} сек")
                
                # Проверка с учетом погрешности для float
                self.assertAlmostEqual(result_file, test['expected'], places=4, 
                                      msg=f"Ожидалось {test['expected']}, получено {result_file}")
                
            finally:
                os.unlink(input_path)
                os.unlink(output_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)