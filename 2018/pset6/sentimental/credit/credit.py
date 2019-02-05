# CS50x Pset6/Sentimental/Credit

# Import modules and functions
from cs50 import get_int
from cc_number import CC_number


# Prompt user for input
while True:
    cc_number = get_int("Credit Card Number: ")
    if (cc_number > 0):
        break

# Assign class CC_number to int object cc_number
cc_number = CC_number(cc_number)

# Validate checksum
cc_number.validate()
