[![Tests](https://github.com/tienpdinh/cisc691/workflows/Tests%20and%20Coverage/badge.svg)](https://github.com/tienpdinh/cisc691/actions)
[![codecov](https://codecov.io/gh/tienpdinh/cisc691/graph/badge.svg?token=3MSAR36YQ1)](https://codecov.io/gh/tienpdinh/cisc691)

# Authorship Attribution System

A stylometric analysis tool for identifying authors based on writing style. This project includes individual implementations by Kenneth and Tien, as well as an enhanced group implementation.

---

## Quick Start

```bash
# Interactive mode
python [run.py](http://_vscodecontentref_/1)

# Analyze specific file
python [run.py](http://_vscodecontentref_/2) data/mystery_texts/unknown.txt

# Run tests
python [run_tests.py](http://_vscodecontentref_/3)

# Run tests with coverage
pip install coverage
coverage run [run_tests.py](http://_vscodecontentref_/4)
coverage report
coverage html  # Creates htmlcov/index.html
```

## Project Structure

```
authorship_attribution/
├── src/                     # Source code
│   ├── kenneth/             # Kenneth's implementation
│   ├── tien/                # Tien's implementation
│   └── enhanced/            # Enhanced group implementation
├── tests/                   # Test suite
│   ├── kenneth/             # Tests for Kenneth's implementation
│   ├── tien/                # Tests for Tien's implementation
│   └── enhanced/            # Tests for enhanced implementation
├── data/
│   ├── known_authors/       # Known author samples
│   └── mystery_texts/       # Mystery texts
├── run.py                   # Entry point
├── run_tests.py             # Test runner
└── README.md
```

## Testing

The project includes comprehensive test coverage:

- **Unit tests**: Test individual functions in isolation
- **Integration tests**: Test complete workflows
- **File I/O tests**: Test file processing with temporary files
- **Error handling tests**: Verify proper exception handling

Run all tests:
```bash
python run_tests.py
```

Run specific test categories:
```bash
python run_tests.py TestTextAnalysis    # Text analysis functions
python run_tests.py TestSignature       # Signature generation
python run_tests.py TestIntegration     # Full pipeline tests
```

## How It Works

Analyzes 5 stylometric features in the indvidual versions:
- Average word length
- Vocabulary diversity  
- Hapax legomena ratio
- Average sentence length
- Sentence complexity

Additional 2 features in the enhanced version:
- Punctuation density
- Stopword ratio

Compares signatures using weighted distance metrics to find best match.

## Data Setup

1. Place known author samples in `data/known_authors/`
2. Place mystery texts in `data/mystery_texts/`
3. Use UTF-8 encoded plain text files