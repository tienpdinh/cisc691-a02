#!/usr/bin/env python3
"""
Entry point for the Authorship Attribution System.

Usage:
    python run.py                          # Interactive mode
    python run.py mystery.txt              # Analyze specific file
    python run.py mystery.txt --quiet      # Analyze without verbose output
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import make_guess, analyze_file

def main():
    if len(sys.argv) == 1:
        make_guess()
    elif len(sys.argv) == 2:
        mystery_file = sys.argv[1]
        try:
            analyze_file(mystery_file, verbose=True)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[2] == "--quiet":
        mystery_file = sys.argv[1]
        try:
            result = analyze_file(mystery_file, verbose=False)
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage:")
        print("  python run.py                    # Interactive mode")
        print("  python run.py mystery.txt        # Analyze specific file")
        print("  python run.py mystery.txt --quiet # Analyze quietly")
        sys.exit(1)

if __name__ == "__main__":
    main()