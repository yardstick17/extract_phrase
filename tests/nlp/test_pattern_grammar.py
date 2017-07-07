#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TestCase

from nltk import RegexpParser

from nlp.pattern_grammer import PatternGrammar


class TestPatternGrammar(TestCase):
    def setUp(self):
        self.pattern_grammar_obj = PatternGrammar()
        self.clause = 'NN_all'

    def test_noun_and_adj_phrases(self):
        noun_phrase_extractor = self.pattern_grammar_obj.noun_and_adj_phrases
        expected_dict = {
            'NN_all': """NP: {(<FW|NN|NN.>+<JJ|JJ.|VB|VB.>?)+<JJ|JJ.|VB|VB.>*<NN|NN.>+}""",
            'NN_CC_JJ_multi': """NP:     { (<,|CC>*<JJ|JJ.>+<NN|NN.>+)+ }""",
        }
        self.assertDictEqual(expected_dict, noun_phrase_extractor)

    def test_get_key_clause_grammar(self):
        grammar = self.pattern_grammar_obj.get_key_clause_grammar(self.clause)
        self.assertIsInstance(grammar, RegexpParser)

    def test_get_noun_and_adj_phrases_grammar(self):
        compiled_grammar = self.pattern_grammar_obj.get_noun_and_adj_phrases_grammar(self.clause)
        self.assertIsInstance(compiled_grammar, RegexpParser)
