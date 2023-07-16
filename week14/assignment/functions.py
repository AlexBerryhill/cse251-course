"""
Course: CSE 251, week 14
File: functions.py
Author: <your name>

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue
import threading

# Caches for storing retrieved data
person_cache = {}
family_cache = {}

# Locks for accessing the caches
person_cache_lock = threading.Lock()
family_cache_lock = threading.Lock()

# -----------------------------------------------------------------------------
def retrieve_family(family_id):
    # Retrieve the family information from the server
    request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    request.start()
    request.join()
    family_data = request.get_response()
    return family_data

# -----------------------------------------------------------------------------
def retrieve_person(person_id):
    # Retrieve the person information from the server
    request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
    request.start()
    request.join()
    person_data = request.get_response()
    return person_data

# -----------------------------------------------------------------------------
def process_family(family_data, tree):
    if family_data is None:
        return
    family_id = family_data['id']
    husband_id = family_data['husband_id']
    wife_id = family_data['wife_id']
    children_ids = family_data['children']

    # Check if the family is already processed and exists in the tree
    if tree.does_family_exist(family_id):
        return

    next_level = []
    # Check if the husband is already processed and exists in the tree
    if husband_id in person_cache:
        husband_data = person_cache[husband_id]
    else:
        husband_data = retrieve_person(husband_id)
        with person_cache_lock:
            person_cache[husband_id] = husband_data

    husband = Person(husband_data)
    next_level.append(husband)
    tree.add_person(husband)

    # Check if the wife is already processed and exists in the tree
    if wife_id in person_cache:
        wife_data = person_cache[wife_id]
    else:
        wife_data = retrieve_person(wife_id)
        with person_cache_lock:
            person_cache[wife_id] = wife_data

    wife = Person(wife_data)
    next_level.append(wife)
    tree.add_person(wife)

    # Check if the children are already processed and exist in the tree
    for child_id in children_ids:
        if child_id in person_cache:
            child_data = person_cache[child_id]
        else:
            child_data = retrieve_person(child_id)
            with person_cache_lock:
                person_cache[child_id] = child_data

        child = Person(child_data)
        tree.add_person(child)

    # Create the family object and add it to the tree
    family = Family(family_data)
    tree.add_family(family)
    return next_level

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # Retrieve the family information from the server
    request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    request.start()
    request.join()

    family_data = request.get_response()

    # Process the family information
    family = Family(family_data)
    tree.add_family(family)

    spouse_reqs = []
    # Retrieve the husband's information from the server
    husband_id = family.get_husband()
    if husband_id:
        request = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
        request.start()
        spouse_reqs.append(request)

    # Retrieve the wife's information from the server
    wife_id = family.get_wife()
    if wife_id:
        request = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
        request.start()
        spouse_reqs.append(request)

    children_ids = family_data['children']
    child_reqs = []
    for child_id in children_ids:
        if not tree.does_person_exist(child_id):
            child_req = Request_thread(f'{TOP_API_URL}/person/{child_id}')
            child_req.start()
            child_reqs.append(child_req)
    
    for spouse_req in spouse_reqs:
        spouse_req.join()
        spouse_data = spouse_req.get_response()
        spouse = Person(spouse_data)
        if not tree.does_person_exist(spouse_data['id']):
            tree.add_person(spouse)
        # Recursively process the parents
        if spouse.get_parentid():
            depth_fs_pedigree(spouse.get_parentid(), tree)
            
    for child_req in child_reqs:
        child_req.join()
        child_data = child_req.get_response()
        child = Person(child_data)
        tree.add_person(child)        

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # Create a queue to store the family IDs for breadth-first traversal
    family_queue = queue.Queue()
    family_queue.put(family_id)

    # Perform breadth-first traversal
    while not family_queue.empty():
        current_family_id = family_queue.get()

        # Retrieve the family information from the server
        request = Request_thread(f'{TOP_API_URL}/family/{current_family_id}')
        request.start()
        request.join()
        family_data = request.get_response()

        # Process the family information
        family = Family(family_data)
        tree.add_family(family)

        # Retrieve the husband's information from the server
        husband_id = family.get_husband()
        request_husband = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
        request_husband.start()
        request_husband.join()
        husband_data = request_husband.get_response()

        # Process the husband's information
        husband = Person(husband_data)
        tree.add_person(husband)

        # Retrieve the wife's information from the server
        wife_id = family.get_wife()
        request_wife = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
        request_wife.start()
        request_wife.join()
        wife_data = request_wife.get_response()

        # Process the wife's information
        wife = Person(wife_data)
        tree.add_person(wife)

        # Add the parent IDs to the queue for further traversal
        if husband.get_parentid():
            family_queue.put(husband.get_parentid())

        if wife.get_parentid():
            family_queue.put(wife.get_parentid())

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # Create a semaphore to limit the number of concurrent connections
    semaphore = threading.Semaphore(5)

    # Create a queue to store the family IDs for breadth-first traversal
    family_queue = queue.Queue()
    family_queue.put(family_id)

    # Perform breadth-first traversal
    while not family_queue.empty():
        current_family_id = family_queue.get()

        # Acquire the semaphore before making the request
        semaphore.acquire()

        # Retrieve the family information from the server
        request = Request_thread(f'{TOP_API_URL}/family/{current_family_id}')
        request.start()
        request.join()
        family_data = request.get_response()

        # Process the family information
        family = Family(family_data)
        tree.add_family(family)

        # Retrieve the husband's information from the server
        husband_id = family.get_husband()
        request_husband = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
        request_husband.start()
        request_husband.join()
        husband_data = request_husband.get_response()

        # Process the husband's information
        husband = Person(husband_data)
        tree.add_person(husband)

        # Retrieve the wife's information from the server
        wife_id = family.get_wife()
        request_wife = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
        request_wife.start()
        request_wife.join()
        wife_data = request_wife.get_response()

        # Process the wife's information
        wife = Person(wife_data)
        tree.add_person(wife)

        # Add the parent IDs to the queue for further traversal
        if husband.get_parentid():
            family_queue.put(husband.get_parentid())

        if wife.get_parentid():
            family_queue.put(wife.get_parentid())

        # Release the semaphore after processing the request
        semaphore.release()
