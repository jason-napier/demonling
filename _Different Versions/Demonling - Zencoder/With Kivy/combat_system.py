"""
Combat System - Handles turn-based combat mechanics
"""

import random
from enum import Enum
from typing import Optional, List, Dict, Tuple
from kivy.event import EventDispatcher
from kivy.logger import Logger

class CombatAction(Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    USE_ITEM = "use_item"
    SPECIAL_ABILITY = "special_ability"

class CombatState(Enum):
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    COMBAT_END = "combat_end"

class CombatManager(EventDispatcher):
    """Manages combat encounters"""
    
    def __init__(self):
        super().__init__()
        self.player = None
        self.enemy = None
        self.combat_state = CombatState.COMBAT_END
        self.turn_count = 0
        self.combat_log = []
        self.player_defending = False
        
        # Register events
        self.register_event_type('on_combat_start')
        self.register_event_type('on_combat_end')
        self.register_event_type('on_player_turn')
        self.register_event_type('on_enemy_turn')
        self.register_event_type('on_damage_dealt')
        self.register_event_type('on_combat_log')
    
    def start_combat(self, player, enemy):
        """Start combat encounter"""
        self.player = player
        self.enemy = enemy
        self.combat_state = CombatState.PLAYER_TURN
        self.turn_count = 0
        self.combat_log = []
        self.player_defending = False
        
        # Reset enemy health
        self.enemy.reset_health()
        
        # Ensure player health is set
        if self.player.current_health <= 0:
            self.player.reset_health()
        
        self.add_to_log(f"Combat begins! {self.player.level} vs {self.enemy.name}")
        self.add_to_log(f"Player: {self.player.current_health}/{self.player.health} HP")
        self.add_to_log(f"Enemy: {self.enemy.current_health}/{self.enemy.health} HP")
        
        Logger.info(f"Combat: Started combat against {self.enemy.name}")
        self.dispatch('on_combat_start')
        self.dispatch('on_player_turn')
    
    def player_action(self, action: CombatAction, target=None):
        """Handle player action"""
        if self.combat_state != CombatState.PLAYER_TURN:
            return False
        
        if action == CombatAction.ATTACK:
            self._player_attack()
        elif action == CombatAction.DEFEND:
            self._player_defend()
        elif action == CombatAction.USE_ITEM:
            self._player_use_item(target)
        elif action == CombatAction.SPECIAL_ABILITY:
            self._player_special_ability(target)
        
        # Check if enemy is defeated
        if not self.enemy.is_alive():
            self._end_combat(victory=True)
            return True
        
        # Switch to enemy turn
        self.combat_state = CombatState.ENEMY_TURN
        self.dispatch('on_enemy_turn')
        
        # Process enemy turn automatically after a short delay
        self._enemy_turn()
        
        return True
    
    def _player_attack(self):
        """Player attacks enemy"""
        damage = self._calculate_damage(self.player.attack, self.enemy.defense)
        actual_damage = self.enemy.take_damage(damage)
        
        self.add_to_log(f"Player attacks for {actual_damage} damage!")
        self.dispatch('on_damage_dealt', 'player', actual_damage)
        
        Logger.info(f"Combat: Player dealt {actual_damage} damage to {self.enemy.name}")
    
    def _player_defend(self):
        """Player defends"""
        self.player_defending = True
        self.add_to_log("Player takes a defensive stance!")
        Logger.info("Combat: Player is defending")
    
    def _player_use_item(self, item_index):
        """Player uses item (MVP+ feature)"""
        # Placeholder for item usage
        self.add_to_log("Player uses an item! (Not yet implemented)")
        Logger.info("Combat: Player used item")
    
    def _player_special_ability(self, ability_index):
        """Player uses special ability (MVP+ feature)"""
        if not self.player.can_use_special_ability(ability_index):
            self.add_to_log("Special ability not available!")
            return
        
        # Placeholder for special abilities
        if ability_index == 0:
            # Fireball - extra damage
            damage = self._calculate_damage(self.player.magic + 5, self.enemy.defense)
            actual_damage = self.enemy.take_damage(damage)
            self.add_to_log(f"Player casts Fireball for {actual_damage} damage!")
        elif ability_index == 1:
            # Heal - restore health
            heal_amount = self.player.magic + 10
            self.player.heal(heal_amount)
            self.add_to_log(f"Player heals for {heal_amount} HP!")
        elif ability_index == 2:
            # Stun - enemy skips next turn (placeholder)
            self.add_to_log("Player casts Stun! Enemy is dazed!")
        
        Logger.info(f"Combat: Player used special ability {ability_index}")
    
    def _enemy_turn(self):
        """Process enemy turn"""
        if self.combat_state != CombatState.ENEMY_TURN:
            return
        
        # Simple AI: always attack
        self._enemy_attack()
        
        # Check if player is defeated
        if not self.player.is_alive():
            self._end_combat(victory=False)
            return
        
        # Reset defending status
        self.player_defending = False
        
        # Switch back to player turn
        self.turn_count += 1
        self.combat_state = CombatState.PLAYER_TURN
        self.dispatch('on_player_turn')
    
    def _enemy_attack(self):
        """Enemy attacks player"""
        base_damage = self._calculate_damage(self.enemy.attack, self.player.defense)
        
        # Apply defend bonus
        if self.player_defending:
            base_damage = max(1, base_damage // 2)
            self.add_to_log(f"Player's defense reduces damage!")
        
        actual_damage = self.player.take_damage(base_damage)
        self.add_to_log(f"{self.enemy.name} attacks for {actual_damage} damage!")
        self.dispatch('on_damage_dealt', 'enemy', actual_damage)
        
        Logger.info(f"Combat: {self.enemy.name} dealt {actual_damage} damage to player")
    
    def _calculate_damage(self, attack: int, defense: int) -> int:
        """Calculate damage with some randomness"""
        base_damage = max(1, attack - defense)
        # Add ±20% randomness
        variance = random.uniform(0.8, 1.2)
        return max(1, int(base_damage * variance))
    
    def _end_combat(self, victory: bool):
        """End combat encounter"""
        self.combat_state = CombatState.COMBAT_END
        
        if victory:
            self.add_to_log(f"Victory! {self.enemy.name} is defeated!")
            Logger.info(f"Combat: Player defeated {self.enemy.name}")
        else:
            self.add_to_log("Defeat! You have been bested...")
            Logger.info(f"Combat: Player defeated by {self.enemy.name}")
        
        self.dispatch('on_combat_end', victory)
    
    def add_to_log(self, message: str):
        """Add message to combat log"""
        self.combat_log.append(message)
        self.dispatch('on_combat_log', message)
        
        # Keep log size manageable
        if len(self.combat_log) > 20:
            self.combat_log.pop(0)
    
    def get_combat_state(self) -> Dict:
        """Get current combat state for UI"""
        if not self.player or not self.enemy:
            return {}
        
        return {
            'player_health': self.player.current_health,
            'player_max_health': self.player.health,
            'enemy_health': self.enemy.current_health,
            'enemy_max_health': self.enemy.health,
            'player_attack': self.player.attack,
            'player_defense': self.player.defense,
            'enemy_attack': self.enemy.attack,
            'enemy_defense': self.enemy.defense,
            'enemy_name': self.enemy.name,
            'turn_count': self.turn_count,
            'combat_state': self.combat_state.value,
            'combat_log': self.combat_log.copy(),
            'player_defending': self.player_defending
        }
    
    def can_use_special_ability(self, ability_index: int) -> bool:
        """Check if player can use special ability"""
        return self.player and self.player.can_use_special_ability(ability_index)
    
    # Event handlers
    def on_combat_start(self):
        """Handle combat start event"""
        pass
    
    def on_combat_end(self, victory):
        """Handle combat end event"""
        pass
    
    def on_player_turn(self):
        """Handle player turn event"""
        pass
    
    def on_enemy_turn(self):
        """Handle enemy turn event"""
        pass
    
    def on_damage_dealt(self, source, damage):
        """Handle damage dealt event"""
        pass
    
    def on_combat_log(self, message):
        """Handle combat log event"""
        pass