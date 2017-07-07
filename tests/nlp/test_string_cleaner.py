#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TestCase

from nlp.string_cleaner import StringCleaner


class TestStringCleaner(TestCase):
    def setUp(self):
        self.unicode_string = 'áƒ˙˙ƒ∂√≈food was ç∂aßmç√∫˙¥amazing!!†©ƒ´ß. The place was ƒ©∂ good.'
        self.whitespace_word = 'aam      aadmi party '
        self.special_char_word = '##gali mohalle ke >>ladke<<??'

    def test_clean(self):
        clean_str = StringCleaner.clean(self.unicode_string)
        exptected_clean_str = 'a food was camc amazing! . the place was good.'
        print('#', clean_str, '#')
        self.assertEqual(exptected_clean_str, clean_str)

    def test__unicode_normalizer(self):
        """
        Should private method be tested ?
        Returns:

        """
        unicode_normalized_string = StringCleaner._unicode_normalizer(self.unicode_string)
        exptected_unicode_normalized_string = 'a  food was camc amazing!! . the place was  good.'
        self.assertEqual(unicode_normalized_string, exptected_unicode_normalized_string)

    def test_make_string_alphanumeric(self):
        alphanumneric_string = StringCleaner.make_string_alphanumeric(self.unicode_string)
        expected_string = 'food was amamazing. The place was  good.'
        self.assertEqual(alphanumneric_string, expected_string)


class TestRemoveMultipleWhitespace(TestCase):
    def test_clean_word_space_both(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace(' beer '), 'beer')

    def test_clean_word_space_right(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace('beer '), 'beer')

    def test_clean_word_space_left(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace(' beer'), 'beer')

    def test_clean_word_upper_start(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace('Beer'), 'beer')

    def test_clean_word_upper_middle(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace('bEEr'), 'beer')

    def test_clean_word_upper_and_spaces(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace(' BEEr'), 'beer')

    def test_clean_word_upper_and_spaces_and_multi_word(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace(' Brown Beer '), 'brown beer')

    def test_clean_word_multi_word_with_spaces_between(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace(' Brown  Beer '), 'brown beer')

    def test_clean_word_empty(self):
        self.assertEqual(StringCleaner.remove_multiple_whitespace(' '), '')
