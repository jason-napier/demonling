"""
Quest System - Manages quests and quest chains
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from constants import *

@dataclass
class Enemy:
    """Enemy data class"""
    name: str
    health: int
    attack: int
    defense: int
    agility: int
    magic: int
    
    def __post_init__(self):
        self.current_health = self.health
    
    def take_damage(self, amount):
        """Take damage"""
        damage = max(1, amount - self.defense)
        self.current_health = max(0, self.current_health - damage)
        return damage
    
    def is_alive(self):
        """Check if enemy is alive"""
        return self.current_health > 0
    
    def reset_health(self):
        """Reset health to maximum"""
        self.current_health = self.health

@dataclass
class Quest:
    """Quest data class"""
    id: str
    name: str
    description: str
    chain_id: str
    prerequisites: List[str]
    energy_cost: int
    xp_reward: int
    gold_reward: int
    soul_shard_reward: int
    enemy: Optional[Enemy] = None
    unlock_feature: Optional[str] = None

class QuestManager:
    """Manages quest chains and progression"""
    
    def __init__(self):
        self.quests = {}
        self.quest_chains = {}
        self.completed_quests = set()
        self.unlocked_quests = set()
        
        # Initialize quest data
        self._initialize_quests()
        
        # Unlock first quest
        self.unlocked_quests.add("ash_bone_01")
    
    def _initialize_quests(self):
        """Initialize all quest data"""
        
        # Ash & Bone Chain
        self.quest_chains["ash_bone"] = {
            "name": "Ash & Bone",
            "description": "Begin your journey as a demon lord",
            "quests": [
                "ash_bone_01", "ash_bone_02", "ash_bone_03", 
                "ash_bone_04", "ash_bone_05"
            ]
        }
        
        # Ash & Bone Quest 1
        self.quests["ash_bone_01"] = Quest(
            id="ash_bone_01",
            name="Awakening",
            description="You awaken in the depths of the underworld. Test your newfound demonic powers.",
            chain_id="ash_bone",
            prerequisites=[],
            energy_cost=1,
            xp_reward=10,
            gold_reward=5,
            soul_shard_reward=1,
            enemy=Enemy("Lesser Imp", 15, 3, 1, 2, 1)
        )
        
        # Ash & Bone Quest 2
        self.quests["ash_bone_02"] = Quest(
            id="ash_bone_02",
            name="First Blood",
            description="Defeat a stronger foe to prove your worth in the demonic hierarchy.",
            chain_id="ash_bone",
            prerequisites=["ash_bone_01"],
            energy_cost=2,
            xp_reward=15,
            gold_reward=8,
            soul_shard_reward=1,
            enemy=Enemy("Bone Skeleton", 25, 5, 2, 1, 0)
        )
        
        # Ash & Bone Quest 3
        self.quests["ash_bone_03"] = Quest(
            id="ash_bone_03",
            name="Claiming Territory",
            description="Establish your first foothold in the demon realm.",
            chain_id="ash_bone",
            prerequisites=["ash_bone_02"],
            energy_cost=3,
            xp_reward=20,
            gold_reward=12,
            soul_shard_reward=1,
            enemy=Enemy("Ash Wraith", 35, 7, 3, 4, 2)
        )
        
        # Ash & Bone Quest 4
        self.quests["ash_bone_04"] = Quest(
            id="ash_bone_04",
            name="Gathering Minions",
            description="Defeat other demons to force them into your service.",
            chain_id="ash_bone",
            prerequisites=["ash_bone_03"],
            energy_cost=4,
            xp_reward=25,
            gold_reward=15,
            soul_shard_reward=1,
            enemy=Enemy("Corrupted Demon", 45, 9, 4, 3, 3)
        )
        
        # Ash & Bone Quest 5 (Boss)
        self.quests["ash_bone_05"] = Quest(
            id="ash_bone_05",
            name="Lord of Ash",
            description="Face the current lord of this realm and claim their throne.",
            chain_id="ash_bone",
            prerequisites=["ash_bone_04"],
            energy_cost=5,
            xp_reward=50,
            gold_reward=25,
            soul_shard_reward=3,
            enemy=Enemy("Ash Lord", 80, 12, 6, 5, 8),
            unlock_feature="minions"
        )
        
        # Blood & Iron Chain (unlocked after Ash & Bone)
        self.quest_chains["blood_iron"] = {
            "name": "Blood & Iron",
            "description": "Expand your dominion through conquest",
            "quests": [
                "blood_iron_01", "blood_iron_02", "blood_iron_03",
                "blood_iron_04", "blood_iron_05"
            ]
        }
        
        # Blood & Iron Quest 1
        self.quests["blood_iron_01"] = Quest(
            id="blood_iron_01",
            name="Iron Throne",
            description="Seek out the Iron Throne to expand your power.",
            chain_id="blood_iron",
            prerequisites=["ash_bone_05"],
            energy_cost=3,
            xp_reward=30,
            gold_reward=20,
            soul_shard_reward=1,
            enemy=Enemy("Iron Guardian", 50, 10, 8, 2, 1)
        )
        
        # Add more quest chains as needed...
    
    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """Get a quest by ID"""
        return self.quests.get(quest_id)
    
    def can_start_quest(self, quest_id: str, player) -> bool:
        """Check if player can start a quest"""
        if quest_id not in self.quests:
            return False
        
        quest = self.quests[quest_id]
        
        # Check if quest is unlocked
        if quest_id not in self.unlocked_quests:
            return False
        
        # Check prerequisites
        for prereq in quest.prerequisites:
            if prereq not in self.completed_quests:
                return False
        
        # Check energy cost
        if player.energy < quest.energy_cost:
            return False
        
        return True
    
    def complete_quest(self, quest_id: str):
        """Mark quest as completed and unlock next quests"""
        if quest_id not in self.quests:
            return
        
        quest = self.quests[quest_id]
        self.completed_quests.add(quest_id)
        
        # Unlock next quests in chain
        self.unlock_next_quest(quest_id)
    
    def unlock_next_quest(self, completed_quest_id: str):
        """Unlock next quest(s) in the chain"""
        completed_quest = self.quests.get(completed_quest_id)
        if not completed_quest:
            return
        
        chain_id = completed_quest.chain_id
        if chain_id not in self.quest_chains:
            return
        
        chain_quests = self.quest_chains[chain_id]["quests"]
        
        try:
            current_index = chain_quests.index(completed_quest_id)
            if current_index + 1 < len(chain_quests):
                next_quest_id = chain_quests[current_index + 1]
                self.unlocked_quests.add(next_quest_id)
        except ValueError:
            pass
        
        # If this is the last quest in the chain, unlock next chain
        if completed_quest_id == "ash_bone_05":
            self.unlocked_quests.add("blood_iron_01")
    
    def is_quest_completed(self, quest_id: str) -> bool:
        """Check if quest is completed"""
        return quest_id in self.completed_quests
    
    def is_quest_unlocked(self, quest_id: str) -> bool:
        """Check if quest is unlocked"""
        return quest_id in self.unlocked_quests
    
    def get_quest_status(self, quest_id: str) -> str:
        """Get quest status (completed, unlocked, locked)"""
        if self.is_quest_completed(quest_id):
            return "completed"
        elif self.is_quest_unlocked(quest_id):
            return "unlocked"
        else:
            return "locked"
    
    def get_available_quests(self, player) -> List[Quest]:
        """Get list of available quests for player"""
        available = []
        
        for quest_id in self.unlocked_quests:
            quest = self.quests.get(quest_id)
            if quest and self.can_start_quest(quest_id, player):
                available.append(quest)
        
        return available
    
    def get_quest_chain(self, chain_id: str) -> Dict:
        """Get quest chain info"""
        return self.quest_chains.get(chain_id, {})
    
    def get_chain_progress(self, chain_id: str) -> Dict:
        """Get progress for a quest chain"""
        chain = self.quest_chains.get(chain_id)
        if not chain:
            return {}
        
        total_quests = len(chain["quests"])
        completed_count = sum(1 for q_id in chain["quests"] if q_id in self.completed_quests)
        
        return {
            "total": total_quests,
            "completed": completed_count,
            "percentage": (completed_count / total_quests) * 100 if total_quests > 0 else 0
        }
    
    def get_progress(self) -> Dict:
        """Get all quest progress for saving"""
        return {
            "completed_quests": list(self.completed_quests),
            "unlocked_quests": list(self.unlocked_quests)
        }
    
    def load_progress(self, data: Dict):
        """Load quest progress from save data"""
        self.completed_quests = set(data.get("completed_quests", []))
        self.unlocked_quests = set(data.get("unlocked_quests", ["ash_bone_01"]))