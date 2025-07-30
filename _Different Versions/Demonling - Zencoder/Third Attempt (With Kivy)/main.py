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
from kivy.uix.scrollview import ScrollView
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
from item_system import ItemSystem, ItemType, ItemRarity

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
        # Main layout container with mobile-friendly padding
        main_layout = BoxLayout(orientation='vertical', padding=['20dp', '20dp', '20dp', '20dp'], spacing='20dp')
        
        # Game title - larger for mobile
        title = Label(
            text='Demonling: Rise of the Realm Lord',
            font_size='26sp',
            bold=True,
            size_hint_y=None,
            height='80dp',
            color=(0.9, 0.1, 0.1, 1),  # Red color for demonic theme
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(title)
        
        # Player stats display area - mobile optimized
        stats_layout = GridLayout(cols=2, size_hint_y=None, height='160dp', spacing='15dp')
        
        # Create stats labels with better mobile sizing
        self.level_label = Label(text='Level: 1', font_size='20sp', bold=True)
        self.xp_label = Label(text='XP: 0/100', font_size='20sp', bold=True)
        self.gold_label = Label(text='Gold: 0', font_size='20sp', bold=True, color=(1, 0.8, 0, 1))  # Gold color
        self.soul_shards_label = Label(text='Soul Shards: 0', font_size='20sp', bold=True, color=(0.8, 0.2, 0.8, 1))  # Purple color
        
        stats_layout.add_widget(self.level_label)
        stats_layout.add_widget(self.xp_label)
        stats_layout.add_widget(self.gold_label)
        stats_layout.add_widget(self.soul_shards_label)
        
        main_layout.add_widget(stats_layout)
        
        # Energy bar with label - mobile optimized
        energy_container = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp', spacing='10dp')
        self.energy_label = Label(text='Energy: 100/100', font_size='18sp', bold=True, color=(0.2, 0.8, 1, 1))  # Blue color
        self.energy_bar = ProgressBar(max=100, value=100, size_hint_y=None, height='30dp')
        energy_container.add_widget(self.energy_label)
        energy_container.add_widget(self.energy_bar)
        main_layout.add_widget(energy_container)
        
        # Navigation buttons - mobile optimized
        button_layout = BoxLayout(orientation='vertical', spacing='15dp')
        
        # Quest button
        quests_btn = CustomButton(
            text='⚔️ Quests',
            size_hint_y=None,
            height='60dp',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='20sp'
        )
        quests_btn.bind(on_press=self.go_to_quests)
        button_layout.add_widget(quests_btn)
        
        # Stats button
        stats_btn = CustomButton(
            text='📊 Character Stats',
            size_hint_y=None,
            height='60dp',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='20sp'
        )
        stats_btn.bind(on_press=self.go_to_stats)
        button_layout.add_widget(stats_btn)
        
        # Inventory button
        inventory_btn = CustomButton(
            text='🎒 Inventory',
            size_hint_y=None,
            height='60dp',
            background_color=(0.8, 0.6, 0.2, 1),
            font_size='20sp'
        )
        inventory_btn.bind(on_press=self.go_to_inventory)
        button_layout.add_widget(inventory_btn)
        
        # Shop button
        shop_btn = CustomButton(
            text='🛒 Shop',
            size_hint_y=None,
            height='60dp',
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='20sp'
        )
        shop_btn.bind(on_press=self.go_to_shop)
        button_layout.add_widget(shop_btn)
        
        # Energy refill button (for testing)
        refill_btn = CustomButton(
            text='⚡ Refill Energy (Test)',
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.2, 0.8, 1),
            font_size='18sp'
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
        
    def go_to_inventory(self, instance):
        """Navigate to inventory screen"""
        self.manager.current = 'inventory'
        
    def go_to_shop(self, instance):
        """Navigate to shop screen"""
        self.manager.current = 'shop'
        
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
        main_layout = BoxLayout(orientation='vertical', padding=['20dp', '20dp', '20dp', '20dp'], spacing='20dp')
        
        # Title
        title = Label(
            text='⚔️ Quest Chains ⚔️',
            font_size='26sp',
            bold=True,
            size_hint_y=None,
            height='60dp',
            color=(0.9, 0.1, 0.1, 1)
        )
        main_layout.add_widget(title)
        
        # Quest list container (will be populated dynamically)
        self.quest_container = BoxLayout(orientation='vertical', spacing='15dp')
        main_layout.add_widget(self.quest_container)
        
        # Back button
        back_btn = CustomButton(
            text='🏠 Back to Home',
            size_hint_y=None,
            height='60dp',
            background_color=(0.5, 0.5, 0.5, 1),
            font_size='20sp'
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
                text=f'📜 Chain: {chain_name}',
                font_size='20sp',
                bold=True,
                size_hint_y=None,
                height='50dp',
                color=(0.9, 0.7, 0.1, 1)  # Gold color
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
            height='60dp',
            background_color=btn_color,
            font_size='18sp'
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
        main_layout = BoxLayout(orientation='vertical', padding=['20dp', '20dp', '20dp', '20dp'], spacing='15dp')
        
        # Combat status area
        self.status_label = Label(
            text='⚔️ Combat Arena ⚔️',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height='60dp',
            color=(0.9, 0.1, 0.1, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Health bars container - mobile optimized
        health_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='140dp', spacing='15dp')
        
        # Player health
        self.player_health_label = Label(text='Your Health: 100/100', font_size='18sp', bold=True, color=(0.2, 0.8, 0.2, 1))
        self.player_health_bar = ProgressBar(max=100, value=100, size_hint_y=None, height='25dp')
        health_layout.add_widget(self.player_health_label)
        health_layout.add_widget(self.player_health_bar)
        
        # Enemy health
        self.enemy_health_label = Label(text='Enemy Health: 100/100', font_size='18sp', bold=True, color=(0.8, 0.2, 0.2, 1))
        self.enemy_health_bar = ProgressBar(max=100, value=100, size_hint_y=None, height='25dp')
        health_layout.add_widget(self.enemy_health_label)
        health_layout.add_widget(self.enemy_health_bar)
        
        main_layout.add_widget(health_layout)
        
        # Status effects display - mobile optimized
        status_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='80dp', spacing='10dp')
        
        # Player status effects
        self.player_status_label = Label(
            text='Player Status: None',
            font_size='16sp',
            size_hint_y=None,
            height='20dp',
            color=(0.2, 0.8, 0.2, 1)
        )
        status_layout.add_widget(self.player_status_label)
        
        # Enemy status effects
        self.enemy_status_label = Label(
            text='Enemy Status: None',
            font_size='16sp',
            size_hint_y=None,
            height='20dp',
            color=(0.8, 0.2, 0.2, 1)
        )
        status_layout.add_widget(self.enemy_status_label)
        
        main_layout.add_widget(status_layout)
        
        # Combat log with proper container
        from ui_components import CombatLog
        self.combat_log = CombatLog(
            size_hint_y=0.4
        )
        main_layout.add_widget(self.combat_log)
        
        # Action buttons - mobile optimized
        self.action_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='140dp', spacing='10dp')
        
        # Primary actions row
        primary_row = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing='15dp')
        
        # Attack button
        self.attack_btn = CustomButton(
            text='⚔️ Attack',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='20sp'
        )
        self.attack_btn.bind(on_press=self.player_attack)
        primary_row.add_widget(self.attack_btn)
        
        # Defend button
        self.defend_btn = CustomButton(
            text='🛡️ Defend',
            background_color=(0.2, 0.2, 0.8, 1),
            font_size='20sp'
        )
        self.defend_btn.bind(on_press=self.player_defend)
        primary_row.add_widget(self.defend_btn)
        
        self.action_layout.add_widget(primary_row)
        
        # Status effect abilities row
        magic_row = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing='10dp')
        
        # Fire spell button
        self.fire_btn = CustomButton(
            text='🔥 Burn',
            background_color=(0.8, 0.4, 0.2, 1),
            font_size='16sp'
        )
        self.fire_btn.bind(on_press=self.cast_fire_spell)
        magic_row.add_widget(self.fire_btn)
        
        # Ice spell button
        self.ice_btn = CustomButton(
            text='❄️ Freeze',
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='16sp'
        )
        self.ice_btn.bind(on_press=self.cast_ice_spell)
        magic_row.add_widget(self.ice_btn)
        
        # Poison spell button
        self.poison_btn = CustomButton(
            text='☠️ Poison',
            background_color=(0.4, 0.2, 0.8, 1),
            font_size='16sp'
        )
        self.poison_btn.bind(on_press=self.cast_poison_spell)
        magic_row.add_widget(self.poison_btn)
        
        # Heal spell button
        self.heal_btn = CustomButton(
            text='💚 Heal',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='16sp'
        )
        self.heal_btn.bind(on_press=self.cast_heal_spell)
        magic_row.add_widget(self.heal_btn)
        
        self.action_layout.add_widget(magic_row)
        
        main_layout.add_widget(self.action_layout)
        
        # End combat button (initially hidden)
        self.end_combat_btn = CustomButton(
            text='🏠 Return to Quests',
            size_hint_y=None,
            height='60dp',
            background_color=(0.5, 0.5, 0.5, 1),
            font_size='20sp'
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
            
        # Clear previous combat log first
        self.combat_log.clear_log()
        
        # Initialize combat system
        self.combat_system = CombatSystem(self.game_manager.player, quest_data['enemy'])
        
        # Update UI
        self.update_combat_display()
        self.add_to_combat_log(f"Battle begins against {quest_data['enemy']['name']}!", "ffff00")
        
        # Enable action buttons
        self.enable_action_buttons()
        if hasattr(self, 'end_combat_btn'):
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
        
        # Update status effects
        player_status = self.combat_system.get_player_status_effects()
        enemy_status = self.combat_system.get_enemy_status_effects()
        
        self.player_status_label.text = f'Player Status: {player_status if player_status else "None"}'
        self.enemy_status_label.text = f'Enemy Status: {enemy_status if enemy_status else "None"}'
        
    def player_attack(self, instance):
        """Handle player attack action"""
        if not self.combat_system:
            return
            
        # Process player turn start
        self.combat_system.process_turn_start(self.combat_system.player)
        
        # Execute player attack
        damage = self.combat_system.player_attack()
        if damage > 0:
            self.add_to_combat_log(f"You attack for {damage} damage!", "00ff00")  # Green for player actions
        
        # Process player turn end
        self.combat_system.process_turn_end(self.combat_system.player)
        
        # Check if enemy is defeated
        if self.combat_system.enemy.current_health <= 0:
            self.handle_victory()
            return
            
        # Update display
        self.update_combat_display()
        
        # Enemy turn
        self.schedule_enemy_turn()
        
    def cast_fire_spell(self, instance):
        """Cast a fire spell that burns the enemy"""
        if not self.combat_system:
            return
            
        # Import status effects
        from combat_system import BurnedEffect
        
        # Create burned effect
        burn_effect = BurnedEffect(duration=3, power=5)
        
        # Apply to enemy
        self.combat_system.add_status_effect_to_enemy(burn_effect)
        self.add_to_combat_log("You cast a fire spell! The enemy is burned!", "ff8800")  # Orange for spells
        
        # Update display
        self.update_combat_display()
        
        # Enemy turn
        self.schedule_enemy_turn()
        
    def cast_ice_spell(self, instance):
        """Cast an ice spell that freezes the enemy"""
        if not self.combat_system:
            return
            
        from combat_system import FrozenEffect
        
        # Create frozen effect
        freeze_effect = FrozenEffect(duration=2)
        
        # Apply to enemy
        self.combat_system.add_status_effect_to_enemy(freeze_effect)
        self.add_to_combat_log("You cast an ice spell! The enemy is frozen!", "88ddff")  # Light blue for ice
        
        # Update display
        self.update_combat_display()
        
        # Enemy turn
        self.schedule_enemy_turn()
        
    def cast_poison_spell(self, instance):
        """Cast a poison spell that poisons the enemy"""
        if not self.combat_system:
            return
            
        from combat_system import PoisonedEffect
        
        # Create poison effect
        poison_effect = PoisonedEffect(duration=4, power=4)
        
        # Apply to enemy
        self.combat_system.add_status_effect_to_enemy(poison_effect)
        self.add_to_combat_log("You cast a poison spell! The enemy is poisoned!", "884488")  # Purple for poison
        
        # Update display
        self.update_combat_display()
        
        # Enemy turn
        self.schedule_enemy_turn()
        
    def cast_heal_spell(self, instance):
        """Cast a healing spell that gives regeneration"""
        if not self.combat_system:
            return
            
        from combat_system import RegeneratingEffect
        
        # Create regenerating effect
        regen_effect = RegeneratingEffect(duration=3, power=10)
        
        # Apply to player
        self.combat_system.add_status_effect_to_player(regen_effect)
        self.add_to_combat_log("You cast a healing spell! You feel regenerated!", "44ff44")  # Green for healing
        
        # Update display
        self.update_combat_display()
        
        # Enemy turn
        self.schedule_enemy_turn()
        
    def player_defend(self, instance):
        """Handle player defend action"""
        if not self.combat_system:
            return
            
        self.combat_system.player_defend()
        self.add_to_combat_log("You take a defensive stance!", "0080ff")  # Blue for defensive actions
        
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
            
        # Process enemy turn start
        self.combat_system.process_turn_start(self.combat_system.enemy)
        
        # Execute enemy attack
        damage = self.combat_system.enemy_attack()
        if damage > 0:
            self.add_to_combat_log(f"Enemy attacks for {damage} damage!", "ff4444")  # Red for enemy actions
        
        # Process enemy turn end
        self.combat_system.process_turn_end(self.combat_system.enemy)
        
        # Update display
        self.update_combat_display()
        
        # Check if player is defeated
        if self.combat_system.player.current_health <= 0:
            self.handle_defeat()
            return
            
        # Re-enable action buttons for next turn
        self.enable_action_buttons()
        
    def disable_action_buttons(self):
        """Disable all action buttons during enemy turn"""
        self.attack_btn.disabled = True
        self.defend_btn.disabled = True
        self.fire_btn.disabled = True
        self.ice_btn.disabled = True
        self.poison_btn.disabled = True
        self.heal_btn.disabled = True
        
    def enable_action_buttons(self):
        """Enable all action buttons for player turn"""
        self.attack_btn.disabled = False
        self.defend_btn.disabled = False
        self.fire_btn.disabled = False
        self.ice_btn.disabled = False
        self.poison_btn.disabled = False
        self.heal_btn.disabled = False
        
    def handle_victory(self):
        """Handle combat victory"""
        self.add_to_combat_log("Victory! You have defeated the enemy!", "ffff00")  # Yellow for victory
        
        # Process quest completion
        quest_id = self.game_manager.current_quest_id
        rewards = self.game_manager.complete_quest(quest_id)
        
        # Show rewards
        reward_text = f"Rewards: {rewards['xp']} XP, {rewards['gold']} Gold"
        if rewards['soul_shards'] > 0:
            reward_text += f", {rewards['soul_shards']} Soul Shards"
            
        self.add_to_combat_log(reward_text, "00ff88")  # Green for rewards
        
        # Generate item loot
        if hasattr(self.game_manager, 'item_system'):
            loot = self.game_manager.item_system.get_random_loot(self.game_manager.player.level)
            for item, quantity in loot:
                if self.game_manager.player.inventory.add_item(item, quantity):
                    loot_text = f"Found: {item.icon} {item.name}"
                    if quantity > 1:
                        loot_text += f" x{quantity}"
                    self.add_to_combat_log(loot_text, "ffd700")  # Gold for loot
                else:
                    self.add_to_combat_log("Inventory full! Item dropped.", "ff4444")  # Red for warning
        
        # Show end combat button
        self.show_end_combat_button()
        
    def handle_defeat(self):
        """Handle combat defeat"""
        self.add_to_combat_log("Defeat! You have been defeated...", "ff0000")  # Red for defeat
        self.add_to_combat_log("Don't give up! Try again when you're stronger.", "ffaa00")  # Orange for encouragement
        
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
        
    def add_to_combat_log(self, message, color=None):
        """Add a message to the combat log"""
        self.combat_log.add_message(message, color)
            
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
        main_layout = BoxLayout(orientation='vertical', padding=['20dp', '20dp', '20dp', '20dp'], spacing='20dp')
        
        # Title
        title = Label(
            text='📊 Character Stats 📊',
            font_size='26sp',
            bold=True,
            size_hint_y=None,
            height='60dp',
            color=(0.2, 0.8, 0.2, 1)
        )
        main_layout.add_widget(title)
        
        # Stats grid - mobile optimized
        stats_grid = GridLayout(cols=2, spacing='15dp', size_hint_y=0.7)
        
        # Create stat labels with colors and better sizing
        self.stat_labels = {
            'level': Label(text='📈 Level: 1', font_size='18sp', bold=True),
            'xp': Label(text='⭐ XP: 0/100', font_size='18sp', bold=True),
            'gold': Label(text='💰 Gold: 0', font_size='18sp', bold=True, color=(1, 0.8, 0, 1)),
            'soul_shards': Label(text='💎 Soul Shards: 0', font_size='18sp', bold=True, color=(0.8, 0.2, 0.8, 1)),
            'attack': Label(text='⚔️ Attack: 10', font_size='18sp', bold=True, color=(0.8, 0.2, 0.2, 1)),
            'defense': Label(text='🛡️ Defense: 5', font_size='18sp', bold=True, color=(0.2, 0.2, 0.8, 1)),
            'agility': Label(text='💨 Agility: 3', font_size='18sp', bold=True, color=(0.2, 0.8, 0.2, 1)),
            'magic': Label(text='🔮 Magic: 1', font_size='18sp', bold=True, color=(0.8, 0.2, 0.8, 1)),
            'health': Label(text='❤️ Health: 100/100', font_size='18sp', bold=True, color=(0.8, 0.2, 0.2, 1)),
            'energy': Label(text='⚡ Energy: 100/100', font_size='18sp', bold=True, color=(0.2, 0.8, 1, 1))
        }
        
        for label in self.stat_labels.values():
            stats_grid.add_widget(label)
            
        main_layout.add_widget(stats_grid)
        
        # Back button
        back_btn = CustomButton(
            text='🏠 Back to Home',
            size_hint_y=None,
            height='60dp',
            background_color=(0.5, 0.5, 0.5, 1),
            font_size='20sp'
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
        effective_stats = player.get_effective_stats()
        equipment_bonuses = player.equipment.get_total_stats()
        
        # Update all stat labels with emojis and show equipment bonuses
        self.stat_labels['level'].text = f'📈 Level: {player.level}'
        self.stat_labels['xp'].text = f'⭐ XP: {player.xp}/{player.xp_to_next_level}'
        self.stat_labels['gold'].text = f'💰 Gold: {player.gold}'
        self.stat_labels['soul_shards'].text = f'💎 Soul Shards: {player.soul_shards}'
        
        # Show base stats with equipment bonuses
        attack_bonus = equipment_bonuses.get('attack', 0)
        defense_bonus = equipment_bonuses.get('defense', 0)
        agility_bonus = equipment_bonuses.get('agility', 0)
        magic_bonus = equipment_bonuses.get('magic', 0)
        
        attack_text = f'⚔️ Attack: {player.attack}'
        if attack_bonus > 0:
            attack_text += f' (+{attack_bonus}) = {effective_stats["attack"]}'
        self.stat_labels['attack'].text = attack_text
        
        defense_text = f'🛡️ Defense: {player.defense}'
        if defense_bonus > 0:
            defense_text += f' (+{defense_bonus}) = {effective_stats["defense"]}'
        self.stat_labels['defense'].text = defense_text
        
        agility_text = f'💨 Agility: {player.agility}'
        if agility_bonus > 0:
            agility_text += f' (+{agility_bonus}) = {effective_stats["agility"]}'
        self.stat_labels['agility'].text = agility_text
        
        magic_text = f'🔮 Magic: {player.magic}'
        if magic_bonus > 0:
            magic_text += f' (+{magic_bonus}) = {effective_stats["magic"]}'
        self.stat_labels['magic'].text = magic_text
        
        self.stat_labels['health'].text = f'❤️ Health: {player.current_health}/{player.max_health}'
        self.stat_labels['energy'].text = f'⚡ Energy: {player.energy}/{player.max_energy}'
        
    def go_back(self, instance):
        """Go back to home screen"""
        self.manager.current = 'home'

class InventoryScreen(Screen):
    """
    Inventory screen showing player's items and equipment.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'inventory'
        self.game_manager = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the inventory screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=['20dp', '20dp', '20dp', '20dp'], spacing='20dp')
        
        # Title
        title = Label(
            text='🎒 Inventory 🎒',
            font_size='26sp',
            bold=True,
            size_hint_y=None,
            height='60dp',
            color=(0.8, 0.6, 0.2, 1)
        )
        main_layout.add_widget(title)
        
        # Tab buttons for different views
        tab_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        
        self.items_tab = CustomButton(
            text='📦 Items',
            background_color=(0.6, 0.6, 0.6, 1),
            font_size='16sp'
        )
        self.items_tab.bind(on_press=self.show_items_tab)
        tab_layout.add_widget(self.items_tab)
        
        self.equipment_tab = CustomButton(
            text='⚔️ Equipment',
            background_color=(0.4, 0.4, 0.4, 1),
            font_size='16sp'
        )
        self.equipment_tab.bind(on_press=self.show_equipment_tab)
        tab_layout.add_widget(self.equipment_tab)
        
        main_layout.add_widget(tab_layout)
        
        # Content area (will be populated based on selected tab)
        self.content_area = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.content_area)
        
        # Button layout for actions
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing='10dp')
        
        # Test items button (for development)
        test_btn = CustomButton(
            text='🧪 Add Test Items',
            background_color=(0.3, 0.3, 0.7, 1),
            font_size='16sp'
        )
        test_btn.bind(on_press=self.add_test_items)
        button_layout.add_widget(test_btn)
        
        # Back button
        back_btn = CustomButton(
            text='🏠 Back to Home',
            background_color=(0.5, 0.5, 0.5, 1),
            font_size='20sp'
        )
        back_btn.bind(on_press=self.go_back)
        button_layout.add_widget(back_btn)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
        
        # Current view state
        self.current_view = 'items'
        
    def on_enter(self):
        """Called when entering this screen"""
        if self.game_manager:
            self.show_items_tab(None)
            
    def show_items_tab(self, instance):
        """Show items tab"""
        self.current_view = 'items'
        self.items_tab.background_color = (0.6, 0.6, 0.6, 1)
        self.equipment_tab.background_color = (0.4, 0.4, 0.4, 1)
        self.update_content()
        
    def show_equipment_tab(self, instance):
        """Show equipment tab"""
        self.current_view = 'equipment'
        self.items_tab.background_color = (0.4, 0.4, 0.4, 1)
        self.equipment_tab.background_color = (0.6, 0.6, 0.6, 1)
        self.update_content()
        
    def update_content(self):
        """Update the content area based on current view"""
        self.content_area.clear_widgets()
        
        if not self.game_manager:
            return
            
        if self.current_view == 'items':
            self.show_items_view()
        elif self.current_view == 'equipment':
            self.show_equipment_view()
            
    def show_items_view(self):
        """Show inventory items"""
        # Create scrollable container
        scroll = ScrollView()
        items_layout = BoxLayout(orientation='vertical', spacing='10dp', size_hint_y=None)
        items_layout.bind(minimum_height=items_layout.setter('height'))
        
        # Show inventory info
        inventory = self.game_manager.player.inventory
        info_label = Label(
            text=f'Inventory: {inventory.get_used_slots()}/{inventory.max_slots} slots used',
            font_size='18sp',
            size_hint_y=None,
            height='40dp',
            color=(0.9, 0.9, 0.9, 1)
        )
        items_layout.add_widget(info_label)
        
        # Group items by type
        item_types = [ItemType.WEAPON, ItemType.ARMOR, ItemType.CONSUMABLE, ItemType.MATERIAL]
        
        for item_type in item_types:
            items = inventory.get_items_by_type(item_type)
            if items:
                # Type header
                type_header = Label(
                    text=f'--- {item_type.value.title()} ---',
                    font_size='20sp',
                    bold=True,
                    size_hint_y=None,
                    height='40dp',
                    color=(0.8, 0.8, 0.2, 1)
                )
                items_layout.add_widget(type_header)
                
                # Item buttons
                for item, quantity in items:
                    item_btn = self.create_item_button(item, quantity)
                    items_layout.add_widget(item_btn)
        
        scroll.add_widget(items_layout)
        self.content_area.add_widget(scroll)
        
    def show_equipment_view(self):
        """Show equipped items"""
        equipment_layout = BoxLayout(orientation='vertical', spacing='15dp')
        
        # Show equipped items
        equipment = self.game_manager.player.equipment
        
        for slot_name, item in equipment.slots.items():
            slot_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing='10dp')
            
            # Slot label
            slot_label = Label(
                text=f'{slot_name.title()}:',
                font_size='18sp',
                size_hint_x=0.3,
                bold=True
            )
            slot_layout.add_widget(slot_label)
            
            # Item or empty slot
            if item:
                item_btn = CustomButton(
                    text=f'{item.icon} {item.name}',
                    background_color=item.get_rarity_color(),
                    font_size='16sp'
                )
                item_btn.bind(on_press=lambda x, s=slot_name: self.unequip_item(s))
                slot_layout.add_widget(item_btn)
            else:
                empty_btn = CustomButton(
                    text='[Empty]',
                    background_color=(0.3, 0.3, 0.3, 1),
                    font_size='16sp'
                )
                empty_btn.disabled = True
                slot_layout.add_widget(empty_btn)
            
            equipment_layout.add_widget(slot_layout)
        
        # Show stat bonuses
        stats = equipment.get_total_stats()
        if stats:
            stats_label = Label(
                text=f'Equipment Bonuses: {", ".join([f"+{v} {k}" for k, v in stats.items() if v > 0])}',
                font_size='16sp',
                size_hint_y=None,
                height='40dp',
                color=(0.2, 0.8, 0.2, 1)
            )
            equipment_layout.add_widget(stats_label)
        
        self.content_area.add_widget(equipment_layout)
        
    def create_item_button(self, item, quantity):
        """Create a button for an inventory item"""
        # Create button text
        btn_text = f'{item.icon} {item.name}'
        if quantity > 1:
            btn_text += f' x{quantity}'
        
        # Add stats info if available
        stats_text = item.get_stat_bonus_text()
        if stats_text:
            btn_text += f' ({stats_text})'
            
        item_btn = CustomButton(
            text=btn_text,
            size_hint_y=None,
            height='50dp',
            background_color=item.get_rarity_color(),
            font_size='14sp'
        )
        
        # Bind appropriate action based on item type
        if item.item_type == ItemType.CONSUMABLE:
            item_btn.bind(on_press=lambda x: self.use_item(item))
        elif item.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
            item_btn.bind(on_press=lambda x: self.equip_item(item))
        else:
            item_btn.bind(on_press=lambda x: self.show_item_info(item))
        
        return item_btn
        
    def use_item(self, item):
        """Use a consumable item"""
        if self.game_manager.player.inventory.get_item_count(item.item_id) > 0:
            item_system = self.game_manager.item_system
            if item_system.use_consumable(item, self.game_manager.player):
                self.game_manager.player.inventory.remove_item(item.item_id, 1)
                self.show_popup(f'Used {item.name}!', 'Success')
                self.update_content()
            else:
                self.show_popup(f'Cannot use {item.name}', 'Error')
        
    def equip_item(self, item):
        """Equip an item"""
        player = self.game_manager.player
        
        # Check level requirement
        if item.level_requirement > player.level:
            self.show_popup(f'Level {item.level_requirement} required!', 'Error')
            return
            
        # Determine slot
        slot = None
        if item.item_type == ItemType.WEAPON:
            slot = 'weapon'
        elif item.item_type == ItemType.ARMOR:
            slot = 'armor'
            
        if slot:
            # Unequip current item if any
            current_item = player.equipment.get_equipped_item(slot)
            if current_item:
                player.inventory.add_item(current_item, 1)
                
            # Equip new item
            player.equipment.equip_item(item, slot)
            player.inventory.remove_item(item.item_id, 1)
            
            self.show_popup(f'Equipped {item.name}!', 'Success')
            self.update_content()
        
    def unequip_item(self, slot):
        """Unequip an item"""
        player = self.game_manager.player
        item = player.equipment.unequip_item(slot)
        
        if item:
            if player.inventory.add_item(item, 1):
                self.show_popup(f'Unequipped {item.name}!', 'Success')
                self.update_content()
            else:
                # Re-equip if inventory is full
                player.equipment.equip_item(item, slot)
                self.show_popup('Inventory full!', 'Error')
        
    def show_item_info(self, item):
        """Show item information popup"""
        info_text = f'{item.name}\n\n{item.description}\n\nType: {item.item_type.value.title()}\nRarity: {item.rarity.value.title()}\nValue: {item.value} gold'
        
        if item.stats:
            info_text += f'\nStats: {item.get_stat_bonus_text()}'
            
        if item.level_requirement > 1:
            info_text += f'\nLevel Required: {item.level_requirement}'
            
        self.show_popup(info_text, 'Item Info')
        
    def show_popup(self, message, title):
        """Show a popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message, text_size=(None, None), halign='center'),
            size_hint=(0.8, 0.6)
        )
        popup.open()
        
    def add_test_items(self, instance):
        """Add test items to inventory for development purposes"""
        if not self.game_manager:
            return
            
        item_system = self.game_manager.item_system
        player = self.game_manager.player
        
        # Add some test items
        test_items = [
            ('iron_sword', 1),
            ('chainmail', 1),
            ('demon_blade', 1),
            ('health_potion', 5),
            ('energy_potion', 3),
            ('soul_crystal', 2)
        ]
        
        added_items = []
        for item_id, quantity in test_items:
            item = item_system.get_item(item_id)
            if item and player.inventory.add_item(item, quantity):
                added_items.append(item.name)
        
        if added_items:
            self.show_popup(f'Added test items: {", ".join(added_items)}', 'Test Items Added')
            self.update_content()
        else:
            self.show_popup('Inventory full or items already added!', 'Error')
        
    def go_back(self, instance):
        """Go back to home screen"""
        self.manager.current = 'home'

