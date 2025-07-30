"""
Combat System Module

This module implements the turn-based combat system for Demonling.
It handles player vs enemy combat with attack, defend, and special abilities.
"""

import random
from kivy.logger import Logger
from enum import Enum

class StatusEffectType(Enum):
    """Types of status effects that can be applied in combat"""
    BURNED = "burned"
    FROZEN = "frozen"
    BLEEDING = "bleeding"
    STUNNED = "stunned"
    ENRAGED = "enraged"
    POISONED = "poisoned"
    REGENERATING = "regenerating"
    STRENGTHENED = "strengthened"
    WEAKENED = "weakened"
    SHIELDED = "shielded"

class StatusEffect:
    """
    Base class for status effects that can be applied to combat entities.
    """
    
    def __init__(self, effect_type, duration, power=1, icon="🔮"):
        """
        Initialize a status effect.
        
        Args:
            effect_type (StatusEffectType): Type of status effect
            duration (int): Number of turns the effect lasts
            power (int): Strength of the effect
            icon (str): Icon to display for the effect
        """
        self.effect_type = effect_type
        self.duration = duration
        self.power = power
        self.icon = icon
        self.name = effect_type.value.title()
        
    def apply_start_effect(self, entity):
        """Apply initial effect when status is first applied"""
        Logger.info(f"Combat: {entity.name} is now {self.name}")
        
    def apply_turn_start_effect(self, entity):
        """Apply effect at the start of the entity's turn"""
        pass
        
    def apply_turn_end_effect(self, entity):
        """Apply effect at the end of the entity's turn"""
        pass
        
    def can_act(self, entity):
        """Check if the entity can perform actions"""
        return True
        
    def modify_damage_dealt(self, damage):
        """Modify damage dealt by the entity"""
        return damage
        
    def modify_damage_taken(self, damage):
        """Modify damage taken by the entity"""
        return damage
        
    def tick(self):
        """Reduce duration by 1 turn"""
        self.duration -= 1
        return self.duration <= 0
        
    def get_description(self):
        """Get a description of the effect"""
        return f"{self.icon} {self.name} ({self.duration} turns)"

class BurnedEffect(StatusEffect):
    """Fire damage over time"""
    
    def __init__(self, duration=3, power=5):
        super().__init__(StatusEffectType.BURNED, duration, power, "🔥")
        
    def apply_turn_end_effect(self, entity):
        """Apply burn damage at end of turn"""
        damage = self.power
        
        # Handle PlayerCombatWrapper differently
        if hasattr(entity, 'player'):
            # This is a PlayerCombatWrapper
            entity.player.current_health = max(0, entity.player.current_health - damage)
        else:
            # This is a regular CombatEntity
            entity.current_health = max(0, entity.current_health - damage)
        
        Logger.info(f"Combat: {entity.name} takes {damage} burn damage! ({entity.current_health}/{entity.max_health} HP)")
        return damage

class FrozenEffect(StatusEffect):
    """Skip next turn"""
    
    def __init__(self, duration=2):
        super().__init__(StatusEffectType.FROZEN, duration, 1, "❄️")
        
    def can_act(self, entity):
        """Frozen entities cannot act"""
        return False
        
    def apply_turn_start_effect(self, entity):
        """Notify that turn is skipped"""
        Logger.info(f"Combat: {entity.name} is frozen and cannot act!")

class BleedingEffect(StatusEffect):
    """Lose HP each action"""
    
    def __init__(self, duration=4, power=3):
        super().__init__(StatusEffectType.BLEEDING, duration, power, "🩸")
        
    def apply_turn_start_effect(self, entity):
        """Apply bleeding damage at start of turn"""
        damage = self.power
        
        # Handle PlayerCombatWrapper differently
        if hasattr(entity, 'player'):
            # This is a PlayerCombatWrapper
            entity.player.current_health = max(0, entity.player.current_health - damage)
        else:
            # This is a regular CombatEntity
            entity.current_health = max(0, entity.current_health - damage)
        
        Logger.info(f"Combat: {entity.name} loses {damage} HP from bleeding! ({entity.current_health}/{entity.max_health} HP)")
        return damage

