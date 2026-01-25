#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:41:05 2024

@author: realmac
"""

# simulation.py
# execute by plot_population.py or animation.py

import random
import numpy as np
from collections import defaultdict

class Pigeon:
    def __init__(self, location, speed, gridSize):
        self.location = np.array(location) 
        self.speed = speed
        self.gridSize = gridSize  # Store gridSize as an instance variable

    def fly(self):
        # Update location within grid constraints, using the instance's gridSize
        self.location += np.random.randint(-self.speed, self.speed + 1, size=2)
        self.location = np.clip(self.location, 0, self.gridSize - 1)
        
class Hawk:
    def __init__(self, location, aggressiveness, gridSize):
        self.location = np.array(location)
        self.aggressiveness = aggressiveness
        self.Energy = 2
        self.huntingBoundary = aggressiveness
        self.gridSize = gridSize  # Store gridSize as an instance variable

    def fly(self):
        # Update location within grid constraints, using the instance's gridSize
        self.location += np.random.randint(-self.huntingBoundary, self.huntingBoundary + 1, size=2)
        self.location = np.clip(self.location, 0, self.gridSize - 1)


def run_simulation(variables):
    # Create pigeons and hawks with the given gridSize
    [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, Hawk_huntingRate, Hawk_birthRate,gridSize,num_generations, density_limit] = variables
    num_pigeons = int((gridSize**2)/2)
    num_hawks = gridSize
    pigeons = [Pigeon([random.randint(0, gridSize-1) for _ in range(2)], random.randint(1, Pigeon_maxSpeed), gridSize) for _ in range(num_pigeons)]
    hawks = [Hawk([random.randint(0, gridSize-1) for _ in range(2)], random.randint(1, Hawk_maxAggressiveness), gridSize) for _ in range(num_hawks)]
    population_sizes = {'pigeons': [], 'hawks': []}
    positions = {'pigeons': [], 'hawks': []}
    attribute_counts = {'aggressiveness' : []}

    # Run the simulation for the specified number of generations
    for _ in range(num_generations):
        pigeon_positions = []
        hawk_positions = []
        aggressiveness_counts = defaultdict(int)

        # Hunting
        pigeon_hunted = set()
        hawk_hunting = set()
        for j, hawk in enumerate(hawks):
            hawk.Energy -= hawk.aggressiveness # Hunting consumes energy comparison to its aggressiveness
            for i, pigeon in enumerate(pigeons):
                distance = np.linalg.norm(hawk.location - pigeon.location) # Hawk hunts the prey within it's hunting range
                if distance <= hawk.huntingBoundary and random.random() < Hawk_huntingRate:
                    hawk.location = pigeon.location # if pigeon is in the hunting boundary of hawk, hawk hunt pigeon, and move its position to where pigeon was
                    hawk.Energy = 2 # Hawk regain energy
                    pigeon_hunted.add(i) # Pigeon hunted died
                    hawk_hunting.add(j)
                    break # end hunting
        pigeons = [pigeon for i, pigeon in enumerate(pigeons) if i not in pigeon_hunted]  # Pigeon hunted died
        hawks = [hawk for hawk in hawks if hawk.Energy > 0]  # Retain only hawks with energy above 0
        
        # Breed
        pigeon_density = [[0 for _ in range(gridSize)] for _ in range(gridSize)]
        for pigeon in pigeons:
               pigeon_density[pigeon.location[0]][pigeon.location[1]] += 1
            
        hawks_breed = [Hawk(hawk.location, hawk.aggressiveness, gridSize) for hawk in hawks if random.random() < Hawk_birthRate]

        hawks += hawks_breed  # Use += to append newly breed hawks
        pigeons += [Pigeon(pigeon.location, pigeon.speed, gridSize) for pigeon in pigeons if random.random() < Pigeon_birthRate and pigeon_density[pigeon.location[0]][pigeon.location[1]] < density_limit]
     
        # Fly
        for pigeon in pigeons:
            pigeon.fly()
            pigeon_positions.append(pigeon.location)
        for j, hawk in enumerate(hawks):
            if j not in hawk_hunting:
                hawk.fly()
            hawk_positions.append(hawk.location)
            aggressiveness_counts[hawk.aggressiveness] += 1 # Count the #hawk by each aggressiveness.
        
        # Record population sizes and position after each generation
        positions['pigeons'].append(pigeon_positions)
        positions['hawks'].append(hawk_positions)
        population_sizes['pigeons'].append(len(pigeons))
        population_sizes['hawks'].append(len(hawks))
        attribute_counts['aggressiveness'].append(dict(aggressiveness_counts))

    return population_sizes, positions, attribute_counts


