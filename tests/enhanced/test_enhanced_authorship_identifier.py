import unittest
import os
import tempfile
from src.enhanced.enhanced_authorship_identifier import (
    clean_word,
    average_word_length,
    different_to_total,
    exactly_once_to_total,
    split_string,
    get_sentences,
    average_sentence_length,
    get_phrases,
    average_sentence_complexity,
    punctuation_density,
    stopword_ratio,
    make_signature,
    get_all_signatures,
    get_score,
    lowest_score,
    process_data,
)


class TestEnhancedAuthorshipIdentifier(unittest.TestCase):

    def setUp(self):
        """Set up temporary directories and files for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.known_dir = os.path.join(self.temp_dir.name, "known")
        os.makedirs(self.known_dir)
        self.mystery_file = os.path.join(self.temp_dir.name, "mystery.txt")

        # Create known author files
        with open(os.path.join(self.known_dir, "author1.txt"), "w") as f:
            f.write("A pearl! Pearl! Lustrous pearl! Rare. What a nice find.")
        with open(os.path.join(self.known_dir, "author2.txt"), "w") as f:
            f.write("Lustrous pearl, Rare, What a nice find.")

        # Create mystery file
        with open(self.mystery_file, "w") as f:
            f.write("Lustrous pearl, Rare, What a nice find.")

    def tearDown(self):
        """Clean up temporary directories and files."""
        self.temp_dir.cleanup()

    def test_clean_word(self):
        self.assertEqual(clean_word("Pearl!"), "pearl")
        self.assertEqual(clean_word("card-board"), "card-board")
        self.assertEqual(clean_word("...hello..."), "hello")

    def test_average_word_length(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        self.assertAlmostEqual(average_word_length(text), 4.1, places=1)

    def test_different_to_total(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        self.assertAlmostEqual(different_to_total(text), 0.7, places=1)

    def test_exactly_once_to_total(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        self.assertAlmostEqual(exactly_once_to_total(text), 0.5, places=1)

    def test_split_string(self):
        self.assertEqual(split_string("one*two[three", "*["), ["one", "two", "three"])
        self.assertEqual(
            split_string(
                "A pearl! Pearl! Lustrous pearl! Rare. What a nice find.", ".?!"
            ),
            ["A pearl", "Pearl", "Lustrous pearl", "Rare", "What a nice find"],
        )

    def test_get_sentences(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        self.assertEqual(
            get_sentences(text),
            ["A pearl", "Pearl", "Lustrous pearl", "Rare", "What a nice find"],
        )

    def test_average_sentence_length(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        self.assertAlmostEqual(average_sentence_length(text), 2.0, places=1)

    def test_get_phrases(self):
        text = "Lustrous pearl, Rare, What a nice find"
        self.assertEqual(
            get_phrases(text), ["Lustrous pearl", "Rare", "What a nice find"]
        )

    def test_average_sentence_complexity(self):
        text1 = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        text2 = "A pearl! Pearl! Lustrous pearl! Rare, what a nice find."
        self.assertAlmostEqual(average_sentence_complexity(text1), 1.0, places=1)
        self.assertAlmostEqual(average_sentence_complexity(text2), 1.25, places=1)

    def test_punctuation_density(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        self.assertAlmostEqual(punctuation_density(text), 0.5, places=1)  # Adjusted value

    def test_stopword_ratio(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare. What a nice find."
        self.assertAlmostEqual(stopword_ratio(text), 0.2, places=1)  # Adjusted value

    def test_make_signature(self):
        text = "A pearl! Pearl! Lustrous pearl! Rare, what a nice find."
        expected_signature = [4.1, 0.7, 0.5, 2.5, 1.25, 0.5, 0.2]  # Adjusted values
        result = make_signature(text)
        for i in range(len(expected_signature)):
            self.assertAlmostEqual(result[i], expected_signature[i], places=1)
        
    def test_get_all_signatures(self):
        signatures = get_all_signatures(self.known_dir)
        self.assertEqual(len(signatures), 2)
        self.assertIn("author1.txt", signatures)
        self.assertIn("author2.txt", signatures)

    def test_get_score(self):
        signature1 = [4.6, 0.1, 0.05, 10, 2, 0.2, 0.3]
        signature2 = [4.3, 0.1, 0.04, 16, 4, 0.1, 0.5]
        weights = [11, 33, 50, 0.4, 4, 2, 3]
        self.assertAlmostEqual(
            get_score(signature1, signature2, weights), 14.999999999999998, places=1
        )
    
    def test_lowest_score(self):
        signatures_dict = {
            "Dan": [1, 1, 1, 1, 1, 0.2, 0.3],
            "Leo": [3, 3, 3, 3, 3, 0.5, 0.7],
        }
        unknown_signature = [1, 0.8, 0.9, 1.3, 1.4, 0.1, 0.5]
        weights = [11, 33, 50, 0.4, 4, 2, 3]
        self.assertEqual(
            lowest_score(signatures_dict, unknown_signature, weights), "Dan"
        )

    def test_process_data(self):
        result = process_data(self.mystery_file, self.known_dir)
        self.assertEqual(result, "author2.txt")


if __name__ == "__main__":
    unittest.main()
