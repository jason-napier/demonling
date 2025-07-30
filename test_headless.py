#!/usr/bin/env python3
"""
Headless Test Script for Demonling
This script tests the app structure without creating GUI windows.
Useful for CI/CD environments like GitHub Actions.
"""

import os
import sys

# Set environment variables for headless operation
os.environ['DISPLAY'] = ':99'
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'

def test_kivy_import():
    """Test if Kivy can be imported"""
    try:
        import kivy
        print(f"✅ Kivy imported successfully (version: {kivy.__version__})")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Kivy: {e}")
        return False

def test_app_imports():
    """Test if all app classes can be imported"""
    try:
        from main import (
            DemonlingApp, 
            LandingScreen, 
            GameScreen, 
            LoadScreen, 
            SettingsScreen, 
            CreditsScreen
        )
        print("✅ All app classes imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import app classes: {e}")
        return False

def test_app_creation():
    """Test if app instance can be created"""
    try:
        from main import DemonlingApp
        
        # Create app instance without running it
        app = DemonlingApp()
        print("✅ App instance created successfully")
        
        # Check app properties
        if hasattr(app, 'title'):
            print(f"✅ App title: {app.title}")
        else:
            print("✅ App has default title")
            
        return True
    except Exception as e:
        print(f"❌ Failed to create app instance: {e}")
        return False

def test_screen_manager():
    """Test if screen manager can be created"""
    try:
        from kivy.uix.screenmanager import ScreenManager
        from main import DemonlingApp
        
        app = DemonlingApp()
        sm = app.build()
        
        if sm is not None:
            print("✅ Screen manager created successfully")
            print(f"✅ Number of screens: {len(sm.screens)}")
            
            # Check if expected screens exist
            expected_screens = ['landing', 'game_screen', 'load_screen', 'settings_screen', 'credits_screen']
            for screen_name in expected_screens:
                if screen_name in sm.screen_names:
                    print(f"✅ Screen '{screen_name}' found")
                else:
                    print(f"⚠️  Screen '{screen_name}' not found")
            
            return True
        else:
            print("❌ Screen manager is None")
            return False
            
    except Exception as e:
        print(f"❌ Failed to create screen manager: {e}")
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

def main():
    """Run all tests"""
    print("🧪 Running Headless Tests for Demonling")
    print("=" * 50)
    
    tests = [
        ("Kivy Import", test_kivy_import),
        ("App Imports", test_app_imports),
        ("App Creation", test_app_creation),
        ("Screen Manager", test_screen_manager),
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
    
    if passed == total:
        print("🎉 All tests passed! App is ready for building.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 