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

def cleaner(room_access, cleaned_count):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    start = time.time()
    while time.time() - start < TIME:
        cleaner_waiting()

        # Get access to the room
        room_access.acquire()

        print(STARTING_CLEANING_MESSAGE)

        cleaner_cleaning(random.randint(1, CLEANING_STAFF))

        print(STOPPING_CLEANING_MESSAGE)

        # Release the room
        room_access.release()

        cleaned_count.value += 1

def guest(room_access, cleaned_count, party_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    start = time.time()
    while time.time() - start < TIME:
        guest_waiting()

        # Get access to the room
        room_access.acquire()

        if cleaned_count.value == 0:
            print(STARTING_PARTY_MESSAGE)

        guest_partying(random.randint(1, HOTEL_GUESTS), cleaned_count.value)

        if cleaned_count.value == CLEANING_STAFF:
            print(STOPPING_PARTY_MESSAGE)

        # Release the room
        room_access.release()

        party_count.value += 1

def main():
    # Start time of the running of the program.
    start_time = time.time()

    # Create a Lock to control room access
    room_access = mp.Lock()

    # Create a Value to track the number of times the room was cleaned
    cleaned_count = mp.Value('i', 0)

    # Create a Value to track the number of parties
    party_count = mp.Value('i', 0)



    # Create a list to store the cleaner processes
    cleaner_processes = []

    # Create cleaner processes
    for _ in range(CLEANING_STAFF):
        p = mp.Process(target=cleaner, args=(room_access, cleaned_count))
        p.start()
        cleaner_processes.append(p)

    # Create guest processes
    for _ in range(HOTEL_GUESTS):
        p = mp.Process(target=guest, args=(room_access, cleaned_count, party_count))
        p.start()

    # Wait for all cleaner processes to finish
    for p in cleaner_processes:
        p.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')

if __name__ == '__main__':
    main()
