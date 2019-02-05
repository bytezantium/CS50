""" This module contains the class "Plaintext".

All of this module's functions and attributes are contained within the Plaintext class.

"""


class Plaintext:
    """Class with data and method attributes for enciphering of plaintext methods a la Caesar and Vigenere"""

    def __init__(self, plaintext):
        """ The Plaintext class __init__ method.

        Args:
            plaintext (str): A plaintext string.

        """
        self.plaintext = plaintext
        """ str: The plaintext string is stored in attrubute self.plaintext"""

    def encipher_caesar(self, key):
        """Enciphers self.plaintext using Caesar's cipher and the parameter key.

        Caesar's cipher: c[i] = (p[i] + k) % 26
        c[i]: ith letter of ciphertext
        p[i]: ith letter of the plaintext
        k: key
        %26: to wrap around 26 letter alphabet

        The function only enciphers alphabetical letters and it preserves case.

        Args:
            key (int) or (str): this could be an integer or a string. In either case, the
                parameter is stored in data attribute self.key and converted to an integer value.

        Returns:
        str: the client string variable "ciphertext" is returned. The ciphertext is the enciphered plaintext.

        Example:
            self.plaintext = "This is CS50!"
            >>> encipher_caesar(self, 12)
            "Vjku ku EU50!"

        """
        self.key = int(key)  # Make sure that key argument is an integer
        """ int: arg1 (key) is stored in attribute self.key and to be safe converted to an integer value"""

        ciphertext = ""

        for char in self.plaintext:
            if char.isalpha():
                if char.isupper():
                    # -65 to convert from Unicode upper case to alphabetical letter and +65 to go back to Unicode
                    char = (((ord(char) + self.key) - 65) % 26) + 65
                else:
                    # -97 to convert from Unicode upper case to alphabetical letter and +97 to go back to Unicode
                    char = (((ord(char) + self.key) - 97) % 26) + 97
                char = chr(char)  # Convert integer to string

            ciphertext += char

        return ciphertext

    def encipher_vigenere(self, key):
        """Enciphers self.plaintext using Vigenere's cipher and the parameter key.

        Vigenere's cipher: c[i] = (p[i] + k[j]) % 26
        c[i]: ith letter of ciphertext
        p[i]: ith letter of the plaintext
        k[j]: jth letter of the key
        %26: to wrap around 26 letter alphabet

        The function only enciphers alphabetical letters and it preserves case.

        Args:
            key (str): parameter one must be an alphabetical string.

        Returns:
        str: the client string variable "ciphertext" is returned. The ciphertext is the enciphered plaintext.

        Example:
            self.plaintext = "HELLO"
            >>> encipher_caesar(self, ABC)
            "HFNLP"

        """
        ciphertext = ""  # to store ciphertext output

        # c[i] = (p[i] + k[j]) % 26
        j = 0  # key index

        for char in self.plaintext:  # iterator for letters in plaintext
            if char.isalpha():  # only encipher alphabetical letters
                kj = key[j % len(key)].upper()  # mod to wrap around key and .upper() for case insensitivity
                kj = ord(kj)  # convert to integer
                kj -= 65  # key converted to alphabetical index to shift by
                if char.isupper():  # Preserve case
                    char = (((ord(char) - 65) + kj) % 26) + 65  # mod26 to wrap around alphabet
                else:
                    char = (((ord(char) - 97) + kj) % 26) + 97
                char = chr(char)  # convert to string
                j += 1  # increment key index by 1

            ciphertext += char  # append each character

        return ciphertext
