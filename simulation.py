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
        self.alive = True

    def move(self):
        move_vector = np.random.randint(-self.speed, self.speed + 1, size=2)
        self.location += move_vector
        self.location = np.clip(self.location, 0, self.grid_size - 1)

class Pigeon(Agent):
    def __init__(self, location, speed, grid_size):
        super().__init__(location, speed, grid_size)

class Hawk(Agent):
    def __init__(self, location, aggressiveness, grid_size):
        # Speed is linked to aggressiveness? For now, we keep it separate or fixed.
        # Let's assume speed = aggressiveness for movement range, or keep it 1.
        super().__init__(location, aggressiveness, grid_size) 
        self.aggressiveness = aggressiveness
        self.energy = 50  # Start mid-way (Max is 100)
        
        # Define the search offsets for this specific hawk based on its level
        # Level 0: Distance 0 (Center)
        self.search_tiers = [ [(0,0)] ] 
        
        # Level 1: Add Distance 1 (Up, Down, Left, Right)
        if aggressiveness >= 1:
            self.search_tiers.append([(0,1), (0,-1), (1,0), (-1,0)])
            
        # Level 2: Add Diagonals (Corners)
        if aggressiveness >= 2:
            self.search_tiers.append([(1,1), (1,-1), (-1,1), (-1,-1)])
            
        # Level 3: Add Distance 2 (Far reach)
        if aggressiveness >= 3:
            self.search_tiers.append([(0,2), (0,-2), (2,0), (-2,0)])

