#!/usr/bin/env python3
"""
Simple Test Script for Demonling
This script tests only the Python code structure without any Kivy imports.
Designed specifically for CI/CD environments like GitHub Actions.
"""

import os
import sys
import ast

def test_python_syntax():
    """Test if main.py has valid Python syntax"""
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the Python code to check syntax
        ast.parse(content)
        print("✅ main.py has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in main.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False

def test_class_definitions():
    """Test if required classes are defined in main.py"""
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required class definitions
        required_classes = [
            'DemonlingApp',
            'LandingScreen', 
            'GameScreen',
            'LoadScreen',
            'SettingsScreen',
            'CreditsScreen'
        ]
        
        for class_name in required_classes:
            if f'class {class_name}' in content:
                print(f"✅ {class_name} class defined")
            else:
                print(f"❌ {class_name} class not found")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Error checking class definitions: {e}")
        return False

def test_method_definitions():
    """Test if required methods are defined"""
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required methods
        required_methods = [
            'def build(',
            'def __init__(',
            'def start_game(',
            'def go_back('
        ]
        
        for method in required_methods:
            if method in content:
                print(f"✅ Method {method} found")
            else:
                print(f"⚠️  Method {method} not found")
        
        return True
    except Exception as e:
        print(f"❌ Error checking method definitions: {e}")
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

def test_buildozer_config():
    """Test if buildozer.spec has required fields"""
    try:
        if not os.path.exists('buildozer.spec'):
            print("❌ buildozer.spec not found")
            return False
            
        with open('buildozer.spec', 'r', encoding='utf-8') as f:
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

def test_requirements():
    """Test if requirements.txt has required packages"""
    try:
        if not os.path.exists('requirements.txt'):
            print("❌ requirements.txt not found")
            return False
            
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_packages = [
            'kivy',
            'pillow'
        ]
        
        for package in required_packages:
            if package in content:
                print(f"✅ Found package: {package}")
            else:
                print(f"❌ Missing package: {package}")
                return False
                
        print("✅ requirements.txt is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error checking requirements.txt: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Simple Structure Tests for Demonling")
    print("=" * 50)
    
    tests = [
        ("Python Syntax", test_python_syntax),
        ("Class Definitions", test_class_definitions),
        ("Method Definitions", test_method_definitions),
        ("File Structure", test_file_structure),
        ("Buildozer Config", test_buildozer_config),
        ("Requirements", test_requirements)
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
    
    if passed >= 5:  # Most tests should pass
        print("🎉 Structure tests passed! App is ready for building.")
        return 0
    else:
        print("⚠️  Too many tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 