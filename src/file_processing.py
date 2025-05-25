import os
from .signature import make_signature

def get_all_signatures(known_dir):
    """Generate text signatures for all files in directory."""
    file_signatures = {}
    
    for filename in os.listdir(known_dir):
        try:
            file_path = os.path.join(known_dir, filename)
            
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                file_signatures[filename] = make_signature(text_content)
                
        except (UnicodeDecodeError, PermissionError, OSError) as e:
            print(f"Warning: Could not process file '{filename}': {e}")
            continue
    
    return file_signatures

def process_data(mystery_filename, known_dir):
    """Identify most likely author using stylometric analysis."""
    from .signature import lowest_score
    
    known_signatures = get_all_signatures(known_dir)
    
    if not known_signatures:
        raise ValueError(f"No valid text files found in directory: {known_dir}")
    
    try:
        with open(mystery_filename, 'r', encoding='utf-8') as mystery_file:
            mystery_text = mystery_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Mystery file not found: {mystery_filename}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Cannot read mystery file as text: {mystery_filename}")
    
    mystery_signature = make_signature(mystery_text)
    
    # Weights: [word_len, unique_ratio, single_occurrence, sentence_len, complexity]
    authorship_weights = [11, 33, 50, 0.4, 4]
    
    return lowest_score(known_signatures, mystery_signature, authorship_weights)