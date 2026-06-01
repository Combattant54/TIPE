import random
from math import sqrt, cos, sin, exp
#On représente un cercle par son
#centre et son rayon. On aura alors une liste
#composée d'une liste de positions du centre,
#d'une liste de rayons et d'une liste de vecteurs vitesse

TAILLE = [0, 0]
RESOLUTION = 0
VITESSE_TYPIQUE = 1
RADIUS = 0.2
MASS = 80 #on suppose que la masse est cste en fn des indiv
TAU = 0.7 # temps de relaxation indiv; pourra changer dans les modèles plus poussés
F = 100
DELTA = 0.33
LAMBDA = 0.2
KAPPA = 400 # : constantes du modèle de Helbing
#à un moment faudra vérifier la pertinence de ces valeurs


def foule_init (n,L): #L est la liste des positions à t=0, n le nb d'individus
    if len(L)!=n:
        raise IndexError("ya un probleme")
    #r = [random.uniform(0.5,1.2) for i in range(n)]
    r = [RADIUS] * n
    #on peut aussi mettre r=cste au début
    ##crée une liste de rayons pour les cercles
    foule = [r] ; foule.append(L.copy())
    foule.append([[0,0]for i in range(n)]) #les electrons partent sans vitesse initiale
    return foule
#0 => rayons
#1=> positions
#2=> vitesses


def personne_i(i,foule):
    if i>len(foule[0])-1 or i<0:
        raise IndexError("fais gaffe aux indices")
    return [foule[0][i],foule[1][i],foule[2][i]]

def distance (i,j,foule): #fonction dist min entre 2 individus
    if i>len(foule[0]) or i<0 or j>len(foule[0]) or j<0 or i==j:
        raise IndexError("pb d'indices")
    di = sqrt((foule[1][i][0]-foule[1][j][0])**2+(foule[1][i][1]-foule[1][j][1])**2)
   
    return (di - foule[0][i]-foule[0][j])

def vect_unit(i,j,foule):
    di = sqrt((foule[1][i][0]-foule[1][j][0])**2+(foule[1][i][1]-foule[1][j][1])**2)
    
    e0 = (foule[1][j][0] - foule[1][i][0])/di
    e1 = (foule[1][j][1] - foule[1][i][1])/di
    
    return [e0,e1]


def f_sociale_j_vers_i(i,j,foule):
    e_ij = vect_unit(i,j,foule)
    d_ij = distance(i,j,foule)
    vit_i = foule[2][i]
    
    prod_scal = vit_i[0]*e_ij[0]+vit_i[1]*e_ij[1]
    
    norme = sqrt(vit_i[0]**2+vit_i[1]**2)
    if norme == 0:
        cos_alpha = 0
    else:
        cos_alpha = prod_scal / norme
    #on calcule le cos de l'angle entre la vitesse et e_ij (alpha)
    
    f = -1*F*exp(-d_ij/DELTA)*(LAMBDA +(1-LAMBDA)*(1+cos_alpha)/2)
    return [f*e_ij[0],f*e_ij[1]]

def force_contact_obstacle (i,OBSTACLE,foule):
    px,py = foule[1][i][0],foule[1][i][1]
    #d0 = DIST(OBSTACLE[0],foule[0][i]), ind=0, i=0
    # for fig in OBSTACLE:
    #     barycentre = [(rxmin+rxmax)/2,(rymin+rymax)/2] #pb si cest pas un rectangle
    #     if DIST(i,barycentre)<d0:
    #         DIST = d0, ind = i
    #     i+=1
    # di = distance_point_rectangle(foule[0][i][0],[foule[0][i][1]],OBSTACLE[ind][0][0],OBSTACLE[ind][1][0],OBSTACLE[ind][0][1],OBSTACLE[ind][1][1]) #besoin des coordonnées de l'obstacle le plus proche
    d0 = distance_point_rectangle(px, py, OBSTACLE[0][0][0], OBSTACLE[0][0][1], OBSTACLE[0][1][0], OBSTACLE[0][1][1])
    ind = 0
    for j in range (len(OBSTACLE)):
        if distance_point_rectangle(px, py, OBSTACLE[j][0][0], OBSTACLE[j][0][1], OBSTACLE[j][1][0], OBSTACLE[j][1][1])<d0:
            ind = j
            d0 = distance_point_rectangle(px, py, OBSTACLE[j][0][0], OBSTACLE[j][0][1], OBSTACLE[j][1][0], OBSTACLE[j][1][1])
    if d0>0:
        return 0
    else:
        if foule[1][i][1]>=OBSTACLE[ind][1][0]:
            return [0,exp(-1000*d0)]
        else: 
            return [-1*exp(-1000*d0),0]

