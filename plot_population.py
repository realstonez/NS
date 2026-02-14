#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:45:13 2024

@author: realmac
"""

# plot_population.py

import matplotlib
matplotlib.use('TkAgg')  # <--- ADD THIS LINE (Forces a pop-up window on Mac)
import matplotlib.pyplot as plt
from simulation import run_simulation
import numpy as np

def plot_population_changes(scenario):
    # Simulation parameters
    Pigeon_maxSpeed = 3
    Pigeon_birthRate = 0.9
    Hawk_maxAggressiveness = 2 # should be modified. want to set as a variable that hawk fight each other
    Hawk_huntingRate = 0.2
    Hawk_birthRate = 0.1
    gridSize = 16
    num_generations = 80
    density_limit = 2
    
    variables = [Pigeon_maxSpeed, Pigeon_birthRate, Hawk_maxAggressiveness, Hawk_huntingRate, Hawk_birthRate, gridSize, num_generations, density_limit]
  
    population_sizes, positions, attribute_counts = run_simulation(variables)
    
    # ... (Keep the simulation running part the same) ...
    # population_sizes, positions, attribute_counts = run_simulation(variables)
    
    # Plot #hawk and #pigeon by generation
    generations = list(range(1, num_generations + 1))
    
    # --- DATA PREP (Keep this part) ---
    all_levels = set()
    for gen_data in attribute_counts['aggressiveness']:
        all_levels.update(gen_data.keys())
    sorted_levels = sorted(list(all_levels))
    
    level_histories = {level: [] for level in sorted_levels}
    for gen_data in attribute_counts['aggressiveness']:
        for level in sorted_levels:
            level_histories[level].append(gen_data.get(level, 0))

    # --- NEW: DUAL-AXIS PLOT ---
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Left Axis: Hawks (Colored lines)
    color_map = plt.get_cmap('tab10') # Get a color palette
    for i, level in enumerate(sorted_levels):
        ax1.plot(generations, level_histories[level], label=f'Hawk Level {level}', color=color_map(i))
    
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Number of Hawks', color='tab:blue', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True, alpha=0.3)

    # Right Axis: Pigeons (Black dashed line)
    ax2 = ax1.twinx()  # <--- This creates the second axis sharing X
    ax2.plot(generations, population_sizes['pigeons'], color='black', linestyle='--', linewidth=2.5, label='Pigeons')
    ax2.set_ylabel('Number of Pigeons', color='black', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='black')

    # Combined Legend (Tricky part: merging two axes into one legend box)
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.title('Co-Evolution: Hawk Levels vs. Pigeon Population')
    
    # --- SECOND PLOT (Average Aggressiveness) ---
    # We create a new figure so it doesn't overwrite the first one
    plt.figure(figsize=(10, 5))
    
    # (Calculate average code stays the same...)
    aggressiveness_avg = []
    for gen_aggressiveness in attribute_counts['aggressiveness']:
        total_hawks = sum(gen_aggressiveness.values())
        weighted_sum = sum(aggr * count for aggr, count in gen_aggressiveness.items())
        aggressiveness_avg.append(weighted_sum / total_hawks if total_hawks > 0 else 0)
    
    plt.plot(generations, aggressiveness_avg, label='Avg Aggressiveness', color='red', marker='x')
    plt.xlabel('Generation')
    plt.ylabel('Average Aggressiveness')
    plt.title('Trend: Is the population getting angrier?')
    plt.grid(True)

    # SHOW ALL CHARTS AT ONCE
    plt.show()
if __name__ == "__main__":
    plot_population_changes('NS')