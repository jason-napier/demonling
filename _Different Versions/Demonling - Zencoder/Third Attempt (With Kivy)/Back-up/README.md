# Demonling: Rise of the Realm Lord

A mobile RPG game built with Python and Kivy, designed for Android and iOS deployment.

## 🎮 Game Overview

Demonling is a single-player RPG where you play as an aspiring Demon Lord, starting from nothing and working your way up to claim the title of Realm Lord. The game features:

- **Turn-based combat** with strategic decision-making
- **Quest chains** with progressive difficulty
- **Energy system** with real-time regeneration (including offline)
- **Character progression** with leveling and stat growth
- **Resource management** (Gold, Soul Shards, Energy)
- **Mobile-optimized** interface designed for touch screens

## 🚀 Features

### Core Gameplay
- **Home Screen**: View stats, energy, and navigate to different game areas
- **Quest System**: Complete quest chains to unlock new content and features
- **Combat System**: Strategic turn-based battles with Attack/Defend mechanics
- **Character Stats**: Level, XP, Gold, Soul Shards, Attack, Defense, Agility, Magic, Health
- **Energy System**: Real-time energy regeneration, including when the app is closed

### Technical Features
- **Cross-platform**: Runs on Windows, macOS, Linux, Android, and iOS
- **Data persistence**: Automatic save/load with backup protection
- **Offline progression**: Energy continues to regenerate when app is closed
- **Mobile-friendly**: Touch-optimized UI with appropriate button sizes

## 📱 Installation

### For Development (Desktop)

1. **Install Python 3.7+**
   ```bash
   python --version  # Should be 3.7 or higher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

### For Mobile Deployment

#### Android (using Buildozer)

1. **Install Buildozer**
   ```bash
   pip install buildozer
   ```

2. **Initialize Buildozer (if needed)**
   ```bash
   buildozer init
   ```

3. **Build APK**
   ```bash
   buildozer android debug
   ```

4. **For release build**
   ```bash
   buildozer android release
   ```

#### iOS (using kivy-ios)

1. **Install kivy-ios**
   ```bash
   pip install kivy-ios
   ```

2. **Build for iOS**
   ```bash
   toolchain build python3 kivy
   toolchain create <YourApp> <directory>
   ```

## 🎯 How to Play

### Getting Started
1. Launch the game to see your character stats
2. Your energy regenerates automatically over time
3. Use the "Quests" button to view available quest chains
4. Complete quests to gain XP, Gold, and Soul Shards

### Combat System
- **Attack**: Deal damage based on your Attack stat minus enemy Defense
- **Defend**: Reduce incoming damage by half on the next enemy attack
- Victory conditions: Reduce enemy HP to 0 to win
- Defeat conditions: If your HP reaches 0, you lose (but can retry)

### Quest Progression
- **Quest Status Indicators**:
  - ✅ **Completed**: Quest finished, can be replayed
  - 🟢 **Available**: Quest unlocked and ready to attempt
  - 🔒 **Locked**: Prerequisites not met
- **Quest Chains**: Complete quests in order to unlock new ones
- **Rewards**: First-time completion grants Soul Shards (premium currency)

### Energy System
- Each quest costs energy to attempt
- Energy regenerates at 1 point per minute
- Energy continues to regenerate when the game is closed
- Use the "Refill Energy" button for testing purposes

## 🏗️ Project Structure

```
demonling/
├── main.py                 # Main application entry point
├── game_manager.py         # Core game logic and state management
├── combat_system.py        # Turn-based combat mechanics
├── quest_system.py         # Quest chains and progression
├── ui_components.py        # Custom UI widgets and components
├── data_manager.py         # Save/load and data persistence
├── buildozer.spec          # Mobile build configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Development

### Code Structure

- **main.py**: Entry point, screen management, and main app loop
- **game_manager.py**: Central game state, player data, and system coordination
- **combat_system.py**: Combat mechanics, enemy AI, and battle resolution
- **quest_system.py**: Quest definition, progress tracking, and rewards
- **ui_components.py**: Custom Kivy widgets for consistent UI theming
- **data_manager.py**: Save/load functionality with data integrity checks

### Key Classes

- **Player**: Manages player stats, resources, and progression
- **GameManager**: Coordinates all game systems and handles save/load
- **CombatSystem**: Handles turn-based combat between player and enemies
- **QuestSystem**: Manages quest chains, availability, and completion
- **DataManager**: Handles data persistence with backup and validation

### Adding New Features

1. **New Quest Chain**: Edit `quest_system.py` to add new quest data
2. **New Enemy Type**: Add to `combat_system.py` enemy templates
3. **New UI Elements**: Create custom widgets in `ui_components.py`
4. **New Game Mechanics**: Extend `game_manager.py` with new systems

## 📚 Game Design

### Quest Chains

1. **Ash & Bone**: Tutorial chain introducing basic combat
2. **Realm of Shadows**: Intermediate challenges with stronger enemies
3. **Infernal Ascension**: Final trials leading to Realm Lord status

### Combat Balance

- **Player Growth**: Stats increase with each level up
- **Enemy Scaling**: Enemies get stronger in later quest chains
- **Energy Costs**: Higher-level quests require more energy
- **Reward Scaling**: Better rewards for more difficult content

### Progression Systems

- **Experience**: Gained from completing quests
- **Gold**: Standard currency for future features
- **Soul Shards**: Premium currency, awarded once per quest
- **Energy**: Limits quest attempts, regenerates over time

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Save File Issues**: Delete save files to start fresh
   - Windows: `%USERPROFILE%\.demonling\`
   - macOS/Linux: `~/.demonling/`

3. **Mobile Build Issues**: Ensure Buildozer is properly configured
   ```bash
   buildozer android clean
   ```

### Debug Mode

- Enable debug logging by setting log level in `buildozer.spec`
- Use the "Refill Energy" button for testing without waiting
- Check console output for detailed error messages

## 🎮 Future Features (Planned)

### Phase 2: Advanced Combat
- **Items**: Potions, scrolls, and consumables
- **Special Abilities**: Fireball, stun, summon mechanics
- **Passive Abilities**: Regeneration, damage bonuses
- **Equipment**: Weapons, armor, and accessories

### Phase 3: Kingdom Management
- **Minions**: Recruit and manage demonic followers
- **Castle**: Build and upgrade your demonic stronghold
- **Dungeons**: Create and manage resource-generating dungeons

### Phase 4: Endgame Content
- **PvP**: Battle other players asynchronously
- **Guilds**: Join forces with other demon lords
- **Events**: Limited-time challenges and rewards

## 📄 License

This project is developed for educational and entertainment purposes. Feel free to use and modify the code for your own projects.

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome! Feel free to:

1. Report bugs or issues
2. Suggest new features or improvements
3. Submit code improvements
4. Share feedback on game balance

## 📞 Support

For questions or support:
- Check the troubleshooting section above
- Review the code comments for implementation details
- Test on desktop before mobile deployment

---

**Enjoy conquering the demonic realms!** 👹⚔️🏰