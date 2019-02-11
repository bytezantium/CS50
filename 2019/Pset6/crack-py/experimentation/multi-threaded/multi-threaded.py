# CS50x 2019/Week6/Pset6/Crack

# Modules
import crypt  # crypt.crypt(word, salt)
from itertools import permutations
import logging
import sys
import string
import time
import threading
import queue


# Constants
PW_MAX_LEN = 5  # Password maximum length ( = num of password groups)
HASH_INPUTS = string.ascii_letters
HASH_GROUPS = PW_MAX_LEN  # Number of password groups
NUM_THREADS = 1 # Number of threads per password group


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


def main():
    """Gets input hash and salt from command line,
       spawns worker threads, initializes queue,
       calls worker function"""

    # Found list to catch found event on threads
    #  via list object going form empty to non-empty
    found = []

    # Check user input
    if len(sys.argv) != 2:
        sys.exit("Usage: python crack.py hash")

    # Extract hash and salt from user input
    user_hash = sys.argv[1]
    salt = user_hash[:2]

    # Instantiate queue
    q = queue.Queue()

    # Start NUM_THREADS worker threads for each password group
    for i in range(NUM_THREADS):
        # Start pool of threads per pw_group
        worker = threading.Thread(name="Worker - {}".format(i),
                                  target=DES_hash_comp,
                                  args=(q, salt,
                                        user_hash, found),
                                  daemon=True
        )
        worker.start()

    # Start Farmer thread, which generetes data for the queue
    #  that the worker threads are working on
    farmer = threading.Thread(name="Farmer",
                              target=queue_generate,
                              args=(q, HASH_INPUTS,
                              HASH_GROUPS, 
                              found),
                              daemon=True
    )
    farmer.start()
    farmer.join()
    
    # Success
    if found:
        time.sleep(2)
        logging.debug("Thread-count: {} (incl. Main)".format(threading.activeCount()))
        logging.debug('success - exiting')
        sys.exit(0)

# Worker function
def DES_hash_comp(queue, salt, input_hash, found):
    """Uses C’s DES-based crypt function to
    multi-thread brute force cracking of input_hash"""

    logging.debug('starting')
    # Hash and compare all pw_group permutations with input_hash
    while not found:
        test_pw = queue.get()
        test_hash = crypt.crypt(test_pw, salt)
        if test_hash == input_hash:
            found.append(test_pw)
            logging.debug('password found - exiting')
            print(f"password: {test_pw}")
        queue.task_done()
    return  # found

# Custom Function
def string_multiply(string, factor):
    """Returns string with characters multiplied by factor"""
    return "".join(char * factor for char in string)

def queue_generate(queue, inputs, groups, found):
    
    #Populate queue with input groups in groups batches
    for i in range(1, groups):
        
        if found: 
            return
        
        test_pw_gen = (permutation_tuple
                        for permutation_tuple in permutations(
                            string_multiply(
                                inputs, i), i
        ))

        test_pws_set = set(test_pw_gen)
        logging.debug("Test-pws_set: {}".format(len(test_pws_set)))
        for test_pw_tuple in test_pws_set:
            if found:
                break
            test_pw = "".join(test_pw_tuple)
            #logging.debug('test_pw: %s' % test_pw)
            #time.sleep(0.01)
            queue.put(test_pw)
        
        if not found: 
            logging.debug('Batch/HASH_GROUPS {0} of {1} Done'.format(
                                                    i, groups)
            )
            time.sleep(1)

if __name__ == "__main__":
    main()