class StunnedEffect(StatusEffect):
    """Cannot act"""
    
    def __init__(self, duration=1):
        super().__init__(StatusEffectType.STUNNED, duration, 1, "😵")
        
    def can_act(self, entity):
        """Stunned entities cannot act"""
        return False
        
    def apply_turn_start_effect(self, entity):
        """Notify that turn is skipped"""
        Logger.info(f"Combat: {entity.name} is stunned and cannot act!")

class EnragedEffect(StatusEffect):
    """Auto-attack, can't use abilities"""
    
    def __init__(self, duration=3, power=2):
        super().__init__(StatusEffectType.ENRAGED, duration, power, "🧠")
        
    def modify_damage_dealt(self, damage):
        """Increase damage dealt while enraged"""
        return int(damage * (1 + self.power * 0.1))
        
    def apply_turn_start_effect(self, entity):
        """Notify about enraged state"""
        Logger.info(f"Combat: {entity.name} is enraged and will auto-attack!")

class PoisonedEffect(StatusEffect):
    """Poison damage over time"""
    
    def __init__(self, duration=5, power=3):
        super().__init__(StatusEffectType.POISONED, duration, power, "☠️")
        
    def apply_turn_end_effect(self, entity):
        """Apply poison damage at end of turn"""
        damage = self.power
        
        # Handle PlayerCombatWrapper differently
        if hasattr(entity, 'player'):
            # This is a PlayerCombatWrapper
            entity.player.current_health = max(0, entity.player.current_health - damage)
        else:
            # This is a regular CombatEntity
            entity.current_health = max(0, entity.current_health - damage)
        
        Logger.info(f"Combat: {entity.name} takes {damage} poison damage! ({entity.current_health}/{entity.max_health} HP)")
        return damage

class RegeneratingEffect(StatusEffect):
    """Heal over time"""
    
    def __init__(self, duration=3, power=8):
        super().__init__(StatusEffectType.REGENERATING, duration, power, "💚")
        
    def apply_turn_end_effect(self, entity):
        """Apply healing at end of turn"""
        healing = self.power
        old_health = entity.current_health
        
        # Handle PlayerCombatWrapper differently
        if hasattr(entity, 'player'):
            # This is a PlayerCombatWrapper
            old_health = entity.player.current_health
            entity.player.current_health = min(entity.player.max_health, entity.player.current_health + healing)
            actual_healing = entity.player.current_health - old_health
        else:
            # This is a regular CombatEntity
            entity.current_health = min(entity.max_health, entity.current_health + healing)
            actual_healing = entity.current_health - old_health
        
        if actual_healing > 0:
            Logger.info(f"Combat: {entity.name} regenerates {actual_healing} HP! ({entity.current_health}/{entity.max_health} HP)")
        return actual_healing

class StrengthenedEffect(StatusEffect):
    """Increased damage dealt"""
    
    def __init__(self, duration=4, power=3):
        super().__init__(StatusEffectType.STRENGTHENED, duration, power, "💪")
        
    def modify_damage_dealt(self, damage):
        """Increase damage dealt"""
        return damage + self.power

class WeakenedEffect(StatusEffect):
    """Decreased damage dealt"""
    
    def __init__(self, duration=3, power=2):
        super().__init__(StatusEffectType.WEAKENED, duration, power, "🔻")
        
    def modify_damage_dealt(self, damage):
        """Decrease damage dealt"""
        return max(1, damage - self.power)

class ShieldedEffect(StatusEffect):
    """Reduced damage taken"""
    
    def __init__(self, duration=2, power=5):
        super().__init__(StatusEffectType.SHIELDED, duration, power, "🛡️")
        
    def modify_damage_taken(self, damage):
        """Reduce damage taken"""
        return max(1, damage - self.power)

