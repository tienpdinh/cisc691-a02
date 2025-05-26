import string

def clean_word(word):
    """Clean word: lowercase and strip end punctuation."""
    word = word.lower()
    word = word.strip(string.punctuation)
    return word

def split_string(text, separators):
    """Split text using any of the separator characters."""
    result_strings = []
    current_substring = ''
    
    for char in text:
        if char in separators:
            trimmed_substring = current_substring.strip()
            if trimmed_substring != '':
                result_strings.append(trimmed_substring)
            current_substring = ''
        else:
            current_substring += char
    
    final_substring = current_substring.strip()
    if final_substring != '':
        result_strings.append(final_substring)
    
    return result_strings

def get_sentences(text):
    """Extract sentences by splitting on '.?!' punctuation."""
    return split_string(text, '.?!')

def get_phrases(sentence):
    """Extract phrases by splitting on ',;:' punctuation."""
    return split_string(sentence, ',;:')

def average_word_length(text):
    """Calculate average word length in characters."""
    words = text.split()
    total_length = 0
    word_count = 0
    
    for word in words:
        cleaned_word = clean_word(word)
        if cleaned_word != '':
            total_length += len(cleaned_word)
            word_count += 1
    
    if word_count == 0:
        raise ZeroDivisionError("No valid words found in text")
    
    return total_length / word_count

def different_to_total(text):
    """Calculate ratio of unique words to total words."""
    words = text.split()
    total_word_count = 0
    unique_words = set()
    
    for word in words:
        cleaned_word = clean_word(word)
        if cleaned_word != '':
            total_word_count += 1
            unique_words.add(cleaned_word)
    
    if total_word_count == 0:
        raise ZeroDivisionError("No valid words found in text")
    
    return len(unique_words) / total_word_count

def exactly_once_to_total(text):
    """Calculate ratio of words appearing exactly once to total words."""
    words = text.split()
    total_word_count = 0
    seen_words = set()
    words_seen_once = set()
    
    for word in words:
        cleaned_word = clean_word(word)
        if cleaned_word != '':
            total_word_count += 1
            
            if cleaned_word in seen_words:
                words_seen_once.discard(cleaned_word)
            else:
                seen_words.add(cleaned_word)
                words_seen_once.add(cleaned_word)
    
    if total_word_count == 0:
        raise ZeroDivisionError("No valid words found in text")
    
    return len(words_seen_once) / total_word_count

def average_sentence_length(text):
    """Calculate average number of words per sentence."""
    sentences = get_sentences(text)
    
    if len(sentences) == 0:
        raise ZeroDivisionError("No sentences found in text")
    
    total_word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            if word.strip() != '':
                total_word_count += 1
    
    return total_word_count / len(sentences)

def average_sentence_complexity(text):
    """Calculate average number of phrases per sentence."""
    sentences = get_sentences(text)
    
    if len(sentences) == 0:
        raise ZeroDivisionError("No sentences found in text")
    
    total_phrase_count = 0
    
    for sentence in sentences:
        phrases = get_phrases(sentence)
        total_phrase_count += len(phrases)
    
    return total_phrase_count / len(sentences)