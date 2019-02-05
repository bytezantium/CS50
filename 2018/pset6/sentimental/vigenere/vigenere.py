# CS50x pset6/sentimental/vigenere

# Imported modules and functions
from cs50 import get_string
from Plaintext import Plaintext
import sys


def main():  # Allow for method call .main() from importers
    # Get a valid key
    if len(sys.argv) != 2 or not sys.argv[1].isalpha():
        sys.exit("Usage: python vigenere.py key (only alphabetical)")

    # Get the plaintext
    plaintext = get_string("plaintext: ")
    plaintext = Plaintext(plaintext)

    # Encipher
    ciphertext = plaintext.encipher_vigenere(sys.argv[1])

    # Print CIPHERTEXT
    print(f"ciphertext: {ciphertext}")


# Allow import without running this module's main()
if __name__ == "__main__":
    main()
