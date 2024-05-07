from multiprocessing import Pool, Process, cpu_count, current_process
from time import time



def factorize(*number):
    factors_list = []
    #print(number)
    for num in number:
        #print(num)
        factors = []
        if type(num) is int: 
            for i in range(1, num + 1):
                if num % i == 0:
                    factors.append(i)
            factors_list.append(factors)
    return factors_list


if __name__ == '__main__':
    print(cpu_count())

    # Вимірюємо час виконання синхронної версії
    start_time = time()
    result_sync = factorize(128, 255, 99999, 10651060)
    end_time = time()
    print("Sync execution time:", end_time - start_time)


    # Вимірюємо час виконання паралельної версії 1 процес
    proces = Process(target=factorize, args=(128, 255, 99999, 10651060))

    start_time = time()
    proces.start()
    proces.join()
    proces.close()
    end_time = time()
    print("Time of parallel execution of one process:", end_time - start_time)


    # Вимірюємо час виконання паралельної версії декілька процесів
    number = [128, 255, 99999, 10651060]
    processes = []
    for num in range(len(number)):
        pr = Process(target=factorize, args=(number[num],))
        processes.append(pr)

    start_time = time()
    [process.start() for process in processes]
    [process.join() for process in processes]
    [process.close() for process in processes]
    end_time = time()
    print("Time of parallel execution of many process:", end_time - start_time)

    # a, b, c, d  = factorize(128, 255, 99999, 10651060)

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
