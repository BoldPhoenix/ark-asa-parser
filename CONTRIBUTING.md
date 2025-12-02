# Contributing to ark-asa-parser

Thank you for your interest in contributing to ark-asa-parser! This library helps the ARK: Survival Ascended community build better tools for server management and player tracking.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Include Python version, OS, and ARK save file version
- Provide sample code that reproduces the issue
- Include relevant error messages

### Suggesting Features

- Open a GitHub issue with the "enhancement" label
- Describe the use case and expected behavior
- Include example code showing how you'd like to use the feature

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes** with real ARK save files
5. **Commit with clear messages**: `git commit -m "Add support for X property type"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ark-asa-parser.git
cd ark-asa-parser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to public functions and classes
- Keep functions focused and modular

## Testing

When contributing, please test with:
- Multiple ARK save files
- Different server configurations
- Edge cases (empty tribes, solo players, etc.)

## Areas for Contribution

### High Priority
- **Float property parser** - For stats like experience, health, stamina
- **Struct property parser** - For nested data structures
- **Dino data extraction** - Parse tamed creature data
- **Building data extraction** - Parse structure information

### Medium Priority
- **Level calculation** - Convert experience to level
- **Inventory parsing** - Extract player/dino inventories
- **Additional examples** - More use cases and tutorials
- **Performance optimization** - Faster file scanning

### Documentation
- More detailed API documentation
- Additional examples
- Tutorial for beginners
- Binary format documentation

## Property Types to Implement

ARK uses various UE5 property types that need parsers:

- ✅ StrProperty (String)
- ✅ IntProperty (Integer)
- ✅ UInt32Property (Unsigned Integer)
- ✅ ArrayProperty (Arrays)
- ⚠️ FloatProperty (Floating point)
- ⚠️ DoubleProperty (Double precision)
- ⚠️ StructProperty (Nested structures)
- ⚠️ ObjectProperty (Object references)
- ⚠️ ByteProperty (Bytes)
- ⚠️ BoolProperty (Booleans)

## Binary Format Notes

ARK ASA uses UE5 property serialization. Each property has:
- Name (length-prefixed string)
- Type (length-prefixed string)
- Size/metadata (varies by type)
- Value (format depends on type)

Different property types have different layouts. Contributing parsers for new types greatly expands the library's capabilities!

## Community

- Be respectful and constructive
- Help others in discussions
- Share your use cases and projects
- Report bugs you encounter

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open a GitHub Discussion
- Check existing issues and PRs
- Review the examples directory

Thank you for helping make ark-asa-parser better for the ARK community!
