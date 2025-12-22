#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:45:13 2024

@author: realmac
"""

# plot_population.py

import matplotlib.pyplot as plt
import numpy as np

def plot_population_changes(scenario):
    # Simulation parameters
    Pigeon_maxSpeed = 3
    Pigeon_birthRate = 0.7
    Hawk_maxAggressiveness = 2
    Hawk_huntingRate = 0.1
    Hawk_birthRate = 0.1
    gridSize = 16
    num_generations = 100
    density_limit = 2
    Hawk_huntingBoundary = 1
    
    if scenario == 'NS':        
        variables = [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, Hawk_huntingRate, Hawk_birthRate, gridSize, num_generations, density_limit]
        from simulation import run_simulation

    elif scenario == 'SS':
        variables = [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, Hawk_huntingRate, Hawk_birthRate, gridSize, num_generations, density_limit]
        from SS_simulation import run_simulation

    elif scenario == 'AR':
        variables = [Pigeon_maxSpeed, Hawk_maxAggressiveness, Hawk_birthRate, gridSize,num_generations, density_limit]        
        from AR_simulation import run_simulation
    
  
    population_sizes, positions, attribute_counts = run_simulation(variables)
    
    # Plot #hawk and #pigeon by generation
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
    
    # Plot hawk's average aggressiveness
    aggressiveness_avg = []
    for gen_aggressiveness in attribute_counts['aggressiveness']:
        total_hawks = sum(gen_aggressiveness.values())
        weighted_sum = sum(aggr * count for aggr, count in gen_aggressiveness.items())
        if total_hawks > 0:
            avg_aggr = weighted_sum / total_hawks
        else:
            avg_aggr = 0
        aggressiveness_avg.append(avg_aggr)
    
    plt.figure(figsize=(10, 5))
    plt.plot(generations, aggressiveness_avg, label='Average Aggressiveness', marker='x')
    plt.xlabel('Generation')
    plt.ylabel('Average Aggressiveness')
    plt.title('Aggressiveness Dynamics Over Generations')
    plt.legend()
    plt.grid(True)
    plt.show()
if __name__ == "__main__":
    plot_population_changes('AR')
