# 🔧 Local Android Build Guide

Since GitHub Actions might take time to set up, here's how to build your Android APK locally using WSL (Windows Subsystem for Linux).

## 🚀 Quick Local Build Setup

### Step 1: Install WSL (Windows Subsystem for Linux)

```powershell
# Open PowerShell as Administrator and run:
wsl --install
```

This will install Ubuntu on Windows. Restart your computer when prompted.

### Step 2: Set Up Build Environment

After restart, open Ubuntu terminal and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip build-essential git zip unzip openjdk-11-jdk

# Install Buildozer
pip3 install buildozer

# Install additional dependencies
sudo apt install -y \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0 \
    gstreamer1.0-plugins-{bad,base,good,ugly} \
    gstreamer1.0-{tools,x} \
    libgirepository1.0-dev \
    libcairo2-dev \
    pkg-config \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev
```

### Step 3: Navigate to Your Project

```bash
# Navigate to your project directory
cd /mnt/c/Users/nside/Documents/_Programing/Python\ Projects/Demonling

# Verify files are there
ls -la
```

### Step 4: Build Android APK

```bash
# Build the APK
buildozer android debug

# The APK will be created in the bin/ directory
ls -la bin/
```

### Step 5: Install on Android Device

1. **Enable Developer Options** on your Android device:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > Developer Options
   - Enable "USB Debugging" and "Install from Unknown Sources"

2. **Transfer APK**:
   - Copy the APK from `bin/` folder to your Android device
   - Install the APK on your device

## 🔄 Development Workflow

```bash
# 1. Make changes to your game
# 2. Test locally in WSL
python3 main.py

# 3. Build new APK
buildozer android debug

# 4. Install on device and test
```

## 🆘 Troubleshooting

### Common Issues:

1. **Buildozer not found**:
   ```bash
   pip3 install --upgrade buildozer
   ```

2. **Permission errors**:
   ```bash
   sudo chmod +x /usr/local/bin/buildozer
   ```

3. **Java not found**:
   ```bash
   sudo apt install openjdk-11-jdk
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
   ```

4. **SDK/NDK download issues**:
   ```bash
   # Buildozer will download these automatically
   # If it fails, check your internet connection
   ```

## 📱 Testing Your APK

1. **Transfer APK** to your Android device
2. **Install APK** (allow unknown sources)
3. **Test all features**:
   - Landing page navigation
   - All buttons work
   - Screen transitions
   - Back button functionality

## 🎯 Success Checklist

- [ ] WSL Ubuntu installed
- [ ] Buildozer installed
- [ ] APK built successfully
- [ ] APK installed on device
- [ ] App runs without crashes
- [ ] All navigation works

## 📞 Next Steps

Once you have the APK working locally, you can:

1. **Share the APK** with others for testing
2. **Upload to Google Play Store** (requires developer account)
3. **Continue developing** new features
4. **Set up GitHub Actions** later when needed

Your Demonling game is now ready for mobile deployment! 🎮📱 