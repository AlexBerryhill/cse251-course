"""
Course: CSE 251
Lesson Week: 09
File: team2.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- This is the same problem as last team activity.  However, you will implement a waiter.  
  When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be a issue picking up the two forks since the waiter is in control of 
  the forks and when philosophers eat.  When a philosopher is finished eating, it will 
  informs the waiter that he/she is finished.  If the waiter indicates to a philosopher
  that they can not eat, the philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- When a philosopher is not eating, it will think for 3 to 5 seconds.
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat
"""

import time
import threading
import random as rand

PHILOSOPHERS = 5
MAX_MEALS_EATEN = PHILOSOPHERS * 5

class Philosopher(threading.Thread):
    def __init__(self, name, waiter):
        threading.Thread.__init__(self)
        self.name:int = int(name) # philosopher number
        self.waiter = waiter # list of locks
        self.meals_eaten = 0

    def run(self):
        for i in range(MAX_MEALS_EATEN):
            # self.print_status('is thinking')
            self.think()
            # self.print_status('is hungry')
            self.get_forks()
            self.eat()
            self.print_status('finished eating')
            self.meals_eaten += 1
            self.put_forks()
            # self.print_status('is thinking')
            self.think()

    def eat(self):
        time.sleep(rand.randint(1, 3))
    
    def think(self):
        time.sleep(rand.randint(1, 3))

    def get_forks(self):
        self.waiter.can_eat(self)

    def put_forks(self):
        self.waiter.finished_eating(self)

    def print_status(self, status):
        print(f'{self.name} {status} {self.meals_eaten} meals')

class Waiter():
    def __init__(self, forks):
        self.forks = forks
        self.lock = threading.Lock()

    def can_eat(self, philosopher):
        with self.lock:
            left = self.forks[philosopher.name]
            right = self.forks[(philosopher.name + 1) % PHILOSOPHERS]
            if left.locked() or right.locked():
                return False
            else:
                return True
    
    def finished_eating(self, philosopher):
        with self.lock:
            philosopher.meals_eaten += 1
            left = self.forks[philosopher.name]
            right = self.forks[(philosopher.name + 1) % PHILOSOPHERS]
            left.release()
            right.release()

def main():
    forks = [threading.Lock() for i in range(PHILOSOPHERS)]
    # Create the waiter (A class would be best here)
    waiter = Waiter(forks)
    # TODO - create the forks
    # create PHILOSOPHERS philosophers
    philosophers = [Philosopher(i, waiter) for i in range(PHILOSOPHERS)]
    # Start them eating and thinking
    for philosopher in philosophers:
        philosopher.start()
    
    # TODO - Wait for all the philosophers to finish
    for philosopher in philosophers:
        philosopher.join()

    # TODO - Display how many times each philosopher ate
    for philosopher in philosophers:
        print(f'Philosopher {philosopher.name} ate {philosopher.meals_eaten} meals')


if __name__ == '__main__':
    main()
