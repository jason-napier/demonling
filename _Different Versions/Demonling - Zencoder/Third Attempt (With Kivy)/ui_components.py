"""
UI Components Module

This module contains custom UI components and widgets
that are used throughout the Demonling game interface.
"""

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.animation import Animation

class CustomButton(Button):
    """
    Custom button with enhanced styling and demonic theme, optimized for mobile.
    """
    
    def __init__(self, **kwargs):
        # Set default properties for demonic theme and mobile usage
        if 'background_color' not in kwargs:
            kwargs['background_color'] = (0.8, 0.2, 0.2, 1)  # Dark red
        if 'font_size' not in kwargs:
            kwargs['font_size'] = '18sp'  # Larger for mobile
        if 'bold' not in kwargs:
            kwargs['bold'] = True
        
        # Mobile-friendly minimum size
        if 'size_hint_y' not in kwargs and 'height' not in kwargs:
            kwargs['size_hint_y'] = None
            kwargs['height'] = '48dp'  # Minimum 48dp for mobile touch targets
        
        super().__init__(**kwargs)
        
        # Add press animation
        self.bind(on_press=self.on_button_press)
        self.bind(on_release=self.on_button_release)
        
        # Add visual enhancements
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.3)  # Dark shadow
            self.shadow_rect = Rectangle(pos=(self.x + 2, self.y - 2), size=self.size)
        
        self.bind(pos=self.update_shadow, size=self.update_shadow)
        
    def update_shadow(self, *args):
        """Update shadow rectangle position"""
        self.shadow_rect.pos = (self.x + 2, self.y - 2)
        self.shadow_rect.size = self.size
        
    def on_button_press(self, instance):
        """Animate button press with opacity effect"""
        Animation(opacity=0.7, duration=0.1).start(self)
        
    def on_button_release(self, instance):
        """Animate button release"""
        Animation(opacity=1.0, duration=0.1).start(self)

