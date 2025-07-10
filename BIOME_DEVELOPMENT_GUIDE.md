# 🎮 Biome Development Guide - Ernie's Adventure

## 🎯 Overview

This guide explains how to collaboratively develop different biomes for Ernie's Adventure. Each biome is now in its own file, allowing multiple developers to work on different areas simultaneously without conflicts.

## 📁 Project Structure

```
Ernie/
├── main.py                    # Main game engine (don't modify)
├── biomes/                    # Biome modules (your workspace!)
│   ├── __init__.py           # Package initialization
│   ├── farm_biome.py         # 🏠 Brett's farming area
│   ├── lake_biome.py         # 🏊 Your girlfriend's lake area
│   ├── forest_biome.py       # 🌲 Available for assignment
│   ├── mountain_biome.py     # 🏔️ Available for assignment
│   ├── crossroads_biome.py   # 🍺 Shared central hub
│   ├── ruins_biome.py        # 🏺 Available for assignment
│   ├── southern_biome.py     # 🔨 Available for assignment
│   └── world_features.py     # 🌍 Shared roads & rivers
├── run_game.sh               # Automated game launcher
└── DEVELOPMENT_GUIDE.md      # Original development guide
```

## 🎨 Your Assigned Biomes

### 🏠 Brett's Area: Farm Biome (`biomes/farm_biome.py`)
- **Location**: Northwest (around coordinates 20, 18)
- **Theme**: Peaceful farming village
- **Features**: Crops, houses, barns, well, farming NPCs
- **Status**: ✅ Assigned to Brett

### 🏊 Girlfriend's Area: Lake Biome (`biomes/lake_biome.py`)
- **Location**: Northeast (around coordinates 75, 25)
- **Theme**: Beautiful crystal lake with fishing
- **Features**: Large lake, fishing dock, fisherman's shack
- **Status**: ✅ Ready for development
- **Expansion Ideas**: See the extensive list in the file!

### 🌲 Available Areas
- **Forest**: Dense mysterious woods with hermit
- **Mountains**: Treacherous peaks with caves
- **Ruins**: Ancient mysterious civilization
- **Southern Village**: Crafting village with blacksmith

## 🛠️ How to Work on Your Biome

### 1. Open Your Biome File
```bash
# For the lake biome (girlfriend's area)
open biomes/lake_biome.py
```

### 2. Understand the Structure
Each biome file has two main functions:

```python
def create_lake_section(world, WORLD_WIDTH, WORLD_HEIGHT):
    """Modify the world map to add your biome features"""
    # Add terrain, buildings, water features, etc.
    pass

def get_lake_npcs():
    """Return list of NPCs for your biome"""
    # Define characters with dialogue
    return npcs
```

### 3. Test Your Changes
```bash
# Test your specific biome
./run_game.sh --spawn lake

# List all available spawn points
./run_game.sh --list-sections
```

### 4. Available Tile Types
Use these characters to create your world:

| Character | Meaning | Color | Walkable |
|-----------|---------|-------|----------|
| `.` | Grass | Green | ✅ |
| `#` | Wall/Rock | Gray | ❌ |
| `T` | Tree | Dark Green | ❌ |
| `F` | Dense Forest | Very Dark Green | ❌ |
| `W` | Water | Blue | ❌ |
| `M` | Mountain | Brown | ❌ |
| `P` | Path/Road | Yellow | ✅ |
| `H` | House/Building | Red | ❌ |
| `C` | Crops | Gold | ✅ |
| `S` | Stone/Ruins | Light Gray | ✅ |
| `D` | Dock | Brown | ✅ |
| `B` | Barn | Dark Red | ❌ |
| `O` | Well | Blue | ❌ |
| `A` | Altar | Purple | ✅ |
| `E` | Cave Entrance | Black | ✅ |
| `R` | Rock | Gray | ❌ |

## 💡 Development Tips

### Creating Terrain
```python
# Example: Create a small lake
for y in range(20, 30):
    for x in range(70, 80):
        if 0 < x < WORLD_WIDTH-1 and 0 < y < WORLD_HEIGHT-1:
            world[y][x] = 'W'  # Water

# Example: Add a building
world[25][75] = 'H'  # House at coordinates (75, 25)
```

### Creating NPCs
```python
def get_your_biome_npcs():
    npcs = []
    
    my_character = {
        'name': 'Character Name',
        'x': 75, 'y': 25,  # World coordinates
        'dialogue': [
            "Hello, traveler!",
            "Welcome to my area!",
            "I have many stories to tell.",
            "Come back anytime!"
        ]
    }
    npcs.append(my_character)
    
    return npcs
```

### Best Practices
1. **Stay in your area**: Don't modify coordinates outside your assigned region
2. **Test frequently**: Use `./run_game.sh --spawn yourarea` to test changes
3. **Respect boundaries**: Don't overwrite roads or water systems
4. **Be creative**: Add unique features that make your biome special!
5. **Use comments**: Explain what your code does for other developers

## 🚀 Git Workflow for Collaboration

### 1. Before You Start
```bash
git pull origin main  # Get latest changes
```

### 2. Work on Your Biome
```bash
# Edit your assigned biome file
# Test your changes with ./run_game.sh --spawn yourarea
```

### 3. Commit Your Changes
```bash
git add biomes/your_biome.py
git commit -m "Enhance lake biome with lily pads and boat dock"
```

### 4. Share Your Work
```bash
git push origin main
```

### 5. Get Others' Updates
```bash
git pull origin main  # Get everyone's latest changes
```

## 🎮 Advanced Features You Can Add

### Interactive Elements
- Boats that move you across water
- Teleportation circles
- Hidden passages
- Treasure chests

### Environmental Features
- Weather effects specific to your biome
- Day/night variations
- Seasonal changes
- Animated water or fire

### Complex NPCs
- NPCs that move around
- Quest givers with tasks
- Shopkeepers with items to buy/sell
- NPCs that react to player actions

### Special Mechanics
- Swimming in your lake
- Fishing mini-games
- Climbing mountains
- Magic portals

## 🐛 Troubleshooting

### Game Won't Start
```bash
# Make sure virtual environment is set up
source ernie_env/bin/activate
pip install -r requirements.txt

# Or use the automated launcher
./run_game.sh
```

### Import Errors
```bash
# Make sure __init__.py exists in biomes folder
# Check that function names match the imports in main.py
```

### Can't See Your Changes
- Make sure you're spawning in the right area: `./run_game.sh --spawn yourarea`
- Check coordinates are within your assigned region
- Verify your functions are properly imported in `biomes/__init__.py`

## 🎊 Examples and Inspiration

Look at the existing biome files for examples:
- `farm_biome.py` - Simple village with buildings and crops
- `lake_biome.py` - Water features with circular lake
- `mountain_biome.py` - Terrain generation with paths
- `world_features.py` - Roads and rivers connecting areas

Each file includes extensive expansion ideas in the comments!

## 💬 Communication

- **Brett's area**: Farm biome (northwest)
- **Girlfriend's area**: Lake biome (northeast) 
- **Coordination**: Discuss shared features like roads
- **Questions**: Ask in your development chat

## 🎯 Next Steps

1. Choose your biome from the available areas
2. Open the corresponding `.py` file in `biomes/`
3. Read the expansion ideas at the bottom of the file
4. Start with small changes and test frequently
5. Have fun and be creative!

Remember: Each biome is a world unto itself - make it uniquely yours! 🌟 