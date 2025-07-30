"""
Demonling: Rise of the Realm Lord
Main Application Entry Point

This is the main entry point for the Demonling RPG game.
It sets up the Kivy application and manages the screen flow.
"""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.logger import Logger
import json
import os
from datetime import datetime, timedelta

# Import our custom modules
from game_manager import GameManager
from combat_system import CombatSystem
from quest_system import QuestSystem
from ui_components import CustomButton, StatsDisplay, EnergyBar
from data_manager import DataManager

# Set minimum Kivy version
kivy.require('2.1.0')

class HomeScreen(Screen):
    """
    Main home screen of the game.
    Displays player stats, energy, and navigation buttons.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.game_manager = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the home screen UI layout"""
        # Main layout container
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Game title
        title = Label(
            text='Demonling: Rise of the Realm Lord',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height=60,
            color=(0.9, 0.1, 0.1, 1)  # Red color for demonic theme
        )
        main_layout.add_widget(title)
        
        # Player stats display area
        stats_layout = GridLayout(cols=2, size_hint_y=None, height=200, spacing=10)
        
        # Create stats labels (will be updated by game manager)
        self.level_label = Label(text='Level: 1', font_size='18sp')
        self.xp_label = Label(text='XP: 0/100', font_size='18sp')
        self.gold_label = Label(text='Gold: 0', font_size='18sp')
        self.soul_shards_label = Label(text='Soul Shards: 0', font_size='18sp')
        
        stats_layout.add_widget(self.level_label)
        stats_layout.add_widget(self.xp_label)
        stats_layout.add_widget(self.gold_label)
        stats_layout.add_widget(self.soul_shards_label)
        
        main_layout.add_widget(stats_layout)
        
        # Energy bar with label
        energy_container = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        self.energy_label = Label(text='Energy: 100/100', font_size='16sp')
        self.energy_bar = ProgressBar(max=100, value=100, size_hint_y=None, height=20)
        energy_container.add_widget(self.energy_label)
        energy_container.add_widget(self.energy_bar)
        main_layout.add_widget(energy_container)
        
        # Navigation buttons
        button_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Quest button
        quests_btn = CustomButton(
            text='Quests',
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        quests_btn.bind(on_press=self.go_to_quests)
        button_layout.add_widget(quests_btn)
        
        # Stats button
        stats_btn = CustomButton(
            text='Character Stats',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        stats_btn.bind(on_press=self.go_to_stats)
        button_layout.add_widget(stats_btn)
        
        # Energy refill button (for testing)
        refill_btn = CustomButton(
            text='Refill Energy (Test)',
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.2, 0.8, 1)
        )
        refill_btn.bind(on_press=self.refill_energy)
        button_layout.add_widget(refill_btn)
        
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)
        
    def on_enter(self):
        """Called when entering this screen"""
        if self.game_manager:
            self.update_display()
            
    def update_display(self):
        """Update all displayed information"""
        if not self.game_manager:
            return
            
        player = self.game_manager.player
        
        # Update stats labels
        self.level_label.text = f'Level: {player.level}'
        self.xp_label.text = f'XP: {player.xp}/{player.xp_to_next_level}'
        self.gold_label.text = f'Gold: {player.gold}'
        self.soul_shards_label.text = f'Soul Shards: {player.soul_shards}'
        
        # Update energy bar
        self.energy_label.text = f'Energy: {player.energy}/{player.max_energy}'
        self.energy_bar.value = player.energy
        self.energy_bar.max = player.max_energy
        
    def go_to_quests(self, instance):
        """Navigate to quest screen"""
        self.manager.current = 'quests'
        
    def go_to_stats(self, instance):
        """Navigate to stats screen"""
        self.manager.current = 'stats'
        
    def refill_energy(self, instance):
        """Refill energy for testing purposes"""
        if self.game_manager:
            self.game_manager.player.energy = self.game_manager.player.max_energy
            self.update_display()
            self.game_manager.save_game()

