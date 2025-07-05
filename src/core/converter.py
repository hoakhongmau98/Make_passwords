"""
Vietnamese Password Converter

This module provides functionality to convert Vietnamese text into passwords
using T9 keypad style conversion and special character substitutions.
"""

from typing import List, Tuple, Optional
from .character_maps import CharacterMaps


class PasswordConverter:
    """
    Converts Vietnamese text strings into passwords using a multi-step process:
    1. T9 conversion (preserves original text with diacritic encoding)
    2. Number conversion (converts characters to T9 keypad numbers)
    3. Special character conversion (converts numbers to special characters)
    """

    def __init__(self, input_text: str):
        """
        Initialize the converter with input text.
        
        Args:
            input_text: The Vietnamese text to convert to a password
            
        Raises:
            ValueError: If input_text is empty or None
        """
        if not input_text or not input_text.strip():
            raise ValueError("Input text cannot be empty")
        
        self.input_text = input_text.strip()
        self.char_maps = CharacterMaps()
        
    def convert_t9_with_diacritics(self) -> Tuple[str, List[str]]:
        """
        Convert text to T9 representation while preserving Vietnamese diacritics.
        
        This method converts Vietnamese characters to their base forms and stores
        the diacritic information for later reconstruction.
        
        Returns:
            Tuple containing:
            - converted_text: Text with Vietnamese diacritics converted to base characters
            - diacritic_keys: List of ASCII codes for diacritic reconstruction
        """
        converted_chars = []
        diacritic_keys = []
        
        for char in self.input_text:
            if char in self.char_maps.VIETNAMESE_TO_BASE:
                # Convert Vietnamese character to base character
                base_char = self.char_maps.get_base_char(char)
                converted_chars.append(base_char)
                
                # Store diacritic information for reconstruction
                ascii_code = self.char_maps.get_ascii_code(char)
                diacritic_keys.append(chr(int(ascii_code)))
            else:
                # Keep non-Vietnamese characters as-is
                converted_chars.append(char)
        
        return ''.join(converted_chars), diacritic_keys
    
    def convert_to_numbers(self) -> Tuple[str, List[str], List[str]]:
        """
        Convert text to T9 keypad numbers with position information.
        
        Returns:
            Tuple containing:
            - number_text: Text converted to T9 keypad numbers
            - diacritic_keys: List of diacritic information
            - position_keys: List of character positions on T9 keypad
        """
        converted_chars = []
        diacritic_keys = []
        position_keys = []
        
        for char in self.input_text:
            if char.isdigit():
                # Keep digits as-is
                converted_chars.append(char)
            else:
                # Convert character to T9 number
                if char in self.char_maps.VIETNAMESE_TO_BASE:
                    base_char = self.char_maps.get_base_char(char)
                    t9_number = self.char_maps.get_t9_number(base_char)
                    converted_chars.append(t9_number)
                    
                    # Store diacritic and position information
                    ascii_code = self.char_maps.get_ascii_code(char)
                    diacritic_keys.append(chr(int(ascii_code)))
                    position_keys.append(self.char_maps.get_t9_position(base_char))
                else:
                    t9_number = self.char_maps.get_t9_number(char)
                    converted_chars.append(t9_number)
                    position_keys.append(self.char_maps.get_t9_position(char))
        
        return ''.join(converted_chars), diacritic_keys, position_keys
    
    def convert_to_special_chars(self) -> Tuple[str, List[str], List[str]]:
        """
        Convert text to special characters (numbers become symbols).
        
        Returns:
            Tuple containing:
            - special_text: Text with numbers converted to special characters
            - diacritic_keys: List of diacritic information
            - position_keys: List of character positions on T9 keypad
        """
        converted_chars = []
        diacritic_keys = []
        position_keys = []
        
        for char in self.input_text:
            if char.isdigit():
                # Convert digit to special character
                special_char = self.char_maps.get_special_char(char)
                converted_chars.append(special_char)
            else:
                # Convert character through T9 then to special character
                if char in self.char_maps.VIETNAMESE_TO_BASE:
                    base_char = self.char_maps.get_base_char(char)
                    t9_number = self.char_maps.get_t9_number(base_char)
                    special_char = self.char_maps.get_special_char(t9_number)
                    converted_chars.append(special_char)
                    
                    # Store diacritic and position information
                    ascii_code = self.char_maps.get_ascii_code(char)
                    diacritic_keys.append(chr(int(ascii_code)))
                    position_keys.append(self.char_maps.get_t9_position(base_char))
                else:
                    t9_number = self.char_maps.get_t9_number(char)
                    special_char = self.char_maps.get_special_char(t9_number)
                    converted_chars.append(special_char)
                    position_keys.append(self.char_maps.get_t9_position(char))
        
        return ''.join(converted_chars), diacritic_keys, position_keys


class PasswordGenerator:
    """
    High-level password generator that combines multiple conversion methods.
    
    This class manages the overall password generation process, including:
    - Splitting input text into components
    - Applying different conversion methods to each component
    - Combining results into a final password with key
    """
    
    def __init__(self, input_text: str):
        """
        Initialize the password generator.
        
        Args:
            input_text: The Vietnamese text to convert to a password
        """
        self.input_text = input_text
        self.components = []
        self.separator_key = '0'  # Default for space separator
        
    def _split_text(self) -> List[str]:
        """
        Split the input text into components based on separators.
        
        Returns:
            List of text components
        """
        if '.' in self.input_text:
            self.separator_key = '1'
            return self.input_text.split('.')
        else:
            self.separator_key = '0'
            return self.input_text.split(' ')
    
    def generate_password(self) -> Tuple[str, str]:
        """
        Generate a password from the input text.
        
        The algorithm applies different conversion methods in a rotating pattern:
        - Position 0, 3, 6, ... : T9 conversion with diacritics
        - Position 1, 4, 7, ... : Special character conversion
        - Position 2, 5, 8, ... : Number conversion
        
        Returns:
            Tuple containing:
            - complete_password: Full password with embedded key
            - password_only: Just the password part
        """
        components = self._split_text()
        password_parts = []
        all_diacritic_keys = []
        all_position_keys = []
        
        for i, component in enumerate(components):
            if not component.strip():
                continue
                
            converter = PasswordConverter(component)
            
            # Apply conversion based on position
            if i % 3 == 0:
                # T9 conversion with diacritics
                converted, diacritic_keys = converter.convert_t9_with_diacritics()
                password_parts.append(converted)
                all_diacritic_keys.extend(diacritic_keys)
                
            elif i % 3 == 1:
                # Special character conversion
                converted, diacritic_keys, position_keys = converter.convert_to_special_chars()
                password_parts.append(converted)
                all_diacritic_keys.extend(diacritic_keys)
                all_position_keys.extend(position_keys)
                
            else:  # i % 3 == 2
                # Number conversion
                converted, diacritic_keys, position_keys = converter.convert_to_numbers()
                password_parts.append(converted)
                all_diacritic_keys.extend(diacritic_keys)
                all_position_keys.extend(position_keys)
        
        # Combine all parts
        password = ''.join(password_parts)
        diacritic_part = ''.join(all_diacritic_keys)
        position_part = ''.join(all_position_keys)
        
        # Create metadata
        password_length = len(password)
        length_str = f"{password_length:02d}" if password_length >= 10 else f"0{password_length}"
        diacritic_count = str(len(diacritic_part))
        
        # Build complete password with embedded key
        complete_password = (
            password + 
            self.separator_key + 
            position_part + 
            diacritic_part + 
            diacritic_count + 
            length_str
        )
        
        return complete_password, password