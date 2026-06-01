# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:03:32 2026

@author: arthur.woelfel
"""

from math import exp, cos

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


arr = np.zeros((100, 100, 2))
img = np.zeros((100, 100))

X = np.linspace(-4, 4, 100)
Y = np.linspace(-2, 4, 100)

X, Y = np.meshgrid(X, Y)

img = stress(X, Y)

print(np.max(img))

h = plt.contourf(X, Y, img)
plt.axis('scaled')
plt.colorbar()
plt.show()
