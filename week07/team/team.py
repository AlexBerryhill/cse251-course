"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 07 Team Activity

Instructions:

1) Make a copy of your assignment 2 program.  Since you are 
   working in a team, you can decide which assignment 2 program 
   that you will use for the team activity.

2) Convert the program to use a process pool and use 
   apply_async() with a callback function to retrieve data 
   from the Star Wars website.  Each request for data must 
   be a apply_async() call.

3) You can continue to use the Request_Thread() class from 
   assignment 02 that makes the call to the server.

"""
from datetime import datetime, timedelta
import requests
import json
from multiprocessing import Pool

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790/'

# Global Variables
call_count = 0


# Function to make API call
def make_api_call(url):
   global call_count
   response = requests.get(url)
   call_count += 1
   if response.status_code == 200:
      print(f'OK: {response.status_code} - {url}')
      return response.json()
   else:
      print(f'Error: {response.status_code} - {url}')
      return None


def main():
   log = Log(show_terminal=True)
   log.start_timer('Starting to retrieve data from the server')

   # Retrieve Top API urls
   top = make_api_call(TOP_API_URL)

   # Retireve Details on film 6
   film6 = make_api_call(top['films'] + '6')

   # Retrieve data in parallel
   catagories = ['characters', 'planets', 'starships', 'vehicles', 'species']
   pool = Pool(processes=len(catagories))
   threads = {}
   for catagory in catagories:
      for url in film6[catagory]:
         threads[url] = pool.apply_async(make_api_call, (url,))

   # Wait for all threads to complete
   pool.close()
   pool.join()

   # Get the responses from threads
   names = {'characters': [], 'planets': [], 'starships': [], 'vehicles': [], 'species': []}
   for catagory in catagories:
      for url in film6[catagory]:
         response = threads[url].get()
         if response is not None:
            names[catagory].append(response['name'])

   for catagory in names:
      names[catagory].sort()

   # Display results
   log.write('-----------------------------------------')
   log.write('Title   : ' + film6['title'])
   log.write('Director: ' + film6['director'])
   log.write('Producer: ' + film6['producer'])
   log.write('Releasd : ' + film6['release_date'] + '\n')

   log.write('Characters: ' + str(len(film6['characters'])))
   characters = ', '.join(names['characters'])
   log.write(characters + '\n')

   log.write('Planets: ' + str(len(film6['planets'])))
   planets = ', '.join(names['planets'])
   log.write(planets + '\n')

   log.write('Starships: ' + str(len(film6['starships'])))
   starships = ', '.join(names['starships'])
   log.write(starships + '\n')

   log.write('Vehicles: ' + str(len(film6['vehicles'])))
   vehicles = ', '.join(names['vehicles'])
   log.write(vehicles + '\n')

   log.write('Species: ' + str(len(film6['species'])))
   specieses = ', '.join(names['species'])
   log.write(specieses + '\n')

   log.stop_timer('Total Time To complete')
   log.write(f'There were {call_count} calls to the server')


if __name__ == "__main__":
   main()

