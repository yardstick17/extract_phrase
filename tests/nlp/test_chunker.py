#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TestCase

import nltk

from nlp import chunker
from nlp.chunker import Chunker
from nlp.pattern_grammer import PatternGrammar


class TestChunker(TestCase):
    def setUp(self):
        compiled_grammar = PatternGrammar().init_all_clause()
        testing_clauses = ['NN_all', 'NN_CC_JJ_multi']
        self.sentence = 'chicken biryani was awesome.'
        self.pos_tagged_sentence = [('the', 'DT'), ('great', 'NN'), ('place', 'NN'), ('was', 'VBD'), ('amazing', 'VBG')]
        self.grammar = compiled_grammar[testing_clauses[0]]
        self.chunker_obj = Chunker(self.grammar)

    def test_chunk_sentence(self):
        extracted_chunk = self.chunker_obj.chunk_sentence(sentence=self.sentence)
        expected_chunk = {'NP': [[('chicken', 'NN'), ('biryani', 'NN')]]}
        self.assertDictEqual(extracted_chunk, expected_chunk)

    def test_chunk_pos_tagged_sentence(self):
        extracted_chunk = self.chunker_obj.chunk_pos_tagged_sentence(pos_tagged_sentence=self.pos_tagged_sentence)
        expected_chunk = {'NP': [[('great', 'NN'), ('place', 'NN')]]}
        self.assertDictEqual(extracted_chunk, expected_chunk)

    def test_extract_rule_and_chunk(self):
        chunked_tree = self.grammar.parse(self.pos_tagged_sentence)
        extracted_dict = self.chunker_obj.extract_rule_and_chunk(chunked_tree)
        expected_chunk_dict = {'NP': [[('great', 'NN'), ('place', 'NN')]]}
        self.assertDictEqual(extracted_dict, expected_chunk_dict)
