# Import modules and functions
from cs50 import get_float

# Prompt user for an amount of change converted to cents
while True:
    change = get_float("Change owed: ")
    change = round(change * 100)
    if change > 0:
        break

# always use largest coin possible and keep track of coins used
quarters = change // 25
dimes = (change % 25) // 10
nickels = ((change % 25) % 10) // 5
pennies = ((change % 25) % 10) % 5

# print the final number of coins
print(quarters + dimes + nickels + pennies)

