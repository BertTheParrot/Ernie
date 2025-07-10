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
    
    # Village clearing (bigger for large houses)
    for y in range(60, 75):
        for x in range(20, 45):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass
    
    # Village buildings (5x5 each, well-spaced)
    buildings = [(22, 62), (32, 62), (27, 68)]  # Better spacing
    for bx, by in buildings:
        for house_y in range(by, by + 5):
            for house_x in range(bx, bx + 5):
                if 0 < house_x < WORLD_WIDTH-1 and 0 < house_y < WORLD_HEIGHT-1:
                    world[house_y][house_x] = 'H'  # House
    
    # Blacksmith forge (6x6 - biggest workshop!)
    forge_x, forge_y = 37, 65
    for forge_y_tile in range(forge_y, forge_y + 6):
        for forge_x_tile in range(forge_x, forge_x + 6):
            if 0 < forge_x_tile < WORLD_WIDTH-1 and 0 < forge_y_tile < WORLD_HEIGHT-1:
                world[forge_y_tile][forge_x_tile] = 'H'  # Forge

def get_southern_npcs():
    """Return NPCs for the southern village"""
    npcs = []
    
    blacksmith = {
        'name': 'Village Blacksmith',
        'x': 39, 'y': 67,  # At the massive 6x6 forge
        'dialogue': [
            "The forge burns hot today!",
            "I craft tools for all the local farmers.",
            "The ore from the eastern mountains is finest.",
            "Need anything repaired, traveler?",
            "My new forge is the biggest in the region!"
        ]
    }
    npcs.append(blacksmith)
    
    wise_woman = {
        'name': 'Wise Woman',
        'x': 24, 'y': 64,  # At the first big house
        'dialogue': [
            "I sense great potential in you, young one.",
            "The world is vast and full of mysteries.",
            "Your journey has only just begun.",
            "Trust in yourself and you'll find your way.",
            "These grand houses reflect our village's wisdom and prosperity."
        ]
    }
    npcs.append(wise_woman)
    
    return npcs 