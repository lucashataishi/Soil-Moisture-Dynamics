import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

size = 50  #Number of pathces of land. Each patch can represent a species in the system
moisture = np.random.rand(size,size)  # Assigns randomly moisture level at each patch. Shouldn't moisture be clusterd?
#moisture = np.zeros((size,size))
trees = np.random.choice([0, 1], size=(size, size), p=[0.8, 0.2])




def diffuse(m, D = 0.1):
    new_m = m.copy()
    for i in range(1, size-1):
        for j in range(1,size-1):
            neighbors = [m[i+1,j],m[i-1,j],
                         m[i,j+1],m[i,j-1]
                         ]
            new_m[i,j] += D *(sum(neighbors) - 4*m[i,j])
    return new_m

def uptake(m, trees, rate = 0.05):
    return m - rate*trees

def loss(m, trees, evap_rate = 0.01, et_rate = 0.03, shade_factor = 0.02):
    # baseline evaporation everywhere
    evap = evap_rate *(1-shade_factor*trees)

    # extra tree transpiration only where trees exist
    et = et_rate *trees

    new_m = m - evap - et
    return np.clip(new_m,0, None)

def rain_input(m, trees, amount = 0.1, infiltration_factor_soil = 1, infiltration_factor_trees = 0.00):
    # water normally infiltrates with a certain factor. Sites where trees exists infiltrate more
    return m + amount*infiltration_factor_soil + amount*infiltration_factor_trees*trees

def animate_moisture(moisture, trees, D = 0.1, rate = 0.5, sweeps=100):
    y, x = np.where(trees == 1)
    fig, ax = plt.subplots(figsize = (8,8))
    im = ax.imshow(moisture, cmap = 'Blues', interpolation = 'bicubic')
    ax.scatter(x,y,c = 'darkgreen', s=10, label = 'Trees')
    title = ax.set_title('Moisture with tree distribtuion')
    plt.colorbar(im, ax=ax, label="Soil Moisture")

    state = moisture.copy()

    def update(frame):
        nonlocal state
        for t in range(sweeps):
            state = diffuse(state, D=D)
            state = loss(state, trees, evap_rate = 0.01, et_rate = 0.03, shade_factor = 0.2)
            state = rain_input(state, trees, amount=0.1, infiltration_factor_soil=1, infiltration_factor_trees=0.0)

        im.set_data(state)
        title.set_text(f"Moisture, sweep={frame + 1}")
        return im, title,




    anim = FuncAnimation(fig, update, frames = sweeps, interval = 10, blit = False,  repeat = False)
    plt.show()
    return anim, state

anim , final_moisture =  animate_moisture(moisture, trees)


average_moisture = np.mean(final_moisture)
print(final_moisture)
print(average_moisture)



#for t in range(100):
#    moisture = diffuse(moisture)
#    moisture = uptake(moisture, trees)
#    moisture = rain_input(moisture)


#y,x = np.where(trees == 1)

#plt.figure(figsize = (8,8))

#Moisture as base layer
#plt.imshow(moisture, cmap = 'Blues', interpolation = 'bicubic')
#plt.colorbar(label="Soil Moisture")

#plt.scatter(x,y,c = 'darkgreen', s = 10, label = "Trees")
#plt.legend()

#plt.title('Soil moisture with tree distribtuion')
#plt.show()

