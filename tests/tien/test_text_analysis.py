import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tien.text_analysis import (
    clean_word,
    split_string,
    get_sentences,
    get_phrases,
    average_word_length,
    different_to_total,
    exactly_once_to_total,
    average_sentence_length,
    average_sentence_complexity,
)

class TestTextAnalysis(unittest.TestCase):
    
    def test_clean_word(self):
        self.assertEqual(clean_word('Pearl!'), 'pearl')
        self.assertEqual(clean_word('card-board'), 'card-board')
        self.assertEqual(clean_word('...Hello...'), 'hello')
        self.assertEqual(clean_word('UPPER'), 'upper')
        self.assertEqual(clean_word(''), '')
    
    def test_split_string(self):
        result = split_string('one*two[three', '*[')
        self.assertEqual(result, ['one', 'two', 'three'])
        
        result = split_string('A pearl! Pearl! Lustrous pearl! Rare. What a nice find.', '.?!')
        expected = ['A pearl', 'Pearl', 'Lustrous pearl', 'Rare', 'What a nice find']
        self.assertEqual(result, expected)
        
        result = split_string('  hello,,world  ', ',')
        self.assertEqual(result, ['hello', 'world'])
        
        result = split_string('|||', '|')
        self.assertEqual(result, [])
    
    def test_get_sentences(self):
        text = 'Hello world. How are you? Fine!'
        result = get_sentences(text)
        self.assertEqual(result, ['Hello world', 'How are you', 'Fine'])
    
    def test_get_phrases(self):
        text = 'First part; second part: third part'
        result = get_phrases(text)
        self.assertEqual(result, ['First part', 'second part', 'third part'])
    
    def test_average_word_length(self):
        text = 'hello world'
        result = average_word_length(text)
        self.assertEqual(result, 5.0)
        
        with self.assertRaises(ZeroDivisionError):
            average_word_length('...')
    
    def test_different_to_total(self):
        text = 'hello hello world'
        result = different_to_total(text)
        self.assertAlmostEqual(result, 2/3, places=3)
        
        text = 'cat dog bird'
        result = different_to_total(text)
        self.assertEqual(result, 1.0)
    
    def test_exactly_once_to_total(self):
        text = 'hello hello world'
        result = exactly_once_to_total(text)
        self.assertAlmostEqual(result, 1/3, places=3)
        
        text = 'the the the the'
        result = exactly_once_to_total(text)
        self.assertEqual(result, 0.0)
    
    def test_average_sentence_length(self):
        text = 'Hello world. How are you?'
        result = average_sentence_length(text)
        self.assertEqual(result, 2.5)
    
    def test_average_sentence_complexity(self):
        text = 'Hello world. How are you, friend?'
        result = average_sentence_complexity(text)
        self.assertEqual(result, 1.5)
