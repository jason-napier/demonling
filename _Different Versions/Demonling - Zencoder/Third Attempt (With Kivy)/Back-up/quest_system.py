"""
Quest System Module

This module manages all quest-related functionality including
quest chains, progress tracking, and reward distribution.
"""

import json
from kivy.logger import Logger
from combat_system import create_enemy_from_template

class QuestSystem:
    """
    Main quest system that manages quest chains, progress, and rewards.
    """
    
    def __init__(self):
        """Initialize quest system with default quest chains"""
        Logger.info("QuestSystem: Initializing")
        
        # Quest progress tracking
        self.completed_quests = set()
        self.unlocked_quests = set()
        
        # Initialize quest data
        self.quest_chains = self.create_default_quest_chains()
        
        # Unlock first quest
        self.unlock_initial_quests()
        
        Logger.info("QuestSystem: Initialization complete")
        
    def create_default_quest_chains(self):
        """
        Create the default quest chains for the game.
        
        Returns:
            dict: Dictionary of quest chains
        """
        quest_chains = {
            "Ash & Bone": {
                "description": "Your first steps into the demonic realm",
                "quests": {
                    "ash_bone_1": {
                        "name": "Weakling's Trial",
                        "description": "Defeat a weak goblin to prove your basic combat skills",
                        "energy_cost": 10,
                        "xp_reward": 25,
                        "gold_reward": 15,
                        "soul_shard_reward": 1,
                        "enemy": create_enemy_from_template('goblin', 0),
                        "prerequisites": [],
                        "unlocks": ["ash_bone_2"]
                    },
                    "ash_bone_2": {
                        "name": "Goblin Slayer",
                        "description": "Face a stronger goblin warrior",
                        "energy_cost": 15,
                        "xp_reward": 40,
                        "gold_reward": 25,
                        "soul_shard_reward": 1,
                        "enemy": create_enemy_from_template('goblin', 1),
                        "prerequisites": ["ash_bone_1"],
                        "unlocks": ["ash_bone_3"]
                    },
                    "ash_bone_3": {
                        "name": "Orc Encounter",
                        "description": "Test your might against an orc",
                        "energy_cost": 20,
                        "xp_reward": 60,
                        "gold_reward": 40,
                        "soul_shard_reward": 1,
                        "enemy": create_enemy_from_template('orc', 0),
                        "prerequisites": ["ash_bone_2"],
                        "unlocks": ["ash_bone_4"]
                    },
                    "ash_bone_4": {
                        "name": "Undead Guardian",
                        "description": "Defeat the skeletal guardian of the ancient ruins",
                        "energy_cost": 25,
                        "xp_reward": 80,
                        "gold_reward": 60,
                        "soul_shard_reward": 2,
                        "enemy": create_enemy_from_template('skeleton', 1),
                        "prerequisites": ["ash_bone_3"],
                        "unlocks": ["ash_bone_5"]
                    },
                    "ash_bone_5": {
                        "name": "Demon's First Challenge",
                        "description": "Face your first true demon opponent",
                        "energy_cost": 30,
                        "xp_reward": 120,
                        "gold_reward": 100,
                        "soul_shard_reward": 3,
                        "enemy": create_enemy_from_template('demon', 0),
                        "prerequisites": ["ash_bone_4"],
                        "unlocks": []  # This unlocks the next chain
                    }
                }
            },
            "Realm of Shadows": {
                "description": "Venture into the darker realms to gain more power",
                "quests": {
                    "shadows_1": {
                        "name": "Shadow Lurker",
                        "description": "Hunt down a creature of pure shadow",
                        "energy_cost": 35,
                        "xp_reward": 150,
                        "gold_reward": 120,
                        "soul_shard_reward": 2,
                        "enemy": {
                            "name": "Shadow Lurker",
                            "attack": 18,
                            "defense": 10,
                            "agility": 12,
                            "magic": 8,
                            "health": 180,
                            "type": "shadow",
                            "ai_behavior": "balanced"
                        },
                        "prerequisites": ["ash_bone_5"],
                        "unlocks": ["shadows_2"]
                    },
                    "shadows_2": {
                        "name": "Dark Mage",
                        "description": "Defeat a corrupted mage who has fallen to darkness",
                        "energy_cost": 40,
                        "xp_reward": 200,
                        "gold_reward": 150,
                        "soul_shard_reward": 3,
                        "enemy": {
                            "name": "Dark Mage",
                            "attack": 22,
                            "defense": 8,
                            "agility": 8,
                            "magic": 20,
                            "health": 160,
                            "type": "human",
                            "ai_behavior": "defensive"
                        },
                        "prerequisites": ["shadows_1"],
                        "unlocks": ["shadows_3"]
                    },
                    "shadows_3": {
                        "name": "Shadow Lord",
                        "description": "Face the master of the shadow realm",
                        "energy_cost": 50,
                        "xp_reward": 300,
                        "gold_reward": 250,
                        "soul_shard_reward": 5,
                        "enemy": {
                            "name": "Shadow Lord",
                            "attack": 28,
                            "defense": 15,
                            "agility": 15,
                            "magic": 25,
                            "health": 250,
                            "type": "shadow",
                            "ai_behavior": "balanced"
                        },
                        "prerequisites": ["shadows_2"],
                        "unlocks": []  # This unlocks features like minions
                    }
                }
            },
            "Infernal Ascension": {
                "description": "The final trials before claiming your throne",
                "quests": {
                    "infernal_1": {
                        "name": "Demon Knight",
                        "description": "Defeat a powerful demon knight",
                        "energy_cost": 60,
                        "xp_reward": 400,
                        "gold_reward": 300,
                        "soul_shard_reward": 4,
                        "enemy": {
                            "name": "Demon Knight",
                            "attack": 35,
                            "defense": 20,
                            "agility": 10,
                            "magic": 15,
                            "health": 300,
                            "type": "demon",
                            "ai_behavior": "aggressive"
                        },
                        "prerequisites": ["shadows_3"],
                        "unlocks": ["infernal_2"]
                    },
                    "infernal_2": {
                        "name": "Arch-Demon",
                        "description": "Challenge one of the mighty arch-demons",
                        "energy_cost": 80,
                        "xp_reward": 600,
                        "gold_reward": 500,
                        "soul_shard_reward": 6,
                        "enemy": {
                            "name": "Arch-Demon",
                            "attack": 45,
                            "defense": 25,
                            "agility": 20,
                            "magic": 30,
                            "health": 400,
                            "type": "demon",
                            "ai_behavior": "balanced"
                        },
                        "prerequisites": ["infernal_1"],
                        "unlocks": ["infernal_3"]
                    },
                    "infernal_3": {
                        "name": "Realm Lord Trial",
                        "description": "Face the ultimate trial to become Realm Lord",
                        "energy_cost": 100,
                        "xp_reward": 1000,
                        "gold_reward": 1000,
                        "soul_shard_reward": 10,
                        "enemy": {
                            "name": "Realm Guardian",
                            "attack": 60,
                            "defense": 30,
                            "agility": 25,
                            "magic": 40,
                            "health": 500,
                            "type": "guardian",
                            "ai_behavior": "balanced"
                        },
                        "prerequisites": ["infernal_2"],
                        "unlocks": []  # Game completion
                    }
                }
            }
        }
        
        return quest_chains
        
    def unlock_initial_quests(self):
        """Unlock the first available quests"""
        self.unlocked_quests.add("ash_bone_1")
        Logger.info("QuestSystem: Initial quests unlocked")
        
    def get_quest_chains(self):
        """Get all quest chains"""
        return self.quest_chains
        
    def get_quest_data(self, quest_id):
        """
        Get data for a specific quest.
        
        Args:
            quest_id (str): ID of the quest
            
        Returns:
            dict: Quest data or None if not found
        """
        for chain_name, chain_data in self.quest_chains.items():
            if quest_id in chain_data["quests"]:
                return chain_data["quests"][quest_id]
        return None
        
    def get_quest_status(self, quest_id):
        """
        Get the status of a quest.
        
        Args:
            quest_id (str): ID of the quest
            
        Returns:
            str: 'completed', 'available', or 'locked'
        """
        if quest_id in self.completed_quests:
            return 'completed'
        elif quest_id in self.unlocked_quests:
            return 'available'
        else:
            return 'locked'
            
    def can_start_quest(self, quest_id):
        """
        Check if a quest can be started.
        
        Args:
            quest_id (str): ID of the quest
            
        Returns:
            bool: True if quest can be started
        """
        return quest_id in self.unlocked_quests
        
    def complete_quest(self, quest_id):
        """
        Mark a quest as completed and handle unlocking.
        
        Args:
            quest_id (str): ID of the quest to complete
            
        Returns:
            bool: True if this was the first completion
        """
        quest_data = self.get_quest_data(quest_id)
        if not quest_data:
            Logger.error(f"QuestSystem: Quest {quest_id} not found")
            return False
            
        # Check if this is first completion
        first_completion = quest_id not in self.completed_quests
        
        # Mark as completed
        self.completed_quests.add(quest_id)
        
        # Unlock next quests
        for unlock_quest in quest_data.get("unlocks", []):
            if self.check_prerequisites(unlock_quest):
                self.unlocked_quests.add(unlock_quest)
                Logger.info(f"QuestSystem: Quest {unlock_quest} unlocked")
                
        Logger.info(f"QuestSystem: Quest {quest_id} completed")
        return first_completion
        
    def check_prerequisites(self, quest_id):
        """
        Check if all prerequisites for a quest are met.
        
        Args:
            quest_id (str): ID of the quest to check
            
        Returns:
            bool: True if all prerequisites are met
        """
        quest_data = self.get_quest_data(quest_id)
        if not quest_data:
            return False
            
        prerequisites = quest_data.get("prerequisites", [])
        
        # Check if all prerequisites are completed
        for prereq in prerequisites:
            if prereq not in self.completed_quests:
                return False
                
        return True
        
    def get_available_quests(self):
        """
        Get all available (unlocked but not completed) quests.
        
        Returns:
            list: List of available quest IDs
        """
        available = []
        for quest_id in self.unlocked_quests:
            if quest_id not in self.completed_quests:
                available.append(quest_id)
        return available
        
    def get_completed_quests(self):
        """
        Get all completed quests.
        
        Returns:
            list: List of completed quest IDs
        """
        return list(self.completed_quests)
        
    def get_progress(self):
        """
        Get quest progress for saving.
        
        Returns:
            dict: Progress data
        """
        return {
            "completed_quests": list(self.completed_quests),
            "unlocked_quests": list(self.unlocked_quests)
        }
        
    def set_progress(self, progress_data):
        """
        Set quest progress from loaded data.
        
        Args:
            progress_data (dict): Progress data to load
        """
        self.completed_quests = set(progress_data.get("completed_quests", []))
        self.unlocked_quests = set(progress_data.get("unlocked_quests", ["ash_bone_1"]))
        
        Logger.info(f"QuestSystem: Progress loaded - {len(self.completed_quests)} completed, {len(self.unlocked_quests)} unlocked")
        
    def reset_progress(self):
        """Reset all quest progress"""
        self.completed_quests.clear()
        self.unlocked_quests.clear()
        self.unlock_initial_quests()
        Logger.info("QuestSystem: Progress reset")
        
    def get_chain_progress(self, chain_name):
        """
        Get progress for a specific quest chain.
        
        Args:
            chain_name (str): Name of the quest chain
            
        Returns:
            dict: Progress information for the chain
        """
        if chain_name not in self.quest_chains:
            return {}
            
        chain_data = self.quest_chains[chain_name]
        total_quests = len(chain_data["quests"])
        completed_count = 0
        
        for quest_id in chain_data["quests"]:
            if quest_id in self.completed_quests:
                completed_count += 1
                
        return {
            "total": total_quests,
            "completed": completed_count,
            "percentage": (completed_count / total_quests) * 100
        }
        
    def get_total_progress(self):
        """
        Get overall quest progress.
        
        Returns:
            dict: Total progress information
        """
        total_quests = 0
        completed_count = len(self.completed_quests)
        
        for chain_data in self.quest_chains.values():
            total_quests += len(chain_data["quests"])
            
        return {
            "total": total_quests,
            "completed": completed_count,
            "percentage": (completed_count / total_quests) * 100 if total_quests > 0 else 0
        }
        
    def get_next_available_quest(self):
        """
        Get the next recommended quest to attempt.
        
        Returns:
            str: Quest ID of next recommended quest, or None
        """
        # Get available quests
        available = self.get_available_quests()
        
        if not available:
            return None
            
        # Prioritize quests from earlier chains
        chain_order = ["Ash & Bone", "Realm of Shadows", "Infernal Ascension"]
        
        for chain_name in chain_order:
            if chain_name in self.quest_chains:
                for quest_id in self.quest_chains[chain_name]["quests"]:
                    if quest_id in available:
                        return quest_id
                        
        # If no prioritized quest found, return first available
        return available[0] if available else None
        
    def is_chain_completed(self, chain_name):
        """
        Check if a quest chain is fully completed.
        
        Args:
            chain_name (str): Name of the quest chain
            
        Returns:
            bool: True if chain is completed
        """
        if chain_name not in self.quest_chains:
            return False
            
        chain_data = self.quest_chains[chain_name]
        
        for quest_id in chain_data["quests"]:
            if quest_id not in self.completed_quests:
                return False
                
        return True
        
    def get_quest_rewards_summary(self, quest_id):
        """
        Get a formatted summary of quest rewards.
        
        Args:
            quest_id (str): ID of the quest
            
        Returns:
            str: Formatted reward summary
        """
        quest_data = self.get_quest_data(quest_id)
        if not quest_data:
            return "No rewards"
            
        rewards = []
        
        if quest_data.get("xp_reward", 0) > 0:
            rewards.append(f"{quest_data['xp_reward']} XP")
            
        if quest_data.get("gold_reward", 0) > 0:
            rewards.append(f"{quest_data['gold_reward']} Gold")
            
        if quest_data.get("soul_shard_reward", 0) > 0:
            rewards.append(f"{quest_data['soul_shard_reward']} Soul Shards")
            
        return ", ".join(rewards) if rewards else "No rewards"