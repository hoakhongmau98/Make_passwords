# Vietnamese Password Converter

A Python package for converting Vietnamese text to passwords and vice versa using T9 keypad style conversion with full Vietnamese diacritics support.

## 🚀 Features

- ✅ **Vietnamese Diacritics Support**: Full support for Vietnamese accents (á, à, ả, ã, ạ, ă, ắ, ằ, ẳ, ẵ, ặ, â, ấ, ầ, ẩ, ẫ, ậ, etc.)
- ✅ **T9 Keypad Conversion**: Uses mobile phone T9 keypad mapping for character conversion
- ✅ **Bidirectional Conversion**: Convert text to password and decode password back to text
- ✅ **Embedded Keys**: Generated passwords include embedded decoding keys
- ✅ **CLI Interface**: Easy-to-use command-line interface
- ✅ **Interactive Mode**: Interactive mode for multiple operations
- ✅ **Password Analysis**: Analyze password strength and structure
- ✅ **Input Validation**: Comprehensive input validation and error handling
- ✅ **No External Dependencies**: Pure Python implementation

## 📦 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/example/vietnamese-password-converter.git
cd vietnamese-password-converter

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e .[dev]
```

### Using pip (when published)

```bash
pip install vietnamese-password-converter
```

## 🎯 Quick Start

### Command Line Usage

```bash
# Generate password from Vietnamese text
python -m src.cli.main -g "Nguyễn Văn An"

# Decode password back to text
python -m src.cli.main -d "Nguyen*$#*286640332132321htGPDnd715"

# Interactive mode
python -m src.cli.main -i

# Analyze password strength
python -m src.cli.main -a "MyPassword123"

# Validate input text
python -m src.cli.main -v "Trần Thị Bảo"
```

### Python API Usage

```python
from src.core.converter import PasswordGenerator
from src.core.decoder import PasswordDecoder

# Generate password
generator = PasswordGenerator("Nguyễn Văn An")
complete_password, password_only = generator.generate_password()
print(f"Password: {password_only}")
print(f"Complete: {complete_password}")

# Decode password
decoder = PasswordDecoder(complete_password)
original_text = decoder.decode()
print(f"Original: {original_text}")
```

## 🛠️ How It Works

The Vietnamese Password Converter uses a sophisticated algorithm that:

1. **Splits text** into components (words separated by spaces or dots)
2. **Applies different conversion methods** in a rotating pattern:
   - Position 0, 3, 6, ...: T9 conversion (preserves text with diacritic encoding)
   - Position 1, 4, 7, ...: Special character conversion (numbers → symbols)
   - Position 2, 5, 8, ...: Number conversion (characters → T9 keypad numbers)
3. **Embeds decoding keys** in the final password for reconstruction
4. **Preserves Vietnamese diacritics** through ASCII encoding

### Example Conversion

```
Input: "Nguyễn Viết Cường"
       ↓
Components: ["Nguyễn", "Viết", "Cường"]
       ↓
Conversion:
- "Nguyễn" (pos 0) → T9 with diacritics → "Nguyen"
- "Viết" (pos 1) → Special chars → "*$#*"
- "Cường" (pos 2) → Numbers → "28664"
       ↓
Password: "Nguyen*$#*28664"
Complete: "Nguyen*$#*286640332132321htGPDnd715"
```

## 📚 API Reference

### Core Classes

#### `PasswordGenerator`
```python
class PasswordGenerator:
    def __init__(self, input_text: str)
    def generate_password(self) -> Tuple[str, str]
```

#### `PasswordDecoder`
```python
class PasswordDecoder:
    def __init__(self, encoded_password: str)
    def decode(self) -> str
```

#### `InputValidator`
```python
class InputValidator:
    @classmethod
    def validate_input_text(cls, text: str) -> Tuple[bool, str]
    @classmethod
    def validate_encoded_password(cls, password: str) -> Tuple[bool, str]
```

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `-g, --generate` | Generate password from text | `-g "Nguyễn Văn An"` |
| `-d, --decode` | Decode password to text | `-d "Nguyen*$#*..."` |
| `-i, --interactive` | Interactive mode | `-i` |
| `-a, --analyze` | Analyze password | `-a "MyPassword123"` |
| `-v, --validate` | Validate input text | `-v "Trần Thị Bảo"` |
| `--info` | Show text information | `--info "Sample text"` |

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e .[test]

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## 📖 Examples

### Basic Usage

```python
from src.core.converter import PasswordGenerator

# Simple text
generator = PasswordGenerator("Tran Van Nam")
password, complete = generator.generate_password()
# Output: password="Tran*$#*626", complete="Tran*$#*62603315215"

# Vietnamese text with diacritics
generator = PasswordGenerator("Nguyễn Thị Lan")
password, complete = generator.generate_password()
# Output: password="Nguyen*$#*526", complete="Nguyen*$#*52603211111715"
```

### Advanced Usage

```python
from src.core.converter import PasswordGenerator
from src.core.decoder import PasswordDecoder, PasswordAnalyzer
from src.utils.validators import InputValidator, PasswordValidator

# Validate input before conversion
text = "Lê Văn Minh"
is_valid, error = InputValidator.validate_input_text(text)
if is_valid:
    generator = PasswordGenerator(text)
    complete_password, password = generator.generate_password()
    
    # Analyze password strength
    strength = PasswordValidator.check_password_strength(password)
    print(f"Strength: {strength['strength']}")
    
    # Decode back to verify
    decoder = PasswordDecoder(complete_password)
    original = decoder.decode()
    print(f"Original: {original}")
```

## 🔧 Configuration

The converter supports various configuration options:

- **Maximum text length**: 100 characters (configurable)
- **Supported separators**: Space (` `) and dot (`.`)
- **Character encoding**: UTF-8 with Vietnamese diacritics
- **T9 keypad mapping**: Standard mobile phone layout

## 🚨 Security Considerations

⚠️ **Important Security Notes:**

1. **Not for sensitive passwords**: This tool is designed for educational and demonstration purposes
2. **Predictable patterns**: The algorithm uses predictable patterns based on input text
3. **No encryption**: The conversion is encoding, not encryption
4. **Visible patterns**: Generated passwords may contain recognizable patterns

For production password generation, use cryptographically secure random generators.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/example/vietnamese-password-converter.git
cd vietnamese-password-converter

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/
```

## 📝 Changelog

### Version 1.0.0
- Initial release
- Core password generation and decoding functionality
- CLI interface with interactive mode
- Vietnamese diacritics support
- Input validation and error handling
- Password strength analysis
- Comprehensive documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Vietnamese language support inspired by the need for culturally-aware password tools
- T9 keypad conversion based on traditional mobile phone input methods
- Community feedback and suggestions for feature improvements

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/example/vietnamese-password-converter/wiki)
2. Search [existing issues](https://github.com/example/vietnamese-password-converter/issues)
3. Create a [new issue](https://github.com/example/vietnamese-password-converter/issues/new)

---

Made with ❤️ for the Vietnamese developer community
