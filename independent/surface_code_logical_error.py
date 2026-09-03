from itertools import combinations
def is_vertical_logical_error(error_pattern):
    """
    Check if the error pattern corresponds to a vertical logical error.
    
    Parameters:
    - error_pattern: List of tuples representing error locations (x, y)
    - code_distance: Distance of the surface code
    
    Returns:
    - True if vertical logical error, False otherwise
    """
    # return True only if for all error pairs the difference in the row index is at least as large as the difference in the column index
    for (x1, y1), (x2, y2) in combinations(error_pattern, 2):
        if abs(y1 - y2) < abs(x1 - x2): # if for all error pairs the difference in the row index is at least as large as the difference in the column index
            return False
        # if the differences are equal, then it must be on the correct diagonal
        if abs(y1 - y2) == abs(x1 - x2) : 
            if (x1+y1) % 2 and (x2-x1) > 0 : return False # on odd parity diagonal, must go left
            if (x1+y1) % 2 ==0 and (x1 - x2) > 0 : return False # on even parity diagonal, must go right
    return True

def count_error_patterns(num_qubits, num_errors, code_distance):
    """
    Count the number of error patterns that lead to a logical error.
    
    Parameters:
    - num_qubits: Total number of qubits in the code
    - num_errors: Number of errors to introduce
    - code_distance: Distance of the surface code
    
    Returns:
    - count: Number of error patterns causing a logical error
    """
    count = 0
    for error_indices in combinations(range(num_qubits), num_errors):
        error_pattern = [(i % (code_distance), i // (code_distance)) for i in error_indices]
        if is_vertical_logical_error(error_pattern):
            count += 1
    return count

if __name__=='__main__':
    code_distances = [ 3, 5, 7, 9]  # Example code distance
    for code_distance in code_distances:
        num_qubits = (code_distance) ** 2
        num_errors = (code_distance + 1) // 2
        count = count_error_patterns(num_qubits, num_errors, code_distance)
        print(f"Code distance {code_distance}: {count} error patterns leading to a vertical logical error.")
