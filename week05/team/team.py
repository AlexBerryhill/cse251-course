"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 3
NO_MORE_VALUES = 'No more'

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def read_thread(queue: mp.Queue, filename: str, number_in_queue_sem: mp.Semaphore) -> None:
    if not os.path.exists('data.txt'):
        print('Error the file "data.txt" not found')
        return

    # load dict
    with open('data.txt') as f:
        data = f.read()
        data = data.split('\n')
        data = [int(i) for i in data if i != '']
    
    for i in data:
        queue.put(i)
        number_in_queue_sem.release()
    queue.put(NO_MORE_VALUES)
    number_in_queue_sem.release()
    
    
        

# Create prime_process function
def prime_process(queue: mp.Queue, number_in_queue_sem: mp.Semaphore, primes: list):
    while True:
        number_in_queue_sem.acquire()
        value = queue.get()
        if value == NO_MORE_VALUES:
            print('no more')
            return
        
        if is_prime(value):
            print(f'Found prime: {value}')
            primes.append(value)


def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    # filename = 'data.txt'
    # create_data_txt(filename)
    
    # Create queue and semaphore
    queue = mp.Queue()
    number_in_queue_sem = mp.Semaphore(0)

    # Create shared data structures
    # primes = []
    primes = mp.Manager().list()

    # Create reading thread
    read_t = threading.Thread(target=read_thread, args=(queue, 'data.txt', number_in_queue_sem))
    read_t.start()

    log = Log(show_terminal=True)
    log.start_timer()

    # Create prime processes
    prime_processes = []
    for _ in range(PRIME_PROCESS_COUNT):
        prime_p = mp.Process(target=prime_process, args=(queue, number_in_queue_sem, primes))
        prime_processes.append(prime_p)

    # Start them all
    for prime_p in prime_processes:
        prime_p.start()

    # TODO wait for them to complete
    read_t.join()
    for prime_p in prime_processes:
        prime_p.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()
