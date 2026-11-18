import unittest

import tags


class TagParsingRegression(unittest.TestCase):
    def test_keeps_both_tags(self) -> None:
        self.assertEqual(tags.split_tags("alpha, beta"), ["alpha", "beta"])

    def test_strips_empty_segments(self) -> None:
        self.assertEqual(tags.split_tags(" alpha , , beta "), ["alpha", "beta"])

    def test_empty_input(self) -> None:
        self.assertEqual(tags.split_tags(""), [])


if __name__ == "__main__":
    unittest.main()