class StatsDisplay(BoxLayout):
    """
    Custom widget for displaying player stats in a formatted way.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.size_hint_y = None
        self.height = 200
        
        # Create stat labels
        self.stat_labels = {}
        self.setup_stats_display()
        
    def setup_stats_display(self):
        """Setup the stats display layout"""
        # Create a grid for stats
        stats_grid = GridLayout(cols=2, spacing=10)
        
        # Define stats to display
        stats = [
            ('level', 'Level'),
            ('xp', 'Experience'),
            ('gold', 'Gold'),
            ('soul_shards', 'Soul Shards'),
            ('attack', 'Attack'),
            ('defense', 'Defense'),
            ('agility', 'Agility'),
            ('magic', 'Magic')
        ]
        
        # Create labels for each stat
        for stat_key, stat_name in stats:
            label = Label(
                text=f'{stat_name}: 0',
                font_size='14sp',
                halign='left',
                valign='middle'
            )
            label.bind(size=label.setter('text_size'))
            self.stat_labels[stat_key] = label
            stats_grid.add_widget(label)
            
        self.add_widget(stats_grid)
        
    def update_stats(self, stats_dict):
        """
        Update displayed stats.
        
        Args:
            stats_dict (dict): Dictionary of stats to display
        """
        for stat_key, value in stats_dict.items():
            if stat_key in self.stat_labels:
                stat_name = self.stat_labels[stat_key].text.split(':')[0]
                self.stat_labels[stat_key].text = f'{stat_name}: {value}'

class EnergyBar(BoxLayout):
    """
    Custom energy bar widget with label and progress bar.
    """
    
    current_energy = NumericProperty(100)
    max_energy = NumericProperty(100)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 60
        
        # Energy label
        self.energy_label = Label(
            text='Energy: 100/100',
            font_size='14sp',
            size_hint_y=None,
            height=20
        )
        self.add_widget(self.energy_label)
        
        # Progress bar
        self.progress_bar = ProgressBar(
            max=100,
            value=100,
            size_hint_y=None,
            height=20
        )
        self.add_widget(self.progress_bar)
        
        # Bind properties
        self.bind(current_energy=self.update_display)
        self.bind(max_energy=self.update_display)
        
    def update_display(self, *args):
        """Update the energy display"""
        self.energy_label.text = f'Energy: {int(self.current_energy)}/{int(self.max_energy)}'
        self.progress_bar.max = self.max_energy
        self.progress_bar.value = self.current_energy
        
        # Change color based on energy level
        energy_ratio = self.current_energy / self.max_energy if self.max_energy > 0 else 0
        
        if energy_ratio > 0.7:
            # Green for high energy
            self.progress_bar.background_color = (0.2, 0.8, 0.2, 1)
        elif energy_ratio > 0.3:
            # Yellow for medium energy
            self.progress_bar.background_color = (0.8, 0.8, 0.2, 1)
        else:
            # Red for low energy
            self.progress_bar.background_color = (0.8, 0.2, 0.2, 1)

class HealthBar(BoxLayout):
    """
    Custom health bar widget for combat display.
    """
    
    current_health = NumericProperty(100)
    max_health = NumericProperty(100)
    entity_name = StringProperty("Entity")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 60
        
        # Health label
        self.health_label = Label(
            text='Health: 100/100',
            font_size='14sp',
            size_hint_y=None,
            height=20
        )
        self.add_widget(self.health_label)
        
        # Progress bar
        self.progress_bar = ProgressBar(
            max=100,
            value=100,
            size_hint_y=None,
            height=20
        )
        self.add_widget(self.progress_bar)
        
        # Bind properties
        self.bind(current_health=self.update_display)
        self.bind(max_health=self.update_display)
        self.bind(entity_name=self.update_display)
        
    def update_display(self, *args):
        """Update the health display"""
        self.health_label.text = f'{self.entity_name}: {int(self.current_health)}/{int(self.max_health)}'
        self.progress_bar.max = self.max_health
        self.progress_bar.value = self.current_health
        
        # Change color based on health level
        health_ratio = self.current_health / self.max_health if self.max_health > 0 else 0
        
        if health_ratio > 0.7:
            # Green for high health
            self.progress_bar.background_color = (0.2, 0.8, 0.2, 1)
        elif health_ratio > 0.3:
            # Yellow for medium health
            self.progress_bar.background_color = (0.8, 0.8, 0.2, 1)
        else:
            # Red for low health
            self.progress_bar.background_color = (0.8, 0.2, 0.2, 1)

class QuestButton(CustomButton):
    """
    Specialized button for quest selection with status indicators.
    """
    
    quest_status = StringProperty("locked")  # locked, available, completed
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(quest_status=self.update_appearance)
        self.update_appearance()
        
    def update_appearance(self, *args):
        """Update button appearance based on quest status"""
        if self.quest_status == "completed":
            self.background_color = (0.2, 0.8, 0.2, 1)  # Green
            self.disabled = False
        elif self.quest_status == "available":
            self.background_color = (0.8, 0.8, 0.2, 1)  # Yellow
            self.disabled = False
        else:  # locked
            self.background_color = (0.5, 0.5, 0.5, 1)  # Gray
            self.disabled = True

class CombatLog(ScrollView):
    """
    Custom scrollable combat log with proper boundaries and mobile-friendly design.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # ScrollView properties for mobile
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.scroll_type = ['bars', 'content']
        self.bar_width = '10dp'
        self.effect_cls = 'ScrollEffect'
        
        # Create the content container
        self.content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing='2dp',
            padding=['5dp', '5dp', '15dp', '5dp']  # Extra right padding for scroll bar
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        # Create the log label
        self.log_label = Label(
            text="Combat begins...",
            font_size='14sp',
            text_size=(None, None),
            valign='top',
            halign='left',
            markup=True,
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1)
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        # Add background for better visibility
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.8)  # Dark semi-transparent background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Add border
        with self.canvas.after:
            Color(0.8, 0.2, 0.2, 1)  # Red border
            self.border_line = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)
        self.bind(pos=self.update_border, size=self.update_border)
        
        self.content_layout.add_widget(self.log_label)
        self.add_widget(self.content_layout)
        
        # Store log messages
        self.log_messages = []
        self.max_messages = 15  # Increased for better mobile experience
        
    def update_bg(self, *args):
        """Update background rectangle"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def update_border(self, *args):
        """Update border line"""
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)
        
    def add_message(self, message, color=None):
        """
        Add a message to the combat log.
        
        Args:
            message (str): Message to add
            color (str): Optional color code for the message
        """
        if color:
            formatted_message = f"[color={color}]{message}[/color]"
        else:
            formatted_message = message
            
        self.log_messages.append(formatted_message)
        
        # Keep only the last N messages
        if len(self.log_messages) > self.max_messages:
            self.log_messages.pop(0)
            
        # Update display
        self.log_label.text = '\n'.join(self.log_messages)
        
        # Update text size for proper wrapping
        self.log_label.text_size = (self.width - 20, None)
        
        # Scroll to bottom
        self.scroll_y = 0
        
    def clear_log(self):
        """Clear all log messages"""
        self.log_messages.clear()
        self.log_label.text = "Combat begins..."
        self.log_label.text_size = (self.width - 20, None)
        self.scroll_y = 1

class ConfirmationPopup(Popup):
    """
    Custom popup for confirmation dialogs.
    """
    
    def __init__(self, message, on_confirm=None, on_cancel=None, **kwargs):
        super().__init__(**kwargs)
        
        self.title = "Confirm"
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False
        
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        # Create content
        content = BoxLayout(orientation='vertical', spacing=10)
        
        # Message
        message_label = Label(
            text=message,
            font_size='16sp',
            text_size=(None, None),
            valign='middle',
            halign='center'
        )
        content.add_widget(message_label)
        
        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        confirm_btn = CustomButton(
            text='Confirm',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        confirm_btn.bind(on_press=self.confirm)
        button_layout.add_widget(confirm_btn)
        
        cancel_btn = CustomButton(
            text='Cancel',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        cancel_btn.bind(on_press=self.cancel)
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(button_layout)
        self.content = content
        
    def confirm(self, instance):
        """Handle confirm action"""
        if self.on_confirm:
            self.on_confirm()
        self.dismiss()
        
    def cancel(self, instance):
        """Handle cancel action"""
        if self.on_cancel:
            self.on_cancel()
        self.dismiss()

class InfoPopup(Popup):
    """
    Custom popup for displaying information.
    """
    
    def __init__(self, message, title="Information", **kwargs):
        super().__init__(**kwargs)
        
        self.title = title
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = True
        
        # Create content
        content = BoxLayout(orientation='vertical', spacing=10)
        
        # Message
        message_label = Label(
            text=message,
            font_size='16sp',
            text_size=(None, None),
            valign='middle',
            halign='center'
        )
        content.add_widget(message_label)
        
        # OK button
        ok_btn = CustomButton(
            text='OK',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        ok_btn.bind(on_press=self.dismiss)
        content.add_widget(ok_btn)
        
        self.content = content

class LoadingSpinner(BoxLayout):
    """
    Custom loading spinner widget.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (100, 100)
        
        # Loading message
        self.loading_label = Label(
            text="Loading...",
            font_size='16sp',
            size_hint_y=None,
            height=30
        )
        self.add_widget(self.loading_label)
        
        # Spinner (simple text animation for now)
        self.spinner_label = Label(
            text="⟳",
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.spinner_label)
        
        # Animation
        self.animation = None
        self.start_animation()
        
    def start_animation(self):
        """Start the loading animation"""
        self.animation = Animation(angle=360, duration=1)
        self.animation.repeat = True
        self.animation.start(self.spinner_label)
        
    def stop_animation(self):
        """Stop the loading animation"""
        if self.animation:
            self.animation.stop(self.spinner_label)

