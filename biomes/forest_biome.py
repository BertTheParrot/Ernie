"""
🌲 Forest Biome - Ernie's Adventure
Developer: Available for Assignment
Location: North-central (around coordinates 15, 15)

This biome contains:
- Dense mysterious woods
- Forest hermit's hut
- Ancient trees and clearings
- Wildlife and forest spirits
"""

import random
from typing import List

def create_forest_section(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the forest section (North-central)"""
    
    # Large forest area - dense tree coverage
    for y in range(5, 30):
        for x in range(5, 45):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                if random.random() < 0.7:  # 70% chance for trees
                    world[y][x] = 'T'  # Tree
                elif random.random() < 0.2:  # Some areas very dense
                    world[y][x] = 'F'  # Dense forest
    
    # Forest clearing for hermit - peaceful open area
    for y in range(13, 18):
        for x in range(13, 18):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass
    
    # Hermit's hut - simple dwelling in the woods
    world[15][15] = 'H'  # House

def get_forest_npcs():
    """Return NPCs specific to the forest area"""
    npcs = []
    
    # Forest Hermit - wise woods dweller
    hermit = {
        'name': 'Forest Hermit',
        'x': 15, 'y': 15,  # In the clearing
        'dialogue': [
            "Oh! A visitor in my peaceful forest!",
            "I've lived among these trees for decades.",
            "The forest spirits whisper of ancient magic.",
            "Beware the deeper parts of the woods...",
            "Nature has many secrets to share.",
            "The trees remember stories from long ago."
        ]
    }
    npcs.append(hermit)
    
    return npcs

# 🎨 Expansion Ideas:
"""
Future additions you could make to this biome:
- Hidden forest paths that change location
- Tree houses connected by rope bridges
- Mushroom circles with magical properties
- Ancient forest shrine
- Talking animals (wise owl, helpful rabbit)
- Berry bushes you can harvest
- Forest maze with moving walls
- Fairy rings that teleport you
- Enchanted clearing with dancing lights
- Treant (walking tree) NPC
- Hidden treasure buried under old tree
- Forest spirits that follow you
- Seasonal changes (autumn leaves, spring flowers)
- Wolf pack that you can befriend
- Druid's grove with healing herbs
- Crystal cave entrance hidden by vines
- Ancient runestones with forest lore
- Hanging bridges between giant trees
- Forest guardian boss creature
""" 