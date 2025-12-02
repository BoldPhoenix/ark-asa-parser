# Quick Publishing Guide

## You Already Have Everything Set Up!

Since you already have your `.pypirc` configured with your PyPI token, publishing is simple.

## Steps to Publish

### 1. Navigate to the package directory

```powershell
cd C:\Users\Administrator\Documents\Github\ark-asa-parser
```

### 2. Build the package

```powershell
# Remove old builds if they exist
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build
python -m build
```

### 3. Upload to PyPI

```powershell
# Upload using your existing .pypirc configuration
twine upload dist/*
```

That's it! Same process as before.

## What About GitHub?

The GitHub Actions workflow (`.github/workflows/publish.yml`) is **optional**. You can:

**Option 1: Ignore it** - Just manually publish like above whenever you want
**Option 2: Delete it** - Remove `.github/workflows/publish.yml` if you don't want automation
**Option 3: Set it up later** - If you want auto-publishing on GitHub releases

For now, just ignore the GitHub Actions stuff and publish manually like you did with version 0.1.0!

## Quick Commands

```powershell
# Navigate
cd C:\Users\Administrator\Documents\Github\ark-asa-parser

# Clean, build, and publish
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
python -m build
twine upload dist/*
```

Done! ✅
