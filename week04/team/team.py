"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue​

def retrieve_thread(data_queue, number_in_queue_sem, log):
    """ Process values from the data_queue """

    while True:
        number_in_queue_sem.acquire()

        value = data_queue.get()
        if value == NO_MORE_VALUES:
            return

        response = requests.get(value)

        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            data = response.json()
            log.write(data['name'])
        else:
            log.write(f'ERROR with {value}')


def file_reader(filename, data_queue, number_in_queue_sem, log):
    """ This thread reading the data file and places the values in the data_queue """

    with open(filename) as f:
        for line in f:
            value = line.strip()
            # print(value)
            
            # sem 2
            data_queue.put(value)

            number_in_queue_sem.release()

    log.write('finished reading file')

    # signal all the retrieve threads one more time
    for _ in range(RETRIEVE_THREADS):
        data_queue.put(NO_MORE_VALUES)      # has something to get() from the queue 
        number_in_queue_sem.release()


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # Create shared queue - this is unbounded meaning it can grow big
    data_queue = queue.Queue()

    # This semaphore indicates the number of items in the queue
    # We start with the value of 0 - meaning no items in the queue
    # When the retrieve_thread function tries to acquire() this semaphore
    # it will wait until the file_reader() function adds something to the queue
    number_in_queue_sem = threading.Semaphore(0)

    # create the threads
    reader = threading.Thread(target=file_reader, args=('urls.txt', data_queue, number_in_queue_sem, log))
    workers = []
    for _ in range(RETRIEVE_THREADS):
        workers.append(threading.Thread(target=retrieve_thread, args=(data_queue, number_in_queue_sem, log)))

    log.start_timer()

    # Get them going - The order doesn't matter
    for worker in workers:
        worker.start()
    reader.start()

    # Wait for them to finish - The order doesn't matter
    reader.join()
    for worker in workers:
        worker.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()