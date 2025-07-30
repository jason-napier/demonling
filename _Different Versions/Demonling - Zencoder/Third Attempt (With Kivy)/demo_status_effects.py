"""
Demo script to showcase the Status Effects system
"""

from combat_system import *
from game_manager import Player

def demo_status_effects():
    """Demonstrate the status effects functionality"""
    print("=== Demonling Status Effects Demo ===")
    print()
    
    # Create entities
    player = Player()
    player_wrapper = PlayerCombatWrapper(player)
    
    enemy_data = {
        'name': 'Test Demon',
        'attack': 15,
        'defense': 5,
        'agility': 10,
        'magic': 8,
        'health': 80,
        'type': 'demon',
        'ai_behavior': 'aggressive'
    }
    enemy = Enemy(enemy_data)
    
    print("1. Created player and enemy for testing")
    print(f"   Player: {player_wrapper.current_health}/{player_wrapper.max_health} HP")
    print(f"   Enemy: {enemy.current_health}/{enemy.max_health} HP")
    print()
    
    # Test Burned effect
    print("2. Testing Burned effect...")
    burn_effect = BurnedEffect(duration=3, power=5)
    enemy.add_status_effect(burn_effect)
    print(f"   Applied burn to enemy: {enemy.get_status_display()}")
    
    # Simulate 3 turns of burn
    for turn in range(3):
        print(f"   Turn {turn + 1}:")
        enemy.process_turn_start()
        damage, healing, expired = enemy.process_turn_end()
        print(f"     Enemy HP: {enemy.current_health}/{enemy.max_health}")
        print(f"     Status: {enemy.get_status_display()}")
    print()
    
    # Test Frozen effect
    print("3. Testing Frozen effect...")
    freeze_effect = FrozenEffect(duration=2)
    enemy.add_status_effect(freeze_effect)
    print(f"   Applied freeze to enemy: {enemy.get_status_display()}")
    
    for turn in range(2):
        print(f"   Turn {turn + 1}:")
        can_act = enemy.can_act()
        print(f"     Can act: {can_act}")
        enemy.process_turn_start()
        enemy.process_turn_end()
        print(f"     Status: {enemy.get_status_display()}")
    print()
    
    # Test Enraged effect
    print("4. Testing Enraged effect...")
    enrage_effect = EnragedEffect(duration=2, power=3)
    enemy.add_status_effect(enrage_effect)
    print(f"   Applied enrage to enemy: {enemy.get_status_display()}")
    
    base_damage = 20
    modified_damage = enemy.deal_damage(base_damage)
    print(f"   Base damage: {base_damage} -> Modified: {modified_damage}")
    print(f"   Is enraged: {enemy.is_enraged()}")
    print()
    
    # Test Regeneration effect
    print("5. Testing Regeneration effect...")
    player_wrapper.player.current_health = 50  # Simulate damage
    print(f"   Player HP before: {player_wrapper.current_health}/{player_wrapper.max_health}")
    
    regen_effect = RegeneratingEffect(duration=3, power=8)
    player_wrapper.add_status_effect(regen_effect)
    print(f"   Applied regen to player: {player_wrapper.get_status_display()}")
    
    for turn in range(3):
        print(f"   Turn {turn + 1}:")
        player_wrapper.process_turn_start()
        damage, healing, expired = player_wrapper.process_turn_end()
        print(f"     Player HP: {player_wrapper.current_health}/{player_wrapper.max_health}")
        print(f"     Status: {player_wrapper.get_status_display()}")
    print()
    
    # Test multiple status effects
    print("6. Testing multiple status effects...")
    enemy.clear_status_effects()
    
    # Apply multiple effects
    poison_effect = PoisonedEffect(duration=3, power=3)
    weak_effect = WeakenedEffect(duration=2, power=4)
    
    enemy.add_status_effect(poison_effect)
    enemy.add_status_effect(weak_effect)
    
    print(f"   Applied poison and weakness: {enemy.get_status_display()}")
    
    base_damage = 25
    modified_damage = enemy.deal_damage(base_damage)
    print(f"   Damage: {base_damage} -> {modified_damage} (weakened)")
    
    enemy.process_turn_start()
    damage, healing, expired = enemy.process_turn_end()
    print(f"   Enemy HP after poison: {enemy.current_health}/{enemy.max_health}")
    print()
    
    # Test status effect interactions
    print("7. Testing Shield vs Damage...")
    player_wrapper.clear_status_effects()
    
    shield_effect = ShieldedEffect(duration=2, power=8)
    player_wrapper.add_status_effect(shield_effect)
    
    damage_taken = 20
    modified_damage = player_wrapper.status_effects.modify_damage_taken(damage_taken)
    print(f"   Incoming damage: {damage_taken} -> {modified_damage} (shielded)")
    print()
    
    print("=== Status Effects Demo Complete ===")

if __name__ == "__main__":
    demo_status_effects()