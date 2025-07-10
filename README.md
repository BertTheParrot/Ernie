# Ernie's Adventure

A 2D Python game built with Pygame where Ernie explores a village and talks to NPCs.

## 🎮 Features

- **2D top-down exploration** with smooth movement
- **WASD controls** for movement
- **NPC interactions** with dialogue system
- **Camera following** the player
- **Sprite-based graphics** with customizable image files
- **Multiple biomes** with diverse terrain and NPCs
- **Multiple NPCs** with unique dialogue

## 🚀 How to Run

### Prerequisites
- Python 3.7 or higher
- Pygame

### Installation & Running Instructions

#### Ubuntu/Debian Linux

1. **Update package list and install Python:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Clone or download the game files:**
   ```bash
   # If using git
   git clone <repository-url>
   cd Ernie
   
   # Or navigate to your game directory
   cd /path/to/Ernie
   ```

3. **Create and activate a virtual environment (recommended):**
   ```bash
   python3 -m venv ernie_env
   source ernie_env/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game:**
   ```bash
   python3 main.py
   ```

#### CentOS/RHEL/Fedora

1. **Install Python and development tools:**
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip python3-devel
   
   # Fedora
   sudo dnf install python3 python3-pip python3-devel
   ```

2. **Install SDL development libraries (required for Pygame):**
   ```bash
   # CentOS/RHEL
   sudo yum install SDL2 SDL2-devel SDL2_image SDL2_image-devel
   
   # Fedora
   sudo dnf install SDL2 SDL2-devel SDL2_image SDL2_image-devel
   ```

3. **Navigate to game directory:**
   ```bash
   cd /path/to/Ernie
   ```

4. **Create and activate virtual environment:**
   ```bash
   python3 -m venv ernie_env
   source ernie_env/bin/activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the game:**
   ```bash
   python3 main.py
   ```

#### macOS

1. **Install Python using Homebrew (recommended):**
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python
   ```

2. **Alternative: Download Python from python.org**
   - Visit https://www.python.org/downloads/
   - Download the latest Python 3.x for macOS
   - Run the installer and follow the instructions

3. **Navigate to game directory:**
   ```bash
   cd /path/to/Ernie
   ```

4. **Create and activate virtual environment:**
   ```bash
   python3 -m venv ernie_env
   source ernie_env/bin/activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the game:**
   ```bash
   python3 main.py
   ```

### Troubleshooting

#### Common Issues

**Ubuntu/CentOS: "pygame module not found"**
```bash
# Make sure you're in the virtual environment
source ernie_env/bin/activate

# Reinstall pygame
pip uninstall pygame
pip install pygame==2.5.2
```

**CentOS: SDL2 compilation errors**
```bash
# Install additional development libraries
sudo yum groupinstall "Development Tools"
sudo yum install gcc gcc-c++ make
```

**macOS: "pygame module not found"**
```bash
# Make sure you're in the virtual environment
source ernie_env/bin/activate

# Try installing with specific flags
pip install pygame==2.5.2 --pre
```

**Display issues on Linux:**
```bash
# Set display environment variable
export DISPLAY=:0

# Or run with specific display
python3 main.py --display :0
```

### Quick Start (All Platforms)

If you have Python already installed:

```bash
# Navigate to game directory
cd /path/to/Ernie

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## 🎯 Controls

- **WASD** or **Arrow Keys** - Move Ernie around
- **SPACE** - Interact with NPCs when close
- **ESC** - Close dialogue boxes
- **Close window** - Quit the game

## 🗺️ Game World

- **Blue rectangle** - Ernie (the player)
- **Green rectangles** - NPCs you can talk to
- **Gray tiles** - Walls (can't walk through)
- **Brown tiles** - Trees (decorative)
- **Green tiles** - Grass (walkable)

## 👥 NPCs

1. **Farmer Joe** (200, 200) - Welcomes you to the village
2. **Wise Old Man** (600, 150) - Gives philosophical advice
3. **Merchant** (400, 500) - Talks about his shop

## 🎮 How to Play

1. **Move around** using WASD or arrow keys
2. **Approach NPCs** (green rectangles) to see interaction prompts
3. **Press SPACE** when close to an NPC to start talking
4. **Press SPACE again** to continue the dialogue
5. **Press ESC** to close dialogue boxes

## 🛠️ Technical Details

- **Pygame** - 2D graphics and input handling
- **Type hints** - Full Python type annotations
- **Object-oriented design** - Clean, modular code structure
- **60 FPS** - Smooth gameplay
- **Collision detection** - Can't walk through walls

## 🎨 Sprite System

The game now uses a flexible sprite system instead of colored rectangles! 

- **Custom Graphics**: Replace simple rectangles with your own artwork
- **Easy Setup**: Just drop PNG files into the `sprites/` directory
- **Automatic Fallbacks**: Game works even without custom sprites
- **Multiple Types**: Player sprites, NPC sprites, and tile sprites

See the **[Sprite Guide](SPRITE_GUIDE.md)** for detailed instructions on creating and using custom sprites.

## 🎯 Future Enhancements

- Sound effects and background music
- More NPCs and dialogue options
- Inventory system
- Quests and objectives
- Save/load functionality
- Animated sprites

---

**Enjoy exploring the village with Ernie!** 🏰👤🗣️ 