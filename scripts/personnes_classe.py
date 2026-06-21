from math import sqrt, cos, exp, tanh


base_speed_factor = 1
max_speed_increase = 0.75
stress_modulation = 8

def speed_increase(stress):
    return base_speed_factor + max_speed_increase * tanh(stress / stress_modulation)
    
def social_decrease(stress):
    return 1 - 0.5 * tanh(stress / stress_modulation)

class Personne():
    def __init__(self, radius, center, speed=[0,0], tau=0.7, mass=80, stress=0, f_soc=150, delta=0.33, lamb=0.2, kappa=800):
        self.radius = radius
        self.center = list(center)
        self.speed = list(speed)
        self.tau = tau
        self.mass = mass
        self.stress_increase_factor = stress
        self.f_soc = f_soc
        self.delta = delta
        self.lamb = lamb
        self.kappa = kappa
        
        self.stress = 0
        self.stress_influence = 0
        self.stress_relaxation = 0.25
    
    def func(self, distance, cos_alpha):
        delta = 2
        return 0.02*exp(-distance / delta) * (self.lamb + (1 - self.lamb) * (1 + cos_alpha)/2 )

    def add_stress_influence(self, pers):
        distance = sqrt((self.center[0] - pers.center[0])**2 + (self.center[1] - pers.center[1])**2)
        
        ps = self.center[0] * pers.center[0] + self.center[1] * pers.center[1]
        
        cos_alpha = ps / distance
        
        corrected_distance = distance - self.radius * 2
        
        s = self.func(corrected_distance, cos_alpha)
        
        self.stress_influence += self.stress_increase_factor * s
        
    
    def distance (self, pers): #fonction dist min entre 2 individus
        if pers is self:
            raise ValueError("Distance with the only one personn not defined")
        elif not isinstance(pers, Personne):
            raise TypeError("Argument of unvalid type of '{}' received instead of expected 'Personne' type".format(str(type(pers))))
        
        
        di = sqrt( (self.center[0]-pers.center[0])**2 + (self.center[1]-pers.center[1])**2 )
        
        return (di - self.radius - pers.radius)
    
    def vect_unit(self, pers):
        if not isinstance(pers, Personne):
            raise TypeError("Argument of unvalid type of '{}' received instead of expected 'Personne' type".format(str(type(pers))))
        di = sqrt((self.center[0]-pers.center[0])**2+(self.center[1]-pers.center[1])**2)
        
        e0 = (pers.center[0] - self.center[0])/di
        e1 = (pers.center[1] - self.center[1])/di
        
        return [e0,e1]
    
    def update_stress(self, dt):
        self.stress = (self.stress + self.stress_influence * dt ) * (1 - self.stress_relaxation * dt)
        self.stress_influence = 0
        
    
    def f_sociale_de_pers(self, pers):
        e_ij = self.vect_unit(pers)
        d_ij = self.distance(pers)
        
        prod_scal = self.speed[0]*e_ij[0] + self.speed[1]*e_ij[1]
        norme = sqrt(self.speed[0]**2 + self.speed[1]**2)
        
        if norme == 0:
            cos_alpha = 0
        else:
            cos_alpha = prod_scal / norme
        #on calcule le cos de l'angle entre la vitesse et e_ij (alpha)
        
        f = -1*self.f_soc*social_decrease(self.stress)*exp(-d_ij/self.delta)*(self.lamb +(1-self.lamb)*(1+cos_alpha)/2)
        return [f*e_ij[0],f*e_ij[1]]
    
    
    def force_contact_de_pers(self, pers):
        di = self.distance(pers)
        if di>=0:
            return [0,0] 
        #la force ne s'applique que quand les gens "rentrent dans les murs
        
        e_ij = self.vect_unit(pers)
        
        f_con = [-self.kappa*exp(-di)*e_ij[0], -self.kappa*exp(-di)*e_ij[1]]
        
        return f_con
    
    def vitesse_update(self, ftot, dt, vitesse_souhaitee): #pfd en légende
        #on utilise les fonctions:
            # -> vitesse souhaitée (on suppose qu'on l'a)
            # -> vitesse (t) (en fait foule va etre update regulierement)
            # -> si jamais ya besoin d'autres forces sociales
        
        a = [0, 0]
        a[0] += (speed_increase(self.stress)*vitesse_souhaitee[0] - self.speed[0]) / self.tau
        a[1] += (speed_increase(self.stress)*vitesse_souhaitee[1] - self.speed[1]) / self.tau
        
        a[0] += ftot[0] / self.mass
        a[1] += ftot[1] / self.mass
        
        self.speed[0] = self.speed[0] + dt * a[0]
        self.speed[1] = self.speed[1] + dt * a[1]
    
    def position_update(self, dt): #on fait la mm: la position à t+dt, c'est celle à t + v * dt
        self.center[0] += dt*self.speed[0]
        self.center[1] += dt*self.speed[1]
    
    def __repr__(self):
        return "Personne({}, {}, {})".format(self.radius, self.center, self.speed)
    