class StatusEffectManager:
    """
    Manages status effects for a combat entity.
    """
    
    def __init__(self):
        self.effects = {}  # effect_type -> StatusEffect
        
    def add_effect(self, effect):
        """
        Add a status effect, replacing any existing effect of the same type.
        
        Args:
            effect (StatusEffect): The effect to add
        """
        # If effect already exists, replace it or extend duration
        if effect.effect_type in self.effects:
            existing = self.effects[effect.effect_type]
            if effect.duration > existing.duration:
                # Replace with longer duration
                self.effects[effect.effect_type] = effect
            else:
                # Extend existing duration
                existing.duration = max(existing.duration, effect.duration)
        else:
            self.effects[effect.effect_type] = effect
            
    def remove_effect(self, effect_type):
        """Remove a status effect"""
        if effect_type in self.effects:
            del self.effects[effect_type]
            
    def has_effect(self, effect_type):
        """Check if entity has a specific effect"""
        return effect_type in self.effects
        
    def get_effect(self, effect_type):
        """Get a specific effect"""
        return self.effects.get(effect_type)
        
    def get_all_effects(self):
        """Get all active effects"""
        return list(self.effects.values())
        
    def apply_start_turn_effects(self, entity):
        """Apply all start-of-turn effects"""
        for effect in list(self.effects.values()):
            effect.apply_turn_start_effect(entity)
            
    def apply_end_turn_effects(self, entity):
        """Apply all end-of-turn effects"""
        damage_taken = 0
        healing_received = 0
        
        for effect in list(self.effects.values()):
            result = effect.apply_turn_end_effect(entity)
            if result and result > 0:
                if effect.effect_type in [StatusEffectType.BURNED, StatusEffectType.BLEEDING, StatusEffectType.POISONED]:
                    damage_taken += result
                elif effect.effect_type == StatusEffectType.REGENERATING:
                    healing_received += result
                    
        return damage_taken, healing_received
        
    def tick_effects(self):
        """Tick all effects and remove expired ones"""
        expired_effects = []
        
        for effect_type, effect in self.effects.items():
            if effect.tick():
                expired_effects.append(effect_type)
                
        for effect_type in expired_effects:
            del self.effects[effect_type]
            
        return expired_effects
        
    def can_act(self, entity):
        """Check if entity can act (not frozen/stunned)"""
        for effect in self.effects.values():
            if not effect.can_act(entity):
                return False
        return True
        
    def is_enraged(self):
        """Check if entity is enraged"""
        return StatusEffectType.ENRAGED in self.effects
        
    def modify_damage_dealt(self, damage):
        """Modify damage dealt by applying all relevant effects"""
        for effect in self.effects.values():
            damage = effect.modify_damage_dealt(damage)
        return max(1, damage)
        
    def modify_damage_taken(self, damage):
        """Modify damage taken by applying all relevant effects"""
        for effect in self.effects.values():
            damage = effect.modify_damage_taken(damage)
        return max(1, damage)
        
    def get_status_display(self):
        """Get a formatted string showing all active effects"""
        if not self.effects:
            return ""
        
        status_icons = []
        for effect in self.effects.values():
            status_icons.append(f"{effect.icon}({effect.duration})")
        
        return " ".join(status_icons)
        
    def clear_all_effects(self):
        """Remove all status effects"""
        self.effects.clear()

