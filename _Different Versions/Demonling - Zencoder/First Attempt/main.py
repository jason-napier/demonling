#!/usr/bin/env python3
"""
Demonling: Rise of the Realm Lord
A single-player RPG-style game where players aspire to become Demon Lords
"""

import sys
import os
import time
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Any

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_state import GameState
from player import Player
from quest_system import QuestSystem
from combat_system import CombatSystem
from ui_manager import UIManager

class DemonlingGame:
    """Main game class that orchestrates all systems"""
    
    def __init__(self):
        self.game_state = GameState()
        self.player = Player()
        self.quest_system = QuestSystem()
        self.combat_system = CombatSystem()
        self.ui = UIManager()
        self.running = True
        
        # Load saved game if exists
        self.load_game()
    
    def run(self):
        """Main game loop"""
        print("🕹️ Welcome to Demonling: Rise of the Realm Lord! 🕹️")
        print("=" * 50)
        
        while self.running:
            try:
                # Update energy based on time passed
                self.player.update_energy()
                
                # Show main menu
                self.show_main_menu()
                
                # Get user input
                choice = input("\nEnter your choice: ").strip()
                
                # Process choice
                self.process_main_menu_choice(choice)
                
            except KeyboardInterrupt:
                print("\n\nThanks for playing Demonling! 👹")
                self.save_game()
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("The game will continue...")
    
    def show_main_menu(self):
        """Display the main game menu"""
        self.ui.clear_screen()
        self.ui.show_header("🏰 DEMON LORD'S STRONGHOLD 🏰")
        
        # Show player stats
        self.ui.show_player_stats(self.player)
        
        # Show menu options
        print("\n📋 What would you like to do?")
        print("1. 🗡️  Start Quest")
        print("2. 📊  View Character Stats")
        print("3. 🏆  View Achievements")
        print("4. ⚡  Refill Energy (Debug)")
        print("5. 💾  Save Game")
        print("6. 🚪  Exit Game")
    
    def process_main_menu_choice(self, choice: str):
        """Process user's main menu choice"""
        if choice == "1":
            self.start_quest_menu()
        elif choice == "2":
            self.show_character_stats()
        elif choice == "3":
            self.show_achievements()
        elif choice == "4":
            self.refill_energy()
        elif choice == "5":
            self.save_game()
            print("✅ Game saved successfully!")
            input("Press Enter to continue...")
        elif choice == "6":
            self.running = False
            self.save_game()
            print("👹 Thanks for playing Demonling!")
        else:
            print("❌ Invalid choice. Please try again.")
            input("Press Enter to continue...")
    
    def start_quest_menu(self):
        """Show quest selection menu"""
        self.ui.clear_screen()
        self.ui.show_header("🗡️ QUEST SELECTION 🗡️")
        
        # Show available quest chains
        quest_chains = self.quest_system.get_quest_chains()
        
        for i, chain in enumerate(quest_chains, 1):
            status = self.quest_system.get_chain_status(chain['id'])
            print(f"{i}. {chain['name']} {status}")
            print(f"   {chain['description']}")
        
        print(f"\n{len(quest_chains) + 1}. 🔙 Back to Main Menu")
        
        try:
            choice = input("\nSelect a quest chain: ").strip()
            if choice == str(len(quest_chains) + 1):
                return
            
            chain_index = int(choice) - 1
            if 0 <= chain_index < len(quest_chains):
                self.start_quest_chain(quest_chains[chain_index])
            else:
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a valid number.")
            input("Press Enter to continue...")
    
    def start_quest_chain(self, chain: Dict[str, Any]):
        """Start a specific quest chain"""
        self.ui.clear_screen()
        self.ui.show_header(f"🗡️ {chain['name']} 🗡️")
        
        # Get quests in this chain
        quests = self.quest_system.get_quests_in_chain(chain['id'])
        
        for i, quest in enumerate(quests, 1):
            status = self.quest_system.get_quest_status(quest['id'])
            print(f"{i}. {quest['name']} {status}")
            print(f"   {quest['description']}")
            if status == '🟢':
                print(f"   Energy Cost: {quest['energy_cost']} | Reward: {quest['xp_reward']} XP, {quest['gold_reward']} Gold")
        
        print(f"\n{len(quests) + 1}. 🔙 Back to Quest Selection")
        
        try:
            choice = input("\nSelect a quest: ").strip()
            if choice == str(len(quests) + 1):
                return
            
            quest_index = int(choice) - 1
            if 0 <= quest_index < len(quests):
                self.start_quest(quests[quest_index])
            else:
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a valid number.")
            input("Press Enter to continue...")
    
    def start_quest(self, quest: Dict[str, Any]):
        """Start a specific quest"""
        # Check if quest is unlocked
        if not self.quest_system.is_quest_unlocked(quest['id']):
            print("🔒 This quest is locked. Complete previous quests first.")
            input("Press Enter to continue...")
            return
        
        # Check if player has enough energy
        if self.player.energy < quest['energy_cost']:
            print(f"⚡ Not enough energy! Need {quest['energy_cost']}, have {self.player.energy}")
            input("Press Enter to continue...")
            return
        
        # Start quest
        print(f"\n🚀 Starting quest: {quest['name']}")
        print(f"📖 {quest['description']}")
        print(f"⚡ Energy Cost: {quest['energy_cost']}")
        
        confirm = input("\nDo you want to start this quest? (y/n): ").strip().lower()
        if confirm != 'y':
            return
        
        # Deduct energy
        self.player.energy -= quest['energy_cost']
        
        # Start combat if quest has enemies
        if 'enemy' in quest:
            result = self.combat_system.start_combat(self.player, quest['enemy'])
            if result['victory']:
                self.complete_quest(quest)
            else:
                print("\n💀 Quest failed! You were defeated in combat.")
                # Restore some energy on failure
                self.player.energy += quest['energy_cost'] // 2
                input("Press Enter to continue...")
        else:
            # Non-combat quest - auto-complete for now
            self.complete_quest(quest)
    
    def complete_quest(self, quest: Dict[str, Any]):
        """Complete a quest and give rewards"""
        print(f"\n🏆 Quest '{quest['name']}' completed!")
        
        # Give rewards
        self.player.gain_xp(quest['xp_reward'])
        self.player.gain_gold(quest['gold_reward'])
        
        # Give soul shard if first time completion
        if not self.quest_system.is_quest_completed(quest['id']):
            self.player.soul_shards += 1
            print(f"✨ First completion bonus: +1 Soul Shard!")
        
        # Mark quest as completed
        self.quest_system.complete_quest(quest['id'])
        
        print(f"📈 Gained {quest['xp_reward']} XP and {quest['gold_reward']} Gold!")
        
        input("Press Enter to continue...")
    
    def show_character_stats(self):
        """Show detailed character statistics"""
        self.ui.clear_screen()
        self.ui.show_header("📊 CHARACTER STATS 📊")
        self.ui.show_detailed_stats(self.player)
        input("\nPress Enter to continue...")
    
    def show_achievements(self):
        """Show player achievements"""
        self.ui.clear_screen()
        self.ui.show_header("🏆 ACHIEVEMENTS 🏆")
        
        # TODO: Implement achievement system
        print("🚧 Achievement system coming soon!")
        
        input("\nPress Enter to continue...")
    
    def refill_energy(self):
        """Refill player energy (debug function)"""
        self.player.energy = self.player.max_energy
        print("⚡ Energy refilled!")
        input("Press Enter to continue...")
    
    def save_game(self):
        """Save the current game state"""
        save_data = {
            'player': self.player.to_dict(),
            'quest_system': self.quest_system.to_dict(),
            'timestamp': datetime.now().isoformat()
        }
        
        os.makedirs('saves', exist_ok=True)
        with open('saves/savegame.json', 'w') as f:
            json.dump(save_data, f, indent=2)
    
    def load_game(self):
        """Load a saved game if it exists"""
        save_path = 'saves/savegame.json'
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r') as f:
                    save_data = json.load(f)
                
                self.player.from_dict(save_data['player'])
                self.quest_system.from_dict(save_data['quest_system'])
                
                print("✅ Saved game loaded successfully!")
            except Exception as e:
                print(f"⚠️ Could not load saved game: {e}")
                print("Starting with a new character...")


def main():
    """Entry point for the game"""
    game = DemonlingGame()
    game.run()


if __name__ == "__main__":
    main()