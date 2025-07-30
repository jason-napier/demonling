"""
Data Manager Module

This module handles all data persistence operations including
saving and loading game state, settings, and user preferences.
"""

import json
import os
from datetime import datetime
from kivy.logger import Logger

# Import platform safely
try:
    from kivy.utils import platform
except ImportError:
    platform = 'unknown'

class DataManager:
    """
    Handles all data persistence operations for the game.
    Manages save files, settings, and data integrity.
    """
    
    def __init__(self):
        """Initialize data manager and set up save directories"""
        Logger.info("DataManager: Initializing")
        
        # Set up save directory based on platform
        self.save_dir = self.get_save_directory()
        self.save_file = os.path.join(self.save_dir, "game_save.json")
        self.settings_file = os.path.join(self.save_dir, "settings.json")
        self.backup_file = os.path.join(self.save_dir, "game_save_backup.json")
        
        # Create save directory if it doesn't exist
        self.create_save_directory()
        
        # Default settings
        self.default_settings = {
            "sound_enabled": True,
            "music_enabled": True,
            "sound_volume": 0.8,
            "music_volume": 0.6,
            "auto_save": True,
            "energy_notifications": True,
            "first_launch": True
        }
        
        Logger.info(f"DataManager: Save directory set to {self.save_dir}")
        
    def get_save_directory(self):
        """
        Get the appropriate save directory based on platform.
        
        Returns:
            str: Path to save directory
        """
        if platform == 'android':
            # On Android, use internal storage
            try:
                from android.storage import app_storage_path
                return app_storage_path()
            except ImportError:
                # Fallback for testing on desktop
                return os.path.join(os.path.expanduser("~"), ".demonling")
        elif platform == 'ios':
            # On iOS, use Documents directory
            import tempfile
            return tempfile.gettempdir()  # Fallback for now
        else:
            # On desktop, use user home directory
            home_dir = os.path.expanduser("~")
            return os.path.join(home_dir, ".demonling")
            
    def create_save_directory(self):
        """Create the save directory if it doesn't exist"""
        try:
            os.makedirs(self.save_dir, exist_ok=True)
            Logger.info(f"DataManager: Save directory created/verified at {self.save_dir}")
        except Exception as e:
            Logger.error(f"DataManager: Failed to create save directory: {e}")
            # Fallback to current directory
            self.save_dir = "."
            self.save_file = "game_save.json"
            self.settings_file = "settings.json"
            self.backup_file = "game_save_backup.json"
            
    def save_data(self, data):
        """
        Save game data to file.
        
        Args:
            data (dict): Game data to save
        """
        try:
            # Add metadata
            save_data = {
                "game_data": data,
                "save_time": datetime.now().isoformat(),
                "version": "1.0",
                "checksum": self.calculate_checksum(data)
            }
            
            # Create backup of existing save
            if os.path.exists(self.save_file):
                self.create_backup()
                
            # Write to file
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
                
            Logger.info("DataManager: Game data saved successfully")
            
        except Exception as e:
            Logger.error(f"DataManager: Failed to save game data: {e}")
            raise
            
    def load_data(self):
        """
        Load game data from file.
        
        Returns:
            dict: Game data or None if no save exists
        """
        try:
            if not os.path.exists(self.save_file):
                Logger.info("DataManager: No save file found")
                return None
                
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
                
            # Verify data integrity
            if not self.verify_save_data(save_data):
                Logger.warning("DataManager: Save data verification failed, attempting backup")
                return self.load_backup()
                
            Logger.info("DataManager: Game data loaded successfully")
            return save_data.get("game_data", {})
            
        except Exception as e:
            Logger.error(f"DataManager: Failed to load game data: {e}")
            Logger.info("DataManager: Attempting to load backup")
            return self.load_backup()
            
    def create_backup(self):
        """Create a backup of the current save file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as src:
                    data = src.read()
                with open(self.backup_file, 'w') as dst:
                    dst.write(data)
                Logger.info("DataManager: Backup created")
        except Exception as e:
            Logger.error(f"DataManager: Failed to create backup: {e}")
            
    def load_backup(self):
        """
        Load game data from backup file.
        
        Returns:
            dict: Game data or None if backup doesn't exist
        """
        try:
            if not os.path.exists(self.backup_file):
                Logger.info("DataManager: No backup file found")
                return None
                
            with open(self.backup_file, 'r') as f:
                save_data = json.load(f)
                
            Logger.info("DataManager: Backup data loaded successfully")
            return save_data.get("game_data", {})
            
        except Exception as e:
            Logger.error(f"DataManager: Failed to load backup data: {e}")
            return None
            
    def verify_save_data(self, save_data):
        """
        Verify the integrity of save data.
        
        Args:
            save_data (dict): Save data to verify
            
        Returns:
            bool: True if data is valid
        """
        try:
            # Check if required fields exist
            if "game_data" not in save_data:
                return False
                
            # Check version compatibility
            version = save_data.get("version", "1.0")
            if not self.is_version_compatible(version):
                Logger.warning(f"DataManager: Incompatible save version: {version}")
                return False
                
            # Verify checksum if available
            if "checksum" in save_data:
                expected_checksum = save_data["checksum"]
                actual_checksum = self.calculate_checksum(save_data["game_data"])
                if expected_checksum != actual_checksum:
                    Logger.warning("DataManager: Checksum mismatch")
                    return False
                    
            return True
            
        except Exception as e:
            Logger.error(f"DataManager: Data verification failed: {e}")
            return False
            
    def calculate_checksum(self, data):
        """
        Calculate a simple checksum for data integrity.
        
        Args:
            data (dict): Data to calculate checksum for
            
        Returns:
            str: Checksum string
        """
        try:
            # Convert to JSON string and calculate hash
            json_str = json.dumps(data, sort_keys=True)
            return str(hash(json_str))
        except:
            return "0"
            
    def is_version_compatible(self, version):
        """
        Check if a save version is compatible with current game version.
        
        Args:
            version (str): Version string to check
            
        Returns:
            bool: True if compatible
        """
        # For now, accept all versions
        # In the future, implement version migration logic
        return True
        
    def save_settings(self, settings):
        """
        Save game settings.
        
        Args:
            settings (dict): Settings to save
        """
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            Logger.info("DataManager: Settings saved successfully")
        except Exception as e:
            Logger.error(f"DataManager: Failed to save settings: {e}")
            
    def load_settings(self):
        """
        Load game settings.
        
        Returns:
            dict: Settings dictionary
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                Logger.info("DataManager: Settings loaded successfully")
                
                # Merge with defaults to ensure all keys exist
                merged_settings = self.default_settings.copy()
                merged_settings.update(settings)
                return merged_settings
            else:
                Logger.info("DataManager: No settings file found, using defaults")
                return self.default_settings.copy()
                
        except Exception as e:
            Logger.error(f"DataManager: Failed to load settings: {e}")
            return self.default_settings.copy()
            
    def delete_save(self):
        """Delete the save file"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                Logger.info("DataManager: Save file deleted")
            if os.path.exists(self.backup_file):
                os.remove(self.backup_file)
                Logger.info("DataManager: Backup file deleted")
        except Exception as e:
            Logger.error(f"DataManager: Failed to delete save files: {e}")
            
    def export_save(self, export_path):
        """
        Export save data to a specific path.
        
        Args:
            export_path (str): Path to export save data to
        """
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as src:
                    data = src.read()
                with open(export_path, 'w') as dst:
                    dst.write(data)
                Logger.info(f"DataManager: Save exported to {export_path}")
            else:
                Logger.warning("DataManager: No save file to export")
        except Exception as e:
            Logger.error(f"DataManager: Failed to export save: {e}")
            
    def import_save(self, import_path):
        """
        Import save data from a specific path.
        
        Args:
            import_path (str): Path to import save data from
        """
        try:
            if os.path.exists(import_path):
                # Create backup of current save
                if os.path.exists(self.save_file):
                    self.create_backup()
                    
                # Copy imported file
                with open(import_path, 'r') as src:
                    data = src.read()
                with open(self.save_file, 'w') as dst:
                    dst.write(data)
                    
                Logger.info(f"DataManager: Save imported from {import_path}")
            else:
                Logger.error(f"DataManager: Import file not found: {import_path}")
        except Exception as e:
            Logger.error(f"DataManager: Failed to import save: {e}")
            
    def get_save_info(self):
        """
        Get information about the current save file.
        
        Returns:
            dict: Save file information
        """
        try:
            if not os.path.exists(self.save_file):
                return {"exists": False}
                
            stat = os.stat(self.save_file)
            
            # Try to load save data for additional info
            try:
                with open(self.save_file, 'r') as f:
                    save_data = json.load(f)
                    
                return {
                    "exists": True,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "save_time": save_data.get("save_time", "Unknown"),
                    "version": save_data.get("version", "Unknown"),
                    "has_backup": os.path.exists(self.backup_file)
                }
            except:
                return {
                    "exists": True,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "save_time": "Unknown",
                    "version": "Unknown",
                    "has_backup": os.path.exists(self.backup_file)
                }
                
        except Exception as e:
            Logger.error(f"DataManager: Failed to get save info: {e}")
            return {"exists": False, "error": str(e)}
            
    def cleanup_old_saves(self, days_old=30):
        """
        Clean up old save files (for space management).
        
        Args:
            days_old (int): Delete files older than this many days
        """
        try:
            cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            
            for filename in os.listdir(self.save_dir):
                if filename.startswith("game_save_") and filename.endswith(".json"):
                    filepath = os.path.join(self.save_dir, filename)
                    if os.path.getmtime(filepath) < cutoff_time:
                        os.remove(filepath)
                        Logger.info(f"DataManager: Cleaned up old save: {filename}")
                        
        except Exception as e:
            Logger.error(f"DataManager: Failed to cleanup old saves: {e}")
            
    def get_storage_usage(self):
        """
        Get storage usage information.
        
        Returns:
            dict: Storage usage information
        """
        try:
            total_size = 0
            file_count = 0
            
            for filename in os.listdir(self.save_dir):
                filepath = os.path.join(self.save_dir, filename)
                if os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                    
            return {
                "total_size": total_size,
                "file_count": file_count,
                "save_dir": self.save_dir
            }
            
        except Exception as e:
            Logger.error(f"DataManager: Failed to get storage usage: {e}")
            return {"total_size": 0, "file_count": 0, "save_dir": self.save_dir}