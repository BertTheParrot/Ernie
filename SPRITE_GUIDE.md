# Sprite System Guide

## Overview

Ernie's Adventure now uses a sprite-based rendering system instead of colored rectangles. This guide explains how the sprite system works and how to customize it with your own artwork.

## Directory Structure

```
sprites/
├── player/
│   ├── player_up.png
│   ├── player_down.png
│   ├── player_left.png
│   └── player_right.png
├── npcs/
│   ├── npc_default.png
│   ├── npc_farmer.png
│   ├── npc_merchant.png
│   └── npc_wise_man.png
└── tiles/
    ├── tile_grass.png
    ├── tile_wall.png
    ├── tile_tree.png
    ├── tile_water.png
    ├── tile_mountain.png
    └── [other tile types]
```

## How the Sprite System Works

### SpriteManager Class

The `SpriteManager` class handles all sprite loading, caching, and fallback functionality:

- **Loading**: Automatically loads PNG files from the sprites directory
- **Caching**: Keeps loaded sprites in memory for better performance
- **Fallbacks**: Uses colored rectangles when sprite files don't exist
- **Scaling**: Automatically scales sprites to the correct tile size (32x32 pixels)

### Automatic Sprite Detection

The system automatically tries to load sprite files when needed:

1. Player sprites: `sprites/player/player_[direction].png`
2. NPC sprites: `sprites/npcs/npc_[type].png`
3. Tile sprites: `sprites/tiles/tile_[type].png`

If a sprite file doesn't exist, the system falls back to the original colored rectangle graphics.

## Adding Custom Sprites

### Player Sprites

Create 32x32 pixel PNG files for each direction:

- `sprites/player/player_up.png` - Player facing up
- `sprites/player/player_down.png` - Player facing down
- `sprites/player/player_left.png` - Player facing left
- `sprites/player/player_right.png` - Player facing right

### NPC Sprites

Create NPC sprites based on character types:

- `sprites/npcs/npc_default.png` - Generic NPC
- `sprites/npcs/npc_farmer.png` - Farm-related NPCs
- `sprites/npcs/npc_merchant.png` - Merchants and traders
- `sprites/npcs/npc_wise_man.png` - Wise men, elders, advisors

The system automatically assigns NPC types based on their names:
- Names containing "farmer" or "joe" → farmer sprite
- Names containing "merchant" or "trader" → merchant sprite
- Names containing "wise", "old", or "elder" → wise_man sprite
- All others → default sprite

### Tile Sprites

Create sprites for world tiles:

- `sprites/tiles/tile_grass.png` - Grass tiles (.)
- `sprites/tiles/tile_wall.png` - Wall tiles (#)
- `sprites/tiles/tile_tree.png` - Tree tiles (T)
- `sprites/tiles/tile_water.png` - Water tiles (W)
- `sprites/tiles/tile_mountain.png` - Mountain tiles (M)
- `sprites/tiles/tile_path.png` - Path tiles (P)
- `sprites/tiles/tile_house.png` - House tiles (H)
- `sprites/tiles/tile_rock.png` - Rock tiles (R)
- `sprites/tiles/tile_stone.png` - Stone ruin tiles (S)
- `sprites/tiles/tile_crops.png` - Crop tiles (C)
- `sprites/tiles/tile_barn.png` - Barn tiles (B)
- `sprites/tiles/tile_well.png` - Well tiles (O)
- `sprites/tiles/tile_dock.png` - Dock tiles (D)
- `sprites/tiles/tile_cave.png` - Cave entrance tiles (E)
- `sprites/tiles/tile_altar.png` - Altar tiles (A)
- `sprites/tiles/tile_forest.png` - Dense forest tiles (F)

## Sprite Guidelines

### Image Requirements

- **Format**: PNG with alpha transparency support
- **Size**: 32x32 pixels (will be automatically scaled)
- **Style**: Pixel art works best for the game's aesthetic
- **Transparency**: Use alpha channel for transparent areas

### Design Tips

1. **Consistency**: Use similar color palettes and art styles
2. **Clarity**: Make sprites recognizable at 32x32 pixel size
3. **Contrast**: Ensure sprites stand out against backgrounds
4. **Animation**: Currently static sprites only (animation support could be added)

## Creating Sample Sprites

The system can generate basic sample sprites for you:

```python
from sprite_manager import SpriteManager
sm = SpriteManager()
sm.create_sample_sprites()
```

This creates simple colored rectangle sprites that you can use as templates or replace with your own artwork.

## Advanced Customization

### Adding New NPC Types

1. Add new sprite files: `sprites/npcs/npc_[new_type].png`
2. Update the `_get_npc_type()` method in `main.py` to recognize new NPC names
3. Use the new type when creating NPCs

### Adding New Tile Types

1. Add new sprite files: `sprites/tiles/tile_[new_type].png`
2. Update the tile mapping in `SpriteManager.get_tile_sprite()`
3. Add the new tile character to your world maps

### Performance Optimization

The sprite system includes several performance optimizations:

- **Sprite caching**: Loaded sprites are cached in memory
- **Preloading**: Common sprites are preloaded at game start
- **Efficient scaling**: Sprites are scaled once when loaded, not every frame

## Troubleshooting

### Common Issues

**Sprites not loading:**
- Check file paths and naming conventions
- Ensure PNG format and correct permissions
- Verify sprite files are in the correct directories

**Performance issues:**
- Use appropriate image sizes (32x32 recommended)
- Avoid overly complex sprites
- Consider the number of unique sprites in your game

**Visual problems:**
- Check alpha channels for transparency
- Ensure consistent pixel art scale
- Test sprites against different backgrounds

### Fallback System

If sprites fail to load, the system automatically falls back to colored rectangles. This ensures the game always works even without custom artwork.

## Example: Creating a Custom Player Sprite

1. Create a 32x32 pixel image in your favorite art program
2. Draw your character facing down
3. Save as `sprites/player/player_down.png`
4. Create similar sprites for other directions
5. Run the game to see your custom character!

The sprite system makes it easy to give Ernie's Adventure a unique visual style while maintaining compatibility with the existing game mechanics. 