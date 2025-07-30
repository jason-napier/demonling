"""
Demonling: Rise of the Realm Lord
Main entry point for the Kivy application
"""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.logger import Logger

# Set minimum Kivy version
kivy.require('2.0.0')

# Import game modules
from game_manager import GameManager
from ui_screens import (
    HomeScreen, 
    QuestScreen, 
    CombatScreen, 
    CharacterScreen,
    SettingsScreen
)

class DemonlingApp(App):
    """Main application class"""
    
    def build(self):
        """Build the application"""
        self.title = "Demonling: Rise of the Realm Lord"
        self.icon = "assets/icon.png"  # We'll create this later
        
        # Initialize game manager
        self.game_manager = GameManager()
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Create and add screens
        self.home_screen = HomeScreen(name='home', game_manager=self.game_manager)
        self.quest_screen = QuestScreen(name='quest', game_manager=self.game_manager)
        self.combat_screen = CombatScreen(name='combat', game_manager=self.game_manager)
        self.character_screen = CharacterScreen(name='character', game_manager=self.game_manager)
        self.settings_screen = SettingsScreen(name='settings', game_manager=self.game_manager)
        
        # Add screens to manager
        self.screen_manager.add_widget(self.home_screen)
        self.screen_manager.add_widget(self.quest_screen)
        self.screen_manager.add_widget(self.combat_screen)
        self.screen_manager.add_widget(self.character_screen)
        self.screen_manager.add_widget(self.settings_screen)
        
        # Set initial screen
        self.screen_manager.current = 'home'
        
        # Schedule energy regeneration
        Clock.schedule_interval(self.update_energy, 1.0)  # Update every second
        
        return self.screen_manager
    
    def update_energy(self, dt):
        """Update energy regeneration"""
        self.game_manager.update_energy()
        # Update home screen if it's current
        if self.screen_manager.current == 'home':
            self.home_screen.update_display()
    
    def on_start(self):
        """Called when the app starts"""
        Logger.info("Demonling: Game starting...")
        self.game_manager.load_game()
        
    def on_stop(self):
        """Called when the app stops"""
        Logger.info("Demonling: Game stopping...")
        self.game_manager.save_game()
    
    def on_pause(self):
        """Called when the app is paused (mobile)"""
        self.game_manager.save_game()
        return True
    
    def on_resume(self):
        """Called when the app resumes (mobile)"""
        self.game_manager.load_game()

if __name__ == '__main__':
    DemonlingApp().run()