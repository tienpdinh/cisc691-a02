#!/usr/bin/env python3
"""
Entry point for the Authorship Attribution System.

Usage:
    python run.py                          # Interactive mode with author choice
    python run.py mystery.txt              # Analyze specific file using Tien's module
    python run.py mystery.txt --quiet      # Analyze without verbose output using Tien's module
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.tien.main import (
    make_guess as tien_make_guess,
    analyze_file as tien_analyze_file,
)
from src.kenneth.authorship_identifier import (
    make_guess as kenneth_make_guess
)
from src.enhanced.enhanced_authorship_identifier import make_guess as enhanced_make_guess


def main():
    print("=" * 60)
    print("AUTHORSHIP ATTRIBUTION SYSTEM")
    print("=" * 60)

    if len(sys.argv) == 1:

        print("\nChoose which version to run:")
        print("1. Kenneth's authorship identifier")
        print("2. Tien's authorship identifier")
        print("3. Groups's enhanced authorship identifier")
        choice = input("Enter 1, 2 or 3: ").strip()

        if choice == "1":
            kenneth_make_guess("data/known_authors")
        elif choice == "2":
            tien_make_guess()
        elif choice == "3":
            enhanced_make_guess("data/known_authors")
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")
            sys.exit(1)

    elif len(sys.argv) == 2:
        mystery_file = sys.argv[1]
        try:
            print("Using Tien's module to analyze...")
            tien_analyze_file(mystery_file, verbose=True)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif len(sys.argv) == 3 and sys.argv[2] == "--quiet":
        mystery_file = sys.argv[1]
        try:
            print("Using Tien's module to analyze quietly...")
            result = tien_analyze_file(mystery_file, verbose=False)
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        print("Usage:")
        print(
            "  python run.py                            # Interactive mode with choice"
        )
        print("  python run.py mystery.txt                # Analyze with Tien's module")
        print(
            "  python run.py mystery.txt --quiet        # Quiet mode with Tien's module"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
