# Import modules and functions
from cs50 import get_int

# Promp user for positive 0-23 int
while True:
    height = get_int("Height: ")
    if height in range(24):
        break

row = 0  # Initialize row
for i in range(height):
    # Print left pyramid
    print(" " * (height - row - 1), end="")  # Print spaces
    print("#" * (row + 1), end="")  # Print bricks
    # Print gap
    print(" " * 2, end="")  # 2 spaces
    # Print right pyramid
    print("#" * (row + 1), end="")
    # Print i many rows
    print()
    row += 1  # Increment row