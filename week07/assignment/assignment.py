"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Alex Berryhill
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.


"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    result_primes.append(is_prime(value))

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt', 'r') as f:
        for line in f:
            if line.strip() == word:
                result_words.append(f'{word} Found')
                return
        result_words.append(f'***** {word} not found *****')

def task_upper(text) -> str:
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    result_upper.append(text.upper())

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    result_sums.append(sum(range(start_value, end_value + 1)))

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        result_names.append(f'{url} has name {response.text}')
    else:
        result_names.append(f'{url} had an error receiving the information')



def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool = mp.Pool(mp.cpu_count())

    # TODO you can change the following
    # TODO start and wait pools
    threads = []
    
    count = 0
    task_files = glob.glob("*.task")
    print(f'Number of task files: {len(task_files)}')
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            threads.append(pool.apply_async(task_prime, args=(task['value'],)))
            # task_prime(task['value'])
        elif task_type == TYPE_WORD:
            threads.append(pool.apply_async(task_word, args=(task['word'],)))
            # task_word(task['word'])
        elif task_type == TYPE_UPPER:
            threads.append(pool.apply_async(task_upper, args=(task['text'],)))
            # task_upper(task['text'])
        elif task_type == TYPE_SUM:
            threads.append(pool.apply_async(task_sum, args=(task['start'], task['end'],)))
            # task_sum(task['start'], task['end'])
        elif task_type == TYPE_NAME:
            threads.append(pool.apply_async(task_name, args=(task['url'],)))
            # task_name(task['url'])
        else:
            log.write(f'Error: unknown task type {task_type}')

    #wait for all processes to complete
    for thread in threads:
        thread.get()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
