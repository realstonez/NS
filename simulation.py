#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:41:05 2024

@author: realmac
"""

# simulation.py

import random

class Pigeon:
    def __init__(self, location, speed, gridSize):
        self.location = location
        self.speed = speed
        self.gridSize = gridSize  # Store gridSize as an instance variable

    def fly(self):
        # Update location within grid constraints, using the instance's gridSize
        self.location = [max(0, min(self.gridSize-1, self.location[i] + random.randint(-self.speed, self.speed))) for i in range(2)]

class Hawk:
    def __init__(self, location, aggressiveness, gridSize):
        self.location = location
        self.aggressiveness = aggressiveness
        self.gridSize = gridSize  # Store gridSize as an instance variable

    def fly(self):
        # Update location within grid constraints, using the instance's gridSize
        self.location = [max(0, min(self.gridSize-1, self.location[i] + random.randint(-self.aggressiveness, self.aggressiveness))) for i in range(2)]

def run_simulation(variables):
    # Create pigeons and hawks with the given gridSize
    [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, Hawk_huntingRate, Hawk_birthRate,gridSize,num_generations] = variables
    num_pigeons = int((gridSize**2)/2)
    num_hawks = gridSize
    pigeons = [Pigeon([random.randint(0, gridSize-1) for _ in range(2)], random.randint(1, Pigeon_maxSpeed), gridSize) for _ in range(num_pigeons)]
    hawks = [Hawk([random.randint(0, gridSize-1) for _ in range(2)], random.randint(1, Hawk_maxAggressiveness), gridSize) for _ in range(num_hawks)]
    population_sizes = {'pigeons': [], 'hawks': []}
    positions = {'pigeons': [], 'hawks': []}

    # Run the simulation for the specified number of generations
    for _ in range(num_generations):
        pigeon_positions = []
        hawk_positions = []

        # Hunt
        hawk_hunt = set()
        pigeon_hunted = set()
        for j,hawk in enumerate(hawks):
            for i, pigeon in enumerate(pigeons):
                if hawk.location == pigeon.location and random.random() < Hawk_huntingRate:
                    hawk_hunt.add(j)
                    pigeon_hunted.add(i)
                    break # end hunting
        hawks_survive = [hawk for j, hawk in enumerate(hawks) if j in hawk_hunt] #hawk failed hunting dies
        pigeons_survive = [pigeon for i, pigeon in enumerate(pigeons) if i not in pigeon_hunted] #pigeon hunted died
        hawks = hawks_survive
        pigeons = pigeons_survive
        
        # Breed
        hawks_breed = [Hawk(hawk.location, hawk.aggressiveness, gridSize) for hawk in hawks if random.random() < Hawk_birthRate]
        pigeon_breed = [Pigeon(pigeon.location, pigeon.speed, gridSize) for pigeon in pigeons if random.random() < Pigeon_birthRate]
        hawks.extend(hawks_breed)
        pigeons.extend(pigeon_breed)
        
        # Fly
        for pigeon in pigeons:
            pigeon.fly()
            pigeon_positions.append(pigeon.location.copy())
        for hawk in hawks:
            hawk.fly()
            hawk_positions.append(hawk.location.copy())
        
        # Record population sizes and position after each generation
        positions['pigeons'].append(pigeon_positions)
        positions['hawks'].append(hawk_positions)
        population_sizes['pigeons'].append(len(pigeons))
        population_sizes['hawks'].append(len(hawks))

    return population_sizes, positions


