#This project intends to study the influence of tree density in the diffusion of moisture

#step 1: define tree distribution as function of a paremeter p (probability density)



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

size = 50
moisture = np.random.rand(size,size)

def tree(density, size):
    tree = np.random.choice([0,1], size = (size,size), p = [1 - density,  density])
    return tree

def diffuse(m,D = 0.1):
    new_m = m.copy()
    for i in range(1, size-1):
        for j in range(1, size-1):
            neighbors = [m[i+1,j],m[i-1,j],m[i,j+1],m[i,j-1]]
            new_m[i,j] += D*(np.sum(neighbors - 4*m[i,j]))
    return new_m

def uptake(m, trees, rate = 0.05):
    return m - rate*trees

def loss(m, trees, evap_rate = 0.01, et_rate = 0.03, shade_factor = 0.5):
    # baseline evaporation everywhere
    evap = evap_rate *(1-shade_factor*trees)

    # extra tree transpiration only where trees exist
    et = et_rate *trees

    new_m = m - evap - et
    return np.clip(new_m,0, None)



def rain_input(m, trees, amount = 0.2, infiltration_factor_soil = 0.4, infiltration_factor_trees = 0.2):
    # water normally infiltrates with a certain factor. Sites where trees exists infiltrate more
    return m + amount*infiltration_factor_soil + amount*infiltration_factor_trees*trees

def final_moisture(m, trees, rate, D, amount, sweeps):
    state = m.copy()
    for t in range(sweeps):
        state = diffuse(state, D=D)
        state = loss(state,trees, evap_rate = 0.01, et_rate = 0.03, shade_factor = 0.5)
        state = rain_input(state, trees, amount = 0.2, infiltration_factor_soil = 0.4, infiltration_factor_trees = 0.2)
    return state

def average_moisture(m, trees, rate, D, amount, sweeps):
    final_state = final_moisture(m, trees, rate, D, amount, sweeps)
    average = np.mean(final_state)
    return average


mean_moisture = []
density_list = []
for d in range(1,50):
    density = d* 0.02
    trees = tree(density,50)
    final_state = final_moisture(moisture, trees, 0.3, 0.1, 0.5, 100)
    average = average_moisture(moisture, trees, 0.3, 0.1, 0.5, 100)
    mean_moisture.append(average)
    density_list.append(density)

print(mean_moisture)

plt.plot(density_list, mean_moisture, label = "Mean moisture")
plt.legend()
plt.xlabel("Tree Density")
plt.ylabel("Moisture")
plt.show()













