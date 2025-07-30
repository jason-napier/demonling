"""
Game Manager Module

This module handles the core game logic, player state management,
and coordinates between different game systems.
"""

import json
import os
from datetime import datetime, timedelta
from kivy.logger import Logger

from quest_system import QuestSystem
from data_manager import DataManager

class Player:
    """
    Player class that manages all player-related data and stats.
    This includes level, experience, resources, and combat stats.
    """
    
    def __init__(self):
        """Initialize player with default starting values"""
        # Basic progression stats
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        
        # Resources
        self.gold = 0
        self.soul_shards = 0
        
        # Energy system
        self.energy = 100
        self.max_energy = 100
        self.energy_regen_rate = 1  # Energy per minute
        self.last_energy_update = datetime.now()
        
        # Combat stats
        self.attack = 10
        self.defense = 5
        self.agility = 3
        self.magic = 1
        
        # Health (calculated from level and defense)
        self.max_health = 100
        self.current_health = self.max_health
        
        # Equipment slots (for future use)
        self.equipment = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
        
        # Ability slots (for future use)
        self.abilities = {
            'special_1': None,
            'special_2': None,
            'special_3': None,
            'passive_1': None,
            'passive_2': None,
            'passive_3': None
        }
        
        # Items (for future use)
        self.items = {
            'item_1': None,
            'item_2': None,
            'item_3': None
        }
        
        Logger.info("Player: Initialized with default stats")
        
    def gain_xp(self, amount):
        """
        Add experience points and handle level ups.
        
        Args:
            amount (int): Amount of XP to gain
        """
        self.xp += amount
        Logger.info(f"Player: Gained {amount} XP (Total: {self.xp})")
        
        # Check for level up
        while self.xp >= self.xp_to_next_level:
            self.level_up()
            
    def level_up(self):
        """Handle player level up and stat increases"""
        self.xp -= self.xp_to_next_level
        self.level += 1
        
        # Calculate new XP requirement (increases by 20% each level)
        self.xp_to_next_level = int(self.xp_to_next_level * 1.2)
        
        # Increase stats based on level
        self.attack += 2
        self.defense += 1
        self.agility += 1
        self.magic += 1
        
        # Increase health and energy
        old_max_health = self.max_health
        self.max_health = 100 + (self.level - 1) * 10
        self.current_health += (self.max_health - old_max_health)  # Heal on level up
        
        self.max_energy = 100 + (self.level - 1) * 5
        
        Logger.info(f"Player: Level up! Now level {self.level}")
        
    def gain_gold(self, amount):
        """
        Add gold to player inventory.
        
        Args:
            amount (int): Amount of gold to gain
        """
        self.gold += amount
        Logger.info(f"Player: Gained {amount} gold (Total: {self.gold})")
        
    def gain_soul_shards(self, amount):
        """
        Add soul shards to player inventory.
        
        Args:
            amount (int): Amount of soul shards to gain
        """
        self.soul_shards += amount
        Logger.info(f"Player: Gained {amount} soul shards (Total: {self.soul_shards})")
        
    def spend_energy(self, amount):
        """
        Spend energy for actions like quests.
        
        Args:
            amount (int): Amount of energy to spend
            
        Returns:
            bool: True if energy was spent, False if insufficient
        """
        if self.energy >= amount:
            self.energy -= amount
            Logger.info(f"Player: Spent {amount} energy (Remaining: {self.energy})")
            return True
        else:
            Logger.info(f"Player: Insufficient energy (Need: {amount}, Have: {self.energy})")
            return False
            
    def update_energy(self):
        """
        Update energy based on time passed since last update.
        This enables offline energy regeneration.
        """
        now = datetime.now()
        time_diff = now - self.last_energy_update
        minutes_passed = time_diff.total_seconds() / 60
        
        # Calculate energy to regenerate
        energy_to_regen = int(minutes_passed * self.energy_regen_rate)
        
        if energy_to_regen > 0:
            old_energy = self.energy
            self.energy = min(self.max_energy, self.energy + energy_to_regen)
            self.last_energy_update = now
            
            if self.energy > old_energy:
                Logger.info(f"Player: Energy regenerated ({old_energy} -> {self.energy})")
                
    def heal(self, amount):
        """
        Heal player by specified amount.
        
        Args:
            amount (int): Amount to heal
        """
        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        
        if self.current_health > old_health:
            Logger.info(f"Player: Healed for {self.current_health - old_health} HP")
            
    def take_damage(self, amount):
        """
        Apply damage to player.
        
        Args:
            amount (int): Amount of damage to take
        """
        self.current_health = max(0, self.current_health - amount)
        Logger.info(f"Player: Took {amount} damage (Health: {self.current_health}/{self.max_health})")
        
    def reset_health(self):
        """Reset player health to maximum (used after combat)"""
        self.current_health = self.max_health
        
    def to_dict(self):
        """Convert player data to dictionary for saving"""
        return {
            'level': self.level,
            'xp': self.xp,
            'xp_to_next_level': self.xp_to_next_level,
            'gold': self.gold,
            'soul_shards': self.soul_shards,
            'energy': self.energy,
            'max_energy': self.max_energy,
            'energy_regen_rate': self.energy_regen_rate,
            'last_energy_update': self.last_energy_update.isoformat(),
            'attack': self.attack,
            'defense': self.defense,
            'agility': self.agility,
            'magic': self.magic,
            'max_health': self.max_health,
            'current_health': self.current_health,
            'equipment': self.equipment,
            'abilities': self.abilities,
            'items': self.items
        }
        
    def from_dict(self, data):
        """Load player data from dictionary"""
        self.level = data.get('level', 1)
        self.xp = data.get('xp', 0)
        self.xp_to_next_level = data.get('xp_to_next_level', 100)
        self.gold = data.get('gold', 0)
        self.soul_shards = data.get('soul_shards', 0)
        self.energy = data.get('energy', 100)
        self.max_energy = data.get('max_energy', 100)
        self.energy_regen_rate = data.get('energy_regen_rate', 1)
        
        # Parse last energy update time
        try:
            self.last_energy_update = datetime.fromisoformat(data.get('last_energy_update', datetime.now().isoformat()))
        except:
            self.last_energy_update = datetime.now()
            
        self.attack = data.get('attack', 10)
        self.defense = data.get('defense', 5)
        self.agility = data.get('agility', 3)
        self.magic = data.get('magic', 1)
        self.max_health = data.get('max_health', 100)
        self.current_health = data.get('current_health', self.max_health)
        self.equipment = data.get('equipment', {'weapon': None, 'armor': None, 'accessory': None})
        self.abilities = data.get('abilities', {
            'special_1': None, 'special_2': None, 'special_3': None,
            'passive_1': None, 'passive_2': None, 'passive_3': None
        })
        self.items = data.get('items', {'item_1': None, 'item_2': None, 'item_3': None})