def run_simulation(variables):
    [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, 
     Hawk_huntingRate, Hawk_birthRate, gridSize, num_generations, density_limit] = variables

    # --- Constants for Energy Economics ---
    MAX_ENERGY = 100
    LIVING_COST = 10
    HUNTING_GAIN = 30
    LAZY_THRESHOLD = 80
    
    # Costs mapped by list index: [Dist0_Cost, Dist1_Cost, Diagonal_Cost, Dist2_Cost]
    TIER_COSTS = [1, 2, 3, 5] 

    # Initialize Population
    num_pigeons = int((gridSize**2)/2)
    num_hawks = gridSize
    
    pigeons = [Pigeon([random.randint(0, gridSize-1) for _ in range(2)], 
                      random.randint(1, Pigeon_maxSpeed), gridSize) for _ in range(num_pigeons)]
    
    # Hawks initialized with random aggressiveness (0 to Max)
    hawks = [Hawk([random.randint(0, gridSize-1) for _ in range(2)], 
                  random.randint(0, Hawk_maxAggressiveness), gridSize) for _ in range(num_hawks)]

    # Data Recording
    history = {
        'population': {'pigeons': [], 'hawks': []},
        'positions': {'pigeons': [], 'hawks': []},
        'aggressiveness': []
    }

    for gen in range(num_generations):
        print(f"Generation {gen + 1}/{num_generations} | Pigeons: {len(pigeons)} | Hawks: {len(hawks)}")

        # --- 1. SPATIAL MAP (The "Phonebook") ---
        # ... rest of your code ...
        # --- 1. SPATIAL MAP (The "Phonebook") ---
        pigeon_map = defaultdict(list)
        for p in pigeons:
            if p.alive:
                pigeon_map[tuple(p.location)].append(p)

        # --- 2. HUNTING PHASE ---
        # Sort hawks: Highest Aggressiveness gets to hunt first
        hawks.sort(key=lambda h: h.aggressiveness, reverse=True)
        
        for hawk in hawks:
            if not hawk.alive: continue
            
            # A. Living Tax (Paid daily)
            hawk.energy -= LIVING_COST
            
            # B. Lazy Check
            if hawk.energy > LAZY_THRESHOLD:
                continue # Skip hunting, sleep today

            # C. Hunting Logic (Tier by Tier)
            # We iterate through tiers to prioritize closest targets (Option A)
            hunt_successful = False
            
            for tier_index, offsets in enumerate(hawk.search_tiers):
                cost = TIER_COSTS[tier_index]
                
                # Check all cells in this distance tier
                potential_victims = []
                for dx, dy in offsets:
                    # Calculate target coordinate
                    tx, ty = hawk.location[0] + dx, hawk.location[1] + dy
                    
                    # Boundary Check: Wall (Cannot hunt outside grid)
                    if 0 <= tx < gridSize and 0 <= ty < gridSize:
                        # Look in the phonebook
                        cell_pigeons = pigeon_map.get((tx, ty), [])
                        # Only see ALIVE pigeons
                        live_in_cell = [p for p in cell_pigeons if p.alive]
                        if live_in_cell:
                            potential_victims.extend(live_in_cell)

                # If we found victims at this distance level, TRY to hunt one
                if potential_victims:
                    # Pick one random victim from this tier
                    victim = random.choice(potential_victims)
                    
                    # PAY THE COST (Attempt Cost)
                    hawk.energy -= cost
                    
                    # Roll the dice
                    if random.random() < Hawk_huntingRate:
                        victim.alive = False # Kill
                        hawk.energy += HUNTING_GAIN
                        # Cap the energy
                        if hawk.energy > MAX_ENERGY:
                            hawk.energy = MAX_ENERGY
                        
                        hunt_successful = True # Mark success
                    
                    # Critical Rule: Whether success or fail, we stop checking this tier?
                    # Actually, usually if you fail a hunt, do you try another bird instantly?
                    # For "Armament Race", usually 1 attempt per turn is standard.
                    # If you want them to keep trying until they run out of energy, remove this break.
                    # But based on "consumes energy proportional to distance", let's assume 1 attempt per tier or 1 attempt total.
                    # YOUR RULE: "once it succeeded... it stops"
                    # Implies if fail, might continue? 
                    # Let's assume for now: Stop after 1 ATTEMPT to prevent infinite loops of failing.
                    break 
            
            # If successful, we are full/done for the day
            if hunt_successful:
                pass # Already handled by break

        # --- 3. CLEANUP & SURVIVAL ---
        # Remove dead pigeons
        pigeons = [p for p in pigeons if p.alive]
        
        # Remove starved hawks
        hawks = [h for h in hawks if h.alive and h.energy > 0]

        # --- 4. BREEDING PHASE ---
        new_hawks = []
        for h in hawks:
            # Reproduction requires significant energy? Or just random?
            # Keeping original logic for now, but adding energy cost to breed could be cool later.
            if random.random() < Hawk_birthRate:
                # Parent passes aggressiveness to child
                child = Hawk(h.location, h.aggressiveness, gridSize)
                # Child starts with half parent's energy or default? Let's say default (50).
                new_hawks.append(child)
        
        new_pigeons = []
        for p in pigeons:
            loc_tuple = tuple(p.location)
            # Re-count live pigeons at this spot for density check
            local_count = len([bird for bird in pigeon_map[loc_tuple] if bird.alive])
            
            if random.random() < Pigeon_birthRate and local_count < density_limit:
                new_pigeons.append(Pigeon(p.location, p.speed, gridSize))

        hawks.extend(new_hawks)
        pigeons.extend(new_pigeons)

        # --- 5. MOVEMENT & RECORDING ---
        current_p_pos = []
        for p in pigeons:
            p.move()
            current_p_pos.append(p.location.copy())
            
        current_h_pos = []
        agg_counts = defaultdict(int)
        for h in hawks:
            h.move()
            current_h_pos.append(h.location.copy())
            agg_counts[h.aggressiveness] += 1

        history['positions']['pigeons'].append(current_p_pos)
        history['positions']['hawks'].append(current_h_pos)
        history['population']['pigeons'].append(len(pigeons))
        history['population']['hawks'].append(len(hawks))
        history['aggressiveness'].append(dict(agg_counts))

    return history['population'], history['positions'], {'aggressiveness': history['aggressiveness']}