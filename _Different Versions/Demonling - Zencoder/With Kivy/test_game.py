#!/usr/bin/env python3
"""
Test script for Demonling game
Tests core game functionality without UI
"""

import time
from game_manager import GameManager
from player import Player
from quest_system import QuestManager
from combat_system import CombatManager

def test_player_creation():
    """Test player creation and stats"""
    print("Testing Player Creation...")
    player = Player()
    
    assert player.level == 1
    assert player.health == 20
    assert player.attack == 5
    assert player.defense == 2
    assert player.gold == 10
    assert player.energy == 10
    
    print("✓ Player creation test passed")

def test_player_leveling():
    """Test player leveling system"""
    print("Testing Player Leveling...")
    player = Player()
    
    # Add enough XP to level up
    player.add_xp(100)
    
    assert player.level == 2
    assert player.health == 25  # Base 20 + 5 per level
    assert player.attack == 7   # Base 5 + 2 per level
    
    print("✓ Player leveling test passed")

def test_quest_system():
    """Test quest system functionality"""
    print("Testing Quest System...")
    quest_manager = QuestManager()
    player = Player()
    
    # Check initial quest state
    assert quest_manager.is_quest_unlocked("ash_bone_01")
    assert not quest_manager.is_quest_unlocked("ash_bone_02")
    assert not quest_manager.is_quest_completed("ash_bone_01")
    
    # Complete first quest
    quest_manager.complete_quest("ash_bone_01")
    
    assert quest_manager.is_quest_completed("ash_bone_01")
    assert quest_manager.is_quest_unlocked("ash_bone_02")
    
    print("✓ Quest system test passed")

def test_combat_system():
    """Test combat system"""
    print("Testing Combat System...")
    combat_manager = CombatManager()
    player = Player()
    
    # Get first quest's enemy
    quest_manager = QuestManager()
    quest = quest_manager.get_quest("ash_bone_01")
    enemy = quest.enemy
    
    # Start combat
    combat_manager.start_combat(player, enemy)
    
    # Check initial state
    combat_state = combat_manager.get_combat_state()
    assert combat_state['player_health'] == 20
    assert combat_state['enemy_health'] == 15
    assert combat_state['combat_state'] == 'player_turn'
    
    print("✓ Combat system test passed")

def test_game_manager():
    """Test game manager integration"""
    print("Testing Game Manager...")
    game_manager = GameManager()
    
    # Test quest starting
    success = game_manager.start_quest("ash_bone_01")
    assert success
    assert game_manager.current_quest is not None
    assert game_manager.player.energy == 9  # Started with 10, spent 1
    
    print("✓ Game manager test passed")

def test_save_load():
    """Test save/load functionality"""
    print("Testing Save/Load...")
    game_manager = GameManager()
    
    # Modify player stats
    game_manager.player.add_xp(50)
    game_manager.player.add_gold(25)
    original_level = game_manager.player.level
    original_xp = game_manager.player.xp
    original_gold = game_manager.player.gold
    
    # Save game
    game_manager.save_game()
    
    # Create new game manager and load
    game_manager2 = GameManager()
    game_manager2.load_game()
    
    # Check if data was preserved
    assert game_manager2.player.level == original_level
    assert game_manager2.player.xp == original_xp
    assert game_manager2.player.gold == original_gold
    
    print("✓ Save/load test passed")

def test_energy_system():
    """Test energy regeneration"""
    print("Testing Energy System...")
    game_manager = GameManager()
    
    # Spend some energy
    game_manager.player.spend_energy(5)
    assert game_manager.player.energy == 5
    
    # Simulate time passing (mock)
    old_time = game_manager.last_energy_update
    game_manager.last_energy_update = old_time - 600  # 10 minutes ago
    
    # Update energy
    game_manager.update_energy()
    
    # Should have regenerated some energy
    assert game_manager.player.energy > 5
    
    print("✓ Energy system test passed")

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("DEMONLING GAME TESTS")
    print("=" * 50)
    
    try:
        test_player_creation()
        test_player_leveling()
        test_quest_system()
        test_combat_system()
        test_game_manager()
        test_save_load()
        test_energy_system()
        
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED! ✓")
        print("The game is ready to run!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()