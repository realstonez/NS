#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 22:24:29 2024

@author: realmac
"""

import random
import matplotlib.pyplot as plt

class Pigeon:
    def __init__(self, speed):
        self.speed = speed
    
    def fly(self):
        pass  # Pigeons don't hunt, just fly

class Hawk:
    def __init__(self, aggressiveness):
        self.aggressiveness = aggressiveness
    
    def hunt(self):
        pass  # Hawks don't fly, just hunt

# Simulate natural selection
population_sizes = {'Pigeons': [], 'Hawks': []}
pigeons = [Pigeon(random.uniform(5, 10)) for _ in range(20)]
hawks = [Hawk(random.uniform(0, 1)) for _ in range(20)]

for generation in range(10):  # Simulate 10 generations
    # Determine survival and reproduction rates based on traits
    # For simplicity, let's assume pigeons always survive and reproduce,
    # while hawks survive and reproduce only if they catch a pigeon
    
    # Update population size (for simplicity, we're not modeling population growth/decline)
    pigeons.extend([Pigeon(random.uniform(5, 10)) for _ in range(3)])  # Pigeons reproduce
    surviving_hawks = [hawk for hawk in hawks if random.random() < hawk.aggressiveness]
    hawks.extend([Hawk(random.uniform(0, 1)) for _ in range(len(surviving_hawks))])  # Hawks reproduce
    
    # Record population sizes
    population_sizes['Pigeons'].append(len(pigeons))
    population_sizes['Hawks'].append(len(hawks))

# Visualize population changes
generations = range(1, 11)  # Number of generations
plt.plot(generations, population_sizes['Pigeons'], label='Pigeons', marker='o')
plt.plot(generations, population_sizes['Hawks'], label='Hawks', marker='o')
plt.xlabel('Generation')
plt.ylabel('Population Size')
plt.title('Population Dynamics')
plt.legend()
plt.grid(True)
plt.show()