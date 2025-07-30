#!/usr/bin/env python3
"""
Test script to verify Demonling installation and dependencies.
Run this before running the main game to ensure everything is set up correctly.

This script checks:
1. Python version compatibility
2. Required dependencies (Kivy, KivyMD, Pillow)
3. Optional dependencies for mobile builds (Buildozer, Kivy-iOS)
"""

# Import system modules for version checking and module importing
import sys  # For accessing Python version and system information
import importlib  # For dynamically importing modules to test if they exist

def test_import(module_name, package_name=None):
    """
    Test if a module can be imported successfully.
    
    Args:
        module_name (str): The name of the module to test
        package_name (str, optional): The package name if testing a submodule
    
    Returns:
        bool: True if import successful, False if failed
    """
    try:
        # Try to import the module
        if package_name:
            # If package_name is provided, import as a submodule
            importlib.import_module(module_name, package_name)
        else:
            # Otherwise, import the module directly
            importlib.import_module(module_name)
        
        # If we get here, the import was successful
        print(f"✅ {module_name} - OK")
        return True
        
    except ImportError as e:
        # Module doesn't exist or can't be imported
        print(f"❌ {module_name} - FAILED: {e}")
        return False
        
    except Exception as e:
        # Some other error occurred (like version conflicts)
        print(f"⚠️  {module_name} - WARNING: {e}")
        return True  # Return True for warnings since the module exists

def main():
    """
    Main function that runs all the installation tests.
    
    Returns:
        bool: True if all required tests pass, False otherwise
    """
    # Print header for the test output
    print("Demonling - Installation Test")
    print("=" * 40)
    
    # Test Python version - Kivy requires Python 3.7 or higher
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if Python version meets minimum requirements
    if python_version < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        return False
    else:
        print("✅ Python version - OK")
    
    # Test required dependencies that the game needs to run
    print("\nTesting required dependencies:")
    print("-" * 30)
    
    # List of core dependencies that must be installed
    dependencies = [
        "kivy",      # Main GUI framework
        "kivymd",    # Material Design components for Kivy
        "PIL",       # Python Imaging Library (Pillow) for image handling
    ]
    
    # Track if all required dependencies pass
    all_passed = True
    
    # Test each required dependency
    for dep in dependencies:
        if not test_import(dep):
            all_passed = False  # Mark as failed if any dependency fails
    
    # Test optional dependencies for mobile app building
    print("\nTesting optional dependencies:")
    print("-" * 30)
    
    # These are optional - the game will still run without them
    # but they're needed for building mobile apps
    optional_deps = [
        "buildozer",  # For building Android APK files
        "kivy_ios",   # For building iOS apps (Mac only)
    ]
    
    # Test optional dependencies (don't affect the overall result)
    for dep in optional_deps:
        test_import(dep)
    
    # Print final results
    print("\n" + "=" * 40)
    
    if all_passed:
        # All required dependencies are installed
        print("🎉 All required dependencies are installed!")
        print("You can now run the game with: python main.py")
        return True
    else:
        # Some required dependencies are missing
        print("❌ Some required dependencies are missing.")
        print("Please install them with: pip install -r requirements.txt")
        return False

# This is the standard Python way to check if this file is being run directly
# (not imported as a module)
if __name__ == "__main__":
    # Run the main test function and exit with appropriate code
    # Exit code 0 = success, Exit code 1 = failure
    success = main()
    sys.exit(0 if success else 1) 