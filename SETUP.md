# ark-asa-parser Repository Setup

Your standalone ark-asa-parser library is ready! Here's how to set it up on GitHub and publish to PyPI.

## Repository Structure

```
ark-asa-parser/
├── ark_asa_parser/          # Main package
│   ├── __init__.py
│   ├── binary_reader.py
│   ├── save_reader.py
│   └── simple_property_reader.py
├── examples/                # Example scripts
│   ├── basic_usage.py
│   ├── scan_cluster.py
│   └── read_individual_files.py
├── .github/
│   └── workflows/
│       └── publish.yml      # PyPI auto-publish
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
├── PUBLISHING.md
└── README.md
```

## Next Steps

### 1. Create GitHub Repository

```bash
cd ark-asa-parser
git init
git add .
git commit -m "Initial commit - ark-asa-parser library"
git branch -M main
git remote add origin https://github.com/BoldPhoenix/ark-asa-parser.git
git push -u origin main
```

### 2. Configure GitHub Secrets

Go to repository Settings → Secrets and variables → Actions:

1. Add `PYPI_API_TOKEN` with your PyPI API token
2. (Optional) Add `TEST_PYPI_API_TOKEN` for testing

### 3. Initial PyPI Release

Option A - Manual:
```bash
pip install build twine
python -m build
twine upload dist/*
```

Option B - GitHub Release:
1. Go to Releases on GitHub
2. Create new release with tag `v0.1.1`
3. GitHub Actions will auto-publish

### 4. Update Your Discord Bot

In your ArkDiscordBot repository, update the dependency:

**pyproject.toml** or **requirements.txt**:
```
ark-asa-parser>=0.1.1
```

Then update imports:
```python
# Old
from bot.ark_data_parser import ArkSaveReader, scan_all_servers

# New
from ark_asa_parser import ArkSaveReader, scan_all_servers
```

### 5. Test Installation

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from PyPI
pip install ark-asa-parser

# Test import
python -c "from ark_asa_parser import ArkSaveReader; print('Success!')"
```

## Features Included

✅ Player name extraction
✅ Character name extraction
✅ Tribe name extraction
✅ Tribe member lists
✅ Multi-server scanning
✅ SQLite database reading
✅ Comprehensive documentation
✅ Example scripts
✅ MIT License
✅ GitHub Actions CI/CD

## What's Different from Discord Bot Version

**Removed:**
- Discord-specific code
- Bot configuration
- Database integration for bot
- Guild-specific features

**Kept:**
- All save file parsing
- Property extraction
- Data models
- Core functionality

## Documentation

- **README.md** - User-facing documentation with examples
- **CONTRIBUTING.md** - Guidelines for contributors
- **PUBLISHING.md** - How to publish new versions
- **CHANGELOG.md** - Version history
- **examples/** - Working code examples

## Future Development

The library is designed to be extended. Priority areas:

1. **More property types** (Float, Struct, Object)
2. **Dino data extraction**
3. **Building data**
4. **Player stats** (health, stamina, etc.)
5. **Performance optimizations**

Contributors welcome! See CONTRIBUTING.md

## Support

- **Issues**: https://github.com/BoldPhoenix/ark-asa-parser/issues
- **PyPI**: https://pypi.org/project/ark-asa-parser/
- **License**: MIT

## Notes

- Keep the library focused on save file parsing
- Avoid adding Discord/bot-specific features
- Maintain backwards compatibility
- Follow semantic versioning
- Document all public APIs

Ready to share with the ARK community! 🦖
