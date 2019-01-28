# CS50x 2019/Week6/Pset6/Crack

# THIS IS ONLY TO EXERCISE THE multiprocessing.Pool class.
#  THIS IS A NON-SENSICAL APPROACH TO SOLVING PSET6/CRACK
#  BECAUSE THE INPUTS (ascii_letters) CANNOT BE DIVIDED UP
#  FOR ALL PERMUTATIONS POSSIBLE TO BE CHECKED. PERMUTATIONS
#  LIKE e.g. aZ would be lost by dividing the ascii.letters input
#  ALSO the PERMUTATIONS funciton is a very inefficient way of 
#  generating the string inputs for the hash function.  
#  ALSO in this particular program the constant checking of the
#  cross-process shared mp.Queue object probably also leads to
#  unnecessary delays. 

# Imports
import crypt  # crypt.crypt(word, salt)
import logging
import os, sys
import string
import time

from itertools import permutations
from multiprocessing import Process, Queue
from multiprocessing import log_to_stderr, get_logger


# Constants
PW_MAX_LEN = 5  # Password maximum length ( = num of password groups)
HASH_INPUTS_1 = string.ascii_lowercase[:13]
HASH_INPUTS_2 = string.ascii_lowercase[13:26]
HASH_INPUTS_3 = string.ascii_uppercase[:13]
HASH_INPUTS_4 = string.ascii_uppercase[13:26]
INPUT_GROUPS = 4
FACTOR = PW_MAX_LEN  # Number of password groups
NUM_PHYS_CORES = 4

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(processName)-10s) (%(process)-4d) %(message)s',
)
# Create logger
logger = get_logger()
logger.setLevel(logging.INFO)
# create console handler and set level to INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter(
    '[%(levelname)s] (%(processName)-10s) (%(process)-4d) %(message)s'
)
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# Worker Function
def worker_crack_password(aninput, user_hash, salt, poison_pill_queue):
    """Cracks DES-based passwor hashed, by generating
        plaintext permutations from aninput, and hashing them
        with DES-based crypt function, to match with user_hash. 
    """
    def string_multiply(string, factor):
        """Returns string with characters multiplied by factor"""
        return "".join(char * factor for char in string)
    
    start_time = time.time()
    for i in range(1, 6):  # The 6 is the FACTOR
        permutation_tuple_generator = (permutation_tuple
                                       for permutation_tuple in permutations(
                                           string_multiply(aninput, i), i)
        )
        for atuple in permutation_tuple_generator:
            if poison_pill_queue.empty():
                test_pw = "".join(atuple)
                test_hash = crypt.crypt(test_pw, salt)
                if test_hash == user_hash:
                    duration = time.time() - start_time
                    print(f"Cracking password took {duration:.2f} seconds")
                    poison_pill_queue.put("P")
                    logging.debug("put poison pill")
                    print(f"password found: {test_pw}")  # password found
                    return
            else:
                return  # Found elsewhere
    
    # Failure
    if poison_pill_queue.empty():
        sys.exit("No password cracked")
    
    # 2nd Found elsewhere, due to racing conditions
    if not poison_pill_queue.empty():
        return


def main():
    """Gets input hash and salt from command line,
       spawns worker threads, initializes queue,
       calls worker function"""

    # Check user input
    if len(sys.argv) != 2:
        sys.exit("Usage: python crack.py hash")

    # Extract hash and salt from user input
    user_hash = sys.argv[1]
    salt = user_hash[:2]

    # Input lists
    inputs = [HASH_INPUTS_1, HASH_INPUTS_2, HASH_INPUTS_3, HASH_INPUTS_4] # [HASH_INPUTS_1, HASH_INPUTS_2, HASH_INPUTS_3, HASH_INPUTS_4]

    # Queue into which the process that finds the password in its input set
    #  can put a poison pill for the other processes to also exit
    pp_queue = Queue()

    # Spawn processes calling the worker 
    processes = []
    for i in range(len(inputs)):
        process = Process(target=worker_crack_password,
                          args=(inputs[i],
                            user_hash,
                            salt,
                            pp_queue),
                          daemon=True
        )
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()

    # Success
    sys.exit(0)

 
if __name__ == "__main__":
    main()
    
