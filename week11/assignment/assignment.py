"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE = 'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE = 'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(room_access, cleaned_count, start_time):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room if it is empty or no guests are inside
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    # start = time.time()
    while time.time() - start_time < TIME:
        cleaner_waiting()

        # with party_population:
        #     if party_population.value == 0:
        room_access.acquire()

        print(STARTING_CLEANING_MESSAGE, flush=True)

        cleaner_cleaning(random.randint(1, CLEANING_STAFF))

        print(STOPPING_CLEANING_MESSAGE, flush=True)

        room_access.release()

        cleaned_count.value += 1

def guest(party_population, room_access, party_count, start_time):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room if it is empty or contains other guests
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving the room
    """
    # start = time.time()
    while time.time() - start_time < TIME:
        guest_waiting()

        with party_population:
            party_population.value += 1

            if party_population.value == 1:
                room_access.acquire()
                if party_population.value != 1:
                    print('ERROR: party_population.value != 1')
                print(STARTING_PARTY_MESSAGE, flush=True)
                
            guest_partying(random.randint(1, HOTEL_GUESTS), party_population.value)

        with party_population:
            party_population.value -= 1
            if party_population.value == 0:
                print(STOPPING_PARTY_MESSAGE, flush=True)
                party_count.value += 1
                room_access.release()
                
def main():
    # Start time of the running of the program.
    start_time = time.time()

    # Add any variables, data structures, processes you need
    room_access = mp.Lock()

    cleaned_count = mp.Value('i', 0)

    party_count = mp.Value('i', 0)

    party_population = mp.Value('i', 0)

    cleaner_processes = []

    # Add any arguments to cleaner() and guest() that you need
    for _ in range(CLEANING_STAFF):
        p = mp.Process(target=cleaner, args=(room_access, cleaned_count, start_time))
        p.start()
        cleaner_processes.append(p)

    guest_processes = []
    for _ in range(HOTEL_GUESTS):
        p = mp.Process(target=guest, args=(party_population, room_access, party_count, start_time))
        p.start()
        guest_processes.append(p)

    # Wait for all processes to finish
    for p in cleaner_processes:
        p.join()

    for p in guest_processes:
        p.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties', flush=True)

if __name__ == '__main__':
    main()
