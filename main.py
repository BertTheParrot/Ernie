import pygame
import sys
import math
import random
import argparse
from typing import List, Dict, Tuple, Optional

# Import sprite manager
from sprite_manager import SpriteManager

# Import animals
from animals import FarmAnimals

# Import biome modules for collaborative development
from biomes import (
    create_farming_section, create_forest_section, create_lake_section,
    create_mountain_section, create_crossroads_section, create_ruins_section,
    create_southern_section, create_connecting_paths, create_random_features
)
from biomes.world_features import create_world_borders
from biomes.farm_biome import get_farm_npcs
from biomes.lake_biome import get_lake_npcs
from biomes.forest_biome import get_forest_npcs
from biomes.mountain_biome import get_mountain_npcs
from biomes.crossroads_biome import get_crossroads_npcs
from biomes.ruins_biome import get_ruins_npcs
from biomes.southern_biome import get_southern_npcs

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
    def __init__(self, x: int, y: int, sprite_manager: SpriteManager):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.speed = PLAYER_SPEED
        self.direction = 'down'
        self.is_moving = False
        self.sprite_manager = sprite_manager
        
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
        
        # Get the appropriate sprite for current direction
        player_sprite = self.sprite_manager.get_player_sprite(self.direction)
        
        # Draw the player sprite
        screen.blit(player_sprite, (screen_x, screen_y))

