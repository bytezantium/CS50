#  Imported modules and functions
from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Split each string a,b into lines
    a = a.splitlines()
    b = b.splitlines()

    # Compute a list of all lines that appear in both a and b
    lines_matches = set(line for line in a if line in b)

    # Return the set
    return lines_matches


def sentences(a, b):
    """Return sentences in both a and b"""

    # Split each string a,b into sentences
    a = sent_tokenize(a, language='english')
    b = sent_tokenize(b, language='english')

    # Compute list of all sentences appearing in both a and b
    sent_matches = set(sent for sent in a if sent in b)

    # Return the set
    return sent_matches


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # Split each string a,b into all substrings of length n
    substr_a = []  # List of substrings in a
    substr_b = []  # List of substrings in b

    # Extract substrings from string and append to lists
    for substr in extract_substrings(a, n):
        substr_a.append(substr)
    for substr in extract_substrings(b, n):
        substr_b.append(substr)

    # Compute a list of all substrings appearing in both a and b - no duplicates
    substr_matches = set(substr for substr in substr_a if substr in substr_b)

    # Return the set
    return substr_matches


def extract_substrings(string, n):
    """Generator that returns all substrings of specified length in a string"""
    len_string = len(string)

    for index in range(0, len_string - n + 1):
        substr = string[index:index + n]
        yield substr  # Substring span ends with end of string
