# main.py for Demonling: Rise of the Realm Lord (with MVP Combat)

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, DictProperty, ListProperty
import time
import random

# --- Game Data ---
# Player stats now include combat attributes
INITIAL_PLAYER_STATS = {
    "level": 1, "xp": 0, "xp_to_next_level": 100,
    "gold": 50, "soul_shards": 0,
    "max_energy": 20, "current_energy": 20, "last_energy_update": time.time(),
    "max_hp": 50, "current_hp": 50,
    "attack": 8, "defense": 4,
    "completed_quests": []  # List of quest IDs completed
}

# Enemies for our quests
ENEMIES = {
    "skeleton_grunt": {"name": "Skeleton Grunt", "hp": 20, "attack": 6, "defense": 2},
    "skeletal_archer": {"name": "Skeletal Archer", "hp": 15, "attack": 8, "defense": 1},
    "bone_collector": {"name": "The Bone Collector", "hp": 40, "attack": 10, "defense": 5}
}

# Quests now have an associated enemy
QUEST_CHAINS = {
    "Ash & Bone": [
        {"id": "ab_1", "name": "First Steps", "cost": 5, "xp": 10, "gold": 5, "enemy": "skeleton_grunt"},
        {"id": "ab_2", "name": "Skeletal Skirmish", "cost": 5, "xp": 15, "gold": 10, "enemy": "skeletal_archer"},
        {"id": "ab_3", "name": "The Bone Collector", "cost": 8, "xp": 25, "gold": 20, "enemy": "bone_collector"},
    ]
}


class HomeScreen(Screen):
    """The main screen of the game, displaying player stats and navigation."""
    pass


class QuestChainScreen(Screen):
    """Displays the list of available quest chains."""

    def on_enter(self, *args):
        layout = self.ids.quest_chain_list
        layout.clear_widgets()
        for chain_name in QUEST_CHAINS.keys():
            btn = Button(text=chain_name, size_hint_y=None, height=40)
            btn.bind(on_press=lambda instance, name=chain_name: self.select_chain(name))
            layout.add_widget(btn)

    def select_chain(self, chain_name):
        self.manager.get_screen('quest_list').set_quest_chain(chain_name)
        self.manager.current = 'quest_list'


class QuestListScreen(Screen):
    """Displays the individual quests within a selected chain."""
    current_chain_name = StringProperty("")

    def set_quest_chain(self, chain_name):
        self.current_chain_name = chain_name

    def on_enter(self, *args):
        self.update_quest_list()

    def update_quest_list(self):
        layout = self.ids.quest_list
        layout.clear_widgets()
        if not self.current_chain_name: return

        app = App.get_running_app()
        quests = QUEST_CHAINS[self.current_chain_name]

        # Determine quest status based on completion
        for i, quest in enumerate(quests):
            status = "locked"
            if i == 0 and quest['id'] not in app.player_stats['completed_quests']:
                status = "unlocked"  # First quest is always unlocked initially
            elif quest['id'] in app.player_stats['completed_quests']:
                status = "completed"
            # Check if previous quest was completed to unlock this one
            elif i > 0 and quests[i - 1]['id'] in app.player_stats['completed_quests']:
                status = "unlocked"

            status_icon = {"locked": "🔒", "unlocked": "🟢", "completed": "✅"}[status]
            quest_text = f"{status_icon} {quest['name']} (Cost: {quest['cost']} E)"
            btn = Button(text=quest_text, size_hint_y=None, height=40)
            if status != "locked":
                btn.bind(on_press=lambda instance, q=quest: self.start_quest(q))
            else:
                btn.disabled = True
            layout.add_widget(btn)

    def start_quest(self, quest_data):
        app = App.get_running_app()
        if app.player_stats['current_energy'] >= quest_data['cost']:
            app.player_stats['current_energy'] -= quest_data['cost']
            app.start_combat(quest_data)
        else:
            print("Not enough energy!")