class QuestScreen(Screen):
    """
    Quest selection and management screen.
    Shows available quest chains and individual quests.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'quests'
        self.game_manager = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the quest screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='Quest Chains',
            font_size='22sp',
            bold=True,
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)
        
        # Quest list container (will be populated dynamically)
        self.quest_container = BoxLayout(orientation='vertical', spacing=10)
        main_layout.add_widget(self.quest_container)
        
        # Back button
        back_btn = CustomButton(
            text='Back to Home',
            size_hint_y=None,
            height=50,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
        
    def on_enter(self):
        """Called when entering this screen"""
        if self.game_manager:
            self.update_quest_list()
            
    def update_quest_list(self):
        """Update the list of available quests"""
        self.quest_container.clear_widgets()
        
        if not self.game_manager:
            return
            
        # Get available quest chains
        quest_chains = self.game_manager.quest_system.get_quest_chains()
        
        for chain_name, chain_data in quest_chains.items():
            # Create chain header
            chain_header = Label(
                text=f'Chain: {chain_name}',
                font_size='18sp',
                bold=True,
                size_hint_y=None,
                height=40
            )
            self.quest_container.add_widget(chain_header)
            
            # Create quest buttons for this chain
            for quest_id, quest_data in chain_data['quests'].items():
                quest_btn = self.create_quest_button(quest_id, quest_data)
                self.quest_container.add_widget(quest_btn)
                
    def create_quest_button(self, quest_id, quest_data):
        """Create a button for a specific quest"""
        # Determine quest status
        status = self.game_manager.quest_system.get_quest_status(quest_id)
        
        # Set button text and color based on status
        if status == 'completed':
            btn_text = f"✅ {quest_data['name']} (Completed)"
            btn_color = (0.2, 0.8, 0.2, 1)  # Green
        elif status == 'available':
            btn_text = f"🟢 {quest_data['name']} (Available)"
            btn_color = (0.8, 0.8, 0.2, 1)  # Yellow
        else:  # locked
            btn_text = f"🔒 {quest_data['name']} (Locked)"
            btn_color = (0.5, 0.5, 0.5, 1)  # Gray
            
        # Add energy cost info
        btn_text += f" [Energy: {quest_data['energy_cost']}]"
        
        quest_btn = CustomButton(
            text=btn_text,
            size_hint_y=None,
            height=50,
            background_color=btn_color
        )
        
        # Only bind action if quest is available
        if status == 'available' or status == 'completed':
            quest_btn.bind(on_press=lambda x: self.start_quest(quest_id))
        
        return quest_btn
        
    def start_quest(self, quest_id):
        """Start a specific quest"""
        if self.game_manager.quest_system.can_start_quest(quest_id):
            # Set current quest and switch to combat
            self.game_manager.current_quest_id = quest_id
            self.manager.current = 'combat'
        else:
            self.show_error_popup("Cannot start quest: insufficient energy or quest locked")
            
    def show_error_popup(self, message):
        """Show an error message popup"""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()
        
    def go_back(self, instance):
        """Go back to home screen"""
        self.manager.current = 'home'

class CombatScreen(Screen):
    """
    Combat screen where battles take place.
    Implements turn-based combat system.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'combat'
        self.game_manager = None
        self.combat_system = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the combat screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Combat status area
        self.status_label = Label(
            text='Combat Status',
            font_size='18sp',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(self.status_label)
        
        # Health bars container
        health_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=10)
        
        # Player health
        self.player_health_label = Label(text='Your Health: 100/100', font_size='16sp')
        self.player_health_bar = ProgressBar(max=100, value=100, size_hint_y=None, height=20)
        health_layout.add_widget(self.player_health_label)
        health_layout.add_widget(self.player_health_bar)
        
        # Enemy health
        self.enemy_health_label = Label(text='Enemy Health: 100/100', font_size='16sp')
        self.enemy_health_bar = ProgressBar(max=100, value=100, size_hint_y=None, height=20)
        health_layout.add_widget(self.enemy_health_label)
        health_layout.add_widget(self.enemy_health_bar)
        
        main_layout.add_widget(health_layout)
        
        # Combat log
        self.combat_log = Label(
            text='Combat begins...',
            font_size='14sp',
            text_size=(None, None),
            size_hint_y=0.4,
            valign='top'
        )
        main_layout.add_widget(self.combat_log)
        
        # Action buttons
        self.action_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        # Attack button
        self.attack_btn = CustomButton(
            text='Attack',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.attack_btn.bind(on_press=self.player_attack)
        self.action_layout.add_widget(self.attack_btn)
        
        # Defend button
        self.defend_btn = CustomButton(
            text='Defend',
            background_color=(0.2, 0.2, 0.8, 1)
        )
        self.defend_btn.bind(on_press=self.player_defend)
        self.action_layout.add_widget(self.defend_btn)
        
        main_layout.add_widget(self.action_layout)
        
        # End combat button (initially hidden)
        self.end_combat_btn = CustomButton(
            text='Return to Quests',
            size_hint_y=None,
            height=50,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.end_combat_btn.bind(on_press=self.end_combat)
        self.end_combat_btn.opacity = 0  # Hide initially
        main_layout.add_widget(self.end_combat_btn)
        
        self.add_widget(main_layout)
        
    def on_enter(self):
        """Called when entering combat screen"""
        if self.game_manager and self.game_manager.current_quest_id:
            self.start_combat()
            
    def start_combat(self):
        """Initialize and start combat"""
        quest_id = self.game_manager.current_quest_id
        quest_data = self.game_manager.quest_system.get_quest_data(quest_id)
        
        if not quest_data:
            self.end_combat_with_error("Quest data not found")
            return
            
        # Initialize combat system
        self.combat_system = CombatSystem(self.game_manager.player, quest_data['enemy'])
        
        # Update UI
        self.update_combat_display()
        self.add_to_combat_log(f"Battle begins against {quest_data['enemy']['name']}!")
        
        # Enable action buttons
        self.attack_btn.disabled = False
        self.defend_btn.disabled = False
        self.end_combat_btn.opacity = 0
        
    def update_combat_display(self):
        """Update the combat display with current health values"""
        if not self.combat_system:
            return
            
        player = self.combat_system.player
        enemy = self.combat_system.enemy
        
        # Update health bars and labels
        self.player_health_label.text = f'Your Health: {player.current_health}/{player.max_health}'
        self.player_health_bar.value = player.current_health
        self.player_health_bar.max = player.max_health
        
        self.enemy_health_label.text = f'Enemy Health: {enemy.current_health}/{enemy.max_health}'
        self.enemy_health_bar.value = enemy.current_health
        self.enemy_health_bar.max = enemy.max_health
        
    def player_attack(self, instance):
        """Handle player attack action"""
        if not self.combat_system:
            return
            
        # Execute player attack
        damage = self.combat_system.player_attack()
        self.add_to_combat_log(f"You attack for {damage} damage!")
        
        # Check if enemy is defeated
        if self.combat_system.enemy.current_health <= 0:
            self.handle_victory()
            return
            
        # Enemy turn
        self.schedule_enemy_turn()
        
    def player_defend(self, instance):
        """Handle player defend action"""
        if not self.combat_system:
            return
            
        self.combat_system.player_defend()
        self.add_to_combat_log("You take a defensive stance!")
        
        # Enemy turn
        self.schedule_enemy_turn()
        
    def schedule_enemy_turn(self):
        """Schedule enemy turn after a short delay"""
        self.disable_action_buttons()
        Clock.schedule_once(self.enemy_turn, 1.0)
        
    def enemy_turn(self, dt):
        """Execute enemy turn"""
        if not self.combat_system:
            return
            
        damage = self.combat_system.enemy_attack()
        self.add_to_combat_log(f"Enemy attacks for {damage} damage!")
        
        # Update display
        self.update_combat_display()
        
        # Check if player is defeated
        if self.combat_system.player.current_health <= 0:
            self.handle_defeat()
            return
            
        # Re-enable action buttons for next turn
        self.enable_action_buttons()
        
    def handle_victory(self):
        """Handle combat victory"""
        self.add_to_combat_log("Victory! You have defeated the enemy!")
        
        # Process quest completion
        quest_id = self.game_manager.current_quest_id
        rewards = self.game_manager.complete_quest(quest_id)
        
        # Show rewards
        reward_text = f"Rewards: {rewards['xp']} XP, {rewards['gold']} Gold"
        if rewards['soul_shards'] > 0:
            reward_text += f", {rewards['soul_shards']} Soul Shards"
            
        self.add_to_combat_log(reward_text)
        
        # Show end combat button
        self.show_end_combat_button()
        
    def handle_defeat(self):
        """Handle combat defeat"""
        self.add_to_combat_log("Defeat! You have been defeated...")
        self.add_to_combat_log("Don't give up! Try again when you're stronger.")
        
        # Show end combat button
        self.show_end_combat_button()
        
    def show_end_combat_button(self):
        """Show the end combat button and hide action buttons"""
        self.disable_action_buttons()
        self.end_combat_btn.opacity = 1
        
    def disable_action_buttons(self):
        """Disable action buttons during enemy turn"""
        self.attack_btn.disabled = True
        self.defend_btn.disabled = True
        
    def enable_action_buttons(self):
        """Enable action buttons for player turn"""
        self.attack_btn.disabled = False
        self.defend_btn.disabled = False
        
    def add_to_combat_log(self, message):
        """Add a message to the combat log"""
        current_log = self.combat_log.text
        if current_log == 'Combat begins...':
            self.combat_log.text = message
        else:
            self.combat_log.text = current_log + '\n' + message
            
    def end_combat(self, instance):
        """End combat and return to quests"""
        self.game_manager.current_quest_id = None
        self.manager.current = 'quests'
        
    def end_combat_with_error(self, error_message):
        """End combat due to error"""
        self.add_to_combat_log(f"Error: {error_message}")
        self.show_end_combat_button()

class StatsScreen(Screen):
    """
    Character stats screen showing detailed player information.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'stats'
        self.game_manager = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the stats screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='Character Stats',
            font_size='22sp',
            bold=True,
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)
        
        # Stats grid
        stats_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.7)
        
        # Create stat labels (will be updated)
        self.stat_labels = {
            'level': Label(text='Level: 1', font_size='16sp'),
            'xp': Label(text='XP: 0/100', font_size='16sp'),
            'gold': Label(text='Gold: 0', font_size='16sp'),
            'soul_shards': Label(text='Soul Shards: 0', font_size='16sp'),
            'attack': Label(text='Attack: 10', font_size='16sp'),
            'defense': Label(text='Defense: 5', font_size='16sp'),
            'agility': Label(text='Agility: 3', font_size='16sp'),
            'magic': Label(text='Magic: 1', font_size='16sp'),
            'health': Label(text='Health: 100/100', font_size='16sp'),
            'energy': Label(text='Energy: 100/100', font_size='16sp')
        }
        
        for label in self.stat_labels.values():
            stats_grid.add_widget(label)
            
        main_layout.add_widget(stats_grid)
        
        # Back button
        back_btn = CustomButton(
            text='Back to Home',
            size_hint_y=None,
            height=50,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
        
    def on_enter(self):
        """Called when entering this screen"""
        if self.game_manager:
            self.update_stats_display()
            
    def update_stats_display(self):
        """Update all stat displays"""
        if not self.game_manager:
            return
            
        player = self.game_manager.player
        
        # Update all stat labels
        self.stat_labels['level'].text = f'Level: {player.level}'
        self.stat_labels['xp'].text = f'XP: {player.xp}/{player.xp_to_next_level}'
        self.stat_labels['gold'].text = f'Gold: {player.gold}'
        self.stat_labels['soul_shards'].text = f'Soul Shards: {player.soul_shards}'
        self.stat_labels['attack'].text = f'Attack: {player.attack}'
        self.stat_labels['defense'].text = f'Defense: {player.defense}'
        self.stat_labels['agility'].text = f'Agility: {player.agility}'
        self.stat_labels['magic'].text = f'Magic: {player.magic}'
        self.stat_labels['health'].text = f'Health: {player.current_health}/{player.max_health}'
        self.stat_labels['energy'].text = f'Energy: {player.energy}/{player.max_energy}'
        
    def go_back(self, instance):
        """Go back to home screen"""
        self.manager.current = 'home'

class DemonlingApp(App):
    """
    Main Kivy application class.
    Manages the overall application lifecycle and screen management.
    """
    
    def build(self):
        """Build and return the main application widget"""
        Logger.info("Demonling: Starting application")
        
        # Initialize game manager
        self.game_manager = GameManager()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Create and add screens
        home_screen = HomeScreen()
        quest_screen = QuestScreen()
        combat_screen = CombatScreen()
        stats_screen = StatsScreen()
        
        # Set game manager reference for all screens
        home_screen.game_manager = self.game_manager
        quest_screen.game_manager = self.game_manager
        combat_screen.game_manager = self.game_manager
        stats_screen.game_manager = self.game_manager
        
        # Add screens to screen manager
        sm.add_widget(home_screen)
        sm.add_widget(quest_screen)
        sm.add_widget(combat_screen)
        sm.add_widget(stats_screen)
        
        # Set initial screen
        sm.current = 'home'
        
        # Schedule energy regeneration
        Clock.schedule_interval(self.update_energy, 60.0)  # Update every minute
        
        Logger.info("Demonling: Application built successfully")
        return sm
        
    def update_energy(self, dt):
        """Update energy regeneration"""
        self.game_manager.update_energy()
        
        # Update home screen if it's current
        if hasattr(self.root, 'current_screen') and self.root.current_screen.name == 'home':
            self.root.current_screen.update_display()
            
    def on_pause(self):
        """Handle application pause (mobile)"""
        self.game_manager.save_game()
        return True
        
    def on_resume(self):
        """Handle application resume (mobile)"""
        self.game_manager.load_game()
        self.game_manager.update_energy()
        
    def on_stop(self):
        """Handle application stop"""
        self.game_manager.save_game()
        Logger.info("Demonling: Application stopped")

# Entry point
if __name__ == '__main__':
    DemonlingApp().run()