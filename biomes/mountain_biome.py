"""
🏔️ Mountain Biome - Ernie's Adventure
Developer: Available for Assignment  
Location: East (around coordinates 82, 30)

This biome contains:
- Treacherous mountain peaks
- Rocky cliffs and caves
- Mountain pass through the range
- Hardy mountain dwellers
"""

import random
from typing import List

def create_mountain_section(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the mountain section (East)"""
    
    # Mountain range - tall rocky peaks
    for y in range(10, 60):
        for x in range(80, 95):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                if random.random() < 0.8:  # 80% mountains
                    world[y][x] = 'M'  # Mountain
                elif random.random() < 0.3:  # Some rock walls
                    world[y][x] = '#'  # Rock wall
    
    # Mountain pass - safe passage through peaks
    for y in range(28, 35):
        for x in range(82, 88):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = 'P'  # Path through mountains
    
    # Cave entrance - mysterious underground
    world[30][85] = 'E'  # Cave entrance

def get_mountain_npcs():
    """Return NPCs specific to the mountain area"""
    npcs = []
    
    # Mountain Guide - experienced climber
    guide = {
        'name': 'Mountain Guide',
        'x': 82, 'y': 30,  # At the mountain pass
        'dialogue': [
            "The peaks are treacherous, friend!",
            "Many caves lead deep into the mountains.",
            "I once found gems in the eastern peaks.",
            "Turn back if you're not prepared!",
            "The weather changes quickly up here.",
            "These mountains hide ancient secrets."
        ]
    }
    npcs.append(guide)
    
    return npcs

# 🎨 Expansion Ideas:
"""
Future additions you could make to this biome:
- Rock climbing mechanics with special gear
- Hidden mountain caves with crystal formations
- Snow-capped peaks with different weather
- Mountain goats that can be befriended
- Avalanche areas that are dangerous to cross
- Ancient dragon's lair in highest peak
- Mountain temple with wise monks
- Rope bridges across deep chasms
- Hot springs for healing and rest
- Mine shafts with precious gems and ores
- Mountain village of hardy miners
- Eagle's nest with rare treasures
- Stone giants that come alive at night
- Mountain spirits that test your courage
- Ice cave with frozen waterfall
- Observatory for studying stars
- Mountain rescue station
- Hidden valley paradise behind the peaks
- Ancient dwarven ruins
- Yeti encounters in the highest reaches
""" 