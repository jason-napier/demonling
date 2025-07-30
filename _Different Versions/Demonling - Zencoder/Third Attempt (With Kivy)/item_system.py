"""
Demonling: Item System
Manages items, inventory, and equipment functionality.
"""

import json
import random
from enum import Enum
from typing import Dict, List, Optional, Any


class ItemType(Enum):
    """Types of items available in the game"""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    MATERIAL = "material"
    QUEST = "quest"


class ItemRarity(Enum):
    """Item rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Item:
    """Base class for all items"""
    
    def __init__(self, item_id: str, name: str, description: str, item_type: ItemType, 
                 rarity: ItemRarity, value: int, **kwargs):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.item_type = item_type
        self.rarity = rarity
        self.value = value
        self.level_requirement = kwargs.get('level_requirement', 1)
        self.stats = kwargs.get('stats', {})
        self.effects = kwargs.get('effects', {})
        self.is_stackable = kwargs.get('is_stackable', False)
        self.max_stack = kwargs.get('max_stack', 1)
        self.icon = kwargs.get('icon', '📦')
        
    def get_rarity_color(self) -> tuple:
        """Get the color associated with this item's rarity"""
        colors = {
            ItemRarity.COMMON: (0.8, 0.8, 0.8, 1),      # Gray
            ItemRarity.UNCOMMON: (0.2, 0.8, 0.2, 1),    # Green
            ItemRarity.RARE: (0.2, 0.5, 1, 1),          # Blue
            ItemRarity.EPIC: (0.8, 0.2, 0.8, 1),        # Purple
            ItemRarity.LEGENDARY: (1, 0.6, 0, 1),       # Orange
        }
        return colors.get(self.rarity, (1, 1, 1, 1))
        
    def get_stat_bonus_text(self) -> str:
        """Get formatted text for stat bonuses"""
        if not self.stats:
            return ""
            
        bonus_text = []
        for stat, value in self.stats.items():
            if value > 0:
                bonus_text.append(f"+{value} {stat.title()}")
            elif value < 0:
                bonus_text.append(f"{value} {stat.title()}")
                
        return " | ".join(bonus_text)
        
    def to_dict(self) -> dict:
        """Convert item to dictionary for saving"""
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type.value,
            'rarity': self.rarity.value,
            'value': self.value,
            'level_requirement': self.level_requirement,
            'stats': self.stats,
            'effects': self.effects,
            'is_stackable': self.is_stackable,
            'max_stack': self.max_stack,
            'icon': self.icon
        }


class InventorySlot:
    """Represents a single inventory slot"""
    
    def __init__(self, item: Optional[Item] = None, quantity: int = 0):
        self.item = item
        self.quantity = quantity
        
    def is_empty(self) -> bool:
        """Check if this slot is empty"""
        return self.item is None or self.quantity <= 0
        
    def can_add(self, item: Item, quantity: int = 1) -> bool:
        """Check if we can add an item to this slot"""
        if self.is_empty():
            return True
        if self.item.item_id == item.item_id and self.item.is_stackable:
            return self.quantity + quantity <= self.item.max_stack
        return False
        
    def add(self, item: Item, quantity: int = 1) -> int:
        """Add item to this slot. Returns remaining quantity that couldn't be added"""
        if self.is_empty():
            self.item = item
            self.quantity = min(quantity, item.max_stack if item.is_stackable else 1)
            return quantity - self.quantity
        elif self.item.item_id == item.item_id and self.item.is_stackable:
            can_add = min(quantity, self.item.max_stack - self.quantity)
            self.quantity += can_add
            return quantity - can_add
        return quantity
        
    def remove(self, quantity: int = 1) -> int:
        """Remove items from this slot. Returns actual quantity removed"""
        if self.is_empty():
            return 0
        removed = min(quantity, self.quantity)
        self.quantity -= removed
        if self.quantity <= 0:
            self.item = None
            self.quantity = 0
        return removed
        
    def to_dict(self) -> dict:
        """Convert slot to dictionary"""
        return {
            'item': self.item.to_dict() if self.item else None,
            'quantity': self.quantity
        }