class DemonicTheme:
    """
    Static class containing theme colors and styles for the demonic theme.
    """
    
    # Primary colors
    PRIMARY_RED = (0.8, 0.2, 0.2, 1)
    PRIMARY_DARK = (0.2, 0.2, 0.2, 1)
    PRIMARY_LIGHT = (0.9, 0.9, 0.9, 1)
    
    # Accent colors
    ACCENT_GOLD = (0.9, 0.7, 0.1, 1)
    ACCENT_PURPLE = (0.6, 0.2, 0.8, 1)
    ACCENT_GREEN = (0.2, 0.8, 0.2, 1)
    
    # Status colors
    STATUS_AVAILABLE = (0.8, 0.8, 0.2, 1)
    STATUS_COMPLETED = (0.2, 0.8, 0.2, 1)
    STATUS_LOCKED = (0.5, 0.5, 0.5, 1)
    
    # Health colors
    HEALTH_HIGH = (0.2, 0.8, 0.2, 1)
    HEALTH_MEDIUM = (0.8, 0.8, 0.2, 1)
    HEALTH_LOW = (0.8, 0.2, 0.2, 1)
    
    @staticmethod
    def get_health_color(health_ratio):
        """
        Get health color based on health ratio.
        
        Args:
            health_ratio (float): Health ratio (0.0 to 1.0)
            
        Returns:
            tuple: RGBA color tuple
        """
        if health_ratio > 0.7:
            return DemonicTheme.HEALTH_HIGH
        elif health_ratio > 0.3:
            return DemonicTheme.HEALTH_MEDIUM
        else:
            return DemonicTheme.HEALTH_LOW
            
    @staticmethod
    def get_quest_color(status):
        """
        Get quest button color based on status.
        
        Args:
            status (str): Quest status
            
        Returns:
            tuple: RGBA color tuple
        """
        if status == "completed":
            return DemonicTheme.STATUS_COMPLETED
        elif status == "available":
            return DemonicTheme.STATUS_AVAILABLE
        else:
            return DemonicTheme.STATUS_LOCKED

