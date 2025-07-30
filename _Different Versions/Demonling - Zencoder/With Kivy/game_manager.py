"""
Game Manager - Central hub for game state and logic
"""

import time
import json
from kivy.logger import Logger
from kivy.event import EventDispatcher

from player import Player
from quest_system import QuestManager
from combat_system import CombatManager
from data_persistence import DataManager
from constants import *

class GameManager(EventDispatcher):
    """Central game manager that coordinates all game systems"""
    
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.quest_manager = QuestManager()
        self.combat_manager = CombatManager()
        self.data_manager = DataManager()
        
        # Game state
        self.current_quest = None
        self.current_enemy = None
        self.last_energy_update = time.time()
        
        # Register for events
        self.register_event_type('on_level_up')
        self.register_event_type('on_quest_complete')
        self.register_event_type('on_combat_end')
        self.register_event_type('on_energy_full')
        
    def update_energy(self):
        """Update energy based on time passed"""
        current_time = time.time()
        time_passed = current_time - self.last_energy_update
        
        if time_passed >= ENERGY_REGEN_TIME:
            energy_to_add = int(time_passed // ENERGY_REGEN_TIME)
            old_energy = self.player.energy
            self.player.add_energy(energy_to_add)
            
            if old_energy < self.player.max_energy and self.player.energy >= self.player.max_energy:
                self.dispatch('on_energy_full')
            
            self.last_energy_update = current_time
    
    def start_quest(self, quest_id):
        """Start a quest"""
        quest = self.quest_manager.get_quest(quest_id)
        if not quest:
            Logger.error(f"GameManager: Quest {quest_id} not found")
            return False
        
        if not self.quest_manager.can_start_quest(quest_id, self.player):
            Logger.info(f"GameManager: Cannot start quest {quest_id}")
            return False
        
        # Check energy cost
        if self.player.energy < quest.energy_cost:
            Logger.info(f"GameManager: Not enough energy for quest {quest_id}")
            return False
        
        self.current_quest = quest
        self.player.spend_energy(quest.energy_cost)
        
        # Start combat if quest has enemy
        if quest.enemy:
            self.current_enemy = quest.enemy
            return self.start_combat()
        else:
            # No combat, just complete quest
            return self.complete_quest(True)
    
    def start_combat(self):
        """Start combat with current enemy"""
        if not self.current_enemy:
            return False
        
        # Reset player health for combat
        self.player.current_health = self.player.health
        
        # Initialize combat
        self.combat_manager.start_combat(self.player, self.current_enemy)
        return True
    
    def complete_quest(self, victory=True):
        """Complete current quest"""
        if not self.current_quest:
            return False
        
        quest = self.current_quest
        
        if victory:
            # Grant rewards
            old_level = self.player.level
            self.player.add_xp(quest.xp_reward)
            self.player.add_gold(quest.gold_reward)
            
            # First-time completion rewards soul shard
            if not self.quest_manager.is_quest_completed(quest.id):
                self.player.add_soul_shards(quest.soul_shard_reward)
            
            # Mark quest as completed
            self.quest_manager.complete_quest(quest.id)
            
            # Check for level up
            if self.player.level > old_level:
                self.dispatch('on_level_up', self.player.level)
            
            # Unlock next quest in chain
            self.quest_manager.unlock_next_quest(quest.id)
            
            Logger.info(f"GameManager: Quest {quest.id} completed successfully")
            self.dispatch('on_quest_complete', quest.id, True)
        else:
            Logger.info(f"GameManager: Quest {quest.id} failed")
            self.dispatch('on_quest_complete', quest.id, False)
        
        # Reset quest state
        self.current_quest = None
        self.current_enemy = None
        
        return True
    
    def can_afford_energy_refill(self):
        """Check if player can afford energy refill"""
        return self.player.soul_shards >= ENERGY_REFILL_COST
    
    def refill_energy(self):
        """Refill player energy using soul shards"""
        if self.can_afford_energy_refill():
            self.player.spend_soul_shards(ENERGY_REFILL_COST)
            self.player.energy = self.player.max_energy
            return True
        return False
    
    def get_player_stats(self):
        """Get formatted player stats"""
        return {
            'level': self.player.level,
            'xp': self.player.xp,
            'xp_to_next': self.player.xp_to_next_level(),
            'gold': self.player.gold,
            'soul_shards': self.player.soul_shards,
            'energy': self.player.energy,
            'max_energy': self.player.max_energy,
            'health': self.player.health,
            'attack': self.player.attack,
            'defense': self.player.defense,
            'agility': self.player.agility,
            'magic': self.player.magic
        }
    
    def get_available_quests(self):
        """Get list of available quests"""
        return self.quest_manager.get_available_quests(self.player)
    
    def save_game(self):
        """Save game state"""
        game_data = {
            'player': self.player.to_dict(),
            'quest_progress': self.quest_manager.get_progress(),
            'last_energy_update': self.last_energy_update,
            'timestamp': time.time()
        }
        
        self.data_manager.save_game(game_data)
        Logger.info("GameManager: Game saved successfully")
    
    def load_game(self):
        """Load game state"""
        game_data = self.data_manager.load_game()
        
        if game_data:
            # Load player data
            if 'player' in game_data:
                self.player.from_dict(game_data['player'])
            
            # Load quest progress
            if 'quest_progress' in game_data:
                self.quest_manager.load_progress(game_data['quest_progress'])
            
            # Handle offline energy regeneration
            if 'timestamp' in game_data:
                offline_time = time.time() - game_data['timestamp']
                offline_energy = int(offline_time // ENERGY_REGEN_TIME)
                if offline_energy > 0:
                    self.player.add_energy(offline_energy)
                    Logger.info(f"GameManager: Added {offline_energy} energy from offline time")
            
            self.last_energy_update = time.time()
            Logger.info("GameManager: Game loaded successfully")
        else:
            Logger.info("GameManager: No save file found, starting new game")
    
    # Event handlers
    def on_level_up(self, level):
        """Handle level up event"""
        Logger.info(f"GameManager: Player leveled up to {level}")
    
    def on_quest_complete(self, quest_id, success):
        """Handle quest completion event"""
        pass
    
    def on_combat_end(self, victory):
        """Handle combat end event"""
        self.complete_quest(victory)
    
    def on_energy_full(self):
        """Handle energy full event"""
        Logger.info("GameManager: Energy is full")