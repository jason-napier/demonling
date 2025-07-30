"""
UI Screens - Kivy screen classes for the game interface
"""

import time
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from constants import *
from combat_system import CombatAction

class BaseScreen(Screen):
    """Base screen with common functionality"""
    
    def __init__(self, game_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = game_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI - to be implemented by subclasses"""
        pass
    
    def on_enter(self):
        """Called when screen is entered"""
        self.update_display()
    
    def update_display(self):
        """Update display - to be implemented by subclasses"""
        pass

class HomeScreen(BaseScreen):
    """Main home screen showing player stats and navigation"""
    
    def setup_ui(self):
        """Setup home screen UI"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(MARGIN), spacing=dp(MARGIN))
        
        # Title
        title = Label(
            text="Demonling: Rise of the Realm Lord",
            size_hint_y=None,
            height=dp(60),
            font_size='24sp',
            color=COLOR_ACCENT
        )
        main_layout.add_widget(title)
        
        # Player stats panel
        stats_panel = self.create_stats_panel()
        main_layout.add_widget(stats_panel)
        
        # Energy section
        energy_section = self.create_energy_section()
        main_layout.add_widget(energy_section)
        
        # Navigation buttons
        nav_buttons = self.create_navigation_buttons()
        main_layout.add_widget(nav_buttons)
        
        # Settings and info
        bottom_buttons = self.create_bottom_buttons()
        main_layout.add_widget(bottom_buttons)
        
        self.add_widget(main_layout)
    
    def create_stats_panel(self):
        """Create player stats display panel"""
        stats_layout = GridLayout(cols=2, spacing=dp(PADDING), size_hint_y=None, height=dp(200))
        
        # Labels for stats
        self.level_label = Label(text="Level: 1", color=COLOR_TEXT)
        self.xp_label = Label(text="XP: 0/100", color=COLOR_TEXT)
        self.gold_label = Label(text="Gold: 0", color=COLOR_TEXT)
        self.soul_shards_label = Label(text="Soul Shards: 0", color=COLOR_TEXT)
        
        # Combat stats
        self.health_label = Label(text="Health: 20", color=COLOR_TEXT)
        self.attack_label = Label(text="Attack: 5", color=COLOR_TEXT)
        self.defense_label = Label(text="Defense: 2", color=COLOR_TEXT)
        self.magic_label = Label(text="Magic: 1", color=COLOR_TEXT)
        
        # Add to layout
        stats_layout.add_widget(self.level_label)
        stats_layout.add_widget(self.xp_label)
        stats_layout.add_widget(self.gold_label)
        stats_layout.add_widget(self.soul_shards_label)
        stats_layout.add_widget(self.health_label)
        stats_layout.add_widget(self.attack_label)
        stats_layout.add_widget(self.defense_label)
        stats_layout.add_widget(self.magic_label)
        
        return stats_layout
    
    def create_energy_section(self):
        """Create energy display and refill section"""
        energy_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        # Energy display
        self.energy_label = Label(text="Energy: 10/20", color=COLOR_TEXT, size_hint_x=0.6)
        energy_layout.add_widget(self.energy_label)
        
        # Energy refill button
        self.refill_button = Button(
            text="Refill Energy\n(5 Soul Shards)",
            size_hint_x=0.4,
            background_color=COLOR_WARNING
        )
        self.refill_button.bind(on_press=self.refill_energy)
        energy_layout.add_widget(self.refill_button)
        
        return energy_layout
    
    def create_navigation_buttons(self):
        """Create main navigation buttons"""
        nav_layout = GridLayout(cols=2, spacing=dp(MARGIN), size_hint_y=None, height=dp(120))
        
        # Quest button
        quest_button = Button(
            text="Quests",
            background_color=COLOR_PRIMARY,
            font_size='18sp'
        )
        quest_button.bind(on_press=lambda x: self.change_screen('quest'))
        nav_layout.add_widget(quest_button)
        
        # Character button
        character_button = Button(
            text="Character",
            background_color=COLOR_PRIMARY,
            font_size='18sp'
        )
        character_button.bind(on_press=lambda x: self.change_screen('character'))
        nav_layout.add_widget(character_button)
        
        # Minions button (locked initially)
        self.minions_button = Button(
            text="Minions\n(Locked)",
            background_color=COLOR_TEXT_DARK,
            font_size='18sp'
        )
        self.minions_button.bind(on_press=self.minions_pressed)
        nav_layout.add_widget(self.minions_button)
        
        # Castle button (locked initially)
        self.castle_button = Button(
            text="Castle\n(Locked)",
            background_color=COLOR_TEXT_DARK,
            font_size='18sp'
        )
        self.castle_button.bind(on_press=self.castle_pressed)
        nav_layout.add_widget(self.castle_button)
        
        return nav_layout
    
    def create_bottom_buttons(self):
        """Create bottom navigation buttons"""
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        # Settings button
        settings_button = Button(
            text="Settings",
            background_color=COLOR_SECONDARY,
            size_hint_x=0.3
        )
        settings_button.bind(on_press=lambda x: self.change_screen('settings'))
        bottom_layout.add_widget(settings_button)
        
        # Spacer
        bottom_layout.add_widget(Label(text="", size_hint_x=0.4))
        
        # Save button
        save_button = Button(
            text="Save Game",
            background_color=COLOR_SUCCESS,
            size_hint_x=0.3
        )
        save_button.bind(on_press=self.save_game)
        bottom_layout.add_widget(save_button)
        
        return bottom_layout
    
    def update_display(self):
        """Update all displayed information"""
        if not self.game_manager:
            return
        
        stats = self.game_manager.get_player_stats()
        
        # Update stat labels
        self.level_label.text = f"Level: {stats['level']}"
        self.xp_label.text = f"XP: {stats['xp']}/{stats['xp_to_next']}"
        self.gold_label.text = f"Gold: {stats['gold']}"
        self.soul_shards_label.text = f"Soul Shards: {stats['soul_shards']}"
        
        self.health_label.text = f"Health: {stats['health']}"
        self.attack_label.text = f"Attack: {stats['attack']}"
        self.defense_label.text = f"Defense: {stats['defense']}"
        self.magic_label.text = f"Magic: {stats['magic']}"
        
        self.energy_label.text = f"Energy: {stats['energy']}/{stats['max_energy']}"
        
        # Update refill button
        can_refill = self.game_manager.can_afford_energy_refill()
        self.refill_button.disabled = not can_refill
        
        # Update locked features
        player = self.game_manager.player
        if 'minions' in player.unlocked_features:
            self.minions_button.text = "Minions"
            self.minions_button.background_color = COLOR_PRIMARY
        
        if 'castle' in player.unlocked_features:
            self.castle_button.text = "Castle"
            self.castle_button.background_color = COLOR_PRIMARY
    
    def change_screen(self, screen_name):
        """Change to specified screen"""
        self.manager.current = screen_name
    
    def refill_energy(self, instance):
        """Refill energy using soul shards"""
        if self.game_manager.refill_energy():
            self.update_display()
            self.show_popup("Energy Refilled!", "Your energy has been fully restored!")
        else:
            self.show_popup("Cannot Refill", "Not enough Soul Shards!")
    
    def minions_pressed(self, instance):
        """Handle minions button press"""
        if 'minions' in self.game_manager.player.unlocked_features:
            self.show_popup("Minions", "Minions feature coming soon!")
        else:
            self.show_popup("Locked", "Complete the Ash & Bone quest chain to unlock Minions!")
    
    def castle_pressed(self, instance):
        """Handle castle button press"""
        if 'castle' in self.game_manager.player.unlocked_features:
            self.show_popup("Castle", "Castle feature coming soon!")
        else:
            self.show_popup("Locked", "Reach level 15 to unlock Castle!")
    
    def save_game(self, instance):
        """Save the game"""
        self.game_manager.save_game()
        self.show_popup("Game Saved", "Your progress has been saved!")
    
    def show_popup(self, title, message):
        """Show a popup with title and message"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        message_label = Label(text=message, color=COLOR_TEXT)
        popup_layout.add_widget(message_label)
        
        close_button = Button(text="OK", size_hint_y=None, height=dp(40))
        popup_layout.add_widget(close_button)
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.4),
            background_color=COLOR_PRIMARY
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class QuestScreen(BaseScreen):
    """Quest selection and management screen"""
    
    def setup_ui(self):
        """Setup quest screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(MARGIN), spacing=dp(MARGIN))
        
        # Title and back button
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        back_button = Button(
            text="< Back",
            size_hint_x=None,
            width=dp(100),
            background_color=COLOR_SECONDARY
        )
        back_button.bind(on_press=lambda x: self.change_screen('home'))
        top_layout.add_widget(back_button)
        
        title = Label(text="Quest Chains", font_size='20sp', color=COLOR_TEXT)
        top_layout.add_widget(title)
        
        # Energy display
        self.energy_label = Label(text="Energy: 10/20", size_hint_x=None, width=dp(150), color=COLOR_TEXT)
        top_layout.add_widget(self.energy_label)
        
        main_layout.add_widget(top_layout)
        
        # Quest list
        scroll = ScrollView()
        self.quest_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.quest_layout.bind(minimum_height=self.quest_layout.setter('height'))
        
        scroll.add_widget(self.quest_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def update_display(self):
        """Update quest display"""
        if not self.game_manager:
            return
        
        # Update energy display
        stats = self.game_manager.get_player_stats()
        self.energy_label.text = f"Energy: {stats['energy']}/{stats['max_energy']}"
        
        # Clear existing quest widgets
        self.quest_layout.clear_widgets()
        
        # Add Ash & Bone chain
        self.add_quest_chain("ash_bone")
        
        # Add Blood & Iron chain if unlocked
        if self.game_manager.quest_manager.is_quest_unlocked("blood_iron_01"):
            self.add_quest_chain("blood_iron")
    
    def add_quest_chain(self, chain_id):
        """Add a quest chain to the display"""
        chain_info = self.game_manager.quest_manager.get_quest_chain(chain_id)
        if not chain_info:
            return
        
        progress = self.game_manager.quest_manager.get_chain_progress(chain_id)
        
        # Chain header
        chain_layout = BoxLayout(orientation='vertical', spacing=dp(5), 
                                size_hint_y=None, height=dp(200))
        
        # Chain title and progress
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        
        chain_title = Label(
            text=f"{chain_info['name']} ({progress['completed']}/{progress['total']})",
            font_size='18sp',
            color=COLOR_ACCENT,
            size_hint_x=0.7
        )
        header_layout.add_widget(chain_title)
        
        # Progress bar
        progress_bar = ProgressBar(
            max=progress['total'],
            value=progress['completed'],
            size_hint_x=0.3
        )
        header_layout.add_widget(progress_bar)
        
        chain_layout.add_widget(header_layout)
        
        # Quest buttons
        quest_grid = GridLayout(cols=5, spacing=dp(5), size_hint_y=None, height=dp(150))
        
        for quest_id in chain_info['quests']:
            quest_button = self.create_quest_button(quest_id)
            quest_grid.add_widget(quest_button)
        
        chain_layout.add_widget(quest_grid)
        
        self.quest_layout.add_widget(chain_layout)
    
    def create_quest_button(self, quest_id):
        """Create a button for a quest"""
        quest = self.game_manager.quest_manager.get_quest(quest_id)
        if not quest:
            return Button(text="???", background_color=COLOR_TEXT_DARK)
        
        status = self.game_manager.quest_manager.get_quest_status(quest_id)
        
        # Set button appearance based on status
        if status == "completed":
            button_color = COLOR_SUCCESS
            button_text = f"✅\n{quest.name}"
        elif status == "unlocked":
            if self.game_manager.player.has_energy(quest.energy_cost):
                button_color = COLOR_PRIMARY
                button_text = f"🟢\n{quest.name}\nEnergy: {quest.energy_cost}"
            else:
                button_color = COLOR_WARNING
                button_text = f"🟡\n{quest.name}\nEnergy: {quest.energy_cost}"
        else:
            button_color = COLOR_TEXT_DARK
            button_text = f"🔒\n{quest.name}"
        
        button = Button(
            text=button_text,
            background_color=button_color,
            font_size='12sp'
        )
        
        # Bind button press
        if status == "unlocked":
            button.bind(on_press=lambda x, qid=quest_id: self.start_quest(qid))
        else:
            button.bind(on_press=lambda x, q=quest: self.show_quest_info(q))
        
        return button
    
    def start_quest(self, quest_id):
        """Start a quest"""
        quest = self.game_manager.quest_manager.get_quest(quest_id)
        if not quest:
            return
        
        # Check if player has enough energy
        if not self.game_manager.player.has_energy(quest.energy_cost):
            self.show_popup("Not Enough Energy", f"You need {quest.energy_cost} energy to start this quest.")
            return
        
        # Show quest confirmation
        self.show_quest_confirmation(quest)
    
    def show_quest_confirmation(self, quest):
        """Show quest start confirmation"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Quest info
        quest_info = Label(
            text=f"Start Quest: {quest.name}\n\n{quest.description}\n\nEnergy Cost: {quest.energy_cost}\nRewards: {quest.xp_reward} XP, {quest.gold_reward} Gold",
            color=COLOR_TEXT
        )
        popup_layout.add_widget(quest_info)
        
        # Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        cancel_button = Button(text="Cancel", background_color=COLOR_SECONDARY)
        start_button = Button(text="Start Quest", background_color=COLOR_SUCCESS)
        
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(start_button)
        popup_layout.add_widget(button_layout)
        
        popup = Popup(
            title=f"Start {quest.name}?",
            content=popup_layout,
            size_hint=(0.8, 0.6),
            background_color=COLOR_PRIMARY
        )
        
        cancel_button.bind(on_press=popup.dismiss)
        start_button.bind(on_press=lambda x: self.confirm_start_quest(quest, popup))
        
        popup.open()
    
    def confirm_start_quest(self, quest, popup):
        """Confirm quest start"""
        popup.dismiss()
        
        if self.game_manager.start_quest(quest.id):
            # Quest started successfully
            if quest.enemy:
                # Go to combat screen
                self.change_screen('combat')
            else:
                # Non-combat quest completed
                self.show_popup("Quest Complete", f"You completed {quest.name}!")
                self.update_display()
        else:
            self.show_popup("Quest Failed", "Could not start quest.")
    
    def show_quest_info(self, quest):
        """Show quest information"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        quest_info = Label(
            text=f"{quest.name}\n\n{quest.description}\n\nEnergy Cost: {quest.energy_cost}\nRewards: {quest.xp_reward} XP, {quest.gold_reward} Gold",
            color=COLOR_TEXT
        )
        popup_layout.add_widget(quest_info)
        
        close_button = Button(text="Close", size_hint_y=None, height=dp(40))
        popup_layout.add_widget(close_button)
        
        popup = Popup(
            title=quest.name,
            content=popup_layout,
            size_hint=(0.8, 0.6),
            background_color=COLOR_PRIMARY
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def change_screen(self, screen_name):
        """Change to specified screen"""
        self.manager.current = screen_name
    
    def show_popup(self, title, message):
        """Show a popup with title and message"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        message_label = Label(text=message, color=COLOR_TEXT)
        popup_layout.add_widget(message_label)
        
        close_button = Button(text="OK", size_hint_y=None, height=dp(40))
        popup_layout.add_widget(close_button)
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.4),
            background_color=COLOR_PRIMARY
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class CombatScreen(BaseScreen):
    """Combat encounter screen"""
    
    def setup_ui(self):
        """Setup combat screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(MARGIN), spacing=dp(MARGIN))
        
        # Combat info section
        combat_info = self.create_combat_info()
        main_layout.add_widget(combat_info)
        
        # Combat log
        log_section = self.create_combat_log()
        main_layout.add_widget(log_section)
        
        # Action buttons
        action_buttons = self.create_action_buttons()
        main_layout.add_widget(action_buttons)
        
        self.add_widget(main_layout)
    
    def create_combat_info(self):
        """Create combat information display"""
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(100))
        
        # Player info
        player_layout = BoxLayout(orientation='vertical')
        
        self.player_name_label = Label(text="Player", font_size='16sp', color=COLOR_TEXT)
        self.player_health_label = Label(text="HP: 20/20", color=COLOR_SUCCESS)
        self.player_stats_label = Label(text="ATK: 5 DEF: 2", color=COLOR_TEXT)
        
        player_layout.add_widget(self.player_name_label)
        player_layout.add_widget(self.player_health_label)
        player_layout.add_widget(self.player_stats_label)
        
        info_layout.add_widget(player_layout)
        
        # VS label
        vs_label = Label(text="VS", font_size='20sp', color=COLOR_ACCENT, size_hint_x=None, width=dp(50))
        info_layout.add_widget(vs_label)
        
        # Enemy info
        enemy_layout = BoxLayout(orientation='vertical')
        
        self.enemy_name_label = Label(text="Enemy", font_size='16sp', color=COLOR_TEXT)
        self.enemy_health_label = Label(text="HP: 15/15", color=COLOR_DANGER)
        self.enemy_stats_label = Label(text="ATK: 3 DEF: 1", color=COLOR_TEXT)
        
        enemy_layout.add_widget(self.enemy_name_label)
        enemy_layout.add_widget(self.enemy_health_label)
        enemy_layout.add_widget(self.enemy_stats_label)
        
        info_layout.add_widget(enemy_layout)
        
        return info_layout
    
    def create_combat_log(self):
        """Create combat log display"""
        log_layout = BoxLayout(orientation='vertical', size_hint_y=0.4)
        
        log_title = Label(text="Combat Log", font_size='16sp', color=COLOR_TEXT, size_hint_y=None, height=dp(30))
        log_layout.add_widget(log_title)
        
        scroll = ScrollView()
        self.log_label = Label(
            text="Combat begins!",
            color=COLOR_TEXT,
            text_size=(None, None),
            valign='top',
            size_hint_y=None
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll.add_widget(self.log_label)
        log_layout.add_widget(scroll)
        
        return log_layout
    
    def create_action_buttons(self):
        """Create combat action buttons"""
        action_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150))
        
        # Turn indicator
        self.turn_label = Label(text="Your Turn", font_size='16sp', color=COLOR_ACCENT, size_hint_y=None, height=dp(30))
        action_layout.add_widget(self.turn_label)
        
        # Main actions
        main_actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        self.attack_button = Button(text="Attack", background_color=COLOR_DANGER)
        self.attack_button.bind(on_press=lambda x: self.player_action(CombatAction.ATTACK))
        main_actions.add_widget(self.attack_button)
        
        self.defend_button = Button(text="Defend", background_color=COLOR_PRIMARY)
        self.defend_button.bind(on_press=lambda x: self.player_action(CombatAction.DEFEND))
        main_actions.add_widget(self.defend_button)
        
        action_layout.add_widget(main_actions)
        
        # Special actions (MVP+ feature)
        special_actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        self.special1_button = Button(text="Fireball", background_color=COLOR_WARNING)
        self.special1_button.bind(on_press=lambda x: self.player_action(CombatAction.SPECIAL_ABILITY, 0))
        special_actions.add_widget(self.special1_button)
        
        self.special2_button = Button(text="Heal", background_color=COLOR_SUCCESS)
        self.special2_button.bind(on_press=lambda x: self.player_action(CombatAction.SPECIAL_ABILITY, 1))
        special_actions.add_widget(self.special2_button)
        
        self.special3_button = Button(text="Stun", background_color=COLOR_SECONDARY)
        self.special3_button.bind(on_press=lambda x: self.player_action(CombatAction.SPECIAL_ABILITY, 2))
        special_actions.add_widget(self.special3_button)
        
        action_layout.add_widget(special_actions)
        
        return action_layout
    
    def on_enter(self):
        """Called when entering combat screen"""
        super().on_enter()
        
        # Bind to combat events
        if self.game_manager.combat_manager:
            self.game_manager.combat_manager.bind(on_combat_log=self.update_combat_log)
            self.game_manager.combat_manager.bind(on_player_turn=self.on_player_turn)
            self.game_manager.combat_manager.bind(on_enemy_turn=self.on_enemy_turn)
            self.game_manager.combat_manager.bind(on_combat_end=self.on_combat_end)
    
    def update_display(self):
        """Update combat display"""
        if not self.game_manager or not self.game_manager.combat_manager:
            return
        
        combat_state = self.game_manager.combat_manager.get_combat_state()
        
        if not combat_state:
            return
        
        # Update player info
        self.player_name_label.text = f"Player (Level {self.game_manager.player.level})"
        self.player_health_label.text = f"HP: {combat_state['player_health']}/{combat_state['player_max_health']}"
        self.player_stats_label.text = f"ATK: {combat_state['player_attack']} DEF: {combat_state['player_defense']}"
        
        # Update enemy info
        self.enemy_name_label.text = combat_state['enemy_name']
        self.enemy_health_label.text = f"HP: {combat_state['enemy_health']}/{combat_state['enemy_max_health']}"
        self.enemy_stats_label.text = f"ATK: {combat_state['enemy_attack']} DEF: {combat_state['enemy_defense']}"
        
        # Update combat log
        if combat_state['combat_log']:
            self.log_label.text = '\n'.join(combat_state['combat_log'])
        
        # Update button states
        is_player_turn = combat_state['combat_state'] == 'player_turn'
        self.attack_button.disabled = not is_player_turn
        self.defend_button.disabled = not is_player_turn
        
        # Update special ability buttons
        self.special1_button.disabled = not (is_player_turn and self.game_manager.player.can_use_special_ability(0))
        self.special2_button.disabled = not (is_player_turn and self.game_manager.player.can_use_special_ability(1))
        self.special3_button.disabled = not (is_player_turn and self.game_manager.player.can_use_special_ability(2))
        
        # Update turn indicator
        if is_player_turn:
            self.turn_label.text = "Your Turn"
            self.turn_label.color = COLOR_SUCCESS
        else:
            self.turn_label.text = "Enemy Turn"
            self.turn_label.color = COLOR_DANGER
    
    def player_action(self, action, target=None):
        """Handle player combat action"""
        if self.game_manager.combat_manager:
            self.game_manager.combat_manager.player_action(action, target)
    
    def update_combat_log(self, combat_manager, message):
        """Update combat log with new message"""
        self.update_display()
    
    def on_player_turn(self, combat_manager):
        """Handle player turn event"""
        self.update_display()
    
    def on_enemy_turn(self, combat_manager):
        """Handle enemy turn event"""
        self.update_display()
        # Schedule enemy action after a delay
        Clock.schedule_once(self.update_display, 1.0)
    
    def on_combat_end(self, combat_manager, victory):
        """Handle combat end event"""
        self.update_display()
        
        # Show result popup
        if victory:
            self.show_popup("Victory!", "You have won the battle!")
        else:
            self.show_popup("Defeat", "You have been defeated...")
        
        # Return to quest screen after a delay
        Clock.schedule_once(lambda dt: self.change_screen('quest'), 2.0)
    
    def change_screen(self, screen_name):
        """Change to specified screen"""
        self.manager.current = screen_name
    
    def show_popup(self, title, message):
        """Show a popup with title and message"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        message_label = Label(text=message, color=COLOR_TEXT)
        popup_layout.add_widget(message_label)
        
        close_button = Button(text="OK", size_hint_y=None, height=dp(40))
        popup_layout.add_widget(close_button)
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.4),
            background_color=COLOR_PRIMARY
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class CharacterScreen(BaseScreen):
    """Character stats and progression screen"""
    
    def setup_ui(self):
        """Setup character screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(MARGIN), spacing=dp(MARGIN))
        
        # Title and back button
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        back_button = Button(
            text="< Back",
            size_hint_x=None,
            width=dp(100),
            background_color=COLOR_SECONDARY
        )
        back_button.bind(on_press=lambda x: self.change_screen('home'))
        top_layout.add_widget(back_button)
        
        title = Label(text="Character", font_size='20sp', color=COLOR_TEXT)
        top_layout.add_widget(title)
        
        main_layout.add_widget(top_layout)
        
        # Character info
        char_info = self.create_character_info()
        main_layout.add_widget(char_info)
        
        # Abilities section
        abilities_section = self.create_abilities_section()
        main_layout.add_widget(abilities_section)
        
        self.add_widget(main_layout)
    
    def create_character_info(self):
        """Create character information display"""
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=0.6)
        
        # Stats column
        stats_layout = BoxLayout(orientation='vertical')
        
        stats_title = Label(text="Statistics", font_size='18sp', color=COLOR_ACCENT, size_hint_y=None, height=dp(40))
        stats_layout.add_widget(stats_title)
        
        self.level_label = Label(text="Level: 1", color=COLOR_TEXT)
        self.xp_label = Label(text="XP: 0/100", color=COLOR_TEXT)
        self.health_label = Label(text="Health: 20", color=COLOR_TEXT)
        self.attack_label = Label(text="Attack: 5", color=COLOR_TEXT)
        self.defense_label = Label(text="Defense: 2", color=COLOR_TEXT)
        self.agility_label = Label(text="Agility: 3", color=COLOR_TEXT)
        self.magic_label = Label(text="Magic: 1", color=COLOR_TEXT)
        
        stats_layout.add_widget(self.level_label)
        stats_layout.add_widget(self.xp_label)
        stats_layout.add_widget(self.health_label)
        stats_layout.add_widget(self.attack_label)
        stats_layout.add_widget(self.defense_label)
        stats_layout.add_widget(self.agility_label)
        stats_layout.add_widget(self.magic_label)
        
        info_layout.add_widget(stats_layout)
        
        # Resources column
        resources_layout = BoxLayout(orientation='vertical')
        
        resources_title = Label(text="Resources", font_size='18sp', color=COLOR_ACCENT, size_hint_y=None, height=dp(40))
        resources_layout.add_widget(resources_title)
        
        self.gold_label = Label(text="Gold: 0", color=COLOR_TEXT)
        self.soul_shards_label = Label(text="Soul Shards: 0", color=COLOR_TEXT)
        self.energy_label = Label(text="Energy: 10/20", color=COLOR_TEXT)
        
        resources_layout.add_widget(self.gold_label)
        resources_layout.add_widget(self.soul_shards_label)
        resources_layout.add_widget(self.energy_label)
        
        # Add some spacing
        resources_layout.add_widget(Label(text=""))
        
        # Unlocked features
        features_title = Label(text="Unlocked Features", font_size='16sp', color=COLOR_ACCENT, size_hint_y=None, height=dp(40))
        resources_layout.add_widget(features_title)
        
        self.features_label = Label(text="None", color=COLOR_TEXT)
        resources_layout.add_widget(self.features_label)
        
        info_layout.add_widget(resources_layout)
        
        return info_layout
    
    def create_abilities_section(self):
        """Create abilities section"""
        abilities_layout = BoxLayout(orientation='vertical', size_hint_y=0.4)
        
        abilities_title = Label(text="Abilities", font_size='18sp', color=COLOR_ACCENT, size_hint_y=None, height=dp(40))
        abilities_layout.add_widget(abilities_title)
        
        # Ability slots
        abilities_grid = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, height=dp(100))
        
        self.ability1_button = Button(text="Fireball\n(Level 5)", background_color=COLOR_TEXT_DARK)
        self.ability2_button = Button(text="Heal\n(Level 10)", background_color=COLOR_TEXT_DARK)
        self.ability3_button = Button(text="Stun\n(Level 15)", background_color=COLOR_TEXT_DARK)
        
        abilities_grid.add_widget(self.ability1_button)
        abilities_grid.add_widget(self.ability2_button)
        abilities_grid.add_widget(self.ability3_button)
        
        abilities_layout.add_widget(abilities_grid)
        
        # Ability descriptions
        self.ability_desc_label = Label(
            text="Abilities unlock as you level up. Use them in combat for powerful effects!",
            color=COLOR_TEXT
        )
        abilities_layout.add_widget(self.ability_desc_label)
        
        return abilities_layout
    
    def update_display(self):
        """Update character display"""
        if not self.game_manager:
            return
        
        stats = self.game_manager.get_player_stats()
        
        # Update stat labels
        self.level_label.text = f"Level: {stats['level']}"
        self.xp_label.text = f"XP: {stats['xp']}/{stats['xp_to_next']}"
        self.health_label.text = f"Health: {stats['health']}"
        self.attack_label.text = f"Attack: {stats['attack']}"
        self.defense_label.text = f"Defense: {stats['defense']}"
        self.agility_label.text = f"Agility: {stats['agility']}"
        self.magic_label.text = f"Magic: {stats['magic']}"
        
        # Update resource labels
        self.gold_label.text = f"Gold: {stats['gold']}"
        self.soul_shards_label.text = f"Soul Shards: {stats['soul_shards']}"
        self.energy_label.text = f"Energy: {stats['energy']}/{stats['max_energy']}"
        
        # Update unlocked features
        player = self.game_manager.player
        if player.unlocked_features:
            features_list = list(player.unlocked_features)
            self.features_label.text = ", ".join(features_list)
        else:
            self.features_label.text = "None"
        
        # Update ability buttons
        if player.can_use_special_ability(0):
            self.ability1_button.text = "Fireball\n(Unlocked)"
            self.ability1_button.background_color = COLOR_WARNING
        
        if player.can_use_special_ability(1):
            self.ability2_button.text = "Heal\n(Unlocked)"
            self.ability2_button.background_color = COLOR_SUCCESS
        
        if player.can_use_special_ability(2):
            self.ability3_button.text = "Stun\n(Unlocked)"
            self.ability3_button.background_color = COLOR_SECONDARY
    
    def change_screen(self, screen_name):
        """Change to specified screen"""
        self.manager.current = screen_name

