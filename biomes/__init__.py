# Biomes package for Ernie's Adventure
# Each biome is in its own file for collaborative development

from .farm_biome import create_farming_section
from .forest_biome import create_forest_section
from .lake_biome import create_lake_section
from .mountain_biome import create_mountain_section
from .crossroads_biome import create_crossroads_section
from .ruins_biome import create_ruins_section
from .southern_biome import create_southern_section
from .world_features import create_connecting_paths, create_random_features

__all__ = [
    'create_farming_section',
    'create_forest_section', 
    'create_lake_section',
    'create_mountain_section',
    'create_crossroads_section',
    'create_ruins_section',
    'create_southern_section',
    'create_connecting_paths',
    'create_random_features'
] 