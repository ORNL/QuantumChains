from itertools import product
import numpy as np
import ast
#----------------------------------------------------------------------

def get_stabilizers_plaquettes(d : int):
    '''
    Creates stabilizer and plaquette matrices. Generally, the definition of plaquettes here can be Z-stabilizers, and the
    definition of stabilizers can be X-stabilizers.
    
    Parameter:
    - d : distance of the surface code.

    Returns:
    - plaquettes : list of matrices that correspond to the location of adjacent data qubits for each plaquette of a single error type (Z or X).
    - stabilizers : list of matrices that correspond to the plaquettes of the other error type, functionally can be applied as a stabilizer.
    '''
    #plaquettes. number of z plaquettes is (d^2-1)/2. number of z plaquettes in a row is (d-3)/2 + 2, d>2, odd d
    plaquettes = [[[0]*d for _ in range(d)] for _ in range((d**2-1)//2)]


    #This creates a list where each element corresponding to its plaquette is 0 for weight-4 and 1 for weight-2.
    plaquette_pattern = ([0] * ((d - 3) // 2 + 1) + [1] * 2 + [0] * ((d - 3) // 2 + 1)) * ((d - 1) // 2)


    #loop over every plaquette. Index goes from 0 to the total - 1.
    for plaquette in range((d**2 - 1) // 2 ):

        #if weight-2 plaquette
        if plaquette_pattern[plaquette] == 1:

            '''((plaquette + (((d - 3) // 2 + 2) % 2)) % 2) is 1 if the row index is even (odd) and
            the number of Z plaquettes in a single row is odd (even). 0 for even-even and odd-odd. 
            This setup determines if the weight-2 is on the far right or far left of the lattice, making
            it easier to know which data qubits are adjacent to the corresponding plaquette'''
            plaquettes[plaquette][plaquette // ((d - 3) // 2 + 2)][(d - 1) * ((plaquette + (((d - 3) // 2 + 2) % 2)) % 2)] += 1
            plaquettes[plaquette][plaquette // ((d - 3) // 2 + 2) + 1][(d - 1) * ((plaquette + (((d - 3) // 2 + 2) % 2)) % 2)] += 1 #down one row

        #if weight-4 plaquette
        if plaquette_pattern[plaquette] == 0:

            plaquettes[plaquette][plaquette // ((d - 3) // 2 + 2)][((plaquette - (plaquette // ((d - 3) // 2 + 2)) % 2) % ((d - 3) // 2 + 2)) * 2 + ((plaquette // ((d - 3) // 2 + 2)) % 2)] += 1
            plaquettes[plaquette][plaquette // ((d - 3) // 2 + 2)][((plaquette - (plaquette // ((d - 3) // 2 + 2)) % 2) % ((d - 3) // 2 + 2)) * 2 + ((plaquette // ((d - 3) // 2 + 2)) % 2) + 1] += 1 #over one column
            plaquettes[plaquette][plaquette // ((d - 3) // 2 + 2) + 1][((plaquette - (plaquette // ((d - 3) // 2 + 2)) % 2) % ((d - 3) // 2 + 2)) * 2 + ((plaquette // ((d - 3) // 2 + 2)) % 2)] += 1 #down one row
            plaquettes[plaquette][plaquette // ((d - 3) // 2 + 2) + 1][((plaquette - (plaquette // ((d - 3) // 2 + 2)) % 2) % ((d - 3) // 2 + 2)) * 2 + ((plaquette // ((d - 3) // 2 + 2)) % 2) + 1] += 1 #over one column, down one row

    #stabilizers
    #reverse rows, then transpose. Same as rotating the surface code by 90 degrees and swapping x and z plaquettes.
    stabilizers = []
    for plaquette in plaquettes:
        plaquette = [row[::-1] for row in plaquette]
        stabilizers.append([list(row) for row in zip(*plaquette)])

    return plaquettes, stabilizers


