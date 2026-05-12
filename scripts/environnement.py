# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 08:37:03 2026

Script qui modélise l'environnement
Ce script doit contenir:
    -> un objectif
    -> une foule
    -> un champs de vitesse souhaitée

IL faut pour cela:
    -> définir la taille de l'espace OK
    -> définir une liste d'obstacles rectangulaires (positions des coins) NON
    -> définir une liste d'obstacles circulaires (après) moyen
    -> définir un champs de vecteur vecteur vitesse qui mène à la sortie hypothèse: (moyen) 
        - il y a une signalisation / les personnes connaissent le chemin pour la sortie
    -> pouvoir récupérer la vitesse souhaitée la plus proche pour en déduire la vitesse OK
    -> pouvoir mesurer la validité de "la personne i à atteint la sortie" (moyen)
    -> conversion pos réelle / approchée (par entiers) OK


@author: arthur.woelfel
"""

from math import sqrt
import personnes
from matplotlib.patches import Rectangle, Circle
from collections import deque

OBSTACLES_RECT = [[[6, 1], [6.8, 7]]]
OBSTACLES_ROND = []
# commencons sans obstacles

#liste de la forme: [[rayons], [positions], [vitesse]]
FOULE = []

PERSONNES_ACTIVES = set()

# liste de la position des objectifs (pour l'instant, x > x_max => personne sortie)
OBJECTIFS = [[[9, 4], [10, 6]]] 

# nombre de pixels par mètre
RESOLUTION = 5 

# taille de l'espace (pour l'instant, en mètres)
TAILLE = [10, 10] 
TAILLE_INT = [int(TAILLE[0] * RESOLUTION) + 1, int(TAILLE[1] * RESOLUTION) + 1]

# le champs des vitesses souhaitées
CHAMP_VITESSES = []

# vitesse typique d'une personne dans une foule
VITESSE_TYPIQUE = 1.3
RADIUS = personnes.RADIUS
MARGIN = personnes.RADIUS

def build_rect(obstacle_color="black", objectif_color="green"):
    rects = []
    for bg, hd in OBSTACLES_RECT:
        r = Rectangle(bg, hd[0] - bg[0], hd[1] - bg[1], color=obstacle_color, fill=True)
        rects.append(r)
    
    for bg, hd in OBJECTIFS:
        xy, width, height = bg, hd[0] - bg[0], hd[1] - bg[1]
        r = Rectangle(xy, width, height, color=objectif_color, fill=True)
        print(f"Green : {xy} - {width} - {height}")
        rects.append(r)
    
    print(str(len(rects)) + " built rectangles")
    
    return rects

def position_reelle_en_coordonees(pos):
    """
    Donne les coordonnées en fonction de la position

    Parameters
    ----------
    pos : list[float, float]
        la position de la personne

    Returns
    -------
    list[int, int]
        la liste des coordonnées entières les plus proche

    """
    x = int(pos[0] * RESOLUTION + 1/2)
    y = int(pos[1] * RESOLUTION + 1/2)
    
    return [x, y]

def coord_en_relle(pos):
    return [pos[0] / RESOLUTION, pos[1] / RESOLUTION]

CADRE = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
# première modélisation d'un champ de vecteur vitesse => tout le monde va vers la droite (l'objectif)
def construire_champ_vitesse():
    champ = []
    for x in range(int(TAILLE[0] * RESOLUTION) + 1):
        L = []
        for y in range(int(TAILLE[1] * RESOLUTION) + 1):
            L.append([0, 0])
        champ.append(L)
       
    print("[CHAMP VITESSE]:champs initialisé")
    file = deque()
    obstacles_set = set()
    objectif_set = set()
    done_dict = {}
    for x_int in range(TAILLE_INT[0]):
        for y_int in range(TAILLE_INT[0]):
            c = coord_en_relle((x_int, y_int))
            if is_obstacle(c):
                obstacles_set.add((x_int, y_int))
            elif objectif_atteint(c):
                objectif_set.add((x_int, y_int))
                file.append((x_int, y_int))
                done_dict[(x_int, y_int)] = 0
    
    print("[CHAMP VITESSE]:objectifs et obstacles définies")
    
    while len(file) > 0:
        el = file.popleft()
        
        for obj in CADRE:
            cel = (el[0] + obj[0], el[1] + obj[1])
            d = done_dict[el] + sqrt(obj[0]**2 + obj[1] ** 2)
            
            if cel in done_dict and done_dict[cel] <= d:
                continue
            
            done_dict[cel] = d
            
            if 0 <= cel[0] < TAILLE_INT[0] and 0 <= cel[1] < TAILLE_INT[1]:
                v = [-obj[0], -obj[1]]
                scale = VITESSE_TYPIQUE * sqrt(v[0]**2 + v[1]**2)
                v[0] = v[0] * scale
                v[1] = v[1] * scale
            
                champ[cel[0]][cel[1]] = v
                if not is_obstacle(coord_en_relle(cel)):
                    file.append(cel)

    print("[CHAMP VITESSE]:début vitesse dans les obstacles")
    done_dict.clear()
    for obs in obstacles_set:
        if obs in done_dict:
            file.append(obs)
            done_dict[obs] = 0
    
    while len(file) > 0:
        el = file.popleft()
        
        for obj in CADRE:
            cel = (el[0] + obj[0], el[1] + obj[1])
            d = done_dict[el] + sqrt(obj[0]**2 + obj[1] ** 2)
            
            if cel in done_dict and done_dict[cel] <= d:
                continue
            
            done_dict[cel] = d
            
            if 0 <= cel[0] < TAILLE_INT[0] and 0 <= cel[1] < TAILLE_INT[1] and is_obstacle(cel):
                v = [-obj[0], -obj[1]]
                scale = VITESSE_TYPIQUE * sqrt(v[0]**2 + v[1]**2)
                v[0] = v[0] * scale
                v[1] = v[1] * scale
            
                champ[cel[0]][cel[1]] = v
                file.append(cel)
    
    print("[CHAMP VITESSE]:champ terminé")
    return champ

def objectif_atteint(position):
    """

    Parameters
    ----------
    position : list[float, float]
        la position de la personne

    Retourne si la personne à atteint l'objectif

    """
    x, y = position
    for rect_bg, rect_hd in OBJECTIFS:
        if rect_bg[0] <= x <= rect_hd[0] and rect_bg[1] <= y <= rect_hd[1]:
            return True
    return False
    
    return position[0] > TAILLE[0]

def is_obstacle(position):
    x, y = position[0], position[1]
    for obstacle_rond in OBSTACLES_ROND:
        pos_obs, rayon = obstacle_rond[0], obstacle_rond[1]
        if (x - pos_obs[0]) ** 2 + (y - pos_obs[1]) ** 2 < (rayon + MARGIN) ** 2:
            return True
    
    for rect_bg, rect_hd in OBSTACLES_RECT:
        if rect_bg[0] <= x+MARGIN and x-MARGIN <= rect_hd[0] and rect_bg[1] <= y+MARGIN and y-MARGIN <= rect_hd[1]:
            return True
    
    return False

def calcul_distance(foule, i, j):
    try:
        p1 = foule[1][i]
        p2 = foule[1][j]
        
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    except Exception as e:
        print(i, len(foule))
        raise e

def inter_perdestrian_distance_metric():
    I = 0
    for i in PERSONNES_ACTIVES:
        for j in PERSONNES_ACTIVES:
            if j < i:
                I += calcul_distance(FOULE, i, j)
    return I

def perform_time_step(dt):
    personnes.vitesse_update(FOULE, dt, PERSONNES_ACTIVES, CHAMP_VITESSES)
    personnes.position_update(FOULE, dt, PERSONNES_ACTIVES)
    desactivation = []
    for i in PERSONNES_ACTIVES:
        if objectif_atteint(FOULE[1][i]):
            desactivation.append(i)
    for i in desactivation:
        PERSONNES_ACTIVES.discard(i)

def gather_parameters():
    param = {}
    
    param["radius"] = personnes.RADIUS
    param["mass"] = personnes.MASS
    param["tau"] = personnes.TAU
    param["speed"] = VITESSE_TYPIQUE
    param["f_social"] = personnes.F
    param["delta"] = personnes.DELTA
    param["lambda"] = personnes.LAMBDA
    param["kappa"] = personnes.KAPPA
    
    
    return param

def pos_pers(i):
    return FOULE[1][i]

def init(pos, obs_rect, obs_rond):
    global FOULE
    global OBSTACLES_ROND
    global CHAMP_VITESSES
    global PERSONNES_ACTIVES
    
    FOULE = personnes.foule_init(len(pos), pos)
    OBSTACLES_ROND = obs_rond

    print("Construction du champ de vitesses")
    CHAMP_VITESSES = construire_champ_vitesse()
    PERSONNES_ACTIVES = set(range(len(FOULE[0])))
    print("len foule:", len(FOULE[1]))
    personnes.TAILLE = TAILLE
    personnes.RESOLUTION = RESOLUTION
