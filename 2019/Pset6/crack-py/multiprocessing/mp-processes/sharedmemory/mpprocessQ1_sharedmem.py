# CS50x 2019/Week6/Pset6/Crack

# Imports
import crypt  # crypt.crypt(word, salt)
import logging
import sys
import string
import time

from multiprocessing import Process, Queue, Value
from multiprocessing import log_to_stderr, get_logger

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


# Constants
PW_MAX_LEN = 5  # Password maximum length
HASH_INPUTS = " " + string.ascii_letters
NUM_PHYS_CORES = 4


# Worker Functions
def Worker_PlaintextGen(aninput,  producer_queue, sharedmemflag):
    """Produces string permutations to be places in producer queue.
        Stops after sharedmemflag value is True/int(1) or after all 
        possible permutations have been produced. 
    """
    # PW_MAX_LEN times for loops
    for fifth in aninput:
        for fourth in aninput:
            for third in aninput:
                for second in aninput:
                        for first in aninput[1:]:
                            if not sharedmemflag.value:
                                test_pw = f"{first}{second}{third}{fourth}{fifth}".strip()
                                producer_queue.put(test_pw)
                            else:
                                producer_queue.cancel_join_thread()  # Prevent join_thread() from blocking.
                                # logging.debug("exiting after cancel_join_thread"))
                                return  # Found
    # Failure
    if not sharedmemflag.value:
        sys.exit("No password cracked")
    
    # 2nd Found exit option due to racing conditions
    if sharedmemflag.value:
        return  # Found.2

def Worker_CrackPw(consumer_queue, user_hash, salt, sharedmemflag):
    """Uses DES-based crypt function to hash inputs in parameter aninput
        and compare the hashes to the user_hash. If a pw is cracked,
        the sharedmemflag is set to True/int(1)
    """
    while not sharedmemflag.value:
        test_pw = consumer_queue.get()
        test_hash = crypt.crypt(test_pw, salt)
        if test_hash == user_hash:
            sharedmemflag.value = 1  # Set shared boolean found to True 
            print(f"password found: {test_pw}")
 
    if sharedmemflag:
        # logging.debug(f"exiting with sharedmemflag: {bool(sharedmemflag.value)}")
        return
    
    else:
        sys.exit("No password could be cracked")


# Main function
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

    # Inputs for Worker_PlaintextGen
    inputs = HASH_INPUTS
    
    # Producer/Consumer queue for Worker_PlaintextGen outputs
    #  and Worker_Crack inputs
    hybrid_queue = Queue()

    # Initialize memory Value shared between worker processes,
    # indicating if password was cracked, to False
    found = Value('i', 0)  # Boolean found == false

    # Spawn processes calling the worker functions 
    processes = []
    
    # Measure execution time of workers
    start_time = time.time()
    
    # PlaintextGen workers
    process = Process(name="Worker_PlaintextGen",
                    target=Worker_PlaintextGen,
                    args=(inputs, hybrid_queue,
                    found),
                    daemon=True
    )
    processes.append(process)
    process.start()
    
    # CrackPW workers
    for i in range(NUM_PHYS_CORES - 1):
        process = Process(name=f"Worker_CrackPW-{i}",
                          target=Worker_CrackPw,
                          args=(hybrid_queue, user_hash,
                          salt, found),
                          daemon=True
        )
        processes.append(process)
        process.start()

    # Start and join processes
    for process in processes:
        process.join()

    # Success
    duration = time.time() - start_time
    print(f"Cracking password took {duration:.2f} seconds")
    sys.exit(0)

 
if __name__ == "__main__":
    main()
    
