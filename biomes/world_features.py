"""
🌍 World Features - Ernie's Adventure
Shared features that connect all biomes

This file contains:
- Road network connecting all areas
- River system flowing through the world
- Random scattered features
- Border walls and boundaries
"""

import random
from typing import List

def create_connecting_paths(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create paths connecting all sections"""
    
    # Main east-west road - the great highway
    for x in range(5, WORLD_WIDTH-5):
        for offset in [-1, 0, 1]:  # 3-tile wide road
            road_y = 40 + offset
            if 0 < road_y < WORLD_HEIGHT-1 and world[road_y][x] not in ['W', 'M']:
                world[road_y][x] = 'P'  # Path
    
    # North-south connecting roads
    # Farm to crossroads connection
    for y in range(25, 40):
        if world[y][25] not in ['W', 'M']:
            world[y][25] = 'P'
    
    # Crossroads to southern village
    for y in range(42, 62):
        if world[y][30] not in ['W', 'M']:
            world[y][30] = 'P'
    
    # Path to ruins
    for x in range(15, 25):
        if world[50][x] not in ['W', 'M']:
            world[50][x] = 'P'

def create_random_features(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Add random features throughout the world"""
    
    # River system - meandering water
    river_x = 45
    for y in range(1, WORLD_HEIGHT-1):
        river_x += random.choice([-1, 0, 0, 1])
        river_x = max(5, min(WORLD_WIDTH-5, river_x))
        
        for x in range(river_x-1, river_x+2):
            if 0 < x < WORLD_WIDTH-1 and world[y][x] not in ['H', 'P']:
                world[y][x] = 'W'  # Water
    
    # Scattered trees and rocks
    for _ in range(150):
        x = random.randint(5, WORLD_WIDTH-5)
        y = random.randint(5, WORLD_HEIGHT-5)
        
        if world[y][x] == '.':
            feature = random.choice(['T', 'R', '.', '.', '.'])
            if feature != '.':
                world[y][x] = feature

def create_world_borders(world: List[List[str]], WORLD_WIDTH: int, WORLD_HEIGHT: int) -> None:
    """Create the border walls around the world"""
    
    # Create border walls
    for y in range(WORLD_HEIGHT):
        for x in range(WORLD_WIDTH):
            if x == 0 or x == WORLD_WIDTH-1 or y == 0 or y == WORLD_HEIGHT-1:
                world[y][x] = '#'  # Wall border

# 🎨 Expansion Ideas for Shared Features:
"""
Future additions for world connectivity:
- Teleportation circles connecting distant areas
- Ferry system across the main river
- Merchant caravan routes with moving traders
- Weather systems affecting all biomes
- Day/night cycle with different events
- Seasonal changes across the world
- Flying mounts to travel quickly between areas
- Underground tunnel network
- Magical portals between special locations
- World events that affect multiple biomes
- Traveling NPCs that move between sections
- Trade routes with economic simulation
- Migratory creatures that move seasonally
- Message system between settlements
- World map that fills in as you explore
""" 