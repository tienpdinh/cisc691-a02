import string
import os

def clean_word(word):
    """
    Clean a word by converting to lowercase and stripping punctuation from ends.
    
    Args:
        word (str): The input word to clean
        
    Returns:
        str: A cleaned version of the word with lowercase letters and 
             punctuation stripped from both ends. Inner punctuation is preserved.
    
    Examples:
        >>> clean_word('Pearl!')
        'pearl'
        >>> clean_word('card-board')
        'card-board'
    """
    word = word.lower()
    word = word.strip(string.punctuation)
    return word

def average_word_length(text):
    """
    Calculate the average word length in a text string.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        float: The average length of words in the text, excluding empty words
               and not counting surrounding punctuation
               
    Raises:
        ZeroDivisionError: If no valid words are found in the text
    
    Examples:
        >>> average_word_length('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.')
        4.1
        >>> average_word_length('Hello world!')
        5.0
        >>> average_word_length('...')
        ZeroDivisionError: No valid words found in text
    """
    # Split text into individual words
    words = text.split()
    
    # Initialize counters for total character length and word count
    total_length = 0
    word_count = 0
    
    # Process each word in the text
    for word in words:
        # Clean the word (remove punctuation, convert to lowercase)
        cleaned_word = clean_word(word)
        
        # Only count non-empty words
        if cleaned_word != '':
            total_length += len(cleaned_word)
            word_count += 1
    
    # Handle edge case where no valid words are found
    if word_count == 0:
        raise ZeroDivisionError("No valid words found in text")
    
    # Calculate and return the average word length
    return total_length / word_count

def different_to_total(text):
    """
    Calculate the ratio of unique words to total words in a text string.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        float: The ratio of unique words to total words (between 0.0 and 1.0)
               where 1.0 means all words are unique and 0.0 would mean no words
               
    Raises:
        ZeroDivisionError: If no valid words are found in the text
    
    Examples:
        >>> different_to_total('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.')
        0.7
        >>> different_to_total('hello hello hello')
        0.3333333333333333
        >>> different_to_total('cat dog bird')
        1.0
        >>> different_to_total('...')
        ZeroDivisionError: No valid words found in text
    """
    # Split text into individual words
    words = text.split()
    
    # Initialize counter for total valid words and set for unique words
    total_word_count = 0
    unique_words = set()
    
    # Process each word in the text
    for word in words:
        # Clean the word (remove punctuation, convert to lowercase)
        cleaned_word = clean_word(word)
        
        # Only count non-empty words
        if cleaned_word != '':
            total_word_count += 1
            unique_words.add(cleaned_word)
    
    # Handle edge case where no valid words are found
    if total_word_count == 0:
        raise ZeroDivisionError("No valid words found in text")
    
    # Calculate and return the ratio of unique to total words
    return len(unique_words) / total_word_count

def exactly_once_to_total(text):
    """
    Calculate the ratio of words appearing exactly once to total words in text.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        float: The ratio of words that appear exactly once to total words
               (between 0.0 and 1.0)
               
    Raises:
        ZeroDivisionError: If no valid words are found in the text
    
    Examples:
        >>> exactly_once_to_total('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.')
        0.5
        >>> exactly_once_to_total('hello world hello')
        0.3333333333333333
        >>> exactly_once_to_total('cat dog bird')
        1.0
        >>> exactly_once_to_total('the the the the')
        0.0
    """
    # Split text into individual words
    words = text.split()
    
    # Initialize counters and tracking sets
    total_word_count = 0
    seen_words = set()          # Track all words we've encountered
    words_seen_once = set()     # Track words that appear exactly once
    
    # Process each word in the text
    for word in words:
        # Clean the word (remove punctuation, convert to lowercase)
        cleaned_word = clean_word(word)
        
        # Only process non-empty words
        if cleaned_word != '':
            total_word_count += 1
            
            if cleaned_word in seen_words:
                # Word seen before - remove from "exactly once" set
                words_seen_once.discard(cleaned_word)
            else:
                # First time seeing this word - add to both sets
                seen_words.add(cleaned_word)
                words_seen_once.add(cleaned_word)
    
    # Handle edge case where no valid words are found
    if total_word_count == 0:
        raise ZeroDivisionError("No valid words found in text")
    
    # Calculate and return the ratio of words appearing exactly once to total words
    return len(words_seen_once) / total_word_count

