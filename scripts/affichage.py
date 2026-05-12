import utils
import matplotlib.pyplot as plt

import numpy as np

RESOLUTION = 30
X_LEN = 5
Y_LEN = 5

SHAPE = (X_LEN * RESOLUTION, Y_LEN * RESOLUTION)

background_color = [0, 0, 0]

def build_background():
    """Construit une matrice "d'arrière plan" qui sert de base pour redessiner tout les objets dessus

    Returns:
        _list_: renvoie un tableau en x * y * 3
    """
    
    M = []
    for i in range(SHAPE[1]):
        L = [background_color[:]for j in range(SHAPE[0])]
        M.append(L)
    
    return M

REPRESENTATIONS = {}

def get_representation(radius, smoothing = True):
    """Renvoie la représentation d'un mask de cercle de bon rayon si possible en réutilisant un déjà utilisé

    Args:
        radius (float): le rayon du cercle dont on veut la représenation

    Returns:
        _type_: _description_
    """
    
    # construit le rayon effectif en fonction de la résolution et du rayon réel
    int_radius = int(RESOLUTION * radius)
    
    # récupère si possible une représentation déjà enregistrée
    if (int_radius in REPRESENTATIONS):
        return REPRESENTATIONS[int_radius]
    
    # construit un nouvelle représentation
    M = []
    for x in range(int_radius * 2 + 1):
        L = []
        for y in range(int_radius * 2 + 1):
            # calcul de la distance entre le centre et le point itéré
            #NOTE : l'utilisation de x et int_radius permet d'avoir un cercle bien circulaire
            # ce n'est pas le cas avec x / RESOLUTION et radius
            d = (x - int_radius)**2 + (y - int_radius)**2
            
            # peut être remplacée par une fonction continue moins brutale (prenant d / radius en argument)
            if smoothing:
                L.append(utils.smoothing_exp(d/int_radius, 1, 1, 0, 1.5))
            elif d <= int_radius**2:
                L.append(1)
            else:
                L.append(0)
        M.append(L)
    
    # sauvegarde la remprésentation calculée pour usage ultérieur
    REPRESENTATIONS[int_radius] = M
    return M

def blend_pixel(p1, p2, mu):
    """Effectue une somme convexe
    avec: mu = 1 ==> p2 et mu = 0 ==> p1

    Returns:
        float: mu * p2 + (1 - mu) * p1
    """

    L = [int(p2[i] * mu + (1 - mu) * p1[i]) for i in range(len(p1))]
    return L

def draw_circle(mat, circle, color=[255, 0, 0], smoothing=True):
    #récupère la représentation du cercle et sa taille
    rep = get_representation(circle.radius)
    
    l = (len(rep) - 1) // 2
    
    # la position sur la grille du centre
    center = circle.position
    center_grid = (int(center[0] * RESOLUTION), int(center[1] * RESOLUTION))
    
    #effectue l'affichage du cercle
    for i in range(2 * l + 1):
        # effectue le lien avec les coordonnées de la grille
        x = center_grid[0] + i - l
        # print("i, x", i, x)
        if x < 0 or x >= SHAPE[0]:
            continue
        
        for j in range(2 * l + 1):
            # effectue le lien avec les coordonnées de la grille
            y = center_grid[1] + j - l
            
            if y < 0 or y >= SHAPE[1]:
                continue
            
            # mise à jour de la grille
            if smoothing:
                mat[y][x] = blend_pixel(mat[y][x], color[:3], rep[i][j])
            elif rep[i][j] > 1/2:
                # print("j, y", j, y)
                mat[y][x] = color[:3]
    
    mat[center_grid[1]][center_grid[0]] = [0, 0, 255]

def draw(circles, square_obastacles, round_obstacles):
    mat = build_background()
    for circle in circles:
        draw_circle(mat, circle)
    
    for circle in round_obstacles:
        draw_circle(mat, circle)

    plt.imshow(mat)
    plt.axis("off")
    plt.show()


if  __name__ == "__main__":
    c = utils.Circle(1, [2, 2])
    arr = np.arange(0, 2, 0.01)
    result = np.array([utils.smoothing_exp(r, 1, 1, 0, 1.5) for r in arr])
    
    # plt.plot(arr, result)
    # plt.show()
    
    
    print(c)
    draw([c], [], [])

