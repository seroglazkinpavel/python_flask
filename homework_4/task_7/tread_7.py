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
import threading
import random
import time

start_time = time.time()
res = [random.randint(1, 100) for _ in range(1000000)]
sum_ = 0
def sum_nunber(num_list):
    global sum_
    for i in num_list:
        sum_ += i

threadings = []

for i in range(10):
    start_index = i * 100000
    end_index = start_index - 100000
    thread = threading.Thread(target=sum_nunber, args=(res[start_index:end_index],))
    threadings.append(thread)
    thread.start()
for tread in threadings:
    tread.join()

print(f"Decision {sum_} in {time.time() - start_time:.2f} seconds")