# 🌍 Ernie's Adventure - Collaborative Development Guide

## 🚀 Quick Start

### Testing Different Sections
```bash
# List all available spawn points
python3 main.py --list-sections

# Spawn in different areas
python3 main.py --spawn farm      # Start in the farming village
python3 main.py --spawn forest    # Start in the mysterious woods
python3 main.py --spawn mountains # Start in the eastern peaks
python3 main.py --spawn lake      # Start by the crystal lake
python3 main.py --spawn crossroads # Start at the central tavern
python3 main.py --spawn ruins     # Start at ancient ruins
python3 main.py --spawn southern  # Start in the crafting village
python3 main.py --spawn center    # Start at world center
```

## 🗺️ World Sections Overview

### Section Layout
```
🌲 Forest     🏔️ Mountains
   (15,15)      (82,30)
              
🏠 Farm       🏛️ Lake
   (20,18)      (75,25)

🛤️ Center     🍺 Crossroads  
   (50,40)      (60,50)

🏺 Ruins      🔨 Southern
   (15,55)      (30,65)
```

## 👥 Collaborative Workflow

### 1. Choose Your Section
Each developer can claim a section to work on:

- **Brett**: Could work on `farm` and `forest` sections
- **Girlfriend**: Could work on `lake` and `mountains` sections
- **Together**: Work on `crossroads` as the central hub

### 2. Section Independence
Each section is designed to be independent:

```python
def _create_YOUR_section(self, world: List[List[str]]) -> None:
    """Create your custom section"""
    # Your code here - won't conflict with other sections
    pass
```

### 3. Testing Your Changes
```bash
# Test only your section
python3 main.py --spawn YOUR_SECTION

# Test connections between sections
python3 main.py --spawn crossroads  # Central hub
```

## 🛠️ Adding New Features to Sections

### Adding New Tile Types
1. Add the tile character to your section creation function
2. Add the rendering code in `draw_world()`
3. Update collision detection in `Player.move()` if needed

Example:
```python
# In your section function
world[y][x] = 'N'  # New tile type

# In draw_world()
elif tile == 'N':  # New tile
    pygame.draw.rect(self.screen, YOUR_COLOR, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

# In collision detection (if solid)
solid_tiles = {'#', 'W', 'M', 'H', 'F', 'S', 'N'}  # Add 'N' if solid
```

### Adding NPCs to Your Section
```python
# In create_npcs()
your_npc = NPC(x*TILE_SIZE, y*TILE_SIZE, "NPC Name", [
    "Dialogue line 1",
    "Dialogue line 2",
    "Reference other sections for world-building!"
])
npcs.append(your_npc)
```

## 🎨 Current Tile Types

| Tile | Character | Description | Walkable |
|------|-----------|-------------|----------|
| Grass | `.` | Basic ground | ✅ |
| Wall | `#` | Stone walls | ❌ |
| Tree | `T` | Trees | ❌ |
| Dense Forest | `F` | Impassable forest | ❌ |
| Water | `W` | Rivers/lakes | ❌ |
| Mountain | `M` | Rocky peaks | ❌ |
| Path | `P` | Roads | ✅ |
| House | `H` | Buildings | ❌ |
| Rock | `R` | Boulders | ❌ |
| Stone Ruins | `S` | Ancient structures | ❌ |
| Crops | `C` | Farm fields | ✅ |
| Barn | `B` | Farm building | ❌ |
| Well | `O` | Water source | ❌ |
| Dock | `D` | Wooden dock | ✅ |
| Cave | `E` | Cave entrance | ❌ |
| Altar | `A` | Mystical altar | ❌ |

## 🔧 Section Development Template

### Creating a New Section
```python
def _create_NEW_section(self, world: List[List[str]]) -> None:
    """Create the NEW section (Location description)"""
    
    # 1. Define your area boundaries
    start_x, end_x = 10, 30  # X coordinates
    start_y, end_y = 10, 30  # Y coordinates
    
    # 2. Clear/prepare the area
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
                world[y][x] = '.'  # Clear grass
    
    # 3. Add your unique features
    # Buildings
    world[15][15] = 'H'  # House
    
    # Special tiles
    world[20][20] = 'X'  # Your custom tile
    
    # Patterns/areas
    for y in range(12, 18):
        for x in range(12, 18):
            if random.random() < 0.4:
                world[y][x] = 'Y'  # Your feature
```

### Adding to WORLD_SECTIONS
```python
WORLD_SECTIONS['newarea'] = {
    'name': 'Your Area Name',
    'spawn': (25, 25),  # Spawn coordinates
    'description': 'A cool description of your area'
}
```

## 🤝 Collaboration Tips

### 1. Communication
- Discuss which sections each person will work on
- Share ideas for connections between sections
- Coordinate NPC dialogue that references other areas

### 2. Git Workflow
```bash
# Create feature branches for each section
git checkout -b feature/lake-section
git checkout -b feature/mountain-section

# Test before merging
python3 main.py --spawn yoursection

# Merge when ready
git checkout main
git merge feature/yoursection
```

### 3. Testing Integration
```bash
# Test all spawn points work
python3 main.py --list-sections

# Test each section
for section in farm forest lake mountains crossroads ruins southern center; do
    echo "Testing $section..."
    python3 main.py --spawn $section
done
```

### 4. Code Organization
- Each section has its own `_create_SECTION_section()` function
- NPCs are added in `create_npcs()` with clear section comments
- New tile types are documented here

## 🎮 Gameplay Design Guidelines

### Making Sections Feel Unique
1. **Theme**: Each section should have a distinct visual/gameplay theme
2. **NPCs**: Characters should fit the section's theme and reference other areas
3. **Challenges**: Different terrain types create different navigation challenges
4. **Rewards**: Hidden areas, interesting NPCs, or useful items

### Connecting the World
- Use roads (`P` tiles) to connect sections naturally
- NPCs should mention other locations
- Create logical geography (rivers flow downhill, etc.)
- Consider trade routes and travel patterns

### Balance
- Not every section needs to be the same size
- Some can be small and focused, others large and explorable
- Mix of safe and dangerous areas
- Variety in density (busy villages vs. empty wilderness)

## 🐛 Common Issues & Solutions

### Spawn Point Problems
```python
# Make sure spawn coordinates are valid
spawn_x, spawn_y = WORLD_SECTIONS[section]['spawn']
if not (0 < spawn_x < WORLD_WIDTH and 0 < spawn_y < WORLD_HEIGHT):
    print(f"Invalid spawn point for {section}!")
```

### Collision Detection
```python
# Remember to update solid_tiles if adding new impassable tiles
solid_tiles = {'#', 'W', 'M', 'H', 'F', 'S', 'YOUR_NEW_SOLID_TILE'}
```

### Testing Your Section
```bash
# Always test your section works
python3 main.py --spawn yoursection

# Check the minimap shows your features correctly
# Verify NPCs appear and dialogue works
# Test movement and collision detection
```

## 📝 Next Steps

1. **Choose your sections** from the available list
2. **Plan your features** - what makes your section unique?
3. **Start small** - add basic terrain and one NPC
4. **Test frequently** - use `--spawn yoursection`
5. **Expand gradually** - add more features over time
6. **Connect to others** - reference other sections in NPC dialogue

Happy developing! 🎮✨ 