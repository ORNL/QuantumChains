// count_partial_chain_gmp.cpp
// (c) Shaked Regev 2025

// Lower-bound the logical error of a rotated surface code

// Qubits lie on a d×d square lattice (d odd).
// Only X errors are considered.
// Assuming an ideal maximum likelihood decoder,
// 	- Fewer than d/2 errors will always be decoded correctly
//  - More than d/2 errors lying on a top-to-bottom chain will be decoded incorrectly (=> logical error)
// Thus, the number of configurations of d′=(d+1)/2 chain-like errors is a lower bound
// on the number of configurations that result in logical Z error.
// Multiplying by p^d′ * (1-p)^(d^2-d′) yields a lower bound on the probability of
// a logical Z error.
#include <iostream>
#include <vector>
#include <stdexcept>
#include <algorithm>
#include <utility>
#include <chrono>
#include <gmpxx.h>  // GNU Multiple Precision Arithmetic Library C++ interface

// Use GMP's C++ interface for arbitrary precision integers
using BigInt = mpz_class;

class ConfigCounter {
private:
    int d, tmax;
    std::vector<std::vector<std::vector<BigInt>>> memo;
    
    // Helper function to get column range for row r_ in the cone rooted at (r,c)
    std::pair<int, int> colrange(int r, int c, int r_) {
        int k = r - r_;
        if (k <= 0) {
            throw std::runtime_error("r_ must be less than r");
        }
        
        int lo, hi;
        if ((r + c) % 2 == 1) { // isodd(r+c)
            lo = c - k;
            hi = c + k - 1;
        } else {
            lo = c - k + 1;
            hi = c + k;
        }
        
        return {std::max(lo, 1), std::min(hi, d)};
    }
    
    // Recursive function to count configurations
    BigInt count_configs_recursive(int t, int r, int c) {
        // Only 1 way to arrange 1 error
        if (t == 1) {
            return BigInt(1);
        }
        
        // Check if we have computed this before
        int it = t - std::max(1, r + tmax - d);
        if (it >= 0 && it < static_cast<int>(memo[r-1][c-1].size()) && memo[r-1][c-1][it] > 0) {
            return memo[r-1][c-1][it];
        }
        
        // First time here. Compute the answer
        BigInt num(0);
        
        // Loop over row of next error
        for (int r_ = std::max(t-1, 1); r_ < r; r_++) {
            // Loop over column of next error
            auto [lo, hi] = colrange(r, c, r_);
            for (int c_ = lo; c_ <= hi; c_++) {
                num += count_configs_recursive(t-1, r_, c_);
            }
        }
        
        // Save the result in lookup table
        if (it >= 0 && it < static_cast<int>(memo[r-1][c-1].size())) {
            memo[r-1][c-1][it] = num;
        }
        
        return num;
    }
    
public:
    BigInt count_configs(int d_val, int t_val) {
        // Validate inputs
        if (d_val <= 0 || d_val % 2 == 0) {
            throw std::runtime_error("d must be an odd whole number");
        }
        if (t_val < 0) {
            throw std::runtime_error("t must be >= 0");
        }
        if (t_val == 0) {
            return BigInt(1);
        }
        
        d = d_val;
        tmax = t_val;
        
        // Initialize memoization table
        memo.assign(d, std::vector<std::vector<BigInt>>(d));
        for (int r = 1; r <= d; r++) {
            for (int c = 1; c <= d; c++) {
                int size = 1 + std::min(r, t_val) - std::max(1, r + t_val - d);
                if (size > 0) {
                    memo[r-1][c-1].assign(size, BigInt(0));
                }
            }
        }
        
        // Enumerate all configurations
        BigInt num(0);
        for (int r = t_val; r <= d; r++) {        // loop over row of first error
            for (int c = 1; c <= d; c++) {        // loop over column of first error
                num += count_configs_recursive(t_val, r, c);
            }
        }
        
        return num;
    }
};

int main(int argc, char* argv[]) {
    ConfigCounter counter;
    int d, t;   
    if (argc >= 2) {
        d = std::stoi(argv[1]);
    } else {
        std::cout << "Enter odd code distance d (e.g., 5): ";
        std::cin >> d;
    }
    t = (d + 1) / 2; 
    
    auto start = std::chrono::high_resolution_clock::now();
    BigInt num = counter.count_configs(d, t);
    auto end = std::chrono::high_resolution_clock::now();
    
    std::cout << "d=" << d << ", t=" << t << ", num configurations = " << num << std::endl;
    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Computation time: " << duration.count() << " ms" << std::endl;
    return 0;
}