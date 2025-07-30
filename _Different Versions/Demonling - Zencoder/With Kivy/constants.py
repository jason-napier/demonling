"""
Game Constants - Configuration values and game balance
"""

# Player starting values
STARTING_GOLD = 10
STARTING_SOUL_SHARDS = 5
STARTING_ENERGY = 10
MAX_ENERGY = 20

# Energy system
ENERGY_REGEN_TIME = 300  # 5 minutes in seconds
ENERGY_REFILL_COST = 5   # Soul shards cost for full refill

# Base player stats
BASE_HEALTH = 20
BASE_ATTACK = 5
BASE_DEFENSE = 2
BASE_AGILITY = 3
BASE_MAGIC = 1

# Stat growth per level
HEALTH_PER_LEVEL = 5
ATTACK_PER_LEVEL = 2
DEFENSE_PER_LEVEL = 1
AGILITY_PER_LEVEL = 1
MAGIC_PER_LEVEL = 1

# Experience system
XP_BASE = 100
XP_MULTIPLIER = 1.5

# UI Colors (RGB values normalized to 0-1)
COLOR_PRIMARY = (0.2, 0.1, 0.3, 1)      # Dark purple
COLOR_SECONDARY = (0.4, 0.2, 0.2, 1)    # Dark red
COLOR_ACCENT = (0.8, 0.2, 0.2, 1)       # Bright red
COLOR_SUCCESS = (0.2, 0.6, 0.2, 1)      # Green
COLOR_WARNING = (0.8, 0.6, 0.2, 1)      # Orange
COLOR_DANGER = (0.8, 0.2, 0.2, 1)       # Red
COLOR_TEXT = (0.9, 0.9, 0.9, 1)         # Light gray
COLOR_TEXT_DARK = (0.3, 0.3, 0.3, 1)    # Dark gray
COLOR_BACKGROUND = (0.1, 0.1, 0.1, 1)   # Very dark gray

# UI Dimensions
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 200
MARGIN = 10
PADDING = 5

# Screen sizes (for responsive design)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Combat constants
DEFEND_DAMAGE_REDUCTION = 0.5  # 50% damage reduction when defending
CRITICAL_HIT_CHANCE = 0.05     # 5% chance for critical hit
CRITICAL_HIT_MULTIPLIER = 1.5  # 1.5x damage for critical hits

# Quest constants
MAX_QUEST_HISTORY = 50  # Maximum number of quest completions to track

# Save file
SAVE_FILE = "demonling_save.json"

# Feature unlock levels
FEATURE_UNLOCK_LEVELS = {
    'first_special_ability': 5,
    'second_special_ability': 10,
    'third_special_ability': 15,
    'first_passive_ability': 20,
    'second_passive_ability': 25,
    'third_passive_ability': 30,
    'minions': 1,  # Unlocked by completing Ash & Bone chain
    'castle': 15,
    'dungeon': 25
}

# Audio settings
MUSIC_VOLUME = 0.7
SOUND_VOLUME = 0.8

# Animation settings
ANIMATION_SPEED = 0.3
FADE_DURATION = 0.2

# Version info
GAME_VERSION = "1.0.0"
GAME_BUILD = "MVP"