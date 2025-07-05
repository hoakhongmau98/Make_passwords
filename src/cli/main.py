#!/usr/bin/env python3
"""
Vietnamese Password Converter CLI

Command-line interface for converting Vietnamese text to passwords and vice versa.
"""

import argparse
import sys
import os
from typing import Optional

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.converter import PasswordGenerator
from core.decoder import PasswordDecoder, PasswordAnalyzer
from utils.validators import InputValidator, PasswordValidator


def print_banner():
    """Print the application banner."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Vietnamese Password Converter                             ║
║                                                                              ║
║  Convert Vietnamese text to secure passwords and vice versa                 ║
║  Supports Vietnamese diacritics and T9 keypad conversion                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def print_help():
    """Print detailed help information."""
    print("""
USAGE:
    python -m src.cli.main [options]

OPTIONS:
    -g, --generate TEXT     Generate password from Vietnamese text
    -d, --decode PASSWORD   Decode password back to Vietnamese text
    -i, --interactive       Run in interactive mode
    -a, --analyze PASSWORD  Analyze password structure and strength
    -v, --validate TEXT     Validate input text
    --info TEXT            Show information about input text
    --help                 Show this help message
    --version              Show version information

EXAMPLES:
    # Generate password from text
    python -m src.cli.main -g "Nguyễn Văn An"
    
    # Decode password back to text
    python -m src.cli.main -d "Nguyen*$#*286640332132321htGPDnd715"
    
    # Interactive mode
    python -m src.cli.main -i
    
    # Analyze password strength
    python -m src.cli.main -a "Nguyen*$#*286640332132321htGPDnd715"

NOTES:
    - Supports Vietnamese diacritics (á, à, ả, ã, ạ, etc.)
    - Use spaces or dots as separators between words
    - Maximum recommended input length: 100 characters
    - Generated passwords include embedded decoding keys
    """)


def generate_password(text: str, verbose: bool = False) -> None:
    """
    Generate password from Vietnamese text.
    
    Args:
        text: Input Vietnamese text
        verbose: Whether to show detailed information
    """
    # Validate input
    is_valid, error_msg = InputValidator.validate_input_text(text)
    if not is_valid:
        print(f"❌ Input validation failed: {error_msg}")
        return
    
    try:
        # Generate password
        generator = PasswordGenerator(text)
        complete_password, password_only = generator.generate_password()
        
        # Show results
        print(f"✅ Password generated successfully!")
        print(f"📝 Original text: {text}")
        print(f"🔐 Password: {password_only}")
        print(f"🔑 Complete password (with key): {complete_password}")
        
        if verbose:
            # Show detailed information
            text_info = InputValidator.get_text_info(text)
            strength_info = PasswordValidator.check_password_strength(password_only)
            
            print("\n📊 Analysis:")
            print(f"   Text length: {text_info['length']} characters")
            print(f"   Word count: {text_info['word_count']}")
            print(f"   Vietnamese characters: {text_info['vietnamese_char_count']}")
            print(f"   Separator: {text_info['separator_type']}")
            print(f"   Password strength: {strength_info['strength']} (score: {strength_info['score']}/7)")
            print(f"   Password entropy: ~{strength_info['entropy']} bits")
        
        print(f"\n💡 Tip: Save the complete password to decode back to original text")
        
    except Exception as e:
        print(f"❌ Error generating password: {str(e)}")


def decode_password(password: str, verbose: bool = False) -> None:
    """
    Decode password back to Vietnamese text.
    
    Args:
        password: Encoded password
        verbose: Whether to show detailed information
    """
    # Validate password format
    is_valid, error_msg = InputValidator.validate_encoded_password(password)
    if not is_valid:
        print(f"❌ Password validation failed: {error_msg}")
        return
    
    try:
        # Decode password
        decoder = PasswordDecoder(password)
        original_text = decoder.decode()
        
        # Show results
        print(f"✅ Password decoded successfully!")
        print(f"🔐 Encoded password: {password}")
        print(f"📝 Original text: {original_text}")
        
        if verbose:
            # Show detailed information
            password_info = PasswordAnalyzer.get_password_info(password)
            
            print("\n📊 Analysis:")
            print(f"   Password length: {password_info['password_length']}")
            print(f"   Separator type: {password_info['separator_type']}")
            print(f"   Diacritic count: {password_info['diacritic_count']}")
            print(f"   Position keys: {password_info['position_keys_count']}")
            print(f"   Password part: {password_info['password_part']}")
        
    except Exception as e:
        print(f"❌ Error decoding password: {str(e)}")


def analyze_password(password: str) -> None:
    """
    Analyze password structure and strength.
    
    Args:
        password: Password to analyze
    """
    try:
        # Check if it's an encoded password
        if PasswordAnalyzer.is_valid_password(password):
            print("🔍 Analyzing encoded password...")
            
            # Get password info
            password_info = PasswordAnalyzer.get_password_info(password)
            
            print(f"✅ Valid encoded password format")
            print(f"📊 Structure Analysis:")
            print(f"   Total length: {len(password)} characters")
            print(f"   Password part length: {password_info['password_length']}")
            print(f"   Separator type: {password_info['separator_type']}")
            print(f"   Diacritic count: {password_info['diacritic_count']}")
            print(f"   Position keys count: {password_info['position_keys_count']}")
            print(f"   Password part: {password_info['password_part']}")
            
            # Analyze strength of password part
            strength_info = PasswordValidator.check_password_strength(password_info['password_part'])
            
            print(f"\n🔐 Password Strength Analysis:")
            print(f"   Strength: {strength_info['strength']} (score: {strength_info['score']}/7)")
            print(f"   Length: {strength_info['length']} characters")
            print(f"   Has uppercase: {'✓' if strength_info['has_uppercase'] else '✗'}")
            print(f"   Has lowercase: {'✓' if strength_info['has_lowercase'] else '✗'}")
            print(f"   Has numbers: {'✓' if strength_info['has_numbers'] else '✗'}")
            print(f"   Has special chars: {'✓' if strength_info['has_special'] else '✗'}")
            print(f"   Estimated entropy: ~{strength_info['entropy']} bits")
            
        else:
            print("🔍 Analyzing regular password...")
            
            # Analyze as regular password
            strength_info = PasswordValidator.check_password_strength(password)
            
            print(f"📊 Password Strength Analysis:")
            print(f"   Strength: {strength_info['strength']} (score: {strength_info['score']}/7)")
            print(f"   Length: {strength_info['length']} characters")
            print(f"   Has uppercase: {'✓' if strength_info['has_uppercase'] else '✗'}")
            print(f"   Has lowercase: {'✓' if strength_info['has_lowercase'] else '✗'}")
            print(f"   Has numbers: {'✓' if strength_info['has_numbers'] else '✗'}")
            print(f"   Has special chars: {'✓' if strength_info['has_special'] else '✗'}")
            print(f"   Estimated entropy: ~{strength_info['entropy']} bits")
            
    except Exception as e:
        print(f"❌ Error analyzing password: {str(e)}")


def validate_text(text: str) -> None:
    """
    Validate input text and show information.
    
    Args:
        text: Text to validate
    """
    # Validate input
    is_valid, error_msg = InputValidator.validate_input_text(text)
    
    if is_valid:
        print(f"✅ Input text is valid")
    else:
        print(f"❌ Input text is invalid: {error_msg}")
    
    # Show text information
    text_info = InputValidator.get_text_info(text)
    
    print(f"\n📊 Text Information:")
    print(f"   Length: {text_info['length']} characters")
    print(f"   Word count: {text_info['word_count']}")
    print(f"   Has Vietnamese characters: {'✓' if text_info['has_vietnamese'] else '✗'}")
    print(f"   Vietnamese character count: {text_info['vietnamese_char_count']}")
    print(f"   Separator type: {text_info['separator_type']}")
    print(f"   Estimated password length: {text_info['estimated_password_length']}")
    
    if text_info['words']:
        print(f"   Words: {', '.join(text_info['words'])}")


def interactive_mode():
    """Run the application in interactive mode."""
    print_banner()
    print("🔄 Interactive Mode - Type 'help' for commands, 'quit' to exit")
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if command.lower() == 'help':
                print("""