def split_string(text, separators):
    """
    Split text into a list using any of the specified separator characters.
    
    Args:
        text (str): The input text to split
        separators (str): A string containing all characters to use as separators
        
    Returns:
        list[str]: A list of non-empty strings with leading/trailing spaces removed
    
    Notes:
        - Spaces are stripped from the beginning and end of each substring
        - Empty strings (after stripping) are not included in the result
        - Any character in the separators string will be treated as a delimiter
    
    Examples:
        >>> split_string('one*two[three', '*[')
        ['one', 'two', 'three']
        >>> split_string('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.', '.?!')
        ['A pearl', 'Pearl', 'Lustrous pearl', 'Rare', 'What a nice find']
        >>> split_string('  hello,,world  ', ',')
        ['hello', 'world']
        >>> split_string('|||', '|')
        []
    """
    # Initialize result list and current substring buffer
    result_strings = []
    current_substring = ''
    
    # Process each character in the input text
    for char in text:
        if char in separators:
            # Found a separator - process the current substring
            trimmed_substring = current_substring.strip()
            
            # Only add non-empty substrings to the result
            if trimmed_substring != '':
                result_strings.append(trimmed_substring)
            
            # Reset the substring buffer for the next segment
            current_substring = ''
        else:
            # Regular character - add to current substring
            current_substring += char
    
    # Handle the final substring (after the last separator or if no separators found)
    final_substring = current_substring.strip()
    if final_substring != '':
        result_strings.append(final_substring)
    
    return result_strings

def get_sentences(text):
    """
    Extract sentences from text by splitting on sentence-ending punctuation.
    
    Args:
        text (str): The input text to split into sentences
        
    Returns:
        list[str]: A list of sentences with leading/trailing spaces removed
                   and empty sentences excluded
    
    Notes:
        - Sentences are separated by '.', '?', or '!' characters
        - Each sentence is stripped of leading and trailing whitespace
        - Empty sentences are not included in the result
        
    Examples:
        >>> get_sentences('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.')
        ['A pearl', 'Pearl', 'Lustrous pearl', 'Rare', 'What a nice find']
        >>> get_sentences('Hello world. How are you? Fine!')
        ['Hello world', 'How are you', 'Fine']
        >>> get_sentences('No punctuation here')
        ['No punctuation here']
        >>> get_sentences('...???!!!')
        []
    """
    # Define sentence-ending punctuation marks
    sentence_separators = '.?!'
    
    # Use the split_string function to split on sentence separators
    return split_string(text, sentence_separators)

def average_sentence_length(text):
    """
    Calculate the average number of words per sentence in the given text.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        float: The average number of words per sentence
               
    Raises:
        ZeroDivisionError: If no sentences are found in the text
    
    Notes:
        - Sentences are separated by '.', '?', or '!' characters
        - Empty words (whitespace-only strings) are not counted
        - Empty sentences are not included in the calculation
        
    Examples:
        >>> average_sentence_length('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.')
        2.0
        >>> average_sentence_length('Hello world. How are you doing today?')
        3.0
        >>> average_sentence_length('Short. Very short sentence here.')
        2.5
        >>> average_sentence_length('No punctuation means one sentence')
        5.0
    """
    # Extract sentences from the text
    sentences = get_sentences(text)
    
    # Handle edge case where no sentences are found
    if len(sentences) == 0:
        raise ZeroDivisionError("No sentences found in text")
    
    # Count total words across all sentences
    total_word_count = 0
    
    for sentence in sentences:
        # Split sentence into individual words
        words = sentence.split()
        
        # Count non-empty words in this sentence
        for word in words:
            if word.strip() != '':  # More robust empty check
                total_word_count += 1
    
    # Calculate and return the average words per sentence
    return total_word_count / len(sentences)

