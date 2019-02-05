# CS50x pset6/sentimental/caesar

# Imported modules and functions
from cs50 import get_string
from Plaintext import Plaintext
import sys


def main():
    """Allow for method call .main() from importers"""

    # Check for 2 command line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python caesar.py key")

    # Prompt user for plaintext
    plaintext = get_string("plaintext: ")
    plaintext = Plaintext(plaintext)

    # Encipher plaintext with user inputted key using caesar cipher
    ciphertext = plaintext.encipher_caesar(sys.argv[1])

    # Print ciphertext
    print(f"ciphertext: {ciphertext}")


# Allow import without running main()
if __name__ == "__main__":
    main()
