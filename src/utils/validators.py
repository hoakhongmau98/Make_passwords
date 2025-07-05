"""
Input validation utilities for Vietnamese password conversion.

This module provides comprehensive validation for Vietnamese text inputs,
including length checks, character validation, and format verification.
"""

import re
from typing import Union, List, Tuple


class InputValidator:
    """
    Validates input text for Vietnamese password conversion.
    """
    
    # Maximum recommended length for password generation
    MAX_TEXT_LENGTH = 100
    MIN_TEXT_LENGTH = 1
    
    # Vietnamese character pattern
    VIETNAMESE_PATTERN = re.compile(r'[aáàạãảăắằặẵẳâấầậẫẩeéèẹẽẻêếềệễểđiíìịĩỉoóòọõỏôốồộỗổơớờợỡởuúùụũủưứừựữửyýỳỵỹỷ]', re.IGNORECASE)
    
    # Valid separators
    VALID_SEPARATORS = {' ', '.'}
    
    @classmethod
    def validate_input_text(cls, text: str) -> Tuple[bool, str]:
        """
        Validate input text for password generation.
        
        Args:
            text: Input text to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text:
            return False, "Input text cannot be empty"
        
        text = text.strip()
        
        if not text:
            return False, "Input text cannot be empty after trimming whitespace"
        
        if len(text) < cls.MIN_TEXT_LENGTH:
            return False, f"Input text must be at least {cls.MIN_TEXT_LENGTH} character long"
        
        if len(text) > cls.MAX_TEXT_LENGTH:
            return False, f"Input text cannot exceed {cls.MAX_TEXT_LENGTH} characters"
        
        # Check for valid characters (letters, numbers, spaces, dots, Vietnamese characters)
        if not cls._has_valid_characters(text):
            return False, "Input text contains invalid characters"
        
        # Check for reasonable word structure
        if not cls._has_reasonable_structure(text):
            return False, "Input text structure is not suitable for password generation"
        
        return True, ""
    
    @classmethod
    def validate_encoded_password(cls, password: str) -> Tuple[bool, str]:
        """
        Validate encoded password format.
        
        Args:
            password: Encoded password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        
        password = password.strip()
        
        if len(password) < 5:
            return False, "Password is too short to be valid"
        
        # Check if last 2 characters are digits (password length)
        if not password[-2:].isdigit():
            return False, "Invalid password format: missing length information"
        
        # Check if third from last character is a digit (diacritic count)
        if not password[-3].isdigit():
            return False, "Invalid password format: missing diacritic count"
        
        # Extract and validate password length
        try:
            password_length = int(password[-2:])
            if password_length <= 0 or password_length >= len(password):
                return False, "Invalid password format: invalid length information"
        except ValueError:
            return False, "Invalid password format: length information is not a valid number"
        
        return True, ""
    
    @classmethod
    def _has_valid_characters(cls, text: str) -> bool:
        """
        Check if text contains only valid characters.
        
        Args:
            text: Text to check
            
        Returns:
            True if all characters are valid, False otherwise
        """
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .")
        vietnamese_chars = set("aáàạãảăắằặẵẳâấầậẫẩeéèẹẽẻêếềệễểđiíìịĩỉoóòọõỏôốồộỗổơớờợỡởuúùụũủưứừựữửyýỳỵỹỷ")
        vietnamese_chars_upper = set(c.upper() for c in vietnamese_chars)
        vietnamese_chars.update(vietnamese_chars_upper)
        
        all_valid = valid_chars.union(vietnamese_chars)
        
        return all(c in all_valid for c in text)
    
    @classmethod
    def _has_reasonable_structure(cls, text: str) -> bool:
        """
        Check if text has reasonable structure for password generation.
        
        Args:
            text: Text to check
            
        Returns:
            True if structure is reasonable, False otherwise
        """
        # Check for excessive consecutive spaces or dots
        if re.search(r'[ ]{3,}', text) or re.search(r'[.]{2,}', text):
            return False
        
        # Check for mixed separators (both space and dot)
        has_space = ' ' in text
        has_dot = '.' in text
        if has_space and has_dot:
            return False
        
        # Check for reasonable word count (1-10 words)
        if ' ' in text:
            words = [w.strip() for w in text.split(' ') if w.strip()]
        elif '.' in text:
            words = [w.strip() for w in text.split('.') if w.strip()]
        else:
            words = [text]
        
        if len(words) < 1 or len(words) > 10:
            return False
        
        # Check for reasonable word lengths (1-20 characters each)
        for word in words:
            if len(word) < 1 or len(word) > 20:
                return False
        
        return True
    
    @classmethod
    def sanitize_input(cls, text: str) -> str:
        """
        Sanitize input text by removing or fixing common issues.
        
        Args:
            text: Input text to sanitize
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Normalize spaces (replace multiple spaces with single space)
        text = re.sub(r' +', ' ', text)
        
        # Remove any characters that are not letters, numbers, spaces, or dots
        text = re.sub(r'[^a-zA-Z0-9 .\u00C0-\u1EF9]', '', text)
        
        return text
    
    @classmethod
    def get_text_info(cls, text: str) -> dict:
        """
        Get information about input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing text information
        """
        if not text:
            return {
                'length': 0,
                'word_count': 0,
                'has_vietnamese': False,
                'separator_type': None,
                'estimated_password_length': 0
            }
        
        text = text.strip()
        
        # Count Vietnamese characters
        vietnamese_matches = cls.VIETNAMESE_PATTERN.findall(text)
        has_vietnamese = len(vietnamese_matches) > 0
        
        # Determine separator type
        separator_type = None
        if ' ' in text:
            separator_type = 'space'
            words = text.split(' ')
        elif '.' in text:
            separator_type = 'dot'
            words = text.split('.')
        else:
            separator_type = 'none'
            words = [text]
        
        # Filter out empty words
        words = [w.strip() for w in words if w.strip()]
        
        # Estimate password length (rough approximation)
        estimated_length = len(text) + len(words) * 2  # Add some padding for conversions
        
        return {
            'length': len(text),
            'word_count': len(words),
            'has_vietnamese': has_vietnamese,
            'vietnamese_char_count': len(vietnamese_matches),
            'separator_type': separator_type,
            'estimated_password_length': estimated_length,
            'words': words
        }


class PasswordValidator:
    """
    Validates password strength and quality.
    """
    
    @classmethod
    def check_password_strength(cls, password: str) -> dict:
        """
        Check the strength of a generated password.
        
        Args:
            password: Password to check
            
        Returns:
            Dictionary containing strength information
        """
        if not password:
            return {
                'score': 0,
                'strength': 'None',
                'has_uppercase': False,
                'has_lowercase': False,
                'has_numbers': False,
                'has_special': False,
                'length': 0,
                'entropy': 0
            }
        
        score = 0
        
        # Length check
        length = len(password)
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        
        # Character type checks
        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_numbers = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if has_uppercase:
            score += 1
        if has_lowercase:
            score += 1
        if has_numbers:
            score += 1
        if has_special:
            score += 1
        
        # Calculate entropy (rough approximation)
        charset_size = 0
        if has_lowercase:
            charset_size += 26
        if has_uppercase:
            charset_size += 26
        if has_numbers:
            charset_size += 10
        if has_special:
            charset_size += 32  # Approximate special characters
        
        entropy = length * (charset_size.bit_length() - 1) if charset_size > 0 else 0
        
        # Determine strength
        if score >= 6:
            strength = 'Strong'
        elif score >= 4:
            strength = 'Medium'
        elif score >= 2:
            strength = 'Weak'
        else:
            strength = 'Very Weak'
        
        return {
            'score': score,
            'strength': strength,
            'has_uppercase': has_uppercase,
            'has_lowercase': has_lowercase,
            'has_numbers': has_numbers,
            'has_special': has_special,
            'length': length,
            'entropy': entropy
        }