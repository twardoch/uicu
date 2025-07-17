#!/usr/bin/env python3
"""
CLI tool for uicu package.
"""
import sys
import argparse
from typing import Optional

import uicu


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="uicu - Unicode and ICU utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uicu script text "Hello, 世界!"
  uicu name "€"
  uicu transliterate "Greek-Latin" "Ελληνικά"
  uicu collate "en-US" "café" "cafe"
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"uicu {uicu.__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Script detection command
    script_parser = subparsers.add_parser("script", help="Detect script of text")
    script_parser.add_argument("text", help="Text to analyze")
    
    # Character name command
    name_parser = subparsers.add_parser("name", help="Get character name")
    name_parser.add_argument("char", help="Character to analyze")
    
    # Transliteration command
    translit_parser = subparsers.add_parser("transliterate", help="Transliterate text")
    translit_parser.add_argument("transform", help="Transform to apply")
    translit_parser.add_argument("text", help="Text to transliterate")
    
    # Collation command
    collate_parser = subparsers.add_parser("collate", help="Compare strings")
    collate_parser.add_argument("locale", help="Locale to use")
    collate_parser.add_argument("text1", help="First text")
    collate_parser.add_argument("text2", help="Second text")
    
    args = parser.parse_args()
    
    try:
        if args.command == "script":
            result = uicu.detect_script(args.text)
            print(result if result else "Unknown")
        
        elif args.command == "name":
            if len(args.char) != 1:
                print("Error: Please provide a single character", file=sys.stderr)
                sys.exit(1)
            result = uicu.name(args.char)
            print(result)
        
        elif args.command == "transliterate":
            transliterator = uicu.Transliterator(args.transform)
            result = transliterator.transliterate(args.text)
            print(result)
        
        elif args.command == "collate":
            collator = uicu.Collator(args.locale)
            result = collator.compare(args.text1, args.text2)
            if result == 0:
                print("Equal")
            elif result < 0:
                print(f"'{args.text1}' < '{args.text2}'")
            else:
                print(f"'{args.text1}' > '{args.text2}'")
        
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
