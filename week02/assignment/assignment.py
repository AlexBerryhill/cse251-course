"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790/'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Threaded_Call(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        global call_count
        response = requests.get(self.url)
        call_count += 1
        if response.status_code == 200:
          self.response = response.json()
        else:
          print(f'Error: {response.status_code} - {self.url}')
          self.response = None

# TODO Add any functions you need here


def main():
  log = Log(show_terminal=True)
  log.start_timer('Starting to retrieve data from the server')


  # TODO Retrieve Top API urls
  top = Threaded_Call(TOP_API_URL)
  top.start()
  top.join()

  # TODO Retireve Details on film 6
  film6 = Threaded_Call(top.response['films'] + '6')
  film6.start()
  film6.join()

  catagories = ['characters', 'planets', 'starships', 'vehicles', 'species']
  threads={'characters':[], 'planets':[], 'starships':[], 'vehicles':[], 'species':[]}
  for catagory in catagories:
    for url in film6.response[catagory]:
      t = Threaded_Call(url)
      threads[catagory].append(t)

  for catagory in threads:
    for t in threads[catagory]:
      t.start()
  
  for catagory in threads:
    for t in threads[catagory]:
      t.join()
  
  names={'characters':[], 'planets':[], 'starships':[], 'vehicles':[], 'species':[]}

  for catagory in threads:
    for t in threads[catagory]:
      names[catagory].append(t.response['name'])

  print(threads['characters'])

  for catagory in names:
    names[catagory].sort()
  
  # for t in threads:
  #   print(t.response)

  # print(threads['characters'][0].response['name'])

  # TODO Display results
  log.write('-----------------------------------------')
  log.write('Title   : ' + film6.response['title'])
  log.write('Director: ' + film6.response['director'])
  log.write('Producer: ' + film6.response['producer'])
  log.write('Releasd : ' + film6.response['release_date'] + '\n')
  
  log.write('Characters: ' + str(len(film6.response['characters'])))
  characters=''
  for character in names['characters']:
    characters += character+', '
  log.write(characters + '\n')
  
  log.write('Planets: ' + str(len(film6.response['planets'])))
  planets=''
  for planet in names['planets']:
    planets += planet+', '
  log.write(planets + '\n')
  
  log.write('Starships: ' + str(len(film6.response['starships'])))
  starships=''
  for starship in names['starships']:
    starships += starship+', '
  log.write(starships + '\n')

  log.write('Vehicles: ' + str(len(film6.response['vehicles'])))
  vehicles=''
  for vehicle in names['vehicles']:
    vehicles += vehicle+', '
  log.write(vehicles + '\n')
  
  log.write('Species: ' + str(len(film6.response['species'])))
  specieses=''
  for species in names['species']:
    specieses += species+', '
  log.write(specieses + '\n')

  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
