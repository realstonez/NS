#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 22:28:10 2024

@author: realmac
"""

import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Pigeon:
    def __init__(self, location, speed):
        self.location = location
        self.speed = speed

    def fly(self):
        self.location = [max(0, min(gridSize, self.location[i] + random.randint(-self.speed, self.speed))) for i in range(2)]

class Hawk:
    def __init__(self, location, aggressiveness):
        self.location = location
        self.aggressiveness = aggressiveness

    def fly(self):
        self.location = [max(0, min(gridSize, self.location[i] + random.randint(-self.aggressiveness, self.aggressiveness))) for i in range(2)]

# Simulation parameters
gridSize = 15
pigeons = [Pigeon([random.randint(0, gridSize) for _ in range(2)], random.randint(1, 3)) for _ in range(200)]
hawks = [Hawk([random.randint(0, gridSize) for _ in range(2)], random.randint(1, 1)) for _ in range(20)]

fig, ax = plt.subplots()
ax.set_xlim(0, gridSize)
ax.set_ylim(0, gridSize)

pigeon_dots, = ax.plot([], [], 'bo', ms=6)  # ms is marker size
hawk_dots, = ax.plot([], [], 'ro', ms=8)

def update(frame):
    # Move all birds
    for pigeon in pigeons:
        pigeon.fly()
    for hawk in hawks:
        hawk.fly()
    
    # Update the positions on the plot
    pigeon_positions = [pigeon.location for pigeon in pigeons]
    hawk_positions = [hawk.location for hawk in hawks]

    pigeon_x, pigeon_y = zip(*pigeon_positions) if pigeon_positions else ([], [])
    hawk_x, hawk_y = zip(*hawk_positions) if hawk_positions else ([], [])

    pigeon_dots.set_data(pigeon_x, pigeon_y)
    hawk_dots.set_data(hawk_x, hawk_y)

    return pigeon_dots, hawk_dots,

ani = FuncAnimation(fig, update, frames=30, blit=True, interval=2000, repeat=False)
plt.show()