class NPC:
    def __init__(self, x: int, y: int, name: str, dialogue: List[str], sprite_manager: SpriteManager, npc_type: str = "default"):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.name = name
        self.dialogue = dialogue
        self.current_dialogue = 0
        self.is_talking = False
        self.sprite_manager = sprite_manager
        self.npc_type = npc_type
        
    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Get the appropriate sprite for this NPC type
        npc_sprite = self.sprite_manager.get_npc_sprite(self.npc_type)
        
        # Draw the NPC sprite
        screen.blit(npc_sprite, (screen_x, screen_y))
        
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
        
        # Create sprite manager
        self.sprite_manager = SpriteManager()
        self.sprite_manager.preload_common_sprites()
        
        # Create world map
        self.world_map = self.create_world()
        
        # Create player at specified spawn point
        spawn_x, spawn_y = WORLD_SECTIONS[spawn_section]['spawn']
        self.player = Player(spawn_x * TILE_SIZE + 16, spawn_y * TILE_SIZE + 16, self.sprite_manager)
        
        # Create NPCs
        self.npcs = self.create_npcs()
        
        # Create farm animals
        self.farm_animals = FarmAnimals(self.sprite_manager)
        if spawn_section == 'farm':  # Only add animals if spawning in farm
            self.farm_animals.create_farm_animals()
        
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
        """Create a large, diverse world map using modular biomes"""
        world = []
        
        # Initialize with grass
        for y in range(WORLD_HEIGHT):
            row = []
            for x in range(WORLD_WIDTH):
                row.append('.')  # Default to grass
            world.append(row)
        
        # Create border walls
        create_world_borders(world, WORLD_WIDTH, WORLD_HEIGHT)
        
        # Create different biomes using separate modules for collaboration
        create_farming_section(world, WORLD_WIDTH, WORLD_HEIGHT)      # 🏠 Brett's area
        create_lake_section(world, WORLD_WIDTH, WORLD_HEIGHT)         # 🏊 Girlfriend's area  
        create_forest_section(world, WORLD_WIDTH, WORLD_HEIGHT)       # 🌲 Available
        create_mountain_section(world, WORLD_WIDTH, WORLD_HEIGHT)     # 🏔️ Available
        create_crossroads_section(world, WORLD_WIDTH, WORLD_HEIGHT)   # 🍺 Shared hub
        create_ruins_section(world, WORLD_WIDTH, WORLD_HEIGHT)        # 🏺 Available
        create_southern_section(world, WORLD_WIDTH, WORLD_HEIGHT)     # 🔨 Available
        
        # Connect everything with roads and features
        create_connecting_paths(world, WORLD_WIDTH, WORLD_HEIGHT)     # Roads between sections
        create_random_features(world, WORLD_WIDTH, WORLD_HEIGHT)      # Scattered elements
        
        return world
    


    def create_npcs(self) -> List[NPC]:
        """Create NPCs from modular biome files"""
        npcs = []
        
        # Load NPCs from each biome module
        biome_npc_functions = [
            get_farm_npcs,
            get_lake_npcs,
            get_forest_npcs,
            get_mountain_npcs,
            get_crossroads_npcs,
            get_ruins_npcs,
            get_southern_npcs
        ]
        
        # Create NPCs from all biomes
        for get_biome_npcs in biome_npc_functions:
            biome_npcs = get_biome_npcs()
            for npc_data in biome_npcs:
                # Determine NPC type based on name
                npc_type = self._get_npc_type(npc_data['name'])
                npc = NPC(
                    npc_data['x'] * TILE_SIZE,
                    npc_data['y'] * TILE_SIZE,
                    npc_data['name'],
                    npc_data['dialogue'],
                    self.sprite_manager,
                    npc_type
                )
                npcs.append(npc)
        
        # Add traveling merchant on the road (shared NPC)
        traveling_merchant = NPC(50*TILE_SIZE, 40*TILE_SIZE, "Traveling Merchant", [
            "Well met, fellow traveler!",
            "The roads are safer with companions.",
            "I trade goods between the villages.",
            "Have you seen the beautiful lake to the northeast?"
        ], self.sprite_manager, "merchant")
        npcs.append(traveling_merchant)
        
        return npcs
        
    def _get_npc_type(self, npc_name: str) -> str:
        """Determine NPC sprite type based on name"""
        name_lower = npc_name.lower()
        
        if "farmer" in name_lower or "joe" in name_lower:
            return "farmer"
        elif "merchant" in name_lower or "trader" in name_lower:
            return "merchant"
        elif "wise" in name_lower or "old" in name_lower or "elder" in name_lower:
            return "wise_man"
        else:
            return "default"
    
    def get_current_biome(self) -> str:
        """Determine which biome the player is currently in based on their position"""
        player_tile_x = self.player.x // TILE_SIZE
        player_tile_y = self.player.y // TILE_SIZE
        
        # Define biome boundaries based on their general areas
        # Note: Check farm first since it's more specific than forest
        biome_areas = {
            'farm': {'x_range': (15, 35), 'y_range': (15, 30)},  # Farm area (northwest)
            'lake': {'x_range': (65, 85), 'y_range': (15, 35)},  # Lake area (northeast)
            'mountain': {'x_range': (80, 95), 'y_range': (10, 50)},  # Mountain area (east)
            'crossroads': {'x_range': (55, 70), 'y_range': (45, 55)},  # Crossroads (center)
            'ruins': {'x_range': (10, 25), 'y_range': (50, 65)},  # Ruins (southwest)
            'southern': {'x_range': (25, 35), 'y_range': (60, 70)},  # Southern village
            'forest': {'x_range': (5, 50), 'y_range': (5, 40)},  # Forest (large area, checked last)
        }
        
        # Check which biome the player is in
        for biome_name, area in biome_areas.items():
            if (area['x_range'][0] <= player_tile_x <= area['x_range'][1] and
                area['y_range'][0] <= player_tile_y <= area['y_range'][1]):
                return biome_name
        
        # Default to "wilderness" if not in any specific biome
        return "wilderness"
        
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
        """Check for NPC and animal interactions"""
        # Check NPCs
        for npc in self.npcs:
            distance = math.sqrt((self.player.x - npc.x)**2 + (self.player.y - npc.y)**2)
            if distance < TILE_SIZE * 1.5:  # Close enough to interact
                # Show interaction prompt
                prompt_text = f"Press SPACE to talk to {npc.name}"
                prompt_surface = self.small_font.render(prompt_text, True, WHITE)
                prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
                self.screen.blit(prompt_surface, prompt_rect)
                return
        
        # Check animals if no NPC is nearby
        animal_interaction = self.farm_animals.check_interactions(self.player.x, self.player.y, TILE_SIZE)
        if animal_interaction:
            prompt_text = f"Press SPACE to interact with {animal_interaction.split(':')[0]}"
            prompt_surface = self.small_font.render(prompt_text, True, WHITE)
            prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
            self.screen.blit(prompt_surface, prompt_rect)
                
    def handle_interaction(self) -> None:
        """Handle space key interaction"""
        # First check NPCs
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
                return
        
        # Then check animals if no NPC was interacted with
        animal_interaction = self.farm_animals.check_interactions(self.player.x, self.player.y, TILE_SIZE)
        if animal_interaction:
            if not self.show_dialogue:
                self.dialogue_text = animal_interaction
                self.show_dialogue = True
            else:
                self.show_dialogue = False
                
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
                
                # Get the appropriate sprite for this tile
                tile_sprite = self.sprite_manager.get_tile_sprite(tile)
                
                # Draw the tile sprite
                self.screen.blit(tile_sprite, (screen_x, screen_y))
                    
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
        
        # Current biome
        current_biome = self.get_current_biome()
        if current_biome in WORLD_SECTIONS:
            biome_name = WORLD_SECTIONS[current_biome]['name']
            biome_color = CYAN  # Use cyan color to make it stand out
        else:
            biome_name = "Wilderness"
            biome_color = LIGHT_GRAY
        
        biome_text = self.small_font.render(f"Biome: {biome_name}", True, biome_color)
        self.screen.blit(biome_text, (10, 90))
        
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
            
            # Update animals
            self.farm_animals.update(self.world_map)
            
            # Update camera
            self.update_camera()
            
            # Clear screen
            self.screen.fill(BLACK)
            
            # Draw world
            self.draw_world()
            
            # Draw animals
            self.farm_animals.draw(self.screen, self.camera_x, self.camera_y)
            
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