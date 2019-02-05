# Credit Card Number Class with methods to check validity of card number

# Import constants module
from cc_constants import (VISA_PRE, VISA_LEN,
                          AMEX_PRE, AMEX_LEN,
                          MASTERCARD_PRE, MASTERCARD_LEN,
                          START, END)


class CC_number:
    """Implements a checksum validation for credit card number"""

    def __init__(self, digits):
        """Converts cc_number into a list of digits - citation: https://stackoverflow.com/a/21270338/10596328"""
        self.digits = [int(i) for i in str(digits)]

    def validate(self):
        """Validates cc_number via Luhn's algorithm"""

        # Sums the items of boths digit lists according to Luhn's algorithm
        sum1 = sum(i for i in self.digits[::-2])
        sum2 = sum(i * 2 % 10 + ((i * 2 // 10) % 10) for i in self.digits[-2::-2])
        checksum = sum1 + sum2

        # Validates checksum according to Luhn's algorithm
        if (checksum % 10) != 0:
            print("INVALID")

        # aggregates first two digits of credit card into a string
        cc_prefix = ''.join(map(str, self.digits[START:END]))

        # Check for company identifier and valid length
        if len(self.digits) in VISA_LEN and cc_prefix[0] in VISA_PRE:
            print("VISA")
        elif len(self.digits) in AMEX_LEN and cc_prefix in AMEX_PRE:
            print("AMEX")
        elif len(self.digits) in MASTERCARD_LEN and cc_prefix in MASTERCARD_PRE:
            print("MASTERCARD")
        else:
            print("INVALID")
