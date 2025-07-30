#!/usr/bin/env python3
"""
Mobile Build Script for Demonling
This script automates the process of building mobile apps for Android and iOS.

Features:
- Android APK building using Buildozer
- iOS app building using Kivy-iOS (Mac only)
- Automatic dependency checking
- Build status reporting
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class MobileBuilder:
    """
    Class to handle mobile app building for Demonling
    """
    
    def __init__(self):
        """Initialize the builder with project information"""
        self.project_name = "Demonling"
        self.project_dir = Path.cwd()
        self.buildozer_spec = self.project_dir / "buildozer.spec"
        
        # Check if we're on the right platform
        self.system = platform.system()
        print(f"🖥️  Detected system: {self.system}")
    
    def check_dependencies(self):
        """
        Check if all required dependencies are installed
        Returns True if all dependencies are available
        """
        print("🔍 Checking dependencies...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 7):
            print("❌ Python 3.7 or higher is required!")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check if main.py exists
        if not (self.project_dir / "main.py").exists():
            print("❌ main.py not found in current directory!")
            return False
        print("✅ main.py found")
        
        # Check if buildozer.spec exists
        if not self.buildozer_spec.exists():
            print("❌ buildozer.spec not found!")
            return False
        print("✅ buildozer.spec found")
        
        # Check if buildozer is installed
        try:
            subprocess.run(["buildozer", "--version"], 
                         capture_output=True, check=True)
            print("✅ Buildozer is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Buildozer not found. Installing...")
            self.install_buildozer()
        
        return True
    
    def install_buildozer(self):
        """Install Buildozer if not already installed"""
        try:
            print("📦 Installing Buildozer...")
            subprocess.run([sys.executable, "-m", "pip", "install", "buildozer"], 
                         check=True)
            print("✅ Buildozer installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Buildozer: {e}")
            return False
        return True
    
    def build_android(self):
        """
        Build Android APK using Buildozer
        Returns True if build was successful
        """
        print("\n🤖 Building Android APK...")
        
        try:
            # Run buildozer android debug
            print("🔨 Running buildozer android debug...")
            result = subprocess.run(["buildozer", "android", "debug"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Android APK built successfully!")
                
                # Find the APK file
                bin_dir = self.project_dir / "bin"
                if bin_dir.exists():
                    apk_files = list(bin_dir.glob("*.apk"))
                    if apk_files:
                        print(f"📱 APK file created: {apk_files[0].name}")
                        print(f"📁 Location: {apk_files[0].absolute()}")
                        return True
                    else:
                        print("⚠️  Build succeeded but no APK file found")
                        return False
                else:
                    print("⚠️  Build succeeded but bin directory not found")
                    return False
            else:
                print("❌ Android build failed!")
                print("Error output:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error during Android build: {e}")
            return False
    
    def build_ios(self):
        """
        Build iOS app using Kivy-iOS (Mac only)
        Returns True if build was successful
        """
        if self.system != "Darwin":
            print("❌ iOS builds are only supported on macOS")
            return False
        
        print("\n🍎 Building iOS app...")
        print("⚠️  iOS builds require Xcode and additional setup")
        print("📚 See README.md for iOS build instructions")
        return False
    
    def clean_builds(self):
        """Clean previous build artifacts"""
        print("\n🧹 Cleaning build artifacts...")
        
        # Remove buildozer build directories
        build_dirs = [".buildozer", "bin", ".gradle"]
        for dir_name in build_dirs:
            dir_path = self.project_dir / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"✅ Removed {dir_name}")
                except Exception as e:
                    print(f"⚠️  Could not remove {dir_name}: {e}")
    
    def run(self):
        """
        Main method to run the mobile build process
        """
        print(f"🚀 Starting {self.project_name} Mobile Build")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            print("\n❌ Dependency check failed. Please install missing dependencies.")
            return False
        
        # Ask user what to build
        print("\n📱 What would you like to build?")
        print("1. Android APK")
        print("2. iOS app (Mac only)")
        print("3. Both (if supported)")
        print("4. Clean build artifacts")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Build cancelled by user")
            return False
        
        success = True
        
        if choice == "1":
            success = self.build_android()
        elif choice == "2":
            success = self.build_ios()
        elif choice == "3":
            android_success = self.build_android()
            ios_success = self.build_ios()
            success = android_success or ios_success  # Success if at least one works
        elif choice == "4":
            self.clean_builds()
            print("✅ Clean completed")
            return True
        else:
            print("❌ Invalid choice")
            return False
        
        if success:
            print("\n🎉 Build process completed successfully!")
            print("\n📋 Next steps:")
            print("• Android: Install the APK on your device")
            print("• iOS: Use Xcode to deploy to device/simulator")
            print("• Share your app with others!")
        else:
            print("\n❌ Build process failed!")
            print("📚 Check the error messages above and refer to the README for troubleshooting")
        
        return success

def main():
    """Main function to run the mobile builder"""
    builder = MobileBuilder()
    success = builder.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 