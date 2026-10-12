'''This script outputs 2 files, one that gives information on every weight-2 error config,
 and the other contains only the configs that are incorrectly corrected. Takes around 2-3 hours to run'''
#3x3x3 

from functions import get_stabilizers_plaquettes
import numpy as np
from itertools import product, chain, combinations
import time
start_time = time.perf_counter()
np.set_printoptions(linewidth=np.inf)

p = 0.002 #Error rate

z_stabilizers, x_stabilizers = get_stabilizers_plaquettes(3)

for i in range(len(z_stabilizers)):
    z_stabilizers[i] = [item for row in z_stabilizers[i] for item in row]
    x_stabilizers[i] = [item for row in x_stabilizers[i] for item in row]

syndrome_list = []
for i in product(range(2), repeat=4):
    syndrome_list += [list(i)]

data_syndrome_matrix = [[0]*16 for _ in range(10)] #16 columns for each syndrome. 10 rows for 0-9 number of data errors.

coset_matrix = [[0]*16 for _ in range(2)] #Cosets are identified by the syndrome they belong to(columns), and parity of its weight(row 0 = even, row 1 = odd)

coset_row = []
for i in product(range(2), repeat=3):
    coset_row += [list(i)]

coset_column = []
for i in product(range(2), repeat=12):
    coset_column += [list(i)]

#Calculate matrix that corresponds to the number of configurations on the 2D lattice that have a given syndrome(column index) based on the number of data errors(row index)
for data_config in product(range(2), repeat=9):

    data_config = list(data_config)

    parity_list = [sum([x * y for x, y in zip(data_config, z_stabilizers[i])]) % 2 for i in range(4)] #Parity check
   
    data_errors = sum(data_config)

    data_syndrome_matrix[data_errors][syndrome_list.index(parity_list)] += 1


#collect all possible weight-2 error configs over the 3x3x3
configs = []
for i1,i2 in combinations(range(39), 2):
    config = [0]*39
    config[i1] += 1
    config[i2] += 1
    configs += [config]

config_list = [[configs[i][:9], configs[i][9:18], configs[i][18:27], configs[i][27:]] for i in range(741)] #indices 0,1,2 correspond to layers 1,2,3. Index 3 corresponds to all 3 layers of ancillas.

config_list_error = []


count = 0
count_bad_configs = 0

with open('weight_2_3x3x3.txt', 'w') as all_file, open('w_2_d_3_errors.txt', 'w') as error_file:
    for error_config in config_list: #loop over all weight-2 errors

        time1 = time.perf_counter()
        count += 1
        print(f'Running config #{count} ...')

        #Calculate syndromes, with and without measurement errors
        syndrome1_data_only = [sum([x * y for x, y in zip(error_config[0], z_stabilizers[i])]) % 2 for i in range(4)]
        syndrome1 = [(x + y) % 2 for x, y in zip(syndrome1_data_only, error_config[3][:4])]

        syndrome2 = [sum([x * y for x, y in zip(error_config[1], z_stabilizers[i])]) % 2 for i in range(4)]
        syndrome2_data_only = [(x + y) % 2 for x, y in zip(syndrome1_data_only, syndrome2)]
        syndrome2 = [(x + y + z) % 2 for x, y, z in zip(syndrome1_data_only, syndrome2, error_config[3][4:8])]

        syndrome3 = [sum([x * y for x, y in zip(error_config[2], z_stabilizers[i])]) % 2 for i in range(4)]
        syndrome3_data_only = [(x + y) % 2 for x, y in zip(syndrome2_data_only, syndrome3)]
        syndrome3 = [(x + y + z) % 2 for x, y, z in zip(syndrome2_data_only, syndrome3, error_config[3][8:12])]



        coset_matrix = [[0]*16 for _ in range(2)]

        #Now loop over the data_syndrome_matrix for all three layers, this calculates the probability of every possible error config occuring, given the measured syndrome, and collects the probabilities into respective cosets.
        #Layer 3
        for i in range(len(data_syndrome_matrix)):
            for j in range(len(data_syndrome_matrix[0])):

                #layer 2
                for a in range(len(data_syndrome_matrix)):
                    for b in range(len(data_syndrome_matrix[0])):
                        
                        #Layer 1
                        for x in range(len(data_syndrome_matrix)):
                            for y in range(len(data_syndrome_matrix[0])): 

                                coset_row_key = (a+x+i)%2 #number of data errors that show up on the third layer

                                coset_column_key = int("".join(str(num) for num in [(q + r + s)%2 for q, r, s in zip(syndrome_list[y], syndrome_list[b], syndrome_list[j])]), 2) 

                                measurement_errors = (
                                    sum((p1 + s1) % 2 + (p1 + p2 + s2) % 2 + (p1 + p2 + p3 + s3) % 2 for p1, p2, p3, s1, s2, s3 in zip(syndrome_list[y], syndrome_list[b], syndrome_list[j], syndrome1, syndrome2, syndrome3))
                                )

                                coset_matrix[coset_row_key][coset_column_key] += data_syndrome_matrix[i][j] * data_syndrome_matrix[a][b] * data_syndrome_matrix[x][y] * (p)**(i + a + x + measurement_errors) * (1-p)**(39 - (i + a + x + measurement_errors))



        coset_matrix = np.array(coset_matrix)
        normalized_coset_matrix = coset_matrix / np.sum(coset_matrix)

        row, col = np.unravel_index(np.argmax(normalized_coset_matrix), normalized_coset_matrix.shape)

        probability = normalized_coset_matrix[row,col]
        likely_syndrome = coset_column[col][-4:]
        all_file.write(f'Config #{count}\n')
        all_file.write(f'error config {error_config}\n')
        all_file.write(f'Measured syndrome{syndrome1} (first layer)\n')
        all_file.write(f'                 {syndrome2} (second layer)\n')
        all_file.write(f'                 {syndrome3} (third layer)\n')
        all_file.write(f'syndrome from data errors: {syndrome3_data_only}\n')
        all_file.write(f'Most likely syndrome {likely_syndrome} | Even or odd: {row} | probability {probability*100}%\n')

        #Check if max-likelihood decoder applies wrong correction
        if (likely_syndrome != syndrome3_data_only) or (sum(error_config[0] + error_config[1] + error_config[2]) % 2 != row): 
            config_list_error += [error_config]
            count_bad_configs += 1

            all_file.write(f'!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!\n')
            error_file.write(f'Config #{count}\n')
            error_file.write(f'error config {error_config}\n')
            error_file.write(f'syndrome from data errors: {syndrome3_data_only}\n')
            error_file.write(f'Most likely syndrome {likely_syndrome} | Even or odd: {row} | probability {probability*100}%\n')
            error_file.write(f'-----------------------------------------------\n')

        else:
            all_file.write(f'CLEAR\n')
        all_file.write(f'-----------------------------------------------\n')

        time2 = time.perf_counter()
        print(f'Config #{count} complete, {time2 - time1} seconds elapsed!\n')

    error_file.write(f'Total configurations {count_bad_configs}\n')

end_time = time.perf_counter()
print(f'{end_time - start_time} seconds')

        


        

        



        







