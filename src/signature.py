from .text_analysis import (
    average_word_length, different_to_total, exactly_once_to_total,
    average_sentence_length, average_sentence_complexity
)

def make_signature(text):
    """
    Generate text signature with 5 metrics:
    [avg_word_length, unique_ratio, single_occurrence_ratio, avg_sentence_length, complexity]
    """
    return [
        average_word_length(text),
        different_to_total(text),
        exactly_once_to_total(text),
        average_sentence_length(text),
        average_sentence_complexity(text)
    ]

def get_score(signature1, signature2, weights):
    """Calculate weighted distance score between two signatures. Lower = more similar."""
    if len(signature1) != 5 or len(signature2) != 5 or len(weights) != 5:
        raise ValueError("All signatures and weights must have exactly 5 elements")
    
    total_score = 0.0
    for i in range(5):
        total_score += abs(signature1[i] - signature2[i]) * weights[i]
    
    return total_score

def lowest_score(signatures_dict, unknown_signature, weights):
    """Find the key with signature most similar to unknown_signature."""
    if not signatures_dict:
        raise ValueError("signatures_dict cannot be empty")
    
    best_match_key = None
    best_match_score = None
    
    for author_key in signatures_dict:
        similarity_score = get_score(signatures_dict[author_key], unknown_signature, weights)
        
        if best_match_score is None or similarity_score < best_match_score:
            best_match_key = author_key
            best_match_score = similarity_score
    
    return best_match_key