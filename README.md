# Demonling - Turn-Based RPG Mobile Game

A Python-based mobile game built with Kivy framework, featuring a turn-based RPG adventure.

<!-- Trigger GitHub Actions build -->

## Features

- **Landing Page**: Beautiful main menu with navigation to different game sections
- **Game Screen**: Placeholder for the main game interface
- **Load Game**: Save/load functionality (placeholder)
- **Settings**: Game configuration options (placeholder)
- **Credits**: Game information and acknowledgments
- **Mobile Ready**: Can be built for Android and iOS devices

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Game (Development)

```bash
python main.py
```

The game will open in a desktop window for development and testing.

## 📱 Mobile App Conversion

### Quick Start (Automated)

Use our automated build script:

```bash
python build_mobile.py
```

This script will:
- Check all dependencies
- Guide you through the build process
- Build Android APK automatically
- Provide clear instructions for iOS builds

### For Android (Manual)

1. **Install Buildozer**:
```bash
pip install buildozer
```

2. **Install System Dependencies** (Linux/Ubuntu):
```bash
sudo apt-get update
sudo apt-get install -y python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
```

3. **Build the APK**:
```bash
buildozer android debug
```

4. **Install on Android device**:
   - Enable "Install from unknown sources" in Android settings
   - Transfer the generated APK from `bin/` folder to your device
   - Install the APK

### For iOS (Mac only)

1. **Install Kivy-iOS**:
```bash
pip install kivy-ios
```

2. **Install Xcode**:
   - Download from Mac App Store
   - Install iOS development tools

3. **Build for iOS**:
```bash
toolchain build kivy
toolchain create Demonling .
toolchain run Demonling ios
```

## 🚀 GitHub Repository Setup

### 1. Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Demonling mobile game"
```

### 2. Connect to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. Automated Builds

The repository includes GitHub Actions for automated Android builds:

- **Automatic builds** on every push to main/master branch
- **APK artifacts** available for download
- **Build status** visible in repository

### 4. Release Management

To create a release:

1. **Tag your version**:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. **Create GitHub Release**:
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Upload the APK from `bin/` folder
   - Add release notes

## Project Structure

```
Demonling/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── buildozer.spec         # Android build configuration
├── build_mobile.py        # Automated build script
├── test_installation.py   # Installation verification
├── run_game.bat          # Windows launcher
├── run_game.sh           # Linux/Mac launcher
├── README.md             # This file
├── LEARNING_GUIDE.md     # Learning resources
└── .github/
    └── workflows/
        └── build.yml     # GitHub Actions workflow
```

## Development Roadmap

### Phase 1: Basic UI ✅
- [x] Landing page with navigation
- [x] Placeholder screens
- [x] Basic styling and layout
- [x] Mobile build configuration

### Phase 2: Core Game Features (Planned)
- [ ] Character creation system
- [ ] Turn-based combat mechanics
- [ ] Quest system
- [ ] Inventory management
- [ ] Save/load functionality

### Phase 3: Advanced Features (Planned)
- [ ] Sound effects and music
- [ ] Graphics and animations
- [ ] Multiplayer features
- [ ] Cloud save support

## 📚 Learning Resources

- **Code Comments**: All code is heavily commented for learning
- **Learning Guide**: See `LEARNING_GUIDE.md` for detailed explanations
- **Kivy Documentation**: https://kivy.org/doc/stable/
- **Buildozer Documentation**: https://buildozer.readthedocs.io/

## 🔧 Troubleshooting

### Common Issues

1. **Buildozer installation problems**:
   ```bash
   pip install --upgrade pip
   pip install buildozer
   ```

2. **Android build failures**:
   - Ensure you have the required system dependencies
   - Check the buildozer.spec configuration
   - Review build logs for specific errors

3. **Mobile app crashes**:
   - Test thoroughly on desktop first
   - Check for platform-specific code
   - Verify all dependencies are included

4. **GitHub Actions build failures**:
   - Check the Actions tab in your repository
   - Review build logs for specific errors
   - Ensure all files are committed to the repository

### Debug Commands

```bash
# Test installation
python test_installation.py

# Check buildozer configuration
buildozer android debug --verbose

# Clean build artifacts
python build_mobile.py  # Choose option 4
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly: `python test_installation.py`
5. Commit your changes: `git commit -m "Add feature"`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the Kivy documentation: https://kivy.org/doc/stable/
- Review the buildozer documentation: https://buildozer.readthedocs.io/
- Create an issue in this repository
- Check the learning guide: `LEARNING_GUIDE.md`

## 🎮 Download

### Latest Release
- **Android APK**: Download from [GitHub Releases](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases)
- **iOS**: Build from source using Xcode

### Development Build
- Clone the repository
- Run `python build_mobile.py`
- Choose Android build option

---

**Happy Gaming! 🎮**

*Built with Python, Kivy, and ❤️* 