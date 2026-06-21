# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:03:32 2026

@author: arthur.woelfel
"""

from math import exp, cos, log

import numpy as np

from matplotlib import pyplot as plt

delta = 1.5

radius = 0.2

l = 0.2

def func(distance, cos_alpha):
    return np.exp(-distance / delta) * (l + (1 - l) * (1 + cos_alpha)/2 )

def stress(X, Y):
    distance = np.sqrt(X**2 + Y**2)
    
    cos_alpha = Y / distance
    
    corrected_distance = distance - radius * 2
    
    S = func(corrected_distance, cos_alpha)
    S[corrected_distance < 0] = 0
    
    return S

base_speed_factor = 1
max_speed_increase = 0.5
stress_modulation = 10
def speed_increase(stress, stress_increase):
    return base_speed_factor + max_speed_increase * np.tanh(stress / stress_modulation)
    
def social_decrease(stress, stress_increase):
    return 1 - np.tanh(stress / stress_modulation)



# pour 1m**2 : R == 0.55
def model_for_speed_density_decrase(density):
    a= 1
    b= 2/log(2)
    return a * np.exp(density / b)


arr = np.zeros((100, 100, 2))
img = np.zeros((500, 200))

X = np.linspace(0, 20, 500)
Y = np.linspace(0, 1, 200)

X, Y = np.meshgrid(X, Y)

speed_img = speed_increase(X, Y)
social_img = social_decrease(X, Y)

print(np.max(speed_img))
print(np.min(social_img))
f, (top, bottom) = plt.subplots(nrows=2, ncols=1)
t = top.contourf(X, Y, speed_img)
b = bottom.contourf(X, Y, social_img)

f.colorbar(t, ax=top)
f.colorbar(b, ax=bottom)

plt.show()
