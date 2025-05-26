import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.signature import make_signature, get_score, lowest_score

class TestSignature(unittest.TestCase):
    
    def test_make_signature(self):
        text = 'Hello world. How are you?'
        signature = make_signature(text)
        self.assertEqual(len(signature), 5)
        self.assertIsInstance(signature[0], float)
    
    def test_get_score(self):
        sig1 = [4.0, 0.5, 0.3, 8, 1]
        sig2 = [4.0, 0.5, 0.3, 8, 1]
        weights = [1, 1, 1, 1, 1]
        
        score = get_score(sig1, sig2, weights)
        self.assertEqual(score, 0.0)
        
        sig3 = [5.0, 0.8, 0.6, 12, 2]
        score = get_score(sig1, sig3, weights)
        self.assertGreater(score, 0)
        
        with self.assertRaises(ValueError):
            get_score([1, 2, 3], sig2, weights)
    
    def test_lowest_score(self):
        signatures = {
            'author1': [4.0, 0.5, 0.3, 8, 1],
            'author2': [6.0, 0.8, 0.7, 15, 3]
        }
        unknown = [4.1, 0.52, 0.31, 8.2, 1.1]
        weights = [1, 1, 1, 1, 1]
        
        result = lowest_score(signatures, unknown, weights)
        self.assertEqual(result, 'author1')
        
        with self.assertRaises(ValueError):
            lowest_score({}, unknown, weights)