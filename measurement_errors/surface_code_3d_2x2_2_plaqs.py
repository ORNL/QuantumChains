#Corey Fox
#2x2x2 (2+1)D rotated surface code. Counting data and measurement error configurations over the weight-2 ancilla qubits.

'''For each syndrome configuration, this script outputs a matrix where the (i,j) entry tells us
how many possible error configurations have a number of i data errors and j measurement errors. These matrices are saved
to the file 'measurement_data_matrix_2x2x2.txt'. '''

'''The number of data errors are only counted as NEW occurances of a data error, due to how they persist in time.
So if a given data qubit has an unchanging data error across subsequent measurements, that would be counted as one data error. 
New data errors are really only counted as changes in the parity (0 or 1) on that data qubit. This feature of the script may 
be a little unintutive when trying to imagine what the configurations actually are, but lends itself better to an analysis on
the probability that each configuration occurs with.'''

from itertools import product
import numpy as np

M = 2 #total measurement layers
total_ancillas = 4
syndrome_combos = product(range(2), repeat=4)
data_error_combos = product(range(2), repeat=2)
file = open("measurement_data_matrix_2x2x2.txt", "w")

ancilla_list1 = []
i=0
for l in data_error_combos:
    i+=1
    ancilla_list1 += [l]


for syndrome in syndrome_combos:

    #Create a dictionary to see how many configurations have a given number of measurement or data errors, respectively. 
    measure_error_dict = {
        0 : 0,
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0
    }
    data_error_dict = {
        0 : 0,
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
    }

    
    data_error_combos = ancilla_list1
    data_measurement_matrix = [[0]*5 for _ in range(9)]

    for data_error_1 in data_error_combos: #first ancilla, first layer
        for data_error_2 in data_error_combos: #second ancilla, first layer
            measurement_count = [0,0,0,0] #reset measurements error counts for each new error configuration. Each entry in this list corresponds to an ancilla.

            data_count = sum(data_error_1) + sum(data_error_2)

            #Parity check on each of the first layer ancillas
            if sum(data_error_1) % 2 != syndrome[0]:
                measurement_count[0] += 1
            if sum(data_error_2) % 2 != syndrome[1]:
                measurement_count[1] += 1

            for data_error_3 in data_error_combos: #first ancilla, second layer
                for data_error_4 in data_error_combos: #second ancilla, second layer

                    data_count += sum(data_error_3) + sum(data_error_4)

                    #parity check on second layer depends also on the data error configuration of the previous layer.
                    if sum([(x + y) % 2 for x,y in zip(data_error_3,data_error_1)]) % 2 != syndrome[2]:
                        measurement_count[2] += 1
                    if sum([(x + y) % 2 for x,y in zip(data_error_4,data_error_2)]) % 2 != syndrome[3]:
                        measurement_count[3] += 1

                    measure_error_dict[sum(measurement_count)] += 1
                    data_error_dict[data_count] += 1
                    data_measurement_matrix[data_count][sum(measurement_count)] += 1

                    measurement_count[2] = 0
                    measurement_count[3] = 0
                    data_count = sum(data_error_1) + sum(data_error_2)

    print(f'Syndrome: {syndrome}')
    #print(measure_error_dict)
    #print(data_error_dict)
    print(np.array(data_measurement_matrix))
    print(f'Total count = {np.sum(data_measurement_matrix)}')
    print('===================================')
    file.write(f'Syndrome: {syndrome}\n')
    file.write(f'{np.array(data_measurement_matrix)}\n')
    file.write(f'Total count = {np.sum(data_measurement_matrix)}\n')
    file.write('===================================\n')
file.close()

                
                

     