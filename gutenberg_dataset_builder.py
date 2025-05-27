import os
import re
import requests
import time
from pathlib import Path
from urllib.parse import urljoin
import zipfile
import io

class GutenbergDatasetBuilder:
    """Build a comprehensive authorship attribution dataset from Project Gutenberg."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.known_authors_dir = self.data_dir / "known_authors"
        self.mystery_texts_dir = self.data_dir / "mystery_texts"
        self.raw_texts_dir = self.data_dir / "raw_texts"
        
        # Create directories
        for dir_path in [self.known_authors_dir, self.mystery_texts_dir, self.raw_texts_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def download_text(self, gutenberg_id, title, author, delay=1):
        """Download a single text from Project Gutenberg."""
        
        # Try multiple URL formats
        urls = [
            f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt",
            f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}.txt",
            f"https://www.gutenberg.org/ebooks/{gutenberg_id}.txt.utf-8"
        ]
        
        for url in urls:
            try:
                print(f"Trying to download: {title} by {author} from {url}")
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    text_content = response.text
                    
                    # Clean the text
                    cleaned_text = self.clean_gutenberg_text(text_content)
                    
                    if len(cleaned_text) > 1000:  # Ensure we have substantial content
                        # Save raw text
                        safe_title = self.make_safe_filename(title)
                        safe_author = self.make_safe_filename(author)
                        
                        raw_filename = self.raw_texts_dir / f"{safe_author}_{safe_title}_{gutenberg_id}.txt"
                        with open(raw_filename, 'w', encoding='utf-8') as f:
                            f.write(cleaned_text)
                        
                        print(f"✓ Downloaded: {title} by {author} ({len(cleaned_text)} characters)")
                        time.sleep(delay)  # Be respectful to the server
                        return cleaned_text
                
            except requests.exceptions.RequestException as e:
                print(f"✗ Failed to download from {url}: {e}")
                continue
        
        print(f"✗ Could not download: {title} by {author}")
        return None
    
    def clean_gutenberg_text(self, text):
        """Clean Project Gutenberg text by removing headers/footers."""
        
        # Find start of actual text (after Gutenberg header)
        start_patterns = [
            r"\*\*\* START OF TH[EI]S? PROJECT GUTENBERG.*?\*\*\*",
            r"\*\*\* START OF THE PROJECT GUTENBERG.*?\*\*\*",
            r"START OF TH[EI]S PROJECT GUTENBERG",
            r"CHAPTER I\b",
            r"Chapter 1\b",
            r"BOOK I\b",
            r"PART I\b"
        ]
        
        start_pos = 0
        for pattern in start_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                start_pos = match.end()
                break
        
        # Find end of actual text (before Gutenberg footer)
        end_patterns = [
            r"\*\*\* END OF TH[EI]S? PROJECT GUTENBERG.*?\*\*\*",
            r"\*\*\* END OF THE PROJECT GUTENBERG.*?\*\*\*",
            r"END OF TH[EI]S PROJECT GUTENBERG",
            r"End of.*?Project Gutenberg"
        ]
        
        end_pos = len(text)
        for pattern in end_patterns:
            match = re.search(pattern, text[start_pos:], re.IGNORECASE | re.DOTALL)
            if match:
                end_pos = start_pos + match.start()
                break
        
        cleaned_text = text[start_pos:end_pos].strip()
        
        # Remove excessive whitespace
        cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_text)
        cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
        
        return cleaned_text
    
    def make_safe_filename(self, text):
        """Convert text to safe filename."""
        # Remove/replace problematic characters
        safe = re.sub(r'[^\w\s-]', '', text)
        safe = re.sub(r'[-\s]+', '_', safe)
        return safe[:50]  # Limit length
    
    def create_author_samples(self, author_texts, min_sample_size=5000, max_samples=5):
        """Create multiple samples per author for better training data."""
        
        author_samples = {}
        
        for author, texts in author_texts.items():
            # Combine all texts for this author
            all_text = ' '.join(texts)
            
            if len(all_text) < min_sample_size:
                print(f"⚠️  {author}: Not enough text ({len(all_text)} chars)")
                continue
            
            # Create multiple samples by splitting the text
            samples = []
            words = all_text.split()
            
            # Calculate words per sample
            words_per_sample = len(words) // max_samples
            if words_per_sample < 1000:  # Ensure each sample has enough content
                words_per_sample = max(1000, len(words) // 2)
            
            for i in range(0, min(max_samples, len(words) // words_per_sample)):
                start_idx = i * words_per_sample
                end_idx = start_idx + words_per_sample
                sample_text = ' '.join(words[start_idx:end_idx])
                
                if len(sample_text) >= min_sample_size:
                    samples.append(sample_text)
            
            if samples:
                author_samples[author] = samples
                print(f"✓ {author}: Created {len(samples)} samples")
        
        return author_samples
    
    def save_dataset(self, author_samples, test_split=0.2):
        """Save the dataset to known_authors and mystery_texts directories."""
        
        for author, samples in author_samples.items():
            safe_author = self.make_safe_filename(author)
            
            # Determine how many samples to use for testing
            num_test_samples = max(1, int(len(samples) * test_split))
            num_train_samples = len(samples) - num_test_samples
            
            # Save training samples to known_authors
            for i, sample in enumerate(samples[:num_train_samples]):
                filename = self.known_authors_dir / f"{safe_author}_{i+1}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(sample)
            
            # Save test samples to mystery_texts (for evaluation)
            for i, sample in enumerate(samples[num_train_samples:]):
                filename = self.mystery_texts_dir / f"mystery_{safe_author}_{i+1}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(sample)
            
            print(f"✓ {author}: {num_train_samples} training, {num_test_samples} mystery samples")

def build_classic_authors_dataset():
    """Build a dataset with classic authors from Project Gutenberg."""
    
    # Curated list of classic authors with their notable works
    classic_authors = {
        "Jane Austen": [
            (1342, "Pride and Prejudice"),
            (158, "Emma"),
            (161, "Sense and Sensibility"),
            (105, "Persuasion"),
            (141, "Mansfield Park"),
            (121, "Northanger Abbey")
        ],
        "Charles Dickens": [
            (98, "A Tale of Two Cities"),
            (1400, "Great Expectations"),
            (766, "David Copperfield"),
            (730, "Oliver Twist"),
            (786, "The Pickwick Papers"),
            (644, "A Christmas Carol")
        ],
        "Mark Twain": [
            (74, "The Adventures of Tom Sawyer"),
            (76, "Adventures of Huckleberry Finn"),
            (102, "The Prince and The Pauper"),
            (86, "A Connecticut Yankee in King Arthur's Court"),
            (119, "The Mysterious Stranger"),
            (3176, "The Gilded Age")
        ],
        "Arthur Conan Doyle": [
            (1661, "The Adventures of Sherlock Holmes"),
            (834, "The Memoirs of Sherlock Holmes"),
            (2097, "The Hound of the Baskervilles"),
            (108, "The Return of Sherlock Holmes"),
            (2852, "His Last Bow"),
            (5231, "The Case Book of Sherlock Holmes")
        ],
        "Lewis Carroll": [
            (11, "Alice's Adventures in Wonderland"),
            (12, "Through the Looking-Glass"),
            (13, "The Hunting of the Snark"),
            (28885, "Sylvie and Bruno"),
            (29042, "Sylvie and Bruno Concluded")
        ],
        "Oscar Wilde": [
            (174, "The Picture of Dorian Gray"),
            (14522, "The Importance of Being Earnest"),
            (902, "Lady Windermere's Fan"),
            (854, "An Ideal Husband"),
            (773, "A Woman of No Importance")
        ],
        "H.G. Wells": [
            (35, "The Time Machine"),
            (36, "The War of the Worlds"),
            (5230, "The Invisible Man"),
            (159, "The Island of Dr. Moreau"),
            (718, "The Food of the Gods"),
            (1743, "The First Men in the Moon")
        ],
        "Edgar Allan Poe": [
            (2147, "The Raven"),
            (932, "The Works of Edgar Allan Poe"),
            (25525, "The Complete Poetical Works"),
            (2148, "The Cask of Amontillado"),
            (2149, "The Fall of the House of Usher")
        ],
        "Herman Melville": [
            (2701, "Moby Dick"),
            (11231, "Bartleby the Scrivener"),
            (10712, "The Confidence-Man"),
            (1900, "Typee"),
            (1892, "Omoo")
        ],
        "Bram Stoker": [
            (345, "Dracula"),
            (5832, "The Lair of the White Worm"),
            (30360, "The Jewel of Seven Stars"),
            (1279, "The Man")
        ]
    }
    
    builder = GutenbergDatasetBuilder()
    author_texts = {}
    
    print("📚 Building Classic Authors Dataset from Project Gutenberg")
    print("=" * 60)
    
    # Download texts for each author
    for author, works in classic_authors.items():
        print(f"\n📖 Downloading works by {author}:")
        author_texts[author] = []
        
        for gutenberg_id, title in works:
            text = builder.download_text(gutenberg_id, title, author)
            if text:
                author_texts[author].append(text)
    
    # Create author samples
    print(f"\n🔧 Creating author samples...")
    author_samples = builder.create_author_samples(author_texts)
    
    # Save dataset
    print(f"\n💾 Saving dataset...")
    builder.save_dataset(author_samples)
    
    # Print summary
    print(f"\n📊 Dataset Summary:")
    print("=" * 40)
    
    known_count = len(list(builder.known_authors_dir.glob("*.txt")))
    mystery_count = len(list(builder.mystery_texts_dir.glob("*.txt")))
    
    print(f"Known author samples: {known_count}")
    print(f"Mystery text samples: {mystery_count}")
    print(f"Total authors: {len(author_samples)}")
    print(f"\nDataset saved to:")
    print(f"  - Known authors: {builder.known_authors_dir}")
    print(f"  - Mystery texts: {builder.mystery_texts_dir}")
    print(f"  - Raw texts: {builder.raw_texts_dir}")
    
    return builder, author_samples

# ===================================================================
# Additional Dataset Builders
# ===================================================================

def build_modern_authors_dataset():
    """Build dataset with public domain modern authors."""
    
    modern_authors = {
        "Virginia Woolf": [
            (4452, "Mrs. Dalloway"),
            (5670, "Night and Day"),
            (144, "A Room of One's Own"),
            (2529, "To the Lighthouse")
        ],
        "James Joyce": [
            (4300, "Dubliners"),
            (2814, "A Portrait of the Artist as a Young Man"),
            (4217, "Chamber Music")
        ],
        "D.H. Lawrence": [
            (4240, "Sons and Lovers"),
            (1540, "Women in Love"),
            (4239, "The Rainbow")
        ],
        "Joseph Conrad": [
            (219, "Heart of Darkness"),
            (974, "Lord Jim"),
            (526, "The Secret Agent"),
            (154, "An Outcast of the Islands")
        ],
        "Jack London": [
            (910, "The Call of the Wild"),
            (1056, "White Fang"),
            (1056, "The Sea-Wolf"),
            (5737, "Martin Eden")
        ]
    }
    
    builder = GutenbergDatasetBuilder("data_modern")
    # Similar implementation as classic authors...
    
def build_poetry_dataset():
    """Build specialized dataset for poetry analysis."""
    
    poets = {
        "William Shakespeare": [
            (1041, "The Sonnets"),
            (1794, "Romeo and Juliet"),
            (1524, "Hamlet"),
            (1533, "Macbeth")
        ],
        "Walt Whitman": [
            (1322, "Leaves of Grass"),
            (8819, "Democratic Vistas"),
            (4856, "Specimen Days")
        ],
        "Emily Dickinson": [
            (12242, "Poems"),
            (2678, "Further Poems"),
            (2679, "The Single Hound")
        ],
        "Robert Frost": [
            (59824, "North of Boston"),
            (59825, "Mountain Interval"),
            (59826, "New Hampshire")
        ]
    }
    
    builder = GutenbergDatasetBuilder("data_poetry")
    # Similar implementation...

# ===================================================================
# Dataset Testing and Validation
# ===================================================================

def test_dataset_quality(data_dir="data"):
    """Test the quality of the generated dataset."""
    
    from src.main import analyze_file
    
    known_dir = Path(data_dir) / "known_authors"
    mystery_dir = Path(data_dir) / "mystery_texts"
    
    print("🧪 Testing Dataset Quality")
    print("=" * 40)
    
    # Test a few mystery texts
    mystery_files = list(mystery_dir.glob("*.txt"))[:10]  # Test first 10
    
    correct = 0
    total = 0
    
    for mystery_file in mystery_files:
        # Extract expected author from filename
        filename = mystery_file.stem
        if "mystery_" in filename:
            expected_author = filename.replace("mystery_", "").split("_")[0]
            
            try:
                result = analyze_file(str(mystery_file), str(known_dir), verbose=False)
                predicted_author = result.split("_")[0] if result else "unknown"
                
                if expected_author.lower() in predicted_author.lower():
                    correct += 1
                    status = "✓"
                else:
                    status = "✗"
                
                print(f"{status} {mystery_file.name}: Expected {expected_author}, Got {predicted_author}")
                total += 1
                
            except Exception as e:
                print(f"✗ Error testing {mystery_file.name}: {e}")
    
    if total > 0:
        accuracy = (correct / total) * 100
        print(f"\n📊 Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    
    return correct, total

# ===================================================================
# Main Execution
# ===================================================================

if __name__ == "__main__":
    print("🚀 Project Gutenberg Authorship Attribution Dataset Builder")
    print("=" * 60)
    
    # Build the classic authors dataset
    builder, author_samples = build_classic_authors_dataset()
    
    # Test dataset quality
    print(f"\n" + "=" * 60)
    test_dataset_quality()
    
    print(f"\n✅ Dataset building complete!")
    print(f"📁 You can now run your authorship attribution system with:")
    print(f"   python run.py")
    print(f"   # Or test with mystery texts:")
    print(f"   python run.py data/mystery_texts/mystery_Jane_Austen_1.txt")