class CombatEntity:
    """
    Base class for entities that can participate in combat.
    This includes both players and enemies.
    """
    
    def __init__(self, name, attack, defense, agility, magic, max_health):
        """
        Initialize a combat entity.
        
        Args:
            name (str): Name of the entity
            attack (int): Base attack power
            defense (int): Defense value
            agility (int): Agility for dodge/crit chances
            magic (int): Magic power for special abilities
            max_health (int): Maximum health points
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.magic = magic
        self.max_health = max_health
        self.current_health = max_health
        
        # Combat state
        self.defending = False
        self.status_effects = StatusEffectManager()
        
        Logger.info(f"Combat: Created entity {name} with {max_health} HP")
        
    def take_damage(self, damage):
        """
        Apply damage to this entity.
        
        Args:
            damage (int): Amount of damage to take
            
        Returns:
            int: Actual damage taken
        """
        # Apply defense reduction
        effective_damage = max(1, damage - self.defense)
        
        # Apply defending bonus
        if self.defending:
            effective_damage = max(1, effective_damage // 2)
            
        # Apply status effect damage modifications
        effective_damage = self.status_effects.modify_damage_taken(effective_damage)
        
        # Apply damage
        self.current_health = max(0, self.current_health - effective_damage)
        
        Logger.info(f"Combat: {self.name} took {effective_damage} damage ({self.current_health}/{self.max_health} HP)")
        return effective_damage
        
    def is_alive(self):
        """Check if entity is still alive"""
        return self.current_health > 0
        
    def deal_damage(self, base_damage):
        """
        Calculate damage dealt by this entity, including status effect modifiers.
        
        Args:
            base_damage (int): Base damage before modifiers
            
        Returns:
            int: Modified damage
        """
        # Apply status effect damage modifications
        return self.status_effects.modify_damage_dealt(base_damage)
        
    def add_status_effect(self, effect):
        """
        Add a status effect to this entity.
        
        Args:
            effect (StatusEffect): The effect to add
        """
        self.status_effects.add_effect(effect)
        effect.apply_start_effect(self)
        
    def remove_status_effect(self, effect_type):
        """Remove a status effect"""
        self.status_effects.remove_effect(effect_type)
        
    def has_status_effect(self, effect_type):
        """Check if entity has a specific status effect"""
        return self.status_effects.has_effect(effect_type)
        
    def can_act(self):
        """Check if this entity can act (not stunned/frozen)"""
        return self.status_effects.can_act(self)
        
    def is_enraged(self):
        """Check if this entity is enraged"""
        return self.status_effects.is_enraged()
        
    def process_turn_start(self):
        """Process start of turn effects"""
        self.status_effects.apply_start_turn_effects(self)
        
    def process_turn_end(self):
        """Process end of turn effects and tick status effects"""
        # Apply end-of-turn effects
        damage_taken, healing_received = self.status_effects.apply_end_turn_effects(self)
        
        # Tick effects and remove expired ones
        expired_effects = self.status_effects.tick_effects()
        
        # Log expired effects
        for effect_type in expired_effects:
            Logger.info(f"Combat: {self.name}'s {effect_type.value} effect has expired")
            
        return damage_taken, healing_received, expired_effects
        
    def get_status_display(self):
        """Get status effects display string"""
        return self.status_effects.get_status_display()
        
    def clear_status_effects(self):
        """Clear all status effects"""
        self.status_effects.clear_all_effects()
        
    def reset_combat_state(self):
        """Reset temporary combat state"""
        self.defending = False
        self.status_effects.clear_all_effects()

class Enemy(CombatEntity):
    """
    Enemy class that extends CombatEntity with AI behavior.
    """
    
    def __init__(self, enemy_data):
        """
        Initialize enemy from data dictionary.
        
        Args:
            enemy_data (dict): Dictionary containing enemy stats
        """
        super().__init__(
            enemy_data['name'],
            enemy_data['attack'],
            enemy_data['defense'],
            enemy_data['agility'],
            enemy_data['magic'],
            enemy_data['health']
        )
        
        self.enemy_type = enemy_data.get('type', 'normal')
        self.special_abilities = enemy_data.get('abilities', [])
        self.ai_behavior = enemy_data.get('ai_behavior', 'aggressive')
        
    def choose_action(self):
        """
        AI chooses an action based on behavior pattern.
        
        Returns:
            str: Action to take ('attack', 'defend', 'special')
        """
        # Check if enemy can use special abilities
        if self.can_use_special_ability():
            special_chance = 0.3 if self.ai_behavior == 'balanced' else 0.2
            if random.random() < special_chance:
                return 'special'
        
        if self.ai_behavior == 'aggressive':
            return 'attack'
        elif self.ai_behavior == 'defensive':
            # Defend if health is low
            if self.current_health < self.max_health * 0.3:
                return 'defend'
            else:
                return 'attack'
        else:
            # Balanced approach
            if self.current_health < self.max_health * 0.5:
                return random.choice(['attack', 'defend'])
            else:
                return 'attack'
                
    def can_use_special_ability(self):
        """Check if enemy can use special abilities"""
        # Can use special abilities if health is below 50% or randomly
        health_percentage = self.current_health / self.max_health
        return health_percentage < 0.5 or random.random() < 0.1
        
    def use_special_ability(self, target):
        """
        Use a special ability based on enemy type.
        
        Args:
            target: The target entity to apply effects to
            
        Returns:
            str: Description of the special ability used
        """
        if self.enemy_type == 'demon':
            return self.demon_special_ability(target)
        elif self.enemy_type == 'undead':
            return self.undead_special_ability(target)
        elif self.enemy_type == 'beast':
            return self.beast_special_ability(target)
        elif self.enemy_type == 'elemental':
            return self.elemental_special_ability(target)
        else:
            return self.generic_special_ability(target)
            
    def demon_special_ability(self, target):
        """Demon special abilities"""
        abilities = [
            ('burn', "unleashes hellfire"),
            ('weaken', "curses with dark magic"),
            ('enrage_self', "enters a demonic fury")
        ]
        
        ability, description = random.choice(abilities)
        
        if ability == 'burn':
            burn_effect = BurnedEffect(duration=3, power=6)
            target.add_status_effect(burn_effect)
            return f"{self.name} {description}! {target.name} is burned!"
        elif ability == 'weaken':
            weaken_effect = WeakenedEffect(duration=3, power=4)
            target.add_status_effect(weaken_effect)
            return f"{self.name} {description}! {target.name} is weakened!"
        elif ability == 'enrage_self':
            enrage_effect = EnragedEffect(duration=2, power=3)
            self.add_status_effect(enrage_effect)
            return f"{self.name} {description}! {self.name} is enraged!"
            
    def undead_special_ability(self, target):
        """Undead special abilities"""
        abilities = [
            ('poison', "breathes toxic miasma"),
            ('bleeding', "inflicts cursed wounds"),
            ('regenerate_self', "draws power from darkness")
        ]
        
        ability, description = random.choice(abilities)
        
        if ability == 'poison':
            poison_effect = PoisonedEffect(duration=4, power=4)
            target.add_status_effect(poison_effect)
            return f"{self.name} {description}! {target.name} is poisoned!"
        elif ability == 'bleeding':
            bleed_effect = BleedingEffect(duration=3, power=4)
            target.add_status_effect(bleed_effect)
            return f"{self.name} {description}! {target.name} is bleeding!"
        elif ability == 'regenerate_self':
            regen_effect = RegeneratingEffect(duration=2, power=6)
            self.add_status_effect(regen_effect)
            return f"{self.name} {description}! {self.name} begins regenerating!"
            
    def beast_special_ability(self, target):
        """Beast special abilities"""
        abilities = [
            ('bleeding', "mauls with claws"),
            ('stun', "roars with stunning force"),
            ('strengthen_self', "becomes more ferocious")
        ]
        
        ability, description = random.choice(abilities)
        
        if ability == 'bleeding':
            bleed_effect = BleedingEffect(duration=4, power=3)
            target.add_status_effect(bleed_effect)
            return f"{self.name} {description}! {target.name} is bleeding!"
        elif ability == 'stun':
            stun_effect = StunnedEffect(duration=1)
            target.add_status_effect(stun_effect)
            return f"{self.name} {description}! {target.name} is stunned!"
        elif ability == 'strengthen_self':
            strengthen_effect = StrengthenedEffect(duration=3, power=5)
            self.add_status_effect(strengthen_effect)
            return f"{self.name} {description}! {self.name} is strengthened!"
            
    def elemental_special_ability(self, target):
        """Elemental special abilities"""
        abilities = [
            ('freeze', "conjures ice magic"),
            ('burn', "erupts with flames"),
            ('shield_self', "hardens with earth magic")
        ]
        
        ability, description = random.choice(abilities)
        
        if ability == 'freeze':
            freeze_effect = FrozenEffect(duration=2)
            target.add_status_effect(freeze_effect)
            return f"{self.name} {description}! {target.name} is frozen!"
        elif ability == 'burn':
            burn_effect = BurnedEffect(duration=2, power=5)
            target.add_status_effect(burn_effect)
            return f"{self.name} {description}! {target.name} is burned!"
        elif ability == 'shield_self':
            shield_effect = ShieldedEffect(duration=3, power=6)
            self.add_status_effect(shield_effect)
            return f"{self.name} {description}! {self.name} is shielded!"
            
    def generic_special_ability(self, target):
        """Generic special abilities for unknown types"""
        abilities = [
            ('weaken', "uses a mysterious power"),
            ('strengthen_self', "focuses its energy")
        ]
        
        ability, description = random.choice(abilities)
        
        if ability == 'weaken':
            weaken_effect = WeakenedEffect(duration=2, power=3)
            target.add_status_effect(weaken_effect)
            return f"{self.name} {description}! {target.name} is weakened!"
        elif ability == 'strengthen_self':
            strengthen_effect = StrengthenedEffect(duration=2, power=3)
            self.add_status_effect(strengthen_effect)
            return f"{self.name} {description}! {self.name} is strengthened!"

class PlayerCombatWrapper:
    """
    Wrapper class to make Player compatible with combat system.
    """
    
    def __init__(self, player):
        """
        Initialize wrapper around player object.
        
        Args:
            player (Player): Player object from game_manager
        """
        self.player = player
        self.name = "Player"
        self.defending = False
        self.status_effects = StatusEffectManager()
        
    @property
    def attack(self):
        return self.player.get_effective_attack()
        
    @property
    def defense(self):
        return self.player.get_effective_defense()
        
    @property
    def agility(self):
        return self.player.agility + self.player.equipment.get_total_stats().get('agility', 0)
        
    @property
    def magic(self):
        return self.player.magic + self.player.equipment.get_total_stats().get('magic', 0)
        
    @property
    def max_health(self):
        return self.player.max_health
        
    @property
    def current_health(self):
        return self.player.current_health
        
    def take_damage(self, damage):
        """Apply damage to player"""
        # Apply defense reduction
        effective_damage = max(1, damage - self.defense)
        
        # Apply defending bonus
        if self.defending:
            effective_damage = max(1, effective_damage // 2)
            
        # Apply damage through player object
        self.player.take_damage(effective_damage)
        
        Logger.info(f"Combat: Player took {effective_damage} damage")
        return effective_damage
        
    def is_alive(self):
        """Check if player is alive"""
        return self.player.current_health > 0
        
    def deal_damage(self, base_damage):
        """Calculate damage dealt by player including status effects"""
        return self.status_effects.modify_damage_dealt(base_damage)
        
    def add_status_effect(self, effect):
        """Add a status effect to player"""
        self.status_effects.add_effect(effect)
        effect.apply_start_effect(self)
        
    def remove_status_effect(self, effect_type):
        """Remove a status effect"""
        self.status_effects.remove_effect(effect_type)
        
    def has_status_effect(self, effect_type):
        """Check if player has a specific status effect"""
        return self.status_effects.has_effect(effect_type)
        
    def can_act(self):
        """Check if player can act (not stunned/frozen)"""
        return self.status_effects.can_act(self)
        
    def is_enraged(self):
        """Check if player is enraged"""
        return self.status_effects.is_enraged()
        
    def process_turn_start(self):
        """Process start of turn effects"""
        self.status_effects.apply_start_turn_effects(self)
        
    def process_turn_end(self):
        """Process end of turn effects and tick status effects"""
        # Apply end-of-turn effects
        damage_taken, healing_received = self.status_effects.apply_end_turn_effects(self)
        
        # Tick effects and remove expired ones
        expired_effects = self.status_effects.tick_effects()
        
        # Log expired effects
        for effect_type in expired_effects:
            Logger.info(f"Combat: Player's {effect_type.value} effect has expired")
            
        return damage_taken, healing_received, expired_effects
        
    def get_status_display(self):
        """Get status effects display string"""
        return self.status_effects.get_status_display()
        
    def clear_status_effects(self):
        """Clear all status effects"""
        self.status_effects.clear_all_effects()
        
    def reset_combat_state(self):
        """Reset combat state"""
        self.defending = False
        self.status_effects.clear_all_effects()

class CombatSystem:
    """
    Main combat system that manages battles between player and enemies.
    """
    
    def __init__(self, player, enemy_data):
        """
        Initialize combat system.
        
        Args:
            player (Player): Player object
            enemy_data (dict): Enemy data dictionary
        """
        self.player = PlayerCombatWrapper(player)
        self.enemy = Enemy(enemy_data)
        
        # Combat state
        self.turn_count = 0
        self.combat_active = True
        self.combat_log = []
        
        Logger.info(f"Combat: Battle started between Player and {self.enemy.name}")
        
    def player_attack(self):
        """
        Execute player attack action.
        
        Returns:
            int: Damage dealt to enemy
        """
        if not self.combat_active:
            return 0
            
        # Check if player can act
        if not self.player.can_act():
            return 0
            
        # Reset defending state
        self.player.defending = False
        
        # Calculate base damage
        base_damage = self.player.attack
        
        # Add some randomness (±20%)
        damage_variance = random.randint(-20, 20) / 100
        damage = int(base_damage * (1 + damage_variance))
        damage = max(1, damage)  # Minimum 1 damage
        
        # Apply player's status effect damage modifiers
        damage = self.player.deal_damage(damage)
        
        # Apply damage to enemy
        actual_damage = self.enemy.take_damage(damage)
        
        # Add to combat log
        self.combat_log.append(f"Player attacks for {actual_damage} damage!")
        
        # Check if enemy is defeated
        if not self.enemy.is_alive():
            self.combat_active = False
            self.combat_log.append(f"{self.enemy.name} has been defeated!")
            
        return actual_damage
        
    def player_defend(self):
        """Execute player defend action"""
        if not self.combat_active:
            return
            
        self.player.defending = True
        self.combat_log.append("Player takes a defensive stance!")
        
    def enemy_attack(self):
        """
        Execute enemy attack action.
        
        Returns:
            int: Damage dealt to player
        """
        if not self.combat_active:
            return 0
            
        # Check if enemy can act
        if not self.enemy.can_act():
            return 0
            
        # Reset enemy defending state
        self.enemy.defending = False
        
        # Enemy chooses action (or is forced to attack if enraged)
        if self.enemy.is_enraged():
            action = 'attack'
        else:
            action = self.enemy.choose_action()
        
        if action == 'defend':
            self.enemy.defending = True
            self.combat_log.append(f"{self.enemy.name} takes a defensive stance!")
            return 0
        elif action == 'special':
            # Use special ability
            ability_description = self.enemy.use_special_ability(self.player)
            self.combat_log.append(ability_description)
            return 0
        else:
            # Attack
            base_damage = self.enemy.attack
            
            # Add some randomness (±20%)
            damage_variance = random.randint(-20, 20) / 100
            damage = int(base_damage * (1 + damage_variance))
            damage = max(1, damage)  # Minimum 1 damage
            
            # Apply enemy's status effect damage modifiers
            damage = self.enemy.deal_damage(damage)
            
            # Apply damage to player
            actual_damage = self.player.take_damage(damage)
            
            # Add to combat log
            self.combat_log.append(f"{self.enemy.name} attacks for {actual_damage} damage!")
            
            # Check if player is defeated
            if not self.player.is_alive():
                self.combat_active = False
                self.combat_log.append("Player has been defeated!")
                
            return actual_damage
            
    def is_combat_over(self):
        """Check if combat has ended"""
        return not self.combat_active or not self.player.is_alive() or not self.enemy.is_alive()
        
    def get_winner(self):
        """
        Get the winner of the combat.
        
        Returns:
            str: 'player', 'enemy', or 'ongoing'
        """
        if not self.is_combat_over():
            return 'ongoing'
        elif self.player.is_alive():
            return 'player'
        else:
            return 'enemy'
            
    def get_combat_log(self):
        """Get the combat log messages"""
        return self.combat_log.copy()
        
    def process_turn_start(self, entity):
        """Process start of turn for an entity"""
        if entity:
            entity.process_turn_start()
            
    def process_turn_end(self, entity):
        """Process end of turn for an entity"""
        if entity:
            damage, healing, expired = entity.process_turn_end()
            
            # Log any damage/healing from status effects
            if damage > 0:
                self.combat_log.append(f"{entity.name} takes {damage} damage from status effects!")
            if healing > 0:
                self.combat_log.append(f"{entity.name} heals {healing} HP from status effects!")
                
            # Check if entity died from status effects
            if not entity.is_alive():
                self.combat_active = False
                self.combat_log.append(f"{entity.name} has been defeated by status effects!")
                
            return damage, healing, expired
        return 0, 0, []
        
    def add_status_effect_to_player(self, effect):
        """Add a status effect to the player"""
        self.player.add_status_effect(effect)
        
    def add_status_effect_to_enemy(self, effect):
        """Add a status effect to the enemy"""
        self.enemy.add_status_effect(effect)
        
    def get_player_status_effects(self):
        """Get player's status effects display"""
        return self.player.get_status_display()
        
    def get_enemy_status_effects(self):
        """Get enemy's status effects display"""
        return self.enemy.get_status_display()
        
    def reset_combat_states(self):
        """Reset temporary combat states"""
        self.player.reset_combat_state()
        self.enemy.reset_combat_state()

