"""
Course: CSE 251
Lesson Week: 09
File: team1.py

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

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat (the % operator helps)
"""

import time
import threading
import random as rand

PHILOSOPHERS = 5
MAX_MEALS_EATEN = PHILOSOPHERS * 5

class Philosopher(threading.Thread):
    def __init__(self, name, forks):
        threading.Thread.__init__(self)
        self.name:int = int(name) # philosopher number
        self.forks = forks # list of locks
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
        self.forks[int(self.name)].acquire()
        self.forks[(int(self.name) + 1) % PHILOSOPHERS].acquire()

    def put_forks(self):
        self.forks[int(self.name)].release()
        self.forks[(int(self.name) + 1) % PHILOSOPHERS].release()

    def print_status(self, status):
        print(f'{self.name} {status} {self.meals_eaten} meals')

def main():
    # create the forks
    forks = [threading.Lock() for i in range(PHILOSOPHERS)]
    # create PHILOSOPHERS philosophers
    philosophers = [Philosopher(i, forks) for i in range(PHILOSOPHERS)]
    #Start them eating and thinking
    for p in philosophers:
        p.start()
    
    # Wait for all the philosophers to finish
    for p in philosophers:
        p.join()
    
    # Display how many times each philosopher ate
    for p in philosophers:
        p.print_status('ate')

    pass

if __name__ == '__main__':
    main()