def barycentre(rectangle):
    return [rectangle[0][0]+rectangle[0][1],rectangle[1][0]+rectangle[1][1]]

def vect_normal_rect(rectangle): #normal dirigé vers la gauche du rectangle 
#ne marche que dans le cas d'un rectangle non incliné
    return [-1,0]
    
    
    # la distance
    #piti probleme: y'a besoin de savoir quel obstacle est le plus proche



    
# def cote_le_plus_proche(foule,L): #L est une liste des coordonnées de 4 points: les sommets du rectangle   
#     m1 = L[0][0], i1 = 0
#     for i in range(4):
#         if L[i][0]<m1:
#             m1=L[i],i1=i
#     if i1==0 : i2=1, m2 = L[1][0]
#     else: i2 = 0, m2 = L[0][0]  # Heureusement il existe un algo plus court
#     for j in range(4):
#         if j!=i1:
#             if L[i][0]<m2:
#                 m2=L[i],i2=j
                
#     M1 = L[0][1], j1 = 0
#     for i in range(4):
#         if L[i][1]<M1:
#             M1=L[i],j1=i
#     if j1==0 : j2=1, M2 = L[1][1]
#     else: j2 = 0, M2 = L[0][1]
#     for j in range(4):
#         if j!=i1:
#             if L[i][1]<M2:
#                 M2=L[i]j2=j
    
#     if foule[0][i][0]<m1:
#         if foule[0][i][1]>M1:
#             d = sqrt(()**2+)
        
        
def distance_point_rectangle(px, py, rx_min, ry_min, rx_max, ry_max):
    """
    Calcule la distance minimale entre un point (px, py) et un rectangle
    défini par ses coins inférieur gauche (rx_min, ry_min) et supérieur droit (rx_max, ry_max).

    Paramètres :
        px, py : coordonnées du point
        rx_min, ry_min : coordonnées du coin inférieur gauche du rectangle
        rx_max, ry_max : coordonnées du coin supérieur droit du rectangle

    Retour :
        Distance minimale (float)
    """
    # Vérification des bornes du rectangle
    if rx_min > rx_max or ry_min > ry_max:
        raise ValueError("Coordonnées du rectangle invalides : min > max.")

    # Calcul de la distance horizontale
    if px < rx_min:
        dx = rx_min - px
    elif px > rx_max:
        dx = px - rx_max
    else:
        dx = 0  # Le point est aligné horizontalement avec le rectangle

    # Calcul de la distance verticale
    if py < ry_min:
        dy = ry_min - py
    elif py > ry_max:
        dy = py - ry_max
    else:
        dy = 0  # Le point est aligné verticalement avec le rectangle

    # Distance euclidienne
    return sqrt(dx**2+ dy**2)


def force_contact_j_vers_i (i,j,foule):
    di = distance(i,j,foule)
    if di>=0:
        return [0,0] 
    #la force ne s'applique que quand les gens "rentrent dans les murs
    
    e_ij = vect_unit(i,j,foule)
    
    
    return [-KAPPA*exp(di)*e_ij[0], -KAPPA*exp(di)*e_ij[1]]

