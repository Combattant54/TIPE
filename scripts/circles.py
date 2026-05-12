# -*- coding: utf-8 -*-
"""
Created on Tue May  5 08:28:58 2026

@author: arthur.woelfel
"""


def closest_point_to_line(l1, l2, point):
    A1 = l2[1] - l1[1]
    B1 = l1[0] - l2[0]
    C1 = A1 * l1[0] + B1 * l1[1]
    C2 = -B1 * point[0] + A1 * point[1]
    
    det = A1*A1 - -B1*B1
    c = [0, 0]
    
    if det != 0:
        c[0] = (A1*C1 - B1*C2)/det
        c[1] = (A1*C2 - -B1*C1)/det
    else:
        c = point.cpoy()
    
    return c



class Circle():
    def __init__(self, position, speed, radius):
        self.radius = radius
        self.position = position[:]
        self.speed = speed[:]
        
        self.future_position(0.1)
    
    def future_position(self, dt):
        return [self.position[0] + self.speed[0] * dt, self.position[1] + self.speed[1] * dt]


