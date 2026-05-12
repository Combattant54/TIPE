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
    -> définir une liste d'obstacles circulaires (après) NON
    -> définir un champs de vecteur vecteur vitesse qui mène à la sortie hypothèse: (base) 
        - il y a une signalisation / les personnes connaissent le chemin pour la sortie
    -> pouvoir récupérer la vitesse souhaitée la plus proche pour en déduire la vitesse OK
    -> pouvoir mesurer la validité de "la personne i à atteint la sortie" (base)
    -> conversion pos réelle / approchée (par entiers) OK


@author: arthur.woelfel
"""

from math import sqrt
import personnes

OBSTACLES_RECT = []
OBSTACLES_ROND = []
# commencons sans obstacles

#liste de la forme: [[rayons], [positions], [vitesse]]
FOULE = []

PERSONNES_ACTIVES = set()

# liste de la position des objectifs (pour l'instant, x > x_max => personne sortie)
OBJECTIFS = [] 

# taille de l'espace (pour l'instant, en mètres)
TAILLE = [10, 10] 

# nombre de pixels par mètre
RESOLUTION = 5 

# le champs des vitesses souhaitées
CHAMP_VITESSES = []

# vitesse typique d'une personne dans une foule
VITESSE_TYPIQUE = 1.3

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


# première modélisation d'un champ de vecteur vitesse => tout le monde va vers la droite (l'objectif)
def construire_champ_vitesse():
    champ = []
    for x in range(int(TAILLE[0] * RESOLUTION) + 1):
        L = []
        for y in range(int(TAILLE[1] * RESOLUTION) + 1):
            L.append([VITESSE_TYPIQUE, 0])
        champ.append(L)
    return champ

def objectif_atteint(position):
    """
    Parameters
    ----------
    position : list[float, float]
        la position de la personne

    Retourne si la personne à atteint l'objectif

    """
    return position[0] > TAILLE[0]

def is_obstacle(position):
    x, y = position[0], position[1]
    for obstacle_rond in OBSTACLES_ROND:
        pos_obs, rayon = obstacle_rond[0], obstacle_rond[1]
        if (x - pos_obs[0]) ** 2 + (y - pos_obs[1]) ** 2 < rayon ** 2:
            return True

    return False

def calcul_distance(foule, i, j):
    p1 = foule[1][i]
    p2 = foule[1][j]
    
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

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
    global OBSTACLES_RECT
    global OBSTACLES_ROND
    global CHAMP_VITESSES
    global PERSONNES_ACTIVES
    
    FOULE = personnes.foule_init(len(pos), pos)
    
    
    OBSTACLES_RECT = obs_rect
    OBSTACLES_ROND = obs_rond

    CHAMP_VITESSES = construire_champ_vitesse()
    PERSONNES_ACTIVES = set(range(len(FOULE[0])))
    personnes.TAILLE = TAILLE
    personnes.RESOLUTION = RESOLUTION