def calcul_force_tot(i,foule,personne_active):
    f_tot = [0,0]
    for j in range(len(foule[0])):
        if j!=i and j in personne_active:
            fsoc = f_sociale_j_vers_i(i,j,foule)
            fcont = force_contact_j_vers_i (i,j,foule)
            #f_obs = force_contact_obstacle(i, OBSTACLE, foule)
            f_tot[0] += fsoc[0] + fcont[0] #+f_obs[0]
            f_tot[1] += fsoc[1] + fcont[1] #+f_obs[1]
    return f_tot

def vitesse_update(foule, dt, personnes_actives, champs_vitesses): #pfd en légende
    #on utilise les fonctions:
        # -> vitesse souhaitée (on suppose qu'on l'a)
        # -> vitesse (t) (en fait foule va etre update regulierement)
        # -> si jamais ya besoin d'autres forces sociales
    for j in personnes_actives: 
            ftot = calcul_force_tot(j,foule, personnes_actives)
            vitesse_souhaitee = calcul_vitesse_souhaitee(foule[1][j], champs_vitesses)
            foule[2][j][0] += dt/TAU * (vitesse_souhaitee[0]-foule[2][j][0]) + dt/MASS * ftot[0]
            foule[2][j][1] += dt/TAU * (vitesse_souhaitee[1]-foule[2][j][1]) + dt/MASS * ftot[1]
    return foule



def norme_sqr(vect):
    return vect[0]**2 + vect[1]**2

def position_update(foule,dt,personnes_actives): #on fait la mm: la position à t+dt, c'est celle à t + vdt  
    for j in personnes_actives: 
        V_j = foule[2][j]
        foule[1][j][0] += dt*V_j[0]
        foule[1][j][1] += dt*V_j[1]
    return foule
    
def calcul_vitesse_souhaitee(pos, champs_vitesses):
    """
    Returne une approximation linéaire de la vitesse souhaitée en un point

    Parameters
    ----------
    pos : list[float, float]
        la polsition de la personne

    Returns
    -------
    V : list[float, float]
        la vitesse souhaitée en un point
    """
    V = [0, 0]
    
    if pos[0] < 0:
        V[0] = 1
    elif pos[0] >= TAILLE[0]:
        V[0] = -1
    
    if pos[1] < 0:
        V[1] = 1
    elif pos[1] >= TAILLE[1]:
        V[1] = -1
    
    # la priorité est de revenir dans la zone
    if V[0] != 0 or V[1] != 0:
        return V
    
    x = pos[0] * RESOLUTION
    y = pos[1] * RESOLUTION
    x_min = int(x)
    y_min = int(y)
    
    
    x_max = x_min + 1
    y_max = y_min + 1 
    
    # x = (1 - t_x) * x_min + t_x * x_max
    # y = (1 - t_y) * y_min + t_y * y_max
    tx = (x - x_min) / (x_max - x_min)
    ty = (y - y_min) / (y_max - y_min)
    
    #calcul des vitesses dans les coins
    v_min_min = champs_vitesses[x_min][y_min]
    v_max_min = champs_vitesses[x_max][y_min]
    v_min_max = champs_vitesses[x_min][y_max]
    v_max_max = champs_vitesses[x_max][y_max]
    
    #hypothèse: la vitesse en x est linéaire sur le carré
    # calcul de v_min en [x, y_min] et de v_max en [x, y_max]
    v_min = [(1 - ty) * v_min_min[0] + ty * v_min_max[0],
             (1 - ty) * v_min_min[1] + ty * v_min_max[1]]
    v_max = [(1 - ty) * v_max_min[0] + ty * v_max_max[0], 
             (1 - ty) * v_max_min[1] + ty * v_max_max[1]]
    
    #calcul de V
    V = [(1 - tx) * v_min[0] + tx * v_max[0],
         (1 - tx) * v_min[1] + tx * v_max[1]]
    
    return V