class CombatSystemAdvanced(CombatSystem):
    """
    Advanced combat system with items, special abilities, and passive effects.
    This is for Phase 2 of combat development.
    """
    
    def __init__(self, player, enemy_data):
        """Initialize advanced combat system"""
        super().__init__(player, enemy_data)
        
        # Additional combat features
        self.special_abilities_used = []
        self.items_used = []
        self.passive_effects_active = []
        
    def use_item(self, item_slot):
        """
        Use an item from player inventory.
        
        Args:
            item_slot (int): Item slot number (1-3)
            
        Returns:
            bool: True if item was used successfully
        """
        # TODO: Implement item system
        # For now, return False as items aren't implemented
        return False
        
    def use_special_ability(self, ability_slot):
        """
        Use a special ability.
        
        Args:
            ability_slot (int): Ability slot number (1-3)
            
        Returns:
            bool: True if ability was used successfully
        """
        # TODO: Implement special ability system
        # For now, return False as abilities aren't implemented
        return False
        
    def apply_passive_effects(self):
        """Apply any passive effects at the start of turn"""
        # TODO: Implement passive effects
        # For now, do nothing
        pass
        
    def calculate_critical_hit(self, attacker):
        """
        Calculate if an attack is a critical hit.
        
        Args:
            attacker (CombatEntity): The attacking entity
            
        Returns:
            bool: True if critical hit
        """
        # Critical hit chance based on agility
        crit_chance = min(0.2, attacker.agility / 100)  # Max 20% crit chance
        return random.random() < crit_chance
        
    def calculate_dodge(self, defender):
        """
        Calculate if an attack is dodged.
        
        Args:
            defender (CombatEntity): The defending entity
            
        Returns:
            bool: True if attack was dodged
        """
        # Dodge chance based on agility
        dodge_chance = min(0.15, defender.agility / 150)  # Max 15% dodge chance
        return random.random() < dodge_chance

