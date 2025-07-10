import pygame
import random
import math
from typing import List, Tuple
from sprite_manager import SpriteManager

class Animal:
    """Represents a farm animal that wanders around"""
    
    def __init__(self, x: int, y: int, animal_type: str, sprite_manager: SpriteManager, 
                 bounds: Tuple[int, int, int, int] = None):
        self.x = x
        self.y = y
        self.width = 32  # TILE_SIZE
        self.height = 32
        self.animal_type = animal_type
        self.sprite_manager = sprite_manager
        
        # Movement properties
        self.speed = 0.5  # Slower than player
        self.direction_x = 0
        self.direction_y = 0
        self.move_timer = 0
        self.move_duration = random.randint(60, 180)  # Frames to move in one direction
        self.rest_duration = random.randint(30, 120)   # Frames to rest
        self.is_resting = False
        
        # Boundary area (min_x, min_y, max_x, max_y) - keeps animals in their area
        if bounds:
            self.bounds = bounds
        else:
            # Default to a small area around spawn point
            self.bounds = (x - 100, y - 100, x + 100, y + 100)
        
        # Animal-specific properties
        self.sounds = self._get_animal_sounds()
        self.behavior = self._get_animal_behavior()
        
    def _get_animal_sounds(self) -> List[str]:
        """Get sounds this animal might make (for future sound system)"""
        sound_map = {
            'cow': ['Moo!', 'Mooo!'],
            'pig': ['Oink!', 'Snort!'],
            'chicken': ['Cluck!', 'Bawk!'],
            'sheep': ['Baa!', 'Bleat!'],
            'horse': ['Neigh!', 'Whinny!'],
            'goat': ['Bleat!', 'Maa!']
        }
        return sound_map.get(self.animal_type, ['...'])
    
    def _get_animal_behavior(self) -> dict:
        """Get behavior properties for this animal type"""
        behaviors = {
            'cow': {'speed_multiplier': 0.7, 'rest_frequency': 0.4},
            'pig': {'speed_multiplier': 0.8, 'rest_frequency': 0.5},
            'chicken': {'speed_multiplier': 1.2, 'rest_frequency': 0.2},
            'sheep': {'speed_multiplier': 0.9, 'rest_frequency': 0.3},
            'horse': {'speed_multiplier': 1.0, 'rest_frequency': 0.2},
            'goat': {'speed_multiplier': 1.1, 'rest_frequency': 0.3}
        }
        return behaviors.get(self.animal_type, {'speed_multiplier': 1.0, 'rest_frequency': 0.3})
    
    def update(self, world_map: List[List[str]]) -> None:
        """Update animal movement and behavior"""
        self.move_timer += 1
        
        # Check if it's time to change behavior
        if self.is_resting:
            if self.move_timer >= self.rest_duration:
                self._start_moving()
        else:
            if self.move_timer >= self.move_duration:
                if random.random() < self.behavior['rest_frequency']:
                    self._start_resting()
                else:
                    self._change_direction()
        
        # Move if not resting
        if not self.is_resting:
            self._move(world_map)
    
    def _start_moving(self) -> None:
        """Start moving in a random direction"""
        self.is_resting = False
        self.move_timer = 0
        self.move_duration = random.randint(60, 180)
        self._change_direction()
    
    def _start_resting(self) -> None:
        """Stop and rest for a while"""
        self.is_resting = True
        self.move_timer = 0
        self.rest_duration = random.randint(30, 120)
        self.direction_x = 0
        self.direction_y = 0
    
    def _change_direction(self) -> None:
        """Change movement direction randomly"""
        directions = [
            (0, 0),    # Stay still
            (1, 0),    # Right
            (-1, 0),   # Left
            (0, 1),    # Down
            (0, -1),   # Up
            (1, 1),    # Diagonal down-right
            (-1, 1),   # Diagonal down-left
            (1, -1),   # Diagonal up-right
            (-1, -1)   # Diagonal up-left
        ]
        
        self.direction_x, self.direction_y = random.choice(directions)
        
        # Normalize diagonal movement
        if self.direction_x != 0 and self.direction_y != 0:
            self.direction_x *= 0.7
            self.direction_y *= 0.7
    
    def _move(self, world_map: List[List[str]]) -> None:
        """Move the animal according to its current direction"""
        if self.direction_x == 0 and self.direction_y == 0:
            return
            
        # Calculate new position
        speed = self.speed * self.behavior['speed_multiplier']
        new_x = self.x + (self.direction_x * speed)
        new_y = self.y + (self.direction_y * speed)
        
        # Check bounds
        if (new_x < self.bounds[0] or new_x > self.bounds[2] or
            new_y < self.bounds[1] or new_y > self.bounds[3]):
            self._change_direction()
            return
        
        # Check collision with solid tiles
        tile_x = int(new_x // 32)
        tile_y = int(new_y // 32)
        
        # Solid tiles that animals can't walk through
        solid_tiles = {'#', 'W', 'M', 'H', 'F', 'S', 'B'}  # Added 'B' for barn
        
        world_height = len(world_map)
        world_width = len(world_map[0]) if world_height > 0 else 0
        
        if (0 <= tile_y < world_height and 0 <= tile_x < world_width and 
            world_map[tile_y][tile_x] in solid_tiles):
            self._change_direction()
            return
            
        # Move to new position
        self.x = new_x
        self.y = new_y
    
    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
        """Draw the animal sprite"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Only draw if on screen
        if (-32 <= screen_x <= 832 and -32 <= screen_y <= 632):
            # Get the appropriate sprite for this animal
            animal_sprite = self.sprite_manager.get_animal_sprite(self.animal_type)
            
            # Draw the animal sprite
            screen.blit(animal_sprite, (screen_x, screen_y))
    
    def get_interaction_text(self) -> str:
        """Get text for when player interacts with animal"""
        return random.choice(self.sounds)

class FarmAnimals:
    """Manager class for all farm animals"""
    
    def __init__(self, sprite_manager: SpriteManager):
        self.sprite_manager = sprite_manager
        self.animals: List[Animal] = []
    
    def add_animal(self, x: int, y: int, animal_type: str, 
                   bounds: Tuple[int, int, int, int] = None) -> None:
        """Add a new animal to the farm"""
        animal = Animal(x, y, animal_type, self.sprite_manager, bounds)
        self.animals.append(animal)
    
    def create_farm_animals(self) -> None:
        """Create animals for the farm biome"""
        # Convert tile coordinates to pixel coordinates
        tile_to_pixel = lambda x, y: (x * 32, y * 32)
        
        # Cow pasture near the barn (around 22, 22)
        cow_bounds = tile_to_pixel(18, 18) + tile_to_pixel(26, 26)
        for i in range(2):  # 2 cows
            cow_x, cow_y = tile_to_pixel(20 + i, 23)
            self.add_animal(cow_x, cow_y, 'cow', cow_bounds)
        
        # Pig pen area (around 17, 24)
        pig_bounds = tile_to_pixel(15, 22) + tile_to_pixel(19, 26)
        for i in range(2):  # 2 pigs
            pig_x, pig_y = tile_to_pixel(16 + i, 24)
            self.add_animal(pig_x, pig_y, 'pig', pig_bounds)
        
        # Chickens near the farm buildings
        chicken_bounds = tile_to_pixel(17, 17) + tile_to_pixel(25, 25)
        for i in range(2):  # 2 chickens
            chicken_x, chicken_y = tile_to_pixel(18 + (i % 2), 20 + (i // 2))
            self.add_animal(chicken_x, chicken_y, 'chicken', chicken_bounds)
        
        # Sheep in a separate field
        sheep_bounds = tile_to_pixel(25, 18) + tile_to_pixel(30, 22)
        for i in range(2):  # 2 sheep
            sheep_x, sheep_y = tile_to_pixel(26 + (i % 2), 19 + (i // 2))
            self.add_animal(sheep_x, sheep_y, 'sheep', sheep_bounds)
    
    def update(self, world_map: List[List[str]]) -> None:
        """Update all animals"""
        for animal in self.animals:
            animal.update(world_map)
    
    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
        """Draw all animals"""
        for animal in self.animals:
            animal.draw(screen, camera_x, camera_y)
    
    def check_interactions(self, player_x: int, player_y: int, tile_size: int) -> str:
        """Check if player is close enough to interact with any animal"""
        for animal in self.animals:
            distance = math.sqrt((player_x - animal.x)**2 + (player_y - animal.y)**2)
            if distance < tile_size * 1.5:  # Close enough to interact
                return f"{animal.animal_type.title()}: {animal.get_interaction_text()}"
        return "" 