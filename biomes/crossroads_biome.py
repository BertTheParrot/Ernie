"""
🍺 Crossroads Biome - Ernie's Adventure
Developer: Shared/Central Hub
Location: Center (around coordinates 60, 50)

This is the central meeting point of the world where all roads converge.
"""

import random
from typing import List

def create_crossroads_section(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the crossroads section (Center)"""
    
    # MASSIVE Tavern building (7x7 - biggest in the world!)
    tavern_x, tavern_y = 58, 47
    for ty in range(tavern_y, tavern_y + 7):
        for tx in range(tavern_x, tavern_x + 7):
            if 0 < tx < WORLD_WIDTH-1 and 0 < ty < WORLD_HEIGHT-1:
                world[ty][tx] = 'H'  # Tavern building
    
    # Inn for travelers (5x5)
    inn_x, inn_y = 50, 50
    for ty in range(inn_y, inn_y + 5):
        for tx in range(inn_x, inn_x + 5):
            if 0 < tx < WORLD_WIDTH-1 and 0 < ty < WORLD_HEIGHT-1:
                world[ty][tx] = 'H'  # Inn
    
    # Stable for horses (4x4)
    stable_x, stable_y = 66, 50
    for ty in range(stable_y, stable_y + 4):
        for tx in range(stable_x, stable_x + 4):
            if 0 < tx < WORLD_WIDTH-1 and 0 < ty < WORLD_HEIGHT-1:
                world[ty][tx] = 'H'  # Stable

def get_crossroads_npcs():
    """Return NPCs for the crossroads area"""
    npcs = []
    
    tavern_keeper = {
        'name': 'Tavern Keeper',
        'x': 61, 'y': 50,  # At the massive 7x7 tavern
        'dialogue': [
            "Welcome to the Crossroads Tavern!",
            "Travelers from all lands stop here.",
            "Have you heard the legends of the ruins?",
            "Stay the night - the roads are dark!",
            "Our tavern is now the grandest in all the land!"
        ]
    }
    npcs.append(tavern_keeper)
    
    return npcs 