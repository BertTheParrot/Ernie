"""
🔨 Southern Biome - Ernie's Adventure
Developer: Available for Assignment
Location: South (around coordinates 30, 65)

A crafting village known for its skilled blacksmith.
"""

import random
from typing import List

def create_southern_section(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the southern village section"""
    
    # Village clearing
    for y in range(62, 68):
        for x in range(28, 34):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass
    
    # Village buildings
    buildings = [(30, 64), (32, 64), (29, 66), (33, 66)]
    for bx, by in buildings:
        if 0 < bx < WORLD_WIDTH-1 and 0 < by < WORLD_HEIGHT-1:
            world[by][bx] = 'H'
    
    # Blacksmith forge
    world[65][30] = 'H'  # Forge

def get_southern_npcs():
    """Return NPCs for the southern village"""
    npcs = []
    
    blacksmith = {
        'name': 'Village Blacksmith',
        'x': 30, 'y': 65,
        'dialogue': [
            "The forge burns hot today!",
            "I craft tools for all the local farmers.",
            "The ore from the eastern mountains is finest.",
            "Need anything repaired, traveler?"
        ]
    }
    npcs.append(blacksmith)
    
    wise_woman = {
        'name': 'Wise Woman',
        'x': 32, 'y': 63,
        'dialogue': [
            "I sense great potential in you, young one.",
            "The world is vast and full of mysteries.",
            "Your journey has only just begun.",
            "Trust in yourself and you'll find your way."
        ]
    }
    npcs.append(wise_woman)
    
    return npcs 