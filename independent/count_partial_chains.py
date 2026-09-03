"""
count_partial_chains.py
(c) Shaked Regev 2025

Lower-bound the logical error of a rotated surface code

Qubits lie on a d×d square lattice (d odd).
Only X errors are considered.
Assuming an ideal maximum likelihood decoder:
    - Fewer than d/2 errors will always be decoded correctly
    - More than d/2 errors lying on a top-to-bottom chain will be decoded incorrectly (=> logical error)
    
Thus, the number of configurations of d′=(d+1)/2 chain-like errors is a lower bound
on the number of configurations that result in logical Z error.
Multiplying by p^d′ * (1-p)^(d^2-d′) yields a lower bound on the probability of
a logical Z error.
"""

import time
from typing import Dict, Tuple


class ConfigCounter:
    """Count partial chain configurations in a rotated surface code."""
    
    def __init__(self):
        self.d = None
        self.tmax = None
        self.memo = None
    
    def colrange(self, r: int, c: int, r_: int) -> Tuple[int, int]:
        """
        Get the column range for row r_ in the cone rooted at (r, c).
        
        Args:
            r: Root row
            c: Root column
            r_: Target row (must be less than r)
            
        Returns:
            Tuple of (lo, hi) representing the valid column range
        """
        k = r - r_
        if k <= 0:
            raise ValueError("r_ must be less than r")
        
        # Determine if (r + c) is odd
        is_odd = (r + c) % 2 == 1
        
        if is_odd:
            lo = c - k
            hi = c + k - 1
        else:
            lo = c - k + 1
            hi = c + k
        
        # Clamp to grid boundaries [1, d]
        lo = max(lo, 1)
        hi = min(hi, self.d)
        
        return (lo, hi)
    
    def count_configs_recursive(self, t: int, r: int, c: int) -> int:
        """
        Recursively count chain-like error configurations.
        
        Args:
            t: Number of errors in the chain
            r: Current row position
            c: Current column position
            
        Returns:
            Number of valid configurations
        """
        # Base case: only 1 way to arrange 1 error
        if t == 1:
            return 1
        
        # Check memoization table
        it = t - max(1, r + self.tmax - self.d)
        if (it >= 0 and 
            it < len(self.memo[r-1][c-1]) and 
            self.memo[r-1][c-1][it] is not None):
            return self.memo[r-1][c-1][it]
        
        # Compute the number of configurations
        num = 0
        
        # Loop over row of next error in the chain
        for r_ in range(max(t - 1, 1), r):
            # Loop over column of next error
            lo, hi = self.colrange(r, c, r_)
            for c_ in range(lo, hi + 1):
                num += self.count_configs_recursive(t - 1, r_, c_)
        
        # Save to memoization table
        if it >= 0 and it < len(self.memo[r-1][c-1]):
            self.memo[r-1][c-1][it] = num
        
        return num
    
    def count_configs(self, d_val: int, t_val: int) -> int:
        """
        Count the total number of chain-like error configurations.
        
        Args:
            d_val: Code distance (must be odd)
            t_val: Length of chain (usually (d+1)/2)
            
        Returns:
            Number of valid configurations
            
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate inputs
        if d_val <= 0 or d_val % 2 == 0:
            raise ValueError("d must be an odd positive integer")
        if t_val < 0:
            raise ValueError("t must be >= 0")
        if t_val == 0:
            return 1
        
        self.d = d_val
        self.tmax = t_val
        
        # Initialize memoization table
        # memo[r][c][it] stores the count for position (r+1, c+1) and time index it
        self.memo = [[[] for _ in range(self.d)] for _ in range(self.d)]
        
        for r in range(1, self.d + 1):
            for c in range(1, self.d + 1):
                # Calculate the size needed for this (r, c) position
                min_it = max(1, r + t_val - self.d)
                max_it = min(r, t_val)
                size = 1 + max_it - min_it
                
                if size > 0:
                    # Initialize with None values
                    self.memo[r-1][c-1] = [None] * size
        
        # Enumerate all configurations
        num = 0
        for r in range(t_val, self.d + 1):      # loop over row of first error
            for c in range(1, self.d + 1):      # loop over column of first error
                num += self.count_configs_recursive(t_val, r, c)
        
        return num


def main():
    """Main entry point."""
    import sys
    
    # Get code distance from command line or user input
    if len(sys.argv) >= 2:
        d = int(sys.argv[1])
    else:
        d = int(input("Enter odd code distance d (e.g., 5): "))
    
    # Calculate chain length
    t = (d + 1) // 2
    
    # Count configurations
    counter = ConfigCounter()
    start_time = time.time()
    num_configs = counter.count_configs(d, t)
    end_time = time.time()
    
    # Output results
    elapsed_ms = (end_time - start_time) * 1000
    print(f"d={d}, t={t}, num configurations = {num_configs}")
    print(f"Computation time: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()
