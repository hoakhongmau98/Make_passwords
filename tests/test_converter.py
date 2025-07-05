"""
Unit tests for the Vietnamese Password Converter
"""

import sys
import os
import pytest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.converter import PasswordGenerator, PasswordConverter
from src.core.decoder import PasswordDecoder, PasswordAnalyzer
from src.core.character_maps import CharacterMaps
from src.utils.validators import InputValidator, PasswordValidator


class TestCharacterMaps:
    """Test character mapping functionality."""
    
    def test_t9_mapping(self):
        """Test T9 keypad mapping."""
        assert CharacterMaps.get_t9_number('a') == '2'
        assert CharacterMaps.get_t9_number('d') == '3'
        assert CharacterMaps.get_t9_number('g') == '4'
        assert CharacterMaps.get_t9_number('j') == '5'
        assert CharacterMaps.get_t9_number('m') == '6'
        assert CharacterMaps.get_t9_number('p') == '7'
        assert CharacterMaps.get_t9_number('t') == '8'
        assert CharacterMaps.get_t9_number('w') == '9'
    
    def test_position_mapping(self):
        """Test T9 position mapping."""
        assert CharacterMaps.get_t9_position('a') == '1'
        assert CharacterMaps.get_t9_position('b') == '2'
        assert CharacterMaps.get_t9_position('c') == '3'
        assert CharacterMaps.get_t9_position('s') == '4'
    
    def test_special_char_mapping(self):
        """Test special character mapping."""
        assert CharacterMaps.get_special_char('0') == ')'
        assert CharacterMaps.get_special_char('1') == '!'
        assert CharacterMaps.get_special_char('2') == '@'
        assert CharacterMaps.get_special_char('3') == '#'
        assert CharacterMaps.get_special_char('4') == '$'
    
    def test_vietnamese_mapping(self):
        """Test Vietnamese character mapping."""
        assert CharacterMaps.get_base_char('á') == 'a'
        assert CharacterMaps.get_base_char('ă') == 'a'
        assert CharacterMaps.get_base_char('â') == 'a'
        assert CharacterMaps.get_base_char('đ') == 'd'
        assert CharacterMaps.get_base_char('ê') == 'e'
        assert CharacterMaps.get_base_char('ô') == 'o'
        assert CharacterMaps.get_base_char('ơ') == 'o'
        assert CharacterMaps.get_base_char('ư') == 'u'


class TestPasswordConverter:
    """Test password conversion functionality."""
    
    def test_init(self):
        """Test converter initialization."""
        converter = PasswordConverter("test")
        assert converter.input_text == "test"
        
        # Test empty input
        with pytest.raises(ValueError):
            PasswordConverter("")
    
    def test_convert_t9_with_diacritics(self):
        """Test T9 conversion with Vietnamese diacritics."""
        converter = PasswordConverter("Nguyễn")
        result, keys = converter.convert_t9_with_diacritics()
        assert result == "Nguyen"
        assert len(keys) > 0
    
    def test_convert_to_numbers(self):
        """Test conversion to T9 numbers."""
        converter = PasswordConverter("abc")
        result, diacritic_keys, position_keys = converter.convert_to_numbers()
        assert result == "222"
        assert position_keys == ['1', '2', '3']
    
    def test_convert_to_special_chars(self):
        """Test conversion to special characters."""
        converter = PasswordConverter("abc")
        result, diacritic_keys, position_keys = converter.convert_to_special_chars()
        assert result == "@@@"
        assert position_keys == ['1', '2', '3']


class TestPasswordGenerator:
    """Test password generation functionality."""
    
    def test_init(self):
        """Test generator initialization."""
        generator = PasswordGenerator("Test Name")
        assert generator.input_text == "Test Name"
    
    def test_split_text_space(self):
        """Test text splitting with space separator."""
        generator = PasswordGenerator("Nguyen Van An")
        components = generator._split_text()
        assert components == ["Nguyen", "Van", "An"]
        assert generator.separator_key == '0'
    
    def test_split_text_dot(self):
        """Test text splitting with dot separator."""
        generator = PasswordGenerator("Nguyen.Van.An")
        components = generator._split_text()
        assert components == ["Nguyen", "Van", "An"]
        assert generator.separator_key == '1'
    
    def test_generate_password_simple(self):
        """Test simple password generation."""
        generator = PasswordGenerator("Test")
        complete_password, password_only = generator.generate_password()
        assert password_only == "Test"
        assert complete_password.startswith("Test")
        assert len(complete_password) > len(password_only)
    
    def test_generate_password_multiple_words(self):
        """Test password generation with multiple words."""
        generator = PasswordGenerator("Hello World Test")
        complete_password, password_only = generator.generate_password()
        assert len(password_only) > 0
        assert len(complete_password) > len(password_only)


