# Publishing to PyPI

This document contains instructions for publishing new versions of ark-asa-parser to PyPI.

## Prerequisites

1. PyPI account with API token
2. GitHub repository set up with secrets
3. Version updated in `pyproject.toml` and `ark_asa_parser/__init__.py`

## Manual Publishing

### 1. Update Version

Edit `pyproject.toml`:
```toml
version = "0.1.1"  # Update this
```

Edit `ark_asa_parser/__init__.py`:
```python
__version__ = "0.1.1"  # Update this
```

### 2. Update CHANGELOG.md

Add new version entry with changes.

### 3. Build Package

```bash
# Install build tools
pip install build twine

# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build
python -m build
```

### 4. Test Build

```bash
# Check package
twine check dist/*

# Test install locally
pip install dist/ark_asa_parser-0.1.1-py3-none-any.whl
```

### 5. Upload to Test PyPI (Optional)

```bash
# Upload to test
twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ ark-asa-parser
```

### 6. Upload to PyPI

```bash
twine upload dist/*
```

## Automated Publishing (GitHub Actions)

### Setup

1. Get PyPI API token from https://pypi.org/manage/account/token/
2. Add as GitHub secret: `PYPI_API_TOKEN`
3. Optionally add Test PyPI token as `TEST_PYPI_API_TOKEN`

### Publishing via Release

1. Update version in code
2. Commit and push changes
3. Create GitHub release with tag (e.g., `v0.1.1`)
4. Workflow automatically publishes to PyPI

### Manual Workflow Trigger

1. Go to Actions tab on GitHub
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Choose branch and whether to use Test PyPI

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking API changes
- **MINOR** (0.1.0): New features, backwards compatible
- **PATCH** (0.0.1): Bug fixes, backwards compatible

## Pre-Release Checklist

- [ ] Version updated in `pyproject.toml`
- [ ] Version updated in `ark_asa_parser/__init__.py`
- [ ] CHANGELOG.md updated
- [ ] All tests passing
- [ ] README.md reflects new features
- [ ] Examples updated if needed
- [ ] Documentation reviewed
- [ ] Git tag created

## Post-Release

- [ ] Verify package on PyPI: https://pypi.org/project/ark-asa-parser/
- [ ] Test installation: `pip install ark-asa-parser`
- [ ] Announce in discussions/community channels
- [ ] Update related documentation

## Troubleshooting

### Build fails
- Check `pyproject.toml` syntax
- Ensure all files are included in MANIFEST.in
- Verify Python version compatibility

### Upload fails
- Check API token is valid
- Ensure version doesn't already exist on PyPI
- Verify package name isn't taken

### Import errors after install
- Check `__init__.py` imports
- Verify package structure
- Test with fresh virtual environment
