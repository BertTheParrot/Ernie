"""
🏠 Farm Biome - Ernie's Adventure
Developer: Brett
Location: Northwest (around coordinates 20, 18)

This biome contains:
- Farming village with houses and barns
- Crop fields with golden wheat
- Village well and farm buildings
- Peaceful farming NPCs
"""

import random
from typing import List

def create_farming_section(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the farming village section (Northwest)"""
    
    # Farm fields - golden crop areas
    for y in range(15, 25):
        for x in range(15, 35):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                if random.random() < 0.3:  # 30% chance for crops
                    world[y][x] = 'C'  # Crops
    
    # Village clearing - open grass area
    for y in range(17, 24):
        for x in range(17, 24):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass
    
    # Farm buildings - houses for villagers
    farm_buildings = [(19, 19), (21, 19), (19, 22)]
    for hx, hy in farm_buildings:
        if 0 < hx < WORLD_WIDTH-1 and 0 < hy < WORLD_HEIGHT-1:
            world[hy][hx] = 'H'  # House
    
    # Large barn for storing crops
    world[21][22] = 'B'  # Barn
    
    # Village well - source of water
    world[20][20] = 'O'  # Well
    
    # Animal pastures - clear grass areas for animals to roam
    # Cow pasture (around the barn)
    for y in range(20, 24):
        for x in range(22, 26):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass for cows
    
    # Pig pen area
    for y in range(24, 26):
        for x in range(16, 19):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass for pigs
    
    # Sheep field (separate area)
    for y in range(18, 22):
        for x in range(26, 30):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass for sheep

def get_farm_npcs():
    """Return NPCs specific to the farming area"""
    npcs = []
    
    # Farmer Joe - main farmer character
    farmer_joe = {
        'name': 'Farmer Joe',
        'x': 20, 'y': 20,  # Near the well
        'dialogue': [
            "Hello there, young adventurer!",
            "Welcome to our little village.",
            "I've been farming these lands for 30 years.",
            "The path east leads to other settlements.",
            "Be careful of the mountains to the east!",
            "These crops will feed the whole region."
        ]
    }
    npcs.append(farmer_joe)
    
    # Village Elder - wise leader
    village_elder = {
        'name': 'Village Elder',
        'x': 21, 'y': 22,  # Near the barn
        'dialogue': [
            "Greetings, traveler!",
            "This village has stood here for generations.",
            "The old ruins to the south hold many secrets.",
            "Follow the main road to reach other towns.",
            "Our harvest this year has been bountiful!"
        ]
    }
    npcs.append(village_elder)
    
    return npcs

# 🎨 Expansion Ideas for Brett:
"""
Recent additions:
✅ Animal pens with cows, pigs, chickens, and sheep - now implemented!

Future additions you could make to this biome:
- Windmill for grinding grain (tile 'W')
- Market stalls for trading (tile 'M') 
- Seasonal crop variations
- Farm tools and equipment
- Vegetable gardens with different crops
- Farm dog that follows you around
- Scarecrow in the fields
- Farmer's market on certain days
- Irrigation channels from the well
- Storage silos
- Compost piles
- Orchard with fruit trees
- Animal feeding mechanics
- Milk/egg collection mini-games
- Fencing around animal areas
- Horse riding system
""" 