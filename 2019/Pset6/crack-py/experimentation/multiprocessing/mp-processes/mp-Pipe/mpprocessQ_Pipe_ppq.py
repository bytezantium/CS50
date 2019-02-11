# CS50x 2019/Week6/Pset6/Crack

# Imports
import crypt  # crypt.crypt(word, salt)
import logging
import sys
import string
import time

from multiprocessing import Process, Pipe, Queue
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
FACTOR = PW_MAX_LEN  # Number of password groups
NUM_PHYS_CORES = 4
WORKER_CRACKS = NUM_PHYS_CORES - 1


# Worker Functions
def Worker_PlaintextGen(aninput,  producer_queue, pipe_end2):
    """Produces string permutations to be places in producer queue.
        Stops after sharedmemflag value is True/int(1) or after all 
        possible permutations have been produced. 
    """
    for fifth in aninput:
        for fourth in aninput:
            for third in aninput:
                for second in aninput:
                        for first in aninput[1:]:
                            if not pipe_end2.poll():  # Non-blocking check for data received
                                test_pw = f"{first}{second}{third}{fourth}{fifth}".strip()
                                producer_queue.put(test_pw)
                            else:
                                logging.debug("Found signal received")
                                for i in range(WORKER_CRACKS - 1):
                                    time.sleep(2)
                                    producer_queue.put(None)
                                    logging.debug(f"Poison-{i} placed")
                                time.sleep(0.5)
                                producer_queue.cancel_join_thread()  # Prevent join_thread() from blocking.
                                logging.debug("exiting after cancel_join_thread")
                                return  # Found
    
    # Racing conditions
    time.sleep(1)
    
    # Failure
    if not pipe_end2.poll():
        for i in range(WORKER_CRACKS):
            producer_queue.put(None)
            logging.debug(f"Poison-{i} placed")
        sys.exit("No password cracked")
    
    # 2nd Found exit option due to racing conditions
    if pipe_end2.poll():
        return  # Found.2

def Worker_CrackPw(consumer_queue, user_hash, salt, pipe_end1):
    """Uses DES-based crypt function to hash inputs in parameter aninput
        and compare the hashes to the user_hash. If a pw is cracked,
        the sharedmemflag is set to True/int(1)
    """
    while True:
        test_pw = consumer_queue.get()
        if test_pw is None:
            logging.debug("Took poison")
            return
        test_hash = crypt.crypt(test_pw, salt)
        if test_hash == user_hash:
            pipe_end1.send(1)  # Send found signal to WorkerPlaintextGen
            pipe_end1.close()
            logging.debug("sent found signal via pipe")
            print(f"password found: {test_pw}")
            return
 
    #else:
        #logging.debug("Took poison")
        #sys.exit("No password could be cracked")


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

    # Instantiate Pipe for conenction between 
    #  Worker_PlaintextGen and Worker_CrackPW
    pipe_end1, pipe_end2 = Pipe()
    
    # Spawn processes calling the worker functions 
    processes = []
    
    # Measure execution time of workers
    start_time = time.time()
    
    # PlaintextGen worker
    process = Process(name="Worker_PlaintextGen",
                      target=Worker_PlaintextGen,
                      args=(inputs, hybrid_queue,
                      pipe_end2),
                      daemon=True
    )
    processes.append(process)
    process.start()
    
    # CrackPW workers
    for i in range(WORKER_CRACKS):
        process = Process(name=f"Worker_CrackPW-{i}",
                          target=Worker_CrackPw,
                          args=(hybrid_queue, user_hash,
                          salt, pipe_end1),
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
    
