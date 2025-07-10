# Farm Animals Guide

## Overview

Ernie's Adventure now features living farm animals that wander around the farm biome! Each animal has unique behaviors, sprites, and can be interacted with. The farm contains 2 of each animal type for a balanced, lively but not overwhelming experience.

## Available Animals

### 🐄 **Cows**
- **Location**: Cow pasture near the barn
- **Behavior**: Slow-moving, rest frequently
- **Sounds**: "Moo!", "Mooo!"
- **Appearance**: Black with white spots

### 🐷 **Pigs** 
- **Location**: Pig pen area
- **Behavior**: Medium speed, rest often
- **Sounds**: "Oink!", "Snort!"
- **Appearance**: Pink

### 🐔 **Chickens**
- **Location**: Around farm buildings  
- **Behavior**: Fast-moving, rarely rest
- **Sounds**: "Cluck!", "Bawk!"
- **Appearance**: White with orange beak and red comb

### 🐑 **Sheep**
- **Location**: Separate sheep field
- **Behavior**: Medium speed, moderate rest
- **Sounds**: "Baa!", "Bleat!"
- **Appearance**: Off-white/cream colored

### 🐴 **Horses** *(Available for future expansion)*
- **Behavior**: Fast-moving, rarely rest
- **Sounds**: "Neigh!", "Whinny!"
- **Appearance**: Brown

### 🐐 **Goats** *(Available for future expansion)*
- **Behavior**: Quick and agile
- **Sounds**: "Bleat!", "Maa!"
- **Appearance**: Cream colored

## Animal Behavior System

### Movement Patterns
- **Wandering**: Animals move randomly within their designated areas
- **Resting**: Animals occasionally stop to rest
- **Boundaries**: Each animal type is confined to its pasture area
- **Collision**: Animals can't walk through buildings, water, or fences

### Individual Behaviors
Each animal type has unique characteristics:
- **Speed multipliers**: Chickens are fastest, cows are slowest
- **Rest frequency**: How often they stop moving
- **Territorial bounds**: Specific areas they're confined to

### AI Features
- **Random direction changes**: Animals change direction periodically
- **Boundary avoidance**: Turn around when reaching pasture edges
- **Obstacle avoidance**: Navigate around buildings and solid objects
- **Realistic timing**: Movement and rest periods vary naturally

## Interaction System

### Player Interactions
- **Approach animals** to see interaction prompts
- **Press SPACE** when close to interact
- **Hear animal sounds** like "Moo!" or "Cluck!"
- **Simple dialogue system** for each animal type

### Future Interaction Ideas
- Feed animals with crops
- Collect milk from cows
- Collect eggs from chickens
- Pet animals for friendship points
- Animal care mini-games

## Technical Implementation

### Animal Class
```python
class Animal:
    - Position and movement
    - Animal type and behavior
    - Boundary constraints
    - Sprite rendering
    - Sound/interaction text
```

### FarmAnimals Manager
```python
class FarmAnimals:
    - Manages all farm animals
    - Updates animal AI each frame
    - Handles rendering and interactions
    - Creates animals for farm biome
```

## Sprite System Integration

### Animal Sprites
- Located in `sprites/animals/` directory
- Named as `animal_[type].png` (e.g., `animal_cow.png`)
- 32x32 pixel size for consistency
- Fallback to colored rectangles if sprites missing

### Special Sprite Features
- **Cows**: Black base with white spots
- **Chickens**: White with orange beak and red comb
- **Other animals**: Solid colors with borders

## Farm Layout

### Animal Areas
- **Cow Pasture**: Near the barn (coordinates 22-26, 20-24)
- **Pig Pen**: South area (coordinates 16-19, 24-26)  
- **Chicken Area**: Around farm buildings (coordinates 17-25, 17-25)
- **Sheep Field**: Separate eastern field (coordinates 26-30, 18-22)

### World Integration
- Animals only appear when spawning in farm biome
- Integrated with existing NPC and world systems
- Proper collision detection with terrain
- Minimap integration possible (future feature)

## Performance Optimization

### Efficient Rendering
- Only draw animals when on screen
- Sprite caching for better performance
- Minimal AI calculations per frame

### Memory Management
- Shared sprite manager across all animals
- Efficient boundary checking
- Optimized collision detection

## Future Enhancements

### Planned Features
- **Animal feeding**: Use crops to feed animals
- **Resource collection**: Milk from cows, eggs from chickens
- **Animal happiness**: Care affects animal productivity
- **Breeding system**: Animals can reproduce
- **Seasonal behaviors**: Different patterns in different seasons

### Advanced AI
- **Flocking behavior**: Animals group together
- **Following player**: Tamed animals follow you
- **Day/night cycles**: Different behaviors at different times
- **Weather reactions**: Animals seek shelter in rain

### Economic Integration
- **Animal products**: Sell milk, eggs, wool
- **Market prices**: Dynamic pricing for animal goods
- **Trading system**: Trade animals between biomes
- **Farm management**: Upgrade pastures and facilities

## Customization

### Adding New Animals
1. Add new animal type to `animals.py`
2. Create sprite in `sprites/animals/animal_[type].png`
3. Define behavior parameters
4. Add to farm biome spawn list
5. Update interaction sounds

### Modifying Behavior
- Edit movement speeds in `_get_animal_behavior()`
- Adjust rest frequencies for different activity levels
- Modify boundary areas in `create_farm_animals()`
- Customize sounds in `_get_animal_sounds()`

## Tips for Players

### Best Practices
- **Visit the farm biome** to see all the animals
- **Walk around different pasture areas** to find all animal types
- **Interact with animals** to hear their unique sounds
- **Watch their movement patterns** - each type behaves differently

### Discovery
- Animals are only in the farm biome currently
- Each animal stays in its designated area
- Animals move independently with realistic AI
- Future biomes may have different animal types

The animals system adds life and personality to the farm, making it feel like a real working farm with living creatures! 