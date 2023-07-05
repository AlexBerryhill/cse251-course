"""
Course: CSE 251
Lesson Week: 11
File: team2.py
Author: Brother Comeau

Purpose: Team Activity 2: Queue, Stack

Instructions:

Part 1:
- Create classes for Queue_t and Stack_t that are thread safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple threads.

Part 2
- Create classes for Queue_p and Stack_p that are process safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple processes.

Queue methods:
    - constructor(<no arguments>)
    - size()
    - get()
    - put(item)

Stack methods:
    - constructor(<no arguments>)
    - push(item)
    - pop()

Steps:
1) write the Queue_t and test it with threads.
2) write the Queue_p and test it with processes.
3) Implement Stack_t and test it 
4) Implement Stack_p and test it 

Note: Testing means having lots of concurrency/parallelism happening.  Also
some methods for lists are thread safe - some are not.

"""
import time
import threading
import multiprocessing as mp

# -------------------------------------------------------------------
class Queue_t:
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._queue = []
    
    def size(self):
        return len(self._queue)
    
    def get(self):
        with self._lock:
            if len(self._queue) > 0:
                return self._queue.pop(0)
            return None
    
    def put(self, item):
        with self._lock:
            self._queue.append(item)

# -------------------------------------------------------------------
class Stack_t:
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._stack = []
    
    def pop(self):
        with self._lock:
            if len(self._stack) > 0:
                return self._stack.pop()
            return None

    def push(self, item):
        with self._lock:
            self._stack.append(item)

# -------------------------------------------------------------------
class Queue_p:
    def __init__(self) -> None:
        super().__init__()
        self._lock = mp.Lock()
        self._queue = mp.Manager().Queue()
    
    def size(self):
        return self._queue.qsize()
    
    def get(self):
        with self._lock:
            if self.size() > 0:
                return self._queue.get()
            return None
    
    def put(self, item):
        with self._lock:
            self._queue.put(item)

# -------------------------------------------------------------------
class Stack_p:
    def __init__(self) -> None:
        self._lock = mp.Lock()
        self._stack = mp.Queue()
    
    def push(self, item):
        with self._lock:
            self._stack.put(item)


def main():
    t_queue = Queue_t()
    t_stack = Stack_t()
    p_queue = Queue_p()
    p_stack = Stack_p()

    # test your classes with threads and processes
    t_queue.put(1)


if __name__ == '__main__':
    main()