class CombatScreen(Screen):
    """Screen for handling the turn-based combat."""
    player_hp = NumericProperty(0)
    player_max_hp = NumericProperty(1)
    enemy_hp = NumericProperty(0)
    enemy_max_hp = NumericProperty(1)
    enemy_name = StringProperty("")
    log_text = StringProperty("")

    def on_enter(self, *args):
        """Called when the combat screen is displayed. Sets up the initial state."""
        app = App.get_running_app()
        self.player_defending = False

        # Player stats
        self.player_hp = app.player_stats['current_hp']
        self.player_max_hp = app.player_stats['max_hp']

        # Enemy stats
        enemy_template = ENEMIES[app.current_quest['enemy']]
        self.enemy_name = enemy_template['name']
        self.enemy_hp = enemy_template['hp']
        self.enemy_max_hp = enemy_template['hp']
        self.enemy_attack = enemy_template['attack']
        self.enemy_defense = enemy_template['defense']

        self.ids.action_buttons.disabled = False
        self.log_text = f"A wild {self.enemy_name} appears!"

    def player_attack_action(self):
        """Player chooses to attack."""
        app = App.get_running_app()
        damage = max(1, app.player_stats['attack'] - self.enemy_defense)
        self.enemy_hp -= damage
        self.log_text = f"You attack the {self.enemy_name} for {damage} damage."
        self.check_for_win()

    def player_defend_action(self):
        """Player chooses to defend."""
        self.player_defending = True
        self.log_text = "You brace for the enemy's attack."
        self.end_player_turn()

    def check_for_win(self):
        """Check if the enemy is defeated."""
        if self.enemy_hp <= 0:
            self.enemy_hp = 0
            self.log_text += f"\nYou have defeated the {self.enemy_name}!"
            self.ids.action_buttons.disabled = True
            Clock.schedule_once(App.get_running_app().end_combat_victory, 2)
        else:
            self.end_player_turn()

    def end_player_turn(self):
        """Disables player controls and schedules the enemy's turn."""
        self.ids.action_buttons.disabled = True
        Clock.schedule_once(self.enemy_turn, 1.5)

    def enemy_turn(self, dt):
        """The enemy performs its action."""
        app = App.get_running_app()

        player_defense = app.player_stats['defense']
        if self.player_defending:
            player_defense *= 2  # Double defense if defending
            self.player_defending = False

        damage = max(1, self.enemy_attack - player_defense)
        self.player_hp -= damage

        self.log_text += f"\nThe {self.enemy_name} attacks you for {damage} damage."

        if self.player_hp <= 0:
            self.player_hp = 0
            self.log_text += "\nYou have been defeated!"
            Clock.schedule_once(App.get_running_app().end_combat_defeat, 2)
        else:
            # It's the player's turn again
            self.ids.action_buttons.disabled = False
            self.log_text += "\nYour turn!"