class TestPasswordDecoder:
    """Test password decoding functionality."""
    
    def test_init(self):
        """Test decoder initialization."""
        # Generate a password first
        generator = PasswordGenerator("Test")
        complete_password, _ = generator.generate_password()
        
        decoder = PasswordDecoder(complete_password)
        assert decoder.encoded_password == complete_password
        
        # Test empty input
        with pytest.raises(ValueError):
            PasswordDecoder("")
    
    def test_decode_simple(self):
        """Test decoding simple password."""
        # Generate and decode
        generator = PasswordGenerator("Test")
        complete_password, _ = generator.generate_password()
        
        decoder = PasswordDecoder(complete_password)
        decoded = decoder.decode()
        assert decoded.lower() == "test"
    
    def test_roundtrip_conversion(self):
        """Test complete roundtrip conversion."""
        original_text = "Hello World"
        
        # Generate password
        generator = PasswordGenerator(original_text)
        complete_password, _ = generator.generate_password()
        
        # Decode password
        decoder = PasswordDecoder(complete_password)
        decoded_text = decoder.decode()
        
        # Compare (case-insensitive)
        assert decoded_text.lower() == original_text.lower()


class TestPasswordAnalyzer:
    """Test password analysis functionality."""
    
    def test_is_valid_password(self):
        """Test password validation."""
        # Generate a valid password
        generator = PasswordGenerator("Test")
        complete_password, _ = generator.generate_password()
        
        assert PasswordAnalyzer.is_valid_password(complete_password)
        assert not PasswordAnalyzer.is_valid_password("invalid")
        assert not PasswordAnalyzer.is_valid_password("")
    
    def test_get_password_info(self):
        """Test password information extraction."""
        generator = PasswordGenerator("Test")
        complete_password, _ = generator.generate_password()
        
        info = PasswordAnalyzer.get_password_info(complete_password)
        assert info['valid']
        assert info['password_length'] > 0
        assert info['separator_type'] in ['space', 'dot']


class TestInputValidator:
    """Test input validation functionality."""
    
    def test_validate_input_text_valid(self):
        """Test valid input text validation."""
        valid_texts = [
            "Nguyen Van An",
            "Test123",
            "Hello World",
            "Nguyễn Văn An",
            "Test.Name.Here"
        ]
        
        for text in valid_texts:
            is_valid, error = InputValidator.validate_input_text(text)
            assert is_valid, f"'{text}' should be valid: {error}"
    
    def test_validate_input_text_invalid(self):
        """Test invalid input text validation."""
        invalid_texts = [
            "",
            "   ",
            "a" * 101,  # Too long
            "Hello@World#Test",  # Invalid characters
        ]
        
        for text in invalid_texts:
            is_valid, error = InputValidator.validate_input_text(text)
            assert not is_valid, f"'{text}' should be invalid"
    
    def test_validate_encoded_password(self):
        """Test encoded password validation."""
        # Generate valid password
        generator = PasswordGenerator("Test")
        complete_password, _ = generator.generate_password()
        
        is_valid, error = InputValidator.validate_encoded_password(complete_password)
        assert is_valid, f"Generated password should be valid: {error}"
        
        # Test invalid passwords
        invalid_passwords = [
            "",
            "abc",
            "test123",
            "1234567890abcd",  # Missing proper format
        ]
        
        for password in invalid_passwords:
            is_valid, error = InputValidator.validate_encoded_password(password)
            assert not is_valid, f"'{password}' should be invalid"
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        assert InputValidator.sanitize_input("  Hello World  ") == "Hello World"
        assert InputValidator.sanitize_input("Hello    World") == "Hello World"
        assert InputValidator.sanitize_input("Hello@#$World") == "HelloWorld"
    
    def test_get_text_info(self):
        """Test text information extraction."""
        info = InputValidator.get_text_info("Nguyễn Văn An")
        assert info['length'] > 0
        assert info['word_count'] == 3
        assert info['has_vietnamese']
        assert info['separator_type'] == 'space'


class TestPasswordValidator:
    """Test password strength validation."""
    
    def test_check_password_strength_empty(self):
        """Test password strength check with empty password."""
        strength = PasswordValidator.check_password_strength("")
        assert strength['strength'] == 'None'
        assert strength['score'] == 0
    
    def test_check_password_strength_weak(self):
        """Test password strength check with weak password."""
        strength = PasswordValidator.check_password_strength("abc")
        assert strength['strength'] in ['Very Weak', 'Weak']
        assert strength['score'] < 4
    
    def test_check_password_strength_strong(self):
        """Test password strength check with strong password."""
        strength = PasswordValidator.check_password_strength("MyStrongPassword123!")
        assert strength['strength'] in ['Medium', 'Strong']
        assert strength['score'] >= 4


if __name__ == "__main__":
    pytest.main([__file__])