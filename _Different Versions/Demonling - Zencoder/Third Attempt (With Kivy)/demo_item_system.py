"""
Demo script to showcase the Item System
"""

from item_system import ItemSystem, ItemType, ItemRarity
from game_manager import Player

def demo_item_system():
    """Demonstrate the item system functionality"""
    print("=== Demonling Item System Demo ===")
    print()
    
    # Create item system and player
    item_system = ItemSystem()
    player = Player()
    
    print("1. Created item system and player")
    print(f"   Player Level: {player.level}")
    print(f"   Player Attack: {player.attack}")
    print(f"   Player Defense: {player.defense}")
    print(f"   Inventory Slots: {player.inventory.get_used_slots()}/{player.inventory.max_slots}")
    print()
    
    # Add starting items
    print("2. Adding starting items...")
    player.add_starting_items(item_system)
    print(f"   Inventory Slots: {player.inventory.get_used_slots()}/{player.inventory.max_slots}")
    
    # Show inventory
    print("\n3. Current inventory:")
    for item, quantity in player.inventory.get_all_items():
        print(f"   - {item.icon} {item.name} x{quantity} ({item.rarity.value})")
    print()
    
    # Test equipment system
    print("4. Testing equipment system...")
    sword = item_system.get_item('rusty_sword')
    armor = item_system.get_item('leather_armor')
    
    if sword:
        print(f"   Equipping {sword.name}...")
        player.equipment.equip_item(sword, 'weapon')
        player.inventory.remove_item(sword.item_id, 1)
        
    if armor:
        print(f"   Equipping {armor.name}...")
        player.equipment.equip_item(armor, 'armor')
        player.inventory.remove_item(armor.item_id, 1)
    
    # Show stats with equipment
    print("\n5. Stats with equipment:")
    print(f"   Base Attack: {player.attack}")
    print(f"   Effective Attack: {player.get_effective_attack()}")
    print(f"   Base Defense: {player.defense}")
    print(f"   Effective Defense: {player.get_effective_defense()}")
    
    equipment_stats = player.equipment.get_total_stats()
    print(f"   Equipment Bonuses: {equipment_stats}")
    print()
    
    # Test consumables
    print("6. Testing consumables...")
    health_potion = item_system.get_item('health_potion')
    if health_potion:
        print(f"   Player Health: {player.current_health}/{player.max_health}")
        player.current_health = 50  # Simulate damage
        print(f"   After damage: {player.current_health}/{player.max_health}")
        
        # Use health potion
        item_system.use_consumable(health_potion, player)
        print(f"   After potion: {player.current_health}/{player.max_health}")
    print()
    
    # Test random loot generation
    print("7. Testing random loot generation...")
    for i in range(5):
        loot = item_system.get_random_loot(player.level)
        if loot:
            for item, quantity in loot:
                print(f"   Loot {i+1}: {item.icon} {item.name} x{quantity} ({item.rarity.value})")
        else:
            print(f"   Loot {i+1}: No loot")
    print()
    
    # Show items by type
    print("8. Items by type:")
    for item_type in ItemType:
        items = item_system.get_items_by_type(item_type)
        print(f"   {item_type.value.title()}: {len(items)} items")
        for item in items[:3]:  # Show first 3
            print(f"     - {item.icon} {item.name} ({item.rarity.value})")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_item_system()