# Imported modules and functions
from cs50 import get_int

while True:  # Get 0-23 height from user
    height = get_int("Height: ")
    if height in range(24):
        break

# Initialize variable row
row = 0

for i in range(height):
    print(" " * (height - row - 1), end="")  # Print spaces
    print("#" * (row + 2), end="")  # Print bricks
    print()  # Print out i many rows
    row += 1  # Increment row