class Inventory:
    """Player inventory management"""
    
    def __init__(self, max_slots: int = 50):
        self.max_slots = max_slots
        self.slots: List[InventorySlot] = [InventorySlot() for _ in range(max_slots)]
        
    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """Add item to inventory. Returns True if successful"""
        remaining = quantity
        
        # First, try to add to existing stacks
        if item.is_stackable:
            for slot in self.slots:
                if not slot.is_empty() and slot.item.item_id == item.item_id:
                    remaining = slot.add(item, remaining)
                    if remaining <= 0:
                        return True
        
        # Then, try to add to empty slots
        for slot in self.slots:
            if slot.is_empty():
                remaining = slot.add(item, remaining)
                if remaining <= 0:
                    return True
                    
        return remaining == 0
        
    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remove item from inventory. Returns True if successful"""
        remaining = quantity
        
        for slot in self.slots:
            if not slot.is_empty() and slot.item.item_id == item_id:
                removed = slot.remove(remaining)
                remaining -= removed
                if remaining <= 0:
                    return True
                    
        return remaining == 0
        
    def get_item_count(self, item_id: str) -> int:
        """Get total count of an item in inventory"""
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.item_id == item_id:
                total += slot.quantity
        return total
        
    def get_items_by_type(self, item_type: ItemType) -> List[tuple]:
        """Get all items of a specific type. Returns list of (item, quantity) tuples"""
        items = []
        for slot in self.slots:
            if not slot.is_empty() and slot.item.item_type == item_type:
                items.append((slot.item, slot.quantity))
        return items
        
    def get_all_items(self) -> List[tuple]:
        """Get all items in inventory. Returns list of (item, quantity) tuples"""
        items = []
        for slot in self.slots:
            if not slot.is_empty():
                items.append((slot.item, slot.quantity))
        return items
        
    def get_used_slots(self) -> int:
        """Get number of used inventory slots"""
        return sum(1 for slot in self.slots if not slot.is_empty())
        
    def to_dict(self) -> dict:
        """Convert inventory to dictionary"""
        return {
            'max_slots': self.max_slots,
            'slots': [slot.to_dict() for slot in self.slots]
        }


class Equipment:
    """Player equipment management"""
    
    def __init__(self):
        self.slots = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
        
    def equip_item(self, item: Item, slot: str) -> Optional[Item]:
        """Equip an item. Returns previously equipped item if any"""
        if slot not in self.slots:
            return None
            
        previous_item = self.slots[slot]
        self.slots[slot] = item
        return previous_item
        
    def unequip_item(self, slot: str) -> Optional[Item]:
        """Unequip an item. Returns the unequipped item"""
        if slot not in self.slots:
            return None
            
        item = self.slots[slot]
        self.slots[slot] = None
        return item
        
    def get_equipped_item(self, slot: str) -> Optional[Item]:
        """Get currently equipped item in slot"""
        return self.slots.get(slot)
        
    def get_total_stats(self) -> Dict[str, int]:
        """Get total stat bonuses from all equipped items"""
        total_stats = {}
        
        for item in self.slots.values():
            if item:
                for stat, value in item.stats.items():
                    total_stats[stat] = total_stats.get(stat, 0) + value
                    
        return total_stats
        
    def to_dict(self) -> dict:
        """Convert equipment to dictionary"""
        return {
            slot: item.to_dict() if item else None
            for slot, item in self.slots.items()
        }


class ItemSystem:
    """Main item system class"""
    
    def __init__(self):
        self.item_database = {}
        self.load_item_database()
        
    def load_item_database(self):
        """Load item database from predefined data"""
        # Define base items
        items_data = {
            # Weapons
            'rusty_sword': {
                'name': 'Rusty Sword',
                'description': 'An old, rusty sword. Better than nothing.',
                'item_type': ItemType.WEAPON,
                'rarity': ItemRarity.COMMON,
                'value': 10,
                'stats': {'attack': 5},
                'icon': '🗡️'
            },
            'iron_sword': {
                'name': 'Iron Sword',
                'description': 'A sturdy iron sword. Reliable in combat.',
                'item_type': ItemType.WEAPON,
                'rarity': ItemRarity.UNCOMMON,
                'value': 50,
                'stats': {'attack': 12},
                'level_requirement': 3,
                'icon': '⚔️'
            },
            'demon_blade': {
                'name': 'Demon Blade',
                'description': 'A blade infused with demonic energy. Crackles with power.',
                'item_type': ItemType.WEAPON,
                'rarity': ItemRarity.RARE,
                'value': 200,
                'stats': {'attack': 25, 'magic': 5},
                'level_requirement': 8,
                'icon': '🔥'
            },
            
            # Armor
            'leather_armor': {
                'name': 'Leather Armor',
                'description': 'Basic leather armor providing minimal protection.',
                'item_type': ItemType.ARMOR,
                'rarity': ItemRarity.COMMON,
                'value': 20,
                'stats': {'defense': 3},
                'icon': '🛡️'
            },
            'chainmail': {
                'name': 'Chainmail',
                'description': 'Sturdy chainmail armor. Offers good protection.',
                'item_type': ItemType.ARMOR,
                'rarity': ItemRarity.UNCOMMON,
                'value': 80,
                'stats': {'defense': 8},
                'level_requirement': 4,
                'icon': '🛡️'
            },
            'demon_plate': {
                'name': 'Demon Plate',
                'description': 'Armor forged from demon scales. Provides excellent protection.',
                'item_type': ItemType.ARMOR,
                'rarity': ItemRarity.EPIC,
                'value': 500,
                'stats': {'defense': 18, 'magic': 3},
                'level_requirement': 12,
                'icon': '🛡️'
            },
            
            # Consumables
            'health_potion': {
                'name': 'Health Potion',
                'description': 'Restores 50 health when consumed.',
                'item_type': ItemType.CONSUMABLE,
                'rarity': ItemRarity.COMMON,
                'value': 25,
                'effects': {'heal': 50},
                'is_stackable': True,
                'max_stack': 10,
                'icon': '🧪'
            },
            'energy_potion': {
                'name': 'Energy Potion',
                'description': 'Restores 30 energy when consumed.',
                'item_type': ItemType.CONSUMABLE,
                'rarity': ItemRarity.COMMON,
                'value': 30,
                'effects': {'energy': 30},
                'is_stackable': True,
                'max_stack': 5,
                'icon': '⚡'
            },
            'soul_crystal': {
                'name': 'Soul Crystal',
                'description': 'A crystallized soul. Can be used for powerful enchantments.',
                'item_type': ItemType.MATERIAL,
                'rarity': ItemRarity.RARE,
                'value': 100,
                'is_stackable': True,
                'max_stack': 99,
                'icon': '💎'
            }
        }
        
        # Create Item objects from data
        for item_id, data in items_data.items():
            self.item_database[item_id] = Item(
                item_id=item_id,
                name=data['name'],
                description=data['description'],
                item_type=data['item_type'],
                rarity=data['rarity'],
                value=data['value'],
                stats=data.get('stats', {}),
                effects=data.get('effects', {}),
                level_requirement=data.get('level_requirement', 1),
                is_stackable=data.get('is_stackable', False),
                max_stack=data.get('max_stack', 1),
                icon=data.get('icon', '📦')
            )
            
    def get_item(self, item_id: str) -> Optional[Item]:
        """Get an item by its ID"""
        return self.item_database.get(item_id)
        
    def get_random_loot(self, player_level: int) -> List[tuple]:
        """Generate random loot based on player level. Returns list of (item, quantity) tuples"""
        loot = []
        
        # Base loot chances
        common_chance = 0.7
        uncommon_chance = 0.2
        rare_chance = 0.08
        epic_chance = 0.02
        
        # Adjust chances based on player level
        if player_level >= 5:
            uncommon_chance += 0.1
            rare_chance += 0.05
        if player_level >= 10:
            rare_chance += 0.1
            epic_chance += 0.03
            
        # Generate loot
        roll = random.random()
        
        if roll < epic_chance and player_level >= 10:
            # Epic loot
            epic_items = [item for item in self.item_database.values() 
                         if item.rarity == ItemRarity.EPIC and item.level_requirement <= player_level]
            if epic_items:
                item = random.choice(epic_items)
                loot.append((item, 1))
                
        elif roll < rare_chance:
            # Rare loot
            rare_items = [item for item in self.item_database.values() 
                         if item.rarity == ItemRarity.RARE and item.level_requirement <= player_level]
            if rare_items:
                item = random.choice(rare_items)
                loot.append((item, 1))
                
        elif roll < uncommon_chance:
            # Uncommon loot
            uncommon_items = [item for item in self.item_database.values() 
                             if item.rarity == ItemRarity.UNCOMMON and item.level_requirement <= player_level]
            if uncommon_items:
                item = random.choice(uncommon_items)
                loot.append((item, 1))
                
        else:
            # Common loot (consumables and materials)
            common_items = [item for item in self.item_database.values() 
                           if item.rarity == ItemRarity.COMMON]
            if common_items:
                item = random.choice(common_items)
                quantity = random.randint(1, 3) if item.is_stackable else 1
                loot.append((item, quantity))
                
        return loot
        
    def get_items_by_type(self, item_type: ItemType) -> List[Item]:
        """Get all items of a specific type"""
        return [item for item in self.item_database.values() if item.item_type == item_type]
        
    def use_consumable(self, item: Item, player) -> bool:
        """Use a consumable item on the player. Returns True if successful"""
        if item.item_type != ItemType.CONSUMABLE:
            return False
            
        for effect, value in item.effects.items():
            if effect == 'heal':
                player.current_health = min(player.max_health, player.current_health + value)
            elif effect == 'energy':
                player.energy = min(player.max_energy, player.energy + value)
            elif effect == 'attack':
                player.attack += value
            elif effect == 'defense':
                player.defense += value
            # Add more effects as needed
            
        return True