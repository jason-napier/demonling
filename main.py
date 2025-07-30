# Import necessary Kivy modules for building the mobile app
from kivy.app import App  # Main app class - every Kivy app needs this
from kivy.uix.screenmanager import ScreenManager, Screen  # For managing different screens/pages
from kivy.uix.button import Button  # For creating clickable buttons
from kivy.uix.label import Label  # For displaying text
from kivy.uix.boxlayout import BoxLayout  # For organizing widgets in rows/columns
from kivy.uix.gridlayout import GridLayout  # For grid-based layouts (not used in this version but imported for future use)
from kivy.core.window import Window  # For controlling window properties
from kivy.uix.image import Image  # For displaying images (not used yet but imported for future use)
from kivy.graphics import Color, Rectangle  # For custom graphics and styling
from kivy.core.text import LabelBase  # For custom fonts (not used yet but imported for future use)
from kivy.resources import resource_add_path  # For managing app resources
import os  # For file system operations

# Set the window size for development (this will be fullscreen on mobile devices)
# This helps us see how the app will look on mobile while developing on desktop
Window.size = (400, 800)  # Width: 400px, Height: 800px (typical mobile aspect ratio)

class LandingScreen(Screen):
    """
    The main landing page of the game - this is the first screen users see
    Contains the game title, subtitle, and main menu buttons
    """
    def __init__(self, **kwargs):
        # Call the parent class (Screen) constructor first
        super().__init__(**kwargs)
        
        # Create the main layout - vertical means widgets stack from top to bottom
        # padding=20 adds space around the edges, spacing=20 adds space between widgets
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Create the main title label
        title = Label(
            text='DEMONLING',  # The text to display
            font_size='48sp',  # Font size (sp = scale-independent pixels)
            size_hint_y=None,  # Don't auto-size height
            height=100,  # Set fixed height of 100 pixels
            color=(1, 0.5, 0, 1)  # Orange color (Red=1, Green=0.5, Blue=0, Alpha=1)
        )
        
        # Create subtitle label
        subtitle = Label(
            text='Turn-Based RPG Adventure',
            font_size='18sp',
            size_hint_y=None,
            height=50,
            color=(0.8, 0.8, 0.8, 1)  # Light gray color
        )
        
        # Create a container for all the menu buttons
        # This keeps them grouped together and properly spaced
        button_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, height=300)
        
        # Create the "Start Game" button
        start_button = Button(
            text='Start Game',
            size_hint_y=None,  # Don't auto-size height
            height=60,  # Fixed height of 60 pixels
            background_color=(0.2, 0.8, 0.2, 1),  # Green color
            color=(1, 1, 1, 1),  # White text color
            font_size='20sp'
        )
        # Bind the button click to the start_game method
        start_button.bind(on_press=self.start_game)
        
        # Create the "Load Game" button
        load_button = Button(
            text='Load Game',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.6, 0.8, 1),  # Blue color
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        load_button.bind(on_press=self.load_game)
        
        # Create the "Settings" button
        settings_button = Button(
            text='Settings',
            size_hint_y=None,
            height=60,
            background_color=(0.8, 0.6, 0.2, 1),  # Orange color
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        settings_button.bind(on_press=self.open_settings)
        
        # Create the "Credits" button
        credits_button = Button(
            text='Credits',
            size_hint_y=None,
            height=60,
            background_color=(0.6, 0.2, 0.8, 1),  # Purple color
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        credits_button.bind(on_press=self.open_credits)
        
        # Add all buttons to the button layout container
        button_layout.add_widget(start_button)
        button_layout.add_widget(load_button)
        button_layout.add_widget(settings_button)
        button_layout.add_widget(credits_button)
        
        # Add all main elements to the main layout
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(button_layout)
        
        # Add a spacer label that takes up remaining space
        # This pushes the version info to the bottom
        layout.add_widget(Label(size_hint_y=1))
        
        # Create version info label at the bottom
        version_label = Label(
            text='Version 1.0.0',
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),  # Gray color
            size_hint_y=None,
            height=30
        )
        layout.add_widget(version_label)
        
        # Add the main layout to this screen
        self.add_widget(layout)
    
    # Method called when "Start Game" button is pressed
    def start_game(self, instance):
        # Switch to the game screen
        # self.manager is the ScreenManager that controls all screens
        self.manager.current = 'game_screen'
    
    # Method called when "Load Game" button is pressed
    def load_game(self, instance):
        self.manager.current = 'load_screen'
    
    # Method called when "Settings" button is pressed
    def open_settings(self, instance):
        self.manager.current = 'settings_screen'
    
    # Method called when "Credits" button is pressed
    def open_credits(self, instance):
        self.manager.current = 'credits_screen'

class GameScreen(Screen):
    """
    The main game screen - this is where the actual game will be played
    Currently shows placeholder content, but will contain the game interface
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create main layout for this screen
        layout = BoxLayout(orientation='vertical', padding=20)
        
        # Create header section with back button and title
        header = BoxLayout(size_hint_y=None, height=60)
        
        # Create back button to return to main menu
        back_button = Button(
            text='← Back',  # Arrow symbol for back
            size_hint_x=None,  # Don't auto-size width
            width=80,  # Fixed width
            background_color=(0.6, 0.6, 0.6, 1)  # Gray color
        )
        back_button.bind(on_press=self.go_back)
        
        # Create screen title
        title = Label(text='Game Screen', font_size='24sp')
        
        # Add back button and title to header
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Create content area for the main game content
        content = BoxLayout(orientation='vertical', spacing=20)
        
        # Create placeholder content explaining what will be here
        placeholder = Label(
            text='🎮\n\nGame Screen\n\nThis is where the main game\nwill be implemented.\n\nFeatures to come:\n• Character creation\n• Turn-based combat\n• Quest system\n• Inventory management\n• World exploration',
            font_size='18sp',
            halign='center'  # Center-align the text
        )
        
        # Add placeholder to content area
        content.add_widget(placeholder)
        
        # Add header and content to main layout
        layout.add_widget(header)
        layout.add_widget(content)
        
        # Add main layout to this screen
        self.add_widget(layout)
    
    # Method called when back button is pressed
    def go_back(self, instance):
        self.manager.current = 'landing'  # Return to landing screen

class LoadScreen(Screen):
    """
    Screen for loading saved games
    Will contain a list of save files and options to load/delete them
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=20)
        
        # Create header with back button and title
        header = BoxLayout(size_hint_y=None, height=60)
        back_button = Button(
            text='← Back',
            size_hint_x=None,
            width=80,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_button.bind(on_press=self.go_back)
        
        title = Label(text='Load Game', font_size='24sp')
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Create content area
        content = BoxLayout(orientation='vertical', spacing=20)
        
        # Placeholder content for save/load functionality
        placeholder = Label(
            text='📁\n\nLoad Game Screen\n\nThis is where saved games\nwill be displayed.\n\nFeatures to come:\n• Save file list\n• Save file details\n• Delete save files\n• Cloud save support',
            font_size='18sp',
            halign='center'
        )
        
        content.add_widget(placeholder)
        
        layout.add_widget(header)
        layout.add_widget(content)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'landing'

class SettingsScreen(Screen):
    """
    Screen for game settings and configuration
    Will contain options like sound volume, graphics quality, etc.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=20)
        
        # Create header
        header = BoxLayout(size_hint_y=None, height=60)
        back_button = Button(
            text='← Back',
            size_hint_x=None,
            width=80,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_button.bind(on_press=self.go_back)
        
        title = Label(text='Settings', font_size='24sp')
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Create content area
        content = BoxLayout(orientation='vertical', spacing=20)
        
        # Placeholder content for settings
        placeholder = Label(
            text='⚙️\n\nSettings Screen\n\nThis is where game settings\nwill be configured.\n\nFeatures to come:\n• Sound volume\n• Music volume\n• Graphics quality\n• Control settings\n• Language options',
            font_size='18sp',
            halign='center'
        )
        
        content.add_widget(placeholder)
        
        layout.add_widget(header)
        layout.add_widget(content)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'landing'

class CreditsScreen(Screen):
    """
    Screen showing game credits and acknowledgments
    Contains information about the development team and thanks
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=20)
        
        # Create header
        header = BoxLayout(size_hint_y=None, height=60)
        back_button = Button(
            text='← Back',
            size_hint_x=None,
            width=80,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_button.bind(on_press=self.go_back)
        
        title = Label(text='Credits', font_size='24sp')
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Create content area
        content = BoxLayout(orientation='vertical', spacing=20)
        
        # Multi-line credits text using triple quotes for better formatting
        credits_text = """
🎭

Credits Screen

Game: Demonling
Genre: Turn-Based RPG

Development Team:
• Game Design & Programming
• UI/UX Design
• Sound Design
• Testing

Special Thanks:
• Kivy Framework
• Python Community
• Beta Testers

© 2024 Demonling Team
        """
        
        # Create label with credits text
        placeholder = Label(
            text=credits_text,
            font_size='16sp',
            halign='center'
        )
        
        content.add_widget(placeholder)
        
        layout.add_widget(header)
        layout.add_widget(content)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'landing'

class DemonlingApp(App):
    """
    Main application class - this is the entry point of the Kivy app
    Inherits from App and must implement the build() method
    """
    def build(self):
        """
        This method is called by Kivy when the app starts
        It should return the root widget of the application
        """
        # Create a screen manager to handle navigation between screens
        sm = ScreenManager()
        
        # Add all the screens to the screen manager
        # Each screen has a unique name that we use to navigate to it
        sm.add_widget(LandingScreen(name='landing'))  # Main menu screen
        sm.add_widget(GameScreen(name='game_screen'))  # Game play screen
        sm.add_widget(LoadScreen(name='load_screen'))  # Load game screen
        sm.add_widget(SettingsScreen(name='settings_screen'))  # Settings screen
        sm.add_widget(CreditsScreen(name='credits_screen'))  # Credits screen
        
        # Return the screen manager as the root widget
        return sm

# This is the standard Python way to check if this file is being run directly
# (not imported as a module)
if __name__ == '__main__':
    # Create and run the app
    DemonlingApp().run() 