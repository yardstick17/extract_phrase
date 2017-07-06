#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import unicodedata

PATTERN_MULTIPLE_DOTS = re.compile(r'\.\.+')
PATTERN_SINGLE_DOT = re.compile(r'\.')
PATTERN_SLASH = re.compile(r'\:+')
PATTERN_ARROW = re.compile(r'\>\>+')
PATTERN_EXCLAMATION = re.compile(r'\!\!+')
PATTERN_COMMA = re.compile(r'\,\,+')
MULTIPLE_WHITESPACE_REGEX = re.compile(r'\s+')

READ_TEXT_CHARS = re.compile('[^a-zA-Z\.\,\s]')


class StringCleaner:
    @staticmethod
    def clean(string):
        unicode_cleaned_string = StringCleaner._unicode_normalizer(string)
        cleaned_string = StringCleaner._remove_multiple_special_chars(unicode_cleaned_string)
        white_space_removed_string = StringCleaner.remove_multiple_whitespace(cleaned_string)
        return white_space_removed_string

    @staticmethod
    def _unicode_normalizer(string):
        return unicodedata.normalize('NFKD', string).encode(
            'ascii', 'ignore').lower().decode('utf-8')

    @staticmethod
    def _remove_multiple_special_chars(string):
        # FIXME : this function is not working as exoected
        """ Removes multiple occurrence of special characters.
        """
        text = PATTERN_MULTIPLE_DOTS.sub('.', string)
        text = PATTERN_SINGLE_DOT.sub('. ', text)
        text = PATTERN_SLASH.sub(' ', text)
        text = PATTERN_ARROW.sub('>', text)
        text = PATTERN_EXCLAMATION.sub('!', text)
        text = PATTERN_COMMA.sub(',', text)
        return text

    @staticmethod
    def remove_multiple_whitespace(word):
        # FIXME : This fuction is not working as expected !!!
        """

         Use this method whenever comparing or making a word list for filtering"""
        return MULTIPLE_WHITESPACE_REGEX.sub(' ', word.lower().strip())

    @staticmethod
    def make_string_alphanumeric(word):
        """
        make string of readable chars only
        Args:
            word:  "áƒ˙˙ƒ∂√≈food was ç∂aßmç√∫˙¥azing!!†©ƒ´ß "

        Returns: "food was amazing"

        """
        return READ_TEXT_CHARS.sub('', word)
