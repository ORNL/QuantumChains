# QuantumChains

## Getting started

```
git clone git@code.ornl.gov:szb/logical_errors_rotated_surface_codes.git
```

## Overview
$`d`$ is the code distance of a rotated surface code, assumed to be odd.
The codes in this repo count the number of configurations of $`d_e=(d+1)/2`$ physical errors that produce a vertical logical error.
All codes in this repo produce the same result.

### Straightforward Julia, limit d=67, recommended for readability.
Implements Algorithm 1 with uint 128 in julia. Limited due to integer overflow. $`d=67`$ takes ~100ms.
```
julia count_partial_chains.jl
```

### Most performant (only slightly faster than julia), limit d=67.
Implements Algorithm 1 with uint 128 in C++. Limited due to integer overflow. $`d=67`$ takes ~75ms.
```
g++ -std=c++2c -O2 count_partial_chains.cpp 
./a.out 67
```
GNU Multiple Precision Arithmetic Library C++ interface
### GMP dependency, no distance limit, very performant.
Implements Algorithm 1 with GMP (GNU Multiple Precision Arithmetic Library C++ interface) dependency. Works for arbitrary distances and is very fast. About 14s on a laptop for $`d=127`$.
```
g++ -O3 -I$(brew --prefix gmp)/include -L$(brew --prefix gmp)/lib count_partial_chains_gmp.cpp -lgmpxx -lgmp -o count_partial_chains_gmp
./count_partial_chains_gmp 127
```

### Memoized python code
Slower than the julia and C++ counterparts, but still quite fast.
```
python3 count_partial_chains.py 67
```

### Readable but slow python code
```
python3 surface_code_logical_error.py
```

## Log error counts by cluster counts
If the probability of a certain error configuration is related to how many physical error clusters it has, 
use this code to get a CSV file of configuration counts by cluster count. 
The sum will always equal the output of the previous code. 
```
julia count_partial_chains_clusters.jl 67   
```
## Authors
Shaked Regev and Ryan Bennink, Oak Ridge National Lab.

## Acknowledgment
Thanks to Andrea Delgado who contributed substantially to the algorithm verification.
