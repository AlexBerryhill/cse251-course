"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: <Your name>

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier
- Do not use try...except statements
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')
    
    def __str__(self) -> str:
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, CARS_TO_PRODUCE, log, car_queue, number_in_queue_sem, empty_slot_sem, factory_stats, factory_id, factory_barrier):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        super().__init__(daemon=True)
        self.log = log
        self.CARS_TO_PRODUCE = CARS_TO_PRODUCE
        self.car_queue = car_queue
        self.number_in_queue_sem = number_in_queue_sem
        self.empty_slot_sem = empty_slot_sem
        self.factory_stats = factory_stats
        self.factory_id = factory_id
        self.factory_barrier = factory_barrier

    def run(self):
        for i in range(self.CARS_TO_PRODUCE):
            # TODO Add you code here
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
            """
            car = Car()
            self.empty_slot_sem.acquire()
            self.car_queue.put(car)
            self.number_in_queue_sem.release()

            self.factory_stats[self.factory_id] += 1
            print(f'Factory: {i} cars created')
        
        # signal the dealer that there there are not more cars to create
        self.factory_barrier.wait()
        
        self.empty_slot_sem.acquire()
        self.car_queue.put(None)
        self.number_in_queue_sem.release()
        print('Factory: No more cars to create')



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, log, car_queue, number_in_queue_sem, empty_slot_sem, dealer_stats, dealer_id):
        # Pass all of data that 1 Dealer needs
        # to sell a car
        super().__init__(daemon=True)
        self.log = log
        self.car_queue = car_queue
        self.number_in_queue_sem = number_in_queue_sem
        self.empty_slot_sem = empty_slot_sem
        self.dealer_stats = dealer_stats
        self.dealer_id = dealer_id

    def run(self):
        while True:
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            self.number_in_queue_sem.acquire()
            car = self.car_queue.get()
            self.empty_slot_sem.release()

            if car is None:
                self.empty_slot_sem.acquire()
                self.car_queue.put(None)
                self.number_in_queue_sem.release()
                print('Dealer: No more cars to sell')
                break
            
            self.dealer_stats[self.dealer_id] += 1
            print(f'Dealer: {car} sold')

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
        print('Dealer: Dealer is closed')

def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """
    
    log.write(f'Running production with {factory_count} factories and {dealer_count} dealerships\n')

    # TODO Create semaphore(s)
    number_in_queue_sem = threading.Semaphore(0)
    empty_slot_sem = threading.Semaphore(MAX_QUEUE_SIZE)

    # TODO Create queue251 
    car_queue = Queue251()
    car_queue.max_size = MAX_QUEUE_SIZE
    # TODO Create lock(s) if needed
    # TODO Create barrier
    factory_barrier = threading.Barrier(factory_count)

    # This is used to track the number of cars receives by each dealer
    
    dealer_stats = list([0] * dealer_count)
    factory_stats = list([0] * factory_count)

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factories = []
    for factory in range(factory_count):
        CARS_TO_CREATE_PER_FACTORY = random.randint(100, 300)
        factories.append(Factory(CARS_TO_CREATE_PER_FACTORY, log, car_queue, number_in_queue_sem, empty_slot_sem, factory_stats, factory_id=factory, factory_barrier=factory_barrier))

    # TODO create your dealerships
    dealerships = []
    for dealer in range(dealer_count):
        dealerships.append(Dealer(log, car_queue, number_in_queue_sem, empty_slot_sem, dealer_stats, dealer_id=dealer))

    log.start_timer()

    # TODO Start all dealerships
    for dealership in dealerships:
        dealership.start()

    # TODO Start all factories
    for factory in factories:
        factory.start()

    # TODO Wait for factories and dealerships to complete
    for factory in factories:
        factory.join()
    print('All factories are closed')
    for dealership in dealerships:
        dealership.join()
    print('All dealerships are closed')

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


