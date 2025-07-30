# GitHub Actions Guide for Demonling

This guide explains how to use the automated GitHub Actions workflows to build and release your Demonling APK.

## 🚀 Available Workflows

### 1. **Test Workflow** (`.github/workflows/test.yml`)
- **Triggers**: Push to main/master, Pull Requests, Manual dispatch
- **Purpose**: Tests the application structure and dependencies
- **What it does**:
  - Installs Python dependencies
  - Runs installation tests
  - Validates Kivy imports
  - Checks app structure
  - Validates buildozer.spec configuration

### 2. **Build Workflow** (`.github/workflows/build.yml`)
- **Triggers**: Push to main/master, Pull Requests, Manual dispatch
- **Purpose**: Builds Android APK and uploads as artifact
- **What it does**:
  - Sets up Python environment
  - Installs dependencies
  - Tests app imports
  - Builds Android APK using Buildozer
  - Uploads APK as downloadable artifact

### 3. **Release Workflow** (`.github/workflows/release.yml`)
- **Triggers**: Push tags starting with 'v' (e.g., v1.0.0)
- **Purpose**: Creates GitHub releases with APK files
- **What it does**:
  - Builds APK automatically
  - Creates GitHub release
  - Attaches APK files to release
  - Generates release notes

## 📋 How to Use

### Testing Your App
1. **Automatic Testing**: Every push to main/master triggers tests
2. **Manual Testing**: Go to Actions tab → Test Application → Run workflow
3. **Check Results**: View test results in the Actions tab

### Building APK
1. **Automatic Build**: Every push to main/master builds APK
2. **Manual Build**: Go to Actions tab → Build Android APK → Run workflow
3. **Download APK**: After build completes, download from Artifacts section

### Creating Releases
1. **Create a Tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
2. **Automatic Release**: GitHub will create a release with APK attached
3. **Download Release**: Users can download APK from the Releases page

## 🔧 Troubleshooting

### Common Issues

#### Build Fails
- **Check logs**: Go to Actions tab and view detailed error logs
- **Dependencies**: Ensure all requirements are in `requirements.txt`
- **Buildozer config**: Verify `buildozer.spec` is properly configured

#### APK Not Found
- **Check paths**: Ensure APK is built in expected location
- **Buildozer output**: Check if buildozer completed successfully
- **File permissions**: Ensure GitHub Actions can access build directories

#### Release Not Created
- **Tag format**: Ensure tag starts with 'v' (e.g., v1.0.0)
- **Permissions**: Check repository permissions for GitHub Actions
- **Token**: Ensure GITHUB_TOKEN is available

### Debugging Steps
1. **Check workflow logs** in Actions tab
2. **Test locally** using `python build_mobile.py`
3. **Verify dependencies** in `requirements.txt`
4. **Check buildozer.spec** configuration
5. **Test app imports** locally

## 📱 APK Distribution

### From GitHub Actions
1. **Build Artifacts**: Download APK from Actions → Artifacts
2. **Releases**: Download APK from Releases page
3. **Direct Links**: Share release URLs for easy downloads

### Installation Instructions
1. **Enable Unknown Sources**: On Android device, go to Settings → Security → Unknown Sources
2. **Download APK**: Get APK from GitHub release or artifacts
3. **Install**: Open APK file and follow installation prompts
4. **Launch**: Find Demonling in your app drawer

## 🔄 Workflow Customization

### Adding New Dependencies
1. **Update requirements.txt**:
   ```
   kivy
   pillow
   requests
   your_new_dependency
   ```
2. **Update buildozer.spec**:
   ```
   requirements = python3,kivy,pillow,requests,your_new_dependency
   ```
3. **Test locally** before pushing

### Modifying Build Process
1. **Edit workflow files** in `.github/workflows/`
2. **Test changes** with manual workflow dispatch
3. **Check logs** for any issues
4. **Commit and push** when working

### Adding New Platforms
1. **Create new workflow** for target platform
2. **Configure build tools** (e.g., Xcode for iOS)
3. **Test thoroughly** before enabling
4. **Update documentation** with new instructions

## 📊 Monitoring

### Workflow Status
- **Green checkmark**: Success
- **Red X**: Failure
- **Yellow dot**: In progress
- **Gray dot**: Skipped

### Performance Metrics
- **Build time**: Typically 10-15 minutes for APK
- **Artifact size**: Usually 20-50MB for APK
- **Success rate**: Monitor for recurring failures

## 🎯 Best Practices

1. **Test Locally First**: Always test changes locally before pushing
2. **Use Semantic Versioning**: Tag releases with v1.0.0 format
3. **Monitor Builds**: Check Actions tab regularly for issues
4. **Keep Dependencies Updated**: Regularly update requirements.txt
5. **Document Changes**: Update README.md with new features
6. **Backup APKs**: Download and store important APK versions

## 🆘 Getting Help

If you encounter issues:

1. **Check existing issues** in GitHub repository
2. **Review workflow logs** for specific error messages
3. **Test locally** using `python build_mobile.py`
4. **Create new issue** with detailed error information
5. **Check Kivy/Buildozer documentation** for platform-specific issues

---

**Happy Building! 🚀📱** 