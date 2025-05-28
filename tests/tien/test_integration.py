import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tien.main import analyze_file

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
        # Create realistic test data
        known_authors = {
            'hemingway.txt': '''The sun rose slowly over the hills. 
                              It was a beautiful morning. The old man sat by the sea.
                              He watched the waves. Simple thoughts filled his mind.''',
            
            'dickens.txt': '''It was the best of times, it was the worst of times.
                            The city bustled with activity, noise, and confusion.
                            People hurried through the streets with great purpose and determination.
                            The complexity of life overwhelmed many residents.'''
        }
        
        self.mystery_text = '''The day began quietly. An old fisherman prepared his boat.
                              The sea called to him. His thoughts were clear and simple.
                              Peace filled the morning air.'''
        
        # Create known authors directory
        self.known_dir = os.path.join(self.temp_dir, 'known_authors')
        os.makedirs(self.known_dir)
        
        for filename, content in known_authors.items():
            with open(os.path.join(self.known_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create mystery file
        self.mystery_file = os.path.join(self.temp_dir, 'mystery.txt')
        with open(self.mystery_file, 'w', encoding='utf-8') as f:
            f.write(self.mystery_text)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_analysis_pipeline(self):
        result = analyze_file(self.mystery_file, self.known_dir, verbose=False)
        self.assertIn(result, ['hemingway.txt', 'dickens.txt'])
        
        # Given the simple, short sentences, should match Hemingway style better
        self.assertEqual(result, 'hemingway.txt')
