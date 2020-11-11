import matplotlib.pyplot as plt
import numpy as np
from grid.grid import Grid
from maps.domain import Domain, Pop, Res, State

from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image




niter = 200
scale = 20
lenN = 15

dt = 0.01
dx = 10 #km

Europe = Domain('maps/europe')
Europe.resize(dx)

count = 0
start = []
Nstart = []

while(count) < lenN:
    i = np.random.randint(10, Europe.shape[0]-10)
    j = np.random.randint(10, Europe.shape[1]-10)

    if Europe.I[i,j] != 0:
        count +=1
        start.append([i,j])
        Nstart.append(100)

N = Pop(start, #array with starting location coordonates
        Nstart, #start populations (pop)
        0.5, #maximum consumption rate per person (pop^-1.year^-1)
        10, #R needed to reach half of maximum consumption rate (res)
        4, #population generated by max consumption (pop)
        0.02, #pop natural death rate (year^-1)
        100, # carrying capacity (pop)
        10, #Diffusion coefficient (km^2/year)
        10,) #Drift coefficient (km^2/(year res))


R =  Res(0.5, #resource natural growth
         200) #resource carrying capacity

sim = Grid(N,
           R,
           Europe,
           1, # production rate (money.resource^-1.year^-1)
           1, # eps -- ressource extraction capacity (%)
           0.01, #C growth rate (year^-1)
           0.01, #alpha -- production taxation (%.year^-1)
           1, #barbarian population
           dt)


fig, ax = plt.subplots()
plt.axis('off')


im=plt.imshow(sim.get_img())
ax.set_title(f'Year: 0')


def animate(i):
    for _ in range(scale):
        sim.update()
    im.set_array(sim.get_img())
    ax.set_title(f'Year: {i*scale*dt}')

    print(f"step {i}\r", sep=' ', end='', flush=True)
    return [im]

writer = PillowWriter(fps=15)
anim = FuncAnimation(fig, animate, frames = niter, blit=False, interval = 100)
anim.save('out.gif', writer=writer)
#plt.show()
