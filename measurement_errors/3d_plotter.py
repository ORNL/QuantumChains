import matplotlib.pyplot as plt
import numpy as np
from functions import get_stabilizers_plaquettes
depthshade = 0


z_stabilizers, x_stabilizers = get_stabilizers_plaquettes(3)

for i in range(len(z_stabilizers)):
    z_stabilizers[i] = [item for row in z_stabilizers[i] for item in row]
    x_stabilizers[i] = [item for row in x_stabilizers[i] for item in row]

fig = plt.figure()
ax = plt.axes(projection='3d')

z = np.linspace(0,5,100)
x = np.array([0.5]*100)
y = np.array([0.5]*100)

lw = 3
lw2 = 2
#----------------------------Data qubits-----------------------------------
#first row
ax.plot3D(np.array([1]*100),np.array([1]*100),z, 'green', lw=lw2, label = "Physical Qubits in Time")
ax.plot3D(np.array([1]*100),np.array([2]*100),z, 'green', lw=lw2)
ax.plot3D(np.array([1]*100),np.array([3]*100),z, 'green', lw=lw2)

#second row
ax.plot3D(np.array([2]*100),np.array([1]*100),z, 'green', lw=lw2)
ax.plot3D(np.array([2]*100),np.array([2]*100),z, 'green', lw=lw2)
ax.plot3D(np.array([2]*100),np.array([3]*100),z, 'green', lw=lw2)

#third row
ax.plot3D(np.array([3]*100),np.array([1]*100),z, 'green', lw=lw2)
ax.plot3D(np.array([3]*100),np.array([2]*100),z, 'green', lw=lw2)
ax.plot3D(np.array([3]*100),np.array([3]*100),z, 'green', lw=lw2)

s=50
for i in [1,3,5]:
    for j in range(1,4):
        ax.scatter([j],[1,2,3],[i], color='black', facecolor = 'none', depthshade=depthshade, s=s)

ax.scatter([1],[1],[1], color='black', depthshade=depthshade, facecolor = 'none', s=s, label = "Physical Qubits")

def d_e_plotter(qubit, layer):
    ax.scatter([(qubit - 1) // 3 + 1],[(qubit - 1) % 3 + 1],[2*layer - 1], color='yellow', depthshade=0, s=s+0.5)
#-------------------------------------------------------------------------------------


#---------------------------Ancilla qubits------------------------------
ax.plot3D(np.array([1.5]*100),np.array([1.5]*100),z, 'blue', lw=lw, label = "Stabilizer Qubits in Time")
ax.plot3D(np.array([1.5]*100),np.array([3.5]*100),z, 'blue', lw=lw)
ax.plot3D(np.array([2.5]*100),np.array([0.5]*100),z, 'blue', lw=lw)
ax.plot3D(np.array([2.5]*100),np.array([2.5]*100),z, 'blue', lw=lw)

ax.scatter([1.5],[1.5],[1,3,5], color = 'black', facecolor = 'none', depthshade=depthshade, s=s, label = "Stabilizer Qubits")
ax.scatter([1.5],[3.5],[1,3,5], color = 'black', facecolor = 'none', depthshade=depthshade, s=s)
ax.scatter([2.5],[0.5],[1,3,5], color = 'black', facecolor = 'none', depthshade=depthshade, s=s)
ax.scatter([2.5],[2.5],[1,3,5], color = 'black', facecolor = 'none', depthshade=depthshade, s=s)

def ancilla_plotter(qubit, layer): #Changes given ancilla color to red
    match qubit:
        case 1:

            x = [1.5]
            y = [1.5]

        case 2:

            x = [1.5]
            y = [3.5]

        case 3:

            x = [2.5]
            y = [0.5]

        case 4:

            x = [2.5]
            y = [2.5]

    ax.scatter(x,y,[2*layer - 1], color = 'red', depthshade=0, s=s)

def m_e_plotter(qubit, layer): #indicates measurement errors 
    match qubit:
        case 1:

            x = [1.5]
            y = [1.5]

        case 2:

            x = [1.5]
            y = [3.5]

        case 3:

            x = [2.5]
            y = [0.5]

        case 4:

            x = [2.5]
            y = [2.5]

    #ax.scatter(x,y,[2*layer - 1], edgecolor = 'blue', facecolor = 'none', depthshade=0, s=s+0.5)
    ax.scatter(x,y,[2*layer - 1], color = 'yellow', depthshade=0, s=s/4)

#------------------------------------------------------------------------------------------

#-------------------------------errors--------------------------------
#change the config to whatever you want to see
error_config = [[0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]

syndrome1_data_only = [sum([x * y for x, y in zip(error_config[0], z_stabilizers[i])]) % 2 for i in range(4)]
syndrome1 = [(x + y) % 2 for x, y in zip(syndrome1_data_only, error_config[3][:4])]

syndrome2 = [sum([x * y for x, y in zip(error_config[1], z_stabilizers[i])]) % 2 for i in range(4)]
syndrome2_data_only = [(x + y) % 2 for x, y in zip(syndrome1_data_only, syndrome2)]
syndrome2 = [(x + y + z) % 2 for x, y, z in zip(syndrome1_data_only, syndrome2, error_config[3][4:8])]

syndrome3 = [sum([x * y for x, y in zip(error_config[2], z_stabilizers[i])]) % 2 for i in range(4)]
syndrome3_data_only = [(x + y) % 2 for x, y in zip(syndrome2_data_only, syndrome3)]
syndrome3 = [(x + y + z) % 2 for x, y, z in zip(syndrome2_data_only, syndrome3, error_config[3][8:12])]

syndrome = [syndrome1, syndrome2, syndrome3]

syndrome_non_trivial = [syndrome[0],[(syndrome[1][i] + syndrome[0][i]) % 2 for i in range(4)],[(syndrome[2][i] + syndrome[1][i]) % 2 for i in range(4)]]
syndrome = syndrome_non_trivial

for layer in range(len(syndrome)): #Plot syndrome measurements. Only turn red when the ancilla changes parity
    for ancilla in range(len(syndrome[layer])):
        if syndrome[layer][ancilla]:
            ancilla_plotter(ancilla + 1,layer + 1)

for m_e in range(len(error_config[3])): #plot measurement errors. Ancilla that are yellow indicate measurement errors.
    if error_config[3][m_e]:
        m_e_plotter(m_e % 4 + 1, m_e // 4 + 1)

for layer in range(3): #plot data errors, only yellow when a new data error is applied.
    for data_qubit in range(len(error_config[layer])):
        if error_config[layer][data_qubit]:
            d_e_plotter(data_qubit + 1, layer + 1)
#-----------------------------------------------------------------------


ax.set_ylim([0,4])
ax.set_xlim([0,4])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Time (t)')

#plt.legend()

#2D planes that separate the measurement rounds. Use them at your own risk
x,y = np.meshgrid(np.linspace(0,4,50), np.linspace(0,4,50))
'''ax.plot_surface(x,y, np.full_like(x, 1), color = 'cyan', alpha = 0.2)
ax.plot_surface(x,y, np.full_like(x, 3), color = 'magenta', alpha = 0.2)
ax.plot_surface(x,y, np.full_like(x, 5), color = 'yellow', alpha = 0.2)'''





plt.show()