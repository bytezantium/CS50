from enum import Enum
import time


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b
       returns 2D list of costs
       dimensions: len(a) + 1 by len(b) + 1
       matrix [i][j] is tuple of
        - edit distance between first i chars of a and first j chars of b
        - last operation in optimal sequence
       edit distance between a and b is matrix[len(a)][len(b)]
    """
    matrix = [[(0, None), ]]

    # Base case first column
    for cost in range(1, len(a) + 1):
        matrix.append([(cost, Operation.DELETED), ])

    # Base case first row
    for cost in range(1, len(b) + 1):
        matrix[0].append((cost, Operation.INSERTED))

    lenA = len(a)
    lenB = len(b)
    row_index = 1

    matrix = helper(a, b, matrix, row_index, lenA, lenB)

    return matrix


def helper(a, b, matrix, row_index, lenA, lenB):
    """recursive helper function for computation of the costs
        for all of the cells inside matrix
    """
    while row_index < lenA + 1:
        for cell in range(1, lenB + 1):
            cost, operation = costcompare(a, b, matrix, row_index, cell)
            matrix[row_index].append((cost, operation))
        return helper(a, b, matrix, row_index + 1, lenA, lenB)

    return matrix


def costcompare(a, b, matrix, row, cell):
    """ Compares deletion vs. insertion vs. substitution costs and
        returns whichever one has minimum cost.
    """
    costs_operations = (deletion_cost(matrix, row, cell),
                        insertion_cost(matrix, row, cell),
                        substitution_cost(matrix, row, cell, a[row - 1], b[cell - 1]))

    def cost_extract(cost_operation):
        """format the cost_operation tuple for min function"""
        cost, operation = cost_operation
        return cost

    return min(costs_operations, key=cost_extract)


def deletion_cost(matrix, row, cell):
    """Deletion: cost[i - 1][j] + 1"""
    cost, _ = matrix[row - 1][cell]
    return (cost + 1, Operation.DELETED)


def insertion_cost(matrix, row, cell):
    """Insertion: cost[i][j - 1] + 1"""
    cost, _ = matrix[row][cell - 1]
    return (cost + 1, Operation.INSERTED)


def substitution_cost(matrix, row, cell, charA, charB):
    """Substitution: cost[i - 1][j - 1] if ith char of a is jth char of b
                     cost[i - 1][j - 1] + 1 otherwise
    """
    cost, _ = matrix[row - 1][cell - 1]
    if charA == charB:
        return (cost, Operation.SUBSTITUTED)
    else:
        return (cost + 1, Operation.SUBSTITUTED)
