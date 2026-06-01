from math import sqrt
import personnes
from matplotlib.patches import Rectangle, Circle
from collections import deque
from personnes_classe import Personne

import time

def strip_vec(vect, dec=2):
    return "[" + ", ".join([f"{coord:0.{dec}f}" for coord in vect])+ "]"

class Simulation():
    LOG_FILE = ".\\logs\\env_class_logs.txt"
    def __init__(self, objectifs, rect_obstacles, taille, sim_id, resolution=5, vitesse_typique=1.3, radius=0.2, margin_fraction=1):
        self.resolution = resolution
        self.taille = taille
        self.vitesse_typique = vitesse_typique
        self.radius = radius
        self.margin = margin_fraction * self.radius
        self.objectifs = objectifs
        self.rect_obstacles = rect_obstacles
        self.round_obstacles = []
        self.taille_int = [int(self.taille[0] * self.resolution) + 1, int(self.taille[1] * self.resolution) + 1]
        self.foule: list[Personne] = []
        self.sim_time = 0
        self.sim_id = sim_id
        self.iterations = 0
        
        with open(Simulation.LOG_FILE, "w") as f:
            f.write("BEGINING SIMULATION {}".format(self.sim_id))
        
        
        self.log(self.rect_obstacles)
        self.log(self.objectifs)
        self.champ_vitesses = self.construire_champ_vitesse()
        
        c = self.position_reelle_en_coordonees([6-0.3, 2])
        
        self.ariving_data = []
        
        
    
    def init_foule(self, foule: list[Personne]):
        self.foule = foule.copy()
        self.personnes_actives = set(range(len(foule)))
    
    def build_rect(self, obstacle_color="black", objectif_color="green"):
        rects = []
        for bg, hd in self.rect_obstacles:
            r = Rectangle(bg, hd[0] - bg[0], hd[1] - bg[1], color=obstacle_color, fill=True, alpha=0.3)
            rects.append(r)
        
        for bg, hd in self.objectifs:
            xy, width, height = bg, hd[0] - bg[0], hd[1] - bg[1]
            r = Rectangle(xy, width, height, color=objectif_color, fill=True)
            self.log(f"Green : {xy} - {width} - {height}")
            rects.append(r)
        
        self.log(str(len(rects)) + " built rectangles")
        
        return rects
    
    def position_reelle_en_coordonees(self, pos):
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
        x = int(pos[0] * self.resolution + 1/2)
        y = int(pos[1] * self.resolution + 1/2)
        
        return [x, y]
    
    def coord_en_relle(self, pos):
        return [pos[0] / self.resolution, pos[1] / self.resolution]
    
    # première modélisation d'un champ de vecteur vitesse => tout le monde va vers la droite (l'objectif)
    def construire_champ_vitesse(self):
        t0 = time.time()
        
        CADRE = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        champ = []
        for x in range(int(self.taille[0] * self.resolution) + 1):
            L = []
            for y in range(int(self.taille[1] * self.resolution) + 1):
                L.append([0, 0])
            champ.append(L)
        
        self.log("[CHAMP VITESSE]:champs initialisé")
        file = deque()
        obstacles_set = set()
        objectif_set = set()
        done_dict = {}
        for x_int in range(self.taille_int[0]):
            for y_int in range(self.taille_int[0]):
                c = self.coord_en_relle((x_int, y_int))
                if self.is_obstacle(c, margin=True):
                    obstacles_set.add((x_int, y_int))
                elif self.objectif_atteint(c):
                    objectif_set.add((x_int, y_int))
                    file.append((x_int, y_int))
                    done_dict[(x_int, y_int)] = 0
        
        self.log("[CHAMP VITESSE]:objectifs et obstacles définies")
        
        while len(file) > 0:
            el = file.popleft()
            
            
            for obj in CADRE:
                cel = (el[0] + obj[0], el[1] + obj[1])
                d = done_dict[el] + sqrt(obj[0]**2 + obj[1] ** 2)
                
                if cel in done_dict and done_dict[cel] <= d:
                    continue
                
                done_dict[cel] = d

                
                if 0 <= cel[0] < self.taille_int[0] and 0 <= cel[1] < self.taille_int[1]:
                    v = [-obj[0], -obj[1]]
                    scale = self.vitesse_typique * sqrt(v[0]**2 + v[1]**2)
                    v[0] = v[0] * scale
                    v[1] = v[1] * scale
                    
                    champ[cel[0]][cel[1]] = v
                    if not self.is_obstacle(self.coord_en_relle(cel)):
                        file.append(cel)

        self.log("[CHAMP VITESSE]:début vitesse dans les obstacles")
        obs_done_dict = {}
        for obs in obstacles_set:
            if obs in done_dict:
                file.append(obs)
                obs_done_dict[obs] = 0
        
        done_dict.clear()
        
        # print("Number obstacles: ", len(obs_done_dict), "el a check", len(file))
        
        while len(file) > 0:
            el = file.popleft()
            
            for obj in CADRE:
                cel = (el[0] + obj[0], el[1] + obj[1])
                d = obs_done_dict[el] + sqrt(obj[0]**2 + obj[1] ** 2)
                
                if cel in obs_done_dict and obs_done_dict[cel] <= d:
                    continue
                
                obs_done_dict[cel] = d
                
                if 0 <= cel[0] < self.taille_int[0] and 0 <= cel[1] < self.taille_int[1] and self.is_obstacle(self.coord_en_relle(cel)):
                    v = [-obj[0], -obj[1]]
                    scale = self.vitesse_typique * sqrt(v[0]**2 + v[1]**2)
                    v[0] = v[0] * scale
                    v[1] = v[1] * scale
                
                    champ[cel[0]][cel[1]] = v
                    file.append(cel)
        
        t1 = time.time()
        
        self.log("[CHAMP VITESSE]:champ terminé en {}s".format(t1 - t0))
        
        return champ
    
    def objectif_atteint(self, position, marge = False):
        """

        Parameters
        ----------
        position : list[float, float]
            la position de la personne

        Retourne si la personne à atteint l'objectif

        """
        x, y = position
        m = self.margin * marge
        for rect_bg, rect_hd in self.objectifs:
            if rect_bg[0] - m <= x <= rect_hd[0] + m and rect_bg[1] - m <= y <= rect_hd[1] + m:
                return True
        return False
    
    def is_obstacle(self, position, margin = True):
    
        x, y = position[0], position[1]
        
        for obstacle_rond in self.round_obstacles:
            pos_obs, rayon = obstacle_rond[0], obstacle_rond[1]
            if (x - pos_obs[0]) ** 2 + (y - pos_obs[1]) ** 2 < (rayon + self.margin*margin) ** 2:
                return True
        
        for rect_bg, rect_hd in self.rect_obstacles:
            if rect_bg[0] <= x+self.margin*margin and x-self.margin*margin <= rect_hd[0] and rect_bg[1] <= y+self.margin*margin and y-self.margin*margin <= rect_hd[1]:
                return True
        
        return False
    
    def calcul_distance(self, i, j):
        try:
            p1 = self.foule[1][i]
            p2 = self.foule[1][j]
            
            return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        except Exception as e:
            self.log(i, len(self.foule))
            raise e
    
    def inter_perdestrian_distance_metric(self):
        I = 0
        for i in self.personnes_actives:
            for j in self.personnes_actives:
                if j < i:
                    I += self.calcul_distance(i, j)
        return I

    def calcul_force_tot(self):
        F = {i:0 for i in range(len(self.foule))}
        for i in self.personnes_actives:
            f = [0, 0]
            for j in self.personnes_actives:
                if j != i:
                    f_soc = self.foule[i].f_sociale_de_pers(self.foule[j])
                    f_con = self.foule[i].force_contact_de_pers(self.foule[j])
                    
                    if(f_con == [0, 0]):
                        #self.log("{} - [00]")
                        pass
                    
                    #f_con = [0, 0]
                    #f_soc = [0, 0]
                    
                    c_i = self.foule[i].center
                    c_j = self.foule[j].center
                    #self.log(f"{i}, c_i: {c_i} - {j}, c_j: {c_j}, f_con: {f_con}")
                    #self.log(f"d: {((c_j[0] - c_i[0])**2 + (c_j[1] - c_i[1])**2)**(1/2)}")
                    
                    f[0] = f[0] + f_soc[0] + f_con[0]
                    f[1] = f[1] + f_soc[1] + f_con[1]
            F[i] = f
        
        return F
    
    def perform_time_step(self, dt):
        self.iterations += 1
        #self.log("", "Start of iteration " + str(self.iterations))
        
        F = self.calcul_force_tot()
        self.sim_time = self.sim_time + dt
        
        for i in self.personnes_actives:
            vi_souhaitee = self.calcul_vitesse_souhaitee(self.foule[i].center)
            s = f"{i} - F: {strip_vec(F[i])} - vi_sou: {strip_vec(vi_souhaitee)}"
            self.foule[i].vitesse_update(F[i], dt, vi_souhaitee)
            self.foule[i].position_update(dt)
            s = s + f" - dt: {dt} - center: {strip_vec(self.foule[i].center)} - vi_act: {strip_vec(self.foule[i].speed)}"
            self.log(s)

        
        desactivation = []
        for i in self.personnes_actives:
            if self.objectif_atteint(self.foule[i].center, marge = True):
                desactivation.append(i)
        for i in desactivation:
            self.log(f"{i} - DESACTIVATION")
            self.personnes_actives.discard(i)
            self.ariving_data.append((i, self.sim_time, self.foule[i]))
            self.log(f"[DESACTIVATION]: personne {i} désactivée, il reste {len(self.personnes_actives)} p.actives")
            self.log(f"[DESACTIVATION]: ariving data updated to {len(self.ariving_data)}")
    
    def calcul_vitesse_souhaitee(self, pos):
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
        elif pos[0] >= self.taille[0]:
            V[0] = -1
        
        if pos[1] < 0:
            V[1] = 1
        elif pos[1] >= self.taille[1]:
            V[1] = -1
        
        # la priorité est de revenir dans la zone
        if V[0] != 0 or V[1] != 0:
            return V
        
        x = pos[0] * self.resolution
        y = pos[1] * self.resolution
        x_min = int(x)
        y_min = int(y)
        
        
        x_max = x_min + 1
        y_max = y_min + 1 
        
        # x = (1 - t_x) * x_min + t_x * x_max
        # y = (1 - t_y) * y_min + t_y * y_max
        tx = (x - x_min) / (x_max - x_min)
        ty = (y - y_min) / (y_max - y_min)
        
        #calcul des vitesses dans les coins
        v_min_min = self.champ_vitesses[x_min][y_min]
        v_max_min = self.champ_vitesses[x_max][y_min]
        v_min_max = self.champ_vitesses[x_min][y_max]
        v_max_max = self.champ_vitesses[x_max][y_max]
        
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
    
    def is_finished(self):
        return len(self.personnes_actives) == 0
    
    def first_evacuation(self):
        assert(self.is_finished())
        return self.ariving_data[0][1]

    def last_evacuation(self):
        assert(self.is_finished())
        return self.ariving_data[-1][1]
    
    def mean_evacuation(self):
        assert(self.is_finished())
        total_time = 0
        for i, t, *_ in self.ariving_data:
            total_time += t
            
        return total_time / len(self.ariving_data)
    
    def log(self, *strings):
        with open(self.LOG_FILE, "a") as f:
            f.writelines(["{:.3f} - {} - {}\n".format(self.sim_time, self.iterations, str(s)) for s in strings])
