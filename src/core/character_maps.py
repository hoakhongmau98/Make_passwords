"""
Character mapping dictionaries for Vietnamese password conversion.

This module contains all the character mappings used for converting Vietnamese text
to passwords and vice versa, including T9 keypad mappings and special character conversions.
"""

from typing import Dict


class CharacterMaps:
    """
    Container for all character mapping dictionaries used in Vietnamese password conversion.
    """

    # T9 keypad mapping (like old mobile phones)
    CHAR_TO_T9_NUMBER: Dict[str, str] = {
        'a': '2', 'b': '2', 'c': '2',
        'd': '3', 'e': '3', 'f': '3',
        'g': '4', 'h': '4', 'i': '4',
        'j': '5', 'k': '5', 'l': '5',
        'm': '6', 'n': '6', 'o': '6',
        'p': '7', 'q': '7', 'r': '7', 's': '7',
        't': '8', 'u': '8', 'v': '8',
        'w': '9', 'x': '9', 'y': '9', 'z': '9'
    }

    # Position of character on T9 keypad (1-4 for each number)
    CHAR_TO_T9_POSITION: Dict[str, str] = {
        'a': '1', 'b': '2', 'c': '3',
        'd': '1', 'e': '2', 'f': '3',
        'g': '1', 'h': '2', 'i': '3',
        'j': '1', 'k': '2', 'l': '3',
        'm': '1', 'n': '2', 'o': '3',
        'p': '1', 'q': '2', 'r': '3', 's': '4',
        't': '1', 'u': '2', 'v': '3',
        'w': '1', 'x': '2', 'y': '3', 'z': '4'
    }

    # Special character replacements for numbers
    NUMBER_TO_SPECIAL_CHAR: Dict[str, str] = {
        '0': ')', '1': '!', '2': '@', '3': '#', '4': '$',
        '5': '%', '6': '^', '7': '&', '8': '*', '9': '('
    }

    # Vietnamese diacritics to base character mapping
    VIETNAMESE_TO_BASE: Dict[str, str] = {
        'a': 'a', 'á': 'a', 'à': 'a', 'ạ': 'a', 'ã': 'a', 'ả': 'a',
        'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ặ': 'a', 'ẵ': 'a', 'ẳ': 'a',
        'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ậ': 'a', 'ẫ': 'a', 'ẩ': 'a',
        'ê': 'e', 'ế': 'e', 'ề': 'e', 'ệ': 'e', 'ễ': 'e', 'ể': 'e',
        'e': 'e', 'é': 'e', 'è': 'e', 'ẹ': 'e', 'ẽ': 'e', 'ẻ': 'e',
        'đ': 'd',
        'i': 'i', 'í': 'i', 'ì': 'i', 'ị': 'i', 'ĩ': 'i', 'ỉ': 'i',
        'o': 'o', 'ó': 'o', 'ò': 'o', 'ọ': 'o', 'õ': 'o', 'ỏ': 'o',
        'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ộ': 'o', 'ỗ': 'o', 'ổ': 'o',
        'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ợ': 'o', 'ỡ': 'o', 'ở': 'o',
        'u': 'u', 'ú': 'u', 'ù': 'u', 'ụ': 'u', 'ũ': 'u', 'ủ': 'u',
        'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ự': 'u', 'ữ': 'u', 'ử': 'u',
        'y': 'y', 'ý': 'y', 'ỳ': 'y', 'ỵ': 'y', 'ỹ': 'y', 'ỷ': 'y',
    }

    # Vietnamese characters to ASCII codes (for encoding)
    VIETNAMESE_TO_ASCII: Dict[str, str] = {
        'a': '49', 'á': '50', 'à': '51', 'ạ': '52', 'ã': '53', 'ả': '54',
        'ă': '55', 'ắ': '56', 'ằ': '57', 'ặ': '58', 'ẵ': '59', 'ẳ': '60',
        'â': '61', 'ấ': '62', 'ầ': '63', 'ậ': '64', 'ẫ': '65', 'ẩ': '66',
        'ê': '67', 'ế': '68', 'ề': '69', 'ệ': '70', 'ễ': '71', 'ể': '72',
        'e': '73', 'é': '74', 'è': '75', 'ẹ': '76', 'ẽ': '77', 'ẻ': '78',
        'đ': '79',
        'i': '80', 'í': '81', 'ì': '82', 'ị': '83', 'ĩ': '84', 'ỉ': '85',
        'o': '86', 'ó': '87', 'ò': '88', 'ọ': '89', 'õ': '90', 'ỏ': '91',
        'ô': '92', 'ố': '93', 'ồ': '94', 'ộ': '95', 'ỗ': '96', 'ổ': '97',
        'ơ': '98', 'ớ': '99', 'ờ': '100', 'ợ': '101', 'ỡ': '102', 'ở': '103',
        'u': '104', 'ú': '105', 'ù': '106', 'ụ': '107', 'ũ': '108', 'ủ': '109',
        'ư': '110', 'ứ': '111', 'ừ': '112', 'ự': '113', 'ữ': '114', 'ử': '115',
        'y': '116', 'ý': '117', 'ỳ': '118', 'ỵ': '119', 'ỹ': '120', 'ỷ': '121',
    }

    # Reverse mapping for decoding
    ASCII_TO_VIETNAMESE: Dict[str, str] = {
        v: k for k, v in VIETNAMESE_TO_ASCII.items()
    }

    # Characters that can have Vietnamese diacritics
    VIETNAMESE_BASE_CHARS = {'a', 'e', 'd', 'o', 'u', 'y', 'i'}

    # Vietnamese vowel type mapping (for complex conversions)
    VOWEL_TYPE_MAPPING: Dict[str, str] = {
        'a': '1', 'ă': '2', 'â': '3',
        'e': '1', 'ê': '2',
        'i': '1',
        'o': '1', 'ô': '2', 'ơ': '3',
        'u': '1', 'ư': '2',
        'y': '1'
    }

    @classmethod
    def get_t9_number(cls, char: str) -> str:
        """Get the T9 keypad number for a character."""
        return cls.CHAR_TO_T9_NUMBER.get(char.lower(), char)

    @classmethod
    def get_t9_position(cls, char: str) -> str:
        """Get the position of character on T9 keypad."""
        return cls.CHAR_TO_T9_POSITION.get(char.lower(), '1')

    @classmethod
    def get_special_char(cls, number: str) -> str:
        """Get special character replacement for a number."""
        return cls.NUMBER_TO_SPECIAL_CHAR.get(number, number)

    @classmethod
    def get_base_char(cls, vietnamese_char: str) -> str:
        """Get base character for Vietnamese diacritic."""
        return cls.VIETNAMESE_TO_BASE.get(vietnamese_char.lower(), vietnamese_char.lower())

    @classmethod
    def get_ascii_code(cls, vietnamese_char: str) -> str:
        """Get ASCII code for Vietnamese character."""
        return cls.VIETNAMESE_TO_ASCII.get(vietnamese_char.lower(), str(ord(vietnamese_char)))

    @classmethod
    def get_vietnamese_char(cls, ascii_code: str) -> str:
        """Get Vietnamese character from ASCII code."""
        return cls.ASCII_TO_VIETNAMESE.get(ascii_code, chr(int(ascii_code)) if ascii_code.isdigit() else ascii_code)

    @classmethod
    def has_vietnamese_diacritics(cls, char: str) -> bool:
        """Check if character can have Vietnamese diacritics."""
        return char.lower() in cls.VIETNAMESE_BASE_CHARS