class GameManager:
    """
    Main game manager that coordinates all game systems.
    Handles save/load, game state, and system interactions.
    """
    
    def __init__(self):
        """Initialize game manager and all subsystems"""
        Logger.info("GameManager: Initializing")
        
        # Initialize player
        self.player = Player()
        
        # Initialize subsystems
        self.quest_system = QuestSystem()
        self.data_manager = DataManager()
        
        # Game state
        self.current_quest_id = None
        self.game_started = False
        
        # Load saved game if it exists
        self.load_game()
        
        Logger.info("GameManager: Initialization complete")
        
    def start_new_game(self):
        """Start a new game with fresh player data"""
        Logger.info("GameManager: Starting new game")
        
        # Reset player to defaults
        self.player = Player()
        
        # Reset quest system
        self.quest_system.reset_progress()
        
        # Mark game as started
        self.game_started = True
        
        # Save initial state
        self.save_game()
        
    def complete_quest(self, quest_id):
        """
        Complete a quest and handle rewards.
        
        Args:
            quest_id (str): ID of the quest to complete
            
        Returns:
            dict: Rewards given to player
        """
        Logger.info(f"GameManager: Completing quest {quest_id}")
        
        # Get quest data
        quest_data = self.quest_system.get_quest_data(quest_id)
        if not quest_data:
            Logger.error(f"GameManager: Quest {quest_id} not found")
            return {}
            
        # Check if player has enough energy
        if not self.player.spend_energy(quest_data['energy_cost']):
            Logger.error(f"GameManager: Insufficient energy for quest {quest_id}")
            return {}
            
        # Mark quest as completed
        first_completion = self.quest_system.complete_quest(quest_id)
        
        # Calculate rewards
        rewards = {
            'xp': quest_data['xp_reward'],
            'gold': quest_data['gold_reward'],
            'soul_shards': quest_data['soul_shard_reward'] if first_completion else 0
        }
        
        # Give rewards to player
        self.player.gain_xp(rewards['xp'])
        self.player.gain_gold(rewards['gold'])
        if rewards['soul_shards'] > 0:
            self.player.gain_soul_shards(rewards['soul_shards'])
            
        # Reset player health after quest
        self.player.reset_health()
        
        # Save game state
        self.save_game()
        
        Logger.info(f"GameManager: Quest {quest_id} completed with rewards: {rewards}")
        return rewards
        
    def can_start_quest(self, quest_id):
        """
        Check if player can start a specific quest.
        
        Args:
            quest_id (str): ID of the quest to check
            
        Returns:
            bool: True if quest can be started
        """
        return self.quest_system.can_start_quest(quest_id) and \
               self.player.energy >= self.quest_system.get_quest_data(quest_id).get('energy_cost', 0)
               
    def update_energy(self):
        """Update player energy regeneration"""
        self.player.update_energy()
        
    def save_game(self):
        """Save current game state"""
        try:
            save_data = {
                'player': self.player.to_dict(),
                'quest_progress': self.quest_system.get_progress(),
                'game_started': self.game_started,
                'save_version': '1.0'
            }
            
            self.data_manager.save_data(save_data)
            Logger.info("GameManager: Game saved successfully")
            
        except Exception as e:
            Logger.error(f"GameManager: Failed to save game: {e}")
            
    def load_game(self):
        """Load saved game state"""
        try:
            save_data = self.data_manager.load_data()
            
            if save_data:
                # Load player data
                if 'player' in save_data:
                    self.player.from_dict(save_data['player'])
                    
                # Load quest progress
                if 'quest_progress' in save_data:
                    self.quest_system.set_progress(save_data['quest_progress'])
                    
                # Load game state
                self.game_started = save_data.get('game_started', False)
                
                Logger.info("GameManager: Game loaded successfully")
            else:
                Logger.info("GameManager: No saved game found, starting fresh")
                
        except Exception as e:
            Logger.error(f"GameManager: Failed to load game: {e}")
            
    def get_player_stats(self):
        """Get formatted player stats for display"""
        return {
            'level': self.player.level,
            'xp': f"{self.player.xp}/{self.player.xp_to_next_level}",
            'gold': self.player.gold,
            'soul_shards': self.player.soul_shards,
            'energy': f"{self.player.energy}/{self.player.max_energy}",
            'attack': self.player.attack,
            'defense': self.player.defense,
            'agility': self.player.agility,
            'magic': self.player.magic,
            'health': f"{self.player.current_health}/{self.player.max_health}"
        }
        
    def reset_game(self):
        """Reset the entire game to initial state"""
        Logger.info("GameManager: Resetting game")
        
        # Delete save file
        self.data_manager.delete_save()
        
        # Start new game
        self.start_new_game()
        
    def get_debug_info(self):
        """Get debug information for development"""
        return {
            'player_level': self.player.level,
            'player_xp': self.player.xp,
            'player_energy': self.player.energy,
            'quest_progress': self.quest_system.get_progress(),
            'current_quest': self.current_quest_id,
            'game_started': self.game_started
        }