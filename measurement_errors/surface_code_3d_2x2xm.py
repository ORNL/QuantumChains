#Corey Fox
#2x2xn (2+1)D rotated surface code. Counting data and measurement error configurations over the weight-2 ancilla qubits.

'''For each syndrome configuration, this script outputs a matrix where the (i,j) entry tells us
how many possible error configurations have a number of i data errors and j measurement errors.
These matrices are saved to the file 'measurement_data_matrix_2x2xm.txt'. '''

'''The number of data errors are only counted as NEW occurances of a data error, due to how they persist in time.
So if a given data qubit has an unchanging data error across subsequent measurements, that would be counted as one data error. 
New data errors are really only counted as changes in the parity (0 or 1) on that data qubit.'''

#This script generalizes the counting in the 'surface_code_3d_2x2_2_plaqs.py' to any M measurements of 2 or more. 

from itertools import product
import numpy as np
import sys

M = 2 #total measurement layers

if M < 2:
    sys.exit("Error: There must be 2 or more measurement rounds to run this script.")

total_ancillas = 4*M
syndrome_combos = product(range(2), repeat=2*M)
data_error_combos = list(product(range(2), repeat=2))
file = open("measurement_data_matrix_2x2xm.txt", "w")


def recursive_count(layer, data_error_1, data_error_2, syndrome_3, syndrome_4, measurement_count, data_count):

    ancilla = layer * 2 - 2
    if layer <= M:
        for data_error_3 in data_error_combos:
            for data_error_4 in data_error_combos:
                data_count += sum(data_error_3) + sum(data_error_4)

                measurement_count[ancilla] = 0
                measurement_count[ancilla + 1] = 0

                #parity check, data error from previous layer carries over.
                if sum([(x + y) % 2 for x,y in zip(data_error_3,data_error_1)]) % 2 != syndrome_3:
                    measurement_count[ancilla] += 1
                if sum([(x + y) % 2 for x,y in zip(data_error_4,data_error_2)]) % 2 != syndrome_4:
                    measurement_count[ancilla + 1] += 1

                if layer < M:
                    recursive_count(layer + 1, data_error_3, data_error_4, syndrome[ancilla], syndrome[ancilla + 1], measurement_count, data_count)
                if layer == M:
                    measure_error_dict[sum(measurement_count)] += 1
                    data_error_dict[data_count] += 1
                    data_measurement_matrix[data_count][sum(measurement_count)] += 1
                data_count -= sum(data_error_3)
                data_count -= sum(data_error_4)

    else:
        return


for syndrome in syndrome_combos:

    measure_error_dict = {}
    for i in range(M*2 + 1):
        measure_error_dict[i] = 0

    data_error_dict = {}
    for i in range(total_ancillas + 1):
        data_error_dict[i] = 0

    data_measurement_matrix = [[0]*(M*2 + 1) for _ in range(total_ancillas + 1)]

    for data_error_1 in data_error_combos: #first ancilla, first layer
        for data_error_2 in data_error_combos: #second ancilla, first layer

            measurement_count = [0]*(M*2) #reset measurement error counts for each new error configuration. Each entry in this list corresponds to an ancilla.

            #Parity check on each of the first layer ancillas
            if sum(data_error_1) % 2 != syndrome[0]:
                measurement_count[0] += 1
            if sum(data_error_2) % 2 != syndrome[1]:
                measurement_count[1] += 1

            recursive_count(2, data_error_1, data_error_2, syndrome[2], syndrome[3], measurement_count, sum(data_error_1) + sum(data_error_2))

    print(f'Syndrome: {syndrome}')
    print(measure_error_dict)
    print(data_error_dict)
    print(np.array(data_measurement_matrix))
    print(f'Total count = {np.sum(data_measurement_matrix)}')
    print('===================================')
    file.write(f'Syndrome: {syndrome}\n')
    file.write(f'{np.array(data_measurement_matrix)}\n')
    file.write(f'Total count = {np.sum(data_measurement_matrix)}\n')
    file.write('===================================\n')




    




file.close()

                
                

     