class DemonlingApp(App):
    """The main application class."""
    player_stats = DictProperty(INITIAL_PLAYER_STATS)
    ENERGY_REGEN_RATE = 300  # 5 minutes per energy

    def build(self):
        self.sm = ScreenManager(transition=FadeTransition(duration=0.2))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(QuestChainScreen(name='quest_chains'))
        self.sm.add_widget(QuestListScreen(name='quest_list'))
        self.sm.add_widget(CombatScreen(name='combat'))

        Clock.schedule_interval(self.regenerate_energy, 1)
        self.regenerate_energy()
        return self.sm

    def on_start(self):
        """Called when the app starts. Restore HP."""
        self.player_stats['current_hp'] = self.player_stats['max_hp']

    def regenerate_energy(self, dt=0):
        if self.player_stats['current_energy'] >= self.player_stats['max_energy']:
            self.player_stats['last_energy_update'] = time.time()
            return
        time_passed = time.time() - self.player_stats['last_energy_update']
        energy_gained = int(time_passed // self.ENERGY_REGEN_RATE)
        if energy_gained > 0:
            new_energy = self.player_stats['current_energy'] + energy_gained
            self.player_stats['current_energy'] = min(new_energy, self.player_stats['max_energy'])
            self.player_stats['last_energy_update'] += energy_gained * self.ENERGY_REGEN_RATE

    def refill_energy(self):
        self.player_stats['current_energy'] = self.player_stats['max_energy']

    def go_to_screen(self, screen_name):
        self.sm.current = screen_name

    def start_combat(self, quest_data):
        self.current_quest = quest_data
        # Restore player HP before each fight
        self.player_stats['current_hp'] = self.player_stats['max_hp']
        self.go_to_screen('combat')

    def end_combat_victory(self, dt):
        """Handles rewards and progression after winning a fight."""
        quest = self.current_quest
        self.player_stats['xp'] += quest['xp']
        self.player_stats['gold'] += quest['gold']

        # Grant soul shard only on first completion
        if quest['id'] not in self.player_stats['completed_quests']:
            self.player_stats['soul_shards'] += 1
            self.player_stats['completed_quests'].append(quest['id'])

        # Check for level up
        if self.player_stats['xp'] >= self.player_stats['xp_to_next_level']:
            self.level_up()

        self.go_to_screen('quest_list')

    def end_combat_defeat(self, dt):
        """Handles returning to the main menu after a loss."""
        # Restore HP after defeat
        self.player_stats['current_hp'] = self.player_stats['max_hp']
        self.go_to_screen('home')

    def level_up(self):
        """Handles player leveling up."""
        self.player_stats['level'] += 1
        self.player_stats['xp'] -= self.player_stats['xp_to_next_level']
        self.player_stats['xp_to_next_level'] = int(
            self.player_stats['xp_to_next_level'] * 1.5)  # Increase XP requirement

        # Increase stats on level up
        self.player_stats['max_hp'] += 10
        self.player_stats['attack'] += 2
        self.player_stats['defense'] += 1
        self.player_stats['current_hp'] = self.player_stats['max_hp']
        print("LEVEL UP!")


from kivy.lang import Builder

Builder.load_string("""
#:kivy 2.1.0

# Define some colors for the UI
#:set color_bg (0.1, 0.1, 0.1, 1)
#:set color_fg (0.8, 0.8, 0.8, 1)
#:set color_accent (0.5, 0.2, 0.8, 1)

<Button>:
    background_color: (0.2, 0.2, 0.2, 1)
    background_normal: ''
    border: (5, 5, 5, 5)

<Label>:
    color: color_fg

<Screen>:
    canvas.before:
        Color:
            rgba: color_bg
        Rectangle:
            pos: self.pos
            size: self.size

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        Label:
            text: 'Demonling'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: 40
        Label:
            id: xp_label
            text: f"LVL: {app.player_stats['level']} | XP: {app.player_stats['xp']} / {app.player_stats['xp_to_next_level']}"
            size_hint_y: None
            height: 20
        GridLayout:
            size_hint_y: None
            height: 40
            cols: 3
            Label:
                text: f"Gold: {app.player_stats['gold']}"
            Label:
                id: energy_label
                text: f"Energy: {app.player_stats['current_energy']} / {app.player_stats['max_energy']}"
            Label:
                text: f"Shards: {app.player_stats['soul_shards']}"
        Label: # Spacer
        BoxLayout:
            size_hint_y: None
            height: 50
            Button:
                text: 'Quests'
                on_press: app.go_to_screen('quest_chains')
            Button:
                text: 'Castle'
                disabled: True
            Button:
                text: 'Army'
                disabled: True
        Button:
            size_hint_y: None
            height: 40
            text: 'Refill Energy (Test)'
            on_press: app.refill_energy()

<QuestChainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10; spacing: 10
        Label:
            text: 'Quest Chains'
            font_size: '20sp'
            size_hint_y: None; height: 40
        ScrollView:
            GridLayout:
                id: quest_chain_list
                cols: 1
                size_hint_y: None; height: self.minimum_height; spacing: 5
        Button:
            text: 'Back'
            size_hint_y: None; height: 40
            on_press: app.go_to_screen('home')

<QuestListScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10; spacing: 10
        Label:
            text: root.current_chain_name
            font_size: '20sp'
            size_hint_y: None; height: 40
        ScrollView:
            GridLayout:
                id: quest_list
                cols: 1
                size_hint_y: None; height: self.minimum_height; spacing: 5
        Button:
            text: 'Back'
            size_hint_y: None; height: 40
            on_press: app.go_to_screen('quest_chains')

<CombatScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        # Enemy Info
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.3
            Label:
                text: root.enemy_name
                font_size: '22sp'
                bold: True
            Label:
                text: f"HP: {int(root.enemy_hp)} / {root.enemy_max_hp}"
                font_size: '18sp'

        # Spacer
        Label:
            size_hint_y: 0.2

        # Player Info
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.3
            Label:
                text: 'Player'
                font_size: '22sp'
                bold: True
            Label:
                text: f"HP: {int(root.player_hp)} / {root.player_max_hp}"
                font_size: '18sp'

        # Combat Log
        Label:
            id: combat_log
            text: root.log_text
            size_hint_y: 0.2
            text_size: self.width, None
            halign: 'center'
            valign: 'middle'

        # Action Buttons
        GridLayout:
            id: action_buttons
            cols: 2
            size_hint_y: None
            height: 60
            spacing: 10
            Button:
                text: 'Attack'
                on_press: root.player_attack_action()
            Button:
                text: 'Defend'
                on_press: root.player_defend_action()

""")

if __name__ == '__main__':
    DemonlingApp().run()
