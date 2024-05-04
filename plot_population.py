#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:45:13 2024

@author: realmac
"""

# plot_population.py

import matplotlib.pyplot as plt
from simulation import run_simulation

def plot_population_changes():
    # Simulation parameters
    Pigeon_maxSpeed = 3
    Pigeon_birthRate = 0.2
    Hawk_maxAggressiveness = 2
    Hawk_huntingRate = 1
    Hawk_birthRate = 1
    gridSize = 16
    num_generations = 13
    
    variables = [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, Hawk_huntingRate, Hawk_birthRate, gridSize, num_generations]
  
    population_sizes, positions = run_simulation(variables)
    
    generations = list(range(1, num_generations + 1))
    plt.figure(figsize=(10, 5))
    plt.plot(generations, population_sizes['pigeons'], label='Pigeons', marker='o')
    plt.plot(generations, population_sizes['hawks'], label='Hawks', marker='o')
    plt.xlabel('Generation')
    plt.ylabel('Population Size')
    plt.title('Population Dynamics Over Generations')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_population_changes()