class CombatLog(BoxLayout):
    """
    Combat log widget that displays combat messages with color coding.
    """
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Create scrollable container
        self.scroll = ScrollView()
        self.log_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing='5dp')
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        
        self.scroll.add_widget(self.log_layout)
        self.add_widget(self.scroll)
        
        # Message history
        self.messages = []
        self.max_messages = 50
        
    def add_message(self, message, color_hex=None):
        """
        Add a message to the combat log.
        
        Args:
            message (str): Message text
            color_hex (str): Hex color code (e.g., 'ff0000' for red)
        """
        # Convert hex to RGBA if provided
        if color_hex:
            try:
                # Remove '#' if present
                color_hex = color_hex.lstrip('#')
                # Convert to RGB values (0-1 range)
                r = int(color_hex[0:2], 16) / 255.0
                g = int(color_hex[2:4], 16) / 255.0
                b = int(color_hex[4:6], 16) / 255.0
                color = (r, g, b, 1)
            except:
                color = (1, 1, 1, 1)  # Default white
        else:
            color = (1, 1, 1, 1)
        
        # Create label
        label = Label(
            text=message,
            color=color,
            font_size='14sp',
            text_size=(None, None),
            size_hint_y=None,
            height='30dp',
            halign='left',
            valign='middle'
        )
        
        # Add to layout
        self.log_layout.add_widget(label)
        self.messages.append(message)
        
        # Remove old messages if too many
        if len(self.messages) > self.max_messages:
            self.log_layout.remove_widget(self.log_layout.children[-1])
            self.messages.pop(0)
        
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)
    
    def scroll_to_bottom(self):
        """Scroll to bottom of log"""
        if self.scroll.scroll_y != 0:
            self.scroll.scroll_y = 0
    
    def clear_log(self):
        """Clear all messages from log"""
        self.log_layout.clear_widgets()
        self.messages.clear()