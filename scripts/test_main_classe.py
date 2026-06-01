import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

from environnement_classe import Simulation
from personnes_classe import Personne
import time


#POS = [[1, 4], [1.1, 4.05], [1, 0.2], [1.5, 2.5], [5, 1]]
POS = [[1, 4], [1, 4.1]]
OBJECTIFS = [[[9, 4], [10, 6]]] 
OBSTACLE_RECTS = [[[6, -1], [7, 5]], [[6, 6],[7, 11]]]
RADIUS = 0.2

#POS = [[1, 1.9], [1.5, 2], [1, 0.2]]
systems = []
dt = 0.05

inter_distance = []
mean_inter_distance = []
num_personns = []
times = []
pos_pers = [[[], []] for i in range(len(POS))]


COLORS = ["red", "green", "blue", "purple", "orange"]

SIMULATION_NUMBER = 15
PARAMS = {"NUMBER": SIMULATION_NUMBER}

DPI = 200

fig, axis = plt.subplots()

TAILLE = [10, 10]
#taille effective de la simulation de la forme ([X0, Y0], [X1, Y1])
SIM_LIMITS = ([-1, -1], [TAILLE[0] + 1, TAILLE[1] + 1]) 
axis.set_xlim(SIM_LIMITS[0][0], SIM_LIMITS[1][0])
axis.set_ylim(SIM_LIMITS[0][1], SIM_LIMITS[1][1])


fig.set_dpi(DPI)
PIXEL_SIZE = fig.get_size_inches()*fig.dpi
SIM_SIZE = (SIM_LIMITS[1][0] - SIM_LIMITS[0][0], SIM_LIMITS[1][1] - SIM_LIMITS[0][1])

#DISPLAY_SIZE = (RADIUS * 2 * PIXEL_SIZE[1] / SIM_SIZE[1])**2
DISPLAY_SIZE = (RADIUS * 40)**2

X, Y = zip(*POS)


def build_foule(radius, pos):
    F = []
    for i, pos in enumerate(pos):
        p = Personne(radius[i], pos)
        F.append(p)
    
    return F

def build_pers_data(n, bl_boundary, tr_boundary):
    X = np.random.uniform(bl_boundary[0], tr_boundary[0], (n))
    Y = np.random.uniform(bl_boundary[1], tr_boundary[1], (n))

    return list(zip(X, Y))
    
def display(P):
    #fig, (ax0, ax1) = plt.subplots(2)
    #ax0.plot(times, inter_distance, "r")
    #ax0.set_title("Inter distance (m) - time (s)")
    
    #ax1.plot(times, mean_inter_distance, "b")
    #ax1.set_title("Mean inter distance (m) - time (s)")
    
    #plt.show()
    
    for i in range(len(P)):
        pos_pers_x, pos_pers_y = P[i]
        plt.scatter(pos_pers_x, pos_pers_y, c=[COLORS[i]]*len(pos_pers_x), s=[DISPLAY_SIZE]*len(pos_pers_x))
    plt.title(f"Positions in simulation n°{SIMULATION_NUMBER}")
    plt.show()
    

def main():
    sim = Simulation(objectifs=OBJECTIFS, rect_obstacles=OBSTACLE_RECTS, taille=[10, 10], radius = RADIUS)
    sim.init_foule(build_foule([RADIUS] * len(POS), POS))
    
    steps = 0
    t0 = time.time()
    P = []
    
    for pers in sim.foule:
        P.append([[], []])
    
    while (not sim.is_finished()) and (steps < 3/dt):
        steps += 1
        sim.perform_time_step(dt)
        
        for i, p in enumerate(sim.foule):
            P[i][0].append(p.center[0])
            P[i][1].append(p.center[1])
        
        
    t1 = time.time()
    
    print("Simulation completed in {}s for {} steps".format(t1 - t0, steps))
    print("Computing a step in {}s or {} steps per second".format((t1 - t0)/steps, int(steps/(t1 - t0))))
    
    display(P)
    
    try:
        first = sim.first_evacuation()
        last = sim.last_evacuation()
        mean = sim.mean_evacuation()
        print("first: {}, last: {}, mean: {}".format(first, last, mean))
    except Exception as e:
        print(e)
        print("not finished")
        print(len(sim.ariving_data))
        print(sim.ariving_data)
        print(sim.foule)
    


if __name__ == "__main__":
    main()