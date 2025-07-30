"""
Player class - Handles player stats, progression, and abilities
"""

import math
from constants import *

class Player:
    """Player character with stats and progression"""
    
    def __init__(self):
        # Core stats
        self.level = 1
        self.xp = 0
        self.gold = STARTING_GOLD
        self.soul_shards = STARTING_SOUL_SHARDS
        
        # Energy system
        self.energy = STARTING_ENERGY
        self.max_energy = MAX_ENERGY
        
        # Combat stats
        self.base_health = BASE_HEALTH
        self.base_attack = BASE_ATTACK
        self.base_defense = BASE_DEFENSE
        self.base_agility = BASE_AGILITY
        self.base_magic = BASE_MAGIC
        
        # Current health (for combat)
        self.current_health = self.health
        
        # Equipment and abilities (MVP+ features)
        self.equipped_items = []
        self.special_abilities = []
        self.passive_abilities = []
        
        # Unlocked features
        self.unlocked_features = set()
    
    @property
    def health(self):
        """Calculate total health including level bonuses"""
        return self.base_health + (self.level - 1) * HEALTH_PER_LEVEL
    
    @property
    def attack(self):
        """Calculate total attack including level bonuses"""
        return self.base_attack + (self.level - 1) * ATTACK_PER_LEVEL
    
    @property
    def defense(self):
        """Calculate total defense including level bonuses"""
        return self.base_defense + (self.level - 1) * DEFENSE_PER_LEVEL
    
    @property
    def agility(self):
        """Calculate total agility including level bonuses"""
        return self.base_agility + (self.level - 1) * AGILITY_PER_LEVEL
    
    @property
    def magic(self):
        """Calculate total magic including level bonuses"""
        return self.base_magic + (self.level - 1) * MAGIC_PER_LEVEL
    
    def xp_to_next_level(self):
        """Calculate XP needed for next level"""
        return self.xp_required_for_level(self.level + 1) - self.xp
    
    def xp_required_for_level(self, level):
        """Calculate total XP required for a given level"""
        if level <= 1:
            return 0
        return int(XP_BASE * (level - 1) * XP_MULTIPLIER)
    
    def add_xp(self, amount):
        """Add XP and handle level ups"""
        self.xp += amount
        
        # Check for level up
        while self.xp >= self.xp_required_for_level(self.level + 1):
            self.level_up()
    
    def level_up(self):
        """Handle level up"""
        self.level += 1
        
        # Restore health on level up
        self.current_health = self.health
        
        # Unlock features at specific levels
        if self.level == 5:
            self.unlocked_features.add('first_special_ability')
        elif self.level == 10:
            self.unlocked_features.add('second_special_ability')
        elif self.level == 15:
            self.unlocked_features.add('third_special_ability')
        elif self.level == 20:
            self.unlocked_features.add('first_passive_ability')
    
    def add_gold(self, amount):
        """Add gold"""
        self.gold += amount
    
    def spend_gold(self, amount):
        """Spend gold if available"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def add_soul_shards(self, amount):
        """Add soul shards"""
        self.soul_shards += amount
    
    def spend_soul_shards(self, amount):
        """Spend soul shards if available"""
        if self.soul_shards >= amount:
            self.soul_shards -= amount
            return True
        return False
    
    def add_energy(self, amount):
        """Add energy up to maximum"""
        self.energy = min(self.max_energy, self.energy + amount)
    
    def spend_energy(self, amount):
        """Spend energy if available"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def has_energy(self, amount):
        """Check if player has enough energy"""
        return self.energy >= amount
    
    def heal(self, amount):
        """Heal player"""
        self.current_health = min(self.health, self.current_health + amount)
    
    def take_damage(self, amount):
        """Take damage"""
        damage = max(1, amount - self.defense)
        self.current_health = max(0, self.current_health - damage)
        return damage
    
    def is_alive(self):
        """Check if player is alive"""
        return self.current_health > 0
    
    def reset_health(self):
        """Reset health to maximum"""
        self.current_health = self.health
    
    def get_combat_stats(self):
        """Get stats for combat display"""
        return {
            'current_health': self.current_health,
            'max_health': self.health,
            'attack': self.attack,
            'defense': self.defense,
            'agility': self.agility,
            'magic': self.magic
        }
    
    def can_use_special_ability(self, ability_index):
        """Check if player can use a special ability"""
        if ability_index == 0:
            return 'first_special_ability' in self.unlocked_features
        elif ability_index == 1:
            return 'second_special_ability' in self.unlocked_features
        elif ability_index == 2:
            return 'third_special_ability' in self.unlocked_features
        return False
    
    def to_dict(self):
        """Convert player to dictionary for saving"""
        return {
            'level': self.level,
            'xp': self.xp,
            'gold': self.gold,
            'soul_shards': self.soul_shards,
            'energy': self.energy,
            'max_energy': self.max_energy,
            'base_health': self.base_health,
            'base_attack': self.base_attack,
            'base_defense': self.base_defense,
            'base_agility': self.base_agility,
            'base_magic': self.base_magic,
            'current_health': self.current_health,
            'equipped_items': self.equipped_items,
            'special_abilities': self.special_abilities,
            'passive_abilities': self.passive_abilities,
            'unlocked_features': list(self.unlocked_features)
        }
    
    def from_dict(self, data):
        """Load player from dictionary"""
        self.level = data.get('level', 1)
        self.xp = data.get('xp', 0)
        self.gold = data.get('gold', STARTING_GOLD)
        self.soul_shards = data.get('soul_shards', STARTING_SOUL_SHARDS)
        self.energy = data.get('energy', STARTING_ENERGY)
        self.max_energy = data.get('max_energy', MAX_ENERGY)
        self.base_health = data.get('base_health', BASE_HEALTH)
        self.base_attack = data.get('base_attack', BASE_ATTACK)
        self.base_defense = data.get('base_defense', BASE_DEFENSE)
        self.base_agility = data.get('base_agility', BASE_AGILITY)
        self.base_magic = data.get('base_magic', BASE_MAGIC)
        self.current_health = data.get('current_health', self.health)
        self.equipped_items = data.get('equipped_items', [])
        self.special_abilities = data.get('special_abilities', [])
        self.passive_abilities = data.get('passive_abilities', [])
        self.unlocked_features = set(data.get('unlocked_features', []))