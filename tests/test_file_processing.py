import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.file_processing import get_all_signatures, process_data

class TestFileProcessing(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files
        test_files = {
            'author1.txt': 'Hello world. This is a test. How are you?',
            'author2.txt': 'The quick brown fox jumps over the lazy dog. Simple sentence here.',
            'mystery.txt': 'Hello there. This is another test. What do you think?'
        }
        
        for filename, content in test_files.items():
            with open(os.path.join(self.temp_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_all_signatures(self):
        signatures = get_all_signatures(self.temp_dir)
        
        self.assertIn('author1.txt', signatures)
        self.assertIn('author2.txt', signatures)
        self.assertEqual(len(signatures['author1.txt']), 5)
    
    def test_process_data(self):
        mystery_path = os.path.join(self.temp_dir, 'mystery.txt')
        
        # Create known authors directory
        known_dir = os.path.join(self.temp_dir, 'known')
        os.makedirs(known_dir)
        
        # Move author files to known directory
        for filename in ['author1.txt', 'author2.txt']:
            old_path = os.path.join(self.temp_dir, filename)
            new_path = os.path.join(known_dir, filename)
            os.rename(old_path, new_path)
        
        result = process_data(mystery_path, known_dir)
        self.assertIn(result, ['author1.txt', 'author2.txt'])
        
        with self.assertRaises(FileNotFoundError):
            process_data('nonexistent.txt', known_dir)