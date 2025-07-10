import pygame
import os
from typing import Dict, Optional, Tuple, List
from enum import Enum

class SpriteType(Enum):
    """Enum for different sprite types"""
    PLAYER = "player"
    NPC = "npcs" 
    TILE = "tiles"
    ANIMAL = "animals"

class SpriteManager:
    """Manages loading, caching, and accessing sprite images"""
    
    def __init__(self, sprites_dir: str = "sprites"):
        self.sprites_dir = sprites_dir
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.tile_size = 32  # Default tile size
        
        # Initialize pygame if not already done
        if not pygame.get_init():
            pygame.init()
            
        # Create fallback surfaces for when sprite files don't exist
        self._create_fallback_sprites()
    
    def _create_fallback_sprites(self) -> None:
        """Create simple colored rectangle fallbacks for missing sprites"""
        self.fallback_sprites = {
            # Player sprites
            "player_down": self._create_colored_sprite((65, 105, 225), (255, 255, 0)),  # Blue with yellow dot
            "player_up": self._create_colored_sprite((65, 105, 225), (255, 255, 0)),
            "player_left": self._create_colored_sprite((65, 105, 225), (255, 255, 0)),
            "player_right": self._create_colored_sprite((65, 105, 225), (255, 255, 0)),
            
            # NPC sprites
            "npc_default": self._create_colored_sprite((34, 139, 34)),  # Green
            "npc_farmer": self._create_colored_sprite((139, 69, 19)),   # Brown
            "npc_merchant": self._create_colored_sprite((128, 0, 128)), # Purple
            "npc_wise_man": self._create_colored_sprite((105, 105, 105)), # Gray
            
            # Tile sprites
            "tile_grass": self._create_colored_sprite((34, 139, 34)),      # Green
            "tile_wall": self._create_colored_sprite((128, 128, 128)),     # Gray
            "tile_tree": self._create_colored_sprite((0, 100, 0)),         # Dark green
            "tile_water": self._create_colored_sprite((65, 105, 225)),     # Blue
            "tile_mountain": self._create_colored_sprite((128, 128, 128)), # Gray
            "tile_path": self._create_colored_sprite((238, 203, 173)),     # Sandy
            "tile_house": self._create_colored_sprite((139, 69, 19)),      # Brown
            "tile_rock": self._create_colored_sprite((192, 192, 192)),     # Light gray
            "tile_stone": self._create_colored_sprite((64, 64, 64)),       # Dark gray
            "tile_crops": self._create_colored_sprite((255, 255, 0)),      # Yellow
            "tile_barn": self._create_colored_sprite((101, 67, 33)),       # Dark brown
            "tile_well": self._create_colored_sprite((192, 192, 192)),     # Light gray
            "tile_dock": self._create_colored_sprite((101, 67, 33)),       # Dark brown
            "tile_cave": self._create_colored_sprite((0, 0, 0)),           # Black
            "tile_altar": self._create_colored_sprite((128, 0, 128)),      # Purple
            "tile_forest": self._create_colored_sprite((0, 100, 0)),       # Dark green
            
            # Animal sprites
            "animal_cow": self._create_colored_sprite((0, 0, 0), (255, 255, 255)),        # Black with white spots
            "animal_pig": self._create_colored_sprite((255, 192, 203)),                   # Pink
            "animal_chicken": self._create_colored_sprite((255, 255, 255), (255, 140, 0)), # White with orange beak
            "animal_sheep": self._create_colored_sprite((245, 245, 245)),                 # Off-white
            "animal_horse": self._create_colored_sprite((139, 69, 19)),                   # Brown
            "animal_goat": self._create_colored_sprite((255, 248, 220)),                  # Cream
        }
    
    def _create_colored_sprite(self, color: Tuple[int, int, int], 
                              accent_color: Optional[Tuple[int, int, int]] = None) -> pygame.Surface:
        """Create a simple colored rectangle sprite as fallback"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill(color)
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        # Add accent dot if specified (for directional indicators)
        if accent_color:
            center_x, center_y = self.tile_size // 2, self.tile_size // 2
            pygame.draw.circle(sprite, accent_color, (center_x, center_y), 4)
            
        return sprite
    
    def load_sprite(self, sprite_type: SpriteType, sprite_name: str) -> pygame.Surface:
        """Load a sprite from file or return fallback"""
        cache_key = f"{sprite_type.value}_{sprite_name}"
        
        # Return cached sprite if available
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]
            
        # Try to load from file
        sprite_path = os.path.join(self.sprites_dir, sprite_type.value, f"{sprite_name}.png")
        
        if os.path.exists(sprite_path):
            try:
                sprite = pygame.image.load(sprite_path).convert_alpha()
                # Scale to tile size if needed
                sprite = pygame.transform.scale(sprite, (self.tile_size, self.tile_size))
                self.sprite_cache[cache_key] = sprite
                return sprite
            except pygame.error:
                print(f"Warning: Could not load sprite {sprite_path}")
        
        # Use fallback sprite
        if sprite_name in self.fallback_sprites:
            fallback_sprite = self.fallback_sprites[sprite_name]
        else:
            # Generic fallback
            fallback_sprite = self._create_colored_sprite((255, 0, 255))  # Magenta for missing sprites
            
        self.sprite_cache[cache_key] = fallback_sprite
        return fallback_sprite
    
    def get_player_sprite(self, direction: str = "down") -> pygame.Surface:
        """Get player sprite for specific direction"""
        return self.load_sprite(SpriteType.PLAYER, f"player_{direction}")
    
    def get_npc_sprite(self, npc_type: str = "default") -> pygame.Surface:
        """Get NPC sprite by type"""
        return self.load_sprite(SpriteType.NPC, f"npc_{npc_type}")
    
    def get_animal_sprite(self, animal_type: str) -> pygame.Surface:
        """Get animal sprite by type"""
        return self.load_sprite(SpriteType.ANIMAL, f"animal_{animal_type}")
    
    def get_tile_sprite(self, tile_char: str) -> pygame.Surface:
        """Get tile sprite based on tile character"""
        tile_mapping = {
            '#': 'wall',
            'T': 'tree', 
            'F': 'forest',
            'W': 'water',
            'M': 'mountain',
            'P': 'path',
            'H': 'house',
            'R': 'rock',
            'S': 'stone',
            'C': 'crops',
            'B': 'barn',
            'O': 'well',
            'D': 'dock',
            'E': 'cave',
            'A': 'altar',
            '.': 'grass'  # Default grass
        }
        
        tile_name = tile_mapping.get(tile_char, 'grass')
        return self.load_sprite(SpriteType.TILE, f"tile_{tile_name}")
    
    def preload_common_sprites(self) -> None:
        """Preload commonly used sprites for better performance"""
        # Player sprites
        for direction in ['up', 'down', 'left', 'right']:
            self.get_player_sprite(direction)
            
        # Common NPC types
        for npc_type in ['default', 'farmer', 'merchant', 'wise_man']:
            self.get_npc_sprite(npc_type)
            
        # Common animal types
        for animal_type in ['cow', 'pig', 'chicken', 'sheep']:
            self.get_animal_sprite(animal_type)
            
        # Common tiles
        common_tiles = ['#', 'T', 'W', 'M', 'P', 'H', '.']
        for tile in common_tiles:
            self.get_tile_sprite(tile)
    
    def create_sample_sprites(self) -> None:
        """Create some sample sprite files for demonstration"""
        os.makedirs(os.path.join(self.sprites_dir, "player"), exist_ok=True)
        os.makedirs(os.path.join(self.sprites_dir, "npcs"), exist_ok=True)
        os.makedirs(os.path.join(self.sprites_dir, "tiles"), exist_ok=True)
        os.makedirs(os.path.join(self.sprites_dir, "animals"), exist_ok=True)
        
        # Create simple sample sprites and save them
        # This creates actual PNG files that can be replaced with better artwork
        for direction in ['up', 'down', 'left', 'right']:
            sprite = self._create_player_sprite(direction)
            path = os.path.join(self.sprites_dir, "player", f"player_{direction}.png")
            pygame.image.save(sprite, path)
            
        # Sample NPC sprites
        npc_types = {
            'default': (34, 139, 34),     # Green
            'farmer': (139, 69, 19),      # Brown  
            'merchant': (128, 0, 128),    # Purple
            'wise_man': (105, 105, 105)   # Gray
        }
        
        for npc_type, color in npc_types.items():
            sprite = self._create_colored_sprite(color)
            path = os.path.join(self.sprites_dir, "npcs", f"npc_{npc_type}.png")
            pygame.image.save(sprite, path)
            
        # Sample animal sprites
        animal_types = {
            'cow': ((0, 0, 0), (255, 255, 255)),      # Black with white spots
            'pig': ((255, 192, 203), None),           # Pink
            'chicken': ((255, 255, 255), (255, 140, 0)), # White with orange beak
            'sheep': ((245, 245, 245), None),         # Off-white
            'horse': ((139, 69, 19), None),           # Brown
            'goat': ((255, 248, 220), None),          # Cream
        }
        
        for animal_type, colors in animal_types.items():
            if animal_type == 'cow':
                sprite = self._create_cow_sprite()
            elif animal_type == 'chicken':
                sprite = self._create_chicken_sprite()
            else:
                accent_color = colors[1] if len(colors) > 1 else None
                sprite = self._create_colored_sprite(colors[0], accent_color)
            path = os.path.join(self.sprites_dir, "animals", f"animal_{animal_type}.png")
            pygame.image.save(sprite, path)
            
        # Sample tile sprites
        tile_types = {
            'tile_grass': (34, 139, 34),      # Green
            'tile_wall': (128, 128, 128),     # Gray
            'tile_tree': (0, 100, 0),         # Dark green
            'tile_water': (65, 105, 225),     # Blue
            'tile_mountain': (128, 128, 128), # Gray
            'tile_path': (238, 203, 173),     # Sandy
            'tile_house': (139, 69, 19),      # Brown
            'tile_rock': (192, 192, 192),     # Light gray
            'tile_stone': (64, 64, 64),       # Dark gray
            'tile_crops': (255, 255, 0),      # Yellow
            'tile_barn': (101, 67, 33),       # Dark brown
            'tile_well': (192, 192, 192),     # Light gray
            'tile_dock': (101, 67, 33),       # Dark brown
            'tile_cave': (0, 0, 0),           # Black
            'tile_altar': (128, 0, 128),      # Purple
            'tile_forest': (0, 100, 0),       # Dark green
        }
        
        for tile_type, color in tile_types.items():
            if tile_type == 'tile_tree':
                # Create special tree sprite with trunk
                sprite = self._create_tree_sprite()
            elif tile_type == 'tile_house':
                # Create special house sprite with roof
                sprite = self._create_house_sprite()
            elif tile_type == 'tile_well':
                # Create special well sprite with center hole
                sprite = self._create_well_sprite()
            elif tile_type == 'tile_cave':
                # Create special cave sprite with entrance
                sprite = self._create_cave_sprite()
            else:
                sprite = self._create_colored_sprite(color)
            path = os.path.join(self.sprites_dir, "tiles", f"{tile_type}.png")
            pygame.image.save(sprite, path)
    
    def _create_player_sprite(self, direction: str) -> pygame.Surface:
        """Create a player sprite with directional indicator"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((65, 105, 225))  # Blue
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        # Add directional indicator
        center_x, center_y = self.tile_size // 2, self.tile_size // 2
        if direction == 'up':
            pygame.draw.circle(sprite, (255, 255, 0), (center_x, 8), 4)
        elif direction == 'down':
            pygame.draw.circle(sprite, (255, 255, 0), (center_x, self.tile_size - 8), 4)
        elif direction == 'left':
            pygame.draw.circle(sprite, (255, 255, 0), (8, center_y), 4)
        elif direction == 'right':
            pygame.draw.circle(sprite, (255, 255, 0), (self.tile_size - 8, center_y), 4)
            
        return sprite
    
    def _create_tree_sprite(self) -> pygame.Surface:
        """Create a tree sprite with trunk (matching original design)"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((0, 100, 0))  # Dark green background
        
        # Add brown trunk in center
        trunk_size = 16
        trunk_x = (self.tile_size - trunk_size) // 2
        trunk_y = (self.tile_size - trunk_size) // 2
        pygame.draw.rect(sprite, (139, 69, 19), (trunk_x, trunk_y, trunk_size, trunk_size))
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        return sprite
    
    def _create_cow_sprite(self) -> pygame.Surface:
        """Create a cow sprite with black base and white spots"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((0, 0, 0))  # Black base
        
        # Add white spots
        spot_positions = [(8, 8), (20, 6), (6, 18), (22, 20), (14, 24)]
        for spot_x, spot_y in spot_positions:
            pygame.draw.circle(sprite, (255, 255, 255), (spot_x, spot_y), 3)
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        return sprite
    
    def _create_chicken_sprite(self) -> pygame.Surface:
        """Create a chicken sprite with white base and orange beak"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((255, 255, 255))  # White base
        
        # Add orange beak
        beak_points = [(24, 14), (28, 16), (24, 18)]
        pygame.draw.polygon(sprite, (255, 140, 0), beak_points)
        
        # Add red comb on top
        comb_points = [(14, 6), (16, 4), (18, 6)]
        pygame.draw.polygon(sprite, (255, 0, 0), comb_points)
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        return sprite
    
    def _create_house_sprite(self) -> pygame.Surface:
        """Create a house sprite with roof (matching original design)"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((139, 69, 19))  # Brown base
        
        # Add red roof triangle at top
        roof_points = [
            (0, 0),
            (self.tile_size // 2, -8),
            (self.tile_size, 0)
        ]
        pygame.draw.polygon(sprite, (255, 0, 0), roof_points)
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        return sprite
    
    def _create_well_sprite(self) -> pygame.Surface:
        """Create a well sprite with center hole (matching original design)"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((192, 192, 192))  # Light gray base
        
        # Add dark blue center circle
        center_x, center_y = self.tile_size // 2, self.tile_size // 2
        pygame.draw.circle(sprite, (0, 0, 139), (center_x, center_y), 8)
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        return sprite
    
    def _create_cave_sprite(self) -> pygame.Surface:
        """Create a cave sprite with entrance (matching original design)"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((0, 0, 0))  # Black base
        
        # Add gray entrance circle
        center_x, center_y = self.tile_size // 2, self.tile_size // 2
        pygame.draw.circle(sprite, (128, 128, 128), (center_x, center_y), 12)
        
        # Add white border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        return sprite 