# Combat utility functions
def create_enemy_from_template(enemy_type, level_modifier=0):
    """
    Create an enemy from a template with level scaling.
    
    Args:
        enemy_type (str): Type of enemy to create
        level_modifier (int): Level modifier for scaling
        
    Returns:
        dict: Enemy data dictionary
    """
    enemy_templates = {
        'goblin': {
            'name': 'Goblin',
            'attack': 8,
            'defense': 3,
            'agility': 5,
            'magic': 1,
            'health': 10,
            'type': 'normal',
            'ai_behavior': 'aggressive'
        },
        'orc': {
            'name': 'Orc',
            'attack': 12,
            'defense': 6,
            'agility': 2,
            'magic': 1,
            'health': 20,
            'type': 'normal',
            'ai_behavior': 'aggressive'
        },
        'skeleton': {
            'name': 'Skeleton',
            'attack': 10,
            'defense': 4,
            'agility': 4,
            'magic': 2,
            'health': 9,
            'type': 'undead',
            'ai_behavior': 'balanced'
        },
        'demon': {
            'name': 'Lesser Demon',
            'attack': 15,
            'defense': 8,
            'agility': 6,
            'magic': 10,
            'health': 50,
            'type': 'demon',
            'ai_behavior': 'balanced'
        }
    }
    
    if enemy_type not in enemy_templates:
        enemy_type = 'goblin'  # Default fallback
        
    enemy_data = enemy_templates[enemy_type].copy()
    
    # Apply level scaling
    if level_modifier > 0:
        enemy_data['attack'] += level_modifier * 2
        enemy_data['defense'] += level_modifier
        enemy_data['agility'] += level_modifier
        enemy_data['magic'] += level_modifier
        enemy_data['health'] += level_modifier * 10
        enemy_data['name'] = f"Level {level_modifier + 1} {enemy_data['name']}"
        
    return enemy_data