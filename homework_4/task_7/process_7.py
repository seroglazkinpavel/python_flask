"""
Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
� Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
� Массив должен быть заполнен случайными целыми числами
от 1 до 100.
� При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
� В каждом решении нужно вывести время выполнения
вычислений.
"""

import random
import time
import multiprocessing

start_time = time.time()
res = [random.randint(1, 100) for _ in range(1000000)]
sum_ = multiprocessing.Value('i', 0)
def sum_nunber(num_list, sum_):
    for i in num_list:
        with sum_.get_lock():
            sum_.value += i

if __name__ == '__main__':
    processes = []
    for i in range(10):
        start_index = i * 100000
        end_index = start_index - 100000
        process = multiprocessing.Process(target=sum_nunber, args=(res[start_index:end_index], sum_))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

    print(f"Decision {sum_.value} in {time.time() - start_time:.2f} seconds")