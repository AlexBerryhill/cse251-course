import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2
STOP = None

def writer_process(shared_list, lock, empty_spots, filled_spots, items_to_send):
    current_value = 1
    while current_value <= items_to_send:
        empty_spots.acquire()  # Wait for an empty spot in the buffer
        lock.acquire()  # Acquire the lock to modify the shared list
        write_index = shared_list[-2] % BUFFER_SIZE
        shared_list[write_index] = current_value
        shared_list[-2] += 1
        current_value += 1
        lock.release()  # Release the lock
        filled_spots.release()  # Increment the filled spots count

def reader_process(shared_list, lock, empty_spots, filled_spots):
    while True:
        filled_spots.acquire()  # Wait for a filled spot in the buffer
        lock.acquire()  # Acquire the lock to modify the shared list
        read_index = shared_list[-3] % BUFFER_SIZE
        value = shared_list[read_index]
        shared_list[-3] += 1
        lock.release()  # Release the lock
        empty_spots.release()  # Increment the empty spots count
        if value is STOP:
            break
        print(value, end=', ', flush=True)

def main():
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    sharable_list = smm.ShareableList([0] * (BUFFER_SIZE + 4))
    sharable_list[-1] = items_to_send  # Set the total items to send
    sharable_list[-2] = 0  # Initialize write index
    sharable_list[-3] = 0  # Initialize read index

    lock = mp.Lock()
    empty_spots = mp.Semaphore(BUFFER_SIZE)
    filled_spots = mp.Semaphore(0)

    writer_processes = []
    reader_processes = []

    for _ in range(WRITERS):
        writer = mp.Process(target=writer_process, args=(sharable_list, lock, empty_spots, filled_spots, items_to_send))
        writer_processes.append(writer)
        writer.start()

    for _ in range(READERS):
        reader = mp.Process(target=reader_process, args=(sharable_list, lock, empty_spots, filled_spots))
        reader_processes.append(reader)
        reader.start()

    for writer in writer_processes:
        writer.join()

    # Send stop signal to readers
    for _ in range(READERS):
        empty_spots.acquire()
        lock.acquire()
        write_index = sharable_list[-2] % BUFFER_SIZE
        sharable_list[write_index] = STOP
        sharable_list[-2] += 1
        lock.release()
        filled_spots.release()

    for reader in reader_processes:
        reader.join()

    received_values = sharable_list[-3] - 1
    print(f'{received_values} values received')
    print(f'{items_to_send} values sent')
    smm.shutdown()


if __name__ == '__main__':
    main()
