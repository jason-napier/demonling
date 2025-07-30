# 🕹️ Demonling: Rise of the Realm Lord

A mobile RPG game built with Kivy where you rise from nothing to become the ultimate Demon Lord!

## 🎮 Game Overview

Demonling is a single-player RPG where you start as a weak demon and gradually build your power through:
- **Quest Progression**: Complete quest chains to unlock new features
- **Turn-Based Combat**: Strategic combat with attack, defend, and special abilities
- **Character Development**: Level up to increase stats and unlock abilities
- **Energy Management**: Real-time energy regeneration, including offline progression
- **Resource Collection**: Gather gold and soul shards to advance your demon lord

## 🚀 Features

### Core Gameplay
- **Home Screen**: View stats, energy, and navigate to different game areas
- **Quest Chains**: Linear progression with unlockable quests
- **Combat System**: Turn-based combat with multiple actions
- **Character Progression**: Level up system with stat growth
- **Energy System**: Real-time regeneration with offline accumulation

### Current Quest Chains
- **Ash & Bone**: Starting quest chain (5 quests)
- **Blood & Iron**: Second quest chain (unlocks after Ash & Bone)

### Combat Features
- **Basic Actions**: Attack and Defend
- **Special Abilities**: Fireball, Heal, Stun (unlock at higher levels)
- **Strategic Depth**: Defense stance reduces damage
- **Enemy Variety**: Different enemies with unique stats

### Progression Systems
- **Level Up**: Gain XP to increase level and stats
- **Stat Growth**: Health, Attack, Defense, Agility, Magic increase with level
- **Feature Unlocks**: New abilities and systems unlock as you progress
- **Save System**: Automatic save/load with offline progression

## 🛠️ Technical Features

### Cross-Platform
- **Mobile-Ready**: Designed for Android and iOS deployment
- **Kivy Framework**: Modern Python UI framework
- **Responsive Design**: Adapts to different screen sizes

### Performance
- **Efficient Architecture**: Modular design with clear separation of concerns
- **Data Persistence**: JSON-based save system with backup functionality
- **Memory Management**: Optimized for mobile device constraints

## 📱 Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Desktop Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py

# Run tests
python test_game.py
```

### Android Build
```bash
# Install buildozer
pip install buildozer

# Initialize buildozer (first time only)
buildozer init

# Build APK
buildozer android debug

# Install on device
buildozer android deploy
```

### iOS Build
```bash
# Requires macOS with Xcode
# Install kivy-ios
pip install kivy-ios

# Build for iOS
kivy-ios build python3 kivy

# Create Xcode project
kivy-ios create <YourApp> <directory>
```

## 🎯 Game Progression

### Starting Out
1. **Level 1**: Begin with basic stats and 10 energy
2. **First Quest**: Complete "Awakening" in Ash & Bone chain
3. **Combat Tutorial**: Learn attack and defend mechanics
4. **Energy Management**: Understand energy costs and regeneration

### Mid-Game
1. **Level 5**: Unlock first special ability (Fireball)
2. **Chain Completion**: Finish Ash & Bone to unlock minions
3. **Strategic Combat**: Use abilities and defensive tactics
4. **Resource Management**: Balance energy spending and soul shard use

### Late Game
1. **Level 15+**: Unlock additional abilities and features
2. **Multiple Chains**: Progress through various quest chains
3. **Advanced Combat**: Master all combat abilities
4. **Feature Unlocks**: Access castle, dungeons, and other systems

## 🏗️ Architecture

### Core Components
- **`main.py`**: Application entry point and screen management
- **`game_manager.py`**: Central game logic coordinator
- **`player.py`**: Player character with stats and progression
- **`quest_system.py`**: Quest chains and progression logic
- **`combat_system.py`**: Turn-based combat mechanics
- **`ui_screens.py`**: Kivy UI screens and interfaces
- **`data_persistence.py`**: Save/load functionality
- **`constants.py`**: Game configuration and balance

### Design Patterns
- **Event-Driven**: Combat and progression use event dispatching
- **Modular Design**: Clear separation of game systems
- **Data-Driven**: Quests and enemies defined in data structures
- **MVC Pattern**: UI, logic, and data layers are separated

## 🎨 Customization

### Game Balance
Edit `constants.py` to adjust:
- Starting stats and resources
- Level progression rates
- Energy regeneration timing
- Combat damage formulas

### Quest Content
Modify `quest_system.py` to:
- Add new quest chains
- Create custom enemies
- Design unique rewards
- Implement special quest mechanics

### UI Theming
Update `constants.py` color values:
- Primary and secondary colors
- UI element styling
- Text and background colors

## 📱 Mobile Deployment

### Android
1. **Development**: Test on desktop first
2. **Build Setup**: Configure `buildozer.spec` with your app details
3. **Build Process**: Use `buildozer android debug` for testing
4. **Release**: Use `buildozer android release` for production
5. **Play Store**: Follow Google Play Store guidelines

### iOS
1. **Development**: Requires macOS with Xcode
2. **Certificates**: Set up Apple Developer certificates
3. **Build Process**: Use kivy-ios tools
4. **App Store**: Follow Apple App Store guidelines

## 🧪 Testing

### Unit Tests
```bash
python test_game.py
```

### Manual Testing
1. **Start Game**: Verify main screen loads
2. **Combat**: Test all combat actions
3. **Progression**: Level up and unlock features
4. **Save/Load**: Test data persistence
5. **Energy**: Verify regeneration timing

## 🔧 Development

### Adding New Features
1. **Design**: Plan the feature and its integration
2. **Implementation**: Add to appropriate modules
3. **UI**: Create or update screens in `ui_screens.py`
4. **Testing**: Add tests and verify functionality
5. **Documentation**: Update README and code comments

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Document functions and classes
- Keep functions focused and modular

## 🐛 Troubleshooting

### Common Issues
- **Import Errors**: Check if all dependencies are installed
- **Screen Issues**: Verify Kivy version compatibility
- **Save Problems**: Check file permissions
- **Build Errors**: Ensure buildozer is properly configured

### Performance Issues
- **Memory Usage**: Monitor on low-end devices
- **Battery Drain**: Optimize update frequencies
- **Loading Times**: Minimize asset sizes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the code documentation

## 🎯 Roadmap

### Phase 1 (Complete)
- ✅ Basic game structure
- ✅ Combat system
- ✅ Quest progression
- ✅ Save/load functionality

### Phase 2 (Planned)
- 🔄 Equipment system
- 🔄 More quest chains
- 🔄 Castle management
- 🔄 Minion system

### Phase 3 (Future)
- 📋 Dungeon exploration
- 📋 PvP elements
- 📋 Achievements
- 📋 Daily challenges

---

**Ready to begin your journey as a Demon Lord? Run `python main.py` and start your conquest!** 👹