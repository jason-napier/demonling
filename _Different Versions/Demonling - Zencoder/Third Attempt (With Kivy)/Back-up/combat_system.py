"""
Combat System Module

This module implements the turn-based combat system for Demonling.
It handles player vs enemy combat with attack, defend, and special abilities.
"""

import random
from kivy.logger import Logger

class CombatEntity:
    """
    Base class for entities that can participate in combat.
    This includes both players and enemies.
    """
    
    def __init__(self, name, attack, defense, agility, magic, max_health):
        """
        Initialize a combat entity.
        
        Args:
            name (str): Name of the entity
            attack (int): Base attack power
            defense (int): Defense value
            agility (int): Agility for dodge/crit chances
            magic (int): Magic power for special abilities
            max_health (int): Maximum health points
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.magic = magic
        self.max_health = max_health
        self.current_health = max_health
        
        # Combat state
        self.defending = False
        self.status_effects = {}  # For future use (poison, stun, etc.)
        
        Logger.info(f"Combat: Created entity {name} with {max_health} HP")
        
    def take_damage(self, damage):
        """
        Apply damage to this entity.
        
        Args:
            damage (int): Amount of damage to take
            
        Returns:
            int: Actual damage taken
        """
        # Apply defense reduction
        effective_damage = max(1, damage - self.defense)
        
        # Apply defending bonus
        if self.defending:
            effective_damage = max(1, effective_damage // 2)
            
        # Apply damage
        self.current_health = max(0, self.current_health - effective_damage)
        
        Logger.info(f"Combat: {self.name} took {effective_damage} damage ({self.current_health}/{self.max_health} HP)")
        return effective_damage
        
    def is_alive(self):
        """Check if entity is still alive"""
        return self.current_health > 0
        
    def reset_combat_state(self):
        """Reset temporary combat state"""
        self.defending = False
        self.status_effects.clear()

class Enemy(CombatEntity):
    """
    Enemy class that extends CombatEntity with AI behavior.
    """
    
    def __init__(self, enemy_data):
        """
        Initialize enemy from data dictionary.
        
        Args:
            enemy_data (dict): Dictionary containing enemy stats
        """
        super().__init__(
            enemy_data['name'],
            enemy_data['attack'],
            enemy_data['defense'],
            enemy_data['agility'],
            enemy_data['magic'],
            enemy_data['health']
        )
        
        self.enemy_type = enemy_data.get('type', 'normal')
        self.special_abilities = enemy_data.get('abilities', [])
        self.ai_behavior = enemy_data.get('ai_behavior', 'aggressive')
        
    def choose_action(self):
        """
        AI chooses an action based on behavior pattern.
        
        Returns:
            str: Action to take ('attack', 'defend', 'special')
        """
        # Simple AI for MVP - mostly attacks
        if self.ai_behavior == 'aggressive':
            return 'attack'
        elif self.ai_behavior == 'defensive':
            # Defend if health is low
            if self.current_health < self.max_health * 0.3:
                return 'defend'
            else:
                return 'attack'
        else:
            # Balanced approach
            if self.current_health < self.max_health * 0.5:
                return random.choice(['attack', 'defend'])
            else:
                return 'attack'

class PlayerCombatWrapper:
    """
    Wrapper class to make Player compatible with combat system.
    """
    
    def __init__(self, player):
        """
        Initialize wrapper around player object.
        
        Args:
            player (Player): Player object from game_manager
        """
        self.player = player
        self.name = "Player"
        self.defending = False
        self.status_effects = {}
        
    @property
    def attack(self):
        return self.player.attack
        
    @property
    def defense(self):
        return self.player.defense
        
    @property
    def agility(self):
        return self.player.agility
        
    @property
    def magic(self):
        return self.player.magic
        
    @property
    def max_health(self):
        return self.player.max_health
        
    @property
    def current_health(self):
        return self.player.current_health
        
    def take_damage(self, damage):
        """Apply damage to player"""
        # Apply defense reduction
        effective_damage = max(1, damage - self.defense)
        
        # Apply defending bonus
        if self.defending:
            effective_damage = max(1, effective_damage // 2)
            
        # Apply damage through player object
        self.player.take_damage(effective_damage)
        
        Logger.info(f"Combat: Player took {effective_damage} damage")
        return effective_damage
        
    def is_alive(self):
        """Check if player is alive"""
        return self.player.current_health > 0
        
    def reset_combat_state(self):
        """Reset combat state"""
        self.defending = False
        self.status_effects.clear()

class CombatSystem:
    """
    Main combat system that manages battles between player and enemies.
    """
    
    def __init__(self, player, enemy_data):
        """
        Initialize combat system.
        
        Args:
            player (Player): Player object
            enemy_data (dict): Enemy data dictionary
        """
        self.player = PlayerCombatWrapper(player)
        self.enemy = Enemy(enemy_data)
        
        # Combat state
        self.turn_count = 0
        self.combat_active = True
        self.combat_log = []
        
        Logger.info(f"Combat: Battle started between Player and {self.enemy.name}")
        
    def player_attack(self):
        """
        Execute player attack action.
        
        Returns:
            int: Damage dealt to enemy
        """
        if not self.combat_active:
            return 0
            
        # Reset defending state
        self.player.defending = False
        
        # Calculate damage
        base_damage = self.player.attack
        
        # Add some randomness (±20%)
        damage_variance = random.randint(-20, 20) / 100
        damage = int(base_damage * (1 + damage_variance))
        damage = max(1, damage)  # Minimum 1 damage
        
        # Apply damage to enemy
        actual_damage = self.enemy.take_damage(damage)
        
        # Add to combat log
        self.combat_log.append(f"Player attacks for {actual_damage} damage!")
        
        # Check if enemy is defeated
        if not self.enemy.is_alive():
            self.combat_active = False
            self.combat_log.append(f"{self.enemy.name} has been defeated!")
            
        return actual_damage
        
    def player_defend(self):
        """Execute player defend action"""
        if not self.combat_active:
            return
            
        self.player.defending = True
        self.combat_log.append("Player takes a defensive stance!")
        
    def enemy_attack(self):
        """
        Execute enemy attack action.
        
        Returns:
            int: Damage dealt to player
        """
        if not self.combat_active:
            return 0
            
        # Reset enemy defending state
        self.enemy.defending = False
        
        # Enemy chooses action
        action = self.enemy.choose_action()
        
        if action == 'defend':
            self.enemy.defending = True
            self.combat_log.append(f"{self.enemy.name} takes a defensive stance!")
            return 0
        else:
            # Attack
            base_damage = self.enemy.attack
            
            # Add some randomness (±20%)
            damage_variance = random.randint(-20, 20) / 100
            damage = int(base_damage * (1 + damage_variance))
            damage = max(1, damage)  # Minimum 1 damage
            
            # Apply damage to player
            actual_damage = self.player.take_damage(damage)
            
            # Add to combat log
            self.combat_log.append(f"{self.enemy.name} attacks for {actual_damage} damage!")
            
            # Check if player is defeated
            if not self.player.is_alive():
                self.combat_active = False
                self.combat_log.append("Player has been defeated!")
                
            return actual_damage
            
    def is_combat_over(self):
        """Check if combat has ended"""
        return not self.combat_active or not self.player.is_alive() or not self.enemy.is_alive()
        
    def get_winner(self):
        """
        Get the winner of the combat.
        
        Returns:
            str: 'player', 'enemy', or 'ongoing'
        """
        if not self.is_combat_over():
            return 'ongoing'
        elif self.player.is_alive():
            return 'player'
        else:
            return 'enemy'
            
    def get_combat_log(self):
        """Get the combat log messages"""
        return self.combat_log.copy()
        
    def reset_combat_states(self):
        """Reset temporary combat states"""
        self.player.reset_combat_state()
        self.enemy.reset_combat_state()

class CombatSystemAdvanced(CombatSystem):
    """
    Advanced combat system with items, special abilities, and passive effects.
    This is for Phase 2 of combat development.
    """
    
    def __init__(self, player, enemy_data):
        """Initialize advanced combat system"""
        super().__init__(player, enemy_data)
        
        # Additional combat features
        self.special_abilities_used = []
        self.items_used = []
        self.passive_effects_active = []
        
    def use_item(self, item_slot):
        """
        Use an item from player inventory.
        
        Args:
            item_slot (int): Item slot number (1-3)
            
        Returns:
            bool: True if item was used successfully
        """
        # TODO: Implement item system
        # For now, return False as items aren't implemented
        return False
        
    def use_special_ability(self, ability_slot):
        """
        Use a special ability.
        
        Args:
            ability_slot (int): Ability slot number (1-3)
            
        Returns:
            bool: True if ability was used successfully
        """
        # TODO: Implement special ability system
        # For now, return False as abilities aren't implemented
        return False
        
    def apply_passive_effects(self):
        """Apply any passive effects at the start of turn"""
        # TODO: Implement passive effects
        # For now, do nothing
        pass
        
    def calculate_critical_hit(self, attacker):
        """
        Calculate if an attack is a critical hit.
        
        Args:
            attacker (CombatEntity): The attacking entity
            
        Returns:
            bool: True if critical hit
        """
        # Critical hit chance based on agility
        crit_chance = min(0.2, attacker.agility / 100)  # Max 20% crit chance
        return random.random() < crit_chance
        
    def calculate_dodge(self, defender):
        """
        Calculate if an attack is dodged.
        
        Args:
            defender (CombatEntity): The defending entity
            
        Returns:
            bool: True if attack was dodged
        """
        # Dodge chance based on agility
        dodge_chance = min(0.15, defender.agility / 150)  # Max 15% dodge chance
        return random.random() < dodge_chance

# Combat utility functions
def create_enemy_from_template(enemy_type, level_modifier=0):
    """
    Create an enemy from a template with level scaling.
    
    Args:
        enemy_type (str): Type of enemy to create
        level_modifier (int): Level modifier for scaling
        
    Returns:
        dict: Enemy data dictionary
    """
    enemy_templates = {
        'goblin': {
            'name': 'Goblin',
            'attack': 8,
            'defense': 3,
            'agility': 5,
            'magic': 1,
            'health': 80,
            'type': 'normal',
            'ai_behavior': 'aggressive'
        },
        'orc': {
            'name': 'Orc',
            'attack': 12,
            'defense': 6,
            'agility': 2,
            'magic': 1,
            'health': 120,
            'type': 'normal',
            'ai_behavior': 'aggressive'
        },
        'skeleton': {
            'name': 'Skeleton',
            'attack': 10,
            'defense': 4,
            'agility': 4,
            'magic': 2,
            'health': 90,
            'type': 'undead',
            'ai_behavior': 'balanced'
        },
        'demon': {
            'name': 'Lesser Demon',
            'attack': 15,
            'defense': 8,
            'agility': 6,
            'magic': 10,
            'health': 150,
            'type': 'demon',
            'ai_behavior': 'balanced'
        }
    }
    
    if enemy_type not in enemy_templates:
        enemy_type = 'goblin'  # Default fallback
        
    enemy_data = enemy_templates[enemy_type].copy()
    
    # Apply level scaling
    if level_modifier > 0:
        enemy_data['attack'] += level_modifier * 2
        enemy_data['defense'] += level_modifier
        enemy_data['agility'] += level_modifier
        enemy_data['magic'] += level_modifier
        enemy_data['health'] += level_modifier * 10
        enemy_data['name'] = f"Level {level_modifier + 1} {enemy_data['name']}"
        
    return enemy_data