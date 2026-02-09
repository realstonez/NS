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

class Agent:
    def __init__(self, location, speed, grid_size):
        self.location = np.array(location)
        self.speed = speed
        self.grid_size = grid_size
        self.alive = True  # We use this flag instead of removing from lists immediately

    def move(self):
        # Update location with random movement
        move_vector = np.random.randint(-self.speed, self.speed + 1, size=2)
        self.location += move_vector
        self.location = np.clip(self.location, 0, self.grid_size - 1)

class Pigeon(Agent):
    def __init__(self, location, speed, grid_size):
        super().__init__(location, speed, grid_size)

class Hawk(Agent):
    def __init__(self, location, aggressiveness, grid_size):
        super().__init__(location, aggressiveness, grid_size) # Speed linked to agg?
        self.aggressiveness = aggressiveness
        self.energy = 2
        self.hunting_boundary = aggressiveness

def run_simulation(variables):
    # Unpack variables
    [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, 
     Hawk_huntingRate, Hawk_birthRate, gridSize, num_generations, density_limit] = variables

    # Initialize Population
    num_pigeons = int((gridSize**2)/2)
    num_hawks = gridSize
    
    pigeons = [Pigeon([random.randint(0, gridSize-1) for _ in range(2)], 
                      random.randint(1, Pigeon_maxSpeed), gridSize) for _ in range(num_pigeons)]
    hawks = [Hawk([random.randint(0, gridSize-1) for _ in range(2)], 
                  random.randint(1, Hawk_maxAggressiveness), gridSize) for _ in range(num_hawks)]

    # Data Recording
    history = {
        'population': {'pigeons': [], 'hawks': []},
        'positions': {'pigeons': [], 'hawks': []},
        'aggressiveness': []
    }

    for gen in range(num_generations):
        # --- 1. OPTIMIZATION: Build the Spatial Map ---
        # Instead of checking everyone, we group them by location (x,y)
        pigeon_map = defaultdict(list)
        for p in pigeons:
            if p.alive:
                loc_tuple = tuple(p.location)
                pigeon_map[loc_tuple].append(p)

        hawk_map = defaultdict(list)
        for h in hawks:
            if h.alive:
                loc_tuple = tuple(h.location)
                hawk_map[loc_tuple].append(h)

        # --- 2. HUNTING PHASE ---
        for hawk in hawks:
            if not hawk.alive: continue
            
            hawk.energy -= hawk.aggressiveness # Metabolic cost
            
            # Optimization: Only look for pigeons AT the hawk's specific location
            # (or you can check neighbors if you want to be more complex later)
            loc_tuple = tuple(hawk.location)
            local_pigeons = pigeon_map.get(loc_tuple, [])
            
            # Simple interaction logic
            if local_pigeons and random.random() < Hawk_huntingRate:
                victim = random.choice(local_pigeons)
                if victim.alive: # Ensure we don't eat a dead bird twice
                    victim.alive = False
                    hawk.energy = 2 # Regain energy
        
        # --- 3. CLEANUP PHASE (Safe List Removal) ---
        # Re-build lists keeping only the living
        pigeons = [p for p in pigeons if p.alive]
        hawks = [h for h in hawks if h.alive and h.energy > 0]

        # --- 4. BREEDING PHASE ---
        # (Simplified logic for the base engine)
        new_hawks = []
        for h in hawks:
            if random.random() < Hawk_birthRate:
                # Pass parent traits to child
                new_hawks.append(Hawk(h.location, h.aggressiveness, gridSize))
        
        new_pigeons = []
        for p in pigeons:
            # Check local density for pigeons
            loc_tuple = tuple(p.location)
            # Re-count live pigeons at this spot
            local_count = len([bird for bird in pigeon_map[loc_tuple] if bird.alive])
            
            if random.random() < Pigeon_birthRate and local_count < density_limit:
                new_pigeons.append(Pigeon(p.location, p.speed, gridSize))

        hawks.extend(new_hawks)
        pigeons.extend(new_pigeons)

        # --- 5. MOVEMENT & RECORDING ---
        current_p_pos = []
        for p in pigeons:
            p.move()
            current_p_pos.append(p.location.copy()) # .copy() is crucial for history!
            
        current_h_pos = []
        agg_counts = defaultdict(int)
        for h in hawks:
            h.move()
            current_h_pos.append(h.location.copy())
            agg_counts[h.aggressiveness] += 1

        # Store data
        history['positions']['pigeons'].append(current_p_pos)
        history['positions']['hawks'].append(current_h_pos)
        history['population']['pigeons'].append(len(pigeons))
        history['population']['hawks'].append(len(hawks))
        history['aggressiveness'].append(dict(agg_counts))

    return history['population'], history['positions'], {'aggressiveness': history['aggressiveness']}