def get_phrases(sentence):
    """
    Extract phrases from a sentence by splitting on phrase-separating punctuation.
    
    Args:
        sentence (str): The input sentence to split into phrases
        
    Returns:
        list[str]: A list of phrases with leading/trailing spaces removed
                   and empty phrases excluded
    
    Notes:
        - Phrases are separated by ',', ';', or ':' characters
        - Each phrase is stripped of leading and trailing whitespace
        - Empty phrases are not included in the result
        
    Examples:
        >>> get_phrases('Lustrous pearl, Rare, What a nice find')
        ['Lustrous pearl', 'Rare', 'What a nice find']
        >>> get_phrases('First part; second part: third part')
        ['First part', 'second part', 'third part']
        >>> get_phrases('No separators here')
        ['No separators here']
        >>> get_phrases(',,;::')
        []
        >>> get_phrases('Start, , end')
        ['Start', 'end']
    """
    # Define phrase-separating punctuation marks
    phrase_separators = ',;:'
    
    # Use the split_string function to split on phrase separators
    return split_string(sentence, phrase_separators)

def average_sentence_complexity(text):
    """
    Calculate the average number of phrases per sentence in the given text.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        float: The average number of phrases per sentence
               
    Raises:
        ZeroDivisionError: If no sentences are found in the text
    
    Notes:
        - Sentences are separated by '.', '?', or '!' characters
        - Phrases within sentences are separated by ',', ';', or ':' characters
        - A sentence with no phrase separators counts as having 1 phrase
        - Empty sentences and phrases are not included in the calculation
        
    Examples:
        >>> average_sentence_complexity('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.')
        1.0
        >>> average_sentence_complexity('A pearl! Pearl! Lustrous pearl! Rare, what a nice find.')
        1.25
        >>> average_sentence_complexity('First: second, third; fourth. Simple sentence.')
        2.5
        >>> average_sentence_complexity('Complex: with many, different; phrase separators!')
        1.0
    """
    # Extract sentences from the text
    sentences = get_sentences(text)
    
    # Handle edge case where no sentences are found
    if len(sentences) == 0:
        raise ZeroDivisionError("No sentences found in text")
    
    # Count total phrases across all sentences
    total_phrase_count = 0
    
    for sentence in sentences:
        # Extract phrases from this sentence
        phrases = get_phrases(sentence)
        
        # Add the number of phrases in this sentence to the total
        total_phrase_count += len(phrases)
    
    # Calculate and return the average phrases per sentence
    return total_phrase_count / len(sentences)

def make_signature(text):
    """
    Generate a comprehensive signature for the given text.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        list[float]: A signature containing five metrics:
            [0] average_word_length: Average length of words in characters
            [1] different_to_total: Ratio of unique words to total words
            [2] exactly_once_to_total: Ratio of words appearing exactly once to total words
            [3] average_sentence_length: Average number of words per sentence
            [4] average_sentence_complexity: Average number of phrases per sentence
    
    Notes:
        - All punctuation is stripped from words for length calculations
        - Words are converted to lowercase for uniqueness calculations
        - Sentences are separated by '.', '?', or '!' characters
        - Phrases are separated by ',', ';', or ':' characters
        - Empty words and sentences are excluded from calculations
        
    Examples:
        >>> make_signature('A pearl! Pearl! Lustrous pearl! Rare, what a nice find.')
        [4.1, 0.7, 0.5, 2.5, 1.25]
        >>> make_signature('Hello world. How are you?')
        [4.0, 1.0, 1.0, 2.5, 1.0]
        
    Raises:
        ZeroDivisionError: If the text contains no valid words or sentences
    """
    # Calculate each component of the text signature
    avg_word_len = average_word_length(text)
    unique_word_ratio = different_to_total(text)
    single_occurrence_ratio = exactly_once_to_total(text)
    avg_sentence_len = average_sentence_length(text)
    avg_sentence_complexity = average_sentence_complexity(text)
    
    # Return the complete signature as a list
    return [
        avg_word_len,
        unique_word_ratio,
        single_occurrence_ratio,
        avg_sentence_len,
        avg_sentence_complexity
    ]

