# CS50x 2019/Week6/Pset6/Crack

# THIS IS ONLY TO EXERCISE THE multiprocessing.Pool class.
#  THIS IS A NON-SENSICAL APPROACH TO SOLVING PSET6/CRACK
#  BECAUSE THE INPUTS (ascii_letters) CANNOT BE DIVIDED UP
#  FOR ALL PERMUTATIONS POSSIBLE TO BE CHECKED. PERMUTATIONS
#  LIKE e.g. aZ would be lost by dividing the ascii.letters input
#  ALSO the PERMUTATIONS funciton is a very inefficient way of 
#  generating the string inputs for the hash function 
#  ALSO in this particular program the SYNC_MANAGER and the 
#  cross-process checking of the namespace.found value makes for
#  unnecessary overhead and causes severe delays and inefficient use
#  of CPU.  

# DOES NOT WORK BECAUSE SHARED MEM CANNOT BE PASSED TO pool.apply_async()
# !!!!!!!!

# Imports
import crypt  # crypt.crypt(word, salt)
import logging
import os, sys
import string
import time

from itertools import permutations
from multiprocessing import Pool, Value
from multiprocessing import log_to_stderr, get_logger


# Constants
PW_MAX_LEN = 5  # Password maximum length ( = num of password groups)
HASH_INPUTS_1 = string.ascii_lowercase[:13]
HASH_INPUTS_2 = string.ascii_lowercase[13:26]
HASH_INPUTS_3 = string.ascii_uppercase[:13]
HASH_INPUTS_4 = string.ascii_uppercase[13:26]
INPUT_GROUPS = 4
FACTOR = PW_MAX_LEN + 1  # Number of password groups
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

# Worker function to crack password
def worker_crack(aninput, user_hash, salt, sharedmemflag):
    """Returns a set of tuples of all the
         factor-length permutations in a string
    """
    def string_multiply(string, factor):
        """Returns string with characters multiplied by factor"""
        return "".join(char * factor for char in string)

    logging.debug(f"Worker Crack start Found: {sharedmemflag.value}")
    for i in range(1, 6):  # The 6 is the FACTOR
        permutation_tuple_generator = (permutation_tuple
                                       for permutation_tuple in permutations(
                                           string_multiply(aninput, i), i)
        )
        for atuple in permutation_tuple_generator:
            if sharedmemflag.value:
                logging.debug(f"Found: {sharedmemflag.value}")
                return
            test_pw = "".join(atuple)
            test_hash = crypt.crypt(test_pw, salt)
            if test_hash == user_hash:
                sharedmemflag.value = 1
                return test_pw
    
    # Failure
    sys.exit("no password cracked")


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
    inputs = [HASH_INPUTS_1, HASH_INPUTS_2, HASH_INPUTS_3, HASH_INPUTS_4]

    # Shared memory map found to share state between processes
    found = Value('i', 0)
    # DOES NOT WORK BECAUSE SHARED MEM CANNOT BE PASSED TO pool.apply_async()
    # !!!!!!!!


    # The function to crack the DES hashed password.
    #  It is the callback function to main's calls to set_tuple_permutations
    #  via pool.apply_async. When the pool of child processes return results,
    #  the main process will process them via the callback function DES_crack.  
    def print_n_return(result):
        """Callback function for worker_crack
            that prints the password found by
            one of the callers. The other callbacks 
            do not print their None values.
        """
        # Only let the caller print, who has found the password
        if result:
            print(f"password: {result}")
        
        return
    
    # Spawn pool of child processes calling the worker 
    #  function: worker_crack in parallel and 
    #  applying async, with callback function: print_n_terminate
    #  to the result returned from the workers. 
    start_time = time.time()
    pool = Pool(NUM_PHYS_CORES)
    for aninput in inputs:
        pool.apply_async(worker_crack,
                         args=(aninput,
                               user_hash,
                               salt,
                               found),
                         callback=print_n_return
    )
    pool.close()
    pool.join()

    # DOES NOT WORK BECAUSE SHARED MEM CANNOT BE PASSED TO pool.apply_async()
    # !!!!!!!!

    duration = time.time() - start_time
    print(f"Cracking password took {duration:.2f}")

    logging.debug(f"Found: {found.value}")

    # Success
    sys.exit(0)

 
if __name__ == "__main__":
    main()
    
