import math

class Vector2():
    def __init__(self, x, y):
        self.coordinates = x, y
    
    def __add__(self, v2):
        if isinstance(v2, Vector2):
            return Vector2(self.x + v2.x, self.y + v2.y)
        else:
            raise TypeError("type : '%s' not expected, should be 'Vector2'" % str(type(v2)))
    
    def __repr__(self):
        return "Vector2(" + str(self.x) + ", "+ str(self.y) + ")"
    
    def __mult__(self, obj):
        if isinstance(obj, Vector2):
            return self.dot(obj)
        
        return Vector2(self.x * obj, self.y * obj)
    
    def __len__(self):
        return 2
    
    def __getitem__(self, i):
        return self.coordinates[i]
    
    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]

    def dot(self, v2):
        return self.x * v2.X + self.y + v2.y
    
    def sqr_magnitude(self):
        return self.x ** 2 + self.y ** 2
    
    def magnitude(self):
        return (self.sqr_magnitude()) ** 1/2


def closest_point_on_line(l1, l2, point):
    # construit une droite passant par l1 et l2 d'équation: ax + by = c1
    a = l2[1] - l1[1]
    b = l1[0] - l2[0]
    c1 = a * l1[0] + b * l2[1]
    
    # construit une droite perpendiculaire à la précédente passant par point d'équations -bx + ay = c2
    c2 = -b * point[0] + a * point[1]
    
    # construit le déterminant du système
    d = a ** 2 + b **2
    
    ## déterminant nul ssi point est sur la droite (l1, l2) donc renvoie point
    if d == 0: 
        return Vector2(point[0], point[1])
    
    # résoud le système algébriquement avec la règle de Cramer
    cx = (a * c1 - b * c2) / d
    cy = (a * c2 + b * c1) / d
    
    return Vector2(cx, cy)

# une fonction de transistion
def in_out_exp(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    elif x < 1/2:
        return 2**(20*x - 10) / 2
    else:
        return (2 - 2**(-20*x + 10)) / 2

# à l'aide d'une fonctionde  transition, effectue une transition entre plusieurs valeurs
def smoothing_exp(t, v0, x0, v1, x1):
    if t < x0:
        return v0
    elif t > x1:
        return v1
    else:
        return (v1 - v0) * in_out_exp( (t-x0) / (x1 - x0) ) + v0
        

class Circle():
    density = 350
    def __init__(self, radius, position, masse=-1, vitesse=[0,0], static=False):
        self.radius = radius
        self.position = Vector2(*position[0:2])
        self.vitesse = Vector2(*vitesse[0:2])
        self.static = static
        if masse == -1:
            self.masse = math.pi * radius**2 * Circle.density
        else:
            self.masse = masse

    def __repr__(self):
        args = [
            str(self.radius),
            str(self.position),
            str(self.masse),
        ]
        if self.vitesse != [0, 0]:
            args.append(str(self.vitesse))
        if self.static:
            args.append("True")
        return "Circle({})".format(", ".join(args))
    
    def predict_pos(self, delta_t):
        return self.position + delta_t * self.vitesse
    
    @classmethod
    def is_collision(cls, c1, c2):
        return (c1.position - c2.position).sqr_magnitude() < c1.radius ** 2 + c1.radius ** 2
    
    @classmethod
    def compute_collision(cls, c1, c2):
        mx = (c1.position[0] + c2.position[0]) / 2
        my = (c1.position[1] + c2.position[1]) / 2
        
        


