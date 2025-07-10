import pygame
import sys
import math
from typing import List, Dict, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
PLAYER_SPEED = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BLUE = (65, 105, 225)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

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
        if new_x < 0 or new_x >= len(world_map[0]) * TILE_SIZE - self.width:
            return
        if new_y < 0 or new_y >= len(world_map) * TILE_SIZE - self.height:
            return
            
        # Check collision with walls
        tile_x = new_x // TILE_SIZE
        tile_y = new_y // TILE_SIZE
        
        if (tile_y < len(world_map) and tile_x < len(world_map[0]) and 
            world_map[tile_y][tile_x] != '#'):
            self.x = new_x
            self.y = new_y
            self.is_moving = True
        else:
            self.is_moving = False
            
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
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ernie's Adventure")
        self.clock = pygame.time.Clock()
        
        # Create world map
        self.world_map = self.create_world()
        
        # Create player
        self.player = Player(400, 300)
        
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
        """Create a simple world map"""
        world = []
        for y in range(20):
            row = []
            for x in range(25):
                if x == 0 or x == 24 or y == 0 or y == 19:
                    row.append('#')  # Wall
                elif (x == 5 and y == 5) or (x == 15 and y == 10) or (x == 8 and y == 15):
                    row.append('T')  # Tree
                else:
                    row.append('.')  # Grass
            world.append(row)
        return world
        
    def create_npcs(self) -> List[NPC]:
        """Create NPCs with dialogue"""
        npcs = []
        
        # Farmer Joe
        farmer_joe = NPC(200, 200, "Farmer Joe", [
            "Hello there, young adventurer!",
            "Welcome to our little village.",
            "I've been farming these lands for 30 years.",
            "If you need any help, just ask around!"
        ])
        npcs.append(farmer_joe)
        
        # Wise Old Man
        wise_man = NPC(600, 150, "Wise Old Man", [
            "Ah, a new face in our village!",
            "I sense great potential in you, young one.",
            "The world is full of mysteries to discover.",
            "Remember, the journey is as important as the destination."
        ])
        npcs.append(wise_man)
        
        # Merchant
        merchant = NPC(400, 500, "Merchant", [
            "Welcome to my shop, traveler!",
            "I have the finest goods in all the land.",
            "Though business has been slow lately...",
            "Feel free to browse my wares!"
        ])
        npcs.append(merchant)
        
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
        
        # Keep camera in bounds
        self.camera_x = max(0, min(self.camera_x, len(self.world_map[0]) * TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, len(self.world_map) * TILE_SIZE - SCREEN_HEIGHT))
        
    def draw_world(self) -> None:
        """Draw the world map"""
        for y in range(len(self.world_map)):
            for x in range(len(self.world_map[y])):
                tile = self.world_map[y][x]
                screen_x = x * TILE_SIZE - self.camera_x
                screen_y = y * TILE_SIZE - self.camera_y
                
                # Only draw tiles that are visible
                if (screen_x > -TILE_SIZE and screen_x < SCREEN_WIDTH + TILE_SIZE and
                    screen_y > -TILE_SIZE and screen_y < SCREEN_HEIGHT + TILE_SIZE):
                    
                    if tile == '#':  # Wall
                        pygame.draw.rect(self.screen, GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    elif tile == 'T':  # Tree
                        pygame.draw.rect(self.screen, BROWN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                    else:  # Grass
                        pygame.draw.rect(self.screen, GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                        
                    # Draw grid lines
                    pygame.draw.rect(self.screen, BLACK, (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
                    
    def draw_ui(self) -> None:
        """Draw UI elements"""
        # Title
        title_text = self.font.render("Ernie's Adventure", True, WHITE)
        self.screen.blit(title_text, (10, 10))
        
        # Controls
        controls_text = self.small_font.render("WASD: Move | SPACE: Interact", True, WHITE)
        self.screen.blit(controls_text, (10, 40))
        
        # Player position (debug)
        pos_text = self.small_font.render(f"Position: ({self.player.x}, {self.player.y})", True, WHITE)
        self.screen.blit(pos_text, (10, 70))
        
        # Dialogue box
        if self.show_dialogue and self.dialogue_text:
            # Draw dialogue background
            dialogue_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
            pygame.draw.rect(self.screen, BLACK, dialogue_rect)
            pygame.draw.rect(self.screen, WHITE, dialogue_rect, 3)
            
            # Draw dialogue text
            dialogue_surface = self.small_font.render(self.dialogue_text, True, WHITE)
            dialogue_rect_text = dialogue_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
            self.screen.blit(dialogue_surface, dialogue_rect_text)
            
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

if __name__ == "__main__":
    game = Game()
    game.run() 