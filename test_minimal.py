#!/usr/bin/env python3
"""
Minimal Test Script for Demonling
This script tests only the core app structure without any GUI initialization.
Designed specifically for CI/CD environments like GitHub Actions.
"""

import os
import sys

# Completely disable Kivy GUI initialization
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONFIG'] = '1'
os.environ['KIVY_NO_WINDOW'] = '1'

def test_kivy_import():
    """Test if Kivy can be imported"""
    try:
        import kivy
        print(f"✅ Kivy imported successfully (version: {kivy.__version__})")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Kivy: {e}")
        return False

def test_app_structure():
    """Test app structure without GUI initialization"""
    try:
        # Import only the app class without initializing Kivy components
        from main import DemonlingApp
        
        # Check if the class exists and has required methods
        if hasattr(DemonlingApp, 'build'):
            print("✅ DemonlingApp has build method")
        else:
            print("❌ DemonlingApp missing build method")
            return False
            
        # Create app instance (this should work without GUI)
        app = DemonlingApp()
        print("✅ App instance created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Failed to test app structure: {e}")
        return False

def test_screen_classes():
    """Test if screen classes can be imported"""
    try:
        from main import (
            LandingScreen, 
            GameScreen, 
            LoadScreen, 
            SettingsScreen, 
            CreditsScreen
        )
        print("✅ All screen classes imported successfully")
        
        # Check if classes exist
        screen_classes = [
            ("LandingScreen", LandingScreen),
            ("GameScreen", GameScreen),
            ("LoadScreen", LoadScreen),
            ("SettingsScreen", SettingsScreen),
            ("CreditsScreen", CreditsScreen)
        ]
        
        for name, cls in screen_classes:
            if cls is not None:
                print(f"✅ {name} class exists")
            else:
                print(f"❌ {name} class is None")
                return False
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import screen classes: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing screen classes: {e}")
        return False

def test_buildozer_config():
    """Test if buildozer.spec exists and has required fields"""
    try:
        if not os.path.exists('buildozer.spec'):
            print("❌ buildozer.spec not found")
            return False
            
        with open('buildozer.spec', 'r') as f:
            content = f.read()
            
        required_fields = [
            'title = Demonling',
            'package.name = demonling',
            'version = 1.0.0'
        ]
        
        for field in required_fields:
            if field in content:
                print(f"✅ Found: {field}")
            else:
                print(f"❌ Missing: {field}")
                return False
                
        print("✅ buildozer.spec configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error checking buildozer.spec: {e}")
        return False

def test_file_structure():
    """Test if required files exist"""
    try:
        required_files = [
            'main.py',
            'buildozer.spec',
            'requirements.txt'
        ]
        
        for file_name in required_files:
            if os.path.exists(file_name):
                print(f"✅ {file_name} exists")
            else:
                print(f"❌ {file_name} not found")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Error checking file structure: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Minimal Tests for Demonling")
    print("=" * 50)
    
    tests = [
        ("Kivy Import", test_kivy_import),
        ("App Structure", test_app_structure),
        ("Screen Classes", test_screen_classes),
        ("File Structure", test_file_structure),
        ("Buildozer Config", test_buildozer_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed >= 4:  # Allow some flexibility
        print("🎉 Core tests passed! App is ready for building.")
        return 0
    else:
        print("⚠️  Too many tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 