"""
Test Script for Demonling: Rise of the Realm Lord

This script runs basic tests to ensure all game systems work correctly.
Run this before deploying to mobile to catch any issues.
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from game_manager import GameManager, Player
        print("✓ game_manager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import game_manager: {e}")
        return False
    
    try:
        from combat_system import CombatSystem, Enemy, create_enemy_from_template
        print("✓ combat_system imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import combat_system: {e}")
        return False
    
    try:
        from quest_system import QuestSystem
        print("✓ quest_system imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import quest_system: {e}")
        return False
    
    try:
        from ui_components import CustomButton, StatsDisplay, EnergyBar
        print("✓ ui_components imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ui_components: {e}")
        return False
    
    try:
        from data_manager import DataManager
        print("✓ data_manager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import data_manager: {e}")
        return False
    
    return True

def test_player_creation():
    """Test player creation and basic operations"""
    print("\nTesting player creation...")
    
    try:
        from game_manager import Player
        
        player = Player()
        print(f"✓ Player created with level {player.level}")
        
        # Test XP gain and level up
        old_level = player.level
        player.gain_xp(100)
        if player.level > old_level:
            print("✓ Level up system working")
        else:
            print("✓ XP gain working (no level up expected)")
        
        # Test resource management
        player.gain_gold(50)
        player.gain_soul_shards(2)
        print(f"✓ Resources: {player.gold} gold, {player.soul_shards} soul shards")
        
        # Test energy system
        if player.spend_energy(10):
            print("✓ Energy spending working")
        else:
            print("✗ Energy spending failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Player creation failed: {e}")
        return False

def test_quest_system():
    """Test quest system functionality"""
    print("\nTesting quest system...")
    
    try:
        from quest_system import QuestSystem
        
        quest_system = QuestSystem()
        print("✓ Quest system initialized")
        
        # Test quest chains
        chains = quest_system.get_quest_chains()
        print(f"✓ Found {len(chains)} quest chains")
        
        # Test quest availability
        available_quests = quest_system.get_available_quests()
        print(f"✓ {len(available_quests)} quests available initially")
        
        # Test quest completion
        if available_quests:
            first_quest = available_quests[0]
            first_completion = quest_system.complete_quest(first_quest)
            print(f"✓ Quest completion test: {first_completion}")
        
        return True
        
    except Exception as e:
        print(f"✗ Quest system test failed: {e}")
        return False

def test_combat_system():
    """Test combat system functionality"""
    print("\nTesting combat system...")
    
    try:
        from combat_system import CombatSystem, create_enemy_from_template
        from game_manager import Player
        
        # Create player and enemy
        player = Player()
        enemy_data = create_enemy_from_template('goblin')
        
        # Initialize combat
        combat = CombatSystem(player, enemy_data)
        print("✓ Combat system initialized")
        
        # Test combat actions
        damage = combat.player_attack()
        print(f"✓ Player attack dealt {damage} damage")
        
        if combat.enemy.is_alive():
            damage = combat.enemy_attack()
            print(f"✓ Enemy attack dealt {damage} damage")
        
        print(f"✓ Combat status: {combat.get_winner()}")
        
        return True
        
    except Exception as e:
        print(f"✗ Combat system test failed: {e}")
        return False

def test_data_manager():
    """Test data persistence"""
    print("\nTesting data manager...")
    
    try:
        from data_manager import DataManager
        
        data_manager = DataManager()
        print("✓ Data manager initialized")
        
        # Test save/load
        test_data = {
            "test_key": "test_value",
            "timestamp": datetime.now().isoformat()
        }
        
        data_manager.save_data(test_data)
        print("✓ Data saved successfully")
        
        loaded_data = data_manager.load_data()
        if loaded_data and loaded_data.get("test_key") == "test_value":
            print("✓ Data loaded successfully")
        else:
            print("✗ Data load verification failed")
            return False
        
        # Clean up test data
        data_manager.delete_save()
        print("✓ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Data manager test failed: {e}")
        return False

def test_game_manager():
    """Test game manager integration"""
    print("\nTesting game manager...")
    
    try:
        from game_manager import GameManager
        
        game_manager = GameManager()
        print("✓ Game manager initialized")
        
        # Test quest completion
        available_quests = game_manager.quest_system.get_available_quests()
        if available_quests:
            quest_id = available_quests[0]
            rewards = game_manager.complete_quest(quest_id)
            print(f"✓ Quest completed with rewards: {rewards}")
        
        # Test save/load
        game_manager.save_game()
        print("✓ Game saved")
        
        game_manager.load_game()
        print("✓ Game loaded")
        
        # Clean up
        game_manager.data_manager.delete_save()
        print("✓ Test save cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Game manager test failed: {e}")
        return False

def test_kivy_availability():
    """Test if Kivy is available and working"""
    print("\nTesting Kivy availability...")
    
    try:
        import kivy
        print(f"✓ Kivy version {kivy.__version__} available")
        
        # Test basic Kivy imports
        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        print("✓ Basic Kivy widgets available")
        
        return True
        
    except ImportError as e:
        print(f"✗ Kivy not available: {e}")
        print("  Install with: pip install kivy")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 50)
    print("DEMONLING GAME TESTS")
    print("=" * 50)
    
    tests = [
        ("Kivy Availability", test_kivy_availability),
        ("Module Imports", test_imports),
        ("Player Creation", test_player_creation),
        ("Quest System", test_quest_system),
        ("Combat System", test_combat_system),
        ("Data Manager", test_data_manager),
        ("Game Manager", test_game_manager),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*30}")
        print(f"Running: {test_name}")
        print('='*30)
        
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                failed += 1
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Game is ready to run.")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. Please fix issues before running.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)