class SettingsScreen(BaseScreen):
    """Settings and game options screen"""
    
    def setup_ui(self):
        """Setup settings screen UI"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(MARGIN), spacing=dp(MARGIN))
        
        # Title and back button
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        back_button = Button(
            text="< Back",
            size_hint_x=None,
            width=dp(100),
            background_color=COLOR_SECONDARY
        )
        back_button.bind(on_press=lambda x: self.change_screen('home'))
        top_layout.add_widget(back_button)
        
        title = Label(text="Settings", font_size='20sp', color=COLOR_TEXT)
        top_layout.add_widget(title)
        
        main_layout.add_widget(top_layout)
        
        # Game options
        options_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Save/Load section
        save_section = self.create_save_section()
        options_layout.add_widget(save_section)
        
        # Game info section
        info_section = self.create_info_section()
        options_layout.add_widget(info_section)
        
        main_layout.add_widget(options_layout)
        
        self.add_widget(main_layout)
    
    def create_save_section(self):
        """Create save/load section"""
        save_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200))
        
        save_title = Label(text="Save Game", font_size='18sp', color=COLOR_ACCENT, size_hint_y=None, height=dp(40))
        save_layout.add_widget(save_title)
        
        # Save buttons
        save_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        save_button = Button(text="Save Game", background_color=COLOR_SUCCESS)
        save_button.bind(on_press=self.save_game)
        save_buttons.add_widget(save_button)
        
        load_button = Button(text="Load Game", background_color=COLOR_PRIMARY)
        load_button.bind(on_press=self.load_game)
        save_buttons.add_widget(load_button)
        
        save_layout.add_widget(save_buttons)
        
        # Dangerous actions
        danger_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        reset_button = Button(text="New Game", background_color=COLOR_DANGER)
        reset_button.bind(on_press=self.confirm_new_game)
        danger_buttons.add_widget(reset_button)
        
        delete_button = Button(text="Delete Save", background_color=COLOR_DANGER)
        delete_button.bind(on_press=self.confirm_delete_save)
        danger_buttons.add_widget(delete_button)
        
        save_layout.add_widget(danger_buttons)
        
        # Save info
        self.save_info_label = Label(text="Save Info: Loading...", color=COLOR_TEXT, size_hint_y=None, height=dp(60))
        save_layout.add_widget(self.save_info_label)
        
        return save_layout
    
    def create_info_section(self):
        """Create game info section"""
        info_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200))
        
        info_title = Label(text="Game Information", font_size='18sp', color=COLOR_ACCENT, size_hint_y=None, height=dp(40))
        info_layout.add_widget(info_title)
        
        version_label = Label(text=f"Version: {GAME_VERSION}", color=COLOR_TEXT)
        info_layout.add_widget(version_label)
        
        build_label = Label(text=f"Build: {GAME_BUILD}", color=COLOR_TEXT)
        info_layout.add_widget(build_label)
        
        credits_label = Label(text="Created with Kivy", color=COLOR_TEXT)
        info_layout.add_widget(credits_label)
        
        # About button
        about_button = Button(text="About", background_color=COLOR_SECONDARY, size_hint_y=None, height=dp(50))
        about_button.bind(on_press=self.show_about)
        info_layout.add_widget(about_button)
        
        return info_layout
    
    def update_display(self):
        """Update settings display"""
        if not self.game_manager:
            return
        
        # Update save info
        save_info = self.game_manager.data_manager.get_save_info()
        if save_info['exists']:
            self.save_info_label.text = f"Save exists - Level {save_info['player_level']}"
        else:
            self.save_info_label.text = "No save file found"
    
    def save_game(self, instance):
        """Save the game"""
        self.game_manager.save_game()
        self.show_popup("Game Saved", "Your progress has been saved!")
        self.update_display()
    
    def load_game(self, instance):
        """Load the game"""
        self.game_manager.load_game()
        self.show_popup("Game Loaded", "Your progress has been loaded!")
        self.update_display()
    
    def confirm_new_game(self, instance):
        """Confirm new game creation"""
        self.show_confirmation(
            "Start New Game?",
            "This will delete your current progress!",
            self.new_game
        )
    
    def new_game(self):
        """Start a new game"""
        self.game_manager.data_manager.delete_save()
        # Reset game state
        self.game_manager.player.__init__()
        self.game_manager.quest_manager.__init__()
        self.game_manager.last_energy_update = time.time()
        self.show_popup("New Game Started", "A new adventure begins!")
        self.update_display()
    
    def confirm_delete_save(self, instance):
        """Confirm save deletion"""
        self.show_confirmation(
            "Delete Save File?",
            "This action cannot be undone!",
            self.delete_save
        )
    
    def delete_save(self):
        """Delete save file"""
        self.game_manager.data_manager.delete_save()
        self.show_popup("Save Deleted", "Save file has been deleted!")
        self.update_display()
    
    def show_about(self, instance):
        """Show about dialog"""
        about_text = """Demonling: Rise of the Realm Lord

