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
        """Create enhanced colored sprites with texture"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        
        # Add gradient effect for better visual appeal
        base_color = color
        highlight_color = tuple(min(255, c + 30) for c in color)
        shadow_color = tuple(max(0, c - 30) for c in color)
        
        # Fill with base color
        sprite.fill(base_color)
        
        # Add simple texture based on color type
        if color == (34, 139, 34):  # Grass
            # Add grass texture
            for i in range(0, self.tile_size, 4):
                for j in range(0, self.tile_size, 4):
                    if (i + j) % 8 == 0:
                        pygame.draw.rect(sprite, highlight_color, (i, j, 2, 1))
        elif color == (65, 105, 225):  # Water
            # Add water ripples
            for i in range(0, self.tile_size, 6):
                pygame.draw.line(sprite, highlight_color, (0, i), (self.tile_size, i), 1)
        elif color == (128, 128, 128):  # Stone/Wall
            # Add stone texture
            for i in range(4):
                x = (i * 8) % self.tile_size
                y = (i * 6) % self.tile_size
                pygame.draw.rect(sprite, shadow_color, (x, y, 3, 3))
        
        # Add accent dot if specified
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
        """Create a detailed player character sprite"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((34, 139, 34))  # Grass background
        
        # Character body (blue shirt)
        body_color = (65, 105, 225)
        head_color = (255, 220, 177)  # Skin tone
        
        # Head
        pygame.draw.circle(sprite, head_color, (16, 10), 6)
        
        # Body
        pygame.draw.rect(sprite, body_color, (11, 14, 10, 12))
        
        # Arms
        pygame.draw.rect(sprite, body_color, (8, 16, 4, 8))
        pygame.draw.rect(sprite, body_color, (20, 16, 4, 8))
        
        # Legs (brown pants)
        leg_color = (101, 67, 33)
        pygame.draw.rect(sprite, leg_color, (12, 26, 3, 6))
        pygame.draw.rect(sprite, leg_color, (17, 26, 3, 6))
        
        # Eyes (black dots)
        if direction == 'left':
            pygame.draw.circle(sprite, (0, 0, 0), (13, 9), 1)
        elif direction == 'right':
            pygame.draw.circle(sprite, (0, 0, 0), (19, 9), 1)
        else:  # up/down
            pygame.draw.circle(sprite, (0, 0, 0), (14, 9), 1)
            pygame.draw.circle(sprite, (0, 0, 0), (18, 9), 1)
        
        # Directional indicator (hat/hair)
        hat_color = (139, 69, 19)
        if direction == 'up':
            pygame.draw.rect(sprite, hat_color, (13, 4, 6, 3))
        elif direction == 'down':
            pygame.draw.rect(sprite, hat_color, (13, 6, 6, 3))
        elif direction == 'left':
            pygame.draw.rect(sprite, hat_color, (10, 5, 6, 3))
        elif direction == 'right':
            pygame.draw.rect(sprite, hat_color, (16, 5, 6, 3))
            
        return sprite
    
    def _create_tree_sprite(self) -> pygame.Surface:
        """Create a detailed tree sprite that actually looks like a tree"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((34, 139, 34))  # Grass green background
        
        # Draw brown trunk (thicker at bottom, thinner at top)
        trunk_bottom_width = 8
        trunk_top_width = 6
        trunk_height = 20
        trunk_x = (self.tile_size - trunk_bottom_width) // 2
        trunk_y = self.tile_size - trunk_height
        
        # Draw trunk with slight taper
        for i in range(trunk_height):
            y = trunk_y + i
            width = trunk_bottom_width - (i * (trunk_bottom_width - trunk_top_width) // trunk_height)
            x = (self.tile_size - width) // 2
            pygame.draw.rect(sprite, (101, 67, 33), (x, y, width, 1))
        
        # Draw tree foliage in layers (darker to lighter green)
        center_x, center_y = self.tile_size // 2, 12
        
        # Dark green base layer (largest)
        pygame.draw.circle(sprite, (0, 100, 0), (center_x, center_y), 12)
        
        # Medium green middle layer
        pygame.draw.circle(sprite, (34, 139, 34), (center_x - 2, center_y - 2), 8)
        
        # Light green highlight layer
        pygame.draw.circle(sprite, (50, 205, 50), (center_x - 3, center_y - 3), 5)
        
        # Add some texture with small dark spots
        for spot_x, spot_y in [(center_x - 6, center_y + 2), (center_x + 4, center_y - 1), (center_x - 1, center_y + 4)]:
            pygame.draw.circle(sprite, (0, 80, 0), (spot_x, spot_y), 1)
        
        return sprite
    
    def _create_cow_sprite(self) -> pygame.Surface:
        """Create a detailed cow sprite"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((34, 139, 34))  # Grass background
        
        # Cow body (white base)
        body_color = (255, 255, 255)
        pygame.draw.ellipse(sprite, body_color, (4, 10, 24, 16))
        
        # Cow head
        pygame.draw.ellipse(sprite, body_color, (6, 6, 12, 10))
        
        # Black spots
        spot_color = (0, 0, 0)
        pygame.draw.ellipse(sprite, spot_color, (8, 12, 6, 4))
        pygame.draw.ellipse(sprite, spot_color, (18, 14, 5, 3))
        pygame.draw.ellipse(sprite, spot_color, (10, 20, 4, 3))
        
        # Legs (black)
        pygame.draw.rect(sprite, spot_color, (8, 24, 2, 4))
        pygame.draw.rect(sprite, spot_color, (12, 24, 2, 4))
        pygame.draw.rect(sprite, spot_color, (18, 24, 2, 4))
        pygame.draw.rect(sprite, spot_color, (22, 24, 2, 4))
        
        # Eyes
        pygame.draw.circle(sprite, spot_color, (10, 9), 1)
        pygame.draw.circle(sprite, spot_color, (14, 9), 1)
        
        # Nose/snout
        pygame.draw.ellipse(sprite, (255, 192, 203), (10, 12, 4, 2))
        
        return sprite
    
    def _create_chicken_sprite(self) -> pygame.Surface:
        """Create a detailed chicken sprite"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((34, 139, 34))  # Grass background
        
        # Chicken body (white)
        body_color = (255, 255, 255)
        pygame.draw.ellipse(sprite, body_color, (8, 12, 16, 12))
        
        # Chicken head
        pygame.draw.circle(sprite, body_color, (12, 8), 5)
        
        # Beak (orange)
        beak_points = [(7, 8), (4, 9), (7, 10)]
        pygame.draw.polygon(sprite, (255, 140, 0), beak_points)
        
        # Comb (red)
        comb_points = [(10, 4), (12, 2), (14, 4)]
        pygame.draw.polygon(sprite, (255, 0, 0), comb_points)
        
        # Eye
        pygame.draw.circle(sprite, (0, 0, 0), (11, 7), 1)
        
        # Tail feathers
        tail_color = (245, 245, 245)
        tail_points = [(22, 14), (28, 10), (26, 18)]
        pygame.draw.polygon(sprite, tail_color, tail_points)
        
        # Legs (orange)
        pygame.draw.rect(sprite, (255, 140, 0), (10, 22, 1, 4))
        pygame.draw.rect(sprite, (255, 140, 0), (14, 22, 1, 4))
        
        # Wing detail
        pygame.draw.arc(sprite, (220, 220, 220), (10, 14, 8, 6), 0, 3.14, 1)
        
        return sprite
    
    def _create_house_sprite(self) -> pygame.Surface:
        """Create a detailed house sprite that looks like a real house"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((34, 139, 34))  # Grass background
        
        # House walls (light brown/tan)
        wall_color = (210, 180, 140)
        wall_rect = (4, 12, 24, 16)
        pygame.draw.rect(sprite, wall_color, wall_rect)
        
        # Roof (dark red, triangular)
        roof_color = (139, 69, 19)
        roof_points = [(2, 12), (16, 4), (30, 12)]
        pygame.draw.polygon(sprite, roof_color, roof_points)
        
        # Door (dark brown)
        door_color = (101, 67, 33)
        door_rect = (13, 18, 6, 10)
        pygame.draw.rect(sprite, door_color, door_rect)
        
        # Door handle (yellow)
        pygame.draw.circle(sprite, (255, 215, 0), (17, 23), 1)
        
        # Windows (light blue with white frames)
        window_frame = (255, 255, 255)
        window_glass = (173, 216, 230)
        
        # Left window
        pygame.draw.rect(sprite, window_frame, (7, 15, 5, 5))
        pygame.draw.rect(sprite, window_glass, (8, 16, 3, 3))
        
        # Right window  
        pygame.draw.rect(sprite, window_frame, (20, 15, 5, 5))
        pygame.draw.rect(sprite, window_glass, (21, 16, 3, 3))
        
        # Chimney (dark gray)
        pygame.draw.rect(sprite, (105, 105, 105), (22, 6, 4, 8))
        
        return sprite
    
    def _create_well_sprite(self) -> pygame.Surface:
        """Create a detailed well sprite"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((34, 139, 34))  # Grass background
        
        # Well base (stone gray)
        well_outer = (169, 169, 169)
        pygame.draw.circle(sprite, well_outer, (16, 16), 12)
        
        # Well inner wall (darker gray)
        pygame.draw.circle(sprite, (105, 105, 105), (16, 16), 10)
        
        # Water (dark blue)
        pygame.draw.circle(sprite, (25, 25, 112), (16, 16), 7)
        
        # Water reflection (light blue)
        pygame.draw.circle(sprite, (70, 130, 180), (14, 14), 2)
        
        # Well roof support posts (brown)
        pygame.draw.rect(sprite, (101, 67, 33), (8, 4, 2, 12))
        pygame.draw.rect(sprite, (101, 67, 33), (22, 4, 2, 12))
        
        # Well roof (dark brown)
        roof_points = [(6, 4), (16, 0), (26, 4)]
        pygame.draw.polygon(sprite, (139, 69, 19), roof_points)
        
        return sprite
    
    def _create_cave_sprite(self) -> pygame.Surface:
        """Create a detailed cave entrance sprite"""
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.fill((105, 105, 105))  # Gray rock background
        
        # Cave opening (black)
        pygame.draw.ellipse(sprite, (0, 0, 0), (6, 8, 20, 16))
        
        # Rock texture around entrance (various grays)
        rock_colors = [(169, 169, 169), (128, 128, 128), (105, 105, 105)]
        
        # Add rocky texture
        for i in range(15):
            x = (i * 7) % 28 + 2
            y = (i * 11) % 28 + 2
            color = rock_colors[i % 3]
            pygame.draw.circle(sprite, color, (x, y), 2)
        
        # Darker shadows around cave entrance
        pygame.draw.arc(sprite, (64, 64, 64), (5, 7, 22, 18), 0, 3.14159, 2)
        
        return sprite