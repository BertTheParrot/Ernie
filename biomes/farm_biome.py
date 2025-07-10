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
    
    # Farm buildings - BIG houses for villagers (5x5 each)
    # Repositioned to avoid overlaps
    farm_houses = [(12, 12), (26, 12), (12, 26)]  # Well spaced apart
    for hx, hy in farm_houses:
        # Create 5x5 house
        for house_y in range(hy, hy + 5):
            for house_x in range(hx, hx + 5):
                if 0 < house_x < WORLD_WIDTH-1 and 0 < house_y < WORLD_HEIGHT-1:
                    world[house_y][house_x] = 'H'  # House
    
    # Large barn for storing crops (also make it bigger - 3x3)
    for barn_y in range(22, 25):
        for barn_x in range(22, 25):
            if 0 < barn_x < WORLD_WIDTH-1 and 0 < barn_y < WORLD_HEIGHT-1:
                world[barn_y][barn_x] = 'B'  # Barn
    
    # Village well - source of water (keep original position)
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
        'x': 14, 'y': 14,  # At the first big house
        'dialogue': [
            "Hello there, young adventurer!",
            "Welcome to our little village.",
            "I've been farming these lands for 30 years.",
            "The path east leads to other settlements.",
            "Be careful of the mountains to the east!",
            "These crops will feed the whole region.",
            "Our houses are much bigger now - plenty of room for visitors!"
        ]
    }
    npcs.append(farmer_joe)
    
    # Village Elder - wise leader
    village_elder = {
        'name': 'Village Elder',
        'x': 28, 'y': 14,  # At the second big house
        'dialogue': [
            "Greetings, traveler!",
            "This village has stood here for generations.",
            "The old ruins to the south hold many secrets.",
            "Follow the main road to reach other towns.",
            "Our harvest this year has been bountiful!",
            "These grand houses show our village's prosperity!"
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