#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 22:28:10 2024

@author: realmac
"""

# animation.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from simulation import run_simulation

def animate_simulation(positions, gridSize):
    fig, ax = plt.subplots()
    ax.set_xlim(0, gridSize)
    ax.set_ylim(0, gridSize)

    pigeon_dots, = ax.plot([], [], 'bo', ms=6)
    hawk_dots, = ax.plot([], [], 'ro', ms=8)

    def update(frame):
        pigeon_positions = positions['pigeons'][frame]
        hawk_positions = positions['hawks'][frame]
        
        pigeon_x, pigeon_y = zip(*pigeon_positions) if pigeon_positions else ([], [])
        hawk_x, hawk_y = zip(*hawk_positions) if hawk_positions else ([], [])

        pigeon_dots.set_data(pigeon_x, pigeon_y)
        hawk_dots.set_data(hawk_x, hawk_y)

        return pigeon_dots, hawk_dots,

    ani = FuncAnimation(fig, update, frames=len(positions['pigeons']), interval=200, blit=True)
    plt.show()

if __name__ == "__main__":
    # variables
    Pigeon_maxSpeed = 3
    Pigeon_birthRate = 0.5
    Hawk_maxAggressiveness = 2
    Hawk_huntingRate = 1
    Hawk_birthRate = 1
    gridSize = 16
    num_generations = 30
    
    variables=[Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, Hawk_huntingRate, Hawk_birthRate,gridSize,num_generations]
    
    population_sizes, positions = run_simulation(variables)
    animate_simulation(positions, gridSize)