An RPG adventure where you rise from nothing to become the ultimate Demon Lord!

Features:
• Turn-based combat
• Quest progression
• Character development
• Energy management
• Offline progression

Created with Kivy framework for cross-platform mobile deployment."""
        
        self.show_popup("About Demonling", about_text)
    
    def show_confirmation(self, title, message, callback):
        """Show confirmation dialog"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        message_label = Label(text=message, color=COLOR_TEXT)
        popup_layout.add_widget(message_label)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        cancel_button = Button(text="Cancel", background_color=COLOR_SECONDARY)
        confirm_button = Button(text="Confirm", background_color=COLOR_DANGER)
        
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(confirm_button)
        popup_layout.add_widget(button_layout)
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.4),
            background_color=COLOR_PRIMARY
        )
        
        cancel_button.bind(on_press=popup.dismiss)
        confirm_button.bind(on_press=lambda x: self.execute_callback(callback, popup))
        
        popup.open()
    
    def execute_callback(self, callback, popup):
        """Execute callback and dismiss popup"""
        popup.dismiss()
        callback()
    
    def change_screen(self, screen_name):
        """Change to specified screen"""
        self.manager.current = screen_name
    
    def show_popup(self, title, message):
        """Show a popup with title and message"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        message_label = Label(text=message, color=COLOR_TEXT)
        popup_layout.add_widget(message_label)
        
        close_button = Button(text="OK", size_hint_y=None, height=dp(40))
        popup_layout.add_widget(close_button)
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.6),
            background_color=COLOR_PRIMARY
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()