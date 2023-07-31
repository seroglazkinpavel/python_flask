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
import asyncio
from random import randint
import time

arr = [randint(1, 100) for _ in range(1_000_000)]
sum = 0

async def sum_number(arr, start_idx, end_idx):
    local_sum = 0
    for i in range(start_idx, end_idx):
        local_sum += arr[i]
    return local_sum



async def main():
    global sum
    tasks = []
    num_tasks = 4
    for i in range(num_tasks):
        start_idx = i * len(arr) // num_tasks
        end_idx = (i + 1) * len(arr) // num_tasks
        task = asyncio.create_task(sum_number(arr, start_idx, end_idx))
        tasks.append(task)
    for task in tasks:
        sum += await task
    return sum

start_time = time.time()
if __name__ == '__main__':
    asyncio.run(main())

    print(f"Decision {sum} in {time.time() - start_time:.2f} seconds")