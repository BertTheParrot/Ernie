import pygame
import sys
import math
import random
import argparse
from typing import List, Dict, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
PLAYER_SPEED = 4

# World size - much larger now!
WORLD_WIDTH = 100  # tiles
WORLD_HEIGHT = 80  # tiles

# World sections for collaborative development
WORLD_SECTIONS = {
    'farm': {
        'name': 'Farming Village',
        'spawn': (20, 18),
        'description': 'A peaceful farming community in the northwest'
    },
    'crossroads': {
        'name': 'Crossroads Tavern',
        'spawn': (60, 50),
        'description': 'The central hub where all roads meet'
    },
    'mountains': {
        'name': 'Mountain Pass',
        'spawn': (82, 30),
        'description': 'Treacherous peaks in the eastern highlands'
    },
    'lake': {
        'name': 'Crystal Lake',
        'spawn': (75, 25),
        'description': 'A serene lake perfect for fishing'
    },
    'forest': {
        'name': 'Whispering Woods',
        'spawn': (15, 15),
        'description': 'Ancient forests filled with mystery'
    },
    'ruins': {
        'name': 'Ancient Ruins',
        'spawn': (15, 55),
        'description': 'Mysterious stone structures from a lost civilization'
    },
    'southern': {
        'name': 'Southern Village',
        'spawn': (30, 65),
        'description': 'A crafting village known for its blacksmith'
    },
    'center': {
        'name': 'World Center',
        'spawn': (50, 40),
        'description': 'The geographical center of the world'
    }
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
BLUE = (65, 105, 225)
DARK_BLUE = (0, 0, 139)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
SANDY = (238, 203, 173)
PURPLE = (128, 0, 128)

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.speed = PLAYER_SPEED
        self.direction = 'down'
        self.is_moving = False
        
    def move(self, dx: int, dy: int, world_map: List[List[str]]) -> None:
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check bounds
        if new_x < TILE_SIZE or new_x >= (WORLD_WIDTH - 1) * TILE_SIZE - self.width:
            return
        if new_y < TILE_SIZE or new_y >= (WORLD_HEIGHT - 1) * TILE_SIZE - self.height:
            return
            
        # Check collision with solid tiles
        tile_x = new_x // TILE_SIZE
        tile_y = new_y // TILE_SIZE
        
        # Check multiple points for better collision detection
        collision_points = [
            (new_x // TILE_SIZE, new_y // TILE_SIZE),                           # Top-left
            ((new_x + self.width - 1) // TILE_SIZE, new_y // TILE_SIZE),        # Top-right
            (new_x // TILE_SIZE, (new_y + self.height - 1) // TILE_SIZE),       # Bottom-left
            ((new_x + self.width - 1) // TILE_SIZE, (new_y + self.height - 1) // TILE_SIZE)  # Bottom-right
        ]
        
        # Solid tiles that can't be walked through
        solid_tiles = {'#', 'W', 'M', 'H', 'F', 'S'}
        
        for check_x, check_y in collision_points:
            if (0 <= check_y < WORLD_HEIGHT and 0 <= check_x < WORLD_WIDTH and 
                world_map[check_y][check_x] in solid_tiles):
                self.is_moving = False
                return
                
        self.x = new_x
        self.y = new_y
        self.is_moving = True
            
    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Draw Ernie (blue rectangle)
        pygame.draw.rect(screen, BLUE, (screen_x, screen_y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (screen_x, screen_y, self.width, self.height), 2)
        
        # Draw direction indicator
        if self.direction == 'up':
            pygame.draw.circle(screen, YELLOW, (screen_x + self.width//2, screen_y + 8), 4)
        elif self.direction == 'down':
            pygame.draw.circle(screen, YELLOW, (screen_x + self.width//2, screen_y + self.height - 8), 4)
        elif self.direction == 'left':
            pygame.draw.circle(screen, YELLOW, (screen_x + 8, screen_y + self.height//2), 4)
        elif self.direction == 'right':
            pygame.draw.circle(screen, YELLOW, (screen_x + self.width - 8, screen_y + self.height//2), 4)

class NPC:
    def __init__(self, x: int, y: int, name: str, dialogue: List[str]):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.name = name
        self.dialogue = dialogue
        self.current_dialogue = 0
        self.is_talking = False
        
    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Draw NPC (green rectangle)
        pygame.draw.rect(screen, GREEN, (screen_x, screen_y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (screen_x, screen_y, self.width, self.height), 2)
        
        # Draw name above NPC
        font = pygame.font.Font(None, 20)
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(screen_x + self.width//2, screen_y - 10))
        screen.blit(name_text, name_rect)
        
    def interact(self) -> str:
        if not self.is_talking:
            self.is_talking = True
            self.current_dialogue = 0
            
        if self.current_dialogue < len(self.dialogue):
            return self.dialogue[self.current_dialogue]
        else:
            self.is_talking = False
            self.current_dialogue = 0
            return ""
            
    def next_dialogue(self) -> str:
        self.current_dialogue += 1
        if self.current_dialogue >= len(self.dialogue):
            self.is_talking = False
            self.current_dialogue = 0
            return ""
        return self.dialogue[self.current_dialogue]

class Game:
    def __init__(self, spawn_section: str = 'farm'):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ernie's Adventure")
        self.clock = pygame.time.Clock()
        
        # Store spawn section
        self.spawn_section = spawn_section
        
        # Create world map
        self.world_map = self.create_world()
        
        # Create player at specified spawn point
        spawn_x, spawn_y = WORLD_SECTIONS[spawn_section]['spawn']
        self.player = Player(spawn_x * TILE_SIZE + 16, spawn_y * TILE_SIZE + 16)
        
        # Create NPCs
        self.npcs = self.create_npcs()
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # UI
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.dialogue_box = None
        self.dialogue_text = ""
        self.show_dialogue = False
        
        # Input
        self.keys = {}
        
    def create_world(self) -> List[List[str]]:
        """Create a large, diverse world map with different biomes"""
        world = []
        
        # Initialize with grass
        for y in range(WORLD_HEIGHT):
            row = []
            for x in range(WORLD_WIDTH):
                row.append('.')  # Default to grass
            world.append(row)
        
        # Create border walls
        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                if x == 0 or x == WORLD_WIDTH-1 or y == 0 or y == WORLD_HEIGHT-1:
                    world[y][x] = '#'
        
        # Create different biomes and features - now organized by sections
        self._create_farming_section(world)      # Northwest - farm area
        self._create_forest_section(world)       # North-central - forest
        self._create_mountain_section(world)     # East - mountains
        self._create_lake_section(world)         # Northeast - lake
        self._create_crossroads_section(world)   # Center - main hub
        self._create_ruins_section(world)        # Southwest - ancient ruins
        self._create_southern_section(world)     # South - crafting village
        self._create_connecting_paths(world)     # Roads between sections
        self._create_random_features(world)      # Scattered elements
        
        return world
    
    def _create_farming_section(self, world: List[List[str]]) -> None:
        """Create the farming village section (Northwest)"""
        # Farm fields
        for y in range(15, 25):
            for x in range(15, 35):
                if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                    if random.random() < 0.3:
                        world[y][x] = 'C'  # Crops
        
        # Village clearing
        for y in range(17, 24):
            for x in range(17, 24):
                if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                    world[y][x] = '.'  # Clear grass
        
        # Farm buildings
        farm_buildings = [(19, 19), (21, 19), (19, 22)]
        for hx, hy in farm_buildings:
            if 0 < hx < WORLD_WIDTH-1 and 0 < hy < WORLD_HEIGHT-1:
                world[hy][hx] = 'H'  # House
        
        # Barn
        world[21][22] = 'B'  # Barn
        
        # Well
        world[20][20] = 'O'  # Well
    
    def _create_forest_section(self, world: List[List[str]]) -> None:
        """Create the forest section (North-central)"""
        # Large forest area
        for y in range(5, 30):
            for x in range(5, 45):
                if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                    if random.random() < 0.7:  # 70% chance for trees
                        world[y][x] = 'T'
                    elif random.random() < 0.2:
                        world[y][x] = 'F'  # Dense forest
        
        # Forest clearing for hermit
        for y in range(13, 18):
            for x in range(13, 18):
                if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                    world[y][x] = '.'
        
        # Hermit's hut
        world[15][15] = 'H'
    
    def _create_mountain_section(self, world: List[List[str]]) -> None:
        """Create the mountain section (East)"""
        # Mountain range
        for y in range(10, 60):
            for x in range(80, 95):
                if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                    if random.random() < 0.8:
                        world[y][x] = 'M'  # Mountain
                    elif random.random() < 0.3:
                        world[y][x] = '#'  # Rock wall
        
        # Mountain pass
        for y in range(28, 35):
            for x in range(82, 88):
                if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                    world[y][x] = 'P'  # Path through mountains
        
        # Cave entrance
        world[30][85] = 'E'  # Cave entrance
    
    def _create_lake_section(self, world: List[List[str]]) -> None:
        """Create the lake section (Northeast)"""
        # Main lake
        lake_center_x, lake_center_y = 75, 25
        for y in range(lake_center_y-8, lake_center_y+8):
            for x in range(lake_center_x-10, lake_center_x+10):
                distance = math.sqrt((x - lake_center_x)**2 + (y - lake_center_y)**2)
                if distance < 8 and 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                    world[y][x] = 'W'
        
        # Fishing dock
        world[28][75] = 'D'  # Dock
        world[29][75] = 'D'
        
        # Fisherman's shack
        world[30][73] = 'H'
    
    def _create_crossroads_section(self, world: List[List[str]]) -> None:
        """Create the crossroads section (Center)"""
        # Tavern and buildings
        tavern_area = [(60, 49), (61, 49), (60, 50), (61, 50)]  # 2x2 tavern
        for tx, ty in tavern_area:
            if 0 < tx < WORLD_WIDTH-1 and 0 < ty < WORLD_HEIGHT-1:
                world[ty][tx] = 'T'  # Tavern (using T for now)
        
        # Inn
        world[58][51] = 'H'
        
        # Stable
        world[63][52] = 'S'
    
    def _create_ruins_section(self, world: List[List[str]]) -> None:
        """Create the ancient ruins section (Southwest)"""
        # Ruins pattern
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
    
    def _create_southern_section(self, world: List[List[str]]) -> None:
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
        world[65][30] = 'F'  # Forge
    
    def _create_connecting_paths(self, world: List[List[str]]) -> None:
        """Create paths connecting all sections"""
        # Main east-west road
        for x in range(5, WORLD_WIDTH-5):
            for offset in [-1, 0, 1]:  # 3-tile wide road
                road_y = 40 + offset
                if 0 < road_y < WORLD_HEIGHT-1 and world[road_y][x] not in ['W', 'M']:
                    world[road_y][x] = 'P'
        
        # North-south connecting roads
        # Farm to crossroads
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
    
    def _create_random_features(self, world: List[List[str]]) -> None:
        """Add random features throughout the world"""
        # River system
        river_x = 45
        for y in range(1, WORLD_HEIGHT-1):
            river_x += random.choice([-1, 0, 0, 1])
            river_x = max(5, min(WORLD_WIDTH-5, river_x))
            
            for x in range(river_x-1, river_x+2):
                if 0 < x < WORLD_WIDTH-1 and world[y][x] not in ['H', 'P']:
                    world[y][x] = 'W'
        
        # Scattered trees and rocks
        for _ in range(150):
            x = random.randint(5, WORLD_WIDTH-5)
            y = random.randint(5, WORLD_HEIGHT-5)
            
            if world[y][x] == '.':
                feature = random.choice(['T', 'R', '.', '.', '.'])
                if feature != '.':
                    world[y][x] = feature

    def create_npcs(self) -> List[NPC]:
        """Create NPCs scattered across the larger world"""
        npcs = []
        
        # Village NPCs
        farmer_joe = NPC(20*TILE_SIZE, 20*TILE_SIZE, "Farmer Joe", [
            "Hello there, young adventurer!",
            "Welcome to our little village.",
            "I've been farming these lands for 30 years.",
            "The path east leads to other settlements.",
            "Be careful of the mountains to the east!"
        ])
        npcs.append(farmer_joe)
        
        village_elder = NPC(21*TILE_SIZE, 22*TILE_SIZE, "Village Elder", [
            "Greetings, traveler!",
            "This village has stood here for generations.",
            "The old ruins to the south hold many secrets.",
            "Follow the main road to reach other towns."
        ])
        npcs.append(village_elder)
        
        # Forest NPCs
        forest_hermit = NPC(15*TILE_SIZE, 15*TILE_SIZE, "Forest Hermit", [
            "Oh! A visitor in my peaceful forest!",
            "I've lived among these trees for decades.",
            "The forest spirits whisper of ancient magic.",
            "Beware the deeper parts of the woods..."
        ])
        npcs.append(forest_hermit)
        
        # Traveler on the road
        traveling_merchant = NPC(50*TILE_SIZE, 40*TILE_SIZE, "Traveling Merchant", [
            "Well met, fellow traveler!",
            "The roads are safer with companions.",
            "I trade goods between the villages.",
            "Have you seen the beautiful lake to the northeast?"
        ])
        npcs.append(traveling_merchant)
        
        # Lake area NPC
        fisherman = NPC(75*TILE_SIZE, 28*TILE_SIZE, "Old Fisherman", [
            "Perfect fishing weather today!",
            "These waters are teeming with fish.",
            "I've caught strange things in the deep parts...",
            "The lake connects to underground rivers."
        ])
        npcs.append(fisherman)
        
        # Mountain area
        mountain_guide = NPC(82*TILE_SIZE, 30*TILE_SIZE, "Mountain Guide", [
            "The peaks are treacherous, friend!",
            "Many caves lead deep into the mountains.",
            "I once found gems in the eastern peaks.",
            "Turn back if you're not prepared!"
        ])
        npcs.append(mountain_guide)
        
        # Second village
        tavern_keeper = NPC(60*TILE_SIZE, 50*TILE_SIZE, "Tavern Keeper", [
            "Welcome to the Crossroads Tavern!",
            "Travelers from all lands stop here.",
            "Have you heard the legends of the ruins?",
            "Stay the night - the roads are dark!"
        ])
        npcs.append(tavern_keeper)
        
        # Ruins explorer
        archaeologist = NPC(15*TILE_SIZE, 53*TILE_SIZE, "Archaeologist", [
            "These ruins predate any known civilization!",
            "I've been studying these stones for years.",
            "The symbols suggest a lost magical culture.",
            "Be careful not to disturb anything!"
        ])
        npcs.append(archaeologist)
        
        # Third village
        blacksmith = NPC(30*TILE_SIZE, 65*TILE_SIZE, "Village Blacksmith", [
            "The forge burns hot today!",
            "I craft tools for all the local farmers.",
            "The ore from the eastern mountains is finest.",
            "Need anything repaired, traveler?"
        ])
        npcs.append(blacksmith)
        
        wise_woman = NPC(32*TILE_SIZE, 63*TILE_SIZE, "Wise Woman", [
            "I sense great potential in you, young one.",
            "The world is vast and full of mysteries.",
            "Your journey has only just begun.",
            "Trust in yourself and you'll find your way."
        ])
        npcs.append(wise_woman)
        
        return npcs
        
    def handle_input(self) -> None:
        """Handle player input"""
        keys = pygame.key.get_pressed()
        
        # Movement
        dx = 0
        dy = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.player.speed
            self.player.direction = 'left'
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.player.speed
            self.player.direction = 'right'
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.player.speed
            self.player.direction = 'up'
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.player.speed
            self.player.direction = 'down'
            
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.world_map)
        else:
            self.player.is_moving = False
            
    def check_interactions(self) -> None:
        """Check for NPC interactions"""
        for npc in self.npcs:
            distance = math.sqrt((self.player.x - npc.x)**2 + (self.player.y - npc.y)**2)
            if distance < TILE_SIZE * 1.5:  # Close enough to interact
                # Show interaction prompt
                prompt_text = f"Press SPACE to talk to {npc.name}"
                prompt_surface = self.small_font.render(prompt_text, True, WHITE)
                prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
                self.screen.blit(prompt_surface, prompt_rect)
                
    def handle_interaction(self) -> None:
        """Handle space key interaction"""
        for npc in self.npcs:
            distance = math.sqrt((self.player.x - npc.x)**2 + (self.player.y - npc.y)**2)
            if distance < TILE_SIZE * 1.5:
                if not self.show_dialogue:
                    self.dialogue_text = npc.interact()
                    self.show_dialogue = True
                else:
                    self.dialogue_text = npc.next_dialogue()
                    if not self.dialogue_text:
                        self.show_dialogue = False
                break
                
    def update_camera(self) -> None:
        """Update camera to follow player"""
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Keep camera in bounds of the larger world
        self.camera_x = max(0, min(self.camera_x, WORLD_WIDTH * TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, WORLD_HEIGHT * TILE_SIZE - SCREEN_HEIGHT))
        
    def draw_world(self) -> None:
        """Draw the world map with all new tile types"""
        start_x = max(0, self.camera_x // TILE_SIZE - 1)
        end_x = min(WORLD_WIDTH, (self.camera_x + SCREEN_WIDTH) // TILE_SIZE + 2)
        start_y = max(0, self.camera_y // TILE_SIZE - 1)
        end_y = min(WORLD_HEIGHT, (self.camera_y + SCREEN_HEIGHT) // TILE_SIZE + 2)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.world_map[y][x]
                screen_x = x * TILE_SIZE - self.camera_x
                screen_y = y * TILE_SIZE - self.camera_y
                
                # Draw different tile types
                if tile == '#':  # Wall
                    pygame.draw.rect(self.screen, GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'T':  # Tree
                    pygame.draw.rect(self.screen, DARK_GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, BROWN, (screen_x + 8, screen_y + 8, 16, 16))
                elif tile == 'F':  # Dense forest
                    pygame.draw.rect(self.screen, DARK_GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'W':  # Water
                    pygame.draw.rect(self.screen, BLUE, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'M':  # Mountain
                    pygame.draw.rect(self.screen, GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.polygon(self.screen, LIGHT_GRAY, [
                        (screen_x + TILE_SIZE//2, screen_y + 4),
                        (screen_x + 4, screen_y + TILE_SIZE - 4),
                        (screen_x + TILE_SIZE - 4, screen_y + TILE_SIZE - 4)
                    ])
                elif tile == 'P':  # Path
                    pygame.draw.rect(self.screen, SANDY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'H':  # House
                    pygame.draw.rect(self.screen, BROWN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.polygon(self.screen, RED, [
                        (screen_x, screen_y),
                        (screen_x + TILE_SIZE//2, screen_y - 8),
                        (screen_x + TILE_SIZE, screen_y)
                    ])
                elif tile == 'R':  # Rock
                    pygame.draw.rect(self.screen, LIGHT_GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'S':  # Stone ruins
                    pygame.draw.rect(self.screen, DARK_GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'C':  # Crops
                    pygame.draw.rect(self.screen, YELLOW, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'B':  # Barn
                    pygame.draw.rect(self.screen, DARK_BROWN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'O':  # Well
                    pygame.draw.rect(self.screen, LIGHT_GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.circle(self.screen, DARK_BLUE, (screen_x + TILE_SIZE//2, screen_y + TILE_SIZE//2), 8)
                elif tile == 'D':  # Dock
                    pygame.draw.rect(self.screen, DARK_BROWN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                elif tile == 'E':  # Cave entrance
                    pygame.draw.rect(self.screen, BLACK, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.circle(self.screen, GRAY, (screen_x + TILE_SIZE//2, screen_y + TILE_SIZE//2), 12)
                elif tile == 'A':  # Altar
                    pygame.draw.rect(self.screen, PURPLE, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                else:  # Grass
                    pygame.draw.rect(self.screen, GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    
                # Draw subtle grid lines for grass only
                if tile == '.':
                    pygame.draw.rect(self.screen, DARK_GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
                    
    def draw_ui(self) -> None:
        """Draw UI elements with spawn section info"""
        # Title with current section
        section_info = WORLD_SECTIONS[self.spawn_section]
        title_text = f"Ernie's Adventure - {section_info['name']}"
        title_surface = self.font.render(title_text, True, WHITE)
        self.screen.blit(title_surface, (10, 10))
        
        # Controls
        controls_text = self.small_font.render("WASD: Move | SPACE: Interact", True, WHITE)
        self.screen.blit(controls_text, (10, 40))
        
        # World coordinates
        world_x = self.player.x // TILE_SIZE
        world_y = self.player.y // TILE_SIZE
        pos_text = self.small_font.render(f"Location: ({world_x}, {world_y})", True, WHITE)
        self.screen.blit(pos_text, (10, 70))
        
        # Draw minimap
        self.draw_minimap()
        
        # Dialogue box
        if self.show_dialogue and self.dialogue_text:
            # Draw dialogue background
            dialogue_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
            pygame.draw.rect(self.screen, BLACK, dialogue_rect)
            pygame.draw.rect(self.screen, WHITE, dialogue_rect, 3)
            
            # Draw dialogue text (handle text wrapping)
            words = self.dialogue_text.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                if self.small_font.size(test_line)[0] < SCREEN_WIDTH - 120:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            # Draw each line
            for i, line in enumerate(lines[:3]):  # Max 3 lines
                line_surface = self.small_font.render(line, True, WHITE)
                line_y = SCREEN_HEIGHT - 130 + i * 25
                self.screen.blit(line_surface, (70, line_y))
    
    def draw_minimap(self) -> None:
        """Draw a small minimap in the corner"""
        minimap_size = 120
        minimap_scale = 3  # 3x3 tiles per pixel
        minimap_x = SCREEN_WIDTH - minimap_size - 10
        minimap_y = 10
        
        # Draw minimap background
        pygame.draw.rect(self.screen, BLACK, (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(self.screen, WHITE, (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Calculate what area of the world to show
        player_world_x = self.player.x // TILE_SIZE
        player_world_y = self.player.y // TILE_SIZE
        
        # Center minimap on player
        map_half = minimap_size // 2 // minimap_scale
        start_x = max(0, min(WORLD_WIDTH - minimap_size // minimap_scale, player_world_x - map_half))
        start_y = max(0, min(WORLD_HEIGHT - minimap_size // minimap_scale, player_world_y - map_half))
        
        # Draw minimap tiles
        for y in range(minimap_size // minimap_scale):
            for x in range(minimap_size // minimap_scale):
                world_x = start_x + x
                world_y = start_y + y
                
                if 0 <= world_x < WORLD_WIDTH and 0 <= world_y < WORLD_HEIGHT:
                    tile = self.world_map[world_y][world_x]
                    
                    # Choose color based on tile type
                    color = GREEN  # Default grass
                    if tile == '#':
                        color = GRAY
                    elif tile in ['T', 'F']:
                        color = DARK_GREEN
                    elif tile == 'W':
                        color = BLUE
                    elif tile == 'M':
                        color = LIGHT_GRAY
                    elif tile == 'P':
                        color = SANDY
                    elif tile == 'H':
                        color = BROWN
                    elif tile in ['R', 'S']:
                        color = DARK_GRAY
                    
                    pygame.draw.rect(self.screen, color, 
                                   (minimap_x + x * minimap_scale, 
                                    minimap_y + y * minimap_scale, 
                                    minimap_scale, minimap_scale))
        
        # Draw player position on minimap
        player_mini_x = minimap_x + (player_world_x - start_x) * minimap_scale
        player_mini_y = minimap_y + (player_world_y - start_y) * minimap_scale
        pygame.draw.rect(self.screen, RED, (player_mini_x, player_mini_y, minimap_scale, minimap_scale))
        
        # Draw NPCs on minimap
        for npc in self.npcs:
            npc_world_x = npc.x // TILE_SIZE
            npc_world_y = npc.y // TILE_SIZE
            
            if (start_x <= npc_world_x < start_x + minimap_size // minimap_scale and
                start_y <= npc_world_y < start_y + minimap_size // minimap_scale):
                npc_mini_x = minimap_x + (npc_world_x - start_x) * minimap_scale
                npc_mini_y = minimap_y + (npc_world_y - start_y) * minimap_scale
                pygame.draw.circle(self.screen, YELLOW, 
                                 (npc_mini_x + minimap_scale//2, npc_mini_y + minimap_scale//2), 2)
            
    def run(self) -> None:
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.handle_interaction()
                    elif event.key == pygame.K_ESCAPE:
                        self.show_dialogue = False
                        
            # Handle input
            self.handle_input()
            
            # Update camera
            self.update_camera()
            
            # Clear screen
            self.screen.fill(BLACK)
            
            # Draw world
            self.draw_world()
            
            # Draw NPCs
            for npc in self.npcs:
                npc.draw(self.screen, self.camera_x, self.camera_y)
                
            # Check for interactions
            self.check_interactions()
            
            # Draw player
            self.player.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Ernie's Adventure - Collaborative World Explorer")
    parser.add_argument('--spawn', 
                       choices=list(WORLD_SECTIONS.keys()),
                       default='farm',
                       help='Choose where to spawn in the world')
    parser.add_argument('--list-sections', 
                       action='store_true',
                       help='List all available spawn sections')
    
    return parser.parse_args()

def list_sections():
    """List all available world sections"""
    print("\n🌍 Available World Sections:")
    print("=" * 50)
    
    for section_id, section_data in WORLD_SECTIONS.items():
        print(f"  {section_id:<12} - {section_data['name']}")
        print(f"               {section_data['description']}")
        print()
    
    print("Usage: python3 main.py --spawn <section_name>")
    print("Example: python3 main.py --spawn forest")

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.list_sections:
        list_sections()
        sys.exit(0)
    
    print(f"🎮 Starting Ernie's Adventure...")
    print(f"📍 Spawning in: {WORLD_SECTIONS[args.spawn]['name']}")
    print(f"📝 {WORLD_SECTIONS[args.spawn]['description']}")
    print()
    
    game = Game(spawn_section=args.spawn)
    game.run() 