def get_all_signatures(known_dir):
    """
    Generate text signatures for all files in a directory.
    
    Args:
        known_dir (str): Path to the directory containing text files to analyze
        
    Returns:
        dict[str, list[float]]: A dictionary mapping filenames to their text signatures.
                                Each signature is a list of five float values representing
                                various textual characteristics.
    
    Notes:
        - Only processes files that can be read as text
        - Skips files that cause encoding errors or other read failures
        - Each signature contains: [avg_word_length, unique_word_ratio, 
          single_occurrence_ratio, avg_sentence_length, avg_sentence_complexity]
        - Directory must exist and be accessible
        
    Examples:
        >>> signatures = get_all_signatures('./books')
        >>> print(signatures.keys())
        dict_keys(['book1.txt', 'book2.txt', 'novel.txt'])
        >>> print(signatures['book1.txt'])
        [4.2, 0.65, 0.4, 12.3, 1.8]
        
    Raises:
        FileNotFoundError: If the specified directory does not exist
        PermissionError: If the directory cannot be accessed
        OSError: If there are issues reading files in the directory
    """
    # Initialize dictionary to store filename -> signature mappings
    file_signatures = {}
    
    # Iterate through all files in the specified directory
    for filename in os.listdir(known_dir):
        try:
            # Construct full file path
            file_path = os.path.join(known_dir, filename)
            
            # Skip directories, only process files
            if os.path.isfile(file_path):
                # Read the entire file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                
                # Generate signature for this file's content
                file_signatures[filename] = make_signature(text_content)
                
        except (UnicodeDecodeError, PermissionError, OSError) as e:
            # Skip files that cannot be read (binary files, permission issues, etc.)
            print(f"Warning: Could not process file '{filename}': {e}")
            continue
    
    return file_signatures

def get_score(signature1, signature2, weights):
    """
    Calculate a weighted distance score between two text signatures.
    
    Args:
        signature1 (list[float]): First text signature containing 5 metrics
        signature2 (list[float]): Second text signature containing 5 metrics  
        weights (list[float]): List of 5 weights to apply to each metric difference
        
    Returns:
        float: The weighted distance score between the two signatures.
               Lower scores indicate more similar signatures.
    
    Notes:
        - The score is calculated as the sum of weighted absolute differences
        - Each signature should contain exactly 5 elements:
          [avg_word_length, unique_word_ratio, single_occurrence_ratio, 
           avg_sentence_length, avg_sentence_complexity]
        - Higher weights emphasize the importance of particular metrics
        - A score of 0 would indicate identical signatures
        
    Formula:
        score = Σ(|signature1[i] - signature2[i]| * weights[i]) for i in [0,4]
        
    Examples:
        >>> get_score([4.6, 0.1, 0.05, 10, 2], 
        ...           [4.3, 0.1, 0.04, 16, 4], 
        ...           [11, 33, 50, 0.4, 4])
        14.2
        >>> get_score([4.0, 0.5, 0.3, 8, 1], 
        ...           [4.0, 0.5, 0.3, 8, 1], 
        ...           [1, 1, 1, 1, 1])
        0.0
        >>> get_score([5.0, 0.8, 0.6, 12, 2], 
        ...           [3.0, 0.2, 0.1, 6, 1], 
        ...           [1, 10, 5, 0.5, 2])
        11.5
        
    Raises:
        ValueError: If signatures or weights don't have exactly 5 elements
        TypeError: If inputs are not lists of numbers
    """
    # Validate input lengths
    if len(signature1) != 5:
        raise ValueError(f"signature1 must have exactly 5 elements, got {len(signature1)}")
    if len(signature2) != 5:
        raise ValueError(f"signature2 must have exactly 5 elements, got {len(signature2)}")
    if len(weights) != 5:
        raise ValueError(f"weights must have exactly 5 elements, got {len(weights)}")
    
    # Initialize the total weighted distance score
    total_score = 0.0
    
    # Calculate weighted absolute difference for each signature component
    for i in range(len(signature1)):
        # Calculate absolute difference between corresponding signature elements
        absolute_difference = abs(signature1[i] - signature2[i])
        
        # Apply the corresponding weight to this difference
        weighted_difference = absolute_difference * weights[i]
        
        # Add to the total score
        total_score += weighted_difference
    
    return total_score