Available commands:
  generate <text>     - Generate password from Vietnamese text
  decode <password>   - Decode password back to text
  analyze <password>  - Analyze password structure and strength
  validate <text>     - Validate input text
  info <text>         - Show information about text
  help                - Show this help
  quit                - Exit the program

Examples:
  generate Nguyễn Văn An
  decode Nguyen*$#*286640332132321htGPDnd715
  analyze MyPassword123
  validate Trần Thị Bảo
                """)
                continue
            
            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("❌ Invalid command. Type 'help' for usage.")
                continue
            
            cmd, arg = parts[0].lower(), parts[1]
            
            if cmd == 'generate':
                generate_password(arg, verbose=True)
            elif cmd == 'decode':
                decode_password(arg, verbose=True)
            elif cmd == 'analyze':
                analyze_password(arg)
            elif cmd == 'validate':
                validate_text(arg)
            elif cmd == 'info':
                validate_text(arg)
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Vietnamese Password Converter - Convert Vietnamese text to passwords and vice versa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.cli.main -g "Nguyễn Văn An"
  python -m src.cli.main -d "Nguyen*$#*286640332132321htGPDnd715"
  python -m src.cli.main -i
  python -m src.cli.main -a "MyPassword123"
        """
    )
    
    parser.add_argument('-g', '--generate', metavar='TEXT', 
                       help='Generate password from Vietnamese text')
    parser.add_argument('-d', '--decode', metavar='PASSWORD', 
                       help='Decode password back to Vietnamese text')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('-a', '--analyze', metavar='PASSWORD',
                       help='Analyze password structure and strength')
    parser.add_argument('-v', '--validate', metavar='TEXT',
                       help='Validate input text')
    parser.add_argument('--info', metavar='TEXT',
                       help='Show information about input text')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        print_help()
        return
    
    # Handle commands
    if args.interactive:
        interactive_mode()
    elif args.generate:
        generate_password(args.generate, verbose=True)
    elif args.decode:
        decode_password(args.decode, verbose=True)
    elif args.analyze:
        analyze_password(args.analyze)
    elif args.validate:
        validate_text(args.validate)
    elif args.info:
        validate_text(args.info)
    else:
        print("❌ No valid command provided. Use --help for usage information.")


if __name__ == "__main__":
    main()