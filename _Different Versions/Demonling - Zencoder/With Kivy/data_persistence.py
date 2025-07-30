"""
Data Persistence - Handles saving and loading game data
"""

import json
import os
from typing import Dict, Optional
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore
from constants import SAVE_FILE

class DataManager:
    """Manages game data persistence"""
    
    def __init__(self):
        # Use Kivy's JsonStore for cross-platform compatibility
        self.store = JsonStore(SAVE_FILE)
        self.save_key = 'game_data'
    
    def save_game(self, game_data: Dict) -> bool:
        """Save game data to file"""
        try:
            self.store.put(self.save_key, **game_data)
            Logger.info(f"DataManager: Game saved successfully to {SAVE_FILE}")
            return True
        except Exception as e:
            Logger.error(f"DataManager: Failed to save game: {e}")
            return False
    
    def load_game(self) -> Optional[Dict]:
        """Load game data from file"""
        try:
            if self.store.exists(self.save_key):
                data = self.store.get(self.save_key)
                Logger.info(f"DataManager: Game loaded successfully from {SAVE_FILE}")
                return data
            else:
                Logger.info("DataManager: No save file found")
                return None
        except Exception as e:
            Logger.error(f"DataManager: Failed to load game: {e}")
            return None
    
    def delete_save(self) -> bool:
        """Delete save file"""
        try:
            if self.store.exists(self.save_key):
                self.store.delete(self.save_key)
                Logger.info("DataManager: Save file deleted")
                return True
            else:
                Logger.info("DataManager: No save file to delete")
                return False
        except Exception as e:
            Logger.error(f"DataManager: Failed to delete save file: {e}")
            return False
    
    def has_save_file(self) -> bool:
        """Check if save file exists"""
        return self.store.exists(self.save_key)
    
    def backup_save(self) -> bool:
        """Create backup of save file"""
        try:
            if self.store.exists(self.save_key):
                data = self.store.get(self.save_key)
                backup_store = JsonStore(f"{SAVE_FILE}.backup")
                backup_store.put(self.save_key, **data)
                Logger.info("DataManager: Backup created successfully")
                return True
            else:
                Logger.info("DataManager: No save file to backup")
                return False
        except Exception as e:
            Logger.error(f"DataManager: Failed to create backup: {e}")
            return False
    
    def restore_backup(self) -> bool:
        """Restore from backup file"""
        try:
            backup_store = JsonStore(f"{SAVE_FILE}.backup")
            if backup_store.exists(self.save_key):
                data = backup_store.get(self.save_key)
                self.store.put(self.save_key, **data)
                Logger.info("DataManager: Backup restored successfully")
                return True
            else:
                Logger.info("DataManager: No backup file found")
                return False
        except Exception as e:
            Logger.error(f"DataManager: Failed to restore backup: {e}")
            return False
    
    def get_save_info(self) -> Dict:
        """Get information about save file"""
        try:
            if self.store.exists(self.save_key):
                data = self.store.get(self.save_key)
                return {
                    'exists': True,
                    'timestamp': data.get('timestamp', 0),
                    'player_level': data.get('player', {}).get('level', 1),
                    'player_gold': data.get('player', {}).get('gold', 0),
                    'player_soul_shards': data.get('player', {}).get('soul_shards', 0),
                    'game_version': data.get('game_version', 'Unknown')
                }
            else:
                return {'exists': False}
        except Exception as e:
            Logger.error(f"DataManager: Failed to get save info: {e}")
            return {'exists': False, 'error': str(e)}
    
    def export_save(self, filepath: str) -> bool:
        """Export save to specified file"""
        try:
            if self.store.exists(self.save_key):
                data = self.store.get(self.save_key)
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
                Logger.info(f"DataManager: Save exported to {filepath}")
                return True
            else:
                Logger.info("DataManager: No save file to export")
                return False
        except Exception as e:
            Logger.error(f"DataManager: Failed to export save: {e}")
            return False
    
    def import_save(self, filepath: str) -> bool:
        """Import save from specified file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                self.store.put(self.save_key, **data)
                Logger.info(f"DataManager: Save imported from {filepath}")
                return True
            else:
                Logger.info(f"DataManager: Import file not found: {filepath}")
                return False
        except Exception as e:
            Logger.error(f"DataManager: Failed to import save: {e}")
            return False
    
    def clear_all_data(self) -> bool:
        """Clear all stored data"""
        try:
            self.store.clear()
            Logger.info("DataManager: All data cleared")
            return True
        except Exception as e:
            Logger.error(f"DataManager: Failed to clear data: {e}")
            return False
    
    def get_storage_size(self) -> int:
        """Get approximate storage size in bytes"""
        try:
            if self.store.exists(self.save_key):
                data = self.store.get(self.save_key)
                return len(json.dumps(data).encode('utf-8'))
            else:
                return 0
        except Exception as e:
            Logger.error(f"DataManager: Failed to get storage size: {e}")
            return 0