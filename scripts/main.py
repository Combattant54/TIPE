# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 08:22:54 2026

@author: arthur.woelfel
"""

import environnement
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

POS = [[1, 4], [1.1, 4.05], [1, 0.2], [1.5, 2.5], [5, 1]]
#POS = [[1, 1.9], [1.5, 2], [1, 0.2]]
systems = []
dt = 0.05

inter_distance = []
mean_inter_distance = []
num_personns = []
times = []
pos_pers = [[[], []] for i in range(len(POS))]


COLORS = ["red", "green", "blue", "purple", "orange"]

SIMULATION_NUMBER = 11
PARAMS = {"NUMBER": SIMULATION_NUMBER}

DPI = 100

fig, axis = plt.subplots()

#taille effective de la simulation de la forme ([X0, Y0], [X1, Y1])
SIM_LIMITS = ([-1, -1], [environnement.TAILLE[0] + 1, environnement.TAILLE[1] + 1]) 
axis.set_xlim(SIM_LIMITS[0][0], SIM_LIMITS[1][0])
axis.set_ylim(SIM_LIMITS[0][1], SIM_LIMITS[1][1])


fig.set_dpi(DPI)
PIXEL_SIZE = fig.get_size_inches()*fig.dpi
SIM_SIZE = (SIM_LIMITS[1][0] - SIM_LIMITS[0][0], SIM_LIMITS[1][1] - SIM_LIMITS[0][1])

DISPLAY_SIZE = (environnement.RADIUS * 2 * PIXEL_SIZE[1] / SIM_SIZE[1])**2

time = 0

X, Y = zip(*POS)

RECTS = []

# DISPLAY_SIZE = (environnement.RADIUS * DPI)**2

try:
    system = axis.scatter(X, Y, color=COLORS[:len(X)], s = [DISPLAY_SIZE]*len(X))
    
except Exception as e:
    print(X)
    print(Y)
    print(COLORS[:len(X)])
    raise e

def init():
    global RECTS
    print("Initializing simulation N°" + str(SIMULATION_NUMBER))
    print(f"initializing environnment with {len(POS)} personns")
    environnement.init(POS, [], [])
    env_params = environnement.gather_parameters()
    for k in env_params:
        PARAMS[k] = env_params[k]
    print(PARAMS)
    
    RECTS = environnement.build_rect()
    for rect in RECTS:
        axis.add_patch(rect)
        
    print("Initialisation finalized")
    
def update(frame):
    global time
    if len(environnement.PERSONNES_ACTIVES) >= 1:
        I = environnement.inter_perdestrian_distance_metric()
        I_mean = I / len(environnement.PERSONNES_ACTIVES)
    else:
        I = 0
        I_mean = 0
    
    inter_distance.append(I)
    mean_inter_distance.append(I_mean)
    num_personns.append(len(environnement.PERSONNES_ACTIVES))
    
    L = []
    for i in range(len(POS)):
        P_i = environnement.pos_pers(i)
        pos_pers[i][0].append(P_i[0])
        pos_pers[i][1].append(P_i[1])
        L.append(P_i)

    system.set_offsets(L)
    
    times.append(time)
    
    environnement.perform_time_step(dt)
    time = time + dt
    
    return RECTS

def display():
    fig, (ax0, ax1) = plt.subplots(2)
    ax0.plot(times, inter_distance, "r")
    ax0.set_title("Inter distance (m) - time (s)")
    
    ax1.plot(times, mean_inter_distance, "b")
    ax1.set_title("Mean inter distance (m) - time (s)")
    
    plt.show()
    
    for i in range(len(POS)):
        pos_pers_x, pos_pers_y = pos_pers[i]
        plt.scatter(pos_pers_x, pos_pers_y, c=[COLORS[i]]*len(pos_pers_x), s=[DISPLAY_SIZE]*len(pos_pers_x))
    plt.title(f"Positions in simulation n°{SIMULATION_NUMBER}")
    plt.show()
    
def main():
    pass
    animation = FuncAnimation(fig=fig, func=update, frames=int(12/dt), interval = dt*1000, repeat = False, blit = True)
    animation.save(f"../results/ANIM_SIM_{SIMULATION_NUMBER}.gif", dpi=DPI)
    
    display()


if __name__ == "__main__":
    init()
    main()