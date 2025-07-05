"""
Vietnamese Password Decoder

This module provides functionality to decode passwords back to Vietnamese text
by reversing the T9 keypad conversion and special character substitutions.
"""

from typing import List, Tuple, Optional
from .character_maps import CharacterMaps


class PasswordDecoder:
    """
    Decodes passwords back to Vietnamese text by reversing the conversion process.
    
    The decoder parses the embedded key information to reconstruct the original
    Vietnamese text with proper diacritics and spacing.
    """
    
    def __init__(self, encoded_password: str):
        """
        Initialize the decoder with an encoded password.
        
        Args:
            encoded_password: The encoded password containing the text and key
            
        Raises:
            ValueError: If encoded_password is empty or invalid format
        """
        if not encoded_password or not encoded_password.strip():
            raise ValueError("Encoded password cannot be empty")
        
        self.encoded_password = encoded_password.strip()
        self.char_maps = CharacterMaps()
        
        # Parse the password components
        self._parse_password()
    
    def _parse_password(self) -> None:
        """
        Parse the encoded password into its components.
        
        Expected format: password + separator_key + position_keys + diacritic_keys + diacritic_count + length
        """
        try:
            # Extract length (last 2 characters)
            self.password_length = int(self.encoded_password[-2:])
            
            # Extract the actual password
            self.password = self.encoded_password[:self.password_length]
            
            # Extract separator key (space or dot)
            self.separator_key = self.encoded_password[self.password_length]
            
            # Extract diacritic count (3rd character from end)
            self.diacritic_count = int(self.encoded_password[-3])
            
            # Extract diacritic keys
            diacritic_start = -(3 + self.diacritic_count)
            self.diacritic_keys = self.encoded_password[diacritic_start:-3]
            
            # Extract position keys
            position_start = self.password_length + 1
            position_end = diacritic_start
            self.position_keys = self.encoded_password[position_start:position_end]
            
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid password format: {e}")
    
    def _parse_password_components(self) -> List[str]:
        """
        Parse the password into its individual components (text, special chars, numbers).
        
        Returns:
            List of password components
        """
        components = []
        current_pos = 0
        
        while current_pos < len(self.password):
            char = self.password[current_pos]
            
            if char.isalpha():
                # Extract alphabetic sequence
                component = self._extract_alpha_sequence(current_pos)
                components.append(component[0])
                current_pos = component[1]
            elif char.isdigit():
                # Extract numeric sequence
                component = self._extract_digit_sequence(current_pos)
                components.append(component[0])
                current_pos = component[1]
            else:
                # Extract special character sequence
                component = self._extract_special_sequence(current_pos)
                components.append(component[0])
                current_pos = component[1]
        
        return components
    
    def _extract_alpha_sequence(self, start_pos: int) -> Tuple[str, int]:
        """Extract a sequence of alphabetic characters."""
        sequence = ""
        pos = start_pos
        
        while pos < len(self.password) and self.password[pos].isalpha():
            sequence += self.password[pos]
            pos += 1
        
        return sequence, pos
    
    def _extract_digit_sequence(self, start_pos: int) -> Tuple[str, int]:
        """Extract a sequence of numeric characters."""
        sequence = ""
        pos = start_pos
        
        while pos < len(self.password) and self.password[pos].isdigit():
            sequence += self.password[pos]
            pos += 1
        
        return sequence, pos
    
    def _extract_special_sequence(self, start_pos: int) -> Tuple[str, int]:
        """Extract a sequence of special characters."""
        sequence = ""
        pos = start_pos
        
        while pos < len(self.password) and not self.password[pos].isalnum():
            sequence += self.password[pos]
            pos += 1
        
        return sequence, pos
    
    def _convert_special_to_numbers(self, special_text: str) -> str:
        """Convert special characters back to numbers."""
        result = ""
        for char in special_text:
            # Find the number that maps to this special character
            for number, special_char in self.char_maps.NUMBER_TO_SPECIAL_CHAR.items():
                if char == special_char:
                    result += number
                    break
            else:
                result += char  # Keep unchanged if not found
        
        return result
    
    def _convert_numbers_to_letters(self, number_text: str, position_keys: List[str]) -> str:
        """
        Convert T9 numbers back to letters using position information.
        
        Args:
            number_text: String of T9 numbers
            position_keys: List of position keys for each character
            
        Returns:
            String of letters
        """
        result = ""
        pos_index = 0
        
        for char in number_text:
            if char.isdigit() and pos_index < len(position_keys):
                # Get all possible letters for this T9 number
                possible_chars = []
                for letter, t9_num in self.char_maps.CHAR_TO_T9_NUMBER.items():
                    if t9_num == char:
                        possible_chars.append(letter)
                
                # Select the correct letter using position key
                if possible_chars:
                    position = int(position_keys[pos_index]) - 1
                    if 0 <= position < len(possible_chars):
                        result += possible_chars[position]
                    else:
                        result += possible_chars[0]  # Default to first
                else:
                    result += char
                
                pos_index += 1
            else:
                result += char
        
        return result
    
    def _restore_vietnamese_diacritics(self, text: str, diacritic_keys: str) -> str:
        """
        Restore Vietnamese diacritics using the diacritic keys.
        
        Args:
            text: Text with base characters
            diacritic_keys: String containing diacritic information
            
        Returns:
            Text with Vietnamese diacritics restored
        """
        result = list(text)
        diacritic_index = 0
        
        for i, char in enumerate(result):
            if char.lower() in self.char_maps.VIETNAMESE_BASE_CHARS and diacritic_index < len(diacritic_keys):
                # Get the ASCII code for the diacritic
                ascii_code = str(ord(diacritic_keys[diacritic_index]))
                
                # Convert back to Vietnamese character
                vietnamese_char = self.char_maps.get_vietnamese_char(ascii_code)
                
                # Preserve case
                if char.isupper():
                    result[i] = vietnamese_char.upper()
                else:
                    result[i] = vietnamese_char
                
                diacritic_index += 1
        
        return ''.join(result)
    
    def decode(self) -> str:
        """
        Decode the password back to Vietnamese text.
        
        Returns:
            The original Vietnamese text
        """
        # Parse password into components
        components = self._parse_password_components()
        
        # Process each component based on its type and position
        processed_components = []
        position_key_index = 0
        diacritic_key_index = 0
        
        for i, component in enumerate(components):
            if i % 3 == 0:
                # First component type: T9 with diacritics (kept as text)
                if diacritic_key_index < len(self.diacritic_keys):
                    # Count Vietnamese characters in this component
                    vietnamese_count = sum(1 for c in component.lower() 
                                         if c in self.char_maps.VIETNAMESE_BASE_CHARS)
                    
                    # Extract diacritic keys for this component
                    component_diacritic_keys = self.diacritic_keys[
                        diacritic_key_index:diacritic_key_index + vietnamese_count
                    ]
                    
                    # Restore diacritics
                    restored = self._restore_vietnamese_diacritics(component, component_diacritic_keys)
                    processed_components.append(restored)
                    
                    diacritic_key_index += vietnamese_count
                else:
                    processed_components.append(component)
            
            elif i % 3 == 1:
                # Second component type: Special characters
                # Convert special chars to numbers, then numbers to letters
                numbers = self._convert_special_to_numbers(component)
                
                # Count how many position keys we need
                letter_count = sum(1 for c in numbers if c.isdigit())
                
                if position_key_index < len(self.position_keys):
                    component_position_keys = self.position_keys[
                        position_key_index:position_key_index + letter_count
                    ]
                    letters = self._convert_numbers_to_letters(numbers, component_position_keys)
                    position_key_index += letter_count
                else:
                    letters = self._convert_numbers_to_letters(numbers, [])
                
                # Restore diacritics if needed
                if diacritic_key_index < len(self.diacritic_keys):
                    vietnamese_count = sum(1 for c in letters.lower() 
                                         if c in self.char_maps.VIETNAMESE_BASE_CHARS)
                    
                    if vietnamese_count > 0:
                        component_diacritic_keys = self.diacritic_keys[
                            diacritic_key_index:diacritic_key_index + vietnamese_count
                        ]
                        letters = self._restore_vietnamese_diacritics(letters, component_diacritic_keys)
                        diacritic_key_index += vietnamese_count
                
                processed_components.append(letters)
            
            else:  # i % 3 == 2
                # Third component type: Numbers
                # Convert numbers to letters
                letter_count = sum(1 for c in component if c.isdigit())
                
                if position_key_index < len(self.position_keys):
                    component_position_keys = self.position_keys[
                        position_key_index:position_key_index + letter_count
                    ]
                    letters = self._convert_numbers_to_letters(component, component_position_keys)
                    position_key_index += letter_count
                else:
                    letters = self._convert_numbers_to_letters(component, [])
                
                # Restore diacritics if needed
                if diacritic_key_index < len(self.diacritic_keys):
                    vietnamese_count = sum(1 for c in letters.lower() 
                                         if c in self.char_maps.VIETNAMESE_BASE_CHARS)
                    
                    if vietnamese_count > 0:
                        component_diacritic_keys = self.diacritic_keys[
                            diacritic_key_index:diacritic_key_index + vietnamese_count
                        ]
                        letters = self._restore_vietnamese_diacritics(letters, component_diacritic_keys)
                        diacritic_key_index += vietnamese_count
                
                processed_components.append(letters)
        
        # Join components with appropriate separator
        separator = ' ' if self.separator_key == '0' else '.'
        result = separator.join(processed_components)
        
        # Apply title case formatting
        return result.title()


class PasswordAnalyzer:
    """
    Utility class for analyzing and validating encoded passwords.
    """
    
    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Check if a password has valid format.
        
        Args:
            password: The password to validate
            
        Returns:
            True if password format is valid, False otherwise
        """
        try:
            decoder = PasswordDecoder(password)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def get_password_info(password: str) -> dict:
        """
        Get information about an encoded password.
        
        Args:
            password: The encoded password
            
        Returns:
            Dictionary containing password information
        """
        try:
            decoder = PasswordDecoder(password)
            return {
                'valid': True,
                'password_length': decoder.password_length,
                'separator_type': 'space' if decoder.separator_key == '0' else 'dot',
                'diacritic_count': decoder.diacritic_count,
                'position_keys_count': len(decoder.position_keys),
                'password_part': decoder.password
            }
        except ValueError as e:
            return {
                'valid': False,
                'error': str(e)
            }