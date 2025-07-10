"""
🏊 Lake Biome - Ernie's Adventure  
Developer: Your Girlfriend
Location: Northeast (around coordinates 75, 25)

This biome contains:
- Beautiful crystal lake with clear blue water
- Wooden fishing docks
- Fisherman's shack
- Peaceful lake NPCs
- Serene water features
"""

import random
import math
from typing import List

def create_lake_section(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the lake section (Northeast)"""
    
    # Main lake - large circular water feature
    lake_center_x, lake_center_y = 75, 25
    for y in range(lake_center_y-8, lake_center_y+8):
        for x in range(lake_center_x-10, lake_center_x+10):
            distance = math.sqrt((x - lake_center_x)**2 + (y - lake_center_y)**2)
            if distance < 8 and 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = 'W'  # Water
    
    # Fishing dock - wooden platform extending into water
    world[28][75] = 'D'  # Dock
    world[29][75] = 'D'  # Dock
    
    # Fisherman's shack - cozy home by the water
    world[30][73] = 'H'  # House

def get_lake_npcs():
    """Return NPCs specific to the lake area"""
    npcs = []
    
    # Old Fisherman - peaceful lake dweller
    fisherman = {
        'name': 'Old Fisherman',
        'x': 75, 'y': 28,  # On the dock
        'dialogue': [
            "Perfect fishing weather today!",
            "These waters are teeming with fish.",
            "I've caught strange things in the deep parts...",
            "The lake connects to underground rivers.",
            "Sometimes I see lights under the water at night.",
            "This lake has the clearest water in all the land."
        ]
    }
    npcs.append(fisherman)
    
    return npcs

# 🎨 Expansion Ideas for Your Girlfriend:
"""
Future additions you could make to this biome:
- Boat that you can ride across the lake (tile 'B')
- Lily pads floating on the water (tile 'L')
- Small islands in the middle of the lake
- Underwater caves entrance (tile 'U')
- Fishing mechanics - catch different fish
- Lake monster that occasionally surfaces
- Reed beds around the shore (tile 'R')
- Swimming area with clear shallow water
- Waterfall flowing into the lake from mountains
- Fish jumping out of water (animated sprites)
- Lake shrine on a small island
- Canoe rental dock
- Lake spirits or water fairies
- Hidden treasure chest underwater
- Bridge crossing the narrowest part
- Duck families swimming around
- Crystal clear viewing areas
- Moonlight reflections on water at night
- Bioluminescent fish that glow
- Secret cave behind waterfall
""" 