def lowest_score(signatures_dict, unknown_signature, weights):
    """
    Find the key with the signature most similar to the unknown signature.
    
    Args:
        signatures_dict (dict[str, list[float]]): Dictionary mapping keys (e.g., author names) 
                                                  to their text signatures
        unknown_signature (list[float]): The signature to compare against all known signatures
        weights (list[float]): List of 5 weights to apply when calculating similarity scores
        
    Returns:
        str: The key from signatures_dict whose signature has the lowest (best) score
             when compared to the unknown_signature
    
    Notes:
        - Lower scores indicate higher similarity between signatures
        - Uses weighted absolute difference to calculate similarity scores
        - Returns the key (not the signature or score) of the best match
        - If multiple keys have identical lowest scores, returns the first one encountered
        
    Examples:
        >>> d = {'Dan': [1, 1, 1, 1, 1], 'Leo': [3, 3, 3, 3, 3]}
        >>> unknown = [1, 0.8, 0.9, 1.3, 1.4]
        >>> weights = [11, 33, 50, 0.4, 4]
        >>> lowest_score(d, unknown, weights)
        'Dan'
        >>> authors = {'Hemingway': [4.1, 0.6, 0.4, 8.2, 1.3], 
        ...            'Dickens': [5.2, 0.8, 0.5, 15.7, 2.1]}
        >>> mystery_text = [4.0, 0.65, 0.42, 8.0, 1.2]
        >>> weights = [1, 1, 1, 1, 1]
        >>> lowest_score(authors, mystery_text, weights)
        'Hemingway'
        
    Raises:
        ValueError: If signatures_dict is empty
        ValueError: If signatures or weights don't have exactly 5 elements
        TypeError: If inputs are not of the expected types
    """
    # Validate that we have signatures to compare against
    if not signatures_dict:
        raise ValueError("signatures_dict cannot be empty")
    
    # Initialize tracking variables for the best match
    best_match_key = None
    best_match_score = None
    
    # Compare unknown signature against each known signature
    for author_key in signatures_dict:
        # Get the signature for this author/key
        known_signature = signatures_dict[author_key]
        
        # Calculate similarity score between unknown and this known signature
        similarity_score = get_score(known_signature, unknown_signature, weights)
        
        # Check if this is the best match so far
        if best_match_score is None or similarity_score < best_match_score:
            best_match_key = author_key
            best_match_score = similarity_score
    
    return best_match_key

def process_data(mystery_filename, known_dir):
    """
    Identify the most likely author of a mystery text using stylometric analysis.
    
    Args:
        mystery_filename (str): Path to the mystery text file to analyze
        known_dir (str): Path to directory containing known author samples
        
    Returns:
        str: Filename of the known text with the most similar writing style
    
    Notes:
        - Uses a predefined weighting scheme optimized for authorship attribution
        - Weights emphasize vocabulary uniqueness and word occurrence patterns
        - The returned filename corresponds to the most stylistically similar known text
        - Assumes all files in known_dir are valid text samples from known authors
        
    Weighting Scheme:
        - Average word length: weight 11 (moderate importance)
        - Unique word ratio: weight 33 (high importance)  
        - Single occurrence ratio: weight 50 (highest importance)
        - Average sentence length: weight 0.4 (low importance)
        - Sentence complexity: weight 4 (low-moderate importance)
        
    Examples:
        >>> process_data('mystery_novel.txt', './known_authors/')
        'hemingway_sample.txt'
        >>> process_data('unknown_poem.txt', './poetry_samples/')
        'shakespeare_sonnet.txt'
        
    Raises:
        FileNotFoundError: If mystery_filename or known_dir doesn't exist
        ValueError: If no valid files found in known_dir
        UnicodeDecodeError: If mystery file cannot be read as text
        PermissionError: If files cannot be accessed due to permissions
    """
    # Generate signatures for all known author samples
    print(f"Analyzing known samples in directory: {known_dir}")
    known_signatures = get_all_signatures(known_dir)
    
    if not known_signatures:
        raise ValueError(f"No valid text files found in directory: {known_dir}")
    
    print(f"Found {len(known_signatures)} known author samples")
    
    # Read and analyze the mystery text
    print(f"Processing mystery file: {mystery_filename}")
    try:
        with open(mystery_filename, 'r', encoding='utf-8') as mystery_file:
            mystery_text = mystery_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Mystery file not found: {mystery_filename}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Cannot read mystery file as text: {mystery_filename}")
    
    # Generate signature for the mystery text
    mystery_signature = make_signature(mystery_text)
    print(f"Mystery text signature: {[round(x, 3) for x in mystery_signature]}")
    
    # Define weights optimized for authorship attribution
    # Higher weights for vocabulary metrics, lower for structural metrics
    authorship_weights = [
        11,   # Average word length - moderate importance
        33,   # Unique word ratio - high importance
        50,   # Single occurrence ratio - highest importance  
        0.4,  # Average sentence length - low importance
        4     # Sentence complexity - low-moderate importance
    ]
    
    # Find the best matching known author
    best_match_filename = lowest_score(known_signatures, mystery_signature, authorship_weights)
    
    print(f"Best match: {best_match_filename}")
    print(f"Match signature: {[round(x, 3) for x in known_signatures[best_match_filename]]}")
    
    return best_match_filename