class ShopScreen(Screen):
    """
    Shop screen where players can buy items using gold.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'shop'
        self.game_manager = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the shop screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=['20dp', '20dp', '20dp', '20dp'], spacing='20dp')
        
        # Title
        title = Label(
            text='🛒 Demon\'s Shop 🛒',
            font_size='26sp',
            bold=True,
            size_hint_y=None,
            height='60dp',
            color=(0.2, 0.6, 0.8, 1)
        )
        main_layout.add_widget(title)
        
        # Player gold display
        self.gold_label = Label(
            text='Gold: 0',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height='40dp',
            color=(1, 0.8, 0, 1)
        )
        main_layout.add_widget(self.gold_label)
        
        # Shop items container
        scroll = ScrollView()
        self.items_layout = BoxLayout(orientation='vertical', spacing='10dp', size_hint_y=None)
        self.items_layout.bind(minimum_height=self.items_layout.setter('height'))
        
        scroll.add_widget(self.items_layout)
        main_layout.add_widget(scroll)
        
        # Back button
        back_btn = CustomButton(
            text='🏠 Back to Home',
            size_hint_y=None,
            height='60dp',
            background_color=(0.5, 0.5, 0.5, 1),
            font_size='20sp'
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
        
    def on_enter(self):
        """Called when entering this screen"""
        if self.game_manager:
            self.update_shop()
            
    def update_shop(self):
        """Update the shop display"""
        self.items_layout.clear_widgets()
        
        if not self.game_manager:
            return
            
        player = self.game_manager.player
        self.gold_label.text = f'Gold: {player.gold}'
        
        # Shop items (for demonstration)
        shop_items = [
            ('rusty_sword', 15),
            ('iron_sword', 75),
            ('leather_armor', 30),
            ('chainmail', 120),
            ('health_potion', 35),
            ('energy_potion', 40),
            ('soul_crystal', 150)
        ]
        
        for item_id, price in shop_items:
            item = self.game_manager.item_system.get_item(item_id)
            if item:
                shop_btn = self.create_shop_button(item, price)
                self.items_layout.add_widget(shop_btn)
        
    def create_shop_button(self, item, price):
        """Create a shop button for an item"""
        # Check if player can afford item
        can_afford = self.game_manager.player.gold >= price
        
        btn_text = f'{item.icon} {item.name} - {price} gold'
        
        # Add stats info if available
        stats_text = item.get_stat_bonus_text()
        if stats_text:
            btn_text += f' ({stats_text})'
        
        btn_color = item.get_rarity_color() if can_afford else (0.3, 0.3, 0.3, 1)
        
        shop_btn = CustomButton(
            text=btn_text,
            size_hint_y=None,
            height='50dp',
            background_color=btn_color,
            font_size='16sp'
        )
        
        if can_afford:
            shop_btn.bind(on_press=lambda x: self.buy_item(item, price))
        else:
            shop_btn.disabled = True
            
        return shop_btn
        
    def buy_item(self, item, price):
        """Buy an item from the shop"""
        player = self.game_manager.player
        
        if player.gold >= price:
            if player.inventory.add_item(item, 1):
                player.gold -= price
                self.show_popup(f'Bought {item.name}!', 'Purchase Successful')
                self.update_shop()
                self.game_manager.save_game()
            else:
                self.show_popup('Inventory full!', 'Purchase Failed')
        else:
            self.show_popup('Not enough gold!', 'Purchase Failed')
            
    def show_popup(self, message, title):
        """Show a popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message, text_size=(None, None), halign='center'),
            size_hint=(0.6, 0.4)
        )
        popup.open()
        
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
        inventory_screen = InventoryScreen()
        shop_screen = ShopScreen()
        
        # Set game manager reference for all screens
        home_screen.game_manager = self.game_manager
        quest_screen.game_manager = self.game_manager
        combat_screen.game_manager = self.game_manager
        stats_screen.game_manager = self.game_manager
        inventory_screen.game_manager = self.game_manager
        shop_screen.game_manager = self.game_manager
        
        # Add screens to screen manager
        sm.add_widget(home_screen)
        sm.add_widget(quest_screen)
        sm.add_widget(combat_screen)
        sm.add_widget(stats_screen)
        sm.add_widget(inventory_screen)
        sm.add_widget(shop_screen)
        
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