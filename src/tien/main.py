import os
from .file_processing import process_data

def make_guess(known_dir="data/known_authors"):
    """Interactive authorship attribution tool."""

    print(f"Known author samples directory: {known_dir}")
    print()
    
    if not os.path.exists(known_dir):
        print(f"Error: Directory '{known_dir}' does not exist.")
        return
    
    if not os.path.isdir(known_dir):
        print(f"Error: '{known_dir}' is not a directory.")
        return
    
    print("Enter the filename of the mystery text you want to analyze.")
    mystery_filename = input("Enter filename: ").strip()
    
    if not mystery_filename:
        print("Error: No filename provided.")
        return
    
    print(f"\nAnalyzing: {mystery_filename}")
    print(f"Comparing against: {known_dir}")
    print("-" * 60)
    
    try:
        best_match = process_data(mystery_filename, known_dir)
        
        print("\nANALYSIS COMPLETE")
        print("=" * 30)
        print(f"Best matching author sample: {best_match}")
        print(f"\nThe mystery text has similar writing style to '{best_match}'.")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please check that the filename is correct and the file exists.")
        
    except ValueError as e:
        print(f"\nError: {e}")
        
    except UnicodeDecodeError as e:
        print(f"\nError: {e}")
        print("The file may be binary or use unsupported encoding.")
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    
    print("\n" + "=" * 60)

def analyze_file(mystery_file, known_dir="data/known_authors", verbose=True):
    """Analyze a single file without user interaction."""
    if verbose:
        print(f"Analyzing: {mystery_file}")
        print(f"Against samples in: {known_dir}")
    
    try:
        result = process_data(mystery_file, known_dir)
        if verbose:
            print(f"Best match: {result}")
        return result
    except Exception as e:
        if verbose:
            print(f"Error: {e}")
        raise