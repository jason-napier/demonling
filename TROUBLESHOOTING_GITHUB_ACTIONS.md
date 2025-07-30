# GitHub Actions Troubleshooting Guide

## 🚨 Current Issues

### Problem: "Test Application" did not start and "Build Android APK" crashed immediately

## 🔧 Solutions

### 1. **Use the Simple Build Workflow**

I've created a new, more reliable workflow: `simple-build.yml`

**To use it:**
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Look for "Simple Build and Test" workflow
4. Click "Run workflow" → "Run workflow"

This workflow:
- ✅ Separates testing and building into different jobs
- ✅ Uses proven Docker approach
- ✅ Has better error handling
- ✅ Tests app structure before building

### 2. **Check Workflow Logs**

If workflows still fail:

1. **Go to Actions tab** in your GitHub repository
2. **Click on the failed workflow**
3. **Click on the failed job** (red X)
4. **Expand the failed step** to see detailed error messages

### 3. **Common Issues and Fixes**

#### Issue: "No module named 'kivy'"
**Fix:** The workflow is trying to import Kivy before it's installed
**Solution:** The new workflow installs dependencies first

#### Issue: "buildozer command not found"
**Fix:** Buildozer isn't available in the GitHub Actions environment
**Solution:** Using Docker image `kivy/buildozer:latest`

#### Issue: "Permission denied"
**Fix:** File permission issues
**Solution:** The new workflow uses proper Docker volume mounting

#### Issue: "APK not found"
**Fix:** Build succeeded but APK wasn't created in expected location
**Solution:** The new workflow searches multiple locations

### 4. **Manual Testing Steps**

Before pushing to GitHub, test locally:

```bash
# Test app imports
python -c "import kivy; print('Kivy OK')"
python -c "from main import DemonlingApp; print('App OK')"

# Test buildozer
buildozer --version

# Test basic build (optional)
buildozer android debug
```

### 5. **Alternative: Use Local Build**

If GitHub Actions continues to fail, use local building:

```bash
# Run the mobile build script
python build_mobile.py

# Or build manually
buildozer android debug
```

### 6. **Workflow Comparison**

| Workflow | Status | Reliability | Speed |
|----------|--------|-------------|-------|
| `test.yml` | ❌ Failing | Low | Fast |
| `build.yml` | ❌ Failing | Low | Medium |
| `simple-build.yml` | ✅ New | High | Medium |
| `release.yml` | ⚠️ Needs testing | Medium | Slow |

## 🎯 Recommended Action Plan

### Step 1: Test the Simple Workflow
1. Push your current changes
2. Go to Actions tab
3. Run "Simple Build and Test" workflow
4. Check if it succeeds

### Step 2: If Simple Workflow Works
1. Delete the old failing workflows
2. Use the simple workflow for all builds
3. Create releases manually or with tags

### Step 3: If Simple Workflow Fails
1. Check the detailed error logs
2. Test locally first
3. Consider using local builds only

## 📋 Debugging Commands

### Check GitHub Actions Environment
```bash
# In workflow, add this step:
- name: Debug Environment
  run: |
    echo "Python version:"
    python --version
    echo "Current directory:"
    pwd
    echo "Files in directory:"
    ls -la
    echo "Python packages:"
    pip list
```

### Check Buildozer Configuration
```bash
# In workflow, add this step:
- name: Check Buildozer Config
  run: |
    echo "Buildozer spec contents:"
    cat buildozer.spec
    echo "Requirements:"
    cat requirements.txt
```

## 🆘 Getting Help

If you continue to have issues:

1. **Share the exact error message** from the workflow logs
2. **Test locally first** using `python build_mobile.py`
3. **Check if the issue is with your code** or the GitHub Actions setup
4. **Consider using local builds** for now and focus on game development

## 🎮 Focus on Game Development

Remember: The most important thing is that your game works! 

- ✅ Your local setup is working perfectly
- ✅ Your app runs and has a good structure
- ✅ You can build locally with `python build_mobile.py`

The GitHub Actions are just for automation - you can always build and distribute APKs manually while we fix the automation issues.

---

**Priority: Get your game working first, then automate the builds! 🚀** 