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
        edit distance between first i chars of a and first j chars of b
        last operation in optimal sequence
       edit distance between a and b is matrix[len(a)][len(b)]
    """

    # In matrix[i][j] store (cost, operation)
        # cost is an int = minimum number of steps to convert first i chars of a into first j chars of b
        # operation is one of Operation.DELETED, Operation.Inserted, Operation.SUBSTITUTED
            # for matrix[0][0], operation is None

    
    # Edit Distance Algorithm
    # cost[i][j] is min of:
        # - Deletion: cost[i - 1][j] + 1
        # - Insertion: cost[i][j - 1] + 1
        # - Substitution: cost[i - 1][j - 1] if ith char of a is jth char of b
        #                 cost[i - 1][j - 1] + 1 otherwise
    
    # Calculating Edit Distance
        # Set up 2D list
        # Add values for base cases (first row and first column)
        # Fill in the other entries in the table
        # Recursive helper function may be helpful

    matrix = [[(0, None),]]

    # Base case first column
    for cost in range(1, len(a) + 1):
        matrix.append([(cost, Operation.DELETED),])

    # Base case first row
    for cost in range(1, len(b) + 1):
        matrix[0].append((cost, Operation.INSERTED))

    #print(f"Matrix1: {matrix}")
    lenA = len(a)
    lenB = len(b)
    row_index = 1

    matrix = helper(a, b, matrix, row_index, lenA, lenB)
    
    for row in matrix:
        for cell in row:
            print(f'{cell[0]}  ', end='')
        print()
    
    return matrix


def helper(a, b, matrix, row_index, lenA, lenB):
    """recursive helper function for computation of the costs
        for all of the cells inside matrix
    """
    while row_index < lenA + 1:
        for cell in range(1, lenB + 1):
            cost, operation = costcompare(a, b, matrix, row_index, cell)
            print(cost, operation)
            matrix[row_index].append((cost, operation))

        print(f"row = {row_index}")
        return helper(a, b, matrix, row_index + 1, lenA, lenB)
    
    return matrix
    


def costcompare(a, b, matrix, row, cell):
    """ Compares deletion vs. insertion vs. substitution costs and
        returns whichever one has minimum cost.
    """
    print(a[row - 1], b[cell - 1])
    costs_operations = (deletion_cost(matrix, row, cell),
                        insertion_cost(matrix, row, cell),
                        substitution_cost(matrix, row, cell, a[row - 1], b[cell - 1]),
    )

    
    def cost_extract(cost_operation):
        """format the cost_operation tuple for min function"""
        cost, operation = cost_operation
        return cost

    print(f"Operation: {min(costs_operations, key=cost_extract)[1]}")
    return min(costs_operations, key=cost_extract)


def deletion_cost(matrix, row, cell):
    """Deletion: cost[i - 1][j] + 1"""
    cost, _ = matrix[row - 1][cell]
    print(f"Deletion cost: {cost} + 1")
    return (cost + 1, Operation.DELETED)


def insertion_cost(matrix, row, cell):
    """Insertion: cost[i][j - 1] + 1"""
    cost, _ = matrix[row][cell - 1]
    print(f"Insertion cost: {cost} + 1")
    return (cost + 1, Operation.INSERTED)


def substitution_cost(matrix, row, cell, charA, charB):
    """Substitution: cost[i - 1][j - 1] if ith char of a is jth char of b
                     cost[i - 1][j - 1] + 1 otherwise
    """
    cost, _ = matrix[row - 1][cell - 1]
    print(f"Substitution cost: {cost} + 1 only if false: {charA} == {charB}: {charA == charB}")
    # time.sleep(0.05)
    if charA == charB:
        return (cost, Operation.SUBSTITUTED)
    else:
        return (cost + 1, Operation.SUBSTITUTED)


if __name__ == "__main__":
    a = 'Yale'
    b = 'Harvard'
    edit_distance = distances(a, b)
    print(f"{a[len(a) - 1]}  {b[len(b) - 1]}")
    print(f"Edit Distance: {edit_distance[len(a)][len(b)]}")