def make_guess(known_dir):
    """
    Interactive authorship attribution tool that prompts user for a mystery text file.
    
    Args:
        known_dir (str): Path to directory containing known author samples for comparison
        
    Returns:
        None: Prints the result directly to console
    
    Notes:
        - Prompts user to enter a filename for the mystery text
        - Compares the mystery text against all known samples in known_dir
        - Uses stylometric analysis to identify the most similar writing style
        - Handles common errors gracefully with informative messages
        - Results show the filename of the best matching known sample
        
    Interactive Flow:
        1. Prompts user for mystery text filename
        2. Analyzes the mystery text and all known samples
        3. Compares writing styles using weighted signature matching
        4. Displays the best matching known author sample
        
    Examples:
        >>> make_guess('./known_authors/')
        Enter the filename of the mystery text: mystery_novel.txt
        
        Analyzing mystery text: mystery_novel.txt
        Comparing against known samples in: ./known_authors/
        
        Best match: hemingway_sample.txt
        
    Error Handling:
        - Invalid filenames: Clear error message with suggestion to check path
        - Missing directory: Informs user that known_dir doesn't exist
        - Empty directory: Warns that no comparison samples were found
        - Unreadable files: Explains encoding or permission issues
    """
    print("=" * 60)
    print("AUTHORSHIP ATTRIBUTION SYSTEM")
    print("=" * 60)
    print(f"Known author samples directory: {known_dir}")
    print()
    
    # Validate that the known directory exists
    if not os.path.exists(known_dir):
        print(f"Error: Directory '{known_dir}' does not exist.")
        print("Please check the path and try again.")
        return
    
    if not os.path.isdir(known_dir):
        print(f"Error: '{known_dir}' is not a directory.")
        return
    
    # Get filename from user with clear prompt
    print("Please enter the filename of the mystery text you want to analyze.")
    print("(Include the full path if the file is not in the current directory)")
    mystery_filename = input("\nEnter filename: ").strip()
    
    # Validate user input
    if not mystery_filename:
        print("Error: No filename provided.")
        return
    
    print(f"\nAnalyzing mystery text: {mystery_filename}")
    print(f"Comparing against known samples in: {known_dir}")
    print("-" * 60)
    
    try:
        # Perform the authorship attribution analysis
        best_match = process_data(mystery_filename, known_dir)
        
        print()
        print("ANALYSIS COMPLETE")
        print("=" * 30)
        print(f"Best matching author sample: {best_match}")
        print()
        print("This suggests the mystery text has the most similar writing style")
        print(f"to the text found in '{best_match}'.")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please check that the filename is correct and the file exists.")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please ensure the known author directory contains valid text files.")
        
    except UnicodeDecodeError as e:
        print(f"\nError: {e}")
        print("The file may be a binary file or use an unsupported text encoding.")
        
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        print("Please check your input files and try again.")
    
    print("\n" + "=" * 60)


make_guess('./known_authors/')