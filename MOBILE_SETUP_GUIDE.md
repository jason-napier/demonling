# 📱 Demonling Mobile Setup Guide

This guide will help you set up your Demonling game for mobile deployment using your GitHub repository at: **https://github.com/jason-napier/demonling**

## 🎯 What We've Accomplished

✅ **Complete Mobile Build Setup**
- Android APK building with Buildozer
- GitHub Actions for automated builds
- Automated build script (`build_mobile.py`)
- Comprehensive documentation

✅ **GitHub Repository Setup**
- Repository connected: https://github.com/jason-napier/demonling
- All files committed and pushed
- GitHub Actions workflow configured

## 🚀 Next Steps for Mobile Deployment

### 1. **GitHub Actions (Automated Builds)**

Your repository now has automated builds! Every time you push changes to the `main` branch, GitHub will automatically:

- Build an Android APK
- Make it available for download
- Show build status in your repository

**To trigger your first automated build:**
```bash
# Make any small change to trigger a build
echo "# Updated for mobile build" >> README.md
git add README.md
git commit -m "Trigger first mobile build"
git push origin main
```

### 2. **Local Android Build (Windows)**

Since you're on Windows, you have two options for building Android APKs:

#### Option A: Use WSL (Windows Subsystem for Linux) - Recommended
```bash
# Install WSL and Ubuntu
wsl --install

# In WSL Ubuntu terminal:
sudo apt update
sudo apt install python3-pip build-essential git
pip3 install buildozer
cd /mnt/c/Users/nside/Documents/_Programing/Python\ Projects/Demonling
buildozer android debug
```

#### Option B: Use GitHub Actions (Easiest)
- Push your code to GitHub
- Go to Actions tab in your repository
- Download the generated APK

### 3. **iOS Build (Mac Required)**

For iOS builds, you'll need:
- A Mac computer
- Xcode installed
- Apple Developer account (for App Store distribution)

```bash
# On Mac:
pip install kivy-ios
toolchain build kivy
toolchain create Demonling .
toolchain run Demonling ios
```

## 📱 Testing Your Mobile App

### Android Testing
1. **Download APK** from GitHub Actions or build locally
2. **Enable "Install from unknown sources"** on your Android device
3. **Transfer APK** to your device
4. **Install and test** the app

### iOS Testing
1. **Build on Mac** using kivy-ios
2. **Open in Xcode**
3. **Deploy to simulator or device**

## 🔧 Customization Options

### App Icon and Splash Screen
Add these files to your project:
```
assets/
├── icon.png          # 512x512 app icon
├── icon-72.png       # 72x72 icon
├── icon-96.png       # 96x96 icon
└── splash.png        # Splash screen image
```

Then update `buildozer.spec`:
```ini
# Uncomment and set these lines:
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png
```

### App Permissions
Edit `buildozer.spec` to add/remove permissions:
```ini
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

## 📊 Monitoring Your Builds

### GitHub Actions Dashboard
- Go to: https://github.com/jason-napier/demonling/actions
- View build history and status
- Download APK artifacts

### Build Logs
If builds fail, check the logs for:
- Missing dependencies
- Configuration errors
- System requirements

## 🎮 Publishing Your App

### Google Play Store
1. **Create developer account** at https://play.google.com/console
2. **Build release APK**: `buildozer android release`
3. **Upload to Play Console**
4. **Submit for review**

### Apple App Store
1. **Create developer account** at https://developer.apple.com
2. **Build iOS app** using kivy-ios
3. **Upload to App Store Connect**
4. **Submit for review**

## 🔄 Continuous Development

### Workflow for Updates
```bash
# 1. Make your changes
# 2. Test locally
python main.py

# 3. Commit and push
git add .
git commit -m "Add new feature"
git push origin main

# 4. GitHub Actions automatically builds new APK
# 5. Download and test the new APK
```

### Version Management
```bash
# Tag releases
git tag v1.0.0
git push origin v1.0.0

# Create GitHub release
# Go to: https://github.com/jason-napier/demonling/releases
```

## 🆘 Troubleshooting

### Common Issues

1. **Buildozer fails on Windows**
   - Use WSL or GitHub Actions instead
   - Buildozer works best on Linux

2. **APK won't install**
   - Check Android version compatibility
   - Verify "Install from unknown sources" is enabled
   - Check APK file integrity

3. **GitHub Actions build fails**
   - Check the Actions tab for error logs
   - Verify all files are committed
   - Check buildozer.spec configuration

### Getting Help
- **GitHub Issues**: Create an issue in your repository
- **Kivy Documentation**: https://kivy.org/doc/stable/
- **Buildozer Documentation**: https://buildozer.readthedocs.io/

## 🎉 Success Checklist

- [ ] Repository connected to GitHub
- [ ] GitHub Actions workflow working
- [ ] First automated build completed
- [ ] APK downloaded and tested
- [ ] App icon and splash screen added (optional)
- [ ] App permissions configured
- [ ] Ready for app store submission

## 📞 Support

Your Demonling mobile game is now ready for deployment! The automated build system will handle most of the complexity, so you can focus on developing your game features.

**Repository**: https://github.com/jason-napier/demonling  
**Actions**: https://github.com/jason-napier/demonling/actions

Happy mobile development! 🎮📱 