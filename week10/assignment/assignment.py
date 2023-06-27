"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Alex Berryhill

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def writer_process(shared_list, lock, empty_spots, filled_spots, items_to_send, writer_id):
  start_value = writer_id * (items_to_send // WRITERS) + 1
  end_value = start_value + (items_to_send // WRITERS) - 1
  for value in range(start_value, end_value + 1):
    empty_spots.acquire()  
    lock.acquire()
    write_index = shared_list[-2] % BUFFER_SIZE
    shared_list[write_index] = value
    shared_list[-2] += 1
    lock.release()
    filled_spots.release()

def reader_process(shared_list, lock, empty_spots, filled_spots, items_to_receive, reader_id):
  received_values = 0
  while received_values < items_to_receive:
    filled_spots.acquire()
    lock.acquire()
    read_index = shared_list[-3] % BUFFER_SIZE
    value = shared_list[read_index]
    shared_list[-3] += 1
    lock.release()
    empty_spots.release()
    if value is None:
      break
    received_values += 1
    print(f'{value}', end=', ', flush=True)

def main():
  items_to_send = random.randint(1000, 10000)

  smm = SharedMemoryManager()
  smm.start()

  sharable_list = smm.ShareableList([None] * (BUFFER_SIZE + 4))
  sharable_list[-1] = items_to_send  # Set the total items to send
  sharable_list[-2] = 0  # Initialize write index
  sharable_list[-3] = 0  # Initialize read index

  lock = mp.Lock()
  empty_spots = mp.Semaphore(BUFFER_SIZE)
  filled_spots = mp.Semaphore(0)

  writer_processes = []
  reader_processes = []

  for i in range(WRITERS):
    writer = mp.Process(target=writer_process, args=(sharable_list, lock, empty_spots, filled_spots, items_to_send, i))
    writer_processes.append(writer)
    writer.start()

  items_to_receive = items_to_send
  for i in range(READERS):
    reader = mp.Process(target=reader_process, args=(sharable_list, lock, empty_spots, filled_spots, items_to_receive, i))
    reader_processes.append(reader)
    reader.start()

  for writer in writer_processes:
    writer.join()

  for _ in range(READERS):
    empty_spots.acquire()
    lock.acquire()
    write_index = sharable_list[-2] % BUFFER_SIZE
    sharable_list[write_index] = None
    sharable_list[-2] += 1
    lock.release()
    filled_spots.release()

  for reader in reader_processes:
    reader.join()

  print(f'\n\n{items_to_send} values sent')
  print(f'{items_to_receive} values received')
  smm.shutdown()


if __name__ == '__main__':
  main()
