"""
🏺 Ruins Biome - Ernie's Adventure
Developer: Available for Assignment
Location: Southwest (around coordinates 15, 55)

Ancient mysterious ruins from a lost civilization.
"""

import random
from typing import List

def create_ruins_section(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the ancient ruins section (Southwest)"""
    
    ruins_center_x, ruins_center_y = 15, 55
    for y in range(ruins_center_y-5, ruins_center_y+5):
        for x in range(ruins_center_x-5, ruins_center_x+5):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                if random.random() < 0.6:
                    world[y][x] = 'S'  # Stone ruins
                elif random.random() < 0.3:
                    world[y][x] = '#'  # Broken walls
    
    # Central altar
    world[55][15] = 'A'  # Altar

def get_ruins_npcs():
    """Return NPCs for the ruins area"""
    npcs = []
    
    archaeologist = {
        'name': 'Archaeologist',
        'x': 15, 'y': 53,
        'dialogue': [
            "These ruins predate any known civilization!",
            "I've been studying these stones for years.",
            "The symbols suggest a lost magical culture.",
            "Be careful not to disturb anything!"
        ]
    }
    npcs.append(archaeologist)
    
    return npcs 