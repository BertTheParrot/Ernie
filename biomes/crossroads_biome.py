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
    
    # Tavern building (2x2)
    tavern_area = [(60, 49), (61, 49), (60, 50), (61, 50)]
    for tx, ty in tavern_area:
        if 0 < tx < WORLD_WIDTH-1 and 0 < ty < WORLD_HEIGHT-1:
            world[ty][tx] = 'H'  # Tavern building
    
    # Inn for travelers
    world[58][51] = 'H'
    
    # Stable for horses
    world[63][52] = 'H'

def get_crossroads_npcs():
    """Return NPCs for the crossroads area"""
    npcs = []
    
    tavern_keeper = {
        'name': 'Tavern Keeper',
        'x': 60, 'y': 50,
        'dialogue': [
            "Welcome to the Crossroads Tavern!",
            "Travelers from all lands stop here.",
            "Have you heard the legends of the ruins?",
            "Stay the night - the roads are dark!"
        ]
    }
    npcs.append(tavern_keeper)
    
    return npcs 