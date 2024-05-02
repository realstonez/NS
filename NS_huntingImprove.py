#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:41:05 2024

@author: realmac
"""

import random
import matplotlib.pyplot as plt

class Pigeon:
    def __init__(self, location, speed):
        self.location = location
        self.speed = speed

    def fly(self):
        # Correctly add element-wise for new location
        self.location = [max(0, min(gridSize, self.location[i] + random.randint(-self.speed, self.speed))) for i in range(2)]

class Hawk:
    def __init__(self, location, aggressiveness):
        self.location = location
        self.aggressiveness = aggressiveness

    def fly(self):
        # Correctly add element-wise for new location
        self.location = [max(0, min(gridSize, self.location[i] + random.randint(-self.aggressiveness, self.aggressiveness))) for i in range(2)]

        
        
# Simulate natural selection
breeding_rate_pigeon = 0.2 # breeding rate of pigeon 
breeding_rate_hawk = 1
hunting_rate_hawk = 0.5 # possibility of hawks' hunting success 
speed_min_pigeon , speed_max_pigeon = 1,3
agg_min_hawk, agg_max_hawk = 1,1 # aggressiveness - put energy more and enhence the hunting possibility
gridSize = 15

Generation = 25

population_sizes = {'Pigeons': [] , 'Hawks': []}


pigeons = [Pigeon([random.randint(0,gridSize) for _ in range(2)],random.randint(speed_min_pigeon, speed_max_pigeon)) for _ in range(200)]

hawks = [Hawk([random.randint(0,gridSize) for _ in range(2)],random.randint(agg_min_hawk, agg_max_hawk)) for _ in range(20)]

for generation in range(Generation):
    # Move all birds
    for pigeon in pigeons:
        pigeon.fly()
    for hawk in hawks:
        hawk.fly()
    

    # Determine which pigeons are hunted
    hunted_pigeon = set()      # Using a set to avoid duplicates
    hunting_hawk = set() 
    for i, hawk in enumerate(hawks):
        for j, pigeon in enumerate(pigeons):
            if pigeon.location == hawk.location and j not in hunted_pigeon and random.random() < hunting_rate_hawk:
                hunted_pigeon.add(j)
                hunting_hawk.add(i)
                break #end hunting

    # Hunting
    new_pigeons = [pigeon for j, pigeon in enumerate(pigeons) if j not in hunted_pigeon ]
    new_hawks = [hawk for i, hawk in enumerate(hawks) if i in hunting_hawk ]
    
    pigeons = new_pigeons
    hawks = new_hawks

    # Reproduce
    breed_pigeon = [Pigeon(pigeon.location,pigeon.speed) for pigeon in pigeons if random.random() < breeding_rate_pigeon]
    breed_hawk = [Hawk(hawk.location,hawk.aggressiveness) for hawk in hawks if random.random() < breeding_rate_hawk]
    
    pigeons.extend(breed_pigeon)
    hawks.extend(breed_hawk)
    
    # Record population sizes
    population_sizes['Pigeons'].append(len(pigeons))
    population_sizes['Hawks'].append(len(hawks))

# Visualize population changes
generations = range(1, len(population_sizes['Pigeons']) + 1)  # Dynamically adjust the range
plt.plot(generations, population_sizes['Pigeons'], label='Pigeons', marker='o')
plt.plot(generations, population_sizes['Hawks'], label='Hawks', marker='o')
plt.xlabel('Generation')
plt.ylabel('Population Size')
plt.title('Population Dynamics')
plt.legend()
plt.grid(True)
plt.show()
