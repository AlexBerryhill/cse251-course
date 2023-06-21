"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Alex Berryhill

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

<Answer here>

Why would it work?

<Answer here>

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0
COLORS_DICT = {
    (0,0,255): 'red',
    (0,255,0): 'green',
    (255,0,0): 'blue',
    (255,255,0): 'yellow',
    (0,255,255): 'cyan',
    (255,0,255): 'magenta',
    (128,0,0): 'maroon',
    (128,128,0): 'olive',
    (0,128,0): 'dark green',
    (128,0,128): 'purple',
    (0,128,128): 'teal',
    (0,0,128): 'navy',
    (72,61,139): 'dark slate blue',
    (143,143,188): 'light slate blue',
    (226,138,43): 'cadet blue',
    (128,114,250): 'aquamarine'
}

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

# class ThreadWithResult(threading.Thread):
#     def __init__(self, target, args):
#         threading.Thread.__init__(self)
#         self.target = target
#         self.args = args
#         self.result = None
    
#     def run(self):
#         print(f'Starting thread {COLORS_DICT[self.args[4]]}')
#         self.target(*self.args)
    
#     def join(self):
#         threading.Thread.join(self)
#         return self.result

def run(self):
    try:
        if self._target is not None:
            self._result=self._target(*self._args, **self._kwargs)
    finally:
        # Avoid a refcycle if the thread is running a function with
        # an argument that has a member that points to the thread.
        del self._target, self._args, self._kwargs

def join(self, timeout=None):
    if not self._initialized:
            raise RuntimeError("Thread.__init__() not called")
    if not self._started.is_set():
        raise RuntimeError("cannot join thread before it is started")
    # if self is current_thread():
    #     raise RuntimeError("cannot join current thread")

    if timeout is None:
        self._wait_for_tstate_lock()
    else:
        # the behavior of a negative timeout isn't documented, but
        # historically .join(timeout=x) for x<0 has acted as if timeout=0
        self._wait_for_tstate_lock(timeout=max(timeout, 0))
    return self._result

threading.Thread.run = run
threading.Thread.join = join

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global stop
    stop = False

    path = _find_end(maze, path=[], color=get_color())
    
    # Store the path variable for later use
    maze.path = path

def _find_end(maze, row=0, col=0, path=None, color=(0, 0, 255)) -> list:
    global stop, thread_count  # Refer to the global stop and thread_count variables
    
    # Base case: If the maze is already at the end position, return the current path
    if maze.at_end(row, col):
        print(f'Found end at {row}, {col}')
        stop = True  # Set the stop flag to True when the end position is found
        return path
    elif(stop):
        # maze.restore(row, col)
        return []

    possible_moves = maze.get_possible_moves(row, col)

    threads=[]
    result = None
    for i, moves in enumerate(possible_moves):
        if maze.can_move_here(moves[0], moves[1]):
            if len(possible_moves) > 1 and i != len(possible_moves) - 1:
                new_color = get_color()
                maze.move(moves[0], moves[1], new_color)
                thread = threading.Thread(target=_find_end, args=(maze, moves[0], moves[1], path + [(moves[0], moves[1])], new_color))
                thread.start()
                thread_count += 1
                threads.append(thread)
            else:
                maze.move(moves[0], moves[1], color)
                # Recursively call solve_path for each possible move
                result = _find_end(maze, moves[0], moves[1], path + [(moves[0], moves[1])], color)
                if result:
                    # If a valid path is found, return it
                    # print(result, COLORS_DICT[color])
                    return result

    for thread in threads:
        result = thread.join()
        if result:
            return result

    # If no valid path is found, return an empty list
    # if not result:
    #     maze.restore(row, col)
    return []

def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()