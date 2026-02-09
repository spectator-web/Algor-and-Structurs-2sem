import unittest
import tracemalloc
import time
import os
import sys
import random
import tempfile

sys.path.append(os.path.dirname(__file__))

from maim import tree_height, file_open

class TestTreeHeight(unittest.TestCase):
    
    def test_case_1_basic_examples(self):
        """Тест 1: Базовые примеры из условия"""
        print("\n" + "="*60)
        print("ТЕСТ 1: Базовые примеры из условия")
        print("="*60)
        
        # Пример 1
        print(f"\nПример 1:")
        print(f"  Вход: n=5, parents=[4, -1, 4, 1, 1]")
        print(f"  Ожидание: 3")
        
        n = 5
        parents = [4, -1, 4, 1, 1]
        result = tree_height(n, parents)
        
        print(f"  Получено: {result}")
        self.assertEqual(result, 3, "Неверная высота для примера 1")
        print(f"  ✓ Тест пройден")
        
        # Пример 2
        print(f"\nПример 2:")
        print(f"  Вход: n=5, parents=[-1, 0, 4, 0, 3]")
        print(f"  Ожидание: 4")
        
        n = 5
        parents = [-1, 0, 4, 0, 3]
        result = tree_height(n, parents)
        
        print(f"  Получено: {result}")
        self.assertEqual(result, 4, "Неверная высота для примера 2")
        print(f"  ✓ Тест пройден")
    
    def test_case_2_small_cases(self):
        """Тест 2: Маленькие деревья"""
        print("\n" + "="*60)
        print("ТЕСТ 2: Маленькие деревья")
        print("="*60)
        
        test_cases = [
            {
                'n': 1,
                'parents': [-1],
                'expected': 1,
                'description': 'Дерево из одного узла (корень)'
            },
            {
                'n': 2,
                'parents': [-1, 0],
                'expected': 2,
                'description': 'Цепочка из 2 узлов'
            },
            {
                'n': 3,
                'parents': [-1, 0, 0],
                'expected': 2,
                'description': 'Дерево с корнем и двумя детьми'
            },
            {
                'n': 4,
                'parents': [-1, 0, 1, 2],
                'expected': 4,
                'description': 'Цепочка из 4 узлов'
            },
            {
                'n': 6,
                'parents': [-1, 0, 0, 1, 1, 0],
                'expected': 3,
                'description': 'Сбалансированное дерево высоты 3'
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nТест {i}: {test['description']}")
            print(f"  Вход: n={test['n']}, parents={test['parents']}")
            print(f"  Ожидание: {test['expected']}")
            
            # Замер времени
            start_time = time.perf_counter()
            result = tree_height(test['n'], test['parents'])
            end_time = time.perf_counter()
            time_taken = end_time - start_time
            
            print(f"  Получено: {result}")
            print(f"  Время: {time_taken:.6f} сек")
            
            self.assertEqual(result, test['expected'],
                           f"Неверная высота для теста {i}")
            
            print(f"  ✓ Тест пройден")
    
    def test_case_3_different_structures(self):
        """Тест 3: Деревья разной структуры"""
        print("\n" + "="*60)
        print("ТЕСТ 3: Деревья разной структуры")
        print("="*60)
        
        # Дерево-звезда: корень и много детей
        n = 1000
        parents = [-1] + [0] * (n - 1)  # Все узлы имеют родителя 0 (кроме корня)
        
        print(f"\nДерево-звезда:")
        print(f"  Вход: n={n}, все узлы кроме корня имеют родителя 0")
        print(f"  Ожидание: 2 (корень и листья)")
        
        start_time = time.perf_counter()
        result = tree_height(n, parents)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        
        print(f"  Получено: {result}")
        print(f"  Время: {time_taken:.6f} сек")
        self.assertEqual(result, 2, "Неверная высота для дерева-звезды")
        print(f"  ✓ Тест пройден")
        
        # Дерево-цепочка (максимальная высота)
        n = 1000
        parents = [-1] + list(range(n - 1))  # Каждый узел имеет родителем предыдущий
        
        print(f"\nДерево-цепочка (линейное дерево):")
        print(f"  Вход: n={n}, цепочка узлов")
        print(f"  Ожидание: {n} (высота равна количеству узлов)")
        
        start_time = time.perf_counter()
        result = tree_height(n, parents)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        
        print(f"  Получено: {result}")
        print(f"  Время: {time_taken:.6f} сек")
        self.assertEqual(result, n, "Неверная высота для дерева-цепочки")
        print(f"  ✓ Тест пройден")
    
    def test_case_4_large_random_data(self):
        """Тест 4: Большие случайные деревья"""
        print("\n" + "="*60)
        print("ТЕСТ 4: Большие случайные деревья")
        print("="*60)
        
        random.seed(42)  # Для воспроизводимости
        
        def generate_random_tree(n):
            """Генерирует случайное дерево с n узлами"""
            parents = [-1]  # Корень
            
            for i in range(1, n):
                # Случайно выбираем родителя из уже созданных узлов
                parent = random.randint(0, i - 1)
                parents.append(parent)
            
            return parents
        
        test_sizes = [1000, 10000, 50000]
        
        for size in test_sizes:
            print(f"\nТест n={size}:")
            print(f"  Генерация случайного дерева из {size} узлов...")
            
            # Генерируем случайное дерево
            parents = generate_random_tree(size)
            
            # Замер времени
            start_time = time.perf_counter()
            result = tree_height(size, parents)
            end_time = time.perf_counter()
            time_taken = end_time - start_time
            
            # Замер памяти
            tracemalloc.start()
            tracemalloc.clear_traces()
            result_mem = tree_height(size, parents)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            memory_mb = peak / 1024 / 1024
            
            print(f"  Высота дерева: {result}")
            print(f"  Время: {time_taken:.4f} сек")
            print(f"  Память: {memory_mb:.2f} МБ")
            
            # Проверяем, что высота в допустимых пределах
            self.assertTrue(1 <= result <= size,
                           f"Высота {result} вне допустимого диапазона для n={size}")
            
            # Проверки производительности
            self.assertLess(time_taken, 2.0,
                          f"Превышено время для n={size}: {time_taken:.2f} сек")
            self.assertLess(memory_mb, 256.0,
                          f"Превышена память для n={size}: {memory_mb:.2f} МБ")
            
            print(f"  ✓ Тест пройден")
    
    def test_case_5_file_operations(self):
        """Тест 5: Работа с файлами"""
        print("\n" + "="*60)
        print("ТЕСТ 5: Работа с файлами")
        print("="*60)
        
        test_cases = [
            {
                'input_data': "5\n4 -1 4 1 1\n",
                'expected_output': "3"
            },
            {
                'input_data': "5\n-1 0 4 0 3\n",
                'expected_output': "4"
            },
            {
                'input_data': "1\n-1\n",
                'expected_output': "1"
            },
            {
                'input_data': "3\n-1 0 0\n",
                'expected_output': "2"
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nТест {i}:")
            print(f"  Входные данные:\n{test['input_data'].strip()}")
            print(f"  Ожидаемый вывод: {test['expected_output']}")
            
            # Создаем временные файлы
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_input.txt') as input_file:
                input_file.write(test['input_data'])
                input_path = input_file.name
            
            output_path = input_path.replace('_input.txt', '_output.txt')
            
            try:
                # Вызываем функцию file_open
                start_time = time.perf_counter()
                result = file_open(input_path, output_path)
                end_time = time.perf_counter()
                time_taken = end_time - start_time
                
                # Читаем результат из файла
                with open(output_path, 'r') as f:
                    file_output = f.read().strip()
                
                print(f"  Вывод в файле: {file_output}")
                print(f"  Возвращенное значение: {result}")
                print(f"  Время: {time_taken:.6f} сек")
                
                # Проверяем результат
                self.assertEqual(file_output, test['expected_output'],
                               f"Неверный вывод в файле для теста {i}")
                self.assertEqual(result, int(test['expected_output']),
                               f"Неверное возвращаемое значение для теста {i}")
                
                print(f"  ✓ Тест пройден")
                
            finally:
                # Удаляем временные файлы
                if os.path.exists(input_path):
                    os.unlink(input_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)
    
    def test_case_6_edge_cases(self):
        """Тест 6: Крайние случаи"""
        print("\n" + "="*60)
        print("ТЕСТ 6: Крайние случаи")
        print("="*60)
        
        test_cases = [
            {
                'name': "Минимальное дерево (1 узел)",
                'n': 1,
                'parents': [-1],
                'expected': 1
            },
            {
                'name': "Максимально несбалансированное дерево (цепочка)",
                'n': 100,
                'parents': [-1] + list(range(99)),
                'expected': 100
            },
            {
                'name': "Полное бинарное дерево (индексация не по уровням)",
                'n': 7,
                'parents': [-1, 0, 0, 1, 1, 2, 2],
                'expected': 3
            },
            {
                'name': "Все узлы независимы от корня (невозможно по условию, но проверяем)",
                'n': 5,
                'parents': [-1, 0, 1, 2, 3],  # Цепочка
                'expected': 5
            },
            {
                'name': "Дерево с отрицательными индексами (за пределами)",
                'n': 3,
                'parents': [-1, 0, -2],  # -2 невалиден
                'should_fail': True
            }
        ]
        
        for test in test_cases:
            print(f"\n{test['name']}:")
            print(f"  Вход: n={test.get('n', 'N/A')}")
            
            if 'should_fail' in test and test['should_fail']:
                print(f"  Ожидание: обработка ошибки")
                # Проверяем, что функция корректно обрабатывает невалидные данные
                try:
                    result = tree_height(test['n'], test['parents'])
                    print(f"  Получено: {result}")
                    # Если дошли сюда, значит функция не упала, что может быть нормально
                    print(f"  ✓ Функция не упала на невалидных данных")
                except Exception as e:
                    print(f"  Исключение: {type(e).__name__}: {e}")
                    print(f"  ✓ Функция обработала ошибку")
            else:
                print(f"  Ожидание: {test['expected']}")
                
                start_time = time.perf_counter()
                result = tree_height(test['n'], test['parents'])
                end_time = time.perf_counter()
                time_taken = end_time - start_time
                
                print(f"  Получено: {result}")
                print(f"  Время: {time_taken:.6f} сек")
                
                self.assertEqual(result, test['expected'],
                               f"Неверная высота для {test['name']}")
                
                print(f"  ✓ Тест пройден")
    
    def test_case_7_performance_stress_test(self):
        """Тест 7: Стресс-тест производительности"""
        print("\n" + "="*60)
        print("ТЕСТ 7: Стресс-тест производительности")
        print("="*60)
        
        print(f"\nМаксимальные ограничения (n=10^5):")
        
        # Тест 1: Дерево-цепочка (максимальная высота)
        n = 100000
        print(f"\n1. Дерево-цепочка из {n} узлов:")
        print(f"  Генерация цепочки...")
        
        parents = [-1] + list(range(n - 1))
        
        # Замер времени
        print(f"  Запуск алгоритма...")
        start_time = time.perf_counter()
        result = tree_height(n, parents)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        
        # Замер памяти
        tracemalloc.start()
        tracemalloc.clear_traces()
        result_mem = tree_height(n, parents)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        memory_mb = peak / 1024 / 1024
        
        print(f"  Высота: {result}")
        print(f"  Время: {time_taken:.4f} сек")
        print(f"  Память: {memory_mb:.2f} МБ")
        
        # Проверки производительности
        self.assertLess(time_taken, 3.0,
                       f"Превышено время 3 секунд: {time_taken:.2f} сек")
        self.assertLess(memory_mb, 512.0,
                       f"Превышена память 512 МБ: {memory_mb:.2f} МБ")
        
        # Проверка корректности
        self.assertEqual(result, n,
                        f"Неверная высота для цепочки: ожидалось {n}, получено {result}")
        
        print(f"  ✓ Тест пройден (в пределах ограничений)")
        
        # Тест 2: Дерево-звезда (минимальная высота для большого n)
        print(f"\n2. Дерево-звезда из {n} узлов:")
        print(f"  Генерация звезды...")
        
        parents = [-1] + [0] * (n - 1)
        
        # Замер времени
        print(f"  Запуск алгоритма...")
        start_time = time.perf_counter()
        result = tree_height(n, parents)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        
        print(f"  Высота: {result}")
        print(f"  Время: {time_taken:.4f} сек")
        
        self.assertEqual(result, 2,
                        f"Неверная высота для звезды: ожидалось 2, получено {result}")
        
        print(f"  ✓ Тест пройден")
        
        # Тест 3: Случайное дерево
        print(f"\n3. Случайное дерево из {n} узлов:")
        print(f"  Генерация случайного дерева...")
        
        # Генерируем случайное дерево
        random.seed(12345)
        parents = [-1]
        for i in range(1, n):
            parent = random.randint(0, i - 1)
            parents.append(parent)
        
        # Замер времени
        print(f"  Запуск алгоритма...")
        start_time = time.perf_counter()
        result = tree_height(n, parents)
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        
        print(f"  Высота: {result}")
        print(f"  Время: {time_taken:.4f} сек")
        
        # Проверяем, что высота в допустимых пределах
        self.assertTrue(1 <= result <= n,
                       f"Высота {result} вне допустимого диапазона 1..{n}")
        
        print(f"  ✓ Тест пройден")

def run_all_tests():
    """Запускает все тесты с красивым выводом"""
    print("\n" + "="*60)
    print("НАЧАЛО ТЕСТИРОВАНИЯ: ВЫСОТА ДЕРЕВА")
    print("="*60)
    
    # Инициализируем случайные числа для воспроизводимости
    random.seed(42)
    
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты в правильном порядке
    suite.addTest(TestTreeHeight('test_case_1_basic_examples'))
    suite.addTest(TestTreeHeight('test_case_2_small_cases'))
    suite.addTest(TestTreeHeight('test_case_3_different_structures'))
    suite.addTest(TestTreeHeight('test_case_4_large_random_data'))
    suite.addTest(TestTreeHeight('test_case_5_file_operations'))
    suite.addTest(TestTreeHeight('test_case_6_edge_cases'))
    suite.addTest(TestTreeHeight('test_case_7_performance_stress_test'))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=0)
    
    total_start = time.perf_counter()
    result = runner.run(suite)
    total_end = time.perf_counter()
    
    print("\n" + "="*60)
    print("РЕЗЮМЕ ТЕСТИРОВАНИЯ")
    print("="*60)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Общее время выполнения тестов: {total_end - total_start:.2f} секунд")
    print("="*60)
    
    if result.failures:
        print("\nПРОБЛЕМНЫЕ ТЕСТЫ:")
        for test, trace in result.failures:
            print(f"\n{test}:")
            print(trace)
    
    return result

if __name__ == '__main__':
    result = run_all_tests()
    sys.exit(0 if result.wasSuccessful() else 1)