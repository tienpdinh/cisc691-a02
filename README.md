[![Tests](https://github.com/tienpdinh/cisc691/workflows/Tests%20and%20Coverage/badge.svg)](https://github.com/tienpdinh/cisc691/actions)
[![codecov](https://codecov.io/gh/tienpdinh/cisc691/branch/main/graph/badge.svg)](https://codecov.io/gh/tienpdinh/cisc691)
![Coverage](https://img.shields.io/badge/coverage-82%25-yellowgreen)

# Authorship Attribution System

Stylometric analysis tool for identifying authors based on writing style.

## Quick Start

```bash
# Interactive mode
python run.py

# Analyze specific file
python run.py data/mystery_texts/unknown.txt

# Quiet mode for scripting
python run.py mystery.txt --quiet
```

## Project Structure

```
authorship_attribution/
├── src/                     # Source code
├── data/
│   ├── known_authors/       # Known author samples
│   └── mystery_texts/       # Mystery texts
├── run.py                   # Entry point
└── README.md
```

## How It Works

Analyzes 5 stylometric features:
- Average word length
- Vocabulary diversity  
- Hapax legomena ratio
- Average sentence length
- Sentence complexity

Compares signatures using weighted distance metrics to find best match.

## Data Setup

1. Place known author samples in `data/known_authors/`
2. Place mystery texts in `data/mystery_texts/`
3. Use UTF-8 encoded plain text files